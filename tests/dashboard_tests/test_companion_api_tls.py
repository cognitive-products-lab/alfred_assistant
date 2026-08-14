"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B24
FUNCTION     : 24.03 — Certificat TLS local pour l'API compagnon
FILE         : tests/dashboard_tests/test_companion_api_tls.py
ROLE         : Vérifie un VRAI handshake TLS de bout en bout sur
               interface/companion_api.py (pas un TestClient in-process —
               un socket réel, un certificat réel, un client HTTPS réel).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
test_companion_api.py (FastAPI TestClient) ne passe jamais par un vrai socket
TLS. Ce fichier démarre un vrai serveur uvicorn HTTPS dans un thread, avec le
certificat généré par tools/security/generate_local_tls_cert.py, et vérifie
qu'un client HTTPS réel (requests, verify=server.crt) obtient une réponse
200 — preuve que le certificat est valide et que la connexion est chiffrée,
pas seulement que le fichier .crt existe sur disque.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import os
import threading
import time

import pytest

pytest.importorskip("fastapi")
requests = pytest.importorskip("requests")
uvicorn = pytest.importorskip("uvicorn")

os.environ.setdefault("COMPANION_API_TOKEN", "test-token-companion-api-tls")

from interface.companion_api import TLS_CERT_PATH, TLS_KEY_PATH, app  # noqa: E402


def _expected_token() -> str:
    """
    Lue au moment de l'appel (pas une constante figee a l'import) : d'autres
    modules de test importes dans la meme session pytest (ex.
    test_companion_api.py) peuvent ecraser cette variable d'environnement
    globale APRES notre propre setdefault(), selon l'ordre de collecte.
    La collecte de tous les modules se termine avant l'execution du premier
    test, donc lire la valeur depuis l'interieur de la fonction de test
    (plutot qu'a l'import) garantit qu'on s'aligne toujours sur la valeur
    reellement active au moment de la requete, quel que soit l'ordre.
    """
    return os.environ["COMPANION_API_TOKEN"]

pytestmark = pytest.mark.skipif(
    not (TLS_CERT_PATH.exists() and TLS_KEY_PATH.exists()),
    reason=(
        "Certificat TLS local absent — generer avec : "
        "python tools/security/generate_local_tls_cert.py"
    ),
)

HOST = "127.0.0.1"
PORT = 8421  # port dedie aux tests, distinct du port de prod 8420


@pytest.fixture(scope="module")
def live_https_server():
    config = uvicorn.Config(
        app,
        host=HOST,
        port=PORT,
        ssl_certfile=str(TLS_CERT_PATH),
        ssl_keyfile=str(TLS_KEY_PATH),
        log_level="warning",
    )
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 5
    while not server.started and time.time() < deadline:
        time.sleep(0.05)
    assert server.started, "Le serveur uvicorn HTTPS n'a pas demarre a temps"

    yield f"https://{HOST}:{PORT}"

    server.should_exit = True
    thread.join(timeout=5)


def test_https_handshake_and_status_with_valid_token(live_https_server):
    response = requests.get(
        f"{live_https_server}/api/status",
        headers={"Authorization": f"Bearer {_expected_token()}"},
        verify=str(TLS_CERT_PATH),
        timeout=5,
    )
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"product", "status", "timestamp"}


def test_https_rejects_invalid_token(live_https_server):
    response = requests.get(
        f"{live_https_server}/api/status",
        headers={"Authorization": "Bearer wrong-token"},
        verify=str(TLS_CERT_PATH),
        timeout=5,
    )
    assert response.status_code == 401


def test_plain_http_request_to_https_port_fails(live_https_server):
    """Confirme que le port ne parle plus HTTP en clair une fois TLS actif."""
    http_url = live_https_server.replace("https://", "http://")
    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get(f"{http_url}/api/status", timeout=3)
