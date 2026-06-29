"""
Enrichissement Knowledge Base ALFRED - Batch 10 : PM/Advanced (15 restants) + cpl/business_strategy (10 premiers)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku_pm(stem, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.professional.product_management.advanced.{stem}",
      "title": title, "domain": "professional", "subdomain": "product_management_advanced",
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": "stratégique, ancré dans les métriques et la réalité des utilisateurs",
        "structure": ["identifier le contexte produit", "expliquer le framework", "proposer une application concrète"],
        "avoid": ["trop théorique", "ignorer les contraintes business", "recommander sans contexte"]
      },
      "tags": tags + ["product management", "produit"],
      "related_knowledge_units": ["knowledges.cpl.strategy.strategy_fundamentals", "knowledges.cpl.product_ia.user_needs_analysis"]
    }

def ku_bs(stem, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.cpl.business_strategy.{stem}",
      "title": title, "domain": "cpl", "subdomain": "business_strategy",
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": "stratégique, ancré dans la réalité opérationnelle et les contraintes de marché",
        "structure": ["analyser le contexte concurrentiel et client", "proposer la lecture stratégique", "recommander les prochaines actions"],
        "avoid": ["conseils trop génériques", "ignorer les contraintes de ressources", "optimisme non fondé"]
      },
      "tags": tags + ["stratégie", "business", "CPL"],
      "related_knowledge_units": ["knowledges.cpl.strategy.strategy_fundamentals", "knowledges.cpl.business_piloting.profitability_analysis"]
    }

# =============================================================================
# professional / product_management / advanced (15 restants)
# =============================================================================

save("professional/product_management/advanced/product_led_growth.json", ku_pm(
  "product_led_growth",
  "Product-Led Growth (PLG)",
  "Le Product-Led Growth est une stratégie de croissance dans laquelle le produit lui-même est le principal moteur d'acquisition, de rétention et d'expansion — par opposition aux modèles Sales-Led ou Marketing-Led.",
  "Le Product-Led Growth (PLG) est une stratégie de go-to-market dans laquelle le produit est le principal vecteur d'acquisition (freemium, essai gratuit, auto-activation), de rétention (valeur continue) et d'expansion (upgrades naturels, expansion au sein des comptes). L'utilisateur expérimente la valeur avant de payer.",
  {
    "plg_pillars": [
      {"pillar": "Acquisition PLG", "mechanism": "L'utilisateur peut commencer à utiliser le produit sans friction (freemium, essai, open source)", "examples": ["Slack freemium", "Notion free tier", "Dropbox storage gratuit initial"]},
      {"pillar": "Activation PLG", "mechanism": "L'onboarding est conçu pour que l'utilisateur atteigne le aha moment sans aide commerciale", "key": "Time-to-value minimum"},
      {"pillar": "Expansion PLG", "mechanism": "La valeur croît avec l'usage — incitation naturelle à upgrader ou à inviter des collègues", "examples": ["Slack : limite de messages gratuits → upgrade team", "Figma : partage → collaborateurs rejoignent"]}
    ],
    "plg_vs_sled": {
      "PLG": "Utilisateur découvre par lui-même → paye si valeur. Scalable, faible CAC, long cycle avant conversion.",
      "Sales-Led": "Commercial démontre → contrat. Plus rapide sur les grands comptes, CAC élevé, nécessite une force de vente."
    },
    "plg_metrics": ["Time to value (TTV)", "Activation rate", "Product Qualified Lead (PQL)", "Expansion MRR", "Viral coefficient (K-factor)"]
  },
  [
    {"prompt": "Mon SaaS devrait-il adopter un modèle PLG ou Sales-Led ?", "answer": "PLG est adapté si : le produit peut être utilisé individuellement sans formation (value time < 30 min), le persona est un utilisateur individuel ou team leader (pas C-suite), et la valeur est ressentie immédiatement. Sales-Led est mieux si : le produit nécessite une intégration complexe, les décisions d'achat impliquent la direction, ou la valeur est dans la personnalisation. Beaucoup de SaaS combinent les deux : PLG pour l'acquisition (freemium) + Sales pour les grands comptes (enterprise)."},
    {"prompt": "Comment améliorer le time-to-value d'un produit PLG ?", "answer": "Cartographier le chemin de l'inscription au aha moment avec des timestamps moyens par étape. Identifier le plus grand délai. Tester : (1) réduire les étapes d'onboarding (chaque champ supplémentaire dans l'inscription coûte 5-10% d'activation), (2) montrer immédiatement un exemple de valeur (templates, données démo pré-remplies), (3) checklist d'activation guidée avec progress bar. L'objectif : le premier 'wow' en moins de 5 minutes."}
  ],
  ["PLG", "freemium", "growth", "SaaS", "time-to-value"]
))

save("professional/product_management/advanced/product_roadmap.json", ku_pm(
  "product_roadmap",
  "Roadmap produit — construction et communication",
  "Une roadmap produit efficace communique la direction et les priorités sans s'engager sur des dates précises pour un futur lointain. Elle doit être vivante, basée sur des outcomes (pas des features), et alignée avec la stratégie.",
  "La roadmap produit est une représentation de la direction stratégique d'un produit dans le temps, montrant les initiatives priorisées et les objectifs à atteindre. Une bonne roadmap communique le pourquoi et le quoi, laissant au comment sa flexibilité, et reste adaptable aux nouvelles informations.",
  {
    "roadmap_types": [
      {"type": "Roadmap maintenant/prochainement/plus tard", "description": "3 horizons sans dates précises — honnêteté sur l'incertitude du futur", "use": "Communication externe, parties prenantes"},
      {"type": "Roadmap par objectif/OKR", "description": "Organisée par outcome à atteindre plutôt que par feature", "use": "Interne, équipe produit"},
      {"type": "Roadmap par thème", "description": "Features regroupées par thème stratégique", "use": "Communication executives, investisseurs"},
      {"type": "Roadmap trimestrielle détaillée", "description": "Plan T+1 avec features et dates, T+2/T+3 moins précis", "use": "Planning opérationnel"}
    ],
    "roadmap_anti_patterns": [
      "Feature list avec dates figées à 18 mois — promesse impossible à tenir",
      "Roadmap qui ne dit pas pourquoi (seulement quoi) — incompréhensible pour les stakeholders",
      "Roadmap non mise à jour — déconnectée de la réalité",
      "Roadmap identique pour toutes les audiences — le discours client ≠ le discours engineering"
    ],
    "outcome_roadmap": "Structurée par objectifs mesurables plutôt que features : 'Q1 : réduire le churn D30 de 35% à 25%' → solutions possibles à identifier, pas dictées. Ce modèle crée de l'agilité : si une hypothèse de feature ne fonctionne pas, on cherche une autre solution au même outcome."
  },
  [
    {"prompt": "Comment convaincre les dirigeants d'adopter une roadmap Now/Next/Later plutôt qu'une roadmap datée ?", "answer": "Arguments : (1) Une roadmap datée au-delà de 3 mois est une fiction — les études montrent que les prévisions produit à 6+ mois sont fausses 80% du temps. (2) Une roadmap datée crée des engagements clients difficiles à tenir si on pivote. (3) Les dates figées ralentissent la réactivité — l'équipe optimise pour 'livrer dans les délais' plutôt que 'créer de la valeur'. Proposition : roadmap datée pour T+1 (trimestre courant), Now/Next/Later pour la suite."},
    {"prompt": "Comment communiquer la roadmap différemment selon l'audience ?", "answer": "Trois variantes : (1) Équipe technique : roadmap par objectif avec les hypothèses de solutions et les questions ouvertes. (2) Dirigeants/investisseurs : roadmap par thème stratégique et impact business attendu. (3) Clients : Now/Next/Later par problème résolu, pas par feature technique — 'vous pourrez bientôt collaborer en temps réel' plutôt que 'WebSocket multiplayer'."}
  ],
  ["roadmap", "OKR", "Now/Next/Later", "communication", "outcome"]
))

save("professional/product_management/advanced/okr_product.json", ku_pm(
  "okr_product",
  "OKR en product management",
  "Les OKR (Objectives and Key Results) alignent l'équipe produit sur des objectifs ambitieux mesurables. La version product est centrée sur les outcomes utilisateurs et métriques produit, pas sur les outputs (features livrées).",
  "Les OKR (Objectives and Key Results) sont un framework de définition et de suivi des objectifs dans lequel chaque Objective est une déclaration qualitative ambitieuse et chaque Key Result est un indicateur quantitatif mesurable qui définit ce que le succès de l'objectif signifie concrètement.",
  {
    "okr_structure": {
      "objective": "Qualitatif, inspirant, mémorable — 'Devenir l'assistant IA le plus apprécié des professionnels indépendants'",
      "key_results": ["Quantitatifs, mesurables, avec un chiffre cible", "3 à 5 KRs par objectif", "Représentent les signaux que l'objectif est atteint"],
      "initiatives": "Les actions et projets qui permettent d'atteindre les KRs — séparées des OKRs"
    },
    "product_okr_examples": [
      {
        "objective": "Améliorer l'activation des nouveaux utilisateurs",
        "key_results": [
          "Time-to-first-value < 10 minutes (vs 25 actuellement)",
          "Taux de complétion onboarding J0 > 60% (vs 35%)",
          "Activation rate D7 > 40% (vs 22%)"
        ]
      }
    ],
    "common_okr_mistakes": [
      "KRs = tâches à faire plutôt que résultats à atteindre ('lancer X feature' plutôt que 'Y% d'utilisation de la feature')",
      "Trop d'OKRs — focus impossible avec > 3 objectifs par équipe",
      "OKRs trop faciles — pas de stretch, pas d'ambition",
      "Lier OKRs à la rémunération — crée des comportements de gaming des métriques"
    ]
  },
  [
    {"prompt": "Comment écrire de bons Key Results pour un produit IA ?", "answer": "Les bons KRs pour un produit IA : mesurer l'impact sur l'utilisateur, pas la performance du modèle. Mauvais : 'améliorer le score BLEU de 0.65 à 0.75' — indicateur technique non corrélé à la valeur perçue. Bon : 'taux de satisfaction des réponses IA > 85%' ou '% d'utilisateurs qui adoptent la suggestion IA au moins 3 fois/semaine > 60%'. Aussi : mesurer la confiance ('% de réponses notées utiles') et l'adoption ('% de workflows utilisant l'IA')."},
    {"prompt": "Quelle différence entre OKR et KPI ?", "answer": "Les KPIs sont des indicateurs de santé en continu (taux d'attrition, MRR, NPS) — ils ne ont pas de date de fin et mesurent l'état courant du business. Les OKRs sont des engagements temporaires et ambitieux (par trimestre ou annuels) sur où l'équipe veut aller. En pratique : les KPIs te disent si tu es en bonne santé, les OKRs te disent si tu progresses vers tes ambitions. Les deux coexistent — les OKRs peuvent chercher à améliorer des KPIs, mais les KPIs ne disparaissent pas quand les OKRs se terminent."}
  ],
  ["OKR", "objectifs", "métriques", "Key Results", "alignement"]
))

save("professional/product_management/advanced/pricing_strategy_saas.json", ku_pm(
  "pricing_strategy_saas",
  "Stratégie de pricing SaaS",
  "Le pricing SaaS est l'une des décisions les plus impactantes sur la croissance et la profitabilité. Les modèles per-seat, usage-based et freemium ont des dynamiques de croissance très différentes. Le prix communique la valeur autant qu'il la capture.",
  "La stratégie de pricing SaaS est l'ensemble des décisions sur le modèle de tarification (freemium, per-seat, usage-based, flat), les niveaux de prix et la segmentation par valeur perçue, qui optimisent conjointement l'acquisition, la rétention et la croissance du revenu.",
  {
    "saas_pricing_models": [
      {"model": "Per-seat", "description": "Prix par utilisateur/mois", "pros": ["Prédictible", "Aligné avec la croissance des équipes"], "cons": ["Frein à l'adoption large dans les grands comptes", "Gaming (comptes partagés)"]},
      {"model": "Usage-based", "description": "Prix proportionnel à l'utilisation (API calls, GB, events)", "pros": ["Aligné sur la valeur créée", "Scalable avec le client"], "cons": ["Revenu imprévisible", "Anxiété des clients sur leur facture"]},
      {"model": "Freemium", "description": "Gratuit avec limites, payant pour plus", "pros": ["Acquisition organique", "PLG-friendly"], "cons": ["Coût d'infrastructure pour les freemium non-convertis", "Conversion souvent < 5%"]},
      {"model": "Tiered flat", "description": "3-4 plans à prix fixe avec features différentes", "pros": ["Simple à communiquer", "Previsible"], "cons": ["Moins capturant de valeur que usage-based"]}
    ],
    "value_metrics": "La métrique de valeur est la dimension sur laquelle le prix varie — ce qui corrèle le mieux avec la valeur perçue par le client. Trouver la bonne value metric (seats, contacts, MAU, API calls) est plus impactant que le niveau de prix lui-même.",
    "price_anchoring": "L'ancrage de prix : présenter le plan premium en premier augmente la perception de valeur des plans inférieurs. Slack montre le prix entreprise pour ancrer avant le plan Pro."
  },
  [
    {"prompt": "Comment choisir entre pricing per-seat et usage-based pour mon SaaS B2B ?", "answer": "Question clé : comment la valeur créée pour le client évolue-t-elle ? Si elle croît avec le nombre d'utilisateurs (collaboration, communication) → per-seat. Si elle croît avec le volume d'usage (API, data processing, emails envoyés) → usage-based. Pour les AI products : souvent usage-based sur les tokens/appels API car la valeur est dans le volume de traitement. Attention : usage-based est plus agressif à convertir (le client perçoit le risque de surcharge) — prévoir un cap ou une garantie de prix maximum."},
    {"prompt": "À quel moment augmenter les prix de mon SaaS ?", "answer": "Trois signaux : (1) Le taux de churn reste bas même après une tentative d'augmentation (willingness to pay prouvée), (2) Ton NPS est > 50 (clients très satisfaits → moins de sensibilité prix), (3) Les clients utilisent massivement et ne se plaignent pas du prix (sous-tarification probable). Méthode : enquête Van Westendorp (4 questions de prix — trop cher, cher mais acceptable, bon rapport qualité/prix, trop bon marché pour être crédible) pour identifier la zone acceptable de prix."}
  ],
  ["pricing", "SaaS", "freemium", "per-seat", "usage-based", "value metric"]
))

save("professional/product_management/advanced/user_story_mapping.json", ku_pm(
  "user_story_mapping",
  "User Story Mapping (Jeff Patton)",
  "Le User Story Mapping organise les user stories en deux dimensions — le flux d'activité (horizontal) et le niveau de détail (vertical) — permettant de voir le produit entier et de prendre des décisions intelligentes de priorisation par tranche (slice).",
  "Le User Story Mapping est une technique de visualisation produit développée par Jeff Patton qui organise les user stories sur une carte bidimensionnelle : l'axe horizontal représente le flux chronologique des activités de l'utilisateur, l'axe vertical représente le niveau de priorité/détail, permettant d'identifier des 'slices' cohérentes pour les releases.",
  {
    "story_map_structure": {
      "backbone": "La rangée supérieure — les activités principales de l'utilisateur dans l'ordre chronologique",
      "walking_skeleton": "La rangée suivante — les user stories minimales qui permettent de 'marcher' dans chaque activité",
      "details": "Les rangées inférieures — les variations, exceptions et améliorations par activité",
      "slices": "Des coupes horizontales qui définissent des releases cohérentes (MVP, V1, V2)"
    },
    "benefits_over_backlog": [
      "Voir le produit entier d'un coup d'oeil — le backlog plat perd le contexte",
      "Conversations autour de la carte — l'image facilite les discussions sur les priorités",
      "Identifier les gaps — les activités sans user stories montrent des angles morts",
      "Slices cohérentes — les releases ont un sens narratif pour l'utilisateur"
    ],
    "mvp_identification": "Sur la story map, le MVP est la slice minimale qui permet à un utilisateur de compléter son job de bout en bout. La question : 'Quel est le chemin critique que tout utilisateur doit pouvoir parcourir ?' Les améliorations et cas edge sont dans les slices suivantes."
  },
  [
    {"prompt": "Comment identifier le MVP d'un produit avec le Story Mapping ?", "answer": "Construire la story map : (1) Identifier les grandes activités utilisateurs (backbone horizontal), (2) Sous chaque activité, lister les user stories ordonnées par importance (verticalement), (3) Tracer une ligne horizontale qui coupe la carte — tout ce qui est au-dessus est le MVP. La ligne doit laisser un chemin complet pour l'utilisateur principal. Test : 'Avec seulement ces stories, est-ce qu'un utilisateur peut accomplir son job principal de bout en bout ?' Si non, lever la ligne."},
    {"prompt": "Story Map vs backlog — quand utiliser l'un plutôt que l'autre ?", "answer": "Story Map pour la vision et la roadmap — quand tu as besoin de comprendre le produit dans sa globalité, aligner l'équipe et décider des slices de releases. Backlog pour l'exécution — quand les stories sont priorisées et l'équipe sait ce qu'elle fait en sprint courant. En pratique : la Story Map génère le backlog, le backlog détaille la Story Map. Revisiter la Story Map à chaque cycle de planification (trimestrielle ou avant chaque release majeure)."}
  ],
  ["story mapping", "MVP", "backlog", "Jeff Patton", "user stories"]
))

save("professional/product_management/advanced/north_star_metric.json", ku_pm(
  "north_star_metric",
  "North Star Metric",
  "La North Star Metric (NSM) est la métrique unique qui capture le mieux la valeur créée pour les utilisateurs ET le succès business à long terme. Elle aligne toute l'équipe sur un objectif commun et guide les décisions de priorité.",
  "La North Star Metric est l'indicateur unique qui représente le mieux la valeur centrale qu'un produit crée pour ses utilisateurs et qui est le plus prédictif de la croissance long terme du business. Elle sert d'étoile polaire pour l'alignement des équipes et la priorisation.",
  {
    "nsm_criteria": [
      "Elle mesure la valeur pour l'utilisateur (pas juste le revenu)",
      "Elle est actionnable par les équipes produit et engineering",
      "Elle est prédictive du revenu long terme",
      "Elle est compréhensible par toute l'équipe",
      "Elle n'est pas gameable sans créer de vraie valeur"
    ],
    "nsm_examples": [
      {"company": "Spotify", "nsm": "Temps écouté par utilisateur actif"},
      {"company": "Airbnb", "nsm": "Nuits réservées"},
      {"company": "Slack", "nsm": "Messages envoyés dans les workspaces"},
      {"company": "Facebook (2008)", "nsm": "DAU (Daily Active Users)"},
      {"company": "Notion", "nsm": "Teams collaborant activement"}
    ],
    "nsm_vs_vanity_metrics": "Les vanity metrics gonflent bien (téléchargements, inscriptions, pageviews) mais ne corrèlent pas avec la valeur réelle. La NSM est difficile à gonfler : tu ne peux pas augmenter les 'nuits réservées' Airbnb sans que des utilisateurs trouvent réellement une valeur dans le service."
  },
  [
    {"prompt": "Comment trouver la North Star Metric de mon produit IA ?", "answer": "Pour un assistant IA : la NSM doit capturer l'engagement de valeur, pas juste l'usage. Questions à poser : 'Quel comportement utilisateur montre qu'ALFRED leur a vraiment créé de la valeur ?' Des candidats : nombre de sessions où l'utilisateur a pris une action concrète suite à une réponse, ou % de réponses notées 'utiles'. Éviter : nombre de messages envoyés (gameable, ne reflète pas la valeur), nombre de connexions (vanity)."},
    {"prompt": "Peut-on avoir plusieurs North Star Metrics ?", "answer": "Non — c'est contradictoire avec le concept. Si tu as plusieurs métriques 'north star', aucune ne joue vraiment ce rôle. En revanche, la NSM est souvent accompagnée de 2-4 'input metrics' (les leviers qui l'alimentent) et de 'guardrail metrics' (les indicateurs à ne pas dégrader). Structure : NSM au sommet, input metrics au milieu (chacune actionnable par une équipe), guardrails en surveillance continue."}
  ],
  ["North Star", "métriques", "alignement", "valeur", "NSM"]
))

save("professional/product_management/advanced/discovery_vs_delivery.json", ku_pm(
  "discovery_vs_delivery",
  "Discovery vs Delivery — équilibre en product management",
  "Le Double Diamond du product management distingue la discovery (comprendre le problème et valider l'opportunité) de la delivery (construire la solution). L'erreur la plus coûteuse est de trop investir en delivery avant d'avoir validé la discovery.",
  "La distinction discovery/delivery en product management sépare les activités de compréhension des problèmes et de validation des opportunités (discovery) des activités de construction et de déploiement des solutions (delivery). Un équilibre sain entre les deux évite de construire des solutions à des problèmes non validés.",
  {
    "discovery_activities": [
      "Interviews utilisateurs (comprendre les jobs et les frustrations)",
      "Analyse de données comportementales",
      "Tests d'hypothèses (prototypes, smoke tests, landing pages)",
      "Mapping des opportunités",
      "Exploration des solutions possibles"
    ],
    "delivery_activities": [
      "Définition des user stories",
      "Développement et tests",
      "Déploiement et monitoring",
      "Itérations sur le produit livré"
    ],
    "common_trap": "Squads 100% en delivery : on construit vite mais on construit les mauvaises choses. Squads 100% en discovery : on apprend mais on ne livre jamais. L'objectif : dual-track où la discovery alimente la delivery en continu.",
    "dual_track": {
      "description": "Two tracks en parallèle : l'équipe développe les features validées (delivery) pendant que le PM/designer valide les prochaines opportunités (discovery)",
      "benefit": "La discovery toujours un pas devant la delivery — plus de moments où l'équipe attend quoi construire"
    }
  },
  [
    {"prompt": "Comment savoir si mon équipe passe trop de temps en delivery vs discovery ?", "answer": "Signe de trop de delivery : l'équipe livre des features régulièrement mais les métriques produit ne bougent pas. Les features livrées ne sont pas ou peu utilisées. Signe de trop de discovery : l'équipe génère des insights mais ne livre pas. Idéal : au moins 20% du temps PM en discovery active. Pour mesurer : combien d'interviews utilisateurs par semaine ? Combien d'hypothèses testées par sprint ? Si la réponse est 'zéro', il faut rééquilibrer."},
    {"prompt": "Comment tester une hypothèse produit sans développer la feature ?", "answer": "Techniques de discovery légère : (1) Smoke test (landing page décrivant la feature avec un CTA 'rejoindre la liste d'attente' — mesurer le % qui s'inscrivent), (2) Wizard of Oz (simuler manuellement la feature pour 5-10 utilisateurs avant de la développer), (3) Prototype cliquable (InVision/Figma — tester l'UX sans code), (4) Fake door (menu ou bouton pour la feature inexistante — mesurer les clics et afficher 'bientôt disponible'). Ces tests coûtent 10x moins qu'un développement."}
  ],
  ["discovery", "delivery", "dual-track", "validation", "prototypage"]
))

save("professional/product_management/advanced/product_led_sales.json", ku_pm(
  "product_led_sales",
  "Product-Led Sales (PLS)",
  "Le Product-Led Sales combine le PLG (acquisition par le produit) et le Sales (conversion des comptes à fort potentiel). Les équipes commerciales s'appuient sur les signaux d'usage produit pour identifier et closer les Product Qualified Leads (PQL).",
  "Le Product-Led Sales est un modèle de go-to-market hybride dans lequel l'acquisition et l'activation initiale se font via le produit (PLG), mais les comptes à fort potentiel sont identifiés par des signaux d'usage produit (Product Qualified Leads) et traités par une équipe commerciale qui s'appuie sur ces données.",
  {
    "pql_definition": {
      "PQL": "Product Qualified Lead — utilisateur ou entreprise qui a atteint un certain niveau d'activation produit, signalant une forte propension à convertir en compte payant",
      "examples": [
        "Utilisateur qui a invité > 3 collègues dans les 7 premiers jours",
        "Compte avec > 5 utilisateurs actifs sur le plan gratuit",
        "Utilisateur qui a atteint 80% de la limite du plan gratuit"
      ]
    },
    "pls_signals": [
      "Volume d'usage élevé sur le plan gratuit",
      "Invitation de nombreux collègues (expansion dans l'entreprise)",
      "Utilisation de features premium en essai",
      "Fort engagement (fréquence quotidienne)",
      "Signaux d'intention (visite de la page pricing, click sur 'upgrade')"
    ],
    "commercial_value_add": "Dans un modèle PLS, le commercial n'explique pas la valeur du produit (l'utilisateur l'a déjà expérimentée) — il accélère l'expansion (account-wide deployment), gère les frictions d'achat (procurement, sécurité, contrat) et monte la conversation au niveau décisionnel."
  },
  [
    {"prompt": "Comment définir les PQL pour mon SaaS ?", "answer": "Méthode data-driven : analyser les utilisateurs qui ont converti au cours des 6 derniers mois et identifier les comportements produit J0-J30 qui les distinguent des non-convertis. Construire un score PQL basé sur ces comportements (pondérés selon leur pouvoir prédictif). Seuil PQL = le niveau de score au-delà duquel le taux de conversion est suffisamment élevé pour justifier l'intervention commerciale. Revoir le modèle tous les trimestres."},
    {"prompt": "Mon équipe sales se plaint que les leads PLG sont de mauvaise qualité — pourquoi ?", "answer": "Deux causes probables : (1) La définition des PQL n'est pas assez précise — elle capture des utilisateurs actifs mais pas prêts à payer. Solution : affiner le modèle PQL avec des données de conversion réelles. (2) L'équipe sales traite les PQL comme des MQL classiques (appels froids) plutôt que comme des utilisateurs qui ont déjà expérimenté la valeur. Approche PLS : le premier message commercial fait référence à l'usage produit ('je vois que tu utilises X fonctionnalité — qu'est-ce qui te permettrait d'en faire plus ?')."}
  ],
  ["PLS", "PLG", "PQL", "sales", "conversion", "SaaS"]
))

save("professional/product_management/advanced/feature_prioritization.json", ku_pm(
  "feature_prioritization",
  "Frameworks de priorisation des features",
  "Prioriser les features est une des décisions les plus difficiles en product management. Les frameworks (RICE, ICE, MoSCoW, Impact/Effort) structurent la décision et créent un alignement autour de critères explicites et partagés.",
  "La priorisation des features en product management est le processus de classement des initiatives produit selon des critères explicites (impact, effort, risque, alignement stratégique) permettant d'allouer les ressources limitées aux opportunités à plus forte valeur.",
  {
    "prioritization_frameworks": [
      {"framework": "RICE", "criteria": "Reach × Impact × Confidence / Effort", "pros": ["Quantitatif", "Transparent"], "cons": ["Subjectivité dans les estimations"]},
      {"framework": "ICE", "criteria": "Impact × Confidence × Ease", "pros": ["Simple", "Rapide"], "cons": ["Moins rigoureux que RICE"]},
      {"framework": "MoSCoW", "criteria": "Must have / Should have / Could have / Won't have", "pros": ["Simple à communiquer", "Bon pour le scope MVP"], "cons": ["Pas quantitatif — contestations sur le classement"]},
      {"framework": "Kano", "criteria": "Basique / Performance / Attractif / Indifférent / Repoussant", "pros": ["Centré sur la satisfaction utilisateur", "Distingue ce qui crée de la satisfaction vs évite de la frustration"], "cons": ["Nécessite des données utilisateurs — plus long à appliquer"]}
    ],
    "pitfalls": [
      "Priorisation par la voix la plus forte — le stakeholder le plus influent dicte le backlog",
      "Priorisation par ancienneté — 'on a promis cette feature depuis 2 ans'",
      "Optimiser uniquement l'effort — les quick wins sont aimés mais pas toujours stratégiques",
      "Ignorer les risques — une feature à fort impact mais à haute incertitude est surestimée"
    ]
  },
  [
    {"prompt": "Quel framework de priorisation utiliser pour une startup early-stage ?", "answer": "ICE ou impact/effort simple pour démarrer — la légèreté compte quand le backlog est petit et l'information incertaine. Éviter la précision fausse de RICE avec des estimations arbitraires. Règle pratique : une réunion de priorisation de 1h par semaine avec les 3-4 critères clés. À mesure que l'équipe grandit et que le backlog s'alourdit, passer à RICE ou à une priorisation par objectif (OKR-driven)."},
    {"prompt": "Comment gérer les demandes features qui viennent de tous les côtés (clients, sales, CEO) ?", "answer": "Processus : (1) Toutes les demandes entrent dans un même endroit (Notion, Jira, Linear), (2) Chaque demande est évaluée sur les mêmes critères (impact utilisateur, alignement stratégie, effort), (3) Les demandes sont groupées par problème (pas par solution proposée — plusieurs clients peuvent avoir le même besoin exprimé différemment), (4) Le PM décide en fonction des critères, explique le raisonnement, et communique la décision. La transparence du processus atténue les frustrations des stakeholders."}
  ],
  ["priorisation", "RICE", "ICE", "MoSCoW", "Kano", "backlog"]
))

save("professional/product_management/advanced/product_market_fit.json", ku_pm(
  "product_market_fit",
  "Product-Market Fit (PMF)",
  "Le Product-Market Fit est le moment où un produit répond suffisamment bien à un besoin de marché pour générer une rétention organique et une croissance par bouche-à-oreille. L'atteindre est la priorité absolue avant de scaler.",
  "Le Product-Market Fit (PMF) est l'état dans lequel un produit satisfait suffisamment bien un besoin de marché réel pour que les utilisateurs l'adoptent massivement, restent actifs et le recommandent naturellement, générant une croissance organique.",
  {
    "pmf_signals": [
      "Rétention qui s'aplatit sur un plateau stable (> 20-40% selon le secteur)",
      "Croissance organique significative (bouche-à-oreille, referrals)",
      "Utilisateurs frustrés à l'idée de ne plus avoir le produit (Rahul Vohra test : > 40% diraient 'très déçus' si le produit disparaissait)",
      "NPS > 40-50",
      "Churn faible et cohérent avec la valeur perçue"
    ],
    "pmf_measurement": {
      "sean_ellis_test": "Demander aux utilisateurs actifs : 'Comment vous sentiriez-vous si vous ne pouviez plus utiliser ce produit ?' > 40% répondent 'très déçu' → PMF probable",
      "retention_curve": "Si la rétention s'aplatit (ne descend pas à zéro), un sous-ensemble d'utilisateurs a trouvé la valeur — creuser ce segment",
      "nps": "Net Promoter Score > 40 = fort signal de PMF"
    },
    "before_after_pmf": {
      "avant": "Chaque utilisateur est convaincu difficilement, les churns sont nombreux et inexpliqués, la croissance dépend de l'acquisition payante",
      "apres": "Les utilisateurs reviennent sans friction, recommandent naturellement, et certains sont des 'power users' qui utilisent le produit quotidiennement"
    }
  },
  [
    {"prompt": "Comment savoir si j'ai atteint le product-market fit ?", "answer": "Test pragmatique : (1) Lance le Sean Ellis Test auprès de tes utilisateurs actifs — si > 40% sont 'très déçus' à l'idée de perdre le produit, signal fort. (2) Regarde ta courbe de rétention à D30/D90 — si elle s'aplatit (ne descend pas à zéro), un segment trouve de la valeur réelle. (3) Observe la croissance organique — si les nouveaux utilisateurs viennent sans acquisition payante, le PMF fait son travail. Le feeling qualitatif : les utilisateurs te demandent des features, pas de l'aide pour comprendre le produit."},
    {"prompt": "Comment scaler avant d'avoir le PMF ?", "answer": "Bonne question — la réponse est : ne pas scaler avant le PMF. Scaler sans PMF amplifie une machine qui fuit : chaque utilisateur acquis churne rapidement, le CAC augmente sans LTV pour le justifier, et l'équipe est épuisée à acquérir pour voir partir. La priorité pré-PMF : réduire le cycle d'apprentissage (interviews rapides, iterations courtes), aller vers les utilisateurs les plus engagés pour comprendre pourquoi ils restent, et doubler sur ce qui génère de la rétention."}
  ],
  ["PMF", "product-market fit", "rétention", "croissance", "Sean Ellis"]
))

save("professional/product_management/advanced/data_informed_decisions.json", ku_pm(
  "data_informed_decisions",
  "Décisions data-informed en product management",
  "Les décisions data-informed combinent les données quantitatives (métriques, cohortes, A/B tests) et qualitatives (interviews, feedback) pour décider, plutôt que de dépendre de l'intuition seule ou des données seules. 'Data-informed' n'est pas 'data-driven' — les données éclairent, le jugement humain décide.",
  "Les décisions data-informed en product management sont des décisions qui intègrent de façon délibérée et rigoureuse les données disponibles (quantitatives et qualitatives) comme input au jugement humain, sans que les données remplacent ce jugement — distinguant l'approche data-informed (les données informent) de l'approche data-driven (les données décident).",
  {
    "data_types": [
      {"type": "Quanti", "examples": ["Métriques d'usage", "Taux de conversion", "Rétention", "A/B tests"], "strength": "Mesure l'ampleur et la significativité des phénomènes", "weakness": "Explique le 'quoi' mais rarement le 'pourquoi'"},
      {"type": "Quali", "examples": ["Interviews utilisateurs", "Tests utilisateurs", "NPS verbatims", "Support tickets"], "strength": "Explique le 'pourquoi' et révèle les motivations profondes", "weakness": "Biais de sélection, difficile à généraliser"}
    ],
    "data_pitfalls": [
      "Fausse précision : donner plus de confiance aux chiffres qu'ils ne méritent",
      "Corrélation ≠ causalité : un dashboard ne dit pas pourquoi une métrique bouge",
      "Biais de survivant : les utilisateurs qui répondent aux enquêtes ne sont pas représentatifs des churners",
      "HiPPO effect (Highest Paid Person's Opinion) : les données sont ignorées au profit de l'opinion du dirigeant",
      "Data paralysis : attendre les données parfaites avant de décider"
    ],
    "decision_process": [
      "Définir la question de décision précisément",
      "Identifier les données disponibles et leurs limites",
      "Formuler des hypothèses basées sur les données quanti",
      "Valider ou invalider avec les données quali",
      "Décider en combinant les signaux et le jugement sur le contexte non capturé"
    ]
  },
  [
    {"prompt": "Comment combiner les données quantitatives et qualitatives pour une décision produit ?", "answer": "Cycle en deux temps : (1) Quanti → identifier le 'quoi' (quelle métrique baisse, quel segment churne, quelle feature n'est pas utilisée), (2) Quali → comprendre le 'pourquoi' (interviews des utilisateurs de ce segment, review des verbatims support). L'erreur courante : décider sur les données quanti seules (on optimise sur une corrélation, pas sur une cause réelle) ou sur les données quali seules (on se laisse influencer par les cas vivants en interview, non représentatifs de l'ensemble)."},
    {"prompt": "Nos données montrent que les utilisateurs utilisent peu la feature X — faut-il la supprimer ?", "answer": "Pas directement. D'abord : identifier quel segment l'utilise, même peu. Si 5% des utilisateurs contribuent à 30% du revenu et utilisent X → la supprimer est risqué. Ensuite : comprendre pourquoi l'adoption est faible (discoverability ? complexité ? pas le bon cas d'usage ?). Puis : tester une amélioration ciblée avant de supprimer. La suppression d'une feature est irréversible du point de vue des utilisateurs — vérifier que ce n'est pas une question d'activation avant de conclure qu'il n'y a pas de valeur."}
  ],
  ["data-informed", "décisions", "quantitatif", "qualitatif", "analytics"]
))

save("professional/product_management/advanced/technical_debt_management.json", ku_pm(
  "technical_debt_management",
  "Gestion de la dette technique en product management",
  "La dette technique est un actif qui accumule des 'intérêts' sous forme de ralentissement de développement et de bugs. Le PM doit comprendre, quantifier et négocier la dette technique pour prendre des décisions éclairées sur le ratio features/refactoring.",
  "La gestion de la dette technique en product management est la capacité du PM à comprendre les implications business de la dette technique accumulée, à la quantifier en termes d'impact sur la vélocité et la qualité, et à négocier avec les équipes d'ingénierie un équilibre sain entre développement de nouvelles features et remboursement de la dette.",
  {
    "technical_debt_definition": "Similairement à la dette financière : un raccourci technique pris maintenant crée des 'intérêts' sous forme de temps supplémentaire requis pour chaque future modification dans la zone concernée. La dette est acceptable si elle est consciente et remboursée à temps.",
    "pm_debt_management": [
      "Allouer 20% de la capacité engineering au remboursement de dette (règle empirique)",
      "Quantifier la dette en termes d'impact vélocité (exemple : 'cette dette nous coûte 15% de notre capacité chaque sprint')",
      "Prioriser la dette qui bloque les futures initiatives stratégiques",
      "Inclure le remboursement de dette dans les roadmaps (pas comme une initiative cachée)"
    ],
    "debt_prioritization": [
      {"priority": "Haute", "criterion": "Dette qui ralentit directement les initiatives prioritaires du prochain trimestre"},
      {"priority": "Moyenne", "criterion": "Dette qui génère des bugs récurrents impactant l'expérience utilisateur"},
      {"priority": "Basse", "criterion": "Dette dans du code rarement modifié ou sur le chemin de la dépréciation"}
    ]
  },
  [
    {"prompt": "Comment convaincre les stakeholders business d'allouer du temps au remboursement de la dette technique ?", "answer": "Traduire en langage business : 'Notre dette technique actuelle nous coûte 2 jours-développeur par sprint de overhead. À 1500€/jour, c'est 3000€ par sprint soit ~72k€/an en coût d'opportunité, sans compter les bugs en production qui coûtent X€ en support.' Une fois la dette quantifiée en euros et en délais de livraison, la conversation change. Et montrer l'impact futur : 'si on ne rembourse pas X module, la feature Y (priorité Q1) prendra 3 mois au lieu d'1 mois'."},
    {"prompt": "Comment ALFRED peut m'aider à gérer la dette technique de mon projet ?", "answer": "ALFRED peut t'aider à structurer le dialogue avec l'équipe engineering : quelles zones de dette ont le plus d'impact sur les initiatives à venir ? Comment quantifier la vélocité perdue ? Et côté roadmap : comment réserver de la capacité pour la dette sans sacrifier la livraison de valeur ? Je peux aussi t'aider à préparer la communication aux stakeholders — transformer un problème technique en décision business."}
  ],
  ["dette technique", "refactoring", "vélocité", "product management", "engineering"]
))

save("professional/product_management/advanced/stakeholder_management.json", ku_pm(
  "stakeholder_management",
  "Gestion des parties prenantes en product management",
  "Le PM est au carrefour d'attentes multiples et souvent contradictoires. La gestion des stakeholders demande de cartographier leurs intérêts, d'adapter la communication, et de gérer les conflits avec transparence et données.",
  "La gestion des parties prenantes en product management est l'ensemble des pratiques permettant d'identifier les personnes impactées ou influentes sur les décisions produit, de comprendre leurs intérêts et niveaux d'influence, d'aligner leurs attentes avec la stratégie produit, et de gérer les conflits de priorisation.",
  {
    "stakeholder_mapping": {
      "axes": ["Influence sur les décisions produit", "Intérêt dans le produit"],
      "quadrants": [
        {"quadrant": "Haute influence / Haut intérêt", "strategy": "Gérer de près — communication fréquente, implication dans les décisions clés"},
        {"quadrant": "Haute influence / Bas intérêt", "strategy": "Garder informés — summary régulier, ne pas saturer"},
        {"quadrant": "Basse influence / Haut intérêt", "strategy": "Garder engagés — feedback régulier, champions potentiels"},
        {"quadrant": "Basse influence / Bas intérêt", "strategy": "Informer minimalement — newsletter produit"}
      ]
    },
    "conflict_management": [
      "Rendre visible les trade-offs (pas de décision magique qui satisfait tout le monde)",
      "Utiliser les données pour trancher plutôt que l'autorité",
      "Escalader avec les options et les recommandations, pas juste le problème",
      "Créer un forum de décision partagé (comité produit) pour les décisions cross-équipes"
    ]
  },
  [
    {"prompt": "Comment gérer un CEO qui veut une feature que tu penses inutile ?", "answer": "Ne pas opposer frontalement. Processus : (1) Comprendre le 'pourquoi' derrière la demande — quel problème le CEO essaie de résoudre ? (2) Valider ou invalider l'hypothèse avec des données (usage actuel, interviews clients, benchmarks) — présenter les données, pas ton opinion, (3) Proposer une alternative si l'hypothèse ne tient pas ('plutôt que X, voici ce qui résoudrait le problème que tu décris'), (4) Si toujours bloqué : proposer un test minimal avant l'investissement complet. Le CEO est souvent le plus exposé aux clients — sa demande mérite une vraie exploration avant d'être écarted."},
    {"prompt": "Comment aligner l'équipe sales et l'équipe produit sur les priorités ?", "answer": "Pratiques concrètes : (1) Sales siège aux sprint reviews — comprend ce qui est livré et pourquoi, (2) PM participe à 2-3 appels clients par mois avec sales — exposure aux vrais problèmes, (3) Mécanisme formel de remontée des demandes clients (avec impact quantifié) — le sales doit quantifier combien de deals la feature aurait accéléré, (4) Partage des métriques produit avec sales — NPS, rétention, activation. L'alignement vient de la compréhension mutuelle des contraintes, pas d'un accord de façade."}
  ],
  ["stakeholders", "alignement", "conflits", "communication", "PM"]
))

# =============================================================================
# cpl / business_strategy (10 premiers)
# =============================================================================

save("cpl/business_strategy/competitive_positioning.json", ku_bs(
  "competitive_positioning",
  "Positionnement concurrentiel",
  "Le positionnement concurrentiel définit comment une offre se distingue dans l'esprit des clients par rapport aux alternatives. Un bon positionnement est clair, défendable et ancré dans un avantage compétitif réel.",
  "Le positionnement concurrentiel est la définition délibérée de la place qu'une entreprise occupe dans l'esprit de ses clients cibles par rapport à ses concurrents, en articulant clairement pour qui l'offre est faite, quelle valeur distinctive elle crée, et pourquoi les clients devraient la préférer.",
  {
    "positioning_statement_structure": "Pour [client cible] qui [besoin/problème], [nom du produit] est [catégorie] qui [bénéfice clé]. Contrairement à [concurrent principal], notre produit [différenciateur clé].",
    "differentiation_types": [
      {"type": "Prix", "description": "Moins cher pour une qualité comparable — fragile si non couplé à une structure de coûts différente"},
      {"type": "Qualité/Performance", "description": "Mieux sur la dimension qui compte le plus pour le segment visé"},
      {"type": "Commodité", "description": "Plus facile, plus rapide, moins d'effort — différenciateur fort dans les marchés où la friction est élevée"},
      {"type": "Spécialisation", "description": "Expert du segment vertical vs généraliste — meilleur fit sur un sous-marché"},
      {"type": "Relation", "description": "Service, accompagnement, relation — difficile à scaler mais très défendable"}
    ],
    "porter_five_forces": [
      "Menace de nouveaux entrants (barrières à l'entrée)",
      "Pouvoir de négociation des clients",
      "Pouvoir de négociation des fournisseurs",
      "Menace des substituts",
      "Intensité concurrentielle dans le secteur"
    ]
  },
  [
    {"prompt": "Comment se positionner sur un marché avec des concurrents établis et mieux financés ?", "answer": "Niche d'abord. Ne pas attaquer frontalement — chercher le segment que les grands acteurs servent mal ou pas du tout (contraintes de taille : les grands ne peuvent pas aller sur des marchés trop petits). Porter le message vers ce segment avec une précision maximum. Objectif : être la référence incontestée pour ce segment avant d'élargir. L'histoire de disruption classique (Clayton Christensen) : commencer en bas de marché ou sur un segment négligé, puis remonter."},
    {"prompt": "Comment vérifier que notre positionnement est perçu comme différenciant par les clients ?", "answer": "Test d'entretien : demander aux clients (existants et potentiels) 'pourquoi vous nous avez choisi plutôt que X ?' et 'qu'est-ce qui vous ferait partir vers un concurrent ?' Si les réponses ne correspondent pas à votre positionnement déclaré → il y a un gap. Compléter avec l'analyse des deals perdus : pourquoi les prospects qui ont choisi un concurrent l'ont-ils fait ? Les raisons réelles de perte révèlent le positionnement perçu vs souhaité."}
  ],
  ["positionnement", "concurrence", "différenciation", "Porter", "avantage compétitif"]
))

save("cpl/business_strategy/b2b_sales_cycle.json", ku_bs(
  "b2b_sales_cycle",
  "Cycle de vente B2B",
  "La vente B2B est un processus structuré en étapes — de la prospection au closing — avec de multiples parties prenantes, des cycles longs (3-18 mois) et des enjeux élevés. Chaque étape a ses techniques et ses KPIs spécifiques.",
  "Le cycle de vente B2B est le processus structuré par lequel une entreprise identifie des prospects, qualifie leur intérêt et leur capacité d'achat, propose une solution adaptée, négocie les conditions et close la transaction, souvent avec plusieurs interlocuteurs et sur des cycles de plusieurs mois.",
  {
    "sales_stages": [
      {"stage": "Prospection", "activities": ["Cold outreach", "Inbound qualification", "Referrals"], "exit_criteria": "Contact établi avec un décideur ou influenceur"},
      {"stage": "Qualification", "activities": ["Discovery call", "Qualification BANT/MEDDIC"], "exit_criteria": "Budget, Autorité, Besoin, Timing confirmés"},
      {"stage": "Découverte", "activities": ["Demo", "Questions approfondies", "Identification des enjeux"], "exit_criteria": "Pain points documentés, champion interne identifié"},
      {"stage": "Proposition", "activities": ["Rédaction offre", "Proof of Concept", "Validation technique"], "exit_criteria": "Offre présentée et reçue positivement"},
      {"stage": "Négociation", "activities": ["Révisions commerciales", "Legal review", "Mise en concurrence"], "exit_criteria": "Accord sur les termes principaux"},
      {"stage": "Closing", "activities": ["Signature", "PO", "KickOff"], "exit_criteria": "Contrat signé et premier versement reçu"}
    ],
    "qualification_frameworks": [
      {"framework": "BANT", "criteria": "Budget, Authority, Need, Timing — qualification rapide en discovery"},
      {"framework": "MEDDIC", "criteria": "Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion — rigoureux pour les grands comptes"},
      {"framework": "SPIN", "criteria": "Situation, Problem, Implication, Need-payoff — technique de questionnement pour révéler les besoins"}
    ]
  },
  [
    {"prompt": "Comment réduire la durée de mon cycle de vente B2B ?", "answer": "Cinq leviers : (1) Qualifier mieux en amont — ne poursuivre que les leads qui ont budget + autorité + besoin + timing alignés. (2) Identifier le champion interne tôt — la personne qui pousse le deal de l'intérieur. (3) Proposer un POC ou pilote payant plutôt qu'un essai gratuit — engage le prospect. (4) Cartographier le processus de décision (qui signe, qui approuve, qui peut bloquer) et adresser chaque partie prenante. (5) Business case chiffré — les deals qui avancent vite ont une justification ROI claire."},
    {"prompt": "Comment gérer un prospect qui dit 'c'est intéressant mais pas maintenant' ?", "answer": "Distinguer le 'pas maintenant' réel du 'non poli'. Questions utiles : 'Qu'est-ce qui doit se passer pour que ça devienne une priorité ?' et 'Quel est l'événement ou la date qui changerait votre timing ?' Si une réponse concrète émerge (budget Q1, fin de contrat existant en mars), c'est un 'pas maintenant' réel — mettre un rappel et reprendre le contact avant cette date. Si la réponse est vague → probabilité de closing faible, à dés-prioriser."}
  ],
  ["vente B2B", "cycle de vente", "BANT", "MEDDIC", "closing"]
))

save("cpl/business_strategy/business_scaling_strategy.json", ku_bs(
  "business_scaling_strategy",
  "Stratégie de scaling business",
  "Le scaling consiste à croître le revenu plus vite que les coûts. Cela requiert d'identifier les leviers de scalabilité (product, sales, marketing), d'automatiser les processus, et de bâtir la structure organisationnelle avant d'en avoir besoin.",
  "La stratégie de scaling est l'ensemble des décisions qui permettent à une entreprise de multiplier son revenu et son impact sans multiplier proportionnellement ses ressources — en identifiant les leviers de croissance non-linéaire, en automatisant les processus répétitifs et en construisant les capacités organisationnelles nécessaires.",
  {
    "scaling_prerequisites": [
      "Product-Market Fit établi — ne pas scaler avant que la rétention soit prouvée",
      "Unit economics positives — CAC < LTV, idéalement LTV/CAC > 3",
      "Processus de vente reproductible — le succès ne dépend pas d'une seule personne",
      "Infrastructure scalable — technique, RH, finance"
    ],
    "scaling_levers": [
      {"lever": "Sales scaling", "methods": ["Embauche et formation de commerciaux", "Channel partnerships", "Alliances"], "constraint": "Chaque commercial nécessite 6-12 mois pour être productif"},
      {"lever": "Marketing scaling", "methods": ["SEO/content", "Paid acquisition", "Growth loops viraux"], "constraint": "ROI variable et souvent long terme"},
      {"lever": "Product scaling (PLG)", "methods": ["Freemium", "Self-serve", "Intégrations"], "constraint": "Nécessite un produit très 'self-service'"},
      {"lever": "Partnership/Channel", "methods": ["Revendeurs", "Intégrateurs", "API partenaires"], "constraint": "Perte de contrôle sur l'expérience client"}
    ],
    "scaling_traps": [
      "Scaler les ventes avant d'avoir un produit stable — génère du churn",
      "Embaucher trop vite — la complexité organisationnelle ralentit l'exécution",
      "Perdre la qualité produit dans la course à la croissance",
      "Ignorer la profitabilité unitaire — croissance sans marge est de la croissance de valeur détruite"
    ]
  },
  [
    {"prompt": "Comment savoir si on est prêts à scaler ?", "answer": "Checklist : (1) La rétention est stable (courbe aplatie, pas de descente continue), (2) Les unit economics sont positives (LTV/CAC > 3, payback period < 18 mois), (3) Le processus de vente est reproductible (un nouveau commercial peut apprendre et performer avec un playbook), (4) Le produit supporte la montée en charge (infrastructure, support), (5) L'équipe de direction peut déléguer les décisions opérationnelles. Si tous ces points sont 'oui' → ready to scale. Sinon : identifier et corriger d'abord."},
    {"prompt": "Comment scaler sans perdre la qualité de service qui a fait notre succès ?", "answer": "La qualité à l'échelle nécessite de codifier ce qui fait le succès : playbooks, standards de qualité, processus de formation. Trois pratiques : (1) Documenter systématiquement les cas réussis (qu'est-ce qui a créé cette satisfaction ?) avant de scaler, (2) Mesurer la qualité à chaque étape (NPS par cohorte, CSAT par commercial, tickets résolus au premier contact), (3) Investir en Customer Success avant le support — accompagnement proactif > support réactif. Le secret : la qualité ne se maintient pas spontanément à l'échelle — elle se construit délibérément."}
  ],
  ["scaling", "croissance", "PMF", "unit economics", "organisation"]
))

save("cpl/business_strategy/consulting_delivery_model.json", ku_bs(
  "consulting_delivery_model",
  "Modèle de delivery en conseil",
  "Le modèle de delivery en conseil définit comment la valeur est livrée au client — diagnostics, recommandations, implémentation ou accompagnement. Le choix du modèle détermine la scalabilité, les marges et le type de relation client.",
  "Le modèle de delivery en conseil est la structure par laquelle une entreprise de conseil organise et livre ses services à ses clients, incluant la méthodologie (diagnostic/recommandation/implémentation), la structure des équipes, le format des livrables et le mode de facturation.",
  {
    "delivery_models": [
      {"model": "Conseil pur (advisory)", "description": "Diagnostics, recommandations, livrables documentés", "pros": ["Marges élevées", "Scalable (plusieurs clients par consultant)"], "cons": ["Mise en oeuvre hors scope — risque de déconnexion entre recommandation et réalité"]},
      {"model": "Accompagnement (coaching)", "description": "Travail aux côtés du client sur sa problématique, transfert de compétences", "pros": ["Fort impact durable", "Relation longue"], "cons": ["Moins scalable", "Dépendance au consultant"]},
      {"model": "Implémentation", "description": "Le consultant implémente la solution (IT, RH, processus)", "pros": ["Valeur tangible et mesurable", "Moins de risque de résistance"], "cons": ["Coûts élevés", "Risque de dépassement de budget"]},
      {"model": "Productisation", "description": "Packaging de la méthodologie en produit ou programme", "pros": ["Scalable", "Marges élevées à terme"], "cons": ["Investissement initial de création de contenu"]}
    ],
    "delivery_quality": [
      "Clarté du scope (périmètre défini contractuellement)",
      "Points de contact réguliers avec le client (status hebdo, revues mensuelles)",
      "Gestion des attentes (underpromise, overdeliver)",
      "Feedback client intégré (pas de livrables en chambre noire)"
    ]
  },
  [
    {"prompt": "Comment choisir entre conseil pur et accompagnement pour mes clients ?", "answer": "Dépend du besoin client : conseil pur si le client a besoin d'une expertise externe pour prendre une décision (diagnostic d'un problème, choix stratégique), accompagnement si le client a besoin de monter en compétence ou de changer ses façons de faire (transformation, adoption d'outils). En pratique : les deux se combinent souvent. La question clé à poser en avant-vente : 'Votre équipe a-t-elle la capacité d'implémenter une fois que vous aurez les recommandations ?' Si non → accompagnement ou implémentation."},
    {"prompt": "Comment éviter le scope creep dans un projet de conseil ?", "answer": "Trois règles : (1) Scope contractuellement défini avec des livrables précis et des critères d'acceptation, (2) Processus formel de demande de changement (change request) avec impact sur le budget et le délai — documenté et signé, (3) Review mensuelle du scope avec le client — vérifier qu'on est alignés sur ce qui est dans / hors périmètre. Le scope creep naît souvent de l'ambiguïté initiale — investir dans la définition du scope en avant-vente est le ROI le plus élevé d'un projet de conseil."}
  ],
  ["conseil", "delivery", "accompagnement", "scope", "consulting"]
))

save("cpl/business_strategy/client_relationship_governance.json", ku_bs(
  "client_relationship_governance",
  "Gouvernance de la relation client",
  "La gouvernance de la relation client structure les interactions, escalades et revues entre une entreprise et ses clients stratégiques — prévenant les crises relationnelles et créant les conditions du renouvellement et de l'expansion.",
  "La gouvernance de la relation client est l'ensemble des processus, rituels et mécanismes d'escalade qui structurent la relation entre un prestataire et ses clients, assurant l'alignement sur les objectifs, la résolution proactive des problèmes et la création de valeur long terme.",
  {
    "governance_rituals": [
      {"ritual": "Réunion opérationnelle", "frequency": "Hebdomadaire ou bimensuelle", "participants": "PM client + PM prestataire", "agenda": "Avancement, bloquants, prochaines étapes"},
      {"ritual": "Revue mensuelle", "frequency": "Mensuelle", "participants": "Équipes opérationnelles + managers", "agenda": "Métriques, incidents, ajustements de plan"},
      {"ritual": "Business Review trimestrielle (QBR)", "frequency": "Trimestrielle", "participants": "Direction + stakeholders clés", "agenda": "ROI réalisé, prochaines priorités, satisfaction, renouvellement"},
      {"ritual": "Revue annuelle stratégique", "frequency": "Annuelle", "participants": "C-level", "agenda": "Vision long terme, plan à 12 mois, investissements"}
    ],
    "account_health_signals": [
      "Engagement dans les rituels (participent-ils aux reviews ?)",
      "Usage produit (vs période précédente)",
      "NPS ou satisfaction déclarée",
      "Nombre de contacts actifs dans le compte",
      "Incidents non résolus",
      "Signaux d'expansion ou de réduction de scope"
    ]
  },
  [
    {"prompt": "Comment détecter qu'un compte client est en risque avant qu'il ne churne ?", "answer": "Signaux d'alerte précoces : (1) Participation aux rituels en baisse (no-shows aux reviews), (2) Usage produit qui stagne ou baisse, (3) Réponses lentes aux communications, (4) Contacts internes qui changent ou ne répondent plus, (5) Questions sur les alternatives ou sur les conditions de résiliation, (6) Escalades répétées non résolues. Un outil : un score de santé compte automatisé combinant ces signaux — dès que le score descend sous un seuil, intervention proactive."},
    {"prompt": "Comment conduire une QBR (Quarterly Business Review) efficace ?", "answer": "Structure QBR : (1) Résumé exécutif de la valeur créée dans le trimestre (en termes business, pas techniques), (2) Métriques vs objectifs définis en début de trimestre, (3) Incidents et résolutions (et plan pour éviter les récurrences), (4) Priorités et investissements du trimestre à venir, (5) Feedback client ouvert. Durée : 60-90 min max. Règle : la QBR ne devrait jamais contenir de surprises — les mauvaises nouvelles sont annoncées avant, pas pendant."}
  ],
  ["relation client", "gouvernance", "QBR", "rétention", "account management"]
))

print("\nBatch 10 PM/Advanced (15) + cpl/business_strategy (10) : DONE")
