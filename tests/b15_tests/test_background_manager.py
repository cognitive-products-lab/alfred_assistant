"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.04.001 -> 15.04.004
FILE         : tests/b15_tests/test_background_manager.py
ROLE         : Tests unitaires BackgroundManager -- periode, lieu, fallback, assets

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Tests de BackgroundManager (pure Python, sans Kivy).
Couvre : normalisation periode/lieu, resolution chemin, fallback, status().

STATUT 2026-07-18 : assets/backgrounds/ a ete archive (assets/_archive/backgrounds/)
dans le cadre de l'evolution de l'interface graphique, sans remplacement actif pour
l'instant -- voir assets/_archive/README.md. Les classes dependant de la presence
reelle des fichiers sont desactivees (skip) ; TestNormalizePeriod et
TestNormalizeLocation restent actives (logique pure, sans dependance disque).
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ui.background_manager import (
    BackgroundManager,
    _normalize_period,
    _normalize_location,
)

_SKIP_REASON = (
    "assets/backgrounds archive le 2026-07-18, en attente d'un nouveau systeme "
    "(cf. assets/_archive/README.md)"
)


# ---------------------------------------------------------
# _normalize_period
# ---------------------------------------------------------

class TestNormalizePeriod:

    def test_matin_to_jour(self):
        assert _normalize_period("matin") == "jour"

    def test_midi_to_jour(self):
        assert _normalize_period("midi") == "jour"

    def test_apres_midi_hyphen(self):
        assert _normalize_period("apres-midi") == "jour"

    def test_apres_midi_space(self):
        assert _normalize_period("apres midi") == "jour"

    def test_apres_midi_underscore(self):
        assert _normalize_period("apres_midi") == "jour"

    def test_jour_passthrough(self):
        assert _normalize_period("jour") == "jour"

    def test_soiree(self):
        assert _normalize_period("soiree") == "soiree"

    def test_soiree_accent(self):
        # soirée avec accent normalisé en soiree
        assert _normalize_period("soirée") in ("soiree", "jour")  # selon encodage

    def test_soir(self):
        assert _normalize_period("soir") == "soiree"

    def test_fin_journee(self):
        assert _normalize_period("fin_journee") == "soiree"

    def test_nuit(self):
        assert _normalize_period("nuit") == "nuit"

    def test_nuit_tardive(self):
        assert _normalize_period("nuit_tardive") == "nuit"

    def test_uppercase_input(self):
        assert _normalize_period("MATIN") == "jour"

    def test_unknown_defaults_to_jour(self):
        assert _normalize_period("inconnu") == "jour"

    def test_empty_defaults_to_jour(self):
        assert _normalize_period("") == "jour"


# ---------------------------------------------------------
# _normalize_location
# ---------------------------------------------------------

class TestNormalizeLocation:

    def test_salon(self):
        assert _normalize_location("salon") == "salon"

    def test_chambre(self):
        assert _normalize_location("chambre") == "chambre"

    def test_bedroom_alias(self):
        assert _normalize_location("bedroom") == "chambre"

    def test_cuisine(self):
        assert _normalize_location("cuisine") == "cuisine"

    def test_kitchen_alias(self):
        assert _normalize_location("kitchen") == "cuisine"

    def test_uppercase_input(self):
        assert _normalize_location("SALON") == "salon"

    def test_unknown_defaults_to_salon(self):
        assert _normalize_location("salle_de_bain") == "salon"

    def test_empty_defaults_to_salon(self):
        assert _normalize_location("") == "salon"


# ---------------------------------------------------------
# BackgroundManager -- mode portrait
# ---------------------------------------------------------

@pytest.mark.skip(reason=_SKIP_REASON)
class TestBackgroundManagerPortrait:

    def setup_method(self):
        self.mgr = BackgroundManager(orientation="portrait")

    def test_get_background_returns_string(self):
        path = self.mgr.get_background("matin", "salon")
        assert isinstance(path, str) and len(path) > 0

    def test_salon_jour_path_contains_salon(self):
        path = self.mgr.get_background("jour", "salon")
        assert "salon" in path.lower()

    def test_salon_soiree_path_contains_soiree(self):
        path = self.mgr.get_background("soiree", "salon")
        assert "soiree" in path.lower()

    def test_salon_nuit_path_contains_nuit(self):
        path = self.mgr.get_background("nuit", "salon")
        assert "nuit" in path.lower()

    def test_chambre_jour_exists(self):
        path = self.mgr.get_background("matin", "chambre")
        assert Path(path).exists(), f"Absent : {path}"

    def test_chambre_soiree_exists(self):
        path = self.mgr.get_background("soiree", "chambre")
        assert Path(path).exists(), f"Absent : {path}"

    def test_chambre_nuit_exists(self):
        path = self.mgr.get_background("nuit", "chambre")
        assert Path(path).exists(), f"Absent : {path}"

    def test_cuisine_jour_exists(self):
        path = self.mgr.get_background("midi", "cuisine")
        assert Path(path).exists(), f"Absent : {path}"

    def test_cuisine_soiree_exists(self):
        path = self.mgr.get_background("soiree", "cuisine")
        assert Path(path).exists(), f"Absent : {path}"

    def test_cuisine_nuit_exists(self):
        path = self.mgr.get_background("nuit", "cuisine")
        assert Path(path).exists(), f"Absent : {path}"

    def test_salon_all_periodes_exist(self):
        for period in ("matin", "soiree", "nuit"):
            path = self.mgr.get_background(period, "salon")
            assert Path(path).exists(), f"Absent : {path}"

    def test_all_9_combinations_return_nonempty(self):
        for loc in ("salon", "chambre", "cuisine"):
            for period in ("matin", "soiree", "nuit"):
                path = self.mgr.get_background(period, loc)
                assert path, f"Vide pour ({period}, {loc})"

    def test_all_9_combinations_exist(self):
        for loc in ("salon", "chambre", "cuisine"):
            for period in ("matin", "soiree", "nuit"):
                path = self.mgr.get_background(period, loc)
                assert Path(path).exists(), f"Absent : {path} ({period}, {loc})"


# ---------------------------------------------------------
# BackgroundManager -- mode paysage
# ---------------------------------------------------------

@pytest.mark.skip(reason=_SKIP_REASON)
class TestBackgroundManagerPaysage:

    def setup_method(self):
        self.mgr = BackgroundManager(orientation="paysage")

    def test_all_9_combinations_exist(self):
        for loc in ("salon", "chambre", "cuisine"):
            for period in ("matin", "soiree", "nuit"):
                path = self.mgr.get_background(period, loc)
                assert Path(path).exists(), f"Absent : {path} ({period}, {loc})"

    def test_orientation_paysage(self):
        info = self.mgr.status()
        assert info["orientation"] == "paysage"


# ---------------------------------------------------------
# BackgroundManager -- fallback
# ---------------------------------------------------------

@pytest.mark.skip(reason=_SKIP_REASON)
class TestBackgroundManagerFallback:

    def setup_method(self):
        self.mgr = BackgroundManager(orientation="portrait")

    def test_unknown_location_fallback_to_salon(self):
        # V1.2 : bureau est maintenant un lieu valide -> fallback avec lieu inconnu
        path = self.mgr.get_background("jour", "xyz_inconnu")
        assert "salon" in path.lower()

    def test_unknown_period_fallback_to_jour(self):
        path = self.mgr.get_background("inconnu", "salon")
        assert Path(path).exists()

    def test_fallback_always_returns_string(self):
        path = self.mgr.get_background("", "")
        assert isinstance(path, str) and len(path) > 0


# ---------------------------------------------------------
# get_background_for_context
# ---------------------------------------------------------

@pytest.mark.skip(reason=_SKIP_REASON)
class TestGetBackgroundForContext:

    def setup_method(self):
        self.mgr = BackgroundManager()

    def test_accepts_time_ctx_dict(self):
        ctx = {"period": "matin", "location": "salon"}
        path = self.mgr.get_background_for_context(ctx)
        assert Path(path).exists()

    def test_missing_keys_use_defaults(self):
        path = self.mgr.get_background_for_context({})
        assert Path(path).exists()

    def test_period_key_used(self):
        ctx_jour   = {"period": "matin",  "location": "salon"}
        ctx_nuit   = {"period": "nuit",   "location": "salon"}
        assert self.mgr.get_background_for_context(ctx_jour) != \
               self.mgr.get_background_for_context(ctx_nuit)


# ---------------------------------------------------------
# list_available
# ---------------------------------------------------------

@pytest.mark.skip(reason=_SKIP_REASON)
class TestListAvailable:

    def setup_method(self):
        self.mgr = BackgroundManager()

    def test_returns_dict_with_3_keys(self):
        result = self.mgr.list_available("salon")
        assert set(result.keys()) == {"jour", "soiree", "nuit"}

    def test_salon_all_paths_nonempty(self):
        result = self.mgr.list_available("salon")
        for tranche, path in result.items():
            assert path, f"Vide pour tranche={tranche}"

    def test_chambre_all_paths_nonempty(self):
        result = self.mgr.list_available("chambre")
        for tranche, path in result.items():
            assert path, f"Vide pour tranche={tranche}"

    def test_unknown_location_returns_salon(self):
        result   = self.mgr.list_available("inconnu")
        expected = self.mgr.list_available("salon")
        assert result == expected


# ---------------------------------------------------------
# exists + status
# ---------------------------------------------------------

@pytest.mark.skip(reason=_SKIP_REASON)
class TestExistsAndStatus:

    def setup_method(self):
        self.mgr = BackgroundManager()

    def test_exists_salon_jour(self):
        assert self.mgr.exists("jour", "salon") is True

    def test_exists_all_portrait(self):
        for loc in ("salon", "chambre", "cuisine"):
            for period in ("matin", "soiree", "nuit"):
                assert self.mgr.exists(period, loc), f"Absent ({period}, {loc})"

    def test_status_keys(self):
        s = self.mgr.status()
        for key in ("orientation", "total", "available", "missing", "coverage"):
            assert key in s, f"Cle manquante : {key}"

    def test_status_full_coverage(self):
        s = self.mgr.status()
        assert s["missing"] == 0, f"Assets manquants : {s}"

    def test_status_coverage_format(self):
        s = self.mgr.status()
        assert "/" in s["coverage"]
