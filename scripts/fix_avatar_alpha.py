# -*- coding: utf-8 -*-
"""
PROJECT      : ALFRED
BLOCK        : OUTILS
FUNCTION     : XX.XX
FILE         : scripts/fix_avatar_alpha.py
ROLE         : Ajout d'un canal alpha (fond transparent) aux PNG d'avatar

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-14
UPDATED      : 2026-06-15
VERSION      : V1.0
STATUS       : TO_TEST

DESCRIPTION :
Ajoute un canal alpha (fond transparent) aux PNG d'avatar qui sont
encore en mode RGB (fond noir/blanc plein) — via flood-fill depuis
les coins, avec tolérance de couleur. Cree un .rgb_backup avant ecriture.

ATTENTION : tolerance=18 peut faire fuir le flood-fill dans les fines
lignes claires (ombres/lumieres) du costume si elles touchent le bord
de la silhouette -- cas observe sur alfred_medium_neutral_e.png et
alfred_medium_working.png (corriges le 15/06 via rembg, cf. backups).
Pour ces cas, preferer une segmentation IA (rembg) plutot que ce script.

Usage : python scripts/fix_avatar_alpha.py
"""
from __future__ import annotations

import shutil
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# (chemin, tolérance flood-fill)
TARGETS = [
    ("assets/avatars/avatar_medium/base_medium/alfred_medium_cybersecurity.png", 18),
    ("assets/avatars/avatar_medium/base_medium/alfred_medium_neutral_e.png", 18),
    ("assets/avatars/avatar_medium/base_medium/alfred_medium_thinking_full.png", 18),
    ("assets/avatars/avatar_medium/base_medium/alfred_medium_working.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_open.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_closed.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_a_eyes_half.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_open.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_closed.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_o_eyes_half.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_open.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_closed.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_m_eyes_half.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_idle_eyes_open.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_idle_eyes_closed.png.png", 18),
    ("assets/avatars/avatar_normal/base_normal/avatar_mouth_idle_eyes_half.png.png", 18),
]


def remove_background(img_bgr: np.ndarray, tol: int) -> np.ndarray:
    """Retourne une image BGRA avec le fond (connecte aux 4 coins) transparent."""
    h, w = img_bgr.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    flood_img = img_bgr.copy()
    flags = cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)

    for seed in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        cv2.floodFill(
            flood_img, mask, seed, 0,
            loDiff=(tol, tol, tol),
            upDiff=(tol, tol, tol),
            flags=flags,
        )

    bg_mask = mask[1:-1, 1:-1]

    # Adoucit le bord de la zone transparente (anti-aliasing)
    bg_mask_blur = cv2.GaussianBlur(bg_mask, (5, 5), 0)

    alpha = 255 - bg_mask_blur
    bgra = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = alpha
    return bgra


def main() -> None:
    for rel, tol in TARGETS:
        path = ROOT / rel
        if not path.exists():
            print(f"SKIP (introuvable) : {rel}")
            continue

        backup = path.with_suffix(path.suffix + ".rgb_backup")
        if not backup.exists():
            shutil.copy2(path, backup)

        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"ERREUR lecture : {rel}")
            continue

        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        result = remove_background(img, tol)
        cv2.imwrite(str(path), result)

        n_transparent = int(np.sum(result[:, :, 3] == 0))
        total = result.shape[0] * result.shape[1]
        print(f"OK : {rel} -> {n_transparent}/{total} px transparents ({100*n_transparent/total:.1f}%)")


if __name__ == "__main__":
    main()
