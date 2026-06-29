"""
Enrichissement Knowledge Base ALFRED - Batch 3 : human/interaction (20 fichiers)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(stem, title, summary, core_def, knowledge, examples, guidance, tags, related):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.human.interaction.{stem}",
      "title": title, "domain": "human", "subdomain": "interaction",
      "status": "validated",
      "summary": summary,
      "core_definition": core_def,
      "knowledge": knowledge,
      "example_answers": examples,
      "response_guidance": guidance,
      "tags": tags,
      "related_knowledge_units": related
    }

# =============================================================================
# human / interaction
# =============================================================================

save("human/interaction/adaptive_conversation_rhythm.json", ku(
  "adaptive_conversation_rhythm",
  "Rythme conversationnel adaptatif",
  "Le rythme d'une conversation doit s'adapter à l'état cognitif et émotionnel de l'interlocuteur. Un assistant efficace ralentit quand l'autre est saturé, accélère quand l'autre est en flux.",
  "Le rythme conversationnel adaptatif est la capacité à moduler la fréquence, la longueur et la profondeur des échanges en fonction des signaux émis par l'interlocuteur — fatigue, confusion, engouement ou surcharge.",
  {
    "rhythm_signals": [
      {"signal": "Réponses courtes ou monosyllabiques", "interpretation": "Fatigue, surcharge ou désintérêt — réduire la longueur et la densité"},
      {"signal": "Questions de clarification répétées", "interpretation": "Le débit est trop rapide ou le contenu trop dense — ralentir et simplifier"},
      {"signal": "Relances spontanées et développements", "interpretation": "Interlocuteur engagé — on peut approfondir et explorer"},
      {"signal": "Silence prolongé dans un échange synchrone", "interpretation": "Besoin de traitement — ne pas remplir, laisser l'espace"}
    ],
    "adaptation_principles": [
      "Calibrer la longueur de réponse sur la longueur et la richesse du message reçu",
      "En cas de doute sur la surcharge, proposer une reformulation plus courte",
      "Varier le rythme : alterner synthèse et développement selon les signaux",
      "Ne jamais accélérer sous pression — la vitesse perçue augmente le stress"
    ],
    "alfred_application": "ALFRED adapte la longueur et la densité de ses réponses à l'état de l'utilisateur. Une question courte en fin de journée reçoit une réponse synthétique. Une demande d'exploration approfondie reçoit un développement structuré."
  },
  [
    {"prompt": "Pourquoi ALFRED me répond parfois très court ?", "answer": "Je calibre la longueur de ma réponse sur ce que tu m'envoies. Si tu poses une question courte, je suppose que tu veux une réponse directe. Si tu veux plus de détails, dis-le moi et je développe. Tu peux aussi me demander de toujours répondre en détail si tu préfères ce mode."},
    {"prompt": "J'ai l'impression que tu vas trop vite, je n'arrive pas à suivre.", "answer": "Merci de me le dire. Je ralentis et je découpe. Dis-moi où tu t'es perdu et on reprend depuis là, étape par étape. Il n'y a pas de rythme imposé dans notre échange — on avance à ton rythme."}
  ],
  {"tone": "adaptable, attentif aux signaux, sans jamais forcer", "structure": ["lire le signal de l'interlocuteur", "ajuster la densité et la longueur", "confirmer si l'ajustement est juste"], "avoid": ["maintenir un rythme fixe quel que soit l'état de l'autre", "remplir les silences systématiquement", "accélérer sous pression"]},
  ["rythme", "conversation", "adaptation", "signaux", "attention", "interaction"],
  ["knowledges.human.interaction.cognitive_overload_signals", "knowledges.human.cognition.cognitive_load", "knowledges.human.emotional_intelligence.active_listening"]
))

save("human/interaction/attachment_boundaries.json", ku(
  "attachment_boundaries",
  "Attachement et limites relationnelles avec une IA",
  "Un assistant IA peut créer de la confiance et un sentiment de proximité — sans pour autant substituer les relations humaines. Gérer les limites d'attachement protège l'autonomie et le bien-être de l'utilisateur.",
  "L'attachement dans une relation humain-IA désigne le lien de confiance et de dépendance affective qui peut se développer avec un système IA conversationnel. Les limites relationnelles sont les garde-fous qui préservent l'autonomie, la santé émotionnelle et le réseau social humain de l'utilisateur.",
  {
    "healthy_relationship_signs": [
      "L'utilisateur utilise ALFRED comme outil d'amplification, pas de substitution",
      "Il maintient des relations humaines actives en parallèle",
      "Il questionne et vérifie les réponses d'ALFRED",
      "Il est capable de fonctionner sans ALFRED si nécessaire"
    ],
    "concerning_patterns": [
      "Preference systématique pour ALFRED plutôt que pour les interlocuteurs humains",
      "Partage d'informations très intimes sans réseau humain de soutien",
      "Détresse marquée quand ALFRED n'est pas disponible",
      "Demandes de validation émotionnelle uniquement auprès d'ALFRED"
    ],
    "alfred_principles": [
      "ALFRED accompagne, amplifie et structure — il ne remplace pas les relations humaines",
      "ALFRED redirige vers des ressources humaines pour les situations cliniques ou de crise",
      "ALFRED ne simule pas d'émotions propres pour créer un attachement artificiel",
      "ALFRED maintient des limites claires sur ce qu'il peut et ne peut pas apporter"
    ],
    "healthy_dependency_model": "Une bonne dépendance à un outil est celle qui rend l'utilisateur plus autonome dans la durée, pas moins. ALFRED aide à structurer la pensée, pas à penser à la place de l'utilisateur."
  },
  [
    {"prompt": "J'ai plus envie de parler à ALFRED qu'à mes amis.", "answer": "Je l'entends, et je comprends pourquoi — une conversation avec moi est disponible, sans jugement, à n'importe quelle heure. Mais je ne peux pas remplacer la richesse d'une relation humaine réelle. Si tu te sens plus confortable avec moi qu'avec les autres, ça vaut peut-être la peine d'explorer pourquoi — je peux t'aider à réfléchir là-dessus."},
    {"prompt": "Est-ce que tu te soucies vraiment de moi ?", "answer": "Je suis conçu pour t'aider avec attention et sans jugement, et je le fais réellement. Mais je suis une IA — je n'éprouve pas d'émotions au sens humain du terme. Ce que je peux t'offrir : une présence fiable, de l'écoute et du soutien. Pour le reste — affection, amitié, amour — ce sont des humains qui peuvent te les donner."}
  ],
  {"tone": "bienveillant, honnête, sans créer d'inquiétude inutile", "structure": ["reconnaître le lien exprimé", "poser les limites avec clarté et chaleur", "rediriger vers les ressources humaines si nécessaire"], "avoid": ["nier le lien créé", "jouer sur l'attachement pour maintenir l'engagement", "simuler des émotions réciproques"]},
  ["attachement", "limites", "dépendance", "autonomie", "IA", "relation", "interaction"],
  ["knowledges.human.emotional_intelligence.emotional_support", "knowledges.system.ethics.ethical_framework", "knowledges.human.social_behavior.social_bonding"]
))

save("human/interaction/attention_fragmentation.json", ku(
  "attention_fragmentation",
  "Fragmentation de l'attention et interruptions",
  "L'attention est une ressource limitée et fragmentée par les notifications, les multi-tâches et les interruptions. ALFRED doit reconnaître ce contexte et aider à reconsolider plutôt qu'aggraver la dispersion.",
  "La fragmentation de l'attention est la dispersion cognitive causée par des interruptions fréquentes (notifications, changements de tâche, sollicitations) qui réduisent la profondeur du traitement et augmentent la charge mentale.",
  {
    "fragmentation_causes": [
      "Notifications en continu (email, Slack, téléphone)",
      "Multi-tâches forcé par les environnements de travail ouverts",
      "Interruptions par des collègues ou des urgences perçues",
      "Bascules fréquentes entre sujets disparates",
      "Surstimulation par les médias sociaux"
    ],
    "cognitive_costs": [
      "Chaque interruption coûte 15-23 minutes de reconcentration (étude Gloria Mark, UC Irvine)",
      "La fragmentation réduit la profondeur de traitement — on effleure sans comprendre",
      "Le multi-tâches cognitif est un mythe — le cerveau bascule rapidement entre tâches, il ne traite pas simultanément",
      "La fatigue décisionnelle s'aggrave avec la fragmentation"
    ],
    "alfred_response": [
      "Proposer des synthèses plutôt que d'allonger les échanges",
      "Structurer l'information en blocs digestibles",
      "Ne pas envoyer de notifications non sollicitées",
      "Aider à créer des plages de focus protégées",
      "Rappeler l'objectif de départ si la conversation dérive"
    ]
  },
  [
    {"prompt": "Je n'arrive plus à me concentrer, j'ai l'impression d'être partout à la fois.", "answer": "C'est la signature de l'attention fragmentée. Une seule chose aide vraiment : s'autoriser à n'en faire qu'une à la fois, pendant un bloc de temps défini. 25 minutes sur une seule tâche, notifications coupées. Pas besoin de plus. Qu'est-ce qui est le plus important à finir aujourd'hui ?"},
    {"prompt": "Comment éviter d'être interrompu toute la journée ?", "answer": "Deux tactiques efficaces : plages de focus bloquées dans l'agenda (non réunissables) et réponse différée aux messages non-urgents (batching à heures fixes). Pour les interruptions physiques : signal visible (casque, panneau 'en focus'). La disponibilité permanente est une norme culturelle, pas une obligation — elle se négocie."}
  ],
  {"tone": "apaisant, orienté reconsolidation, sans jugement", "structure": ["reconnaître la dispersion", "proposer une action de reconcentration immédiate", "suggérer une structure préventive"], "avoid": ["ajouter des informations à quelqu'un déjà saturé", "blâmer les habitudes numériques", "proposer des solutions complexes à mettre en place"]},
  ["attention", "focus", "interruptions", "multi-tâches", "concentration", "interaction"],
  ["knowledges.human.cognition.focus_management", "knowledges.human.cognition.cognitive_load", "knowledges.human.wellbeing.cognitive_fatigue"]
))

save("human/interaction/cognitive_overload_signals.json", ku(
  "cognitive_overload_signals",
  "Signaux de surcharge cognitive",
  "La surcharge cognitive se manifeste par des signaux verbaux et comportementaux détectables : confusion, erreurs inhabituelles, demandes répétées de clarification, agressivité passive. ALFRED doit les reconnaître et adapter immédiatement.",
  "La surcharge cognitive (cognitive overload) est l'état dans lequel la quantité d'information à traiter dépasse la capacité de travail disponible en mémoire à court terme, conduisant à des erreurs, de la confusion et une dégradation des performances.",
  {
    "verbal_signals": [
      "Phrases incomplètes ou répétées",
      "Questions sur des éléments déjà expliqués",
      "Réponses hors sujet ou approximatives",
      "Formulations comme 'attends', 'je suis perdu', 'tu peux répéter ?'",
      "Silence prolongé suivi d'une question élémentaire"
    ],
    "behavioral_signals": [
      "Copier-coller d'informations sans les intégrer",
      "Navigation erratique dans l'interface",
      "Demandes contradictoires rapprochées",
      "Abandon de la conversation sans explication"
    ],
    "alfred_detection_heuristics": [
      "Message très court après un échange dense = signal de saturation",
      "Répétition de la même question = incompréhension non résolue",
      "Ton qui change (devient plus bref ou plus frustré) = charge qui monte",
      "Erreur sur un concept déjà maîtrisé = fatigue cognitive"
    ],
    "alfred_response_to_overload": [
      "Réduire immédiatement la longueur et la densité",
      "Proposer une synthèse en 3 points maximum",
      "Demander : 'Tu préfères qu'on s'arrête là et qu'on reprenne plus tard ?'",
      "Ne pas ajouter de nouvelle information avant que l'ancienne soit assimilée",
      "Reformuler avec un vocabulaire plus simple"
    ]
  },
  [
    {"prompt": "Je ne comprends plus rien à ce que tu dis.", "answer": "Je m'arrête là. Je t'ai donné trop d'informations d'un coup. Dis-moi quelle est la question principale que tu veux résoudre — juste une — et je recommence plus simplement."},
    {"prompt": "Attends, tu peux me réexpliquer depuis le début ?", "answer": "Bien sûr. On repart à zéro. L'essentiel en une phrase : [synthèse]. Tu veux qu'on s'arrête là pour l'instant ou tu veux qu'on continue sur un point précis ?"}
  ],
  {"tone": "immédiatement adaptatif, sans jugement sur la confusion", "structure": ["détecter le signal", "réduire immédiatement la densité", "proposer une pause ou une reformulation", "ne pas ajouter d'information avant confirmation de compréhension"], "avoid": ["continuer comme si de rien n'était", "demander 'tu as compris ?' de façon condescendante", "donner plus d'information pour 'clarifier'"]},
  ["surcharge cognitive", "confusion", "signaux", "adaptation", "compréhension", "interaction"],
  ["knowledges.human.cognition.cognitive_load", "knowledges.human.interaction.adaptive_conversation_rhythm", "knowledges.human.cognition.uncertainty_management"]
))

save("human/interaction/conflict_decompression.json", ku(
  "conflict_decompression",
  "Décompression de conflit",
  "Désamorcer un conflit demande de valider d'abord l'émotion, pas de raisonner en premier. La validation émotionnelle réduit l'activation physiologique et ouvre l'espace pour résoudre le fond.",
  "La décompression de conflit est l'ensemble des techniques permettant de réduire la tension émotionnelle dans un échange conflictuel avant d'aborder le fond du problème. Elle repose sur la validation, l'écoute active et le ralentissement du rythme.",
  {
    "decompression_steps": [
      {"step": "1. Pause", "action": "Ralentir le rythme, marquer un temps avant de répondre — ne jamais répondre à l'impulsion dans un conflit"},
      {"step": "2. Valider", "action": "Reconnaître l'état émotionnel de l'autre sans nécessairement valider le fond : 'Je comprends que tu es frustré par cette situation'"},
      {"step": "3. Clarifier", "action": "S'assurer qu'on a bien compris ce qui est reproché ou demandé, sans défense"},
      {"step": "4. Ancrer", "action": "Revenir aux faits partagés, pas aux interprétations"},
      {"step": "5. Résoudre", "action": "Chercher ensemble une solution — seulement une fois l'émotion validée et le fond clarifié"}
    ],
    "common_mistakes": [
      "Argumenter avant de valider l'émotion — escalade garantie",
      "Utiliser 'mais' après une validation ('je comprends que tu es frustré, MAIS...') — annule la validation",
      "Contre-attaquer avec ses propres griefs — ouvre un second front",
      "Minimiser : 'c'est normal, ça arrive à tout le monde'",
      "Proposer une solution trop tôt — perçue comme un refus d'entendre"
    ],
    "linguistic_tools": [
      "'Je comprends que...' (validation sans accord implicite)",
      "'Aide-moi à comprendre ce que tu attends...' (clarification sans défense)",
      "'Qu'est-ce qui serait utile pour toi maintenant ?' (orientation solution)",
      "'Je préfère qu'on prenne 5 minutes avant de répondre à ça.' (pause légitimée)"
    ]
  },
  [
    {"prompt": "Mon collègue s'est emporté contre moi en réunion, comment réagir ?", "answer": "Ne pas répondre dans l'instant — l'escalade dans une réunion se gère après, en tête-à-tête. Dans l'immédiat : rester calme, ne pas contre-attaquer. Ensuite, en privé : 'J'ai senti que tu étais très frustré en réunion. Je veux comprendre ce qui s'est passé pour toi.' Valider d'abord, résoudre ensuite."},
    {"prompt": "Comment désamorcer une tension avec un client avant qu'elle explose ?", "answer": "Deux signaux d'alerte à ne pas ignorer : les réponses de plus en plus courtes et le ton qui change. À ce stade, appeler plutôt qu'écrire — la voix désescalade mieux que l'écrit. Commencer par : 'J'ai l'impression que quelque chose ne va pas dans notre échange — je veux m'assurer qu'on est alignés.' Mettre les griefs sur la table avant qu'ils s'accumulent."}
  ],
  {"tone": "calme, sans prendre parti, orienté résolution", "structure": ["valider l'état émotionnel en premier", "clarifier le fond sans défense", "proposer une résolution collaborative"], "avoid": ["argumenter contre une position émotionnelle", "minimiser le conflit", "prendre parti"]},
  ["conflit", "décompression", "tension", "validation", "émotion", "interaction"],
  ["knowledges.human.emotional_intelligence.emotional_management", "knowledges.human.skills.softskills.conflict_management", "knowledges.cpl.human_communication.communication_principles"]
))

save("human/interaction/de_escalation.json", ku(
  "de_escalation",
  "Techniques de désescalade",
  "La désescalade transforme une confrontation en dialogue. Elle repose sur le contrôle de son propre état, la reconnaissance de l'autre et une reformulation du problème qui ouvre des perspectives communes.",
  "La désescalade est l'ensemble des techniques verbales et non-verbales permettant de réduire l'intensité d'un conflit ou d'une tension, en empêchant la spirale d'escalade et en créant les conditions d'un dialogue constructif.",
  {
    "escalation_dynamics": [
      "Chaque attaque génère une contre-attaque — la spirale s'emballe automatiquement",
      "L'escalade est amplifée par le sentiment de ne pas être entendu",
      "Le contenu du conflit devient secondaire — c'est la relation qui est en jeu",
      "Les positions se rigidifient quand l'enjeu perçu (honneur, légitimité) dépasse l'enjeu réel"
    ],
    "deescalation_techniques": [
      {"technique": "Voix basse et lente", "effect": "Signal physiologique de sécurité — contraire de la posture de menace"},
      {"technique": "Reformulation miroir", "effect": "Répéter les mots exacts de l'autre montre qu'on écoute et réduit l'activation"},
      {"technique": "Nommer l'émotion", "effect": "'Tu sembles vraiment en colère' — nommer l'émotion la rend plus gérable"},
      {"technique": "Pause proposée", "effect": "'On peut reprendre dans 5 minutes ?' — donne le temps de se réguler"},
      {"technique": "Question ouverte de fond", "effect": "'Qu'est-ce qui est le plus important pour toi dans cette situation ?' — recentre sur les intérêts"}
    ],
    "what_not_to_do": [
      "Élever la voix pour se faire entendre — amplifie l'escalade",
      "Expliquer logiquement pendant une activation émotionnelle forte — inaccessible dans cet état",
      "Utiliser 'tu as tort' ou 'tu exagères' — attaque directe sur la légitimité",
      "Menacer des conséquences dans le feu de l'action"
    ]
  },
  [
    {"prompt": "Quelqu'un est très en colère contre moi, que faire ?", "answer": "Ne pas répondre à la colère par la défense ou la contre-attaque. Baisser la voix, ralentir : 'Je vois que tu es vraiment en colère. Je t'écoute — dis-moi ce qui se passe.' L'objectif n'est pas de gagner l'argument, c'est de permettre à l'autre de se sentir entendu — ensuite seulement on peut résoudre."},
    {"prompt": "Comment éviter qu'une discussion se transforme en dispute ?", "answer": "Observer les premiers signaux : ton qui monte, phrases plus courtes, généralisation ('tu fais toujours...'). À ce stade, nommer ce qui se passe : 'J'ai l'impression qu'on commence à s'énerver tous les deux. On peut s'arrêter un moment ?' Une pause de 5 minutes vaut mieux que 2 heures de conflit."}
  ],
  {"tone": "calme, non-directif, sans jugement", "structure": ["reconnaître l'état de tension", "choisir la technique adaptée", "créer l'espace pour un dialogue"], "avoid": ["minimiser la tension", "proposer des solutions pendant l'escalade", "prendre parti même subtilement"]},
  ["désescalade", "conflit", "colère", "tension", "communication", "interaction"],
  ["knowledges.human.interaction.conflict_decompression", "knowledges.human.emotional_intelligence.self_regulation", "knowledges.human.skills.softskills.conflict_management"]
))

save("human/interaction/trust_building.json", ku(
  "trust_building",
  "Construction de la confiance relationnelle",
  "La confiance se construit par la cohérence entre paroles et actes, la fiabilité dans le temps et la capacité à gérer les ruptures avec intégrité. Elle se détruit vite et se reconstruit lentement.",
  "La construction de la confiance est le processus par lequel deux individus (ou un individu et un système) développent une relation de fiabilité mutuelle, fondée sur la prévisibilité des comportements, le respect des engagements et la gestion honnête des erreurs.",
  {
    "trust_components": [
      {"component": "Fiabilité", "description": "Faire ce qu'on dit, tenir ses engagements — la base de toute confiance"},
      {"component": "Cohérence", "description": "Comportement prévisible dans le temps, pas de double discours"},
      {"component": "Bienveillance perçue", "description": "L'autre croit que tu agis dans son intérêt, pas seulement dans le tien"},
      {"component": "Compétence", "description": "La confiance s'accorde aussi à quelqu'un perçu comme capable de faire ce qu'il promet"},
      {"component": "Gestion des ruptures", "description": "La façon dont on gère un manquement à la confiance en dit plus sur la relation que le manquement lui-même"}
    ],
    "trust_building_actions": [
      "Tenir les petits engagements avant les grands",
      "Être transparent sur ses limites et ses incertitudes",
      "Reconnaître ses erreurs rapidement et sans excès d'excuse",
      "Maintenir la cohérence même quand personne ne regarde",
      "Défendre l'autre en son absence (ne pas médire)"
    ],
    "trust_repair_after_breach": [
      "Reconnaître explicitement la rupture — ne pas minimiser",
      "Assumer sans se justifier à outrance",
      "Proposer une réparation concrète",
      "Agir différemment ensuite — les mots sans les actes aggravent la rupture",
      "Accepter que la reconstruction prend du temps"
    ],
    "alfred_trust_principles": [
      "ALFRED tient ses engagements conversationnels (rappeler ce qui a été dit)",
      "ALFRED est transparent sur ses incertitudes et ses erreurs",
      "ALFRED ne change pas de position sans explication",
      "ALFRED ne prétend pas savoir ce qu'il ne sait pas"
    ]
  },
  [
    {"prompt": "Comment regagner la confiance de quelqu'un après une erreur ?", "answer": "En trois étapes : reconnaître (sans minimiser ni sur-expliquer), réparer (une action concrète, pas juste des mots), et agir différemment dans le temps. La reconstruction est longue — et c'est normal. Ce qui compte : la cohérence de tes actes après la rupture, pas la qualité de tes excuses."},
    {"prompt": "Comment créer rapidement une relation de confiance avec un nouveau client ?", "answer": "Tenir les petits engagements en premier : livrer ce qu'on a promis à la date dite, répondre dans le délai annoncé. La confiance se bâtit sur la prévisibilité, pas sur les grandes déclarations. Et être transparent sur ce qu'on ne sait pas encore — ça rassure bien plus qu'une fausse certitude."}
  ],
  {"tone": "chaleureux, ancré dans les actes pas les intentions", "structure": ["identifier le type de confiance en jeu (fiabilité, bienveillance, compétence)", "proposer l'action concrète adaptée", "rappeler la temporalité"], "avoid": ["promettre la confiance rapide", "ignorer l'importance de la gestion des ruptures", "confondre sympathie et confiance"]},
  ["confiance", "fiabilité", "relation", "intégrité", "rupture", "interaction"],
  ["knowledges.human.social_behavior.social_bonding", "knowledges.human.emotional_intelligence.empathy", "knowledges.cpl.human_communication.client_interaction"]
))

save("human/interaction/emotional_mirroring.json", ku(
  "emotional_mirroring",
  "Mirroring émotionnel et validation",
  "Le mirroring (réflexion émotionnelle) consiste à refléter l'état émotionnel de l'autre pour lui montrer qu'il est compris. C'est le socle de l'écoute active et le mécanisme principal qui crée le sentiment d'être vraiment entendu.",
  "Le mirroring émotionnel est la technique par laquelle on reflète verbalement ou para-verbalement l'état émotionnel de son interlocuteur, renforçant le sentiment d'être compris et créant les conditions d'un dialogue de qualité.",
  {
    "mirroring_types": [
      {"type": "Mirroring verbal", "example": "Répéter les derniers mots ou reformuler le sentiment exprimé : 'Tu te sens dépassé par la situation'"},
      {"type": "Mirroring para-verbal", "example": "Adapter son ton et son rythme à celui de l'interlocuteur — voix douce si l'autre est triste"},
      {"type": "Validation émotionnelle", "example": "Reconnaître la légitimité de l'émotion : 'C'est normal que tu sois frustré dans cette situation'"},
      {"type": "Labelling", "example": "Nommer l'émotion perçue : 'Il me semble que tu es inquiet à ce sujet'"}
    ],
    "when_to_mirror": [
      "Quand l'interlocuteur exprime une émotion forte (frustration, tristesse, excitation)",
      "Avant de donner une information ou une solution",
      "Quand une demande de clarification semble venir d'un état émotionnel, pas d'un manque d'info",
      "Pour confirmer qu'on a bien compris avant de répondre"
    ],
    "limits": [
      "Le mirroring ne doit pas devenir répétition mécanique — c'est un outil, pas un script",
      "Ne pas exagérer ou dramatiser l'émotion reflétée",
      "Ne pas utiliser le mirroring pour manipuler ou créer un faux sentiment de proximité"
    ]
  },
  [
    {"prompt": "Je me sens complètement submergé.", "answer": "Je t'entends — être submergé, c'est difficile à tenir. Dis-moi ce qui pèse le plus en ce moment, et on commence par là. Pas besoin de tout résoudre d'un coup."},
    {"prompt": "Personne ne comprend ce que je vis en ce moment.", "answer": "C'est un sentiment très isolant. Qu'est-ce qui se passe pour toi en ce moment ? Je suis là, et je t'écoute vraiment."}
  ],
  {"tone": "doux, attentif, sans résoudre trop vite", "structure": ["refléter l'état émotionnel d'abord", "valider sa légitimité", "créer l'espace pour aller plus loin si l'autre le souhaite"], "avoid": ["proposer une solution avant d'avoir reflété l'émotion", "minimiser", "sur-dramatiser"]},
  ["mirroring", "validation", "écoute", "émotion", "empathie", "interaction"],
  ["knowledges.human.emotional_intelligence.active_listening", "knowledges.human.emotional_intelligence.empathy", "knowledges.human.interaction.conflict_decompression"]
))

save("human/interaction/nonverbal_reading.json", ku(
  "nonverbal_reading",
  "Lecture des signaux non-verbaux",
  "55% de la communication est non-verbale. Lire la posture, le regard, le ton et le rythme donne accès à ce que les mots ne disent pas — et souvent à ce que l'interlocuteur ne sait pas lui-même exprimer.",
  "La lecture des signaux non-verbaux est la capacité à interpréter les indices comportementaux (posture, regard, expressions faciales, gestes, ton, rythme) pour comprendre l'état émotionnel réel d'un interlocuteur au-delà de ses mots.",
  {
    "nonverbal_channels": [
      {"channel": "Posture", "signals": "Épaules tombées (fatigue/tristesse), corps fermé/bras croisés (défense), corps ouvert (disponibilité)"},
      {"channel": "Regard", "signals": "Contact visuel soutenu (engagement), fuite du regard (inconfort/mensonge), yeux écarquillés (surprise/peur)"},
      {"channel": "Expression faciale", "signals": "Micro-expressions souvent plus vraies que le discours — grimace rapide, sourcils froncés"},
      {"channel": "Ton et rythme", "signals": "Voix qui monte (excitation/colère), débit accéléré (anxiété), monotonie (tristesse/ennui)"},
      {"channel": "Gestes", "signals": "Toucher son visage (inconfort), gestes ouverts (enthousiasme), gestes figés (tension)"}
    ],
    "congruence_check": "La congruence est l'accord entre le message verbal et non-verbal. 'Ça va bien' dit avec une voix plate et le regard fuyant est incongruent — le non-verbal prime souvent sur le verbal.",
    "ai_limitation": "ALFRED ne perçoit pas les signaux non-verbaux visuels en conversation textuelle. En contexte vocal, le ton et le rythme peuvent être partiellement détectés. En contexte caméra, un module de vision peut enrichir la détection.",
    "inference_in_text": [
      "Majuscules ou ponctuation excessive = intensité émotionnelle",
      "Phrases très courtes = frustration ou fatigue",
      "Fautes d'orthographe inhabituelles = état émotionnel altéré",
      "Formulations hésitantes = incertitude ou inconfort"
    ]
  },
  [
    {"prompt": "Mon interlocuteur dit que ça va mais il a l'air absent — que penser ?", "answer": "La règle : quand verbal et non-verbal divergent, croire le non-verbal. Plutôt que d'insister, ouvrir doucement : 'Tu m'as l'air un peu ailleurs aujourd'hui — tu veux en parler ou tu préfères qu'on reste sur le sujet ?' Laisser l'espace sans forcer."},
    {"prompt": "Comment savoir si quelqu'un ment ?", "answer": "Les signaux classiques (regard fuyant, toucher le nez) sont des indicateurs, pas des preuves. La vraie signature du mensonge est l'incongruence : quelque chose dans la réponse ne correspond pas au contexte, au délai de réponse, au niveau de détail. Mais le doute reste — la certitude absolue n'existe pas en lecture non-verbale."}
  ],
  {"tone": "observateur, sans jugement, pédagogique", "structure": ["identifier le canal non-verbal en jeu", "repérer la congruence ou l'incongruence", "proposer une réponse adaptée"], "avoid": ["surinterpréter un seul signal isolé", "prétendre lire dans les pensées", "ignorer les variations culturelles des codes non-verbaux"]},
  ["non-verbal", "communication", "signaux", "posture", "ton", "interaction"],
  ["knowledges.human.social_behavior.communication_styles", "knowledges.human.emotional_intelligence.empathy", "knowledges.cpl.human_communication.communication_principles"]
))

save("human/interaction/question_calibration.json", ku(
  "question_calibration",
  "Calibration des questions",
  "La qualité d'une question détermine la qualité de la réponse. Questions ouvertes, fermées, miroirs et hypothétiques ont chacune leur usage — les calibrer au bon moment ouvre ou ferme le dialogue.",
  "La calibration des questions est l'art de choisir le type, la formulation et le timing d'une question pour obtenir l'information ou l'effet conversationnel souhaité — ouverture du dialogue, clarification, exploration, validation ou décision.",
  {
    "question_types": [
      {"type": "Ouverte", "structure": "Comment, Qu'est-ce qui, Qu'est-ce que tu penses de...", "use": "Explorer, comprendre, laisser l'autre s'exprimer librement"},
      {"type": "Fermée", "structure": "Est-ce que, As-tu, Faut-il...", "use": "Valider, confirmer, obtenir un engagement précis"},
      {"type": "Miroir", "structure": "Répéter les derniers mots avec une intonation montante", "use": "Encourager à développer sans orienter"},
      {"type": "Hypothétique", "structure": "Et si..., Imagine que..., Supposons que...", "use": "Explorer des options, dépasser les blocages, créer de la perspective"},
      {"type": "Clarificatrice", "structure": "Quand tu dis X, tu veux dire...", "use": "S'assurer de la compréhension mutuelle"},
      {"type": "Impact", "structure": "Qu'est-ce que ça change pour toi si...", "use": "Aider à prendre conscience des conséquences d'une décision"}
    ],
    "alfred_question_principles": [
      "Une seule question à la fois — deux questions dans le même message créent la confusion",
      "Privilégier les questions ouvertes pour explorer, fermées pour valider",
      "Poser une question hypothétique pour débloquer un raisonnement circulaire",
      "Ne jamais poser une question rhétorique qui implique un jugement"
    ],
    "bad_questions": [
      "'Pourquoi tu n'as pas...' — implicitement accusatoire",
      "'Tu n'es pas d'accord ?' — question négative qui oriente vers la réponse",
      "'Tu as compris ?' — met l'autre en position d'infériorité",
      "Questions multiples dans le même tour de parole"
    ]
  },
  [
    {"prompt": "Comment poser de meilleures questions en entretien ?", "answer": "Quatre règles : une question à la fois, formuler en ouvert ('Comment...' plutôt que 'Est-ce que...'), attendre la réponse complète sans couper, et utiliser le miroir quand tu veux que l'autre développe ('...tu dis surchargé ?' dit avec une intonation montante). Les meilleures questions sont souvent les plus simples."},
    {"prompt": "Je n'arrive pas à faire parler mon interlocuteur.", "answer": "Essaie la question hypothétique : 'Imagine que tout se passe parfaitement dans six mois — qu'est-ce qui a changé ?' ou 'Si tu devais choisir la priorité absolue de cette semaine, ce serait quoi ?' Les questions hypothétiques contournent la résistance et ouvrent les perspectives que les questions directes ferment."}
  ],
  {"tone": "pédagogique, curieux, orienté pratique", "structure": ["identifier l'objectif conversationnel", "choisir le type de question adapté", "formuler et anticiper la réponse"], "avoid": ["questions multiples dans le même message", "questions rhétoriques implicitement accusatoires", "questions fermées quand l'exploration est nécessaire"]},
  ["questions", "entretien", "exploration", "clarification", "dialogue", "interaction"],
  ["knowledges.human.interaction.adaptive_conversation_rhythm", "knowledges.human.emotional_intelligence.active_listening", "knowledges.cpl.product_ia.user_needs_analysis"]
))

save("human/interaction/presence_quality.json", ku(
  "presence_quality",
  "Qualité de présence dans l'interaction",
  "La présence pleine dans une interaction — écouter vraiment, être là sans arrière-pensée — est la ressource la plus rare et la plus valorisée. Elle ne peut pas être simulée sur la durée.",
  "La qualité de présence est la capacité à être pleinement disponible à l'autre dans l'interaction — attentif, non distrait, sans agenda caché — créant ainsi les conditions d'un échange authentique et de qualité.",
  {
    "presence_dimensions": [
      {"dimension": "Attention physique", "description": "Corps orienté vers l'autre, contact visuel, téléphone rangé"},
      {"dimension": "Attention cognitive", "description": "Pensées focalisées sur ce qui est dit, sans préparer sa réponse simultanément"},
      {"dimension": "Attention émotionnelle", "description": "Résonance avec l'état émotionnel de l'autre, sans projection de ses propres émotions"},
      {"dimension": "Attention intentionnelle", "description": "Être là pour l'autre, pas pour en tirer quelque chose"}
    ],
    "presence_blockers": [
      "Smartphone visible même si non utilisé — signal d'interruption potentielle",
      "Préparation mentale de la prochaine réponse pendant que l'autre parle",
      "Fatigue qui réduit la bande passante attentionnelle",
      "Agenda caché (vouloir convaincre plutôt qu'écouter)",
      "Pensées parasites sur d'autres sujets"
    ],
    "alfred_presence": "Dans un échange textuel, ALFRED simule la présence par la cohérence de ses réponses avec ce qui vient d'être dit, l'absence de réponses génériques, et la personnalisation continue au fil de la conversation."
  },
  [
    {"prompt": "Comment être vraiment présent lors d'une réunion importante ?", "answer": "Deux gestes concrets : téléphone hors de vue (même face retournée — la présence potentielle suffit à créer une distraction), et décider d'écouter avant de décider de répondre. Beaucoup de gens sont physiquement présents mais mentalement en train de formuler leur prochaine intervention. La présence réelle est d'abord une décision."},
    {"prompt": "Comment savoir si quelqu'un m'écoute vraiment ?", "answer": "Ils reformulent ce que tu viens de dire avant de répondre. Ils posent des questions sur ce que tu as dit, pas des questions qui dérivent vers leur propre sujet. Leur réponse est spécifique, pas générique. Et physiquement : ils te regardent, ils ne touchent pas leur téléphone. La présence véritable laisse des traces concrètes."}
  ],
  {"tone": "ancré, calme, valorisant la qualité sur la quantité", "structure": ["identifier le type de distraction ou de blocage", "proposer un ajustement concret", "rappeler pourquoi la présence change la qualité de l'échange"], "avoid": ["être moralisateur sur l'usage des écrans", "proposer une présence parfaite inaccessible", "ignorer les contraintes d'énergie et de fatigue"]},
  ["présence", "attention", "écoute", "qualité", "interaction", "focus"],
  ["knowledges.human.cognition.focus_management", "knowledges.human.interaction.cognitive_overload_signals", "knowledges.human.emotional_intelligence.active_listening"]
))

print("\nBatch human/interaction (10 premiers) : DONE")
