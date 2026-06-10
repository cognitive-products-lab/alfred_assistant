"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.06
FILE         : network_security.py
ROLE         : Sécurité réseau — filtrage IP, anti-SSRF, TLS

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

UPDATED      : 2026-06-01
VERSION      : V1.1
STATUS       : ACTIVE

UPDATED      : 2026-06-01
VERSION      : V1.2
STATUS       : ACTIVE

DESCRIPTION :
V1.2 : TLS certificate validation, DNS domain reputation filtering,
rate-limiting par IP source, load_network_policy depuis JSON.
Rétrocompatible V1.1.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations
"""
network_security.py
Bloc 20.06 — Sécurité réseau pour ALFRED.

Rôle :
- filtrage IP (allowlist / blocklist) ;
- prévention SSRF (URLs privées / locales interdites) ;
- détection d'anomalies réseau (connexions répétées, plage inconnue) ;
- validation TLS basique pour les requêtes sortantes.

Local-first : aucune dépendance réseau externe.
"""


import ipaddress
import json
import re
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

from src.security.security_logger import log_event
from src.security.incident_manager import register_incident

_lock = threading.Lock()
_connection_log: dict[str, list[float]] = {}

WINDOW_SECONDS = 60
MAX_CONNECTIONS_PER_WINDOW = 30

_ROOT         = Path(__file__).resolve().parents[2]
_NET_CONFIG   = _ROOT / "config" / "security" / "network_policy.json"

# Plages privées/locales interdites dans les URLs (anti-SSRF)
_PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]

# IP explicitement bloquées — chargées depuis config/security/network_policy.json
_IP_BLOCKLIST: set[str] = set()

# IP explicitement autorisées — vide = tout le monde passe si non bloqué
_IP_ALLOWLIST: set[str] = set()


def load_network_policy(path: Path | None = None) -> dict:
    """
    Charge la politique réseau depuis un fichier JSON.
    Format attendu :
      {
        "blocklist": ["1.2.3.4", "5.6.7.8"],
        "allowlist": [],
        "max_connections_per_window": 30,
        "window_seconds": 60
      }
    Retourne un dict avec les listes chargées.
    """
    global MAX_CONNECTIONS_PER_WINDOW, WINDOW_SECONDS

    config_path = path or _NET_CONFIG
    if not config_path.exists():
        return {"blocklist": [], "allowlist": [], "loaded": False}

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
        with _lock:
            _IP_BLOCKLIST.update(data.get("blocklist", []))
            _IP_ALLOWLIST.update(data.get("allowlist", []))
        if "max_connections_per_window" in data:
            MAX_CONNECTIONS_PER_WINDOW = int(data["max_connections_per_window"])
        if "window_seconds" in data:
            WINDOW_SECONDS = int(data["window_seconds"])
        log_event(
            f"network_security: policy chargée — "
            f"blocklist={len(_IP_BLOCKLIST)} allowlist={len(_IP_ALLOWLIST)}",
            "INFO",
        )
        return {"blocklist": list(_IP_BLOCKLIST), "allowlist": list(_IP_ALLOWLIST),
                "loaded": True}
    except Exception as exc:
        log_event(f"network_security: impossible de charger la policy — {exc}", "ERROR")
        return {"blocklist": [], "allowlist": [], "loaded": False, "error": str(exc)}


def save_network_policy(path: Path | None = None) -> bool:
    """Sauvegarde la politique réseau courante en JSON."""
    config_path = path or _NET_CONFIG
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with _lock:
            data = {
                "blocklist": sorted(_IP_BLOCKLIST),
                "allowlist": sorted(_IP_ALLOWLIST),
                "max_connections_per_window": MAX_CONNECTIONS_PER_WINDOW,
                "window_seconds": WINDOW_SECONDS,
            }
        config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return True
    except Exception as exc:
        log_event(f"network_security: impossible de sauvegarder la policy — {exc}", "ERROR")
        return False


# Chargement automatique au démarrage si le fichier existe
load_network_policy()


def _is_private_ip(ip_str: str) -> bool:
    """Retourne True si l'IP appartient à une plage privée/locale."""
    try:
        addr = ipaddress.ip_address(ip_str)
        return any(addr in net for net in _PRIVATE_NETWORKS)
    except ValueError:
        return False


def check_ip(ip: str) -> dict:
    """
    Vérifie si une IP est autorisée.

    Returns:
        dict avec allowed (bool) et reason (str).
    """
    if ip in _IP_BLOCKLIST:
        log_event(f"IP bloquée : {ip}", "WARNING")
        return {"allowed": False, "reason": "IP en liste noire"}

    if _IP_ALLOWLIST and ip not in _IP_ALLOWLIST:
        log_event(f"IP non autorisée (hors allowlist) : {ip}", "WARNING")
        return {"allowed": False, "reason": "IP absente de la liste blanche"}

    return {"allowed": True, "reason": "OK"}


def check_url_ssrf(url: str) -> dict:
    """
    Vérifie qu'une URL externe ne pointe pas vers une ressource interne (SSRF).

    Returns:
        dict avec allowed (bool) et reason (str).
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
    except Exception:
        return {"allowed": False, "reason": "URL invalide"}

    if not parsed.scheme in {"http", "https"}:
        log_event(f"Schéma URL interdit : {parsed.scheme} ({url})", "WARNING")
        return {"allowed": False, "reason": f"Schéma interdit : {parsed.scheme}"}

    # Résolution IP directe dans l'URL
    try:
        addr = ipaddress.ip_address(hostname)
        if _is_private_ip(str(addr)):
            log_event(f"SSRF bloqué — IP privée dans URL : {url}", "ERROR")
            register_incident("HIGH", f"Tentative SSRF détectée : {url}", source="network_security")
            return {"allowed": False, "reason": "IP privée dans URL — SSRF bloqué"}
    except ValueError:
        pass

    # Noms d'hôte typiques de la boucle locale
    if hostname in {"localhost", "local", "metadata", "169.254.169.254"}:
        log_event(f"SSRF bloqué — hostname local : {url}", "ERROR")
        register_incident("HIGH", f"Tentative SSRF (hostname local) : {url}", source="network_security")
        return {"allowed": False, "reason": "Hostname local — SSRF bloqué"}

    return {"allowed": True, "reason": "OK"}


def record_connection(source: str) -> None:
    """Enregistre une connexion entrante pour détection d'anomalie."""
    with _lock:
        now = time.time()
        _connection_log.setdefault(source, [])
        _connection_log[source] = [t for t in _connection_log[source] if now - t < WINDOW_SECONDS]
        _connection_log[source].append(now)

        count = len(_connection_log[source])
        if count >= MAX_CONNECTIONS_PER_WINDOW:
            log_event(
                f"Anomalie réseau — connexions excessives depuis {source} "
                f"({count}/{MAX_CONNECTIONS_PER_WINDOW} en {WINDOW_SECONDS}s)",
                "WARNING",
            )
            if count == MAX_CONNECTIONS_PER_WINDOW:
                register_incident(
                    "MEDIUM",
                    f"Connexions excessives depuis {source} ({count} en {WINDOW_SECONDS}s)",
                    source="network_security",
                )


def get_connection_stats(source: str) -> dict:
    """Retourne les stats de connexion pour une source."""
    with _lock:
        now = time.time()
        recent = [t for t in _connection_log.get(source, []) if now - t < WINDOW_SECONDS]
        return {
            "source": source,
            "connections_in_window": len(recent),
            "max_allowed": MAX_CONNECTIONS_PER_WINDOW,
            "window_seconds": WINDOW_SECONDS,
            "anomaly": len(recent) >= MAX_CONNECTIONS_PER_WINDOW,
        }


def add_to_blocklist(ip: str) -> None:
    """Ajoute une IP à la liste noire."""
    _IP_BLOCKLIST.add(ip)
    log_event(f"IP ajoutée à la liste noire : {ip}", "WARNING")


def remove_from_blocklist(ip: str) -> None:
    """Retire une IP de la liste noire."""
    _IP_BLOCKLIST.discard(ip)
    log_event(f"IP retirée de la liste noire : {ip}", "INFO")


def get_network_status() -> dict:
    """Résumé de l'état réseau pour le dashboard."""
    with _lock:
        now = time.time()
        anomalies = [
            src for src, times in _connection_log.items()
            if len([t for t in times if now - t < WINDOW_SECONDS]) >= MAX_CONNECTIONS_PER_WINDOW
        ]
    return {
        "blocklist_size":   len(_IP_BLOCKLIST),
        "allowlist_size":   len(_IP_ALLOWLIST),
        "active_sources":   len(_connection_log),
        "anomalous_sources": anomalies,
        "domain_blocklist": len(_DOMAIN_BLOCKLIST),
        "ip_rate_limited":  len(_IP_RATE_LOCK),
    }


# ─── V1.2 : Rate-limiting par IP source ───────────────────────────────────────

_IP_ATTEMPTS:   dict[str, list[float]] = {}
_IP_RATE_LOCK:  dict[str, float]       = {}
MAX_IP_REQUESTS   = 100    # requêtes max par IP par fenêtre
IP_WINDOW_SECONDS = 60
IP_LOCKOUT_SECONDS = 300   # 5 min de blocage


def check_ip_rate_limit(source_ip: str) -> dict:
    """
    Vérifie le rate limit pour une IP source (protection DDoS/scan).

    Returns:
        dict avec allowed (bool), retry_after (float), reason (str).
    """
    with _lock:
        now = time.time()
        if source_ip in _IP_RATE_LOCK and now < _IP_RATE_LOCK[source_ip]:
            retry = round(_IP_RATE_LOCK[source_ip] - now, 1)
            return {"allowed": False, "retry_after": retry,
                    "reason": f"IP rate-limitée — réessayer dans {retry:.0f}s"}

        _IP_ATTEMPTS.setdefault(source_ip, [])
        _IP_ATTEMPTS[source_ip] = [
            t for t in _IP_ATTEMPTS[source_ip] if now - t < IP_WINDOW_SECONDS
        ]
        _IP_ATTEMPTS[source_ip].append(now)

        count = len(_IP_ATTEMPTS[source_ip])
        if count >= MAX_IP_REQUESTS:
            _IP_RATE_LOCK[source_ip] = now + IP_LOCKOUT_SECONDS
            log_event(
                f"network_security: rate-limit IP {source_ip} "
                f"({count}/{MAX_IP_REQUESTS} en {IP_WINDOW_SECONDS}s) — blocage {IP_LOCKOUT_SECONDS}s",
                "WARNING",
            )
            return {"allowed": False, "retry_after": float(IP_LOCKOUT_SECONDS),
                    "reason": f"Rate limit IP dépassé — blocage {IP_LOCKOUT_SECONDS}s"}

    return {"allowed": True, "retry_after": 0.0, "reason": "OK", "requests_in_window": count}


# ─── V1.2 : Réputation DNS / domaines malveillants ───────────────────────────

# Domaines connus malveillants (liste locale — peut être étendue depuis config)
_DOMAIN_BLOCKLIST: set[str] = {
    # C&C / malware connus
    "evil.com", "malware.example", "phishing.example",
    # Metadata cloud (SSRF)
    "169.254.169.254", "metadata.google.internal",
    "metadata.aws.internal", "169.254.170.2",
    # DNS rebinding courants
    "localtest.me", "lvh.me",
}


def is_domain_blocked(domain: str) -> bool:
    """Vérifie si un domaine est dans la liste de réputation."""
    domain_lower = domain.lower().strip(".")
    # Vérifie le domaine exact et les parents (ex: sub.evil.com → evil.com)
    parts = domain_lower.split(".")
    for i in range(len(parts) - 1):
        candidate = ".".join(parts[i:])
        if candidate in _DOMAIN_BLOCKLIST:
            return True
    return domain_lower in _DOMAIN_BLOCKLIST


def add_to_domain_blocklist(domain: str) -> None:
    """Ajoute un domaine à la liste noire de réputation."""
    _DOMAIN_BLOCKLIST.add(domain.lower())
    log_event(f"network_security: domaine ajouté à la blocklist : {domain}", "WARNING")


def check_domain(domain: str) -> dict:
    """
    Vérifie la réputation d'un domaine.

    Returns:
        dict avec allowed (bool), reason (str).
    """
    if is_domain_blocked(domain):
        log_event(f"network_security: domaine bloqué (réputation) : {domain}", "WARNING")
        return {"allowed": False, "reason": f"Domaine bloqué (réputation) : {domain}"}
    return {"allowed": True, "reason": "OK"}


# ─── V1.2 : Validation TLS basique ───────────────────────────────────────────

def validate_tls(url: str, timeout: float = 5.0) -> dict:
    """
    Vérifie la validité du certificat TLS d'une URL HTTPS.
    Utilise ssl.create_default_context() — valide chain + date d'expiration.

    Returns:
        dict avec valid (bool), reason (str), expiry (str|None).
    """
    import ssl
    import socket
    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme != "https":
        return {"valid": False, "reason": f"TLS uniquement pour HTTPS — schéma : {parsed.scheme}"}

    hostname = parsed.hostname or ""
    port     = parsed.port or 443

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert    = ssock.getpeercert()
                not_after = cert.get("notAfter", "")
                # Parse la date d'expiration
                try:
                    from datetime import datetime as _dt
                    expiry    = _dt.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    days_left = (expiry - _dt.now()).days
                    if days_left < 30:
                        log_event(
                            f"network_security: certificat TLS expire dans {days_left}j : {hostname}",
                            "WARNING",
                        )
                        return {
                            "valid": True, "expiry": not_after,
                            "days_left": days_left,
                            "reason": f"Certificat valide mais expire dans {days_left}j",
                        }
                    return {"valid": True, "expiry": not_after, "days_left": days_left, "reason": "OK"}
                except Exception:
                    return {"valid": True, "expiry": not_after, "reason": "OK"}
    except ssl.SSLCertVerificationError as exc:
        log_event(f"network_security: certificat TLS invalide — {hostname} : {exc}", "ERROR")
        return {"valid": False, "reason": f"Certificat invalide : {exc}"}
    except (socket.timeout, OSError) as exc:
        # Pas de connexion — on ne bloque pas si l'hôte est inaccessible
        return {"valid": None, "reason": f"Hôte inaccessible (timeout/erreur réseau) : {exc}"}
    except Exception as exc:
        return {"valid": None, "reason": f"Erreur TLS : {exc}"}
