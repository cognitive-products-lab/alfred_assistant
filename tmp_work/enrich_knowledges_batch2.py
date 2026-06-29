"""
Enrichissement Knowledge Base ALFRED - Batch 2 : CPL ProductIA + HumanComm + Ethics
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

# =============================================================================
# CPL / PRODUCT IA
# =============================================================================

save("cpl/product_ia/product_design_methodology.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.product_ia.product_design_methodology",
  "title": "Méthodologie de design produit IA",
  "domain": "cpl", "subdomain": "product_ia",
  "status": "validated",
  "summary": "Designer un produit IA exige de combiner discovery utilisateur, faisabilité technique et éthique. Le design part toujours d'un problème réel, pas d'une technologie disponible.",
  "core_definition": "La méthodologie de design produit IA est un processus itératif qui articule la compréhension des besoins utilisateurs, la définition d'une proposition de valeur, la conception des interactions (UX/conversation), l'intégration des modèles IA et la validation continue en conditions réelles.",
  "knowledge": {
    "design_process": [
      {"phase": "Discovery", "actions": ["Interviews utilisateurs (jobs-to-be-done)", "Cartographie des douleurs actuelles", "Benchmark des alternatives"], "output": "Problem statement validé"},
      {"phase": "Define", "actions": ["Personas prioritaires", "User stories IA (avec attendus et cas limites)", "Critères d'évaluation de la qualité IA"], "output": "Scope produit et critères de succès"},
      {"phase": "Design", "actions": ["Conversation design (flow de dialogue)", "UI minimaliste centrée sur la confiance", "Fallbacks et gestion des erreurs IA"], "output": "Prototype basse fidélité"},
      {"phase": "Prototype & Test", "actions": ["Test utilisateur sur le prototype", "Évaluation de la qualité des réponses IA", "Ajustements prompts / modèle"], "output": "MVP validé"},
      {"phase": "Itérer", "actions": ["Métriques d'usage et satisfaction", "Feedback loops", "Versioning du modèle"], "output": "Produit évolutif"}
    ],
    "ai_product_specificities": [
      "Le comportement du modèle IA est non déterministe — prévoir des tests systématiques sur des cas limites",
      "La confiance utilisateur se construit par la transparence sur les limites du système",
      "Les hallucinations doivent être mitigées par design (sources, hedges, fallbacks)",
      "Le design conversationnel remplace souvent le design d'interface classique",
      "La latence perçue impacte la satisfaction — optimiser les temps de réponse ou les masquer"
    ],
    "trust_design_principles": [
      "Annoncer clairement que l'utilisateur interagit avec une IA",
      "Montrer les sources quand possible",
      "Permettre à l'utilisateur de corriger ou remettre en question une réponse",
      "Ne jamais simuler une certitude que le système n'a pas",
      "Expliquer pourquoi l'IA ne peut pas répondre à certaines questions"
    ]
  },
  "example_answers": [
    {"prompt": "Comment concevoir les interactions d'un assistant IA ?", "answer": "On part des conversations réelles : quelles questions les utilisateurs posent, dans quel ordre, avec quel niveau de précision ? On mappe les intentions (intents) et les réponses attendues. Ensuite on conçoit les cas nominaux et les cas limites (question floue, hors périmètre, réponse incorrecte). Un bon assistant IA gère l'échec aussi bien que le succès."},
    {"prompt": "Comment éviter que l'IA hallucine en production ?", "answer": "Design défensif : borner le domaine de réponse (RAG sur une base de connaissance maîtrisée), ajouter des phrases de hedge ('je ne suis pas certain mais...'), afficher les sources, et laisser l'utilisateur valider. Aucun système LLM ne garantit l'exactitude — le design doit le prendre en compte."},
    {"prompt": "Quelle différence entre UX classique et conversation design ?", "answer": "L'UX classique conçoit des interfaces visuelles avec des états, des boutons, des flows. Le conversation design conçoit des échanges en langage naturel avec des intentions, des entités, des tours de parole et des stratégies de récupération. Les deux partagent le même objectif : que l'utilisateur arrive à ses fins sans friction."}
  ],
  "response_guidance": {
    "tone": "pratique, orienté terrain, sensible aux contraintes IA",
    "structure": ["identifier la phase du projet produit", "pointer les spécificités IA à anticiper", "recommander une action concrète", "signaler les pièges classiques"],
    "avoid": ["traiter un produit IA comme un produit logiciel standard", "ignorer la question de la confiance utilisateur", "recommander sans tenir compte des capacités réelles du modèle disponible"]
  },
  "tags": ["design produit", "IA", "conversation design", "UX IA", "trust", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.product_ia.user_needs_analysis", "knowledges.cpl.product_ia.tech_tradeoff_framework", "knowledges.professional.engineering.ai.prompt_engineering"]
})

save("cpl/product_ia/user_needs_analysis.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.product_ia.user_needs_analysis",
  "title": "Analyse des besoins utilisateurs",
  "domain": "cpl", "subdomain": "product_ia",
  "status": "validated",
  "summary": "Comprendre les vrais besoins utilisateurs exige d'aller au-delà des demandes exprimées. La méthode Jobs-to-be-Done, les entretiens et l'observation permettent de découvrir les douleurs latentes et les motivations profondes.",
  "core_definition": "L'analyse des besoins utilisateurs est le processus de compréhension approfondie des motivations, douleurs, contextes et objectifs réels des utilisateurs cibles, au-delà de leurs demandes de surface. Elle est la base de tout produit qui résout un vrai problème.",
  "knowledge": {
    "discovery_methods": [
      {"method": "Entretien utilisateur", "when": "Phase de discovery, avant de coder", "tips": ["Poser des questions ouvertes", "Aller au 'pourquoi' derrière chaque réponse", "Observer les comportements réels, pas les intentions déclarées"]},
      {"method": "Jobs-to-be-Done (JTBD)", "when": "Quand on veut comprendre la vraie motivation d'usage", "tips": ["Que cherche l'utilisateur à accomplir dans sa vie / son travail ?", "Quel progrès veut-il faire ?", "Que se passe-t-il s'il n'y arrive pas ?"]},
      {"method": "Shadowing / Observation", "when": "Pour découvrir les frictions non verbalisées", "tips": ["Observer sans intervenir", "Noter les moments de confusion ou d'hésitation", "Identifier les workarounds spontanés"]},
      {"method": "Analyse de données d'usage", "when": "Sur un produit existant", "tips": ["Où les utilisateurs abandonnent-ils ?", "Quelles fonctions sont les plus / moins utilisées ?", "Quels patterns révèlent des besoins non servis ?"]}
    ],
    "need_types": [
      {"type": "Besoins fonctionnels", "example": "Organiser mes tâches, retrouver une information rapidement"},
      {"type": "Besoins émotionnels", "example": "Se sentir compétent, ne pas stresser, avoir confiance"},
      {"type": "Besoins sociaux", "example": "Être perçu comme compétent par ses pairs, collaborer facilement"},
      {"type": "Besoins latents", "example": "Besoins réels que l'utilisateur n'exprime pas car il ne les voit pas encore"}
    ],
    "common_biases": [
      "Confondre ce que l'utilisateur dit vouloir et ce dont il a besoin",
      "Généraliser à partir de trop peu d'entretiens (minimum 5-7 pour commencer à saturer)",
      "Sélectionner uniquement des utilisateurs enthousiastes — les sceptiques sont plus informatifs",
      "Poser des questions fermées qui confirment l'hypothèse de départ"
    ]
  },
  "example_answers": [
    {"prompt": "Comment savoir ce que veulent vraiment nos utilisateurs ?", "answer": "En posant des questions ouvertes sur leurs problèmes actuels, pas sur les features souhaitées. 'Décris-moi ta dernière semaine de travail' révèle plus que 'Qu'est-ce qu'on devrait ajouter ?' Les utilisateurs décrivent leurs douleurs mieux qu'ils ne prescrivent des solutions."},
    {"prompt": "On a 500 retours utilisateurs, comment les analyser ?", "answer": "Classer les retours par thème (pas par feature) : quels problèmes reviennent ? Quel niveau d'intensité ('c'est gênant' vs 'c'est bloquant') ? Ensuite remonter à la cause racine — un même problème peut avoir des expressions très différentes. Prioriser selon l'intensité et la fréquence."},
    {"prompt": "Comment mener un bon entretien utilisateur en 30 minutes ?", "answer": "Trois parties : contexte (qui tu es, comment tu travailles aujourd'hui — 10 min), douleurs actuelles (ce qui te frustre, ce que tu contournes — 15 min), validation légère de l'hypothèse produit en dernier (5 min, sans pitcher). L'erreur classique : pitcher trop tôt et biaiser toutes les réponses suivantes."}
  ],
  "response_guidance": {
    "tone": "curieux, centré utilisateur, ancré dans l'observation",
    "structure": ["identifier la méthode adaptée au stade", "guider la collecte", "aider à l'interprétation", "pointer les biais potentiels"],
    "avoid": ["confondre feedback quantitatif et compréhension qualitative", "valider des hypothèses au lieu de les tester", "ignorer les utilisateurs non-enthousiastes"]
  },
  "tags": ["besoins utilisateurs", "JTBD", "discovery", "entretien", "UX research", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.product_ia.product_design_methodology", "knowledges.professional.product_management.product_discovery", "knowledges.professional.product_management.user_feedback_loops"]
})

save("cpl/product_ia/tech_tradeoff_framework.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.product_ia.tech_tradeoff_framework",
  "title": "Cadre de décision technique (tradeoffs)",
  "domain": "cpl", "subdomain": "product_ia",
  "status": "validated",
  "summary": "Chaque choix technique implique des compromis : performance vs coût, flexibilité vs rapidité, contrôle vs dépendance. Un cadre de tradeoffs structure ces arbitrages en alignant les décisions tech sur les priorités business.",
  "core_definition": "Le cadre de décision technique (tech tradeoff framework) est un outil d'analyse qui permet de comparer des options techniques selon plusieurs dimensions (performance, coût, maintenabilité, sécurité, time-to-market, dépendance) pour prendre des décisions alignées sur les objectifs business actuels.",
  "knowledge": {
    "tradeoff_dimensions": [
      {"dimension": "Performance vs Coût", "question": "Quelle latence / qualité est acceptable face à quel coût d'infrastructure ?"},
      {"dimension": "Build vs Buy", "question": "Développer en interne vs utiliser une solution existante — impact sur le contrôle, la différenciation et la dette technique"},
      {"dimension": "Flexibilité vs Rapidité", "question": "Architecture générique et évolutive vs solution spécialisée et rapide à déployer"},
      {"dimension": "Contrôle vs Dépendance", "question": "Maîtrise totale (open source, local) vs dépendance à un fournisseur (SaaS, API)"},
      {"dimension": "Qualité vs Time-to-market", "question": "Perfectionnisme qui retarde vs MVP imparfait qui apprend vite"},
      {"dimension": "Scalabilité vs Simplicité", "question": "Architecture scalable mais complexe vs architecture simple mais limitée"}
    ],
    "decision_process": [
      "Définir les critères non-négociables (sécurité, RGPD, performance minimale)",
      "Identifier les contraintes actuelles (budget, équipe, délai)",
      "Scorer chaque option sur chaque dimension selon l'importance business actuelle",
      "Choisir l'option avec le meilleur alignement — pas la solution parfaite, la solution adaptée maintenant",
      "Documenter les hypothèses pour réévaluer dans 6 mois"
    ],
    "ai_specific_tradeoffs": [
      {"tradeoff": "LLM local vs API externe", "local": "Confidentialité, coût fixe, latence maîtrisée", "api": "Qualité supérieure, maintenance nulle, coût variable"},
      {"tradeoff": "RAG vs Fine-tuning", "rag": "Flexible, actualisable, transparent sur les sources", "fine_tuning": "Meilleure cohérence stylistique, nécessite des données annotées et plus de coût"},
      {"tradeoff": "Embeddings propriétaires vs open source", "proprietary": "Performance haute, coût récurrent", "open_source": "Contrôle total, qualité variable selon le modèle"}
    ]
  },
  "example_answers": [
    {"prompt": "Faut-il utiliser l'API OpenAI ou un modèle local pour ALFRED ?", "answer": "Dépend des priorités : si la confidentialité des données est critique (données personnelles, usage local), un modèle local comme Llama / Mistral via Ollama est préférable malgré une qualité inférieure. Si la qualité de la réponse prime et que les données ne sont pas sensibles, l'API OpenAI reste supérieure aujourd'hui. ALFRED peut gérer les deux en parallèle selon le contexte."},
    {"prompt": "On doit choisir entre MongoDB et PostgreSQL pour stocker la mémoire d'ALFRED.", "answer": "Pour de la mémoire conversationnelle structurée (épisodes, contextes), PostgreSQL avec JSONB est plus maintenable et queryable. MongoDB convient mieux si les schémas de données sont très variables ou si la scalabilité horizontale est critique dès le départ — rarement le cas en early stage. PostgreSQL + pgvector pour les embeddings est une stack solide et simple."},
    {"prompt": "Comment choisir entre construire ou acheter une solution de vector database ?", "answer": "Acheter (Pinecone, Weaviate, Qdrant cloud) si tu veux avancer vite et que la maintenance infra n'est pas un objectif. Construire (pgvector, Chroma local) si tu as des contraintes de confidentialité, de coût ou de contrôle. En early stage, commencer par le plus simple — migrer plus tard si nécessaire."}
  ],
  "response_guidance": {
    "tone": "analytique, sans dogmatisme technologique, ancré dans les contraintes réelles",
    "structure": ["identifier les dimensions de tradeoff pertinentes", "collecter les contraintes non-négociables", "comparer les options sur les critères clés", "recommander avec les hypothèses explicites"],
    "avoid": ["imposer une technologie sans connaître les contraintes", "ignorer le time-to-market", "sous-estimer la dette technique des décisions rapides"]
  },
  "tags": ["tradeoff", "décision technique", "build vs buy", "architecture", "IA", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.product_ia.product_design_methodology", "knowledges.professional.engineering.ai.rag_architecture", "knowledges.professional.engineering.systeme_design.software_architecture"]
})

# =============================================================================
# CPL / HUMAN COMMUNICATION
# =============================================================================

save("cpl/human_communication/communication_principles.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.human_communication.communication_principles",
  "title": "Principes de communication humaine",
  "domain": "cpl", "subdomain": "human_communication",
  "status": "validated",
  "summary": "Une communication efficace adapte son message au destinataire, au contexte et au canal. Clarté, écoute active et intention explicite sont les trois piliers d'une communication qui crée de la confiance.",
  "core_definition": "Les principes de communication humaine décrivent les mécanismes fondamentaux par lesquels les individus transmettent et reçoivent des informations, des émotions et des intentions. Une communication efficace aligne le message émis, le canal choisi et la compréhension du destinataire.",
  "knowledge": {
    "communication_model": {
      "elements": ["Émetteur (intention, état émotionnel)", "Message (contenu verbal + non-verbal)", "Canal (oral, écrit, visuel, synchrone, asynchrone)", "Récepteur (interprétation, contexte, filtres cognitifs)", "Bruit (interférences, ambiguïtés, préjugés)", "Feedback (confirmation de compréhension)"],
      "key_insight": "Ce qui compte n'est pas ce qu'on dit, mais ce que l'autre comprend."
    },
    "principles": [
      "Clarté : message simple, une idée principale par échange",
      "Intention explicite : dire ce qu'on attend de l'interlocuteur (information, décision, soutien)",
      "Écoute active : reformuler, poser des questions, ne pas préparer sa réponse pendant que l'autre parle",
      "Adaptation : ajuster le registre, la profondeur et le vocabulaire au destinataire",
      "Feedback loop : vérifier que le message a été compris comme voulu",
      "Timing : choisir le bon moment (état émotionnel de l'autre, contexte de disponibilité)"
    ],
    "communication_styles": [
      {"style": "Assertif", "description": "Direct, clair sur ses besoins, respectueux de l'autre — style à privilégier"},
      {"style": "Passif", "description": "Évite le conflit, ne dit pas vraiment ce qu'il pense — crée de la frustration latente"},
      {"style": "Agressif", "description": "Direct mais sans respect — défensif, ferme l'écoute"},
      {"style": "Passif-agressif", "description": "Apparemment doux mais sous-entendus négatifs — toxique dans le temps"}
    ],
    "non_verbal_weight": "55% de la communication est non-verbale (posture, regard, mimiques), 38% paraverbal (ton, rythme, volume), 7% seulement verbal (les mots). Dans un contexte écrit ou IA : la formulation porte 100% du sens, d'où l'importance du ton et de la précision."
  },
  "example_answers": [
    {"prompt": "Comment améliorer ma communication avec mon équipe ?", "answer": "Commence par vérifier que tes messages contiennent toujours : l'information principale, ce que tu attends de l'autre (réponse, décision, action), et le délai. Beaucoup de malentendus viennent d'intentions non formulées. Et pose la question : 'Comment tu as compris ça ?' — les divergences d'interprétation se révèlent vite."},
    {"prompt": "Comment dire quelque chose de difficile sans blesser ?", "answer": "Structure en trois temps : d'abord les faits observables (sans jugement), ensuite l'impact que ça a créé, enfin ce que tu attends. 'Lors de la réunion, quand la présentation a été coupée, j'ai perdu le fil et le client aussi. J'aimerais qu'on prépare un plan B pour la prochaine fois.' — factuel, non agressif, orienté solution."},
    {"prompt": "Pourquoi un message clair pour moi est mal compris par les autres ?", "answer": "La malédiction de la connaissance : on oublie ce que c'est de ne pas savoir ce qu'on sait. Ce qui est évident pour toi est opaque pour quelqu'un sans ton contexte. Remède : expliciter les hypothèses, définir les termes techniques, demander une reformulation. Le test : un non-spécialiste peut-il comprendre sans questions ?"}
  ],
  "response_guidance": {
    "tone": "bienveillant, clair, non moralisateur",
    "structure": ["identifier le type de situation communicationnelle", "pointer le mécanisme en jeu", "proposer une formulation ou une méthode", "anticiper la réaction de l'interlocuteur"],
    "avoid": ["donner des leçons de communication", "ignorer le contexte émotionnel de la situation", "recommander l'assertivité sans tenir compte des enjeux de pouvoir"]
  },
  "tags": ["communication", "assertivité", "écoute active", "message", "clarté", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.human_communication.client_interaction", "knowledges.human.skills.softskills.communication", "knowledges.human.emotional_intelligence.empathy"]
})

save("cpl/human_communication/client_interaction.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.human_communication.client_interaction",
  "title": "Interaction client — principes et pratiques",
  "domain": "cpl", "subdomain": "human_communication",
  "status": "validated",
  "summary": "Une relation client solide se construit sur la confiance, la clarté des attentes et la capacité à gérer les imprévus avec professionnalisme. Chaque interaction est une opportunité de renforcer ou d'éroder cette confiance.",
  "core_definition": "L'interaction client englobe l'ensemble des échanges entre un prestataire ou un produit et ses clients : onboarding, suivi de projet, gestion des attentes, escalades et clôture. La qualité de ces interactions détermine la satisfaction, la fidélité et les recommandations.",
  "knowledge": {
    "interaction_phases": [
      {"phase": "Onboarding", "objective": "Créer confiance, aligner les attentes, définir les règles du jeu", "pitfalls": "Promettre sans encadrer les conditions, négliger le suivi initial"},
      {"phase": "Suivi actif", "objective": "Maintenir la visibilité sur l'avancement, anticiper les blocages", "pitfalls": "Silence entre les livrables, absence de proactivité sur les problèmes"},
      {"phase": "Gestion des difficultés", "objective": "Communiquer rapidement, proposer des solutions, ne pas défensif", "pitfalls": "Cacher un problème, rejeter la responsabilité, promettre sans tenir"},
      {"phase": "Clôture et fidélisation", "objective": "Valider la satisfaction, capitaliser sur la relation, explorer les suites", "pitfalls": "Disparaître après livraison, ne pas demander de retex"}
    ],
    "client_communication_rules": [
      "Anticiper les questions avant qu'elles soient posées",
      "Toujours confirmer par écrit les décisions verbales",
      "Ne jamais annoncer un problème sans proposer une solution ou une alternative",
      "Adapter le niveau de détail technique au profil du client",
      "Être proactif sur les délais : mieux vaut annoncer un retard tôt qu'une surprise à la deadline"
    ],
    "difficult_situations": [
      {"situation": "Client insatisfait", "response": "Écouter sans se défendre d'abord, valider le ressenti, puis expliquer et proposer une solution concrète"},
      {"situation": "Demande hors scope", "response": "Reconnaître la valeur de la demande, expliquer l'impact scope/délai/coût, proposer un devis ou un report"},
      {"situation": "Retard sur livraison", "response": "Prévenir le plus tôt possible, expliquer la cause sans excuses excessives, donner une nouvelle date ferme"},
      {"situation": "Malentendu sur les attentes", "response": "Revenir aux éléments écrits (brief, cahier des charges), reformuler ensemble l'attendu, repartir d'un commun accord"}
    ]
  },
  "example_answers": [
    {"prompt": "Un client est mécontent d'un livrable, comment réagir ?", "answer": "Première étape : écouter sans interrompre ni se justifier. 'Je comprends ta déception, dis-moi précisément ce qui ne correspond pas à tes attentes.' Une fois le problème bien cerné : proposer une solution concrète et un délai. Ne pas sur-promettre pour calmer — promettre ce qu'on peut tenir, tenir ce qu'on promet."},
    {"prompt": "Comment annoncer un retard à un client ?", "answer": "Le plus tôt possible — pas à la deadline. Formuler : la nouvelle date ferme, la cause (sans excuse excessive), ce qu'on fait pour rattraper. 'Je préfère te prévenir maintenant plutôt que te surprendre vendredi : la livraison sera décalée au [date] en raison de [cause]. Voilà ce qu'on met en place pour tenir ce nouvel engagement.' Court et professionnel."},
    {"prompt": "Le client demande une fonctionnalité hors scope, comment dire non ?", "answer": "Ne pas dire 'non' brut — dire 'oui, et voilà ce que ça implique'. 'C'est une bonne idée. Pour l'intégrer dans ce projet, il faudrait ajouter X jours et Y euros. Je peux en faire un devis, ou on peut l'inscrire en priorité pour la prochaine phase.' La demande est valorisée, les contraintes sont explicites, le client choisit."}
  ],
  "response_guidance": {
    "tone": "professionnel, empathique, orienté solution",
    "structure": ["identifier la phase de la relation client", "calibrer le message selon l'enjeu émotionnel", "formuler concrètement", "anticiper la réaction et les suites"],
    "avoid": ["promettre ce qu'on ne peut pas tenir pour calmer", "être défensif ou rejeter la responsabilité", "utiliser du jargon technique avec un client non technique"]
  },
  "tags": ["client", "relation client", "communication", "confiance", "gestion de projet", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.human_communication.communication_principles", "knowledges.cpl.execution.project_management_core", "knowledges.human.skills.softskills.assertiveness"]
})

save("cpl/human_communication/emotional_intelligence.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.human_communication.emotional_intelligence",
  "title": "Intelligence émotionnelle en contexte professionnel",
  "domain": "cpl", "subdomain": "human_communication",
  "status": "validated",
  "summary": "L'intelligence émotionnelle en contexte pro, c'est la capacité à reconnaître ses propres émotions et celles des autres pour adapter son comportement et créer des interactions productives, même sous pression.",
  "core_definition": "L'intelligence émotionnelle (IE) en contexte professionnel est la capacité à identifier, comprendre et gérer ses propres émotions et celles de ses interlocuteurs afin d'améliorer la qualité des relations, des décisions et des performances collectives.",
  "knowledge": {
    "ie_components": [
      {"component": "Conscience de soi", "description": "Reconnaître ses propres émotions en temps réel et leur impact sur ses décisions et comportements"},
      {"component": "Maîtrise de soi", "description": "Réguler ses réactions émotionnelles — ne pas agir sous l'impulsion, surtout sous pression"},
      {"component": "Motivation intrinsèque", "description": "Rester orienté vers ses objectifs malgré les obstacles, sans dépendre de la validation externe"},
      {"component": "Empathie", "description": "Comprendre le point de vue et les émotions des autres, même sans les partager"},
      {"component": "Compétences sociales", "description": "Créer et maintenir des relations, influencer positivement, gérer les conflits"}
    ],
    "professional_applications": [
      "Feedback : donner une critique constructive en reconnaissant d'abord l'effort",
      "Conflit : désamorcer une tension en nommant l'émotion perçue ('j'ai l'impression que tu es frustré par cette situation')",
      "Négociation : lire les signaux non-verbaux pour adapter le timing et le message",
      "Leadership : créer un environnement où les équipes se sentent en sécurité pour s'exprimer",
      "Décision sous pression : différer une décision importante quand l'état émotionnel est altéré"
    ],
    "ie_in_ai_interactions": [
      "Détecter les signaux émotionnels dans les messages (frustration, anxiété, enthousiasme)",
      "Adapter le ton avant d'adapter le contenu",
      "Valider l'état émotionnel avant de proposer des solutions",
      "Ne jamais minimiser une difficulté ('c'est simple') quand l'utilisateur la perçoit comme difficile",
      "Proposer une aide sans créer de dépendance émotionnelle"
    ]
  },
  "example_answers": [
    {"prompt": "Mon collègue s'est énervé en réunion, comment gérer ?", "answer": "D'abord, ne pas répondre à l'énervement par un contre-argument — ça escalade. Reconnaître : 'Je vois que tu es frustré par cette situation.' Puis marquer une pause si possible. Une fois la tension retombée, aborder le fond : 'On reprend quand tu veux, le sujet mérite qu'on le traite calmement.'"},
    {"prompt": "Comment donner du feedback négatif sans créer de conflit ?", "answer": "Structure SBI : Situation (le contexte précis), Behavior (le comportement observable, pas la personne), Impact (ce que ça a produit concrètement). 'Lors de la présentation de lundi, quand les données de la slide 3 n'étaient pas à jour, le client a perdu confiance. J'aimerque les chiffres soient toujours vérifiés la veille.' — factuel, non personnel, orienté amélioration."},
    {"prompt": "Je suis stressé avant une décision importante, que faire ?", "answer": "L'état émotionnel altère la qualité des décisions. Si possible, différer de quelques heures. Sinon, externaliser : écrire la décision à prendre, les options, les critères — ça sort la décision de la tête où les émotions brouillent tout. Et demander un regard extérieur si l'enjeu est élevé."}
  ],
  "response_guidance": {
    "tone": "empathique, sans jugement, orienté pratique",
    "structure": ["reconnaître l'état émotionnel sous-jacent", "valider avant d'expliquer", "proposer une méthode concrète", "laisser l'utilisateur choisir"],
    "avoid": ["minimiser les émotions ('c'est normal, ça arrive à tout le monde')", "donner des conseils non demandés sur la gestion émotionnelle", "confondre intelligence émotionnelle et manipulation"]
  },
  "tags": ["intelligence émotionnelle", "empathie", "feedback", "conflit", "relations pro", "cpl"],
  "related_knowledge_units": ["knowledges.human.emotional_intelligence.empathy", "knowledges.human.emotional_intelligence.self_regulation", "knowledges.cpl.human_communication.communication_principles"]
})

# =============================================================================
# CPL / HUMAN ORGANIZATION
# =============================================================================

save("cpl/human_organization/energy_management.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.human_organization.energy_management",
  "title": "Gestion de l'énergie personnelle",
  "domain": "cpl", "subdomain": "human_organization",
  "status": "validated",
  "summary": "L'énergie, pas le temps, est la ressource centrale de la performance. Gérer son énergie revient à alterner charge et récupération, aligner les tâches cognitives sur les pics d'énergie, et protéger sa capacité à travailler dans la durée.",
  "core_definition": "La gestion de l'énergie personnelle (Energy Management) est la pratique d'optimiser sa capacité physique, cognitive, émotionnelle et motivationnelle pour maintenir une performance durable sans s'épuiser. Elle s'oppose à la gestion du temps pure, qui ignore la qualité de l'attention disponible.",
  "knowledge": {
    "energy_dimensions": [
      {"dimension": "Physique", "description": "Sommeil, alimentation, mouvement — le socle sur lequel tout repose", "signals": "Fatigue chronique, maux de tête, tensions musculaires"},
      {"dimension": "Cognitive", "description": "Capacité de concentration, de raisonnement, de création", "signals": "Difficulté à se concentrer, erreurs fréquentes, pensée ralentie"},
      {"dimension": "Émotionnelle", "description": "Régulation des émotions, résilience face au stress, qualité des relations", "signals": "Irritabilité, surréaction, isolement"},
      {"dimension": "Motivationnelle", "description": "Sens, alignement valeurs/actions, engagement", "signals": "Procrastination, cynisme, désengagement"}
    ],
    "energy_management_practices": [
      "Identifier ses pics d'énergie quotidiens et planifier les tâches cognitives lourdes à ces moments",
      "Blocs de travail focalisé (90 min max) alternés avec des micro-récupérations (10-15 min)",
      "Fin de journée rituel de clôture (lister les 3 choses faites + les 2 priorités de demain)",
      "Protéger le sommeil comme une priorité non-négociable (qualité > quantité)",
      "Identifier et éliminer les activités 'énergivores' à faible valeur",
      "Alimentation et hydratation comme levier cognitif (pic glycémique = crash attentionnel)"
    ],
    "recovery_types": [
      {"type": "Micro-récupération", "duration": "5-15 min", "exemples": "marcher, s'étirer, regarder par la fenêtre, respiration"},
      {"type": "Meso-récupération", "duration": "30-90 min", "exemples": "déjeuner sans écran, sieste courte (20 min), sortie en nature"},
      {"type": "Macro-récupération", "duration": "2 jours à 2 semaines", "exemples": "weekend déconnecté, vacances réelles (sans email)"}
    ],
    "burnout_early_signals": [
      "Fatigue qui ne disparaît pas après une nuit de sommeil",
      "Perte de plaisir dans des activités habituellement appréciées",
      "Irritabilité disproportionnée face à des micro-événements",
      "Difficulté croissante à démarrer les tâches (procrastination inhabituelle)",
      "Sentiment de ne jamais 'en faire assez' malgré le travail effectué"
    ]
  },
  "example_answers": [
    {"prompt": "Je suis épuisé mais j'ai encore beaucoup à faire — comment gérer ?", "answer": "L'épuisement sur une tâche cognitive nuit à la qualité du résultat. 20 minutes de récupération réelle (marche, repos sans écran) permettent souvent de récupérer 2h de performance. Ce n'est pas perdre du temps — c'est en gagner. Identifier la tâche la plus critique et la faire en premier, puis prendre une vraie pause."},
    {"prompt": "Comment mieux gérer mon énergie dans la journée ?", "answer": "D'abord : observer son rythme naturel pendant 3 jours. Quand es-tu le plus alerte ? Quand as-tu un creux ? Planifier le travail profond (écriture, analyse, code) sur les pics, les tâches légères (emails, admin) sur les creux. Et introduire deux micro-pauses actives dans la matinée et l'après-midi."},
    {"prompt": "Je sens que je vais vers le burnout — quels signaux prendre au sérieux ?", "answer": "Quatre signaux critiques : fatigue qui persiste après sommeil, irritabilité hors contexte, perte de sens ('à quoi ça sert'), erreurs inhabituelles. Si tu cumules trois de ces quatre, il faut ralentir maintenant. Pas réduire légèrement — vraiment ralentir. Et en parler à quelqu'un de confiance ou à un professionnel si ça dure."}
  ],
  "response_guidance": {
    "tone": "bienveillant, ancré dans le concret, sans injonction à la performance",
    "structure": ["identifier la dimension d'énergie concernée", "reconnaître l'état actuel sans minimiser", "proposer une action de récupération immédiate", "suggérer un ajustement structurel si pertinent"],
    "avoid": ["répondre 'travaille plus intelligemment' sans méthode", "ignorer les signaux de burnout", "confondre optimisation de l'énergie et glorification de la productivité"]
  },
  "tags": ["énergie", "burnout", "récupération", "focus", "performance durable", "cpl"],
  "related_knowledge_units": ["knowledges.human.wellbeing.burnout_signals", "knowledges.lifestyle.health.fatigue_management", "knowledges.human.self_alignment.routines.energy_management"]
})

# =============================================================================
# CPL / ETHICS GOVERNANCE
# =============================================================================

save("cpl/ethics_governance/ethical_ai_framework.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.ethics_governance.ethical_ai_framework",
  "title": "Cadre éthique pour l'IA",
  "domain": "cpl", "subdomain": "ethics_governance",
  "status": "validated",
  "summary": "Une IA éthique est transparente sur ses limites, équitable dans ses réponses, respectueuse de la vie privée et conçue pour augmenter l'autonomie humaine — jamais pour la remplacer ou la manipuler.",
  "core_definition": "Le cadre éthique pour l'IA est l'ensemble des principes, règles et pratiques qui guident la conception, le déploiement et l'usage d'un système IA de manière responsable, équitable et respectueuse des droits fondamentaux des individus.",
  "knowledge": {
    "core_principles": [
      {"principle": "Transparence", "description": "L'utilisateur sait qu'il interagit avec une IA et comprend ses limites", "alfred_application": "ALFRED annonce clairement qu'il est une IA, hedges ses incertitudes, ne simule pas une certitude qu'il n'a pas"},
      {"principle": "Équité", "description": "Pas de discrimination selon le genre, l'origine, l'âge ou la situation socio-économique", "alfred_application": "Réponses identiques en qualité quelle que soit la formulation ou le profil de l'utilisateur"},
      {"principle": "Vie privée", "description": "Minimisation des données collectées, consentement éclairé, stockage sécurisé", "alfred_application": "Données stockées localement, pas de transfert vers le cloud sans consentement explicite"},
      {"principle": "Sécurité", "description": "Le système ne peut pas être détourné pour nuire", "alfred_application": "Refus des demandes offensives, des tentatives de manipulation ou d'extraction d'informations sensibles"},
      {"principle": "Responsabilité", "description": "Des humains restent responsables des décisions assistées par l'IA", "alfred_application": "ALFRED propose, aide à réfléchir, mais laisse toujours la décision finale à l'utilisateur"},
      {"principle": "Bénéfice humain", "description": "L'IA est au service de l'humain, pas l'inverse", "alfred_application": "ALFRED augmente les capacités de l'utilisateur, protège son autonomie et ne crée pas de dépendance"}
    ],
    "red_lines": [
      "Ne jamais se présenter comme humain à un utilisateur qui demande sincèrement",
      "Ne jamais générer de contenu illégal, discriminatoire ou manipulatoire",
      "Ne jamais collecter ou inférer des données sensibles sans consentement",
      "Ne jamais prendre de décision autonome à fort impact (médical, juridique, financier) sans validation humaine",
      "Ne jamais contourner un refus utilisateur par une reformulation détournée"
    ],
    "regulatory_context": {
      "EU_AI_Act": "Classifie les systèmes IA selon leur niveau de risque. Les assistants personnels sont en risque limité mais doivent respecter la transparence.",
      "RGPD": "S'applique à toute IA traitant des données personnelles — consentement, minimisation, droit à l'oubli.",
      "ISO_42001": "Norme de management des systèmes IA — gouvernance, traçabilité, évaluation continue."
    }
  },
  "example_answers": [
    {"prompt": "Est-ce qu'ALFRED respecte les règles éthiques de l'IA ?", "answer": "Oui, par design. ALFRED est transparent sur ses limites, stocke les données localement, ne se présente jamais comme humain, et laisse toujours la décision finale à l'utilisateur. L'objectif est d'augmenter ton autonomie, pas d'y substituer. Si tu veux vérifier un point spécifique (données, sécurité, comportement), demande-moi."},
    {"prompt": "Comment s'assurer qu'un système IA ne discrimine pas ?", "answer": "Trois niveaux : données d'entraînement (représentatives et sans biais historiques), évaluation régulière des sorties sur des cas tests diversifiés, et mécanismes de feedback utilisateur pour signaler les réponses problématiques. Pour ALFRED, les réponses sont générées par des modèles de base — la vigilance reste nécessaire sur les biais des LLM utilisés."},
    {"prompt": "Que faire si ALFRED donne une réponse éthiquement problématique ?", "answer": "Le signaler immédiatement — une réponse qui te choque ou qui te semble biaisée doit être remontée. L'IA n'est pas parfaite. Ton feedback est le mécanisme de correction le plus efficace à court terme. À plus long terme, les garde-fous système (filtres, règles de comportement) s'améliorent en continu."}
  ],
  "response_guidance": {
    "tone": "clair, rigoureux, sans condescendance éthique",
    "structure": ["identifier le principe éthique en jeu", "expliquer son application concrète dans ALFRED", "reconnaître les limites actuelles", "proposer une action ou une vérification"],
    "avoid": ["être moralisateur", "promettre une IA 'parfaitement éthique'", "ignorer les tensions entre principes (transparence vs vie privée)"]
  },
  "tags": ["éthique IA", "AI Act", "RGPD", "transparence", "autonomie", "gouvernance", "cpl"],
  "related_knowledge_units": ["knowledges.professional.governance_ai.ai_ethics_operationalization", "knowledges.professional.standards_iso.iso_42001_ai_management_system", "knowledges.system.ethics.ethical_framework"]
})

save("cpl/ethics_governance/governance_model.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.ethics_governance.governance_model",
  "title": "Modèle de gouvernance organisationnelle",
  "domain": "cpl", "subdomain": "ethics_governance",
  "status": "validated",
  "summary": "La gouvernance définit qui décide quoi, selon quelles règles et avec quelle responsabilité. Un modèle de gouvernance clair évite les conflits de compétences, accélère les décisions et protège la conformité.",
  "core_definition": "Le modèle de gouvernance est le système formel ou semi-formel qui définit les structures de décision, les rôles et responsabilités, les règles d'escalade et les mécanismes de contrôle au sein d'une organisation ou d'un projet.",
  "knowledge": {
    "governance_elements": [
      {"element": "Instances de décision", "description": "Comités, boards, tribu produit — qui décide quoi, à quelle fréquence"},
      {"element": "RACI", "description": "Responsible, Accountable, Consulted, Informed — clarifier qui fait, qui valide, qui est consulté"},
      {"element": "Règles d'escalade", "description": "À quel niveau une décision doit-elle remonter ? Quel délai d'escalade ?"},
      {"element": "Audit et contrôle", "description": "Comment vérifie-t-on la conformité des décisions aux règles définies ?"},
      {"element": "Amendement", "description": "Comment les règles de gouvernance peuvent-elles être modifiées ?"}
    ],
    "governance_models": [
      {"model": "Centralisé", "description": "Décisions concentrées en haut. Rapide pour les décisions stratégiques, lent pour les opérations.", "best_for": "Organisations jeunes, situations de crise"},
      {"model": "Décentralisé", "description": "Décisions déléguées aux équipes opérationnelles. Rapide, mais risque de fragmentation.", "best_for": "Organisations matures avec une culture forte"},
      {"model": "Matriciel", "description": "Doubles lignes hiérarchiques (fonctionnel + projet). Flexible, mais ambiguïté sur la responsabilité.", "best_for": "Grandes organisations avec projets transversaux"},
      {"model": "Holacratique", "description": "Auto-organisation par cercles et rôles. Pas de hiérarchie formelle.", "best_for": "Équipes très autonomes, culture de confiance élevée"}
    ],
    "governance_for_ai": [
      "Définir un owner de chaque système IA (responsabilité claire)",
      "Établir des règles de validation avant déploiement (tests, audit éthique)",
      "Créer un processus de signalement des comportements inattendus",
      "Réviser régulièrement les règles comportementales des systèmes en production",
      "Tracer les décisions importantes prises avec assistance IA"
    ]
  },
  "example_answers": [
    {"prompt": "Comment structurer la gouvernance d'un projet IA en entreprise ?", "answer": "Quatre éléments essentiels : un owner identifié (accountability claire), une instance de validation avant déploiement (comité tech + éthique), des règles comportementales documentées (ce que le système peut/ne peut pas faire), et un processus de signalement des problèmes. Simple et opérationnel dès le premier trimestre."},
    {"prompt": "Notre équipe n'arrive pas à décider — problème de gouvernance ou de personnes ?", "answer": "Souvent les deux, mais le plus souvent c'est un problème de gouvernance masqué par un problème de personnes. Questions clés : qui est accountable (pas responsible) de la décision ? Y a-t-il un RACI formalisé ? Les règles d'escalade sont-elles claires ? Souvent, clarifier le RACI suffit à débloquer les décisions."},
    {"prompt": "Qu'est-ce qu'un bon RACI ?", "answer": "Un bon RACI a un seul Accountable par décision (pas deux), des Responsibles clairement identifiés, peu de Consulted (max 3-4 sinon c'est une réunion déguisée), et des Informed bien ciblés. Trop de monde dans la colonne A ou R = décision paralysée. Le RACI n'est pas un outil de politesse — c'est un outil de clarté."}
  ],
  "response_guidance": {
    "tone": "structuré, orienté clarté et efficacité",
    "structure": ["identifier le problème de gouvernance sous-jacent", "proposer le bon outil (RACI, instance, règle d'escalade)", "calibrer selon la taille et la maturité de l'organisation"],
    "avoid": ["proposer une gouvernance trop lourde pour une petite structure", "ignorer la culture organisationnelle existante", "confondre gouvernance et bureaucratie"]
  },
  "tags": ["gouvernance", "RACI", "décision", "organisation", "responsabilité", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.ethics_governance.ethical_ai_framework", "knowledges.cpl.execution.decision_making_framework", "knowledges.professional.governance_ai.ai_governance_basics"]
})

save("cpl/ethics_governance/accessibility_principles.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.ethics_governance.accessibility_principles",
  "title": "Principes d'accessibilité (produit et communication)",
  "domain": "cpl", "subdomain": "ethics_governance",
  "status": "validated",
  "summary": "L'accessibilité consiste à concevoir des produits et communications utilisables par tous, quelles que soient les capacités cognitives, physiques ou technologiques. C'est à la fois une obligation légale, une valeur éthique et un avantage business.",
  "core_definition": "L'accessibilité (a11y) est la conception de produits, services et communications de sorte qu'ils puissent être utilisés par des personnes présentant un handicap (visuel, moteur, cognitif, auditif) et plus largement par tout utilisateur dans des conditions dégradées (mauvais réseau, stress, mobile, age avancé).",
  "knowledge": {
    "wcag_principles": [
      {"principle": "Perceptible", "meaning": "L'information doit être présentée de façon que tous puissent la percevoir (alternatives textuelles aux images, sous-titres vidéo, contraste suffisant)"},
      {"principle": "Utilisable", "meaning": "L'interface doit être navigable sans souris (clavier, lecteur d'écran), sans délai arbitraire, sans contenu épileptogène"},
      {"principle": "Compréhensible", "meaning": "Le texte doit être lisible, le comportement prévisible, les erreurs clairement expliquées"},
      {"principle": "Robuste", "meaning": "Le contenu doit fonctionner avec les technologies actuelles et futures (navigateurs, assistants vocaux)"}
    ],
    "cognitive_accessibility": [
      "Langage simple (phrases courtes, vocabulaire commun, pas de jargon non expliqué)",
      "Structure visuelle claire (titres, listes, espacement)",
      "Charge cognitive réduite (pas plus de 7±2 éléments par groupement)",
      "Feedback immédiat sur les actions (confirmation, erreur, chargement)",
      "Pas d'urgence artificielle qui stresse l'utilisateur"
    ],
    "ai_accessibility": [
      "Réponses en langage naturel adapté au niveau de l'utilisateur",
      "Possibilité de demander une reformulation plus simple",
      "Ne jamais supposer un niveau d'expertise non confirmé",
      "Support vocal ET textuel pour les interactions",
      "Éviter les longs blocs de texte — structurer avec des listes ou des étapes"
    ],
    "business_case": [
      "15% de la population mondiale vit avec un handicap (OMS)",
      "Les améliorations d'accessibilité bénéficient à 100% des utilisateurs (sous-titres, langage clair, contraste)",
      "Obligation légale en UE (European Accessibility Act 2025 pour les produits numériques)",
      "Améliore le SEO et la compatibilité mobile"
    ]
  },
  "example_answers": [
    {"prompt": "Comment rendre ALFRED plus accessible ?", "answer": "Trois axes : langage (réponses simples, possibilité de simplifier à la demande), structure (listes plutôt que longs paragraphes, titres clairs), et modes d'interaction (vocal + texte, réponse adaptée au contexte mobile vs desktop). L'accessibilité cognitive profite à tout le monde, pas seulement aux personnes en situation de handicap."},
    {"prompt": "Quels sont les critères WCAG les plus importants à respecter en priorité ?", "answer": "Niveau AA minimum : contraste texte/fond ≥ 4.5:1, navigation clavier complète, alternatives textuelles aux images informatives, pas de contenu uniquement par la couleur. Pour une IA : clarté du langage et structure de réponse sont les critères d'accessibilité cognitive les plus impactants."},
    {"prompt": "Accessibilité et design, est-ce compatible ?", "answer": "Oui. Les contraintes d'accessibilité améliorent souvent le design pour tout le monde. Un contraste élevé est plus lisible en plein soleil. Un langage simple est compris plus vite. Une navigation au clavier est précieuse pour les power users. L'accessibilité n'est pas une contrainte sur le design — c'est une contrainte de qualité."}
  ],
  "response_guidance": {
    "tone": "pédagogique, positif, sans culpabiliser",
    "structure": ["identifier l'axe d'accessibilité concerné", "citer le critère ou le principe applicable", "proposer une amélioration concrète", "rappeler le bénéfice universel"],
    "avoid": ["traiter l'accessibilité comme un coût supplémentaire", "négliger l'accessibilité cognitive au profit de l'accessibilité technique", "promettre la conformité totale sans audit"]
  },
  "tags": ["accessibilité", "WCAG", "a11y", "inclusion", "design universel", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.ethics_governance.ethical_ai_framework", "knowledges.cpl.product_ia.product_design_methodology", "knowledges.professional.frameworks.rgpd_gdpr_basics"]
})

print("\nBatch CPL Product IA + Human Comm + Ethics : DONE (10 fichiers)")
