"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED — tests network_security V1.2
BLOCK        : B20 · FUNCTION : 20.TEST
VERSION      : V1.2 · STATUS : ACTIVE
════════════════════════════════════════════════════════════
"""
import pytest
from src.security.network_security import (
    check_ip, add_to_blocklist, remove_from_blocklist,
    check_url_ssrf, check_domain, add_to_domain_blocklist,
    is_domain_blocked, check_ip_rate_limit,
    validate_tls, get_network_status,
    _IP_BLOCKLIST, _IP_ALLOWLIST, _DOMAIN_BLOCKLIST,
    _IP_ATTEMPTS, _IP_RATE_LOCK,
)


@pytest.fixture(autouse=True)
def clean_state():
    _IP_BLOCKLIST.clear()
    _IP_ALLOWLIST.clear()
    _IP_ATTEMPTS.clear()
    _IP_RATE_LOCK.clear()
    # Garder le domaine blocklist de base, vider les custom
    custom = {d for d in _DOMAIN_BLOCKLIST if d.endswith(".custom")}
    for d in custom:
        _DOMAIN_BLOCKLIST.discard(d)
    yield
    _IP_BLOCKLIST.clear()
    _IP_ALLOWLIST.clear()
    _IP_ATTEMPTS.clear()
    _IP_RATE_LOCK.clear()


# ─── check_ip ────────────────────────────────────────────────────────────────

def test_check_ip_clean():
    result = check_ip("8.8.8.8")
    assert result["allowed"] is True

def test_check_ip_blocklisted():
    add_to_blocklist("1.2.3.4")
    result = check_ip("1.2.3.4")
    assert result["allowed"] is False

def test_remove_from_blocklist():
    add_to_blocklist("5.5.5.5")
    remove_from_blocklist("5.5.5.5")
    assert check_ip("5.5.5.5")["allowed"] is True


# ─── check_url_ssrf ──────────────────────────────────────────────────────────

@pytest.mark.parametrize("url", [
    "http://127.0.0.1:8080/admin",
    "http://10.0.0.1/secret",
    "http://192.168.1.1/config",
    "http://172.16.0.1/internal",
    "gopher://127.0.0.1:25/MAIL",
    "ldap://internal-server/dc=admin",
])
def test_ssrf_blocked(url):
    result = check_url_ssrf(url)
    assert result["allowed"] is False

@pytest.mark.parametrize("url", [
    "https://api.openweathermap.org/data",
    "https://cognitive-products-lab.fr/api",
])
def test_legitimate_url_allowed(url):
    result = check_url_ssrf(url)
    assert result["allowed"] is True

def test_localhost_blocked():
    assert check_url_ssrf("http://localhost/admin")["allowed"] is False


# ─── check_domain (V1.2) ─────────────────────────────────────────────────────

def test_domain_blocklist_known():
    result = check_domain("169.254.169.254")
    assert result["allowed"] is False

def test_domain_clean():
    result = check_domain("cognitive-products-lab.fr")
    assert result["allowed"] is True

def test_add_domain_blocklist():
    add_to_domain_blocklist("evil.custom")
    assert is_domain_blocked("evil.custom") is True
    assert check_domain("sub.evil.custom")["allowed"] is False

def test_subdomain_of_blocked():
    add_to_domain_blocklist("evil.custom")
    assert is_domain_blocked("a.b.evil.custom") is True

def test_non_blocked_domain():
    assert is_domain_blocked("google.com") is False


# ─── check_ip_rate_limit (V1.2) ──────────────────────────────────────────────

def test_fresh_ip_allowed():
    result = check_ip_rate_limit("10.20.30.40")
    assert result["allowed"] is True

def test_ip_rate_limit_structure():
    result = check_ip_rate_limit("10.20.30.41")
    assert "allowed" in result
    assert "retry_after" in result
    assert "reason" in result

def test_ip_rate_limit_different_ips_isolated():
    from src.security.network_security import MAX_IP_REQUESTS
    # Remplir le quota pour une IP
    for _ in range(MAX_IP_REQUESTS + 1):
        check_ip_rate_limit("1.1.1.100")
    # Une autre IP doit rester libre
    assert check_ip_rate_limit("2.2.2.200")["allowed"] is True

def test_ip_rate_limit_triggers_after_max():
    from src.security.network_security import MAX_IP_REQUESTS
    ip = "3.3.3.100"
    for _ in range(MAX_IP_REQUESTS + 1):
        check_ip_rate_limit(ip)
    result = check_ip_rate_limit(ip)
    assert result["allowed"] is False
    assert result["retry_after"] > 0


# ─── validate_tls (V1.2) ─────────────────────────────────────────────────────

def test_validate_tls_non_https():
    result = validate_tls("http://example.com")
    assert result["valid"] is False
    assert "HTTPS" in result["reason"] or "https" in result["reason"].lower()

def test_validate_tls_structure():
    result = validate_tls("https://example.com", timeout=3.0)
    assert "valid" in result
    assert "reason" in result
    # valid peut être True (cert OK), False (cert KO) ou None (timeout)
    assert result["valid"] in (True, False, None)

def test_validate_tls_invalid_host():
    result = validate_tls("https://nonexistent.invalid.local", timeout=1.0)
    # Doit gérer gracieusement sans lever d'exception
    assert "valid" in result


# ─── get_network_status (V1.2) ───────────────────────────────────────────────

def test_network_status_v12_fields():
    status = get_network_status()
    assert "blocklist_size" in status
    assert "anomalous_sources" in status
    assert "domain_blocklist" in status      # nouveau V1.2
    assert "ip_rate_limited" in status       # nouveau V1.2

def test_network_status_domain_count():
    initial = get_network_status()["domain_blocklist"]
    add_to_domain_blocklist("new.custom")
    updated = get_network_status()["domain_blocklist"]
    assert updated == initial + 1
