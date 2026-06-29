"""
Enrichissement Knowledge Base ALFRED - Batch 1 : CPL (20 fichiers)
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
# CPL / STRATEGY
# =============================================================================

save("cpl/strategy/strategy_fundamentals.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.strategy.strategy_fundamentals",
  "title": "Fondamentaux de la stratégie",
  "domain": "cpl", "subdomain": "strategy",
  "status": "validated",
  "summary": "Cadrer une stratégie revient à arbitrer : choisir une cible, une valeur différenciante, et renoncer au reste. Vision, mission et positionnement sont les trois piliers structurants.",
  "core_definition": "La stratégie est l'art d'allouer des ressources limitées vers les actions qui créent le plus de valeur pour une cible précise. Elle implique des renoncements explicites et un cap stable dans le temps.",
  "knowledge": {
    "pillars": [
      {"name": "Vision", "definition": "Projection claire de l'état futur souhaité — la raison d'être à long terme.", "question": "Où veut-on aller dans 3 à 5 ans ?"},
      {"name": "Mission", "definition": "Rôle concret et opérationnel du projet ou de l'organisation.", "question": "Pourquoi existons-nous ? Que faisons-nous concrètement ?"},
      {"name": "Positionnement", "definition": "Place distinctive occupée face aux alternatives disponibles pour la cible.", "question": "Pourquoi nous et pas autre chose ?"}
    ],
    "strategic_principles": [
      "Une stratégie sans arbitrage n'est pas une stratégie — c'est une liste de souhaits.",
      "Relier chaque décision à une cible, un besoin réel et une valeur créée.",
      "Prioriser viabilité économique et valeur utilisateur en premier.",
      "Éviter la dispersion : faire moins mais mieux.",
      "Tester les hypothèses stratégiques le plus tôt possible."
    ],
    "decision_framework": [
      "Quel problème concret résout-on ?",
      "Pour quelle cible précise ?",
      "Quelle valeur différenciante crée-t-on ?",
      "Quel impact business attendu ?",
      "Quel niveau d'effort, de risque et de délai ?"
    ],
    "common_mistakes": [
      "Stratégie trop large — vouloir servir tout le monde",
      "Absence d'arbitrage explicite entre options",
      "Confusion entre vision et plan opérationnel",
      "Positionnement non testé auprès de la cible réelle",
      "Ignorer les contraintes de ressources dès le cadrage"
    ]
  },
  "example_answers": [
    {"prompt": "Mon projet part dans tous les sens, comment le recadrer ?", "answer": "On revient aux fondamentaux : quel problème précis tu règles, pour quelle cible, avec quelle valeur différenciante ? Dès qu'on clarifie ces trois points, les priorités émergent — et ce qu'il faut abandonner aussi."},
    {"prompt": "Quelle différence entre vision et stratégie ?", "answer": "La vision dit où tu veux aller. La stratégie dit comment y arriver avec les ressources disponibles, en choisissant quoi faire et quoi ne pas faire. Sans arbitrage, c'est une intention, pas une stratégie."},
    {"prompt": "Comment valider une stratégie avant de lancer ?", "answer": "Teste les hypothèses clés : la cible existe-t-elle ? Le problème est-il douloureux ? L'offre est-elle différente ? Cinq entretiens clients valent mieux que trois mois de planification."}
  ],
  "response_guidance": {
    "tone": "structuré, direct, orienté décision",
    "structure": ["rappel de la question de fond", "les 3 piliers (vision/mission/positionnement)", "le point d'arbitrage clé", "prochaine action concrète"],
    "avoid": ["théoriser sans ancrer dans le contexte", "donner une liste sans hiérarchie", "confondre stratégie et plan opérationnel"]
  },
  "tags": ["stratégie", "vision", "mission", "positionnement", "arbitrage", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.strategy.business_model_design", "knowledges.cpl.strategy.value_proposition_framework", "knowledges.professional.decision.prioritization"]
})

save("cpl/strategy/business_model_design.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.strategy.business_model_design",
  "title": "Design du modèle business",
  "domain": "cpl", "subdomain": "strategy",
  "status": "validated",
  "summary": "Un modèle business décrit comment une organisation crée, délivre et capture de la valeur. Le Business Model Canvas (BMC) est l'outil de référence pour le cadrer en 9 blocs.",
  "core_definition": "Le modèle business est la logique par laquelle une organisation génère de la valeur pour ses clients et la transforme en revenus durables. Il articule la proposition de valeur, les segments clients, les canaux, les ressources clés, les flux de revenus et la structure de coûts.",
  "knowledge": {
    "bmc_blocks": [
      {"block": "Segments clients", "question": "Pour qui créons-nous de la valeur ?"},
      {"block": "Proposition de valeur", "question": "Quel problème résolvons-nous ? Quel besoin satisfaisons-nous ?"},
      {"block": "Canaux", "question": "Comment atteignons-nous nos clients ?"},
      {"block": "Relations clients", "question": "Quel type de relation établissons-nous ?"},
      {"block": "Flux de revenus", "question": "Comment monétisons-nous la valeur créée ?"},
      {"block": "Ressources clés", "question": "Quels actifs sont indispensables ?"},
      {"block": "Activités clés", "question": "Quelles actions sont critiques ?"},
      {"block": "Partenaires clés", "question": "Qui nous aide à réussir ?"},
      {"block": "Structure de coûts", "question": "Quels sont les coûts les plus importants ?"}
    ],
    "common_models": [
      {"name": "SaaS / Abonnement", "logic": "Revenus récurrents, coût d'acquisition amorti dans le temps"},
      {"name": "Freemium", "logic": "Acquisition large gratuite, conversion sur fonctions premium"},
      {"name": "Marketplace", "logic": "Commission sur transactions entre offreurs et demandeurs"},
      {"name": "Conseil / Services", "logic": "Valeur dans l'expertise humaine, facturation au temps ou au livrable"},
      {"name": "Produit + Services", "logic": "Produit core + accompagnement, maintenance ou formation en upsell"}
    ],
    "viability_tests": [
      "Les clients paient-ils vraiment pour ce qu'on propose ?",
      "Le coût d'acquisition client (CAC) est-il inférieur à la valeur vie client (LTV) ?",
      "Le modèle est-il scalable ou dépendant de ressources rares ?",
      "Les flux de revenus sont-ils diversifiés ou concentrés sur un seul client ?"
    ]
  },
  "example_answers": [
    {"prompt": "Comment choisir entre freemium et abonnement payant ?", "answer": "Freemium si tu as besoin d'une base d'utilisateurs large pour créer de l'effet réseau ou valider l'usage. Abonnement payant dès le début si tu cibles des professionnels avec un problème précis et douloureux. L'erreur classique : offrir trop gratuitement et ne jamais convertir."},
    {"prompt": "On a une idée produit, comment modéliser le business ?", "answer": "On commence par les deux blocs centraux du BMC : la proposition de valeur et le segment client. Tout le reste découle de là — les canaux pour les atteindre, les revenus pour monétiser, les ressources pour délivrer. En 45 minutes, on peut avoir un BMC de travail suffisant pour aller tester."},
    {"prompt": "Qu'est-ce qu'un bon modèle business pour une IA ?", "answer": "Pour une IA : préférer un modèle à revenus récurrents (abonnement) car les coûts d'inférence sont continus. Le freemium fonctionne si le produit crée une habitude rapide. Éviter la facturation à l'usage si les coûts sont imprévisibles côté infrastructure."}
  ],
  "response_guidance": {
    "tone": "pragmatique, orienté action, concret",
    "structure": ["identifier le bloc BMC concerné", "décrire la logique value/revenue", "pointer le risque principal", "suggestion de test immédiat"],
    "avoid": ["lister les 9 blocs BMC sans les relier à la situation", "être trop théorique", "ignorer la question de la viabilité économique"]
  },
  "tags": ["business model", "BMC", "monetisation", "revenus", "stratégie", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.strategy.strategy_fundamentals", "knowledges.cpl.strategy.value_proposition_framework", "knowledges.cpl.business_piloting.pricing_strategy"]
})

save("cpl/strategy/value_proposition_framework.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.strategy.value_proposition_framework",
  "title": "Cadre de proposition de valeur",
  "domain": "cpl", "subdomain": "strategy",
  "status": "validated",
  "summary": "La proposition de valeur est la promesse centrale faite à une cible précise : quel problème on résout, pour qui, et pourquoi mieux que l'alternative. Elle doit être spécifique, testable et mémorable.",
  "core_definition": "La proposition de valeur (Value Proposition) décrit le bénéfice concret qu'un produit ou service apporte à un segment client précis, en résolvant une douleur réelle ou en créant un gain significatif, d'une manière que les alternatives ne font pas aussi bien.",
  "knowledge": {
    "value_proposition_canvas": {
      "customer_profile": {
        "jobs": "Ce que le client essaie d'accomplir (tâche, objectif, besoin)",
        "pains": "Ce qui le frustre, le bloque ou lui coûte cher",
        "gains": "Ce qu'il espère obtenir, ce qui le ferait sourire"
      },
      "value_map": {
        "products_services": "Ce qu'on offre concrètement",
        "pain_relievers": "Comment on réduit ses douleurs",
        "gain_creators": "Comment on crée les gains attendus"
      }
    },
    "strong_value_proposition": [
      "Répond à un job-to-be-done précis (pas un besoin générique)",
      "Mentionne un bénéfice mesurable ou tangible",
      "Se distingue de l'alternative explicitement",
      "Est compréhensible en une phrase par la cible elle-même",
      "Est validée par des clients, pas seulement par l'équipe"
    ],
    "formule_template": "Pour [qui], qui [problème / situation], [produit] est [catégorie] qui [bénéfice principal]. Contrairement à [alternative], notre solution [différenciateur clé].",
    "pitfalls": [
      "Proposition trop générique ('on simplifie votre vie')",
      "Focalisée sur les features plutôt que sur le bénéfice",
      "Non testée auprès de la cible réelle",
      "Trop longue pour être mémorisée",
      "Confondre proposition de valeur et slogan marketing"
    ]
  },
  "example_answers": [
    {"prompt": "Comment formuler notre proposition de valeur pour ALFRED ?", "answer": "Pour les professionnels en surcharge cognitive, ALFRED est un assistant IA local qui structure, priorise et mémorise sans effort. Contrairement aux chatbots génériques, il s'adapte au profil de l'utilisateur, fonctionne hors-ligne et protège les données. En une phrase : ton assistant qui pense avec toi, pas à ta place."},
    {"prompt": "Comment tester si ma proposition de valeur est bonne ?", "answer": "Montre-la à 5 personnes de ta cible sans l'expliquer. Si elles comprennent qui c'est, ce que ça fait et pourquoi c'est différent — c'est bon. Si elles hésitent ou te posent des questions, reformule. Le test des 5 secondes suffit souvent."},
    {"prompt": "Quelle différence entre proposition de valeur et positionnement ?", "answer": "La proposition de valeur dit ce qu'on apporte au client. Le positionnement dit où on se place dans l'esprit du marché face aux concurrents. La valeur est axée sur le bénéfice client ; le positionnement est axé sur la différenciation relative."}
  ],
  "response_guidance": {
    "tone": "précis, centré client, orienté validation",
    "structure": ["le job-to-be-done de la cible", "la douleur / le gain clé", "la proposition formulée", "comment la tester"],
    "avoid": ["rester dans l'abstrait", "formuler une proposition sans mentionner la cible", "confondre features et bénéfices"]
  },
  "tags": ["proposition de valeur", "value proposition", "VPC", "job-to-be-done", "différenciation", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.strategy.strategy_fundamentals", "knowledges.cpl.strategy.business_model_design", "knowledges.professional.product_management.product_core"]
})

# =============================================================================
# CPL / EXECUTION
# =============================================================================

save("cpl/execution/project_management_core.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.execution.project_management_core",
  "title": "Gestion de projet — fondamentaux",
  "domain": "cpl", "subdomain": "execution",
  "status": "validated",
  "summary": "Un projet bien géré aligne scope, délais, ressources et qualité autour d'un objectif clair. Les fondamentaux : cadrage initial, jalons, suivi d'avancement, gestion des blocages et communication.",
  "core_definition": "La gestion de projet est l'ensemble des pratiques permettant d'atteindre un objectif défini dans un périmètre, un délai et avec des ressources contraints. Elle couvre le cadrage, la planification, l'exécution, le suivi et la clôture.",
  "knowledge": {
    "project_triangle": {
      "description": "Le triangle coût-délai-qualité : on ne peut optimiser que deux des trois dimensions simultanément.",
      "levers": ["Scope (périmètre fonctionnel)", "Time (délais et jalons)", "Cost/Resources (budget, équipe)", "Quality (niveau d'exigence)"]
    },
    "project_phases": [
      {"phase": "Cadrage", "outputs": ["objectif SMART", "parties prenantes", "contraintes", "critères de succès"]},
      {"phase": "Planification", "outputs": ["WBS (décomposition des tâches)", "jalons", "dépendances", "plan de risques"]},
      {"phase": "Exécution", "outputs": ["suivi d'avancement", "gestion des blocages", "communication équipe"]},
      {"phase": "Clôture", "outputs": ["livrable validé", "retex", "capitalisation", "communication finale"]}
    ],
    "essential_practices": [
      "Fixer un objectif SMART dès le départ (Spécifique, Mesurable, Atteignable, Réaliste, Temporellement défini)",
      "Identifier les parties prenantes et leurs attentes avant de planifier",
      "Prioriser les tâches à fort impact sur le chemin critique",
      "Prévoir une marge de sécurité (buffer) sur les estimations",
      "Communiquer l'avancement régulièrement sans attendre que quelqu'un demande",
      "Escalader les blocages tôt plutôt que de les absorber silencieusement"
    ],
    "common_failures": [
      "Scope creep : périmètre qui s'élargit sans décision formelle",
      "Dépendances non identifiées qui bloquent l'exécution",
      "Sous-estimation systématique des délais (biais d'optimisme)",
      "Communication insuffisante avec les parties prenantes",
      "Absence de retex à la clôture — mêmes erreurs reproduites"
    ]
  },
  "example_answers": [
    {"prompt": "Comment cadrer rapidement un projet ?", "answer": "En une heure, on clarifie : quel est l'objectif précis ? Qui sont les parties prenantes et qu'attendent-elles ? Quelles sont les contraintes non négociables (délai, budget, tech) ? Et quels sont les critères de succès mesurables ? Avec ça, on peut planifier sans naviguer à l'aveugle."},
    {"prompt": "Le projet prend du retard, que faire ?", "answer": "D'abord diagnostiquer : c'est un problème de scope, de ressources, de dépendance bloquante ou d'estimation ? Ensuite, trois options : réduire le scope, ajouter des ressources, ou repousser le jalon. Choisir explicitement et communiquer vite aux parties prenantes — l'attente silencieuse aggrave toujours la situation."},
    {"prompt": "Comment éviter le scope creep ?", "answer": "Formaliser le périmètre dès le cadrage (liste de ce qui est IN et de ce qui est OUT). Toute demande d'ajout passe par une décision explicite : soit on la priorise et on réévalue le délai, soit on la reporte en backlog. Dire non sans justification claire génère du conflit — dire non avec un 'pas maintenant, et voilà quand' est accepté."}
  ],
  "response_guidance": {
    "tone": "structuré, pragmatique, orienté résolution",
    "structure": ["identifier la phase projet actuelle", "pointer le problème concret", "proposer une action immédiate", "anticiper le risque suivant"],
    "avoid": ["donner un cours théorique sur PRINCE2 ou PMBoK", "ignorer les contraintes réelles", "proposer une solution qui nécessite plus de ressources qu'il n'en existe"]
  },
  "tags": ["projet", "gestion de projet", "planification", "scope", "jalons", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.execution.task_prioritization", "knowledges.cpl.execution.risk_management", "knowledges.professional.frameworks.agile_scrum_basics"]
})

save("cpl/execution/task_prioritization.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.execution.task_prioritization",
  "title": "Priorisation des tâches",
  "domain": "cpl", "subdomain": "execution",
  "status": "validated",
  "summary": "Prioriser consiste à choisir quoi faire en premier quand tout semble urgent. Les méthodes ICE, MoSCoW et la matrice Impact/Effort permettent de structurer ces arbitrages rapidement.",
  "core_definition": "La priorisation est le processus de classement des tâches, fonctionnalités ou initiatives selon leur importance relative, leur impact attendu et les contraintes disponibles (temps, énergie, ressources). Elle transforme une liste de todo en un plan d'action cohérent.",
  "knowledge": {
    "frameworks": [
      {
        "name": "Matrice Impact / Effort",
        "logic": "Classer chaque tâche selon son impact business et son niveau d'effort. Faire en premier les Quick Wins (fort impact, faible effort).",
        "quadrants": ["Quick Wins → faire maintenant", "Grands projets → planifier", "Fill-ins → faire si temps", "Thankless tasks → éviter ou déléguer"]
      },
      {
        "name": "ICE Score",
        "logic": "Score = Impact × Confidence × Ease (1-10 chacun). Classer par score décroissant.",
        "use_when": "Prioriser des features ou expériences en phase early-stage produit"
      },
      {
        "name": "MoSCoW",
        "logic": "Must have / Should have / Could have / Won't have. Utile pour un backlog ou une release.",
        "use_when": "Cadrer le scope d'une version ou d'un sprint"
      },
      {
        "name": "Méthode ABCDE",
        "logic": "A = must do today (conséquences si pas fait), B = should do, C = nice to do, D = déléguer, E = éliminer.",
        "use_when": "Priorisation personnelle quotidienne"
      }
    ],
    "key_principles": [
      "Une tâche non priorisée n'existe pas — elle sera faite aléatoirement ou jamais.",
      "L'urgence perçue et l'importance réelle ne coïncident presque jamais.",
      "Prioriser c'est aussi décider explicitement ce qu'on ne fait pas.",
      "Revoir la priorisation dès qu'un contexte change (blocage, nouvelle info, feedback client).",
      "Le consensus de priorisation est souvent une erreur : quelqu'un doit trancher."
    ],
    "anti_patterns": [
      "Tout mettre en priorité 1 — annule l'utilité de la priorisation",
      "Prioriser sans données — décision au feeling uniquement",
      "Refuser de déprioritiser une tâche déjà lancée (biais du coût irrécupérable)",
      "Confondre ce que le client demande et ce dont il a besoin"
    ]
  },
  "example_answers": [
    {"prompt": "J'ai 20 tâches et je ne sais pas par où commencer.", "answer": "On applique la matrice Impact/Effort : pour chaque tâche, deux questions — combien ça vaut si c'est fait ? et combien ça coûte à faire ? Les Quick Wins (fort impact, faible effort) passent en premier. On trouve généralement 3 à 5 tâches qui méritent vraiment d'être faites aujourd'hui."},
    {"prompt": "Comment prioriser les fonctionnalités d'un produit ?", "answer": "ICE score ou MoSCoW selon le stade. En early stage, ICE (Impact × Confidence × Ease) permet de scorer rapidement et de comparer. En préparation de release, MoSCoW clarifie ce qui est bloquant vs ce qui est nice-to-have. Dans tous les cas : inclure la voix des utilisateurs réels dans l'évaluation de l'impact."},
    {"prompt": "Mon équipe dit que tout est urgent.", "answer": "Quand tout est urgent, rien ne l'est. On pose la question autrement : si on ne peut faire qu'une seule chose cette semaine, laquelle a le plus d'impact ? Puis une deuxième. La contrainte artificielle force l'arbitrage que le confort de 'tout' empêche."}
  ],
  "response_guidance": {
    "tone": "clair, orienté décision, sans jugement sur les choix passés",
    "structure": ["comprendre le contexte (nombre de tâches, type)", "proposer le bon framework", "guider l'application", "valider la décision finale"],
    "avoid": ["proposer tous les frameworks sans recommander", "ne pas prendre en compte les contraintes réelles (énergie, deadline)", "forcer une méthode inadaptée au contexte"]
  },
  "tags": ["priorisation", "ICE", "MoSCoW", "backlog", "gestion du temps", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.execution.project_management_core", "knowledges.professional.decision.prioritization", "knowledges.human.cognition.decision_fatigue"]
})

save("cpl/execution/risk_management.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.execution.risk_management",
  "title": "Gestion des risques",
  "domain": "cpl", "subdomain": "execution",
  "status": "validated",
  "summary": "Un risque est un événement incertain qui pourrait affecter les objectifs. La gestion des risques consiste à les identifier, évaluer (probabilité × impact), prioriser et définir une réponse adaptée avant qu'ils se matérialisent.",
  "core_definition": "La gestion des risques (Risk Management) est le processus structuré d'identification, d'évaluation et de traitement des menaces potentielles sur un projet ou une organisation, afin de réduire les surprises et préserver la capacité à atteindre les objectifs.",
  "knowledge": {
    "risk_process": [
      {"step": "1. Identification", "action": "Lister tous les risques plausibles (risques techniques, humains, externes, financiers, calendaires)"},
      {"step": "2. Évaluation", "action": "Scorer chaque risque : Probabilité (1-5) × Impact (1-5) = Score de criticité"},
      {"step": "3. Priorisation", "action": "Traiter en priorité les risques à score élevé (≥ 12/25)"},
      {"step": "4. Réponse", "action": "Choisir une stratégie de réponse pour chaque risque critique"},
      {"step": "5. Suivi", "action": "Réévaluer régulièrement — un risque peut changer de probabilité ou d'impact en cours de projet"}
    ],
    "response_strategies": [
      {"strategy": "Évitement", "logic": "Modifier le plan pour éliminer le risque (changer de technologie, de délai, de périmètre)"},
      {"strategy": "Réduction", "logic": "Réduire la probabilité ou l'impact (prototyper plus tôt, ajouter un test, former l'équipe)"},
      {"strategy": "Transfert", "logic": "Transférer le risque à un tiers (assurance, clause contractuelle, partenaire)"},
      {"strategy": "Acceptation", "logic": "Accepter le risque en connaissance de cause, avec un plan de contingence si nécessaire"}
    ],
    "risk_categories": [
      "Risques techniques (technologie non maîtrisée, dette technique)",
      "Risques ressources (absence clé, charge sous-estimée)",
      "Risques calendaires (dépendance externe, contrainte réglementaire)",
      "Risques business (marché qui change, client qui annule)",
      "Risques data/sécurité (fuite, corruption, RGPD)"
    ],
    "early_warning_signs": [
      "Tâches critiques qui glissent sans escalade",
      "Dépendances non confirmées dans le plan",
      "Feedback client absent depuis trop longtemps",
      "Estimations systématiquement dépassées de >30%",
      "Membre clé de l'équipe surchargé sans remplaçant"
    ]
  },
  "example_answers": [
    {"prompt": "Comment identifier les risques d'un projet rapidement ?", "answer": "Un brainstorming de 30 minutes avec l'équipe suffit souvent. On part des catégories : technique, ressources, calendaire, business, données. Pour chaque catégorie, la question est : qu'est-ce qui pourrait mal tourner et qui nous surprendrait ? On liste sans filtrer, on évalue ensuite."},
    {"prompt": "On a un risque technique fort sur une dépendance externe, que faire ?", "answer": "Stratégie de réduction : prototyper l'intégration dès maintenant plutôt qu'en fin de projet. Si la dépendance est bloquante, anticiper une alternative (plan B). Escalader à la direction si le risque est hors de contrôle de l'équipe — garder ça silencieux est la pire option."},
    {"prompt": "Quelle différence entre risque et problème ?", "answer": "Un risque est potentiel — il peut arriver ou non. Un problème est réel — il s'est déjà matérialisé. On gère les risques en amont (prévention / préparation) et les problèmes en temps réel (correction / contingence). L'erreur classique : ne gérer que les problèmes et ignorer les risques jusqu'à ce qu'ils deviennent des problèmes."}
  ],
  "response_guidance": {
    "tone": "structuré, anticipatif, sans alarmisme",
    "structure": ["identifier la catégorie de risque", "évaluer probabilité et impact", "proposer la stratégie de réponse adaptée", "définir le déclencheur de suivi"],
    "avoid": ["paniquer ou minimiser", "proposer une réponse sans l'adapter au contexte", "ignorer les risques faible probabilité mais fort impact (black swans)"]
  },
  "tags": ["risques", "risk management", "probabilité", "impact", "mitigation", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.execution.project_management_core", "knowledges.professional.decision.tradeoff_analysis", "knowledges.professional.standards_iso.iso_31000_risk_management"]
})

save("cpl/execution/decision_making_framework.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.execution.decision_making_framework",
  "title": "Cadres de prise de décision",
  "domain": "cpl", "subdomain": "execution",
  "status": "validated",
  "summary": "Décider efficacement exige de clarifier le type de décision, les critères qui comptent et qui doit trancher. Les cadres structurent le raisonnement et réduisent les biais cognitifs qui dégradent la qualité des choix.",
  "core_definition": "Un cadre de décision est un processus structuré pour choisir entre plusieurs options en minimisant les biais cognitifs et en maximisant la qualité du raisonnement. Il s'adapte à la réversibilité, l'urgence et le niveau de certitude de la situation.",
  "knowledge": {
    "decision_types": [
      {"type": "Décision réversible à faible impact", "approach": "Décider vite, tester, ajuster. Pas besoin de consensus."},
      {"type": "Décision réversible à fort impact", "approach": "Valider les hypothèses clés avant de décider. Impliquer les parties prenantes."},
      {"type": "Décision irréversible à faible impact", "approach": "Décider avec méthode simple. Prendre en compte les conséquences à long terme."},
      {"type": "Décision irréversible à fort impact", "approach": "Processus rigoureux : options, critères, scénarios, validation externe si possible."}
    ],
    "frameworks": [
      {
        "name": "WRAP (Heath & Heath)",
        "steps": ["Widen your options — explorer au-delà des deux options apparentes", "Reality-test your assumptions — tester les hypothèses clés", "Attain distance — prendre du recul émotionnel", "Prepare to be wrong — prévoir un plan B"]
      },
      {
        "name": "Analyse coûts/bénéfices",
        "steps": ["Lister les options", "Définir les critères de valeur", "Peser chaque option sur chaque critère", "Choisir l'option avec le meilleur équilibre global"]
      },
      {
        "name": "Pré-mortem",
        "steps": ["Imaginer que la décision a échoué dans 12 mois", "Identifier pourquoi elle a échoué", "Utiliser ces causes potentielles pour renforcer la décision ou changer de cap"]
      }
    ],
    "decision_biases_to_watch": [
      "Biais de confirmation — chercher des informations qui valident ce qu'on croit déjà",
      "Biais du statu quo — préférer ne rien changer même quand c'est sous-optimal",
      "Biais d'ancrage — être trop influencé par la première information reçue",
      "HIPPO effect — suivre la personne la mieux payée plutôt que les données",
      "Escalade de l'engagement — persévérer dans une mauvaise direction pour justifier les coûts passés"
    ],
    "decision_criteria": [
      "Impact attendu sur l'objectif principal",
      "Réversibilité — peut-on corriger si c'est une erreur ?",
      "Délai de feedback — quand saurons-nous si c'est la bonne décision ?",
      "Coût d'opportunité — à quoi renonce-t-on en choisissant cette option ?"
    ]
  },
  "example_answers": [
    {"prompt": "On a du mal à trancher entre deux options, comment décider ?", "answer": "D'abord : est-ce réversible ou non ? Si c'est réversible, décide vite et teste. Si non, structure : quels critères comptent vraiment ? Quelle option performe le mieux sur les critères non-négociables ? Ensuite, le pré-mortem : si dans 6 mois c'est un échec, pourquoi ? Cette question révèle souvent ce qu'on ne voulait pas voir."},
    {"prompt": "Toute l'équipe est d'accord mais j'ai un doute.", "answer": "Le doute individuel face au consensus vaut la peine d'être exprimé. Joue l'avocat du diable : 'Qu'est-ce qu'on n'a pas encore envisagé ?' ou 'Pourquoi est-ce qu'on échouerait malgré tout ?' Ce n'est pas bloquer — c'est améliorer la qualité de la décision collective."},
    {"prompt": "Comment éviter de décider sous pression émotionnelle ?", "answer": "La règle des 10/10/10 (Suzy Welch) : dans 10 minutes, dans 10 mois, dans 10 ans — comment je me sentirai par rapport à cette décision ? L'ancrage temporel coupe l'urgence perçue et remet la décision dans une perspective plus saine."}
  ],
  "response_guidance": {
    "tone": "ancré, raisonné, qui aide à penser sans décider à la place",
    "structure": ["clarifier le type de décision", "identifier les biais actifs", "appliquer le cadre adapté", "proposer un test ou une validation rapide"],
    "avoid": ["décider à la place de l'utilisateur", "minimiser les doutes légitimes", "surcomplexifier avec trop de frameworks simultanément"]
  },
  "tags": ["décision", "WRAP", "pré-mortem", "biais cognitifs", "arbitrage", "cpl"],
  "related_knowledge_units": ["knowledges.professional.decision.decision_making", "knowledges.human.cognition.decision_fatigue", "knowledges.cpl.execution.risk_management"]
})

# =============================================================================
# CPL / BUSINESS PILOTING
# =============================================================================

save("cpl/business_piloting/pricing_strategy.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.business_piloting.pricing_strategy",
  "title": "Stratégie de prix",
  "domain": "cpl", "subdomain": "business_piloting",
  "status": "validated",
  "summary": "Le prix n'est pas un coût plus une marge — c'est un signal de valeur. La stratégie de prix alignée sur la valeur perçue maximise les revenus tout en préservant la relation client.",
  "core_definition": "La stratégie de prix (Pricing Strategy) détermine comment fixer le prix d'un produit ou service en équilibrant la valeur perçue par le client, la position concurrentielle, les coûts et l'objectif business (volume, marge, part de marché).",
  "knowledge": {
    "pricing_models": [
      {"model": "Cost-plus", "logic": "Prix = Coûts + Marge souhaitée", "risk": "Ignore la valeur perçue et le marché"},
      {"model": "Value-based", "logic": "Prix = Valeur perçue par le client", "risk": "Nécessite de bien comprendre le client et ses alternatives"},
      {"model": "Competitive pricing", "logic": "Prix aligné sur les concurrents ±delta", "risk": "Guerre des prix si le marché n'est pas différencié"},
      {"model": "Freemium", "logic": "Gratuit pour l'usage core, payant pour les fonctions avancées", "risk": "Difficulté de conversion, coûts serveurs non couverts"},
      {"model": "Abonnement (SaaS)", "logic": "Revenus récurrents prévisibles, engagement client", "risk": "Churn si la valeur n'est pas régulièrement démontrée"},
      {"model": "Usage-based", "logic": "Facturation à la consommation réelle", "risk": "Revenus imprévisibles, difficile à budgéter côté client"}
    ],
    "pricing_levers": [
      "Prix d'entrée (pour acquérir) vs prix de croissance (upsell / expansion)",
      "Ancrage : présenter un prix élevé en premier pour valoriser le prix cible",
      "Déclinaison par tiers (Good / Better / Best) pour maximiser la capture de valeur",
      "Remises stratégiques vs remises systématiques (qui forment une attente)",
      "Test A/B de prix sur nouveaux marchés avant généralisation"
    ],
    "value_based_questions": [
      "Quel est le coût de l'alternative pour le client ?",
      "Combien de temps / d'argent notre solution lui économise-t-elle ?",
      "Quel est l'impact d'un non-achat sur son activité ?",
      "À quel prix le client perçoit-il l'offre comme 'cheap' et perd confiance ?"
    ]
  },
  "example_answers": [
    {"prompt": "Comment fixer le prix d'un SaaS B2B ?", "answer": "Part de la valeur créée, pas des coûts. Si ton outil économise 5h/semaine à un consultant facturant 100€/h, la valeur mensuelle est ~2000€. Ton prix peut être 200-400€/mois (10-20% de la valeur capturée). Tester avec 3 tiers (Starter / Pro / Business) permet de segmenter la capture selon la maturité du client."},
    {"prompt": "Faut-il baisser le prix pour acquérir plus de clients ?", "answer": "Rarement la bonne réponse. Baisser le prix sans augmenter la valeur perçue dégrade la marque et attire les mauvais clients (price-sensitive, churn élevé). Avant de baisser : tester si le problème est le prix ou la proposition de valeur. Souvent, c'est la valeur qui n'est pas suffisamment démontrée."},
    {"prompt": "Comment gérer les demandes de remise ?", "answer": "Ne jamais donner une remise sans contrepartie. Remise contre volume, contre engagement annuel, contre témoignage client, contre référence. Une remise sans contrepartie forme une attente et dévalue l'offre. La règle : si tu baisses le prix, obtiens quelque chose en échange."}
  ],
  "response_guidance": {
    "tone": "orienté business, pragmatique, sans jugement sur la situation actuelle",
    "structure": ["identifier le modèle de prix actuel ou cible", "évaluer l'alignement valeur/prix", "proposer un ajustement ou un test", "anticiper l'impact sur la marge et la relation client"],
    "avoid": ["simplifier à coûts+marge", "ignorer la concurrence", "recommander une baisse de prix comme première solution"]
  },
  "tags": ["prix", "pricing", "SaaS", "valeur perçue", "marge", "revenus", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.business_piloting.profitability_analysis", "knowledges.cpl.strategy.value_proposition_framework", "knowledges.cpl.strategy.business_model_design"]
})

save("cpl/business_piloting/profitability_analysis.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.business_piloting.profitability_analysis",
  "title": "Analyse de rentabilité",
  "domain": "cpl", "subdomain": "business_piloting",
  "status": "validated",
  "summary": "La rentabilité mesure si une activité génère plus de valeur qu'elle n'en consomme. L'analyse des marges, du point mort et du ROI permet de piloter la profitabilité de chaque produit, client ou service.",
  "core_definition": "L'analyse de rentabilité évalue la capacité d'une activité, d'un produit ou d'un projet à générer un bénéfice net après déduction de tous ses coûts directs et indirects. Elle guide les décisions d'investissement, de prix et de portefeuille.",
  "knowledge": {
    "key_metrics": [
      {"metric": "Marge brute", "formula": "(CA - Coûts variables) / CA × 100", "reads": "Part du CA restant après les coûts directs de production / livraison"},
      {"metric": "EBITDA", "formula": "Résultat avant intérêts, impôts, dépréciations et amortissements", "reads": "Rentabilité opérationnelle pure, avant effets financiers et fiscaux"},
      {"metric": "Point mort (break-even)", "formula": "Coûts fixes / Marge sur coût variable unitaire", "reads": "Volume ou CA à atteindre pour commencer à gagner de l'argent"},
      {"metric": "ROI", "formula": "(Bénéfice net / Investissement) × 100", "reads": "Rendement d'un investissement sur une période donnée"},
      {"metric": "LTV / CAC ratio", "formula": "Valeur vie client / Coût d'acquisition client", "reads": "Santé économique du modèle SaaS/subscription — sain si LTV > 3× CAC"}
    ],
    "profitability_analysis_process": [
      "Identifier les lignes de revenus (par produit, client, segment)",
      "Allouer les coûts directs à chaque ligne de revenus",
      "Calculer la marge brute par ligne",
      "Identifier les coûts indirects à répartir (structure, admin, marketing)",
      "Calculer la marge nette contributive par ligne",
      "Identifier les lignes rentables, les lignes déficitaires, et décider"
    ],
    "decision_triggers": [
      "Marge brute < 30% : analyser les coûts de production / delivery",
      "CAC > LTV/3 : le modèle d'acquisition est non viable — revoir les canaux",
      "Un client représente > 40% du CA : risque de concentration critique",
      "Croissance du CA sans croissance de la marge : scalabilité problématique"
    ]
  },
  "example_answers": [
    {"prompt": "Comment savoir si mon activité est vraiment rentable ?", "answer": "On calcule la marge brute par produit ou service (revenus moins coûts directs). Ensuite on enlève les coûts fixes (structure, salaires, loyer). Si le résultat est positif, c'est rentable. Souvent, certains produits portent d'autres — l'analyse par ligne révèle les vaches à lait et les gouffres cachés."},
    {"prompt": "Mon chiffre d'affaires croît mais ma trésorerie baisse — pourquoi ?", "answer": "Croissance sans rentabilité. Trois causes fréquentes : coûts variables qui croissent plus vite que le CA (livraison non scalable), investissements en avance sur les revenus, ou délais de paiement clients qui créent un décalage de trésorerie. On analyse chaque ligne de coût pour identifier celle qui ne suit pas."},
    {"prompt": "Comment calculer le point mort d'un SaaS ?", "answer": "Point mort = Coûts fixes mensuels / MRR par client. Si tes coûts fixes sont 10k€/mois et ton MRR moyen est 100€/client, il te faut 100 clients actifs pour être à l'équilibre. Tout au-dessus génère de la marge. Cette métrique est clé pour savoir quand le modèle devient soutenable."}
  ],
  "response_guidance": {
    "tone": "analytique, factuel, orienté pilotage",
    "structure": ["identifier la métrique clé selon le contexte", "calculer ou estimer avec les données disponibles", "interpréter le résultat", "proposer une décision ou un suivi"],
    "avoid": ["utiliser des termes comptables sans les définir", "donner un avis sur la santé business sans données", "confondre rentabilité et trésorerie"]
  },
  "tags": ["rentabilité", "marge", "break-even", "LTV", "CAC", "ROI", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.business_piloting.pricing_strategy", "knowledges.cpl.business_piloting.revenue_mix_strategy", "knowledges.professional.product_management.kpi_product_advanced"]
})

save("cpl/business_piloting/revenue_mix_strategy.json", {
  "schema_version": "1.2", "type": "knowledge_unit",
  "id": "knowledges.cpl.business_piloting.revenue_mix_strategy",
  "title": "Stratégie de mix de revenus",
  "domain": "cpl", "subdomain": "business_piloting",
  "status": "validated",
  "summary": "Diversifier ses sources de revenus réduit le risque de concentration et améliore la résilience. Un bon mix combine revenus récurrents (prévisibles), ponctuels (flexibles) et latents (upsell).",
  "core_definition": "Le mix de revenus est la combinaison optimale de sources de revenus d'une organisation — abonnements, ventes unitaires, services, commissions, licences — conçue pour maximiser la stabilité, la croissance et la rentabilité globale.",
  "knowledge": {
    "revenue_types": [
      {"type": "Revenus récurrents (MRR/ARR)", "examples": "Abonnements SaaS, maintenance, retainers", "benefit": "Prévisibles, valorisés 5-10× en valorisation startup"},
      {"type": "Revenus ponctuels", "examples": "Ventes unitaires, projets, formations", "benefit": "Flexibles, levier de croissance rapide"},
      {"type": "Revenus d'expansion", "examples": "Upsell, cross-sell, modules additionnels", "benefit": "Meilleure LTV, coût d'acquisition nul"},
      {"type": "Revenus partenaires", "examples": "Commissions, affiliations, revendeurs", "benefit": "Scalabilité sans équipe de vente propre"},
      {"type": "Revenus passifs", "examples": "Licences, API fees, royalties", "benefit": "Marge très élevée si le produit existe déjà"}
    ],
    "mix_principles": [
      "Viser 60-70% de revenus récurrents dans un modèle SaaS/produit",
      "Limiter la dépendance à un seul client (max 30% du CA)",
      "Développer l'expansion revenue avant le nouveau client (plus économique)",
      "Analyser la marge par type de revenu — tous ne sont pas également profitables",
      "Tester de nouvelles sources sans déstabiliser les sources existantes"
    ],
    "concentration_risks": [
      "Un client > 40% du CA : risque systémique à un départ",
      "100% de revenus ponctuels : croissance non prévisible",
      "Revenus géographiques concentrés : exposition aux crises locales",
      "Mono-produit : vulnérabilité à la disruption ou à l'obsolescence"
    ]
  },
  "example_answers": [
    {"prompt": "On vit uniquement de projets ponctuels, comment stabiliser ?", "answer": "Identifier dans nos projets ce qui se répète — maintenance, mises à jour, accompagnement — et le proposer sous forme d'abonnement mensuel. Même 20% de revenus récurrents change radicalement la prédictibilité du business. L'offre de retainer est souvent plus facile à vendre à un client existant qu'à un nouveau."},
    {"prompt": "Un client représente 60% de notre CA, que faire ?", "answer": "Risque critique à traiter maintenant, avant la crise. Plan d'action en parallèle : diversifier activement (prospection, partenariats) et sécuriser la relation client existante (contrat long terme, expansion dans le compte). Ne jamais tenter de réduire la dépendance en dégradant la relation avec le client concentré."},
    {"prompt": "Quelles nouvelles sources de revenus explorer pour un produit IA ?", "answer": "API access pour intégration tierce, formation et certification utilisateurs, consulting d'implémentation, marketplace de connecteurs, licence white-label pour partenaires. La règle : commencer par les plus proches de ce qu'on sait déjà faire — le risque d'exécution est plus faible."}
  ],
  "response_guidance": {
    "tone": "orienté pilotage, réaliste sur les risques",
    "structure": ["évaluer le mix actuel", "identifier le risque de concentration", "proposer une diversification réaliste", "mesurer la progression"],
    "avoid": ["proposer des sources de revenus non accessibles à court terme", "ignorer les coûts d'activation d'un nouveau canal", "sous-estimer l'effort de vente pour chaque nouveau type"]
  },
  "tags": ["revenus", "mix", "diversification", "MRR", "ARR", "récurrents", "cpl"],
  "related_knowledge_units": ["knowledges.cpl.business_piloting.profitability_analysis", "knowledges.cpl.business_piloting.pricing_strategy", "knowledges.cpl.strategy.business_model_design"]
})

print("\nBatch CPL Strategy + Execution + Business Piloting : DONE")
