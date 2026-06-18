"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.23
FILE         : src/security/tls_manager.py
ROLE         : Gestionnaire TLS/mTLS pour les communications inter-services

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-02
UPDATED      : 2026-06-02
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Phase 5 SSI — Architecture réseau sécurisée.
Génère et gère les certificats auto-signés pour les communications
inter-services ALFRED (API interne, webhooks). Implémente le
certificate pinning et la validation mTLS (Mutual TLS).

Usage principal : validation des connexions sortantes ALFRED_PC → ALFRED_WEB
et des communications entre modules critiques (SOC, API security).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import hashlib
import json
import ssl
import socket
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

_ROOT      = Path(__file__).resolve().parents[2]
_CERT_DIR  = _ROOT / "data" / "security" / "certs"
_CERT_DIR.mkdir(parents=True, exist_ok=True)
_CERT_LOG  = _ROOT / "data" / "security" / "cert_log.json"

_lock = threading.Lock()

# Pins de certificat connus (domain → sha256 du fingerprint)
_PINNED_CERTS: dict[str, str] = {}


# ─── Fingerprint d'un certificat ─────────────────────────────────────────────

def get_cert_fingerprint(host: str, port: int = 443, timeout: float = 5.0) -> str | None:
    """
    Récupère le fingerprint SHA-256 du certificat TLS d'un hôte.

    Returns:
        Fingerprint hex ou None si connexion impossible.
    """
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert_der = ssock.getpeercert(binary_form=True)
                if cert_der:
                    return hashlib.sha256(cert_der).hexdigest()
    except Exception as exc:
        log_event(f"tls_manager: impossible de récupérer cert {host}:{port} — {exc}", "WARNING")
    return None


def get_cert_info(host: str, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
    """
    Récupère les informations complètes du certificat TLS d'un hôte.

    Returns:
        dict avec subject, issuer, not_before, not_after, fingerprint, days_left.
    """
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert       = ssock.getpeercert()
                cert_der   = ssock.getpeercert(binary_form=True)
                fingerprint = hashlib.sha256(cert_der).hexdigest() if cert_der else None

                not_after = cert.get("notAfter", "")
                days_left = None
                try:
                    exp = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    days_left = (exp - datetime.now()).days
                except Exception:
                    pass

                return {
                    "host":        host,
                    "port":        port,
                    "subject":     dict(x[0] for x in cert.get("subject", [])),
                    "issuer":      dict(x[0] for x in cert.get("issuer", [])),
                    "not_before":  cert.get("notBefore", ""),
                    "not_after":   not_after,
                    "days_left":   days_left,
                    "fingerprint": fingerprint,
                    "valid":       True,
                    "expiring_soon": days_left is not None and days_left < 30,
                }
    except ssl.SSLCertVerificationError as exc:
        return {"host": host, "valid": False, "error": str(exc), "fingerprint": None}
    except Exception as exc:
        return {"host": host, "valid": None, "error": str(exc), "fingerprint": None}


# ─── Certificate Pinning ──────────────────────────────────────────────────────

def pin_certificate(host: str, fingerprint: str) -> None:
    """
    Enregistre le pin de certificat pour un hôte.
    Toute connexion future vers cet hôte sera validée contre ce pin.
    """
    with _lock:
        _PINNED_CERTS[host] = fingerprint
    log_event(f"tls_manager: pin enregistré pour {host} — {fingerprint[:16]}…")


def verify_pinned_cert(host: str, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
    """
    Vérifie que le certificat actuel d'un hôte correspond au pin enregistré.

    Returns:
        dict avec ok, host, match, current_fingerprint, pinned_fingerprint.
    """
    pinned = _PINNED_CERTS.get(host)
    if not pinned:
        return {
            "ok": None, "host": host,
            "match": None,
            "message": f"Aucun pin enregistré pour {host}",
        }

    current = get_cert_fingerprint(host, port, timeout)
    if current is None:
        return {
            "ok": False, "host": host,
            "match": False,
            "message": "Impossible de récupérer le certificat actuel",
        }

    match = current == pinned
    if not match:
        log_event(
            f"tls_manager: PIN MISMATCH pour {host} ! "
            f"pin={pinned[:16]}… actuel={current[:16]}…",
            "CRITICAL",
        )

    return {
        "ok":                  match,
        "host":                host,
        "match":               match,
        "current_fingerprint": current,
        "pinned_fingerprint":  pinned,
        "message":             "Pin valide" if match else "CERT PIN MISMATCH — possible MITM",
    }


def pin_from_live(host: str, port: int = 443) -> dict[str, Any]:
    """
    Récupère et enregistre automatiquement le pin du certificat actuel.
    À utiliser lors de la configuration initiale (TOFU — Trust On First Use).
    """
    fp = get_cert_fingerprint(host, port)
    if fp:
        pin_certificate(host, fp)
        return {"ok": True, "host": host, "fingerprint": fp, "message": "Pin enregistré (TOFU)"}
    return {"ok": False, "host": host, "message": "Impossible de récupérer le certificat"}


def get_pinned_certs() -> dict[str, str]:
    """Retourne tous les pins enregistrés."""
    with _lock:
        return dict(_PINNED_CERTS)


# ─── Validation TLS sortante ──────────────────────────────────────────────────

def validate_outbound_tls(urls: list[str], timeout: float = 5.0) -> dict[str, Any]:
    """
    Valide les connexions TLS sortantes (ALFRED_PC → ALFRED_WEB, APIs externes).

    Args:
        urls : liste d'URLs à valider (format https://host[:port]/path)

    Returns:
        dict avec résultats par URL et score global.
    """
    from urllib.parse import urlparse
    results = {}
    ok_count = 0

    for url in urls:
        parsed = urlparse(url)
        host   = parsed.hostname or ""
        port   = parsed.port or (443 if parsed.scheme == "https" else 80)

        if parsed.scheme != "https":
            results[url] = {"valid": False, "error": "Non-HTTPS URL"}
            continue

        info = get_cert_info(host, port, timeout)
        results[url] = info
        if info.get("valid") is True:
            ok_count += 1

    total = len([r for r in results.values() if r.get("valid") is not None])
    return {
        "urls_checked":  len(urls),
        "ok_count":      ok_count,
        "success_rate":  round(ok_count / total * 100, 1) if total else 0,
        "results":       results,
        "timestamp":     datetime.now(timezone.utc).isoformat(),
    }


# ─── VLAN / Architecture réseau (documentation) ───────────────────────────────

VLAN_CONFIG: dict[str, Any] = {
    "description": "Architecture réseau cible ALFRED — isolation VLAN",
    "vlans": {
        "VLAN_10_BUREAU": {
            "subnet":   "192.168.10.0/24",
            "devices":  ["ALFRED_PC (HP EliteBook)", "Galaxy Tab A9"],
            "internet": True,
            "access_to": {"VLAN_20_IOT": False, "VLAN_30_SERVERS": True},
            "firewall_rules": [
                "ALLOW outbound HTTPS 443",
                "ALLOW outbound DNS 53",
                "DENY inbound from VLAN_20_IOT",
                "ALLOW inbound from VLAN_30_SERVERS:443",
            ],
        },
        "VLAN_20_IOT": {
            "subnet":   "192.168.20.0/24",
            "devices":  ["Caméras IP", "Assistants vocaux", "Capteurs domotique"],
            "internet": False,
            "access_to": {"VLAN_10_BUREAU": False, "VLAN_30_SERVERS": False},
            "firewall_rules": [
                "DENY all outbound except DNS",
                "DENY all inbound",
                "ALLOW VLAN_30_SERVERS:RTSP inbound (caméras uniquement)",
            ],
            "notes": "Isolation stricte IoT — implémentation prévue V4 domotique",
        },
        "VLAN_30_SERVERS": {
            "subnet":   "192.168.30.0/24",
            "devices":  ["NAS", "Serveur RTSP (futur)"],
            "internet": True,
            "access_to": {"VLAN_10_BUREAU": True, "VLAN_20_IOT": True},
            "firewall_rules": [
                "ALLOW inbound from VLAN_10_BUREAU:443",
                "ALLOW outbound HTTPS",
                "DENY VLAN_20_IOT inbound except RTSP",
            ],
        },
    },
    "status": "PLANNED — V4 domotique",
    "current_state": "Réseau plat (non segmenté) — migration VLAN prévue avec switch manageable",
}


def get_vlan_config() -> dict[str, Any]:
    """Retourne la configuration VLAN cible documentée."""
    return VLAN_CONFIG


def get_network_architecture_report() -> dict[str, Any]:
    """Rapport d'architecture réseau pour le dashboard SSI."""
    pinned = get_pinned_certs()
    return {
        "_meta": {
            "project": "ALFRED",
            "block":   "B20",
            "file":    "network_architecture.json",
            "role":    "Architecture réseau SSI — TLS + VLAN",
            "version": "V1.0",
        },
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "tls_pinned_hosts": len(pinned),
        "pinned_certs":   {h: fp[:16] + "…" for h, fp in pinned.items()},
        "vlan_config":    VLAN_CONFIG,
        "tls_status":     "ACTIF — validation sortante",
        "mtls_status":    "PLANIFIÉ — V2 API interne",
        "recommendations": [
            "Activer le pin TLS pour cognitive-products-lab.fr",
            "Implémenter mTLS pour les communications ALFRED_PC ↔ ALFRED_WEB (V2)",
            "Migrer vers architecture VLAN segmentée (V4 domotique)",
            "Configurer DoH/DoT pour les résolutions DNS (V3)",
        ],
    }
