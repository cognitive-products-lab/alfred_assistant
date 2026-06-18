"""Process raw mouth images (real alpha) into LOCKED v1.0 layer PNGs per
mouth_spec.yaml.

Crops content from source images, scales to fit the mouth bbox
[470,262,580,325] (110x63px, anchor 525,293) and pastes onto a 1024x1536
transparent canvas, centered on the anchor.
"""
from pathlib import Path

import numpy as np
from PIL import Image

SRC_DIR = Path(r"D:\PROJET_ALFRED\ALFRED_PC\assets\avatars\avatar_medium\base_medium\mouths")
OUT_DIR = Path(r"D:\PROJET_ALFRED\ALFRED_PC\assets\avatars\avatar_medium\base_medium")
NO_FACE = OUT_DIR / "avatar_medium_no_face.png"

CANVAS_W, CANVAS_H = 1024, 1536
BBOX = (470, 262, 580, 325)  # x0,y0,x1,y1
BBOX_W = BBOX[2] - BBOX[0]
BBOX_H = BBOX[3] - BBOX[1]
ANCHOR_X = 525
ANCHOR_Y = 293

WHITE_THRESHOLD = 245


def white_to_alpha(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    arr = np.array(rgba)
    alpha = arr[:, :, 3]
    transparent_ratio = (alpha < 50).mean()
    if transparent_ratio > 0.10:
        return rgba

    rgb = arr[:, :, :3].astype(np.float32)
    min_channel = rgb.min(axis=2)
    new_alpha = np.clip((255 - min_channel) * (255.0 / (255 - WHITE_THRESHOLD)), 0, 255)
    out = np.dstack([rgb, new_alpha]).astype(np.uint8)
    return Image.fromarray(out, mode="RGBA")


def crop_to_content(img: Image.Image) -> Image.Image:
    arr = np.array(img)
    mask = arr[:, :, 3] > 10
    ys, xs = np.where(mask)
    x0, x1 = xs.min(), xs.max() + 1
    y0, y1 = ys.min(), ys.max() + 1
    return img.crop((x0, y0, x1, y1))


def place_on_canvas(content: Image.Image) -> Image.Image:
    scale = min(BBOX_W / content.width, BBOX_H / content.height)
    new_w = max(1, round(content.width * scale))
    new_h = max(1, round(content.height * scale))
    resized = content.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    paste_x = round(ANCHOR_X - new_w / 2)
    paste_y = round(ANCHOR_Y - new_h / 2)
    canvas.alpha_composite(resized, (paste_x, paste_y))
    return canvas


def main():
    variants = {
        "mouth_closed.png": SRC_DIR / "mouth_closed.png",
        "mouth_m.png": SRC_DIR / "mouth_m.png",
        "mouth_a.png": SRC_DIR / "mouth_a.png",
        "mouth_e.png": SRC_DIR / "mouth_e.png",
        "mouth_i.png": SRC_DIR / "mouth_i.png",
        "mouth_o.png": SRC_DIR / "mouth_o.png",
        "mouth_u.png": SRC_DIR / "mouth_u.png",
        "mouth_smile.png": SRC_DIR / "mouth_smile.png",
        "mouth_big_smile.png": SRC_DIR / "mouth_big_smile.png",
        "mouth_concerned.png": SRC_DIR / "mouth_concerned.png",
        "mouth_surprised.png": SRC_DIR / "mouth_surprised.png",
    }

    base = Image.open(NO_FACE).convert("RGBA")

    for out_name, src_path in variants.items():
        img = Image.open(src_path)
        rgba = white_to_alpha(img)
        content = crop_to_content(rgba)
        canvas = place_on_canvas(content)

        out_path = OUT_DIR / out_name
        canvas.save(out_path)

        arr = np.array(canvas)
        mask = arr[:, :, 3] > 128
        ys, xs = np.where(mask)
        bx0, bx1 = xs.min(), xs.max()
        by0, by1 = ys.min(), ys.max()
        cx = (bx0 + bx1) / 2
        cy = (by0 + by1) / 2
        print(f"{out_name}: bbox=({bx0},{by0})-({bx1},{by1}) "
              f"center=({cx:.1f},{cy:.1f}) target_anchor=({ANCHOR_X},{ANCHOR_Y})")

        overlay = base.copy()
        overlay.alpha_composite(canvas)
        overlay.save(OUT_DIR / f"preview_{out_name}")


if __name__ == "__main__":
    main()
