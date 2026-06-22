"""Génère tous les sprites avatar_medium depuis les calques (no_face + eyes + mouth).

Speaking frames (lip-sync) + sprites d'état (idle, listening, thinking...).
Toutes les images utilisent avatar_medium_no_face.png comme base pour
garantir la cohérence visuelle entre états.

Backups automatiques avant écrasement (.lipsync_backup).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tmp_work"))

from compose_avatar import compose, BASE_DIR

# ── Frames lip-sync speaking ──────────────────────────────────────────────────
# Consommées par _SPEAKING_MEDIUM_FRAMES dans avatar_renderer.py
SPEAKING_FRAMES = {
    "alfred_medium_neutral_a": ("open",   "a"),
    "alfred_medium_neutral_e": ("open",   "e"),
    "alfred_medium_neutral_i": ("open",   "i"),
    "alfred_medium_neutral_o": ("open",   "o"),
    "alfred_medium_neutral_u": ("open",   "u"),
    "alfred_medium_neutral_m": ("half",   "m"),
}

# -- Sprites d'etat --──────────────────────────────────────────────────────────
# Consommés par _MEDIUM_SPRITES dans avatar_renderer.py
STATE_SPRITES = {
    "alfred_medium_neutral":      ("half",   "closed"),   # idle / focus / offline
    "alfred_medium_listening":    ("open",   "closed"),   # listening
    "alfred_medium_thinking":     ("half",   "closed"),   # thinking (yeux mi-clos)
    "alfred_medium_explaining":   ("open",   "closed"),   # speaking état de base
    "alfred_medium_love":         ("happy",  "smile"),    # support
    "alfred_medium_excited":      ("open",   "big_smile"),  # challenge
    "alfred_medium_very_excited": ("happy",  "big_smile"),  # complicite
    "alfred_medium_cybersecurity":("open",   "concerned"),  # error
}

ALL_SPRITES = {**SPEAKING_FRAMES, **STATE_SPRITES}


def build(out_name: str, eyes: str, mouth: str, dry_run: bool) -> None:
    out_path = BASE_DIR / f"{out_name}.png"
    backup   = BASE_DIR / f"{out_name}.png.lipsync_backup"

    if dry_run:
        print(f"  [DRY] {out_name}.png  <-  eyes_{eyes} + mouth_{mouth}")
        return

    if out_path.exists() and not backup.exists():
        shutil.copy2(out_path, backup)
        print(f"         backup : {backup.name}")

    p = compose(eyebrows="none", eyes=eyes, mouth=mouth, out_name=out_name)
    print(f"  OK  {p.name}  (eyes={eyes}, mouth={mouth})")


def main(dry_run: bool = False, only: str = "all") -> None:
    print(f"Base dir : {BASE_DIR}\n")

    if only in ("all", "speaking"):
        print("-- Speaking frames --")
        for out_name, (eyes, mouth) in SPEAKING_FRAMES.items():
            build(out_name, eyes, mouth, dry_run)

    if only in ("all", "states"):
        print("\n-- Sprites d'etat --")
        for out_name, (eyes, mouth) in STATE_SPRITES.items():
            build(out_name, eyes, mouth, dry_run)

    if not dry_run:
        print("\nSprites générés. Relance alfred_with_ui pour tester.")


if __name__ == "__main__":
    dry  = "--dry"     in sys.argv
    only_speaking = "--speaking" in sys.argv
    only_states   = "--states"   in sys.argv
    only = "speaking" if only_speaking else "states" if only_states else "all"
    main(dry_run=dry, only=only)
