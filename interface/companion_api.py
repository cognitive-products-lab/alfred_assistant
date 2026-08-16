"""
PROJECT      : ALFRED
BLOCK        : B24
FUNCTION     : 24.02 — Intégration API compagnon
FILE         : interface/companion_api.py
ROLE         : API locale consommée par le PoC Compagnon ALFRED_ANDROID
               (GET /api/status, GET /api/notifications) + dispatcher RPC
               générique (POST /api/rpc) et hébergement statique de
               interface/desktop_ui/ (/ui/) pour le pont window.AlfredBridge
               (voir index.html) — permet à une WebView Android de charger
               l'interface complète d'ALFRED PC, pas seulement le PoC natif.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-13
UPDATED      : 2026-08-14 — /api/rpc générique + /ui/ statique + run_server_in_thread()
                (appelé depuis src/alfred_desktop.py pour partager le pipeline live —
                nécessaire pour que send_message obtienne de vraies réponses)
VERSION      : V1.2
STATUS       : CODÉ — /api/status et /api/notifications testés en conditions réelles
                (cf. ALFRED_ANDROID/README.md) ; /api/rpc et /ui/ codés, pas encore
                testés avec un vrai client Android (WebView)

DESCRIPTION :
Ré-implémentation de l'API compagnon documentée dans ALFRED_ANDROID/README.md mais
absente du dépôt (point C4-F du plan d'action du 13/07/2026). Contrat calqué
exactement sur le client Android existant :
  - CompanionApiService.kt  : GET /api/status, GET /api/notifications,
                              header Authorization envoyé par le client
  - Models.kt               : StatusResponse{product,status,timestamp},
                              Reminder{id,title,due_at,recurrent,active},
                              NotificationsResponse{notifications}
  - CompanionViewModel.kt   : authHeader = "Bearer ${token}"

Authentification : jeton statique COMPANION_API_TOKEN (.env), comparé en
temps constant (hmac.compare_digest) pour éviter une attaque par timing.
Réutilise le moteur de rappels existant (src/v3/proactive/reminder_engine.py)
comme source des notifications — aucune nouvelle collecte de données créée.

⚠️ Écoute sur 0.0.0.0 par choix : nécessaire pour être joignable depuis
l'émulateur Android (10.0.2.2) ou un téléphone physique sur le même réseau
Wi-Fi local. Ne jamais exposer ce port au-delà du réseau local (jeton
statique — cf. limites documentées dans ALFRED_ANDROID/README.md).

TLS : si data/security/certs/companion_api/{server.crt,server.key} existent
(générés par tools/security/generate_local_tls_cert.py), le serveur démarre
en HTTPS. Sinon, avertissement explicite et démarrage en HTTP (pas de
régression silencieuse pour un poste où le certificat n'a pas encore été
généré). Le certificat est auto-signé et local — le client ALFRED_ANDROID
doit embarquer le .crt correspondant comme ancre de confiance
(network_security_config.xml) pour que la connexion aboutisse. JWT reste
hors scope de ce durcissement (cf. docs/mobilite/vision_mobilite_v2.md).

USAGE :
    python interface/companion_api.py
    (ou start_companion_api.bat sous Windows)
"""

from __future__ import annotations

import hmac
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException

ROOT = Path(__file__).resolve().parents[1]
# Nécessaire pour `from src...` (get_notifications, /api/rpc) quand ce fichier
# est lancé directement (python interface/companion_api.py) : sys.path[0] est
# alors le dossier interface/, pas la racine du projet — même correctif que
# src/alfred_desktop.py.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

COMPANION_API_HOST = "0.0.0.0"
COMPANION_API_PORT = 8420

TLS_CERT_PATH = ROOT / "data" / "security" / "certs" / "companion_api" / "server.crt"
TLS_KEY_PATH = ROOT / "data" / "security" / "certs" / "companion_api" / "server.key"


def _tls_kwargs() -> dict:
    """Active HTTPS si le certificat local existe, sinon retombe sur HTTP (avec avertissement)."""
    if TLS_CERT_PATH.exists() and TLS_KEY_PATH.exists():
        return {"ssl_certfile": str(TLS_CERT_PATH), "ssl_keyfile": str(TLS_KEY_PATH)}
    print(
        "[ALFRED] ATTENTION : certificat TLS local introuvable "
        f"({TLS_CERT_PATH}) — démarrage en HTTP non chiffré. "
        "Générer avec : python tools/security/generate_local_tls_cert.py"
    )
    return {}

app = FastAPI(title="ALFRED Companion API", version="1.0.0")


def _expected_token() -> str:
    token = os.getenv("COMPANION_API_TOKEN", "")
    if not token:
        raise RuntimeError(
            "COMPANION_API_TOKEN manquant dans .env — générer avec : "
            "python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    return token


def _require_token(authorization: str | None) -> None:
    expected = f"Bearer {_expected_token()}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="Jeton invalide ou manquant")


def _require_token_qs(token: str | None) -> None:
    """Variante pour /api/events : EventSource ne permet pas d'en-tête
    Authorization, le jeton passe donc en query string pour cet endpoint
    précis (même modèle de menace que le jeton statique déjà utilisé
    ailleurs : réseau local, TLS optionnel — voir en-tête de fichier)."""
    expected = _expected_token()
    if not token or not hmac.compare_digest(token, expected):
        raise HTTPException(status_code=401, detail="Jeton invalide ou manquant")


# ============================================================
# Évènements temps réel (réponses, streaming, visèmes...) — diffusés par
# src/alfred_desktop.py::_push() vers tout client SSE connecté, en plus de
# l'appel evaluate_js() historique vers la fenêtre pywebview.
# ============================================================

import queue  # noqa: E402
import threading  # noqa: E402

_event_subscribers: list[queue.Queue] = []
_event_subscribers_lock = threading.Lock()


def broadcast_event(js_call: str, *args) -> None:
    """Pousse un évènement pipeline (onResponse, onThinking, ...) vers tous
    les clients SSE connectés — voir window.__alfredBridge côté JS."""
    message = {"event": js_call, "args": list(args)}
    with _event_subscribers_lock:
        subs = list(_event_subscribers)
    for q in subs:
        try:
            q.put_nowait(message)
        except Exception:
            pass


# ============================================================
# Audio TTS pour clients distants — PiperTTS joue nativement sur les
# haut-parleurs du PC (sounddevice) et n'envoie jamais le son lui-même aux
# clients distants (WebView Android, navigateur) ; seul cet unique dernier
# WAV généré est exposé ici, pour lecture côté client (voir onAudioReady
# dans interface/desktop_ui/index.html). Pas d'historique : un seul buffer
# "dernier son", écrasé à chaque nouvelle phrase — suffisant car le client
# le récupère dès l'évènement onAudioReady, avant la phrase suivante.
# ============================================================

_latest_tts_audio: bytes | None = None
_latest_tts_audio_lock = threading.Lock()


def set_latest_tts_audio(wav_bytes: bytes) -> None:
    global _latest_tts_audio
    with _latest_tts_audio_lock:
        _latest_tts_audio = wav_bytes


@app.get("/api/tts_audio/latest")
def get_latest_tts_audio(authorization: str | None = Header(default=None)):
    _require_token(authorization)
    with _latest_tts_audio_lock:
        audio = _latest_tts_audio
    if audio is None:
        raise HTTPException(status_code=404, detail="Aucun audio TTS disponible")
    from fastapi.responses import Response

    return Response(content=audio, media_type="audio/wav")


@app.get("/api/status")
def get_status(authorization: str | None = Header(default=None)) -> dict:
    _require_token(authorization)
    return {
        "product": "ALFRED",
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/notifications")
def get_notifications(authorization: str | None = Header(default=None)) -> dict:
    _require_token(authorization)
    from src.v3.proactive.reminder_engine import ReminderEngine

    engine = ReminderEngine()
    reminders = engine.get_active()
    return {
        "notifications": [
            {
                "id": r.id,
                "title": r.title,
                "due_at": r.due_at,
                "recurrent": r.recurrent,
                "active": r.active,
            }
            for r in reminders
        ]
    }


_RPC_METHODS: tuple[str, ...] = (
    # Mêmes noms que les méthodes de AlfredDesktopAPI (src/alfred_desktop.py) —
    # whitelist stricte : seuls ces noms peuvent être invoqués via /api/rpc,
    # jamais un attribut arbitraire de l'instance.
    "send_message", "get_settings", "save_setting",
    "get_recommandations", "get_emotion_state", "set_emotion_override", "correct_emotion",
    "get_planning", "get_devices", "get_activite", "get_kpis", "get_notifications",
    "get_context_consent", "set_context_consent",
    "run_backup", "summarize_today", "search_knowledge",
    "get_weather", "set_weather_consent", "search_weather", "reset_weather_location",
    "get_calendar_events", "set_calendar_consent", "get_google_auth_status",
    "start_google_auth", "disconnect_google_calendar", "create_calendar_event",
    "get_home_devices", "set_home_consent", "set_home_project_id",
    "get_home_auth_url", "submit_home_auth_code", "disconnect_home", "execute_home_command",
)

_api_instance = None  # instancié à la 1ère requête (import différé, évite le cycle avec src.alfred_desktop)


def _get_api_instance():
    global _api_instance
    if _api_instance is None:
        from src.alfred_desktop import AlfredDesktopAPI

        _api_instance = AlfredDesktopAPI()
    return _api_instance


@app.post("/api/rpc")
def rpc(payload: dict, authorization: str | None = Header(default=None)) -> dict:
    """
    Dispatcher générique consommé par le pont JS window.AlfredBridge (interface/
    desktop_ui/index.html) quand la page ne tourne pas dans la fenêtre pywebview.
    Body : {"method": "get_kpis", "args": {}}. Réutilise exactement les mêmes
    fonctions que le pont pywebview.api — aucune logique dupliquée.
    """
    _require_token(authorization)
    method = payload.get("method")
    args = payload.get("args") or {}
    if not isinstance(method, str) or method not in _RPC_METHODS:
        raise HTTPException(status_code=404, detail=f"Méthode RPC inconnue : {method!r}")
    if not isinstance(args, dict):
        raise HTTPException(status_code=400, detail="'args' doit être un objet")

    if method == "send_message":
        # Tout appel /api/rpc vient par définition d'un client distant (WebView
        # Android, navigateur) — jamais de la fenêtre pywebview locale, qui
        # appelle window.pywebview.api directement. Détermine quelle interface
        # joue l'audio TTS de la réponse (voir src/main.py, tts_piper.py::speak).
        args = {**args, "origin": "remote"}

    api = _get_api_instance()
    func = getattr(api, method)
    try:
        result = func(**args)
    except TypeError as exc:
        raise HTTPException(status_code=400, detail=f"Arguments invalides pour {method} : {exc}") from exc
    except Exception as exc:  # noqa: BLE001 — remonté tel quel au client distant, journalisé côté serveur
        print(f"[ALFRED] Erreur RPC {method}: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"ok": True, "result": result}


@app.get("/api/events")
async def events(token: str | None = None):
    """
    Flux SSE des évènements pipeline (onResponse, onThinking, onStreamPhrase,
    onSpeaking, onListening, onVoiceError, onVisemes) — consommé par le pont
    window.AlfredBridge côté JS pour afficher les vraies réponses en mode
    texte/vocal distant. Sans ce flux, /api/rpc::send_message envoie bien le
    message mais la réponse ne s'affiche jamais côté client distant.
    """
    _require_token_qs(token)
    import asyncio
    import json as _json

    q: queue.Queue = queue.Queue()
    with _event_subscribers_lock:
        _event_subscribers.append(q)

    async def stream():
        try:
            while True:
                try:
                    item = await asyncio.get_event_loop().run_in_executor(None, q.get, True, 15)
                    yield f"data: {_json.dumps(item, ensure_ascii=False)}\n\n"
                except queue.Empty:
                    yield ": keep-alive\n\n"
        finally:
            with _event_subscribers_lock:
                if q in _event_subscribers:
                    _event_subscribers.remove(q)

    from fastapi.responses import StreamingResponse

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# Sert interface/desktop_ui/ (utilisé par ALFRED PC lui-même via pywebview en
# file://, mais aussi par toute WebView/navigateur distant — ex. ALFRED_ANDROID)
# sous /ui/. Monté après les routes /api/* pour ne jamais les masquer.
from fastapi.staticfiles import StaticFiles  # noqa: E402

app.mount(
    "/ui",
    StaticFiles(directory=str(ROOT / "interface" / "desktop_ui"), html=True),
    name="ui",
)


def run_server_in_thread() -> None:
    """
    Démarre ce serveur (API + /ui/ statique) dans un thread daemon du process
    appelant, au lieu d'un process séparé — nécessaire pour que /api/rpc partage
    le même pipeline ALFRED (ui_bridge, hooks onResponse/...) que la fenêtre
    pywebview. Voir src/alfred_desktop.py.
    """
    import threading

    import uvicorn

    _expected_token()
    tls_kwargs = _tls_kwargs()
    scheme = "https" if tls_kwargs else "http"

    def _serve() -> None:
        print(f"[ALFRED] API + interface distante sur {scheme}://{COMPANION_API_HOST}:{COMPANION_API_PORT}/ui/")
        uvicorn.run(app, host=COMPANION_API_HOST, port=COMPANION_API_PORT, log_level="warning", **tls_kwargs)

    threading.Thread(target=_serve, name="alfred-api-server", daemon=True).start()


if __name__ == "__main__":
    import uvicorn

    _expected_token()  # échoue tôt et clairement si le jeton n'est pas configuré
    tls_kwargs = _tls_kwargs()
    scheme = "https" if tls_kwargs else "http"
    print(f"[ALFRED] API compagnon sur {scheme}://{COMPANION_API_HOST}:{COMPANION_API_PORT}")
    print(f"[ALFRED] Emulateur Android : {scheme}://10.0.2.2:8420")
    uvicorn.run(app, host=COMPANION_API_HOST, port=COMPANION_API_PORT, **tls_kwargs)
