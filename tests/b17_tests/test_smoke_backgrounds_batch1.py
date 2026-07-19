"""
PROJECT      : ALFRED
BLOCK        : B17
FUNCTION     : SMOKE
FILE         : tests/b17_tests/test_smoke_backgrounds_batch1.py
ROLE         : Smoke tests (lot 1) pour les assets background (avatar) B17
               sans couverture de test.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie que chaque image background est un fichier image valide et non
corrompu (ouverture + verify() Pillow), avec des dimensions non nulles.

STATUT 2026-07-18 : assets/backgrounds/ a ete archive (assets/_archive/backgrounds/)
dans le cadre de l'evolution de l'interface graphique, sans remplacement actif pour
l'instant. Module desactive en attente d'un nouveau systeme de backgrounds -- voir
assets/_archive/README.md.
"""

from pathlib import Path

import pytest
from PIL import Image

pytest.skip(
    "assets/backgrounds archive le 2026-07-18, en attente d'un nouveau systeme "
    "(cf. assets/_archive/README.md)",
    allow_module_level=True,
)

ROOT = Path(__file__).resolve().parents[2]

BACKGROUND_FILES = [
    "assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_debut_journee.png",
    "assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_fin_journee.png",
    "assets/backgrounds/mode_paysage/interieur/chambre/background_paysage_interieur_chambre_nuit.png",
    "assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_debut fin journee.jpg",
    "assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_matinee.jpg",
    "assets/backgrounds/mode_portrait/exterieur/transport/background_portrait_exterieur_transport_soiree.jpg",
    "assets/backgrounds/mode_portrait/interieur/bureau/open_office/background_paysage_interieur_bureau_open_office.png",
    "assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_debut_journee.png",
    "assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_fin_journee.png",
    "assets/backgrounds/mode_portrait/interieur/chambre/background_portrait_interieur_chambre_nuit.jpg",
    "assets/backgrounds/mode_portrait/interieur/specifique/sport/background_portrait_interieur_sport.png",
    "assets/backgrounds/mode_portrait/orientation portrait/specifique/Transport/background_portrait_exterieur_transport_debut fin journee.jpg",
]


@pytest.mark.parametrize("relpath", BACKGROUND_FILES)
def test_background_image_is_valid_and_not_corrupted(relpath):
    path = ROOT / relpath
    assert path.exists(), f"fichier manquant : {relpath}"

    with Image.open(path) as img:
        img.verify()

    with Image.open(path) as img:
        width, height = img.size
        assert width > 0 and height > 0
        assert img.format in ("PNG", "JPEG")
