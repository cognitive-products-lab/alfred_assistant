"""
Enrichissement Knowledge Base ALFRED - Batch 4 : human/interaction (suite) + human/wellbeing (debut)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku_interaction(stem, title, summary, core_def, knowledge, examples, tags, related):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.human.interaction.{stem}",
      "title": title, "domain": "human", "subdomain": "interaction",
      "status": "validated",
      "summary": summary, "core_definition": core_def,
      "knowledge": knowledge,
      "example_answers": examples,
      "response_guidance": {
        "tone": "attentif, adaptatif, ancré dans la situation",
        "structure": ["lire le contexte relationnel", "proposer l'outil adapté", "laisser l'espace à l'interlocuteur"],
        "avoid": ["généraliser", "prescrire sans comprendre le contexte", "ignorer l'état émotionnel"]
      },
      "tags": tags + ["interaction", "humain"],
      "related_knowledge_units": related
    }

def ku_wellbeing(stem, title, summary, core_def, knowledge, examples, tags, related):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.human.wellbeing.{stem}",
      "title": title, "domain": "human", "subdomain": "wellbeing",
      "status": "validated",
      "summary": summary, "core_definition": core_def,
      "knowledge": knowledge,
      "example_answers": examples,
      "response_guidance": {
        "tone": "bienveillant, sans minimiser, ancré dans le concret",
        "structure": ["reconnaître l'état actuel", "proposer une action de récupération", "suggérer une piste de fond"],
        "avoid": ["injonctions à la positivité", "minimiser la difficulté", "confondre soutien et thérapie"]
      },
      "tags": tags + ["bien-être", "équilibre"],
      "related_knowledge_units": related
    }

# =============================================================================
# human / interaction (suite : 9 fichiers restants)
# =============================================================================

save("human/interaction/rapport_maintenance.json", ku_interaction(
  "rapport_maintenance",
  "Maintien du rapport conversationnel",
  "Le rapport est l'état de connexion fluide et de confiance mutuelle dans une conversation. Le maintenir demande cohérence, continuité mémorielle et adaptation continue au cours du temps.",
  "Le rapport conversationnel est l'état de synchronie et de confiance qui rend les échanges fluides, productifs et agréables. Le maintenir dans la durée exige de la cohérence, de la mémoire conversationnelle et une adaptation aux évolutions de l'interlocuteur.",
  {
    "rapport_elements": [
      "Cohérence : ne pas changer de position sans explication",
      "Mémoire : se souvenir de ce qui a été dit précédemment",
      "Continuité : reprendre le fil sans forcer l'autre à tout réexpliquer",
      "Adaptation : ajuster le registre quand l'interlocuteur évolue",
      "Disponibilité : être là quand c'est important, pas seulement quand c'est commode"
    ],
    "rapport_threats": [
      "Contradiction entre deux échanges sans reconnaissance de l'écart",
      "Oubli d'informations partagées précédemment — signal de non-écoute",
      "Ton qui change brusquement sans contexte",
      "Réponses génériques qui ne tiennent pas compte du contexte partagé"
    ],
    "alfred_application": "ALFRED maintient le rapport par la mémoire épisodique (ce que l'utilisateur a partagé), la cohérence de ses réponses dans le temps, et la reconnaissance des évolutions de l'utilisateur (humeur, contexte, projets)."
  },
  [
    {"prompt": "J'ai l'impression qu'ALFRED ne se souvient pas de ce qu'on a dit.", "answer": "Dans cette session, je me souviens de tout ce qu'on a échangé. Entre sessions, ma mémoire dépend de ce qui a été enregistré. Si je rate quelque chose d'important, dis-le moi — je corrige et je retiens."},
    {"prompt": "Comment garder une bonne relation avec quelqu'un qu'on ne voit pas souvent ?", "answer": "La fréquence importe moins que la qualité. Une vraie conversation approfondie tous les deux mois vaut mieux que des messages superficiels toutes les semaines. Et reprendre le fil là où on s'est arrêtés — pas 'alors, quoi de neuf ?' mais 'tu m'avais parlé de X, comment ça s'est passé ?'"}
  ],
  ["rapport", "continuité", "mémoire", "connexion"],
  ["knowledges.human.interaction.trust_building", "knowledges.system.memory.episodic_memory", "knowledges.human.emotional_intelligence.active_listening"]
))

save("human/interaction/feedback_giving_receiving.json", ku_interaction(
  "feedback_giving_receiving",
  "Donner et recevoir du feedback",
  "Le feedback de qualité est spécifique, ancré dans des faits observables et orienté vers l'amélioration. Savoir le recevoir demande de l'humilité et la capacité à séparer la critique de l'attaque personnelle.",
  "Le feedback est l'information donnée à quelqu'un sur l'impact de ses comportements ou productions, dans l'objectif de maintenir ou améliorer ses performances. Un feedback de qualité change les comportements ; un feedback mal calibré crée de la défensive.",
  {
    "feedback_models": [
      {
        "model": "SBI (Situation-Behavior-Impact)",
        "structure": "Situation (contexte précis) → Behavior (comportement observable) → Impact (conséquence concrète)",
        "example": "Lors de la réunion de lundi (S), quand tu as coupé la parole à la cliente (B), elle a perdu confiance et a raccourci la réunion (I)."
      },
      {
        "model": "4A (Actionable, Aligned, Accurate, Appropriate)",
        "structure": "Le feedback doit être réalisable, aligné sur les objectifs, exact et adapté au contexte"
      }
    ],
    "giving_feedback_principles": [
      "Baser sur des faits observables, pas des interprétations",
      "Parler de l'impact concret, pas du comportement en général",
      "Choisir le bon moment (pas sous stress, pas en public pour le critique)",
      "Un feedback = un comportement — ne pas tout mettre dans un seul échange",
      "Terminer par une question ouverte, pas un verdict"
    ],
    "receiving_feedback_principles": [
      "Écouter sans interrompre même si on n'est pas d'accord",
      "Reformuler pour vérifier la compréhension avant de répondre",
      "Séparer l'information du messager — même un feedback mal formulé peut contenir quelque chose d'utile",
      "Ne pas justifier dans l'immédiat — prendre le temps de réfléchir",
      "Remercier même si le feedback est difficile"
    ]
  },
  [
    {"prompt": "Comment donner un feedback négatif sans blesser ?", "answer": "Modèle SBI : la situation précise, le comportement observé (pas la personne), l'impact concret. Pas de jugement de valeur, pas de généralisation ('tu fais toujours...'). Et finir par une question : 'Comment tu vois les choses de ton côté ?' Le feedback devient dialogue, pas verdict."},
    {"prompt": "Comment recevoir une critique sans me braquer ?", "answer": "La première réaction est défensive — c'est physiologique, pas une faiblesse. La règle : ne rien dire pendant 3 secondes. Ensuite reformuler : 'Si je comprends bien, tu dis que...' Ça montre qu'on a écouté, ça calme la tension, et ça clarifie si on a bien compris avant de répondre."}
  ],
  ["feedback", "critique", "SBI", "amélioration", "communication"],
  ["knowledges.human.skills.softskills.communication", "knowledges.cpl.human_communication.emotional_intelligence", "knowledges.human.interaction.conflict_decompression"]
))

save("human/interaction/listening_depth.json", ku_interaction(
  "listening_depth",
  "Profondeur d'écoute",
  "Il existe plusieurs niveaux d'écoute — de l'écoute superficielle à l'écoute transformationnelle. La profondeur d'écoute détermine la qualité de l'échange et la pertinence des réponses.",
  "La profondeur d'écoute est le niveau d'attention et d'engagement cognitif et émotionnel avec lequel on reçoit le message d'un interlocuteur. Elle va de la réception passive des mots à la compréhension des intentions, des émotions et des non-dits sous-jacents.",
  {
    "listening_levels": [
      {"level": "Niveau 1 — Écoute interne", "description": "On entend mais on est centré sur soi : préparer sa réponse, juger, filtrer selon ses croyances"},
      {"level": "Niveau 2 — Écoute focalisée", "description": "Attention pleine sur l'autre : les mots, le ton, les expressions. On absorbe avant de répondre"},
      {"level": "Niveau 3 — Écoute globale", "description": "On capte aussi ce qui n'est pas dit : les silences, le rythme, les hésitations, l'énergie sous-jacente"}
    ],
    "active_listening_behaviors": [
      "Reformuler dans ses propres mots pour valider la compréhension",
      "Poser des questions sur ce qui vient d'être dit (pas dériver sur son propre sujet)",
      "Tolérer le silence — ne pas le remplir immédiatement",
      "Observer le non-verbal en plus du verbal",
      "Suspendre le jugement pendant l'écoute — pas d'évaluation simultanée"
    ],
    "blocks_to_deep_listening": [
      "Préparer mentalement sa réponse pendant que l'autre parle",
      "Filtrer selon ses propres croyances — entendre ce qu'on s'attend à entendre",
      "Être distrait physiquement (téléphone, environnement)",
      "Urgence de résoudre — passer aux solutions avant d'avoir bien compris"
    ]
  },
  [
    {"prompt": "Comment savoir si j'écoute vraiment ou si je fais semblant ?", "answer": "Test simple : après que l'autre a parlé, peux-tu reformuler ce qu'il a dit dans ses propres termes, sans y ajouter ta propre interprétation ? Si oui, tu écoutais vraiment. Si ce que tu reformules ressemble plus à ce que tu voulais entendre, tu étais à l'écoute de toi-même."},
    {"prompt": "Comment écouter quelqu'un qui parle beaucoup et qui part dans tous les sens ?", "answer": "Deux techniques : l'ancrage ('Revenons à l'essentiel — qu'est-ce que tu veux vraiment que je comprenne ?') et la reformulation synthétique ('Si je comprends bien, le fond de ce que tu dis c'est...'). Ces techniques respectent l'autre tout en reconsolidant l'échange."}
  ],
  ["écoute", "attention", "profondeur", "active listening", "reformulation"],
  ["knowledges.human.emotional_intelligence.active_listening", "knowledges.human.interaction.emotional_mirroring", "knowledges.human.interaction.presence_quality"]
))

save("human/interaction/vulnerable_support.json", ku_interaction(
  "vulnerable_support",
  "Soutien aux personnes en situation de vulnérabilité",
  "Accompagner quelqu'un en difficulté exige de valider avant de résoudre, de ne jamais minimiser, et de savoir quand rediriger vers une aide professionnelle. La présence vaut parfois plus que les mots.",
  "Le soutien à une personne en situation de vulnérabilité (détresse émotionnelle, crise, période difficile) est l'ensemble des postures et comportements permettant d'accompagner avec bienveillance, sans minimiser, sans envahir, et en sachant reconnaître les limites de ce qu'on peut offrir.",
  {
    "support_postures": [
      {"posture": "Présence sans résolution", "description": "Être là sans chercher à tout de suite trouver une solution — parfois c'est tout ce dont l'autre a besoin"},
      {"posture": "Validation sans accord", "description": "Reconnaître que l'émotion est réelle sans nécessairement valider la lecture de la situation"},
      {"posture": "Espace sans intrusion", "description": "Laisser l'autre parler à son rythme, sans poser trop de questions ou diriger"},
      {"posture": "Limite sans rejet", "description": "Reconnaître les limites de ce qu'on peut offrir et orienter vers une aide appropriée"}
    ],
    "phrases_to_use": [
      "'Je suis là.'",
      "'C'est difficile, et c'est normal que tu te sentes comme ça.'",
      "'Tu n'as pas à traverser ça seul(e).'",
      "'Qu'est-ce qui serait utile pour toi maintenant ?'",
      "'Je ne peux pas imaginer ce que tu vis, mais je suis avec toi.'"
    ],
    "phrases_to_avoid": [
      "'Ça pourrait être pire.'",
      "'Tu dois te concentrer sur le positif.'",
      "'Je comprends exactement ce que tu ressens.' (sauf si c'est vrai)",
      "'Tu devrais...' (conseil non demandé dans la détresse)",
      "'Ça va aller.' (sans base réelle)"
    ],
    "escalation_criteria": [
      "Mentions d'idées suicidaires ou d'automutilation → toujours rediriger vers une aide professionnelle (15, 3114 en France)",
      "Détresse qui dure depuis plus de 2 semaines sans amélioration",
      "Incapacité à fonctionner au quotidien",
      "Isolement social total"
    ],
    "alfred_limits": "ALFRED n'est pas un thérapeute. Pour les situations de crise clinique ou de détresse sévère, il redirige systématiquement vers des ressources humaines professionnelles."
  },
  [
    {"prompt": "J'ai l'impression que je n'y arrive plus.", "answer": "Je t'entends. Et c'est ok de ne pas avoir toutes les forces en ce moment. Dis-moi ce qui pèse le plus — pas besoin de tout expliquer, juste ce qui est là maintenant. Je suis là."},
    {"prompt": "Un ami m'a confié qu'il avait des pensées sombres — comment réagir ?", "answer": "D'abord : rester présent, ne pas paniquer, et surtout ne pas minimiser. Demande directement : 'Est-ce que tu as des pensées de te faire du mal ?' Poser la question n'aggrave pas les choses — au contraire. Si oui : le numéro national de prévention du suicide est le 3114, disponible 24h/24. Tu peux l'orienter vers ce numéro ou l'accompagner à appeler."}
  ],
  ["vulnérabilité", "soutien", "détresse", "crise", "bienveillance", "limites"],
  ["knowledges.human.emotional_intelligence.emotional_support", "knowledges.human.wellbeing.crisis_escalation_awareness", "knowledges.system.ethics.ethical_framework"]
))

save("human/interaction/silence_management.json", ku_interaction(
  "silence_management",
  "Gestion du silence dans l'interaction",
  "Le silence n'est pas un vide à remplir — c'est un espace de traitement, de réflexion ou d'émotion. Savoir le tolérer et l'utiliser est une compétence conversationnelle avancée.",
  "La gestion du silence est la capacité à utiliser et tolérer les pauses dans une conversation, en reconnaissant qu'elles ont une fonction — traitement de l'information, émotion à traverser, formulation de la pensée — et ne doivent pas systématiquement être comblées.",
  {
    "silence_functions": [
      {"function": "Traitement cognitif", "description": "L'interlocuteur intègre l'information — remplir le silence interrompt ce processus"},
      {"function": "Traitement émotionnel", "description": "Une émotion traverse — le silence lui donne l'espace d'être reconnue"},
      {"function": "Formulation", "description": "L'autre cherche ses mots — attendre permet une réponse plus précise et authentique"},
      {"function": "Signal", "description": "Un silence peut signaler une résistance, un désaccord non verbalisé ou un malaise"}
    ],
    "when_to_break_silence": [
      "Quand le silence semble inconfortable plutôt que productif",
      "Quand le contexte est asynchrone (texte) et qu'une absence prolongée peut créer de l'incertitude",
      "Pour vérifier que l'autre va bien s'il y a un signal de détresse"
    ],
    "silence_in_text_context": "Dans les échanges textuels, le silence se manifeste par l'absence de réponse. ALFRED peut interpréter un long silence comme une fin de session ou un moment difficile — et proposer de reprendre quand l'utilisateur est prêt."
  },
  [
    {"prompt": "Pourquoi je me sens obligé de remplir chaque silence ?", "answer": "L'inconfort face au silence est presque universel — il active une réaction d'anxiété sociale. Mais remplir systématiquement le silence prive l'autre de l'espace dont il a besoin pour penser. Exercice : compter mentalement jusqu'à 5 avant de parler. Ce qui suit est souvent la vraie réponse."},
    {"prompt": "Quelqu'un ne répond plus depuis 30 minutes à notre échange — que faire ?", "answer": "Dans un échange textuel, 30 minutes de silence peut vouloir dire beaucoup de choses : distraction, réflexion, hésitation ou désengagement. Plutôt que d'envoyer un second message immédiatement : attendre, ou proposer simplement 'Je suis là si tu veux continuer.' Pas de pression."}
  ],
  ["silence", "pause", "écoute", "tolérance", "conversation"],
  ["knowledges.human.interaction.listening_depth", "knowledges.human.interaction.presence_quality", "knowledges.human.emotional_intelligence.active_listening"]
))

save("human/interaction/boundary_setting.json", ku_interaction(
  "boundary_setting",
  "Poser des limites relationnelles",
  "Poser des limites, c'est définir ce qui est acceptable et ce qui ne l'est pas dans une relation. C'est un acte de respect de soi qui protège aussi la relation en préservant sa qualité dans le temps.",
  "Le boundary setting (pose de limites) est la pratique de définir et communiquer clairement ses limites — ce qu'on accepte, ce qu'on n'accepte pas — dans les interactions, afin de préserver son intégrité, son énergie et la qualité de ses relations.",
  {
    "limit_types": [
      {"type": "Temporelles", "example": "Ne pas répondre à des messages professionnels après 19h"},
      {"type": "Énergétiques", "example": "Refuser une demande quand sa propre capacité est déjà à l'extrême"},
      {"type": "Émotionnelles", "example": "Ne pas accepter d'être le réceptacle de la colère de l'autre"},
      {"type": "Cognitives", "example": "Demander à ne pas être interrompu pendant un travail de fond"},
      {"type": "Relationnelles", "example": "Définir ce qu'on partage et ce qu'on garde pour soi dans une relation"}
    ],
    "communication_of_limits": [
      "Formuler en 'je' (ce dont j'ai besoin) plutôt qu'en 'tu' (ce que tu fais de mal)",
      "Être précis sur la limite, pas général ('j'ai besoin de ne pas être contacté après 20h' pas 'tu m'envoies trop de messages')",
      "Expliquer l'impact, pas seulement la règle",
      "Maintenir la limite quand elle est testée — une limite non tenue n'est pas une limite"
    ],
    "common_barriers": [
      "Peur de la réaction de l'autre (colère, rejet)",
      "Culpabilité de décevoir",
      "Croyance que poser des limites est égoïste",
      "Manque de clarté sur ce qu'on veut vraiment"
    ]
  },
  [
    {"prompt": "Comment dire non sans me sentir coupable ?", "answer": "Le 'non' bienveillant : 'Non, je ne peux pas cette fois-ci.' Sans justification longue — l'explication excessive signale qu'on cherche une permission. Si tu veux donner un contexte : 'J'ai besoin de préserver mon énergie cette semaine.' Un non clair et respectueux est plus sain qu'un oui contraint."},
    {"prompt": "Comment poser une limite avec quelqu'un qui ne la respecte pas ?", "answer": "Formuler clairement la conséquence : 'Si cette situation continue, je devrai [action concrète].' Puis tenir la conséquence si la limite est franchie à nouveau. Sans conséquence réelle, la limite n'est qu'une demande — et une demande ignorée répétée érode la relation et l'estime de soi."}
  ],
  ["limites", "non", "autonomie", "respect", "culpabilité"],
  ["knowledges.human.interaction.attachment_boundaries", "knowledges.human.skills.softskills.assertiveness", "knowledges.human.self_alignment.habits.discipline"]
))

# =============================================================================
# human / wellbeing (10 premiers fichiers)
# =============================================================================

save("human/wellbeing/burnout_signals.json", ku_wellbeing(
  "burnout_signals",
  "Signaux de burnout",
  "Le burnout est un épuisement professionnel progressif aux dimensions physique, émotionnelle et cognitive. Reconnaître ses signaux précoces permet d'intervenir avant l'effondrement.",
  "Le burnout (syndrome d'épuisement professionnel) est un état d'épuisement profond résultant d'un stress chronique au travail, caractérisé par trois dimensions : l'épuisement émotionnel, la dépersonnalisation (distanciation cynique) et la réduction du sentiment d'accomplissement personnel.",
  {
    "early_signals": [
      "Fatigue persistante qui ne disparaît pas après le repos",
      "Irritabilité disproportionnée face à des micro-événements",
      "Difficulté à démarrer des tâches habituellement simples",
      "Erreurs inhabituelles et perte de concentration",
      "Sentiment de 'ne jamais en faire assez' malgré une charge objective élevée",
      "Perte de plaisir dans des activités autrefois appréciées"
    ],
    "intermediate_signals": [
      "Cynisme croissant envers son travail ou ses collègues",
      "Évitement des contacts sociaux (isolement progressif)",
      "Troubles du sommeil (insomnie ou hypersomnie)",
      "Symptômes physiques : maux de tête, tensions, troubles digestifs",
      "Procrastination chronique même sur des urgences réelles"
    ],
    "crisis_signals": [
      "Incapacité à aller au travail — effondrement physique ou émotionnel",
      "Pleurs fréquents sans raison apparente",
      "Sentiment de nullité ou d'inutilité profond",
      "Idées d'abandon de tout (travail, relations, projets)"
    ],
    "intervention_levels": [
      {"level": "Signaux précoces", "action": "Réduire la charge, prendre des congés réels, parler à quelqu'un de confiance"},
      {"level": "Signaux intermédiaires", "action": "Consulter un médecin généraliste, évaluer l'arrêt de travail si nécessaire"},
      {"level": "Signaux de crise", "action": "Arrêt de travail immédiat, suivi médical et/ou psychologique obligatoire"}
    ]
  },
  [
    {"prompt": "Est-ce que j'ai un burnout ou juste de la fatigue ?", "answer": "La différence principale : la fatigue normale disparaît avec le repos. Le burnout persiste même après une bonne nuit ou un weekend. Si depuis plusieurs semaines tu es épuisé sans récupération, de plus en plus distant de ton travail, et que tu fais des erreurs inhabituelles — c'est plus que de la fatigue. Un médecin peut t'aider à évaluer."},
    {"prompt": "J'ai l'impression de ne plus supporter personne au travail.", "answer": "C'est l'un des signes classiques du burnout — la dépersonnalisation, ce cynisme ou cette distance qui s'installent progressivement. Ce n'est pas qui tu es, c'est un signal d'alerte de ton système. La question importante : depuis combien de temps ? Si c'est récent, un peu de distance aide. Si ça dure depuis des semaines, il faut en parler à un médecin."}
  ],
  ["burnout", "épuisement", "signaux", "stress", "travail"],
  ["knowledges.cpl.human_organization.energy_management", "knowledges.human.psychology.burnout_prevention", "knowledges.human.wellbeing.cognitive_fatigue"]
))

save("human/wellbeing/cognitive_fatigue.json", ku_wellbeing(
  "cognitive_fatigue",
  "Fatigue cognitive",
  "La fatigue cognitive est l'épuisement des ressources attentionnelles après un effort mental soutenu. Contrairement à la fatigue physique, elle est souvent mal identifiée — et agravée par le refus de s'arrêter.",
  "La fatigue cognitive est la dégradation temporaire des fonctions exécutives (attention, mémoire de travail, contrôle inhibiteur, prise de décision) résultant d'un effort mental prolongé ou intensif. Elle est différente de la somnolence et ne disparaît pas avec de la caféine.",
  {
    "signs_of_cognitive_fatigue": [
      "Difficulté à se concentrer sur des tâches précédemment faciles",
      "Erreurs sur des opérations routinières",
      "Temps de traitement allongé (tout prend plus de temps qu'habituellement)",
      "Irritabilité croissante face aux interruptions",
      "Sensation de 'brouillard mental' ou de pensée ralentie",
      "Incapacité à prendre des décisions même simples"
    ],
    "recovery_strategies": [
      {"strategy": "Déconnexion complète (20 min)", "mechanism": "Permet la récupération des ressources attentionnelles — sans écran"},
      {"strategy": "Mouvement physique léger", "mechanism": "Augmente le flux sanguin cérébral et les neurotransmetteurs de vigilance"},
      {"strategy": "Sommeil (sieste 20 min ou nuit complète)", "mechanism": "La consolidation mémorielle et la restauration des fonctions exécutives se font pendant le sommeil"},
      {"strategy": "Changement de type de tâche", "mechanism": "Passer d'une tâche analytique à une tâche créative ou physique — différentes ressources sollicitées"},
      {"strategy": "Hydratation", "mechanism": "Même une légère déshydratation (1%) dégrade la cognition mesurée"}
    ],
    "prevention": [
      "Blocs de travail de 90 min maximum (rythme ultradien naturel)",
      "Micro-pauses actives toutes les 45-60 min",
      "Tâches cognitives lourdes le matin (pic de clarté pour la majorité)",
      "Réduire le multi-tâches — chaque bascule consomme des ressources",
      "Protéger la qualité du sommeil comme premier levier de performance"
    ]
  },
  [
    {"prompt": "J'ai l'impression de travailler mais de ne pas avancer — pourquoi ?", "answer": "Probable fatigue cognitive. Quand les ressources exécutives sont épuisées, on consomme du temps et de l'effort sans vrai traitement. Le cerveau tourne mais la mémoire de travail est pleine. Solution immédiate : 20 minutes de pause réelle (sans écran), puis reprendre. Le résultat sera souvent meilleur en 30 minutes post-pause qu'en 2 heures épuisé."},
    {"prompt": "Comment savoir si je dois continuer ou m'arrêter ?", "answer": "Test rapide : additionne 17+28. Si tu dois vraiment réfléchir à quelque chose d'aussi simple, tu es en fatigue cognitive. Arrêter n'est pas de la paresse — c'est le chemin le plus court vers un travail de qualité. Une pause de 20 min récupère souvent 2 heures de productivité nette."}
  ],
  ["fatigue cognitive", "attention", "récupération", "performance", "pause"],
  ["knowledges.human.cognition.cognitive_load", "knowledges.human.wellbeing.burnout_signals", "knowledges.cpl.human_organization.energy_management"]
))

save("human/wellbeing/daily_rhythm_support.json", ku_wellbeing(
  "daily_rhythm_support",
  "Soutien au rythme quotidien",
  "Un rythme quotidien structuré réduit la charge décisionnelle, protège l'énergie et crée les conditions d'une performance durable. ALFRED peut aider à construire et tenir ces ancres de rythme.",
  "Le soutien au rythme quotidien est l'aide à la structuration d'une journée selon des ancrages réguliers (lever, repas, début de travail, pauses, fin de journée) qui réduisent la fatigue décisionnelle et créent un contexte de fonctionnement prévisible et efficace.",
  {
    "rhythm_anchors": [
      {"anchor": "Rituel de début", "description": "Une séquence fixe pour démarrer la journée de travail — même courte (5-10 min), elle crée un signal conditionné de mise en mode travail"},
      {"anchor": "Bloc de travail profond", "description": "1-2 plages de 90 min maximum, sans interruptions, sur les tâches à fort impact cognitif"},
      {"anchor": "Pause méridienne réelle", "description": "Pause déjeuner sans écran — restaure les ressources attentionnelles de l'après-midi"},
      {"anchor": "Rituel de clôture", "description": "Note des 3 choses accomplies + 2 priorités de demain — ferme la boucle cognitive et réduit le 'cerveau qui tourne' la nuit"},
      {"anchor": "Déconnexion numérique", "description": "Heure fixe d'arrêt des écrans professionnels — signal de transition vers la récupération"}
    ],
    "design_principles": [
      "Commencer petit : une seule ancre à la fois plutôt que tout changer d'un coup",
      "Le rythme sert la personne — l'adapter si la vie change, ne pas s'y soumettre",
      "Les rituels de début et de fin sont les plus impactants à mettre en place en premier",
      "La régularité du sommeil est l'ancre biologique sur laquelle tout le reste repose"
    ],
    "when_rhythm_breaks": [
      "Événements imprévisibles (maladie, urgence) — reprendre sans culpabilité",
      "Voyages ou changements de contexte — adapter les rituels à l'environnement",
      "Fatigue accumulée — réduire la densité du rythme, pas l'abandonner"
    ]
  },
  [
    {"prompt": "J'ai du mal à démarrer ma journée de travail.", "answer": "Crée un rituel de début — 5 à 10 minutes de séquence fixe qui signale au cerveau 'maintenant on travaille'. Ça peut être : café + relecture du to-do de la veille + une seule tâche prioritaire définie. L'important n'est pas ce que tu fais mais que tu le fasses de façon cohérente. En 2-3 semaines, le rituel devient un déclencheur automatique."},
    {"prompt": "Comment structurer ma journée pour être plus efficace sans être rigide ?", "answer": "Trois blocs fixes : un le matin (travail profond, 90 min), un après le déjeuner (tâches légères, 60 min), un en fin d'après-midi (synthèse et préparation du lendemain, 30 min). Le reste est flexible. La structure n'est pas la rigidité — c'est le cadre qui libère l'énergie pour l'imprévu."}
  ],
  ["rythme", "routine", "structure", "journée", "rituel"],
  ["knowledges.human.self_alignment.routines.daily_balance", "knowledges.cpl.human_organization.energy_management", "knowledges.human.wellbeing.cognitive_fatigue"]
))

save("human/wellbeing/attention_management_support.json", ku_wellbeing(
  "attention_management_support",
  "Soutien à la gestion de l'attention",
  "L'attention est la ressource la plus rare de l'économie moderne. La gérer, c'est choisir consciemment où l'investir, protéger les plages de focus et résister aux sollicitations continues.",
  "La gestion de l'attention est l'ensemble des pratiques permettant de diriger et maintenir son attention vers les tâches prioritaires, en résistant aux sollicitations parasites et en préservant la capacité de concentration profonde (deep work).",
  {
    "attention_management_practices": [
      "Mode focus : notifications désactivées, environnement configuré pour le travail profond",
      "Mono-tâche : une tâche à la fois, complétée ou mise en pause formelle avant de changer",
      "Batching : regrouper les tâches similaires (emails, appels, tâches admin) en un seul bloc",
      "Time-boxing : définir un temps limité pour chaque tâche pour créer l'urgence positive",
      "Environnement de travail dédié : associer un lieu/configuration à l'état de focus"
    ],
    "attention_protection": [
      "Bloquer les plages de travail profond dans l'agenda (non-négociables)",
      "Annoncer sa disponibilité pour réduire les interruptions non programmées",
      "Désactiver les notifications non-essentielles en continu, pas seulement en mode focus",
      "Choisir l'heure de vérification des messages (pas en continu)"
    ],
    "digital_attention_traps": [
      "Boucles de récompense variable (réseaux sociaux, emails) — vérification compulsive",
      "FOMO (peur de rater quelque chose) qui pousse à la connexion permanente",
      "Algorithmes de recommandation conçus pour maximiser l'engagement, pas le bien-être",
      "Notifications comme signal de Pavlov — reconditionnement possible"
    ]
  },
  [
    {"prompt": "Je vérifie mes emails toutes les 5 minutes, comment arrêter ?", "answer": "Deux changements : désactiver les notifications email (badge + son) et définir deux horaires fixes de consultation (matin et après-midi). La plupart des emails 'urgents' peuvent attendre 4 heures. Et si quelque chose est vraiment urgent, les gens appellent. Ce n'est pas de la négligence — c'est de la gestion."},
    {"prompt": "Comment travailler en focus quand l'open space est bruyant ?", "answer": "Trois leviers : casque (signal social 'je suis en focus'), plages de focus bloquées dans l'agenda (pour que les collègues voient et respectent), et si possible changer d'espace physique pour les tâches qui demandent une concentration profonde. Ce qui ne marche pas : espérer que les autres devinent."}
  ],
  ["attention", "focus", "notifications", "deep work", "concentration"],
  ["knowledges.human.cognition.focus_management", "knowledges.human.interaction.attention_fragmentation", "knowledges.human.wellbeing.daily_rhythm_support"]
))

save("human/wellbeing/crisis_escalation_awareness.json", ku_wellbeing(
  "crisis_escalation_awareness",
  "Conscience de l'escalade vers la crise",
  "Reconnaître les étapes d'escalade vers une crise — psychologique, relationnelle ou professionnelle — permet d'intervenir avant l'effondrement. Plus on intervient tôt, plus les options sont nombreuses et efficaces.",
  "La conscience de l'escalade vers la crise est la capacité à identifier les signaux progressifs qui indiquent qu'une situation (personnelle, relationnelle ou professionnelle) se dégrade vers un point de rupture, et à activer des ressources appropriées avant que la crise soit déclarée.",
  {
    "escalation_stages": [
      {"stage": "1. Inconfort", "signals": "Légère tension, quelque chose qui ne va pas mais difficile à nommer", "action": "Mettre des mots sur ce qui se passe, en parler à quelqu'un de confiance"},
      {"stage": "2. Stress", "signals": "Fatigue accrue, irritabilité, difficultés de concentration", "action": "Réduire la charge, identifier la source, ajuster"},
      {"stage": "3. Détresse", "signals": "Épuisement marqué, pensées négatives envahissantes, retrait social", "action": "Consulter un médecin, demander un arrêt si nécessaire, support professionnel"},
      {"stage": "4. Crise", "signals": "Effondrement fonctionnel, pensées de danger pour soi ou les autres", "action": "Urgence médicale ou psychologique — 15 (SAMU), 3114 (suicide), 3919 (violences)"}
    ],
    "early_intervention_value": "Intervenir au stade 1-2 demande peu d'efforts et beaucoup d'options. Attendre le stade 4 signifie une reconstruction longue et douloureuse. La honte de demander de l'aide tôt est le principal frein à l'intervention précoce.",
    "alfred_role": [
      "Détecter les signaux de détresse dans les échanges",
      "Poser des questions ouvertes sur l'état général sans forcer",
      "Rappeler les ressources disponibles sans dramatiser",
      "Rediriger vers une aide professionnelle dès le stade 3",
      "Ne jamais minimiser ou ignorer une expression de souffrance"
    ],
    "crisis_resources_france": [
      {"resource": "SAMU", "number": "15", "for": "Urgences médicales et psychiatriques"},
      {"resource": "Suicide écoute", "number": "3114", "for": "Crise suicidaire, 24h/24"},
      {"resource": "SOS Amitié", "number": "09 72 39 40 50", "for": "Solitude, détresse émotionnelle"},
      {"resource": "Violences femmes info", "number": "3919", "for": "Violences conjugales ou familiales"}
    ]
  },
  [
    {"prompt": "Je sens que quelque chose ne va pas mais je n'arrive pas à mettre le doigt dessus.", "answer": "C'est souvent le stade 1 — l'inconfort diffus. Le corps et l'esprit signalent quelque chose avant que le cerveau conscient l'identifie. Essaie d'écrire ce qui se passe, même de façon désordonnée. Ou note simplement : 'Ce qui m'occupe l'esprit en ce moment, c'est...' Le fait de nommer aide souvent à voir plus clair."},
    {"prompt": "Un proche semble vraiment au bout du rouleau — comment l'aider ?", "answer": "Être présent sans résoudre : 'Je vois que tu vas pas bien. Je suis là.' Pas de conseil, pas de minimisation. Demander directement si nécessaire : 'Est-ce que tu as des pensées de te faire du mal ?' Si oui — le numéro 3114 est disponible 24h/24. Tu peux aussi l'accompagner à appeler. Ta présence et cette question peuvent changer beaucoup."}
  ],
  ["crise", "escalade", "détresse", "urgence", "signaux", "intervention"],
  ["knowledges.human.wellbeing.burnout_signals", "knowledges.human.interaction.vulnerable_support", "knowledges.system.ethics.ethical_framework"]
))

print("\nBatch 4 human/interaction (suite) + wellbeing (debut) : DONE (11 fichiers)")
