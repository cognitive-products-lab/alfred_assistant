"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.04.001 -> 15.04.006
FILE         : src/ui/background_manager.py
ROLE         : Selection background selon periode, lieu et contexte

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
VERSION      : V1.2
STATUS       : STABLE

DESCRIPTION :
Selectionne l'image de fond appropriee selon la periode du jour,
le lieu et le contexte d'activite.

V1.2 : catalogue elargi depuis tree_assets_2026-05-15 :
  Interieur : salon, chambre, cuisine, bureau
  Exterieur : transport, ville, foret/rural, jardin (saisons)
  Specifique : soiree_tv, sport

Periodes reconnues :
  matin | midi | apres-midi -> "jour"
  soiree -> "soiree"
  nuit -> "nuit"

Lieux V1.2 :
  salon (defaut) | chambre | cuisine | bureau
  transport | ville | jardin | rural | foret

Specifiques :
  soiree_tv | sport
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional


# ============================================================
# Racines assets
# ============================================================

_ASSETS = Path(__file__).resolve().parents[2] / "assets" / "backgrounds"
_PORT   = _ASSETS / "mode_portrait"
_PORT_I = _PORT   / "interieur"
_PORT_E = _PORT   / "exterieur"
_PORT_O = _PORT   / "orientation portrait"   # doublons organisationnels
_PORT_S = _PORT_I / "specifique"

_PAYS   = _ASSETS / "mode_paysage"
_PAYS_I = _PAYS   / "interieur"
_PAYS_E = _PAYS   / "exterieur"
_PAYS_S = _PAYS_I / "specifiques"


# ============================================================
# Tables portrait (tranche normalisee : jour | soiree | nuit)
# ============================================================

_PORTRAIT_TABLE: dict[tuple[str, str], Path] = {

    # ── Salon ──────────────────────────────────────────────
    ("salon", "jour"):   _PORT_I / "salon" / "background_portrait_interieur_salon_jour.png",
    ("salon", "soiree"): _PORT_I / "salon" / "background_portrait_interieur_salon_soiree.png",
    ("salon", "nuit"):   _PORT_I / "salon" / "background_portrait_interieur_salon_nuit.png",

    # ── Chambre ────────────────────────────────────────────
    ("chambre", "jour"):   _PORT_I / "chambre" / "background_portrait_interieur_chambre_debut_journee.png",
    ("chambre", "soiree"): _PORT_I / "chambre" / "background_portrait_interieur_chambre_fin_journee.png",
    ("chambre", "nuit"):   _PORT_I / "chambre" / "background_portrait_interieur_chambre_nuit.jpg",

    # ── Cuisine ────────────────────────────────────────────
    ("cuisine", "jour"):   _PORT_I / "cuisine" / "background_portrait_interieur_cuisine_journee.png",
    ("cuisine", "soiree"): _PORT_I / "cuisine" / "background_portrait_interieur_cuisine_soiree.png",
    ("cuisine", "nuit"):   _PORT_I / "cuisine" / "background_portrait_interieur_cuisine_nuit.png",

    # ── Bureau ─────────────────────────────────────────────
    ("bureau", "jour"):   _PORT_I / "bureau" / "open_office" / "background_paysage_interieur_bureau_open_office.png",
    ("bureau", "soiree"): _PORT_I / "bureau" / "open_office" / "background_paysage_interieur_bureau_open_office.png",
    ("bureau", "nuit"):   _PORT_I / "bureau" / "open_office" / "background_paysage_interieur_bureau_open_office.png",

    # ── Transport ──────────────────────────────────────────
    ("transport", "jour"):   _PORT_E / "transport" / "background_portrait_exterieur_transport_journee.png",
    ("transport", "soiree"): _PORT_E / "transport" / "background_portrait_exterieur_transport_soiree.jpg",
    ("transport", "nuit"):   _PORT_E / "transport" / "Background_portrait_exterieur_transport_nuit.png",

    # ── Ville ──────────────────────────────────────────────
    ("ville", "jour"):   _PORT_E / "ville" / "Background_portrait_exterieur_ville_journee.png",
    ("ville", "soiree"): _PORT_E / "ville" / "background_portrait_exterieur_ville_matinee.png",
    ("ville", "nuit"):   _PORT_E / "ville" / "Background_portrait_exterieur_ville_journee.png",

    # ── Foret / Rural ──────────────────────────────────────
    ("foret", "jour"):   _PORT_E / "foret" / "background_portrait_exterieur_rural_jour.png",
    ("foret", "soiree"): _PORT_E / "foret" / "background_portrait_exterieur_rural_jour.png",
    ("foret", "nuit"):   _PORT_E / "foret" / "background_portrait_exterieur_rural_jour.png",
    ("rural", "jour"):   _PORT_E / "foret" / "background_portrait_exterieur_rural_jour.png",
    ("rural", "soiree"): _PORT_E / "foret" / "background_portrait_exterieur_rural_jour.png",
    ("rural", "nuit"):   _PORT_E / "foret" / "background_portrait_exterieur_rural_jour.png",

    # ── Specifiques ────────────────────────────────────────
    ("soiree_tv", "jour"):   _PORT_S / "soiree_tv" / "background_portrait_interieur_soiree tv_nuit.png",
    ("soiree_tv", "soiree"): _PORT_S / "soiree_tv" / "background_portrait_interieur_soiree tv_nuit.png",
    ("soiree_tv", "nuit"):   _PORT_S / "soiree_tv" / "background_portrait_interieur_soiree tv_nuit.png",

    ("sport", "jour"):   _PORT_S / "sport" / "background_portrait_interieur_sport.png",
    ("sport", "soiree"): _PORT_S / "sport" / "background_portrait_interieur_sport.png",
    ("sport", "nuit"):   _PORT_S / "sport" / "background_portrait_interieur_sport.png",
}

# ============================================================
# Tables paysage
# ============================================================

_PAYSAGE_TABLE: dict[tuple[str, str], Path] = {

    # ── Salon ──────────────────────────────────────────────
    ("salon", "jour"):   _PAYS_I / "salon" / "background_paysage_interieur_salon_journee.png",
    ("salon", "soiree"): _PAYS_I / "salon" / "background_paysage_interieur_salon_soiree.png",
    ("salon", "nuit"):   _PAYS_I / "salon" / "background_paysage_interieur_salon_nuit.png",

    # ── Chambre ────────────────────────────────────────────
    ("chambre", "jour"):   _PAYS_I / "chambre" / "background_paysage_interieur_chambre_debut_journee.png",
    ("chambre", "soiree"): _PAYS_I / "chambre" / "background_paysage_interieur_chambre_fin_journee.png",
    ("chambre", "nuit"):   _PAYS_I / "chambre" / "background_paysage_interieur_chambre_nuit.png",

    # ── Cuisine ────────────────────────────────────────────
    ("cuisine", "jour"):   _PAYS_I / "cuisine" / "Background_paysage_interieur_cuisine_jour.png",
    ("cuisine", "soiree"): _PAYS_I / "cuisine" / "background_paysage_interieur_cuisine_soiree.png",
    ("cuisine", "nuit"):   _PAYS_I / "cuisine" / "Background_paysage_interieur_cuisine_nuit.png",

    # ── Bureau ─────────────────────────────────────────────
    ("bureau", "jour"):   _PAYS_I / "bureau" / "open_office" / "background_paysage_interieur_bureau_open_office.png",
    ("bureau", "soiree"): _PAYS_I / "bureau" / "open_office" / "background_paysage_interieur_bureau_open_office.png",
    ("bureau", "nuit"):   _PAYS_I / "bureau" / "open_office" / "background_paysage_interieur_bureau_open_office.png",

    # ── Transport extérieur ────────────────────────────────
    ("transport", "jour"):   _PAYS_E / "transport" / "background_paysage_exterieur_transport_journee.png",
    ("transport", "soiree"): _PAYS_E / "transport" / "background_paysage_exterieur_transport_fin_journee.png",
    ("transport", "nuit"):   _PAYS_E / "transport" / "Background_paysage_exterieur_transport_nuit.png",

    # ── Rural extérieur ────────────────────────────────────
    ("rural", "jour"):   _PAYS_E / "rural" / "background_paysage_exterieur_rural_journee.png",
    ("rural", "soiree"): _PAYS_E / "rural" / "background_paysage_exterieur_rural_journee.png",
    ("rural", "nuit"):   _PAYS_E / "rural" / "background_paysage_exterieur_rural_journee.png",

    # ── Specifiques ────────────────────────────────────────
    ("soiree_tv", "jour"):   _PAYS_S / "background_paysage_interieur_spe_soiree_tv.png",
    ("soiree_tv", "soiree"): _PAYS_S / "background_paysage_interieur_spe_soiree_tv.png",
    ("soiree_tv", "nuit"):   _PAYS_S / "background_paysage_interieur_spe_soiree_tv.png",

    ("sport", "jour"):   _PAYS_S / "background_paysage_interieur_sport.png",
    ("sport", "soiree"): _PAYS_S / "background_paysage_interieur_sport.png",
    ("sport", "nuit"):   _PAYS_S / "background_paysage_interieur_sport.png",
}

_DEFAULT = _PORT_I / "salon" / "background_portrait_interieur_salon_jour.png"


# ============================================================
# Lieux valides
# ============================================================

_VALID_LOCATIONS = {
    "salon", "chambre", "cuisine", "bureau",
    "transport", "ville", "foret", "rural",
    "soiree_tv", "sport",
}


# ============================================================
# Normalisation periode
# ============================================================

def _normalize_period(period: str) -> str:
    """Reduit la periode a 3 tranches : jour | soiree | nuit."""
    p = period.lower().strip().replace("-", "_").replace(" ", "_")
    if p in {"matin", "debut_journee", "midi", "apres_midi", "apres-midi", "apres midi", "jour", "journee"}:
        return "jour"
    if p in {"soiree", "soir", "fin_journee", "crepuscule"}:
        return "soiree"
    if p in {"nuit", "nuit_tardive", "minuit"}:
        return "nuit"
    return "jour"


def _normalize_location(location: str) -> str:
    """Normalise le nom du lieu."""
    loc = location.lower().strip().replace("-", "_").replace(" ", "_")
    _aliases = {
        "chambre": "chambre",
        "bedroom": "chambre",
        "cuisine": "cuisine",
        "kitchen": "cuisine",
        "bureau": "bureau",
        "office": "bureau",
        "open_office": "bureau",
        "salle_reunion": "bureau",
        "transport": "transport",
        "voiture": "transport",
        "bus": "transport",
        "train": "transport",
        "ville": "ville",
        "city": "ville",
        "foret": "foret",
        "forest": "foret",
        "rural": "rural",
        "campagne": "rural",
        "soiree_tv": "soiree_tv",
        "tv": "soiree_tv",
        "sport": "sport",
        "salle_sport": "sport",
        "gym": "sport",
    }
    return _aliases.get(loc, "salon")


# ============================================================
# BackgroundManager
# ============================================================

class BackgroundManager:
    """
    Selectionne le background ALFRED selon periode, lieu et contexte.

    Usage :
        mgr = BackgroundManager()
        path = mgr.get_background(period="soiree", location="salon")

    Retourne toujours un chemin valide (fallback progressif).
    """

    def __init__(self, orientation: str = "portrait") -> None:
        self._orientation = orientation
        self._table = (
            _PORTRAIT_TABLE if orientation == "portrait" else _PAYSAGE_TABLE
        )

    # ----------------------------------------------------------
    # API principale
    # ----------------------------------------------------------

    def get_background(
        self,
        period:   str = "jour",
        location: str = "salon",
    ) -> str:
        """
        Retourne le chemin absolu du background.
        Fallback progressif : lieu demande -> salon/tranche -> salon/jour -> defaut.
        """
        tranche = _normalize_period(period)
        lieu    = _normalize_location(location)

        path = self._table.get((lieu, tranche))

        if path is None or not path.exists():
            path = self._table.get(("salon", tranche))
        if path is None or not path.exists():
            path = self._table.get(("salon", "jour"))
        if path is None or not path.exists():
            path = _DEFAULT

        return str(path)

    def get_background_for_context(self, time_ctx: dict) -> str:
        """Raccourci : prend directement le dict de get_time_context()."""
        return self.get_background(
            period=time_ctx.get("period", "jour"),
            location=time_ctx.get("location", "salon"),
        )

    def get_background_for_activity(self, activity: str, period: str = "jour") -> str:
        """
        Background par activite specifique.

        Args:
            activity : "soiree_tv" | "sport" | "sortie" | nom lieu
            period   : periode du jour
        """
        return self.get_background(period=period, location=activity)

    def list_available(self, location: str = "salon") -> dict[str, str]:
        """Liste les 3 backgrounds disponibles pour un lieu."""
        lieu = _normalize_location(location)
        result: dict[str, str] = {}
        for tranche in ("jour", "soiree", "nuit"):
            p = self._table.get((lieu, tranche))
            result[tranche] = str(p) if p and p.exists() else ""
        return result

    def list_locations(self) -> list[str]:
        """Retourne la liste des lieux disponibles."""
        return sorted(_VALID_LOCATIONS)

    def exists(self, period: str = "jour", location: str = "salon") -> bool:
        path = self.get_background(period, location)
        return Path(path).exists()

    def status(self) -> dict:
        total = len(self._table)
        ok    = sum(1 for p in self._table.values() if p.exists())
        return {
            "orientation": self._orientation,
            "total":       total,
            "available":   ok,
            "missing":     total - ok,
            "coverage":    f"{ok}/{total}",
            "locations":   self.list_locations(),
        }
