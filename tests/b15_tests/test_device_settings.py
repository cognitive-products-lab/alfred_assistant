"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.05
FILE         : tests/b15_tests/test_device_settings.py
ROLE         : Tests unitaires src/ui/device_settings.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-10
UPDATED      : 2026-06-10
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Tests de la persistance des réglages devices et du cache de
pré-chargement asynchrone (prefetch_devices_async / get_cached_*),
sans dépendre de matériel caméra/audio réel.
"""

import shutil
import tempfile
import time
from pathlib import Path

import pytest

from src.ui import device_settings as ds


@pytest.fixture(autouse=True)
def _isolated_settings_file(monkeypatch):
    """Redirige _SETTINGS_FILE vers un fichier temporaire pour chaque test."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_device_settings_"))
    fake_file = tmp_dir / "device_settings.json"
    monkeypatch.setattr(ds, "_SETTINGS_FILE", fake_file)
    yield fake_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture(autouse=True)
def _reset_cache():
    """Vide le cache de devices avant/après chaque test."""
    with ds._device_cache_lock:
        ds._device_cache.clear()
    yield
    with ds._device_cache_lock:
        ds._device_cache.clear()


# =============================================================================
# Persistance
# =============================================================================

def test_settings_file_does_not_exist_initially(_isolated_settings_file):
    assert ds.settings_file_exists() is False


def test_load_device_settings_returns_defaults_when_absent():
    settings = ds.load_device_settings()
    assert settings == ds._DEFAULTS


def test_save_then_load_roundtrip(_isolated_settings_file):
    new_settings = {
        "camera_index": 1,
        "audio_input_index": 2,
        "audio_output_index": 3,
    }
    ds.save_device_settings(new_settings)

    assert ds.settings_file_exists() is True
    loaded = ds.load_device_settings()
    assert loaded == new_settings


def test_load_merges_partial_settings_with_defaults(_isolated_settings_file):
    _isolated_settings_file.parent.mkdir(parents=True, exist_ok=True)
    _isolated_settings_file.write_text('{"camera_index": 2}', encoding="utf-8")

    loaded = ds.load_device_settings()
    assert loaded["camera_index"] == 2
    assert loaded["audio_input_index"] == ds._DEFAULTS["audio_input_index"]
    assert loaded["audio_output_index"] == ds._DEFAULTS["audio_output_index"]


# =============================================================================
# Cache / prefetch
# =============================================================================

def test_get_cached_cameras_falls_back_to_live_scan_when_empty():
    cams = ds.get_cached_cameras()
    assert isinstance(cams, list)
    assert len(cams) >= 1
    assert "index" in cams[0] and "name" in cams[0]


def test_prefetch_devices_async_fills_cache(monkeypatch):
    # Stubs rapides : éviter le scan OpenCV réel (lent sans caméra branchée)
    monkeypatch.setattr(ds, "list_cameras", lambda: [{"index": 0, "name": "Caméra 0"}])
    monkeypatch.setattr(ds, "list_audio_inputs", lambda: [{"index": 0, "name": "Micro 0"}])
    monkeypatch.setattr(ds, "list_audio_outputs", lambda: [{"index": 0, "name": "Sortie 0"}])

    ds.prefetch_devices_async()

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        with ds._device_cache_lock:
            if all(k in ds._device_cache for k in ("cameras", "audio_inputs", "audio_outputs")):
                break
        time.sleep(0.05)

    with ds._device_cache_lock:
        assert "cameras" in ds._device_cache
        assert "audio_inputs" in ds._device_cache
        assert "audio_outputs" in ds._device_cache


def test_get_cached_accessors_use_cache_without_rescanning(monkeypatch):
    sentinel_cams = [{"index": 0, "name": "Caméra factice"}]
    sentinel_inputs = [{"index": 0, "name": "Micro factice"}]
    sentinel_outputs = [{"index": 0, "name": "Sortie factice"}]

    with ds._device_cache_lock:
        ds._device_cache["cameras"] = sentinel_cams
        ds._device_cache["audio_inputs"] = sentinel_inputs
        ds._device_cache["audio_outputs"] = sentinel_outputs

    # Si le cache est utilisé, ces fonctions ne doivent jamais être appelées
    monkeypatch.setattr(ds, "list_cameras", lambda: pytest.fail("list_cameras ne doit pas être appelé"))
    monkeypatch.setattr(ds, "list_audio_inputs", lambda: pytest.fail("list_audio_inputs ne doit pas être appelé"))
    monkeypatch.setattr(ds, "list_audio_outputs", lambda: pytest.fail("list_audio_outputs ne doit pas être appelé"))

    assert ds.get_cached_cameras() == sentinel_cams
    assert ds.get_cached_audio_inputs() == sentinel_inputs
    assert ds.get_cached_audio_outputs() == sentinel_outputs


# =============================================================================
# Application des réglages audio
# =============================================================================

def test_apply_audio_settings_with_default_indexes_does_not_raise():
    ds.apply_audio_settings({"audio_input_index": -1, "audio_output_index": -1})
