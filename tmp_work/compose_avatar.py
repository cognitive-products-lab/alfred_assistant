"""Compose a full avatar_medium face from avatar_medium_no_face.png +
eyebrows/eyes/mouth layers.

Usage: python compose_avatar.py <eyebrows> <eyes> <mouth> <out_name>
All names without extension/prefix, e.g.:
    python compose_avatar.py neutral open closed test_neutral
"""
import sys
from pathlib import Path

from PIL import Image

BASE_DIR = Path(r"D:\PROJET_ALFRED\ALFRED_PC\assets\avatars\avatar_medium\base_medium")
NO_FACE = BASE_DIR / "avatar_medium_no_face.png"

CANVAS_W, CANVAS_H = 1024, 1536

# Decalage applique a chaque calque (sourcils/yeux/bouche) pour les
# repositionner sur le visage de avatar_medium_no_face.png (face skin
# bbox mesuree ~ x325-700, y255-480, cx~515). Les bbox LOCKED v1.0
# (eyebrows y172-196, eyes y193-222, mouth anchor y293) placent les
# calques dans la zone des cheveux -- offset vertical pour les ramener
# sur le visage.
OFFSET_X = 0
OFFSET_Y = 127

# Decalage specifique par calque (additionnel a OFFSET_X/OFFSET_Y).
LAYER_EXTRA_DY = {
    "eyebrows": 0,
    "eyes": 0,
    "mouth": 0,
}

# Sourcils non utilisables avec cette base (avatar_medium_no_face.png) :
# la frange de la coiffure couvre x415-615/y jusqu'a ~320-335, qui est
# la zone ou les sourcils devraient apparaitre une fois OFFSET_Y applique.
# Decision V1 (15/06/2026) : pas de sourcils pour cet avatar -- la valeur
# "eyebrows" passee a compose() est ignoree tant que EYEBROWS_ENABLED=False.
# Les calques eyebrows_*.png restent disponibles pour une future base avec
# une frange plus courte.
EYEBROWS_ENABLED = False


def _shift(layer: Image.Image, dx: int, dy: int) -> Image.Image:
    shifted = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    shifted.alpha_composite(layer, (dx, dy))
    return shifted


def compose(eyebrows: str, eyes: str, mouth: str, out_name: str) -> Path:
    base = Image.open(NO_FACE).convert("RGBA")
    for layer_name, value in (("eyebrows", eyebrows), ("eyes", eyes), ("mouth", mouth)):
        if value == "none":
            continue
        if layer_name == "eyebrows" and not EYEBROWS_ENABLED:
            continue
        layer_path = BASE_DIR / f"{layer_name}_{value}.png"
        layer = Image.open(layer_path).convert("RGBA")
        dy = OFFSET_Y + LAYER_EXTRA_DY.get(layer_name, 0)
        layer = _shift(layer, OFFSET_X, dy)
        base.alpha_composite(layer)
    out_path = BASE_DIR / f"{out_name}.png"
    base.save(out_path)
    return out_path


if __name__ == "__main__":
    eyebrows, eyes, mouth, out_name = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    p = compose(eyebrows, eyes, mouth, out_name)
    print(f"saved: {p}")
