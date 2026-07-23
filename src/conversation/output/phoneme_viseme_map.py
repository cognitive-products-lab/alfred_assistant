"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.03.005
FILE         : src/conversation/output/phoneme_viseme_map.py
ROLE         : Table phonème IPA (espeak-ng fr) -> visème V00-V14

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT — à valider par test réel (voir avatar V00-V14)

DESCRIPTION :
Table de correspondance construite à partir de
assets/avatars/avatar_medium/Architecture retenue avatar.txt (groupes de
phonèmes par visème, définis avec l'avatar). Un phonème absent de la table
(None) ne déclenche PAS de changement de bouche : la forme précédente est
conservée. C'est volontaire pour les marqueurs de prosodie espeak-ng qui ne
correspondent à aucun son (accents '^'/'$'ˈ'/'ˌ', tiret de liaison '-',
diacritique de nasalisation '̃') et pour les espaces entre mots (éviter de
refermer la bouche à chaque mot en parole fluide). La ponctuation qui marque
une vraie pause (',', '.') referme la bouche (V00).
"""

# Silence / repos
V00_SILENCE = "V00"

PHONEME_TO_VISEME: dict[str, str | None] = {
    # Marqueurs de structure espeak-ng — pas de son, ne change pas la bouche
    "^": V00_SILENCE,   # début de phrase
    "$": V00_SILENCE,   # fin de phrase
    " ": None,          # frontière de mot — garde la forme en cours
    "-": None,          # frontière de syllabe
    "ˈ": None,          # accent primaire (prosodie, pas un son)
    "ˌ": None,          # accent secondaire
    "̃": None,           # diacritique de nasalisation — garde la voyelle portée
    ",": V00_SILENCE,   # pause réelle
    ".": V00_SILENCE,
    ";": V00_SILENCE,
    ":": V00_SILENCE,
    "!": V00_SILENCE,
    "?": V00_SILENCE,

    # V01 — M, B, P (lèvres jointes)
    "m": "V01", "b": "V01", "p": "V01",

    # V02 — F, V (lèvre inférieure sous les dents)
    "f": "V02", "v": "V02",

    # V03 — T, D, N (petite ouverture)
    "t": "V03", "d": "V03", "n": "V03", "ɲ": "V03",

    # V04 — L (langue légèrement visible)
    "l": "V04",

    # V05 — S, Z (bouche étirée, dents proches)
    "s": "V05", "z": "V05",

    # V06 — CH, J (lèvres légèrement projetées)
    "ʃ": "V06", "ʒ": "V06",

    # V07 — K, G (ouverture moyenne) — ŋ (vélaire nasale) regroupée ici
    "k": "V07", "ɡ": "V07", "g": "V07", "ŋ": "V07",

    # V08 — R (bouche semi-arrondie)
    "ʁ": "V08", "ɹ": "V08", "r": "V08",

    # V09 — A (grande ouverture verticale)
    "a": "V09", "ɑ": "V09",

    # V10 — É, È, AI (ouverture horizontale)
    "e": "V10", "ɛ": "V10",

    # V11 — I, Y (lèvres très étirées) — j (semi-voyelle "yeux") regroupée ici
    "i": "V11", "y": "V11", "j": "V11",

    # V12 — O, AU (bouche ronde moyenne)
    "o": "V12", "ɔ": "V12",

    # V13 — OU, W (petite bouche ronde projetée)
    "u": "V13", "w": "V13",

    # V14 — U, EU, Œ (bouche arrondie et serrée) — ə (e muet) et ɥ (semi-voyelle
    # "huit", arrondie) regroupées ici faute de catégorie dédiée
    "ø": "V14", "œ": "V14", "ə": "V14", "ɥ": "V14",
}


def phoneme_to_viseme(phoneme: str) -> str | None:
    """Retourne le code visème (V00-V14) pour un phonème IPA, ou None si le
    phonème ne doit pas changer la bouche affichée (marqueur muet)."""
    return PHONEME_TO_VISEME.get(phoneme, None)


def build_viseme_timeline(alignments: list, sample_rate: int) -> list[dict]:
    """
    Convertit la liste de PhonemeAlignment (piper, include_alignments=True)
    en timeline de visèmes compacte pour l'avatar : fusionne les phonèmes
    consécutifs qui partagent le même visème (ou qui n'en changent pas) en
    un seul segment, pour minimiser le nombre de changements de sprite côté JS.

    Args:
        alignments  : list[piper.voice.PhonemeAlignment] (phoneme, num_samples, ...)
        sample_rate : fréquence d'échantillonnage du modèle (ex. 22050)

    Returns:
        list[{"v": "V03", "t": 120, "d": 80}] — t/d en millisecondes,
        t = début absolu depuis le début de la phrase.
    """
    timeline: list[dict] = []
    t_ms = 0.0
    current_viseme: str | None = None

    for alignment in alignments:
        dur_ms = (float(alignment.num_samples) / sample_rate) * 1000.0
        viseme = phoneme_to_viseme(alignment.phoneme)

        if viseme is None:
            # Marqueur muet : prolonge le segment en cours sans le fermer
            if timeline:
                timeline[-1]["d"] += dur_ms
            t_ms += dur_ms
            continue

        if viseme == current_viseme and timeline:
            timeline[-1]["d"] += dur_ms
        else:
            timeline.append({"v": viseme, "t": round(t_ms, 1), "d": round(dur_ms, 1)})
            current_viseme = viseme

        t_ms += dur_ms

    return timeline
