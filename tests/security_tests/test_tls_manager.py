"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED — tests tls_manager
BLOCK        : B20 · FUNCTION : 20.TEST
VERSION      : V1.0 · STATUS : ACTIVE
════════════════════════════════════════════════════════════
"""
import pytest
from src.security.tls_manager import (
    get_cert_fingerprint, get_cert_info,
    pin_certificate, verify_pinned_cert, pin_from_live,
    get_pinned_certs, validate_outbound_tls,
    get_vlan_config, get_network_architecture_report,
    _PINNED_CERTS,
)


@pytest.fixture(autouse=True)
def clean_pins():
    _PINNED_CERTS.clear()
    yield
    _PINNED_CERTS.clear()


# ─── pin_certificate / get_pinned_certs ──────────────────────────────────────

def test_pin_certificate_stores():
    pin_certificate("example.com", "abc123deadbeef" * 4)
    pins = get_pinned_certs()
    assert "example.com" in pins
    assert pins["example.com"] == "abc123deadbeef" * 4


def test_pin_certificate_multiple():
    pin_certificate("host1.com", "fp1" * 20)
    pin_certificate("host2.com", "fp2" * 20)
    pins = get_pinned_certs()
    assert len(pins) == 2


def test_get_pinned_certs_empty():
    assert get_pinned_certs() == {}


# ─── verify_pinned_cert ───────────────────────────────────────────────────────

def test_verify_no_pin():
    result = verify_pinned_cert("not-pinned.example.com")
    assert result["ok"] is None
    assert "Aucun pin" in result["message"]


def test_verify_pinned_cert_mismatch(monkeypatch):
    pin_certificate("myhost.com", "aabbcc" * 10 + "deadbeef")
    # Simuler un fingerprint différent
    monkeypatch.setattr(
        "src.security.tls_manager.get_cert_fingerprint",
        lambda host, port, timeout: "different" * 8,
    )
    result = verify_pinned_cert("myhost.com")
    assert result["ok"] is False
    assert result["match"] is False
    assert "MISMATCH" in result["message"]


def test_verify_pinned_cert_match(monkeypatch):
    fp = "a1b2c3" * 10 + "d4e5"
    pin_certificate("myhost.com", fp)
    monkeypatch.setattr(
        "src.security.tls_manager.get_cert_fingerprint",
        lambda host, port, timeout: fp,
    )
    result = verify_pinned_cert("myhost.com")
    assert result["ok"] is True
    assert result["match"] is True


def test_verify_pinned_cert_unreachable(monkeypatch):
    pin_certificate("unreachable.test", "fp" * 32)
    monkeypatch.setattr(
        "src.security.tls_manager.get_cert_fingerprint",
        lambda *a, **kw: None,
    )
    result = verify_pinned_cert("unreachable.test")
    assert result["ok"] is False


# ─── get_cert_info ────────────────────────────────────────────────────────────

def test_get_cert_info_non_https():
    # HTTP ne doit pas planter — retourne erreur gracieuse
    result = get_cert_info("httpbin.org", port=80, timeout=2.0)
    assert "host" in result

def test_get_cert_info_unreachable():
    result = get_cert_info("nonexistent.invalid.local", timeout=1.0)
    assert "host" in result
    assert result.get("valid") in (False, None)


# ─── validate_outbound_tls ────────────────────────────────────────────────────

def test_validate_outbound_non_https():
    result = validate_outbound_tls(["http://example.com"])
    assert "results" in result
    assert result["results"]["http://example.com"]["valid"] is False

def test_validate_outbound_structure():
    result = validate_outbound_tls(["https://cognitive-products-lab.fr"], timeout=3.0)
    assert "urls_checked" in result
    assert "ok_count" in result
    assert "success_rate" in result
    assert "timestamp" in result

def test_validate_outbound_empty():
    result = validate_outbound_tls([])
    assert result["urls_checked"] == 0


# ─── VLAN config ─────────────────────────────────────────────────────────────

def test_vlan_config_structure():
    cfg = get_vlan_config()
    assert "vlans" in cfg
    assert "VLAN_10_BUREAU" in cfg["vlans"]
    assert "VLAN_20_IOT" in cfg["vlans"]
    assert "VLAN_30_SERVERS" in cfg["vlans"]


def test_vlan_iot_isolated():
    cfg = get_vlan_config()
    iot = cfg["vlans"]["VLAN_20_IOT"]
    assert iot["internet"] is False
    assert iot["access_to"]["VLAN_10_BUREAU"] is False


# ─── network_architecture_report ─────────────────────────────────────────────

def test_architecture_report_structure():
    report = get_network_architecture_report()
    assert "_meta" in report
    assert "tls_pinned_hosts" in report
    assert "vlan_config" in report
    assert "recommendations" in report

def test_architecture_report_recommendations_not_empty():
    report = get_network_architecture_report()
    assert len(report["recommendations"]) >= 3
