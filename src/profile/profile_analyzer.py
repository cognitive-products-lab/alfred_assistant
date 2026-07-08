"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : XX.XX
FILE         : src/profile/profile_analyzer.py
ROLE         : Analyseur de profil psychométrique — passation conversationnelle
               des questionnaires Q00-Q09 et calcul des scores

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-22
UPDATED      : 2026-07-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Ce module gère la passation conversationnelle des questionnaires psychométriques :
  - Q01 : Bien-être subjectif (SWLS + PANAS-SF)
  - Q02 : Style cognitif (Analytique/Intuitif + Verbal/Visuel)
  - Q03 : Régulation émotionnelle (ERQ + PSS)
  - Q04 : Motivations et valeurs (SDT)
  - Q09 : Personnalité HEXACO-24 (6 dimensions — Ashton & Lee 2009)
  - Q00 : Profil complémentaire (qualitatif)

Principe UX central : les questionnaires sont posés question par question dans la
conversation ALFRED — pas de formulaire à remplir. L'utilisateur peut s'arrêter,
reprendre, et chaque réponse est sauvegardée immédiatement.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Chemins par défaut (overridables pour les tests)
# ---------------------------------------------------------------------------
_BASE_DIR = Path(__file__).resolve().parent.parent.parent  # racine du projet
_ANSWERS_PATH = _BASE_DIR / "data" / "profile" / "answers_template.json"


# ---------------------------------------------------------------------------
# Définition des questionnaires et de leurs items
# ---------------------------------------------------------------------------

#: Métadonnées de chaque questionnaire
QUESTIONNAIRE_META: Dict[str, Dict[str, Any]] = {
    "q01_bien_etre_subjectif": {
        "label": "Bien-être subjectif",
        "duration_min": 7,
        "duration_max": 9,
        "min_for_partial": 7,
        "sections": ["swls", "panas_positif", "panas_negatif"],
    },
    "q02_style_cognitif": {
        "label": "Style cognitif",
        "duration_min": 8,
        "duration_max": 10,
        "min_for_partial": 8,
        "sections": ["analytique", "intuitif", "verbal", "visuel"],
    },
    "q03_regulation_emotionnelle": {
        "label": "Régulation émotionnelle",
        "duration_min": 8,
        "duration_max": 10,
        "min_for_partial": 8,
        "sections": ["reevaluation", "suppression", "stress"],
    },
    "q04_motivations_valeurs": {
        "label": "Motivations et valeurs",
        "duration_min": 9,
        "duration_max": 11,
        "min_for_partial": 9,
        "sections": ["autonomie", "competence", "appartenance"],
    },
    "q09_hexaco_personnalite": {
        "label": "Personnalité HEXACO-24",
        "duration_min": 8,
        "duration_max": 10,
        "min_for_partial": 12,
        "sections": ["honnetete_humilite", "emotivite", "extraversion", "agreabilite", "conscienciosite", "ouverture"],
    },
    "q00_profil_complementaire": {
        "label": "Profil complémentaire",
        "duration_min": 10,
        "duration_max": 15,
        "min_for_partial": 12,
        "sections": ["energie", "accessibilite", "limites", "communication", "contexte"],
    },
}


#: Items ordonnés pour chaque questionnaire
#: Chaque item : (question_id, texte_alfred, type_reponse)
#: type_reponse : "likert_5" | "likert_7" | "choix_binaire" | "texte_libre"
QUESTIONNAIRE_ITEMS: Dict[str, List[Tuple[str, str, str]]] = {

    "q01_bien_etre_subjectif": [
        ("swls_01",
         "Première question — dans l'ensemble, est-ce que tu as l'impression que ta vie "
         "correspond à ce que tu imaginais qu'elle serait, à ton idéal ? "
         "Tu peux répondre de 1 (pas du tout) à 7 (tout à fait).",
         "likert_7"),
        ("swls_02",
         "Est-ce que tu dirais que les conditions de ta vie en ce moment sont excellentes ? "
         "De 1 à 7.",
         "likert_7"),
        ("swls_03",
         "Et globalement, tu es satisfaite de ta vie en ce moment ? De 1 à 7.",
         "likert_7"),
        ("swls_04",
         "Est-ce que tu as l'impression d'avoir obtenu les choses importantes que tu voulais "
         "jusqu'ici dans ta vie — même si tout n'est pas parfait ? De 1 à 7.",
         "likert_7"),
        ("swls_05",
         "Si tu pouvais recommencer ta vie depuis le début, est-ce que tu changerais beaucoup "
         "de choses ? Réponds en inversant : 1 = je changerais tout, 7 = je ne changerais "
         "presque rien.",
         "likert_7"),
        ("pan_p_01",
         "Ces dernières semaines, à quel point tu t'es sentie enthousiaste — pleine d'élan, "
         "d'envie ? De 1 (pas du tout) à 7 (énormément).",
         "likert_7"),
        ("pan_p_02",
         "Et active, énergique — physiquement et mentalement ? De 1 à 7.",
         "likert_7"),
        ("pan_p_03",
         "Est-ce que tu t'es sentie inspirée ces dernières semaines — des idées qui viennent, "
         "une envie de créer ? De 1 à 7.",
         "likert_7"),
        ("pan_p_04",
         "Déterminée — avec une direction claire, une volonté d'avancer ? De 1 à 7.",
         "likert_7"),
        ("pan_p_05",
         "Et attentive, concentrée — capable de te focaliser sur ce que tu faisais ? "
         "De 1 à 7.",
         "likert_7"),
        ("pan_n_01",
         "Ces dernières semaines, tu t'es sentie irritable ou agacée — des choses qui t'ont "
         "mis les nerfs en pelote ? De 1 à 7.",
         "likert_7"),
        ("pan_n_02",
         "Stressée ou sous pression — avec l'impression d'avoir trop à gérer ? De 1 à 7.",
         "likert_7"),
        ("pan_n_03",
         "Nerveuse ou anxieuse — avec des pensées qui tournent, de l'inquiétude ? De 1 à 7.",
         "likert_7"),
        ("pan_n_04",
         "Et épuisée, à bout — vraiment vidée ? De 1 à 7.",
         "likert_7"),
    ],

    "q02_style_cognitif": [
        ("cog_a_01",
         "Quand tu as un problème complexe à résoudre, est-ce que tu préfères naturellement "
         "le découper en étapes avant d'agir ? De 1 (non, j'y vais à l'intuition) "
         "à 7 (oui, j'ai besoin de structurer d'abord).",
         "likert_7"),
        ("cog_a_02",
         "Est-ce que tu te sens à l'aise quand il y a des règles précises et des procédures "
         "claires à suivre ? De 1 à 7.",
         "likert_7"),
        ("cog_a_03",
         "Quand tu raisonnes, tu as tendance à vérifier chaque étape avant de conclure — "
         "ou tu vas assez directement à la conclusion ? De 1 (je conclus vite) "
         "à 7 (je vérifie chaque étape).",
         "likert_7"),
        ("cog_a_04",
         "Est-ce que tu préfères comprendre les détails avant de voir la vue d'ensemble, "
         "ou c'est plutôt l'inverse ? De 1 (vue d'ensemble d'abord) à 7 (détails d'abord).",
         "likert_7"),
        ("cog_i_01",
         "Est-ce qu'il t'arrive souvent de percevoir des solutions ou des connexions entre "
         "idées sans pouvoir l'expliquer clairement sur le moment ? De 1 à 7.",
         "likert_7"),
        ("cog_i_02",
         "Tu préfères comprendre la 'big picture' d'un sujet avant d'aller dans les détails ? "
         "De 1 (non, je préfère les détails d'abord) à 7 (oui, vue d'ensemble avant tout).",
         "likert_7"),
        ("cog_i_03",
         "Est-ce que tu te fies facilement à ton instinct pour prendre des décisions, "
         "même sur des sujets complexes ? De 1 à 7.",
         "likert_7"),
        ("cog_i_04",
         "Est-ce que tu apprends mieux en faisant les choses directement qu'en étudiant "
         "des théories ? De 1 à 7.",
         "likert_7"),
        ("cog_v_01",
         "Pour mémoriser quelque chose, tu préfères l'écrire ou l'expliquer à voix haute "
         "plutôt que de faire un dessin ou un schéma ? De 1 à 7.",
         "likert_7"),
        ("cog_v_02",
         "Quand tu réfléchis, tu utilises plutôt des mots et des phrases dans ta tête ? "
         "De 1 à 7.",
         "likert_7"),
        ("cog_v_03",
         "Tu comprends mieux un concept quand il t'est expliqué en mots, même sans schéma ? "
         "De 1 à 7.",
         "likert_7"),
        ("cog_vs_01",
         "Est-ce que tu retiens mieux les infos quand elles sont sous forme de schéma ou "
         "de diagramme ? De 1 à 7.",
         "likert_7"),
        ("cog_vs_02",
         "Quand tu essaies de te souvenir de quelque chose, tu visualises souvent une image "
         "mentale ? De 1 à 7.",
         "likert_7"),
        ("cog_vs_03",
         "Tu comprends facilement les cartes, graphiques et représentations spatiales ? "
         "De 1 à 7.",
         "likert_7"),
        ("fmt_01",
         "Question de format — pour une explication complexe, tu préfères quoi : "
         "(A) une liste numérotée avec des étapes bien séparées, ou "
         "(B) un texte continu bien rédigé ? Réponds A ou B.",
         "choix_binaire"),
        ("fmt_02",
         "Et pour mémoriser un concept nouveau : (A) le lire ou l'entendre plusieurs fois "
         "formulé de façons différentes, ou (B) voir un schéma ou une représentation visuelle ? "
         "A ou B.",
         "choix_binaire"),
    ],

    "q03_regulation_emotionnelle": [
        ("re_01",
         "Quand tu ressens de l'inquiétude ou de la frustration, est-ce que ça t'aide de te "
         "dire que 'finalement c'est pas si grave' — et est-ce que ça marche vraiment pour toi ? "
         "De 1 (jamais, ça ne marche pas) à 5 (tout le temps, ça m'aide vraiment).",
         "likert_5"),
        ("re_02",
         "Quand tu es dans une situation stressante, tu réussis à la regarder sous un autre angle "
         "— voir le côté positif ou relativiser — pour te sentir mieux ? De 1 à 5.",
         "likert_5"),
        ("re_03",
         "Est-ce que tu utilises des 'rappels mentaux' — te remémorer ce qui va bien, ce que "
         "tu as accompli — pour retrouver un état plus positif ? De 1 à 5.",
         "likert_5"),
        ("re_04",
         "Tu contrôles assez facilement tes émotions en changeant ta façon de penser à une "
         "situation — pas en les refoulant, mais en les recadrant ? De 1 à 5.",
         "likert_5"),
        ("re_05",
         "Quand tu te sens vraiment dépassée, tu réussis à prendre du recul et à relativiser "
         "— sans que ça te coûte trop ? De 1 à 5.",
         "likert_5"),
        ("sup_01",
         "Est-ce que tu gardes souvent tes émotions pour toi — les gens autour de toi ne "
         "voient pas forcément quand tu es stressée ? De 1 à 5.",
         "likert_5"),
        ("sup_02",
         "Tu fais attention à ne pas laisser paraître ce que tu ressens vraiment ? De 1 à 5.",
         "likert_5"),
        ("sup_03",
         "Quand tu as des émotions négatives, tu évites généralement de les exprimer "
         "ouvertement ? De 1 à 5.",
         "likert_5"),
        ("str_01",
         "Ces derniers mois, tu as souvent eu l'impression d'être débordée par des choses "
         "imprévues — des trucs que tu n'avais pas vus venir ? De 1 (jamais) à 5 (très souvent).",
         "likert_5"),
        ("str_02",
         "Tu as eu du mal à contrôler les choses importantes dans ta vie — l'impression "
         "que ça t'échappait ? De 1 à 5.",
         "likert_5"),
        ("str_03",
         "Tu t'es sentie nerveuse ou stressée ces derniers mois ? De 1 à 5.",
         "likert_5"),
        ("str_04",
         "Tu as eu confiance en ta capacité à gérer tes problèmes — même les gros ? "
         "De 1 (pas du tout confiance) à 5 (pleinement confiance).",
         "likert_5"),
        ("str_05",
         "Les difficultés s'accumulaient au point que tu avais du mal à les surmonter ? "
         "De 1 à 5.",
         "likert_5"),
        ("strat_01",
         "Quand tu es très stressée ou épuisée, tu as plutôt tendance à faire quoi : "
         "(A) continuer et pousser pour finir ce que tu as commencé, ou "
         "(B) t'arrêter, récupérer, et reprendre ensuite ? A ou B.",
         "choix_binaire"),
        ("strat_02",
         "Et quand tu as un problème émotionnel difficile : (A) tu en parles pour le traiter "
         "— que ce soit à quelqu'un ou en l'écrivant — ou (B) tu le mets de côté et tu avances ? "
         "A ou B.",
         "choix_binaire"),
    ],

    "q04_motivations_valeurs": [
        ("sdt_aut_01",
         "Première question — est-ce que tu as besoin de choisir toi-même comment tu fais les "
         "choses ? Les approches imposées, ça te freine ? De 1 (pas vraiment, je m'adapte) "
         "à 7 (oui, j'ai besoin d'autonomie sur la méthode).",
         "likert_7"),
        ("sdt_aut_02",
         "Tu travailles nettement mieux quand tu peux organiser ton temps et tes tâches à ta "
         "propre façon ? De 1 à 7.",
         "likert_7"),
        ("sdt_aut_03",
         "Même quand tu demandes des avis, c'est important pour toi d'avoir le dernier mot "
         "sur tes propres décisions ? De 1 à 7.",
         "likert_7"),
        ("sdt_aut_04",
         "Quand quelqu'un te dit précisément quoi faire et comment le faire, tu te sens "
         "frustrée ? De 1 à 7.",
         "likert_7"),
        ("sdt_aut_05",
         "C'est tes propres valeurs qui guident tes actions, pas la pression externe ou "
         "l'approbation des autres ? De 1 à 7.",
         "likert_7"),
        ("sdt_aut_06",
         "Tu as besoin de comprendre le 'pourquoi' d'une tâche pour vraiment t'y impliquer "
         "— pas juste exécuter ? De 1 à 7.",
         "likert_7"),
        ("sdt_comp_01",
         "Tu as besoin de sentir que tu progresses, que tu t'améliores — la stagnation "
         "te pèse vraiment ? De 1 à 7.",
         "likert_7"),
        ("sdt_comp_02",
         "Les défis difficiles te motivent plus que les tâches faciles ? De 1 à 7.",
         "likert_7"),
        ("sdt_comp_03",
         "Tu aimes maîtriser les sujets en profondeur — pas juste avoir une vague idée ? "
         "De 1 à 7.",
         "likert_7"),
        ("sdt_comp_04",
         "Quand tu apprends quelque chose, tu as besoin de vraiment comprendre pour te sentir "
         "à l'aise — pas juste connaître les grandes lignes ? De 1 à 7.",
         "likert_7"),
        ("sdt_comp_05",
         "La qualité de ce que tu produis compte beaucoup pour toi — les approximations "
         "t'insatisfont ? De 1 à 7.",
         "likert_7"),
        ("sdt_comp_06",
         "Tu te sens particulièrement bien quand tu réussis des choses difficiles par "
         "toi-même — sans aide extérieure ? De 1 à 7.",
         "likert_7"),
        ("sdt_app_01",
         "C'est important pour toi que ton travail ait un impact réel sur les autres "
         "— pas juste pour toi ? De 1 à 7.",
         "likert_7"),
        ("sdt_app_02",
         "Tu as besoin de te sentir connectée à quelque chose de plus grand — une mission, "
         "une cause — pour être vraiment engagée ? De 1 à 7.",
         "likert_7"),
        ("sdt_app_03",
         "Le fait d'appartenir à un groupe ou d'être reconnue par tes pairs compte "
         "pour toi ? De 1 à 7.",
         "likert_7"),
        ("sdt_app_04",
         "Tu aimes partager tes réussites et tes projets — pas pour te vanter, mais pour "
         "créer de la connexion ? De 1 à 7.",
         "likert_7"),
        ("sdt_app_05",
         "Tu es plus motivée quand tu travailles pour quelqu'un ou quelque chose en dehors "
         "de toi — pas juste pour toi ? De 1 à 7.",
         "likert_7"),
        ("sdt_app_06",
         "La reconnaissance par des personnes que tu respectes compte vraiment pour toi ? "
         "De 1 à 7.",
         "likert_7"),
    ],

    "q09_hexaco_personnalite": [
        # Dimension H — Honnêteté-Humilité
        ("hex_h_01",
         "Première affirmation — je ne serais jamais prêt(e) à flatter quelqu'un pour obtenir "
         "une faveur, même si ça pourrait m'aider. De 1 (pas du tout d'accord) à 5 (tout à fait d'accord).",
         "likert_5"),
        ("hex_h_02",
         "Si cela m'avantageait, je serais prêt(e) à tromper discrètement les gens. De 1 à 5.",
         "likert_5"),
        ("hex_h_03",
         "Je traite tout le monde de façon égale — que la personne ait du pouvoir ou non, "
         "que je puisse en tirer quelque chose ou pas. De 1 à 5.",
         "likert_5"),
        ("hex_h_04",
         "Le statut social, le luxe, les marques — j'avoue que ça m'attire plus que je ne le "
         "laisse paraître. De 1 à 5.",
         "likert_5"),
        # Dimension E — Émotivité
        ("hex_e_01",
         "Passons aux émotions — quand quelqu'un me blesse, j'ai besoin d'un bon moment avant "
         "de me sentir mieux, même si je ne le montre pas forcément. De 1 à 5.",
         "likert_5"),
        ("hex_e_02",
         "En situation de stress ou de pression, je me détends assez facilement — "
         "ça ne me déstabilise pas longtemps. De 1 à 5.",
         "likert_5"),
        ("hex_e_03",
         "Dans les moments difficiles, j'ai vraiment besoin du soutien de mes proches "
         "pour traverser ça. De 1 à 5.",
         "likert_5"),
        ("hex_e_04",
         "Je suis une personne assez peu sentimentale — les films et les histoires touchantes "
         "ne m'émeuvent pas beaucoup. De 1 à 5.",
         "likert_5"),
        # Dimension X — eXtraversion
        ("hex_x_01",
         "Nouvelle section — en groupe, j'aime être au centre de l'attention, animer, "
         "prendre la parole. De 1 à 5.",
         "likert_5"),
        ("hex_x_02",
         "Je préfère vraiment les activités solitaires ou en petit comité aux grandes "
         "réunions sociales. De 1 à 5.",
         "likert_5"),
        ("hex_x_03",
         "Quand je rencontre de nouvelles personnes, j'entame facilement la conversation "
         "— je n'attends pas que l'autre fasse le premier pas. De 1 à 5.",
         "likert_5"),
        ("hex_x_04",
         "Dans les réunions ou soirées, j'ai souvent l'impression de ne pas avoir "
         "grand-chose à dire. De 1 à 5.",
         "likert_5"),
        # Dimension A — Agréabilité
        ("hex_a_01",
         "Je suis capable de pardonner facilement à quelqu'un qui m'a blessé(e), "
         "sans en garder de rancœur. De 1 à 5.",
         "likert_5"),
        ("hex_a_02",
         "Quand je ne suis pas d'accord avec quelqu'un, je le dis clairement — "
         "sans chercher à arrondir les angles. De 1 à 5.",
         "likert_5"),
        ("hex_a_03",
         "Je préfère faire des compromis plutôt que de maintenir ma position "
         "jusqu'au bout d'une discussion. De 1 à 5.",
         "likert_5"),
        ("hex_a_04",
         "Je peux être assez critique envers les autres — surtout quand je pense "
         "qu'ils font les choses à moitié. De 1 à 5.",
         "likert_5"),
        # Dimension C — Conscienciosité
        ("hex_c_01",
         "Avant de rendre un travail, je vérifie toujours qu'il est exact et "
         "qu'il n'y a pas d'erreurs ou d'oublis. De 1 à 5.",
         "likert_5"),
        ("hex_c_02",
         "J'ai tendance à repousser les tâches — à laisser traîner des choses "
         "que j'aurais dû faire avant. De 1 à 5.",
         "likert_5"),
        ("hex_c_03",
         "J'organise soigneusement mon temps et mes ressources — "
         "j'ai des systèmes, des listes, des méthodes. De 1 à 5.",
         "likert_5"),
        ("hex_c_04",
         "Il m'arrive d'être négligent(e) — de bâcler des tâches ou de ne pas "
         "finir ce que j'ai commencé. De 1 à 5.",
         "likert_5"),
        # Dimension O — Ouverture à l'expérience
        ("hex_o_01",
         "Dernière section — je suis curieux(se) de comprendre comment fonctionne "
         "le monde : les sciences, les comportements humains, les idées. De 1 à 5.",
         "likert_5"),
        ("hex_o_02",
         "Honnêtement, je ne me considère pas comme quelqu'un de très imaginatif "
         "ou créatif. De 1 à 5.",
         "likert_5"),
        ("hex_o_03",
         "Quand j'ai un problème à résoudre, j'explore volontiers des approches "
         "inhabituelles — même si ça prend plus de temps. De 1 à 5.",
         "likert_5"),
        ("hex_o_04",
         "Je préfère les activités et environnements familiers aux expériences "
         "vraiment nouvelles. De 1 à 5.",
         "likert_5"),
    ],

    "q00_profil_complementaire": [
        ("energie_01",
         "Quels moments de la journée tu es la plus concentrée, la plus productive ? "
         "Réponds librement en quelques mots.",
         "texte_libre"),
        ("energie_02",
         "Combien de temps tu tiens en moyenne sur une tâche complexe avant d'avoir besoin "
         "d'une pause ? Là encore, quelques mots suffisent.",
         "texte_libre"),
        ("energie_03",
         "À quoi ressemble une 'surcharge' pour toi — les signes que tu as atteint ta limite ?",
         "texte_libre"),
        ("energie_04",
         "Qu'est-ce qui t'aide à récupérer — pause courte, changement d'activité, silence, "
         "mouvement, autre chose ?",
         "texte_libre"),
        ("energie_05",
         "Tu préfères un rythme soutenu et continu, ou des cycles courts avec des pauses "
         "fréquentes ?",
         "texte_libre"),
        ("access_01",
         "Est-ce que tu as des préférences visuelles — taille de texte, contraste, thème "
         "sombre ou clair, sensibilité à certaines couleurs ?",
         "texte_libre"),
        ("access_02",
         "Et des préférences audio — vitesse de la voix, ton, sensibilité à certains sons ?",
         "texte_libre"),
        ("access_03",
         "Tu préfères interagir par la voix, par l'écrit, ou les deux selon le contexte ?",
         "texte_libre"),
        ("access_04",
         "Est-ce que tu as besoin de sous-titres ou de transcriptions systématiques ?",
         "texte_libre"),
        ("access_05",
         "Tu souhaites des notifications d'ALFRED, et à quelle fréquence — immédiate, groupée, "
         "ou désactivée par défaut ?",
         "texte_libre"),
        ("limites_01",
         "Y a-t-il des sujets que tu préfères qu'ALFRED n'aborde jamais de lui-même ?",
         "texte_libre"),
        ("limites_02",
         "Y a-t-il des sujets sensibles sur lesquels ALFRED doit faire preuve de prudence "
         "particulière ?",
         "texte_libre"),
        ("limites_03",
         "Y a-t-il des tons ou façons de répondre à éviter absolument — en dehors de ceux "
         "qu'on a déjà identifiés ?",
         "texte_libre"),
        ("limites_04",
         "Y a-t-il des actions qu'ALFRED ne doit jamais faire sans confirmation explicite "
         "de ta part ?",
         "texte_libre"),
        ("comm_01",
         "Tu préfères des réponses directes — conclusion d'abord — ou progressives — "
         "raisonnement puis conclusion ?",
         "texte_libre"),
        ("comm_02",
         "Tu préfères systématiquement des étapes numérotées, ou seulement pour les sujets "
         "complexes ?",
         "texte_libre"),
        ("comm_03",
         "Tu as besoin d'exemples concrets même pour des sujets simples ?",
         "texte_libre"),
        ("comm_04",
         "Tu préfères un résumé en fin de réponse longue, ou ça alourdit inutilement ?",
         "texte_libre"),
        ("comm_05",
         "Le niveau d'humour actuel d'ALFRED te convient ? Tu veux plus, moins, ou pareil ?",
         "texte_libre"),
        ("contexte_01",
         "À quoi ressemble une journée type pour toi en ce moment — travail, thèse, projet "
         "ALFRED, vie perso ?",
         "texte_libre"),
        ("contexte_02",
         "Quels sont tes objectifs prioritaires sur les 3 prochains mois ?",
         "texte_libre"),
        ("contexte_03",
         "Y a-t-il des contraintes récurrentes — santé, emploi du temps, charge mentale — "
         "dont ALFRED devrait tenir compte dans ses propositions ?",
         "texte_libre"),
        ("interaction_01",
         "Quel mode par défaut tu veux avec ALFRED ? Le companion_mode actuel te convient, "
         "ou tu préfères un autre mode selon les moments ?",
         "texte_libre"),
        ("interaction_02",
         "Tu veux qu'ALFRED soit proactif — qu'il propose spontanément des actions — ou "
         "qu'il attende toujours une demande explicite ?",
         "texte_libre"),
        ("interaction_03",
         "À quelle fréquence tu veux qu'ALFRED te fasse un point d'avancement sur les "
         "projets en cours ?",
         "texte_libre"),
    ],
}


# ---------------------------------------------------------------------------
# QuestionnaireSession
# ---------------------------------------------------------------------------

class QuestionnaireSession:
    """
    Gère la passation conversationnelle des questionnaires psychométriques.

    Usage typique :
        session = QuestionnaireSession()
        q = session.next_question("q01_bien_etre_subjectif")
        # → ALFRED pose q["text"] dans la conversation
        session.save_answer("q01_bien_etre_subjectif", q["id"], user_response)
        progress = session.get_progress()
    """

    #: Secondes estimées par question
    _SECONDS_PER_QUESTION = 30

    def __init__(self, answers_path: Optional[Path] = None) -> None:
        """
        Charge l'état de session depuis le fichier de réponses.

        :param answers_path: Chemin vers answers_template.json. Si None, utilise
            le chemin par défaut du projet.
        """
        self._path = answers_path or _ANSWERS_PATH
        self._data: Dict[str, Any] = self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> Dict[str, Any]:
        """Charge le fichier JSON des réponses. Crée le fichier depuis le template si absent."""
        if self._path.exists():
            with open(self._path, encoding="utf-8") as f:
                return json.load(f)
        # Fichier absent → créer depuis le template inclus dans ce module
        template_path = _BASE_DIR / "data" / "profile" / "answers_template.json"
        if template_path.exists() and template_path != self._path:
            with open(template_path, encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"_meta": {}, "questionnaires": {}}
        return data

    def _save(self) -> None:
        """Sauvegarde immédiate de l'état courant."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # Met à jour la date de dernière modification dans les méta
        if "_meta" in self._data:
            self._data["_meta"]["last_updated"] = _now_iso()
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Accès aux données d'un questionnaire
    # ------------------------------------------------------------------

    def _get_q_data(self, questionnaire_id: str) -> Optional[Dict[str, Any]]:
        """Retourne les données brutes d'un questionnaire, ou None si inconnu."""
        return self._data.get("questionnaires", {}).get(questionnaire_id)

    def _ensure_q_exists(self, questionnaire_id: str) -> None:
        """Vérifie que le questionnaire existe dans le fichier de données."""
        if self._get_q_data(questionnaire_id) is None:
            raise ValueError(
                f"Questionnaire inconnu : '{questionnaire_id}'. "
                f"IDs valides : {list(QUESTIONNAIRE_META.keys())}"
            )

    # ------------------------------------------------------------------
    # Interface principale
    # ------------------------------------------------------------------

    def next_question(
        self, questionnaire_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Renvoie la prochaine question non répondue du questionnaire.

        :param questionnaire_id: ID du questionnaire (ex: "q01_bien_etre_subjectif")
        :returns: Dict avec les clés :
            - ``id`` (str) : identifiant de la question
            - ``text`` (str) : texte qu'ALFRED doit prononcer/afficher
            - ``type`` (str) : "likert_5" | "likert_7" | "choix_binaire" | "texte_libre"
            - ``index`` (int) : position 0-based dans le questionnaire
            - ``total`` (int) : nombre total de questions
            - ``progress_pct`` (float) : pourcentage d'avancement [0.0–100.0]
        :returns: ``None`` si le questionnaire est completement répondu.
        :raises ValueError: si ``questionnaire_id`` est inconnu.
        """
        self._ensure_q_exists(questionnaire_id)
        q_data = self._get_q_data(questionnaire_id)
        answers: Dict[str, Any] = q_data.get("answers", {})
        items = QUESTIONNAIRE_ITEMS.get(questionnaire_id, [])

        # Trouve le premier item sans réponse (None)
        for index, (qid, text, qtype) in enumerate(items):
            if answers.get(qid) is None:
                total = len(items)
                answered = sum(1 for v in answers.values() if v is not None)
                # Met à jour l'index courant dans session_state
                ss = q_data.setdefault("session_state", {})
                ss["current_question_index"] = index
                if ss.get("started_at") is None:
                    ss["started_at"] = _now_iso()
                self._save()
                return {
                    "id": qid,
                    "text": text,
                    "type": qtype,
                    "index": index,
                    "total": total,
                    "progress_pct": round(answered / total * 100, 1),
                }

        # Toutes les questions ont été répondues
        ss = q_data.setdefault("session_state", {})
        ss["is_complete"] = True
        self._save()
        return None

    def save_answer(
        self,
        questionnaire_id: str,
        question_id: str,
        answer: Any,
    ) -> None:
        """
        Sauvegarde immédiatement la réponse à une question.

        :param questionnaire_id: ID du questionnaire.
        :param question_id: ID de la question (ex: "swls_01").
        :param answer: Valeur de la réponse :
            - int pour likert_5 / likert_7
            - str ("A" | "B") pour choix_binaire
            - str libre pour texte_libre
        :raises ValueError: si le questionnaire ou la question est inconnue,
            ou si la valeur est hors-échelle pour un Likert.
        """
        self._ensure_q_exists(questionnaire_id)
        q_data = self._get_q_data(questionnaire_id)
        answers = q_data.setdefault("answers", {})

        if question_id not in answers:
            raise ValueError(
                f"Question inconnue : '{question_id}' dans '{questionnaire_id}'."
            )

        # Validation de la valeur selon le type
        item_type = self._get_item_type(questionnaire_id, question_id)
        answer = self._validate_answer(answer, item_type, question_id)

        answers[question_id] = answer

        # Mise à jour du session_state
        ss = q_data.setdefault("session_state", {})
        ss["last_saved_at"] = _now_iso()
        ss["questions_answered"] = sum(1 for v in answers.values() if v is not None)
        total = len(QUESTIONNAIRE_ITEMS.get(questionnaire_id, []))
        ss["total_questions"] = total
        ss["is_complete"] = ss["questions_answered"] >= total

        self._save()

    def get_progress(self) -> Dict[str, Dict[str, Any]]:
        """
        Retourne l'état d'avancement de chaque questionnaire.

        :returns: Dict keyed by questionnaire_id. Chaque entrée contient :
            - ``label`` (str) : nom lisible
            - ``answered`` (int) : questions répondues
            - ``total`` (int) : questions totales
            - ``pct_complete`` (float) : pourcentage [0.0–100.0]
            - ``is_complete`` (bool)
            - ``started_at`` (str | None)
            - ``last_saved_at`` (str | None)
            - ``estimated_remaining_min`` (float) : temps restant estimé en minutes
        """
        result: Dict[str, Dict[str, Any]] = {}

        for qid, meta in QUESTIONNAIRE_META.items():
            q_data = self._get_q_data(qid)
            if q_data is None:
                result[qid] = {
                    "label": meta["label"],
                    "answered": 0,
                    "total": len(QUESTIONNAIRE_ITEMS.get(qid, [])),
                    "pct_complete": 0.0,
                    "is_complete": False,
                    "started_at": None,
                    "last_saved_at": None,
                    "estimated_remaining_min": meta["duration_max"],
                }
                continue

            answers = q_data.get("answers", {})
            total = len(QUESTIONNAIRE_ITEMS.get(qid, []))
            answered = sum(1 for v in answers.values() if v is not None)
            remaining_q = total - answered
            remaining_sec = remaining_q * self._SECONDS_PER_QUESTION
            remaining_min = math.ceil(remaining_sec / 60)

            ss = q_data.get("session_state", {})
            result[qid] = {
                "label": meta["label"],
                "answered": answered,
                "total": total,
                "pct_complete": round(answered / total * 100, 1) if total > 0 else 0.0,
                "is_complete": ss.get("is_complete", False),
                "started_at": ss.get("started_at"),
                "last_saved_at": ss.get("last_saved_at"),
                "estimated_remaining_min": remaining_min,
            }

        return result

    def can_compute_partial_scores(self, questionnaire_id: str) -> bool:
        """
        Indique si assez de réponses sont disponibles pour un score partiel indicatif.

        Le seuil minimal est défini dans ``QUESTIONNAIRE_META[qid]["min_for_partial"]``.

        :param questionnaire_id: ID du questionnaire.
        :returns: True si le seuil minimal de réponses est atteint.
        :raises ValueError: si ``questionnaire_id`` est inconnu.
        """
        if questionnaire_id not in QUESTIONNAIRE_META:
            raise ValueError(f"Questionnaire inconnu : '{questionnaire_id}'")

        q_data = self._get_q_data(questionnaire_id)
        if q_data is None:
            return False

        answers = q_data.get("answers", {})
        answered = sum(1 for v in answers.values() if v is not None)
        threshold = QUESTIONNAIRE_META[questionnaire_id]["min_for_partial"]
        return answered >= threshold

    def compute_scores(
        self, questionnaire_id: str, partial: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Calcule les scores d'un questionnaire (complet ou partiel).

        :param questionnaire_id: ID du questionnaire.
        :param partial: Si True, calcule même si le questionnaire est incomplet
            (requiert ``can_compute_partial_scores() == True``).
        :returns: Dict des scores, ou None si pas assez de réponses.
        :raises ValueError: si le questionnaire est inconnu.
        """
        self._ensure_q_exists(questionnaire_id)
        if not partial and not self._get_q_data(questionnaire_id)["session_state"].get(
            "is_complete", False
        ):
            return None
        if partial and not self.can_compute_partial_scores(questionnaire_id):
            return None

        q_data = self._get_q_data(questionnaire_id)
        answers = q_data.get("answers", {})

        if questionnaire_id == "q01_bien_etre_subjectif":
            scores = self._score_q01(answers)
        elif questionnaire_id == "q02_style_cognitif":
            scores = self._score_q02(answers)
        elif questionnaire_id == "q03_regulation_emotionnelle":
            scores = self._score_q03(answers)
        elif questionnaire_id == "q04_motivations_valeurs":
            scores = self._score_q04(answers)
        elif questionnaire_id == "q09_hexaco_personnalite":
            scores = self._score_q09(answers)
        else:
            return None  # questionnaire qualitatif (q00) — pas de scoring numérique

        scores["computed_at"] = _now_iso()
        scores["is_partial"] = partial

        # Persistance des scores dans le fichier
        q_data["scores"] = scores
        self._save()
        return scores

    # ------------------------------------------------------------------
    # Méthodes de scoring par questionnaire
    # ------------------------------------------------------------------

    @staticmethod
    def _mean(values: List[Optional[Any]]) -> Optional[float]:
        """Calcule la moyenne en ignorant les None."""
        nums = [v for v in values if isinstance(v, (int, float))]
        return round(sum(nums) / len(nums), 2) if nums else None

    @staticmethod
    def _sum_likert(values: List[Optional[Any]]) -> Optional[int]:
        """Somme les valeurs numériques en ignorant les None."""
        nums = [v for v in values if isinstance(v, (int, float))]
        return sum(nums) if nums else None

    def _score_q01(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Q01 — SWLS + PANAS."""
        swls_keys = ["swls_01", "swls_02", "swls_03", "swls_04", "swls_05"]
        panp_keys = ["pan_p_01", "pan_p_02", "pan_p_03", "pan_p_04", "pan_p_05"]
        pann_keys = ["pan_n_01", "pan_n_02", "pan_n_03", "pan_n_04"]

        swls_total = self._sum_likert([answers.get(k) for k in swls_keys])
        panas_pos = self._sum_likert([answers.get(k) for k in panp_keys])
        panas_neg = self._sum_likert([answers.get(k) for k in pann_keys])

        return {
            "swls_total": swls_total,
            "panas_positif": panas_pos,
            "panas_negatif": panas_neg,
        }

    def _score_q02(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Q02 — Style cognitif."""
        a_keys = ["cog_a_01", "cog_a_02", "cog_a_03", "cog_a_04"]
        i_keys = ["cog_i_01", "cog_i_02", "cog_i_03", "cog_i_04"]
        v_keys = ["cog_v_01", "cog_v_02", "cog_v_03"]
        vs_keys = ["cog_vs_01", "cog_vs_02", "cog_vs_03"]

        score_a = self._mean([answers.get(k) for k in a_keys])
        score_i = self._mean([answers.get(k) for k in i_keys])
        score_v = self._mean([answers.get(k) for k in v_keys])
        score_vs = self._mean([answers.get(k) for k in vs_keys])

        profil_ai = None
        if score_a is not None and score_i is not None:
            diff = score_a - score_i
            if diff > 1.5:
                profil_ai = "analytique"
            elif diff < -1.5:
                profil_ai = "intuitif"
            else:
                profil_ai = "mixte"

        profil_vvs = None
        if score_v is not None and score_vs is not None:
            diff = score_v - score_vs
            if diff > 1.0:
                profil_vvs = "verbal"
            elif diff < -1.0:
                profil_vvs = "visuel_spatial"
            else:
                profil_vvs = "mixte"

        return {
            "score_analytique": score_a,
            "score_intuitif": score_i,
            "profil_ai": profil_ai,
            "score_verbal": score_v,
            "score_visuel_spatial": score_vs,
            "profil_vvs": profil_vvs,
        }

    def _score_q03(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Q03 — Régulation émotionnelle."""
        re_keys = ["re_01", "re_02", "re_03", "re_04", "re_05"]
        sup_keys = ["sup_01", "sup_02", "sup_03"]
        str_keys = ["str_01", "str_02", "str_03", "str_04", "str_05"]

        rc = self._mean([answers.get(k) for k in re_keys])
        sup = self._mean([answers.get(k) for k in sup_keys])

        # PSS : str_04 est un item positif → inverser (score = 6 - réponse sur échelle 1-5)
        str_values = []
        for k in str_keys:
            v = answers.get(k)
            if isinstance(v, (int, float)):
                str_values.append(6 - v if k == "str_04" else v)
        pss = self._sum_likert(str_values) if str_values else None

        return {
            "reevaluation_cognitive": rc,
            "suppression": sup,
            "stress_percu_pss": pss,
        }

    def _score_q09(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Q09 — HEXACO-24. Items _02 et _04 de chaque dimension sont inversés (6 - valeur)."""
        dims = {
            "honnetete_humilite": ["hex_h_01", "hex_h_02", "hex_h_03", "hex_h_04"],
            "emotivite":          ["hex_e_01", "hex_e_02", "hex_e_03", "hex_e_04"],
            "extraversion":       ["hex_x_01", "hex_x_02", "hex_x_03", "hex_x_04"],
            "agreabilite":        ["hex_a_01", "hex_a_02", "hex_a_03", "hex_a_04"],
            "conscienciosite":    ["hex_c_01", "hex_c_02", "hex_c_03", "hex_c_04"],
            "ouverture":          ["hex_o_01", "hex_o_02", "hex_o_03", "hex_o_04"],
        }
        result: Dict[str, Any] = {}
        for dim_name, keys in dims.items():
            values = []
            for k in keys:
                v = answers.get(k)
                if isinstance(v, (int, float)):
                    # _02 et _04 sont inversés (se terminent par "02" ou "04")
                    values.append(6 - v if k.endswith("_02") or k.endswith("_04") else v)
            result[dim_name] = self._mean(values)
        return result

    def _score_q04(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        """Q04 — Motivations SDT."""
        aut_keys = [f"sdt_aut_0{i}" for i in range(1, 7)]
        comp_keys = [f"sdt_comp_0{i}" for i in range(1, 7)]
        app_keys = [f"sdt_app_0{i}" for i in range(1, 7)]

        aut = self._mean([answers.get(k) for k in aut_keys])
        comp = self._mean([answers.get(k) for k in comp_keys])
        app = self._mean([answers.get(k) for k in app_keys])

        dominante = None
        if all(v is not None for v in [aut, comp, app]):
            scores_map = {"autonomie": aut, "competence": comp, "appartenance": app}
            max_k = max(scores_map, key=lambda k: scores_map[k])
            max_v = scores_map[max_k]
            others = [v for k, v in scores_map.items() if k != max_k]
            dominante = max_k if (max_v - max(others)) >= 0.5 else "equilibre"

        return {
            "autonomie": aut,
            "competence": comp,
            "appartenance": app,
            "motivation_dominante": dominante,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_item_type(questionnaire_id: str, question_id: str) -> Optional[str]:
        """Retourne le type de réponse attendu pour un item donné."""
        for qid, text, qtype in QUESTIONNAIRE_ITEMS.get(questionnaire_id, []):
            if qid == question_id:
                return qtype
        return None

    @staticmethod
    def _validate_answer(answer: Any, item_type: Optional[str], question_id: str) -> Any:
        """
        Valide et normalise une réponse selon le type d'item.

        :raises ValueError: si la valeur est hors-échelle ou invalide.
        """
        if item_type == "likert_5":
            val = int(answer)
            if not (1 <= val <= 5):
                raise ValueError(
                    f"Réponse hors-échelle pour '{question_id}' "
                    f"(likert_5, attendu 1-5, reçu {val})."
                )
            return val
        if item_type == "likert_7":
            val = int(answer)
            if not (1 <= val <= 7):
                raise ValueError(
                    f"Réponse hors-échelle pour '{question_id}' "
                    f"(likert_7, attendu 1-7, reçu {val})."
                )
            return val
        if item_type == "choix_binaire":
            val = str(answer).strip().upper()
            if val not in ("A", "B"):
                raise ValueError(
                    f"Réponse invalide pour '{question_id}' "
                    f"(choix_binaire, attendu A ou B, reçu '{answer}')."
                )
            return val
        # texte_libre ou None → retourner tel quel
        return answer


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    """Retourne l'horodatage UTC courant au format ISO 8601."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
