"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/weather_data.py
ROLE         : Orchestration météo pour le widget dashboard (consentement, code postal
                par défaut du profil, cache, appel réseau)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Point d'entrée unique appelé par AlfredDesktopAPI. Tant que le consentement
(src/ui/weather_prefs.py) n'est pas activé, aucun appel réseau n'est fait —
même logique de "porte" que emotion_override_prefs.py pour la désactivation
de l'estimation émotionnelle, mais ici la porte est fermée par défaut.

Code postal par défaut : extrait du champ libre "localite" de
data/profile/identity_{USER_ID}.json (ex. "45300 Manchecourt, Loiret" ->
"45300"), sauf si l'utilisateur a cherché un autre code postal (auquel cas
weather_prefs.last_postal_code prend le dessus jusqu'à un reset explicite).

Cache mémoire de 20 minutes par code postal — la météo ne change pas assez
vite pour justifier un appel à chaque rafraîchissement du dashboard (25s),
et geo.api.gouv.fr / open-meteo.com sont des services publics gratuits à
ne pas solliciter inutilement.
"""

from __future__ import annotations

import json
import time

_CACHE_TTL_SECONDS = 20 * 60
_cache: dict[str, tuple[float, dict]] = {}


def _default_location() -> tuple[str | None, str | None]:
    """Code postal + indice de commune (désambiguïsation) depuis le profil utilisateur."""
    try:
        from paths import PATHS
        from src.integrations.weather_client import extract_postal_code, extract_commune_hint

        identity_file = PATHS.data_profile / "identity_celine.json"
        if not identity_file.exists():
            return None, None
        data = json.loads(identity_file.read_text(encoding="utf-8"))
        localite = data.get("identity", {}).get("localite", "")
        return extract_postal_code(localite), extract_commune_hint(localite)
    except Exception:
        return None, None


def _fetch_cached(postal_code: str, commune_hint: str | None = None) -> dict:
    now = time.time()
    cached = _cache.get(postal_code)
    if cached and (now - cached[0]) < _CACHE_TTL_SECONDS:
        return cached[1]

    from src.integrations.weather_client import get_weather_for_postal_code, WeatherError

    try:
        result = get_weather_for_postal_code(postal_code, commune_hint=commune_hint)
        result_out = {"ok": True, **result}
    except WeatherError as exc:
        result_out = {"ok": False, "error": str(exc)}
    _cache[postal_code] = (now, result_out)
    return result_out


def get_weather_state() -> dict:
    """État complet pour le widget dashboard — une seule méthode à appeler côté JS."""
    from src.ui.weather_prefs import load_weather_prefs

    prefs = load_weather_prefs()
    if not prefs["consent"]:
        return {"consent": False}

    is_override = prefs.get("last_postal_code") is not None
    if is_override:
        postal_code, commune_hint = prefs["last_postal_code"], None
    else:
        postal_code, commune_hint = _default_location()

    if not postal_code:
        return {"consent": True, "no_location": True}

    result = _fetch_cached(postal_code, commune_hint=commune_hint)
    return {"consent": True, "no_location": False, "is_override": is_override, **result}


def set_weather_consent(enabled: bool) -> dict:
    from src.ui.weather_prefs import set_consent

    set_consent(enabled)
    return get_weather_state()


def search_weather(postal_code: str) -> dict:
    """Cherche la météo d'un autre code postal et le retient comme override persistant."""
    from src.ui.weather_prefs import set_last_postal_code, load_weather_prefs

    postal_code = (postal_code or "").strip()
    if not load_weather_prefs()["consent"]:
        return {"consent": False}

    if not postal_code.isdigit() or len(postal_code) != 5:
        return {"consent": True, "no_location": False, "is_override": True,
                "ok": False, "error": f"« {postal_code} » n'est pas un code postal valide (5 chiffres)."}

    set_last_postal_code(postal_code)
    return get_weather_state()


def reset_weather_location() -> dict:
    """Revient à la localisation du profil (supprime l'override de code postal)."""
    from src.ui.weather_prefs import set_last_postal_code

    set_last_postal_code(None)
    return get_weather_state()
