"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : SMOKE
FILE         : tests/b15_tests/test_smoke_avatars_batch1.py
ROLE         : Smoke tests (lot 1) pour les assets avatar/voix B15 sans
               couverture de test (images PNG, modeles vocaux Piper).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie que chaque image avatar est valide (Pillow verify()) et que les
modeles vocaux Piper (.onnx + .onnx.json) sont presents et coherents.
"""

import json
from pathlib import Path

import pytest
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]

AVATAR_IMAGES = [
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_closed.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_half.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_a_eyes_open.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_idle_eyes_closed.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_idle_eyes_half.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_closed.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_half.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_m_eyes_open.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_closed.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_half.png.png",
    "assets/avatars/no_active_avatar_normal/base_normal/avatar_mouth_o_eyes_open.png.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_neutral.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_a.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_e.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_i.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_o.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_u.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_m.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_listening.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_thinking.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_thinking_full.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_explaining.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_happy.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_working.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_confused.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_cybersecurity.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_love.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_excited.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_very_excited.png",
    "assets/avatars/avatar_medium/base_medium/alfred_medium_idea.png",
]


@pytest.mark.parametrize("relpath", AVATAR_IMAGES)
def test_avatar_image_is_valid_and_not_corrupted(relpath):
    path = ROOT / relpath
    assert path.exists(), f"fichier manquant : {relpath}"
    with Image.open(path) as img:
        img.verify()
    with Image.open(path) as img:
        width, height = img.size
        assert width > 0 and height > 0
        assert img.format == "PNG"


VOICE_MODEL_DIRS = [
    "assets/voices",
    "assets/models/tts/fr_FR",
]

VOICE_ONNX_FILES = [
    "fr_FR-upmc-medium.onnx",
    "fr_FR-mls_1840-low.onnx",
]


@pytest.mark.parametrize("base_dir", VOICE_MODEL_DIRS)
@pytest.mark.parametrize("onnx_name", VOICE_ONNX_FILES)
def test_voice_model_onnx_and_config_present(base_dir, onnx_name):
    onnx_path = ROOT / base_dir / onnx_name
    json_path = ROOT / base_dir / f"{onnx_name}.json"
    assert onnx_path.exists() and onnx_path.stat().st_size > 1_000_000, (
        f"modèle .onnx manquant ou anormalement petit : {onnx_path}"
    )
    assert json_path.exists()
    config = json.loads(json_path.read_text(encoding="utf-8"))
    assert "audio" in config
    assert isinstance(config["phoneme_id_map"], dict) and config["phoneme_id_map"]


def test_model_card_readable():
    path = ROOT / "assets" / "models" / "tts" / "fr_FR" / "MODEL_CARD"
    text = path.read_text(encoding="utf-8", errors="replace")
    assert text.strip()
