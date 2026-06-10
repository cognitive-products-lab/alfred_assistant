"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_network_security.py
ROLE         : Tests unitaires — network_security.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : vérification IP (blocklist/allowlist), prévention SSRF
(IP privées, hostnames locaux, schémas interdits), stats connexions.
════════════════════════════════════════════════════════════
"""

import pytest
from src.security.network_security import (
    check_ip,
    check_url_ssrf,
    record_connection,
    get_connection_stats,
    add_to_blocklist,
    remove_from_blocklist,
    get_network_status,
    _IP_BLOCKLIST,
    _IP_ALLOWLIST,
)


@pytest.fixture(autouse=True)
def clean_blocklist():
    """Vide la blocklist/allowlist avant chaque test."""
    _IP_BLOCKLIST.clear()
    _IP_ALLOWLIST.clear()
    yield
    _IP_BLOCKLIST.clear()
    _IP_ALLOWLIST.clear()


# ─── check_ip — liste noire ───────────────────────────────────────────────────

def test_blocklisted_ip_denied():
    add_to_blocklist("1.2.3.4")
    result = check_ip("1.2.3.4")
    assert result["allowed"] is False
    assert "noire" in result["reason"].lower() or "list" in result["reason"].lower()


def test_non_blocklisted_ip_allowed():
    result = check_ip("8.8.8.8")
    assert result["allowed"] is True


def test_remove_from_blocklist():
    add_to_blocklist("5.5.5.5")
    remove_from_blocklist("5.5.5.5")
    result = check_ip("5.5.5.5")
    assert result["allowed"] is True


# ─── check_url_ssrf — IPs privées ────────────────────────────────────────────

@pytest.mark.parametrize("url", [
    "http://127.0.0.1:8080/admin",
    "http://10.0.0.1/secret",
    "http://192.168.1.1/config",
    "http://172.16.0.1/internal",
    "http://169.254.169.254/metadata",
])
def test_ssrf_private_ip_blocked(url):
    result = check_url_ssrf(url)
    assert result["allowed"] is False, f"SSRF non bloqué : {url}"
    assert "SSRF" in result["reason"] or "privée" in result["reason"] or "local" in result["reason"].lower()


@pytest.mark.parametrize("hostname_url", [
    "http://localhost/admin",
    "http://local/config",
    "http://metadata/latest",
])
def test_ssrf_local_hostname_blocked(hostname_url):
    result = check_url_ssrf(hostname_url)
    assert result["allowed"] is False, f"Hostname local non bloqué : {hostname_url}"


@pytest.mark.parametrize("scheme_url", [
    "gopher://127.0.0.1:25/MAIL",
    "ftp://internal.server/data",
    "file:///etc/passwd",
    "ldap://internal-server/dc=admin",
])
def test_ssrf_forbidden_scheme_blocked(scheme_url):
    result = check_url_ssrf(scheme_url)
    assert result["allowed"] is False, f"Schéma non bloqué : {scheme_url}"


@pytest.mark.parametrize("safe_url", [
    "https://api.openweathermap.org/data",
    "https://www.googleapis.com/oauth2",
    "https://cognitive-products-lab.fr/api",
])
def test_ssrf_legitimate_url_allowed(safe_url):
    result = check_url_ssrf(safe_url)
    assert result["allowed"] is True, f"URL légitime bloquée : {safe_url}"


# ─── Détection anomalies connexion ────────────────────────────────────────────

def test_connection_stats_initial():
    source = "test_source_stats_001"
    stats = get_connection_stats(source)
    assert stats["connections_in_window"] == 0
    assert stats["anomaly"] is False


def test_connection_counted():
    source = "test_source_counted_001"
    record_connection(source)
    record_connection(source)
    stats = get_connection_stats(source)
    assert stats["connections_in_window"] == 2


# ─── get_network_status ───────────────────────────────────────────────────────

def test_network_status_structure():
    status = get_network_status()
    assert "blocklist_size" in status
    assert "allowlist_size" in status
    assert "active_sources" in status
    assert "anomalous_sources" in status


def test_network_status_reflects_blocklist():
    add_to_blocklist("9.9.9.9")
    status = get_network_status()
    assert status["blocklist_size"] >= 1
