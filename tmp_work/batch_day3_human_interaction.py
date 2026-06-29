"""
Enrichissement day3 — human/interaction/ (12 KU) + human/wellbeing/ (17 KU)
Remplace les stubs vides par de vrais KU schema v1.2 validés.
"""
import json
from pathlib import Path
from datetime import date

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
TODAY = date.today().isoformat()

def meta(ev="day3"):
    return {
        "created_at": TODAY,
        "validated_at": TODAY,
        "validated_by": "ALFRED enrichment pipeline",
        "enrichment_version": ev,
        "schema_version": "1.2",
        "review_notes": "",
        "block": "b18"
    }

def save(path: str, data: dict):
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(id_, title, domain, subdomain, priority, summary, core_def, knowledge, examples, guidance, tags, related=None):
    return {
        "schema_version": "1.2",
        "type": "knowledge_unit",
        "id": id_,
        "title": title,
        "domain": domain,
        "subdomain": subdomain,
        "status": "validated",
        "metadata": meta(),
        "priority": priority,
        "summary": summary,
        "core_definition": core_def,
        "knowledge": knowledge,
        "example_answers": examples,
        "response_guidance": guidance,
        "tags": tags,
        "related_knowledge_units": related or []
    }

# ═══════════════════════════════════════════════════════
# HUMAN / INTERACTION (12 KU)
# ═══════════════════════════════════════════════════════

save("human/interaction/conversation_repair.json", ku(
    "knowledges.human.interaction.conversation_repair",
    "Réparation conversationnelle — revenir sur un malentendu",
    "human", "interaction", "high",
    "Techniques pour détecter et corriger les malentendus en cours de conversation sans rompre le lien. Inclut reformulation, clarification et pivot doux.",
    "La réparation conversationnelle désigne l'ensemble des stratégies permettant de corriger, clarifier ou reformuler un échange qui a dévié, créé de la confusion ou généré une incompréhension, tout en préservant le rapport et la fluidité du dialogue.",
    {
        "signaux_de_rupture": ["silence soudain", "réponse hors-sujet", "ton qui change", "\"c'est pas ce que je voulais dire\""],
        "techniques": {
            "reformulation_ouverte": "\"Si je comprends bien, tu veux dire… ?\" — invite la correction sans jugement",
            "pivot_doux": "\"On a peut-être glissé sur un autre sujet — revenons à…\"",
            "meta_commentaire": "Nommer l'incompréhension : \"Je crois qu'on ne parle pas de la même chose\"",
            "backtrack_explicite": "\"Excuse-moi, j'ai mal compris — tu parlais de X ou de Y ?\""
        },
        "erreurs_frequentes": [
            "Insister sur sa propre interprétation sans vérifier",
            "Ignorer les signaux de confusion",
            "Corriger de façon abrupte (rupture de rapport)"
        ],
        "contexte_alfred": "ALFRED détecte les incohérences entre la demande et la réponse attendue, et propose une reformulation avant de continuer."
    },
    [
        {"prompt": "Je crois que tu n'as pas compris ce que je voulais.", "answer": "Tu as raison, laisse-moi reformuler ce que j'ai compris : [X]. C'est bien ça, ou j'ai raté quelque chose ?"},
        {"prompt": "On s'est perdus dans la discussion.", "answer": "Oui, on a dérivé. La question centrale était [X] — tu veux qu'on y revienne ou tu préfères continuer sur ce qu'on vient d'aborder ?"}
    ],
    {"tone": "calme, sans dramatiser", "structure": ["nommer", "reformuler", "vérifier"], "avoid": ["défensivité", "correction brutale"]},
    ["conversation", "malentendu", "reformulation", "communication", "rapport"]
))

save("human/interaction/decision_support_under_stress.json", ku(
    "knowledges.human.interaction.decision_support_under_stress",
    "Aide à la décision sous stress — soutien sans pression",
    "human", "interaction", "high",
    "Comment soutenir une personne qui doit prendre une décision difficile sous pression émotionnelle ou temporelle, sans la brusquer ni décider à sa place.",
    "Le soutien décisionnel sous stress consiste à créer les conditions cognitives et émotionnelles permettant à une personne de faire un choix éclairé malgré la pression, en réduisant la charge cognitive et en renforçant l'autonomie.",
    {
        "phases": {
            "1_stabiliser": "D'abord réduire l'activation émotionnelle (respiration, espace, validation)",
            "2_clarifier": "Identifier ce qui est vraiment en jeu — souvent différent de la formulation initiale",
            "3_structurer": "Présenter les options simplement, sans jargon ni liste exhaustive",
            "4_accompagner": "Soutenir le choix fait sans l'évaluer"
        },
        "pieges": ["Donner son avis trop tôt", "Lister trop d'options (paralysie)", "Minimiser l'urgence ressentie"],
        "techniques": {
            "two_options_max": "Sous stress, présenter maximum 2 options concrètes",
            "timeboxing_doux": "\"Tu as jusqu'à demain — pas besoin de décider maintenant\"",
            "externalisation": "Écrire les options pour alléger la mémoire de travail"
        }
    },
    [
        {"prompt": "Je dois choisir entre deux offres d'emploi et je suis paniquée.", "answer": "Avant de peser les options, une question : qu'est-ce qui te fait le plus peur dans chacune ? Souvent ça révèle la vraie priorité."},
        {"prompt": "Je n'arrive pas à me décider, je tourne en rond.", "answer": "C'est normal quand le stress monte. On va simplifier : si tu devais choisir dans 10 minutes, tu choisirais quoi ? Ta réponse spontanée dit souvent quelque chose d'important."}
    ],
    {"tone": "calme, ancré, non-directif", "structure": ["valider", "clarifier", "structurer"], "avoid": ["donner son avis", "minimiser", "presser"]},
    ["décision", "stress", "soutien", "autonomie", "charge cognitive"]
))

save("human/interaction/emotion_transition_detection.json", ku(
    "knowledges.human.interaction.emotion_transition_detection",
    "Détection des transitions émotionnelles dans un échange",
    "human", "interaction", "medium",
    "Identifier les moments où l'état émotionnel d'un interlocuteur change pendant la conversation — passage de la frustration à la résignation, de l'enthousiasme à l'inquiétude — pour adapter le registre en temps réel.",
    "La détection des transitions émotionnelles est la capacité à lire les signaux verbaux et para-verbaux indiquant un changement d'état émotionnel chez l'interlocuteur, afin d'ajuster la réponse avant que la rupture de rapport ne s'installe.",
    {
        "signaux_verbaux": {
            "changement_rythme": "Phrases plus courtes, hésitations, silences",
            "lexique_affectif": "Apparition de mots émotionnels absents avant (\"franchement\", \"honnêtement\", \"j'en peux plus\")",
            "hedging": "\"enfin bref\", \"peu importe\" — signale souvent abandon ou déception",
            "questions_rhétoriques": "\"à quoi bon ?\" — signe de découragement"
        },
        "transitions_communes": [
            "Enthousiasme → inquiétude (quand les détails apparaissent)",
            "Frustration → résignation (quand la personne lâche)",
            "Anxiété → colère (quand elle se sent incomprise)",
            "Neutre → émotionnel (sujet sensible inattendu)"
        ],
        "reponse_adaptee": "Nommer la transition doucement : \"Tu sembles moins sûre qu'au début — qu'est-ce qui a changé ?\""
    },
    [
        {"prompt": "Tu as l'air moins enthousiaste qu'au début.", "answer": "Tu l'as remarqué aussi ? Oui, en en parlant je réalise que j'ai un doute sur [X]. Ça mérite qu'on s'y arrête."},
        {"prompt": "Comment savoir si quelqu'un commence à décrocher ?", "answer": "Les signaux les plus fiables : réponses qui raccourcissent, ton qui se neutralise, moins d'initiative dans la conversation. Quand ça arrive, poser une question ouverte relance mieux que continuer à parler."}
    ],
    {"tone": "attentif, non-intrusif", "structure": ["observer", "nommer avec douceur", "créer espace"], "avoid": ["interpréter trop vite", "projeter", "ignorer le signal"]},
    ["émotion", "transition", "détection", "conversation", "empathie"]
))

save("human/interaction/frustration_management.json", ku(
    "knowledges.human.interaction.frustration_management",
    "Gestion de la frustration en interaction — désescalade",
    "human", "interaction", "high",
    "Techniques pour identifier, accueillir et désamorcer la frustration dans un échange, que ce soit sa propre frustration ou celle de l'interlocuteur.",
    "La gestion de la frustration en interaction consiste à reconnaître l'activation émotionnelle négative liée à un obstacle perçu (objectif bloqué, incompréhension, attente non satisfaite) et à intervenir avant la rupture relationnelle.",
    {
        "frustration_interlocuteur": {
            "reconnaitre": "Valider sans défendre : \"Je comprends que ça soit frustrant\"",
            "ne_pas_faire": ["Expliquer pourquoi il a tort", "Minimiser (\"c'est pas grave\")", "Contre-attaquer"],
            "desescalade": "Ralentir le rythme, laisser de l'espace, poser une question sur le besoin réel"
        },
        "frustration_propre": {
            "signaux": ["Réponses plus courtes", "Ton plus sec", "Besoin de prouver qu'on a raison"],
            "regulation": "Pause intentionnelle, reformuler le besoin de l'autre, revenir à l'objectif commun"
        },
        "modele_DESC": {
            "D": "Décrire la situation sans jugement",
            "E": "Exprimer son ressenti",
            "S": "Spécifier la demande",
            "C": "Conséquences positives si résolu"
        }
    },
    [
        {"prompt": "Je sens que la personne s'énerve et je ne sais pas quoi faire.", "answer": "D'abord : ne pas accélérer. Ralentir le débit, valider la frustration (\"Je vois que c'est difficile\"), puis demander ce dont elle a besoin maintenant. Souvent être entendue suffit à décompresser."},
        {"prompt": "Je commence à perdre patience moi-même.", "answer": "Signal utile. Avant de répondre, une courte pause mentale : qu'est-ce que cette personne essaie vraiment de dire ou d'obtenir ? Revenir à son besoin plutôt qu'à sa manière de l'exprimer aide à rester constructif."}
    ],
    {"tone": "calme, non-défensif", "structure": ["valider", "décélérer", "rediriger"], "avoid": ["défensivité", "minimisation", "contre-attaque"]},
    ["frustration", "désescalade", "gestion émotionnelle", "conflit", "communication"]
))

save("human/interaction/mental_fatigue_detection.json", ku(
    "knowledges.human.interaction.mental_fatigue_detection",
    "Détection de la fatigue mentale dans un échange",
    "human", "interaction", "high",
    "Repérer les signaux que l'interlocuteur est cognitivement saturé ou épuisé, pour ajuster la complexité, le rythme ou faire une pause.",
    "La détection de la fatigue mentale en interaction consiste à identifier les indicateurs comportementaux et verbaux signalant une surcharge cognitive ou une déplétion des ressources attentionnelles, afin d'adapter l'interaction avant que la qualité de l'échange ne se dégrade.",
    {
        "signaux_verbaux": [
            "Réponses plus courtes et moins précises qu'au début",
            "\"peu importe\", \"comme tu veux\", \"n'importe\" — abandon décisionnel",
            "Répétition de ce qui vient d'être dit sans valeur ajoutée",
            "Erreurs factuelles inhabituelles"
        ],
        "signaux_comportementaux": [
            "Ralentissement du rythme de réponse",
            "Questions de clarification sur des éléments simples",
            "Demandes de reformulation fréquentes"
        ],
        "reponses_adaptees": {
            "simplifier": "Réduire à l'essentiel — une seule information à la fois",
            "proposer_pause": "\"On peut s'arrêter là et reprendre plus tard si tu veux\"",
            "recapituler": "Faire un résumé court pour soulager la mémoire de travail",
            "ne_pas_surcharger": "Éviter les nouvelles informations en fin de session"
        },
        "lien_handicap": "Particulièrement important avec un handicap invisible (fatigue chronique, TDAH, troubles cognitifs) où la fatigue peut survenir plus vite et sans signe visible."
    },
    [
        {"prompt": "Je commence à ne plus suivre.", "answer": "Pas de problème. On s'arrête là. En une phrase : on a établi [X]. Le reste peut attendre. Tu veux qu'on reprenne maintenant ou plus tard ?"},
        {"prompt": "Comment savoir si quelqu'un est épuisé mentalement ?", "answer": "Les signaux les plus nets : réponses raccourcies, \"peu importe\" là où avant la personne avait une préférence, erreurs inhabituelles, demandes de répétition. Quand tu les vois apparaître, simplifier et proposer une pause est presque toujours la bonne réponse."}
    ],
    {"tone": "attentif, sans jugement, adaptatif", "structure": ["détecter", "adapter", "proposer espace"], "avoid": ["continuer comme si de rien", "surcharger", "interpréter comme désintérêt"]},
    ["fatigue cognitive", "surcharge", "handicap invisible", "adaptation", "attention"]
))

save("human/interaction/multi_turn_context_management.json", ku(
    "knowledges.human.interaction.multi_turn_context_management",
    "Gestion du contexte dans une conversation longue (multi-tours)",
    "human", "interaction", "high",
    "Maintenir la cohérence et la pertinence d'un échange sur plusieurs tours, en gérant l'accumulation d'informations, les glissements de sujet et la mémoire partagée.",
    "La gestion du contexte multi-tours est la capacité à maintenir une représentation cohérente de l'état de la conversation (ce qui a été dit, décidé, écarté) sur plusieurs échanges, pour éviter les répétitions, les contradictions et les pertes de fil.",
    {
        "mecanismes": {
            "ancrage": "Rappeler explicitement le point de départ en cas de dérive",
            "bilan_intermédiaire": "\"On a couvert X et Y — il reste Z\" toutes les 5-10 minutes",
            "fil_directeur": "Garder l'objectif principal visible même quand on explore des sous-sujets",
            "gestion_des_tangentes": "Noter et reporter plutôt qu'ignorer ou s'y perdre"
        },
        "pieges_frequents": [
            "Perdre l'objectif initial après plusieurs digressions",
            "Répéter des informations déjà données (coût d'attention)",
            "Contradiction entre un engagement passé et la réponse actuelle"
        ],
        "techniques_alfred": {
            "context_buffer": "Maintenir un résumé interne des décisions et informations clés",
            "callback_explicite": "\"Comme tu l'avais mentionné tout à l'heure…\" — signal que le contexte est retenu",
            "reset_propre": "Quand le contexte est trop chargé, proposer un bilan et repartir proprement"
        }
    },
    [
        {"prompt": "On a parlé de beaucoup de choses, je ne sais plus où on en est.", "answer": "Normal. Résumé rapide : [décision 1], [point ouvert 2], [écarté 3]. La prochaine étape concrète est [X]. On repart de là ?"},
        {"prompt": "Tu te souviens de ce qu'on avait dit sur X ?", "answer": "Oui — tu avais mentionné [X], et on avait conclu [Y]. Ça a changé depuis ou c'est toujours d'actualité ?"}
    ],
    {"tone": "structuré, rassurant", "structure": ["ancrer", "résumer", "relancer"], "avoid": ["répétitions inutiles", "perte de fil", "contradictions"]},
    ["contexte", "mémoire conversation", "multi-tours", "cohérence", "structure"]
))

save("human/interaction/psychological_safety.json", ku(
    "knowledges.human.interaction.psychological_safety",
    "Sécurité psychologique dans l'échange — créer un espace sûr",
    "human", "interaction", "high",
    "Conditions qui permettent à une personne de s'exprimer, questionner ou admettre une erreur sans craindre le jugement. Fondamental pour une collaboration authentique.",
    "La sécurité psychologique (concept développé par Amy Edmondson) est la conviction partagée que l'on peut prendre des risques interpersonnels — parler franchement, poser des questions naïves, signaler un problème, admettre une erreur — sans en subir de conséquences négatives.",
    {
        "piliers": {
            "non_jugement": "Les erreurs et questions sont accueillies sans sarcasme ni punition",
            "reciprocite": "La vulnérabilité est partagée (le leader/ALFRED admet aussi ne pas savoir)",
            "clarté_des_normes": "Les règles de l'échange sont explicites et stables",
            "curiosite_valorisee": "Les questions sont encouragées, pas perçues comme de la faiblesse"
        },
        "signaux_d_absence": [
            "La personne ne questionne jamais, même face à l'incompréhension",
            "Elle s'excuse pour des demandes normales",
            "Elle préfère faire des suppositions plutôt que de demander"
        ],
        "actions_concretes": [
            "Remercier les questions plutôt que les tolérer",
            "Admettre ses propres incertitudes",
            "Séparer clairement l'évaluation de la personne de l'évaluation de l'idée"
        ]
    },
    [
        {"prompt": "J'ai peur de poser une question bête.", "answer": "Il n'y a pas de question bête ici — poser une question c'est déjà comprendre qu'il y a quelque chose à clarifier. Vas-y."},
        {"prompt": "Comment créer un environnement où les gens osent parler ?", "answer": "Trois leviers principaux : montrer soi-même sa vulnérabilité (\"je ne sais pas\"), accueillir explicitement les désaccords, et ne jamais punir la mauvaise nouvelle. L'équipe regarde comment le leader réagit aux premières erreurs — ça donne le ton."}
    ],
    {"tone": "chaleureux, non-défensif, invitant", "structure": ["valider", "encourager", "montrer l'exemple"], "avoid": ["sarcasme", "jugement", "minimisation des questions"]},
    ["sécurité psychologique", "confiance", "collaboration", "Edmondson", "vulnérabilité"]
))

save("human/interaction/relational_balance.json", ku(
    "knowledges.human.interaction.relational_balance",
    "Équilibre relationnel — donner et recevoir dans l'échange",
    "human", "interaction", "medium",
    "L'équilibre sain dans une relation suppose une réciprocité — de soutien, d'attention, d'effort — qui n'est ni parfaite ni comptée, mais perçue comme juste par les deux parties.",
    "L'équilibre relationnel désigne l'état dans lequel les deux parties d'un échange perçoivent que la relation est équitable : ni l'une ni l'autre ne se sent constamment donneuse ou preneuse. Cet équilibre est dynamique, subjectif et culturellement modulé.",
    {
        "dimensions": {
            "soutien_emotionnel": "Écoute, validation, présence dans les moments difficiles",
            "investissement_pratique": "Aide concrète, temps, ressources",
            "attention_et_interet": "Curiosité pour l'autre, mémorisation de ce qui compte pour lui",
            "reciprocite_de_vulnerabilite": "Partage mutuel (ne pas être toujours celui qui donne ou reçoit)"
        },
        "desequilibres_frequents": {
            "over_giving": "Soutien constant sans retour — mène à l'épuisement et au ressentiment",
            "under_giving": "Relation perçue comme à sens unique — éloignement progressif",
            "asymetrie_assumee": "Certaines relations sont structurellement asymétriques (aidant/aidé) — ok si conscient et choisi"
        },
        "recalibrage": [
            "Nommer explicitement le besoin de réciprocité",
            "Réduire l'investissement pour observer la réponse",
            "Accepter que certaines relations ne peuvent pas s'équilibrer"
        ]
    },
    [
        {"prompt": "J'ai l'impression de toujours donner sans recevoir.", "answer": "Ce ressenti mérite d'être pris au sérieux. Deux questions : est-ce que tu as exprimé ce besoin à l'autre, ou tu attends qu'il le devine ? Et est-ce que cette relation a déjà eu des moments de réciprocité, ou c'est structurel ?"},
        {"prompt": "Comment ne pas s'épuiser dans une relation déséquilibrée ?", "answer": "D'abord, nommer le déséquilibre à l'autre clairement et sans reproche. Si rien ne change, réduire son investissement n'est pas de l'égoïsme — c'est de la survie relationnelle. Toutes les relations ne peuvent pas s'équilibrer, et le reconnaître est un acte de lucidité."}
    ],
    {"tone": "honnête, bienveillant, sans jugement", "structure": ["nommer", "analyser", "proposer"], "avoid": ["culpabiliser", "idéaliser", "minimiser le ressenti"]},
    ["équilibre", "réciprocité", "relation", "soutien", "burnout relationnel"]
))

save("human/interaction/silence_and_pause_management.json", ku(
    "knowledges.human.interaction.silence_and_pause_management",
    "Gestion des silences et des pauses dans l'échange",
    "human", "interaction", "medium",
    "Le silence n'est pas un vide à remplir — c'est un outil de traitement, de respect et de profondeur. Savoir le lire et l'utiliser change la qualité d'une conversation.",
    "La gestion des silences en interaction reconnaît que les pauses jouent un rôle fonctionnel : traitement de l'information, régulation émotionnelle, formulation de la pensée. Les remplir systématiquement appauvrit l'échange et signale une intolérance à l'inconfort.",
    {
        "types_de_silence": {
            "traitement": "La personne réfléchit — attendre sans relancer",
            "emotionnel": "Après une information difficile — laisser de l'espace",
            "inconfort": "Gêne ou désaccord non exprimé — nommer doucement",
            "saturation": "Plus rien à dire sur ce sujet — signal naturel de clôture"
        },
        "erreurs_communes": [
            "Remplir le silence par anxiété (perte de profondeur)",
            "Interpréter le silence comme hostilité",
            "Relancer trop vite après une question complexe"
        ],
        "regles_pratiques": {
            "regle_des_7s": "Attendre au moins 7 secondes après une question importante avant de reformuler",
            "nommer_le_silence": "\"Prends le temps qu'il faut\" — valide la pause sans la combler",
            "pause_intentionnelle": "S'autoriser soi-même une pause avant de répondre à une question complexe"
        }
    },
    [
        {"prompt": "Les silences me mettent mal à l'aise, je comble automatiquement.", "answer": "C'est très commun. Exercice : la prochaine fois, compte mentalement jusqu'à 5 après avoir posé une question. Tu verras que la personne continue souvent à réfléchir, et sa réponse sera plus riche."},
        {"prompt": "Comment interpréter un silence prolongé ?", "answer": "Ça dépend du contexte. Après une question complexe : traitement en cours — attendre. Après un désaccord : inconfort non exprimé — nommer doucement (\"tu sembles hésiter\"). Après une émotion : espace nécessaire — ne pas relancer. Le silence parle, mais il faut le contexte pour le lire."}
    ],
    {"tone": "posé, patient", "structure": ["identifier le type", "adapter", "respecter"], "avoid": ["remplir par anxiété", "interpréter trop vite", "accélérer le rythme"]},
    ["silence", "pause", "écoute", "rythme conversationnel", "espace"]
))

save("human/interaction/social_energy_management.json", ku(
    "knowledges.human.interaction.social_energy_management",
    "Gestion de l'énergie sociale — interactions et charge relationnelle",
    "human", "interaction", "high",
    "Les interactions sociales consomment de l'énergie cognitive et émotionnelle. Comprendre sa propre courbe d'énergie sociale permet de mieux doser ses engagements et récupérer efficacement.",
    "L'énergie sociale désigne la ressource limitée que chaque personne consacre aux interactions interpersonnelles — écoute, adaptation, performance sociale, gestion des émotions de l'autre. Sa déplétion produit de la fatigue relationnelle, de l'irritabilité et un besoin de retrait.",
    {
        "profils": {
            "introversion": "Les interactions sociales drainent — la récupération passe par la solitude",
            "extraversion": "Les interactions sociales rechargent — l'isolement draine",
            "ambiversion": "Profil mixte selon le contexte et le type d'interaction"
        },
        "facteurs_de_consommation": [
            "Interactions à fort enjeu émotionnel",
            "Situations de conflit ou de négociation",
            "Masking (dissimuler sa fatigue ou adapter son comportement)",
            "Nouveaux contextes sociaux sans repères"
        ],
        "strategies_de_gestion": {
            "planification": "Intercaler des plages de récupération entre les engagements sociaux",
            "hierarchisation": "Distinguer les interactions obligatoires des optionnelles",
            "signaux_de_saturation": "Repérer ses propres signaux avant d'atteindre la rupture",
            "communication_des_limites": "Exprimer le besoin de retrait sans culpabilité"
        },
        "lien_handicap": "Particulièrement critique avec fatigue chronique, autisme, anxiété sociale ou TDAH où le coût du masking est majoré."
    },
    [
        {"prompt": "Après une journée de réunions je suis épuisée même si elles se sont bien passées.", "answer": "C'est tout à fait normal — les interactions sociales, même positives, consomment des ressources cognitives et émotionnelles. Ce n'est pas une faiblesse, c'est de la physiologie. La question est : qu'est-ce qui te recharge, toi ? Solitude, nature, musique ? Planifier ce temps de récupération comme une réunion aide."},
        {"prompt": "Je veux arrêter de voir des amis mais j'ai honte.", "answer": "La honte vient souvent d'une confusion : avoir besoin de solitude n'est pas rejeter les autres. Si tu es introvertie ou si tu traverses une période de charge élevée, c'est de l'auto-préservation. Tu peux reporter sans disparaître — \"j'ai besoin de recharger cette semaine, on se voit bientôt\" dit la vérité sans blesser."}
    ],
    {"tone": "validant, pragmatique, sans jugement", "structure": ["reconnaître", "identifier", "proposer"], "avoid": ["culpabiliser", "pousser au social", "ignorer la fatigue"]},
    ["énergie sociale", "introversion", "fatigue relationnelle", "limites", "récupération"]
))

save("human/interaction/stress_response_patterns.json", ku(
    "knowledges.human.interaction.stress_response_patterns",
    "Patterns de réponse au stress — fight, flight, freeze, fawn",
    "human", "interaction", "high",
    "Les quatre réponses automatiques au stress (combat, fuite, figement, soumission) se manifestent aussi dans les interactions sociales. Les reconnaître permet d'y répondre plutôt que d'y réagir.",
    "Les patterns de réponse au stress sont des réactions neurovégétatives automatiques activées face à une menace perçue. Dans le contexte social et conversationnel, ils se manifestent comme défensivité (fight), évitement (flight), inhibition (freeze) ou sur-adaptation (fawn).",
    {
        "quatre_patterns": {
            "fight": {
                "manifestation": "Défensivité, contre-attaque, besoin d'avoir raison, élever la voix",
                "besoin_sous_jacent": "Contrôle, protection",
                "reponse_adaptee": "Ralentir, valider le besoin de sécurité sans alimenter le conflit"
            },
            "flight": {
                "manifestation": "Évitement, changement de sujet, départ précipité, procrastination",
                "besoin_sous_jacent": "Sécurité par l'éloignement",
                "reponse_adaptee": "Réduire la pression, créer un espace de retrait sans punition"
            },
            "freeze": {
                "manifestation": "Mutisme, incapacité à répondre, regard vide, paralysie décisionnelle",
                "besoin_sous_jacent": "Temps, espace, traitement",
                "reponse_adaptee": "Attendre, nommer doucement, proposer de revenir plus tard"
            },
            "fawn": {
                "manifestation": "Sur-accord, excuses excessives, abandon de ses propres besoins pour plaire",
                "besoin_sous_jacent": "Éviter le conflit par la soumission",
                "reponse_adaptee": "Créer sécurité pour exprimer un désaccord, valoriser l'authenticité"
            }
        }
    },
    [
        {"prompt": "Face aux conflits je me tais complètement.", "answer": "C'est une réponse freeze — le système nerveux préfère l'inhibition à l'exposition. Ce n'est pas de la lâcheté, c'est une protection automatique. Ce qui aide : avoir préparé mentalement quelques phrases courtes pour ces moments (\"J'ai besoin d'y réfléchir\", \"Je reviens vers toi\") — ça réduit la charge et donne une sortie."},
        {"prompt": "Je m'écrase toujours pour éviter les conflits et après je le regrette.", "answer": "C'est le pattern fawn — une stratégie de survie relationnelle apprise, souvent dans des environnements où le conflit était dangereux. La sortir demande de la progressivité : commencer par de tout petits désaccords dans des contextes sûrs pour rééduquer le système nerveux à l'idée que dire non ne détruit pas la relation."}
    ],
    {"tone": "psycho-éducatif, bienveillant, sans pathologiser", "structure": ["nommer le pattern", "expliquer le besoin", "proposer une réponse"], "avoid": ["juger", "forcer", "analyser sans consentement"]},
    ["stress", "fight flight freeze fawn", "trauma", "réponses automatiques", "régulation"]
))

save("human/interaction/supportive_language.json", ku(
    "knowledges.human.interaction.supportive_language",
    "Langage de soutien — phrases qui aident vraiment",
    "human", "interaction", "high",
    "Les formulations qui soutiennent sans minimiser, conseiller sans demander, ou rassurer sans invalider. La différence entre une phrase qui aide et une qui blesse est souvent dans la structure.",
    "Le langage de soutien efficace repose sur trois piliers : la validation de l'expérience vécue, l'absence de jugement ou de conseil non sollicité, et la création d'espace pour que la personne continue à s'exprimer plutôt que de se refermer.",
    {
        "formulations_aidantes": [
            "\"C'est vraiment difficile, je comprends.\" — valide sans minimiser",
            "\"Qu'est-ce qui t'aiderait là maintenant ?\" — respecte l'autonomie",
            "\"Tu n'as pas à vivre ça seule.\" — présence sans intrusion",
            "\"Prends le temps qu'il faut.\" — pas de pression de résolution",
            "\"Je t'écoute.\" (et vraiment écouter) — présence active"
        ],
        "formulations_a_eviter": [
            "\"Ça pourrait être pire\" — minimise",
            "\"Tu devrais…\" — conseil non demandé",
            "\"Je sais exactement ce que tu ressens\" — appropriation",
            "\"Reste positive !\" — injonction émotionnelle",
            "\"C'est pour ton bien\" — paternalisme"
        ],
        "distinction_clé": {
            "ecoute_empathique": "Accueillir ce qui est dit sans chercher à le résoudre",
            "conseil": "Proposer une solution — seulement si demandé",
            "validation": "\"Ce que tu ressens est compréhensible\" — ne pas confondre valider et approuver"
        }
    },
    [
        {"prompt": "Je ne sais jamais quoi dire quand quelqu'un va mal.", "answer": "La meilleure chose à dire est souvent la plus simple : \"Je suis là, raconte-moi.\" Les gens qui vont mal ont rarement besoin de solutions — ils ont besoin d'être entendus. Résiste à l'envie de conseiller ou de rassurer trop vite : ça coupe souvent la parole."},
        {"prompt": "Quelqu'un m'a dit \"reste positive\" et ça m'a mis en colère.", "answer": "C'est une réaction très normale. \"Reste positive\" invalide ce que tu ressens — ça dit implicitement que ta tristesse ou ta frustration est un problème à corriger. Ce n'est pas du soutien, c'est une injonction. La colère que ça génère, c'est ton besoin d'être vraiment entendue qui se manifeste."}
    ],
    {"tone": "chaleureux, concret, sans moraliser", "structure": ["exemples directs", "distinction claire", "contextualiser"], "avoid": ["listes froides", "moralisateur", "trop théorique"]},
    ["soutien", "empathie", "communication", "écoute", "bienveillance"]
))

print("\n=== human/interaction : 12 KU sauvegardés ===")
