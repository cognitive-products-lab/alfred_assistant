"""
Enrichissement day3 — product_management/advanced stubs (9 KU)
Remplace les stubs _meta par de vrais KU schema v1.2 validés.
"""
import json
from pathlib import Path
from datetime import date

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
TODAY = date.today().isoformat()

def meta():
    return {"created_at": TODAY, "validated_at": TODAY,
            "validated_by": "ALFRED enrichment pipeline",
            "enrichment_version": "day3", "schema_version": "1.2",
            "review_notes": "", "block": "b18"}

def save(path, data):
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(id_, title, priority, summary, core_def, knowledge, examples, guidance, tags):
    return {"schema_version": "1.2", "type": "knowledge_unit", "id": id_, "title": title,
            "domain": "professional", "subdomain": "product_management_advanced",
            "status": "validated", "metadata": meta(), "priority": priority,
            "summary": summary, "core_definition": core_def, "knowledge": knowledge,
            "example_answers": examples, "response_guidance": guidance,
            "tags": tags, "related_knowledge_units": []}

# 1 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/opportunity_solution_tree.json", ku(
    "knowledges.professional.product_management.advanced.opportunity_solution_tree",
    "Opportunity Solution Tree — relier découverte et delivery",
    "high",
    "Framework de Teresa Torres qui relie visuellement l'outcome visé, les opportunités utilisateurs, les solutions potentielles et les expériences à mener — évite le feature factory.",
    "L'Opportunity Solution Tree (OST) est un arbre de décision visuel qui part d'un outcome business désiré, identifie les opportunités (besoins, pain points, désirs utilisateurs) qui y contribuent, génère des solutions pour chaque opportunité, et planifie les expériences pour les valider avant de les construire.",
    {"structure": {
        "niveau_1": "Outcome désiré (ex : augmenter la rétention J30 de 20%)",
        "niveau_2": "Opportunités — besoins et friction utilisateurs qui bloquent l'outcome",
        "niveau_3": "Solutions — idées pour résoudre chaque opportunité",
        "niveau_4": "Expériences — tests rapides pour valider les solutions avant de les développer"
     },
     "pourquoi_utile": "Empêche de sauter directement aux solutions sans comprendre les opportunités. Rend visibles les hypothèses implicites. Structure la continuous discovery.",
     "construction": [
        "1. Définir l'outcome avec le business (OKR ou North Star)",
        "2. Mener des interviews régulières pour identifier les opportunités",
        "3. Générer plusieurs solutions par opportunité (pas une seule)",
        "4. Prioriser les expériences à mener selon impact × confiance × effort"
     ],
     "erreurs_frequentes": [
        "Mettre des features à la place des opportunités",
        "Un seul chemin de l'outcome à la solution (pas un arbre)",
        "Sauter les expériences pour aller directement au développement"
     ]},
    [{"prompt": "Comment construire un Opportunity Solution Tree pour mon produit ?",
      "answer": "Partir de l'outcome que ton équipe cherche à atteindre ce trimestre (pas une feature, un résultat mesurable). Ensuite, lister les opportunités que tu as découvertes en interviews : quels besoins non satisfaits, quelles frictions, quels moments de satisfaction qu'on pourrait amplifier ? Pour chaque opportunité, générer 3+ idées de solution — la diversité est importante. Enfin, pour chaque solution prometteuse, définir l'expérience la plus rapide qui te donnera de la confiance avant de construire."},
     {"prompt": "Quelle différence entre une opportunité et une solution dans un OST ?",
      "answer": "Une opportunité c'est un besoin, une friction ou un désir utilisateur — formulé du point de vue de l'utilisateur (\"les utilisateurs abandonnent à l'étape de configuration parce qu'elle est trop complexe\"). Une solution c'est ce qu'on construit pour y répondre — formulé du point de vue du produit (\"assistant de configuration en 3 étapes avec valeurs par défaut intelligentes\"). L'OST force à distinguer les deux — on peut avoir plusieurs solutions pour une même opportunité."}],
    {"tone": "product management, Teresa Torres, orienté pratique",
     "structure": ["structure de l'arbre", "construction", "erreurs"],
     "avoid": ["confondre feature et opportunité", "présenter comme une solution magique"]},
    ["OST", "opportunity solution tree", "Teresa Torres", "discovery", "product management", "continuous discovery"]
))

# 2 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/outcome_driven_product.json", ku(
    "knowledges.professional.product_management.advanced.outcome_driven_product",
    "Outcome-Driven Product — piloter par les résultats, pas les features",
    "high",
    "Approche de product management qui mesure le succès à l'aune des changements de comportement utilisateur (outcomes) plutôt que du volume de features livrées.",
    "L'approche Outcome-Driven Product consiste à définir le succès d'un produit par les changements mesurables dans le comportement ou la situation des utilisateurs (outcomes) plutôt que par la quantité de fonctionnalités développées (outputs), en responsabilisant les équipes sur les résultats et non sur les livrables.",
    {"concepts": {
        "output": "Ce qu'on produit (features, pages, API endpoints) — mesurable mais pas suffisant",
        "outcome": "Changement de comportement ou de situation chez l'utilisateur (rétention, engagement, succès tâche)",
        "impact": "Résultat business final (CA, parts de marché, NPS)"
     },
     "chaine_logique": "Output → Outcome → Impact — la majorité des PM mesurent les outputs, le but est de mesurer les outcomes",
     "comment_definir_un_outcome": [
        "\"Quel changement de comportement utilisateur cherchons-nous ?\"",
        "\"Comment saurons-nous que nous avons réussi sans regarder nos livrables ?\"",
        "Doit être mesurable, atteignable par l'équipe, centré utilisateur"
     ],
     "organisation": "Les équipes outcome-driven reçoivent un problème à résoudre, pas une liste de features à livrer — elles ont l'autonomie de trouver la meilleure solution",
     "reference": "Josh Seiden 'Outcomes Over Output' — manifeste de cette approche"},
    [{"prompt": "Notre équipe livre beaucoup mais l'impact est faible. Pourquoi ?",
      "answer": "Symptôme classique du feature factory : on livre des outputs (fonctionnalités) sans mesurer si elles génèrent les outcomes voulus (changements de comportement utilisateur). Trois questions à poser à chaque feature livrée : quel comportement utilisateur devrait changer ? comment on mesure ce changement ? est-ce que le changement a eu lieu ? Si l'équipe ne peut pas répondre aux deux premières questions avant de livrer, le problème est structurel."},
     {"prompt": "Comment donner un outcome à mon équipe plutôt qu'une liste de features ?",
      "answer": "Format : \"Nous croyons que si nous [réduisons la friction à l'onboarding], nous observerons [une augmentation de l'activation J1 de X à Y]. Nous saurons avoir réussi quand [la métrique atteint Y pendant 4 semaines].\" C'est une hypothesis-driven roadmap. L'équipe est responsable de l'outcome — elle choisit les solutions pour y arriver. Ça nécessite de la confiance dans l'équipe et de la clarté sur les métriques."}],
    {"tone": "product management, orienté transformation organisationnelle",
     "structure": ["concepts", "chaîne logique", "définir un outcome", "organisation"],
     "avoid": ["opposer output et outcome de façon manichéenne", "ignorer la difficulté du changement culturel"]},
    ["outcome", "output", "product management", "feature factory", "résultats", "Josh Seiden"]
))

# 3 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/problem_space_analysis.json", ku(
    "knowledges.professional.product_management.advanced.problem_space_analysis",
    "Analyse de l'espace problème — comprendre avant de résoudre",
    "high",
    "Méthodes pour explorer et structurer l'espace problème avant de générer des solutions : interviews, cartographie des pains, définition du problème central et critères de succès.",
    "L'analyse de l'espace problème est la phase de compréhension profonde du problème à résoudre avant toute génération de solution, visant à éviter de résoudre le mauvais problème ou une version superficielle du problème réel.",
    {"outils": {
        "interviews_utilisateurs": "Comprendre le contexte, les comportements actuels, les frustrations réelles — pas les solutions souhaitées",
        "5_pourquoi": "Remonter la chaîne causale pour trouver la cause racine du problème",
        "jobs_to_be_done": "\"Quand [situation], j'essaie de [progression], mais [obstacle]\" — cadrer le vrai job",
        "problem_statement": "\"[Utilisateur] a du mal à [X] parce que [Y], ce qui entraîne [Z]\" — formaliser le problème"
     },
     "questions_a_poser": [
        "Pour qui est-ce un problème (qui le ressent le plus fort) ?",
        "Dans quelle situation le problème se manifeste-t-il ?",
        "Quelles solutions de contournement existent déjà (signal que le problème est réel) ?",
        "Quel serait l'impact si le problème était résolu ?"
     ],
     "separration_problem_solution": "Rester dans l'espace problème le plus longtemps possible avant de générer des solutions — les équipes tendent à sauter aux solutions après 5 minutes de description du problème",
     "livrable": "Problem brief : définition du problème validée, segment cible, métriques de succès, périmètre hors-scope"},
    [{"prompt": "Comment s'assurer qu'on résout le bon problème ?",
      "answer": "Trois disciplines : 1) Interviews sans mention de solutions — demander à l'utilisateur de décrire sa situation, ses comportements actuels, ses workarounds. La solution se cache dans les workarounds. 2) Les 5 pourquoi sur chaque symptôme identifié — descendre jusqu'à la cause racine. 3) Valider le problem statement avec des utilisateurs avant de passer aux solutions : \"Est-ce que cette formulation décrit bien votre problème ?\" Si non, recommencer."},
     {"prompt": "Qu'est-ce qu'un bon problem statement ?",
      "answer": "Structure : \"[Segment utilisateur précis] a du mal à [tâche ou objectif spécifique] dans [contexte] parce que [cause racine], ce qui entraîne [impact mesurable].\" Bon indicateur : le problem statement dit ce qu'on cherche à résoudre sans dicter la solution. Si en lisant le problem statement une seule solution vient à l'esprit, il est trop contraint. Il devrait ouvrir plusieurs chemins possibles."}],
    {"tone": "discovery, orienté rigueur méthodologique",
     "structure": ["outils", "questions", "séparation problem/solution", "livrable"],
     "avoid": ["prescrire les solutions", "sous-estimer le temps nécessaire à l'exploration"]},
    ["espace problème", "problem statement", "discovery", "interviews", "5 pourquoi", "JTBD"]
))

# 4 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/product_discovery_advanced.json", ku(
    "knowledges.professional.product_management.advanced.product_discovery_advanced",
    "Product Discovery avancée — techniques et cadences de découverte continue",
    "high",
    "Pratiques avancées de discovery produit : continuous discovery, tests d'hypothèses, prototype testing, assumption mapping et integration dans les sprints agiles.",
    "La product discovery avancée désigne les pratiques structurées qui permettent à une équipe de réduire systématiquement l'incertitude sur ce qu'il faut construire — en testant des hypothèses avec de vraies données utilisateurs avant d'investir en développement.",
    {"cadence": {
        "weekly_interviews": "Au moins un entretien utilisateur par semaine — Teresa Torres recommande 1 par PM par semaine",
        "assumption_mapping": "Cartographier les hypothèses selon leur importance et leur incertitude",
        "experiment_backlog": "Backlog d'expériences parallèle au backlog de développement",
        "learning_review": "Rituel hebdomadaire ou bi-mensuel : qu'a-t-on appris, comment ça change nos priorités"
     },
     "techniques": {
        "prototype_papier": "Tester une idée en 2h avec un prototype basse fidélité avant de coder",
        "fake_door": "Tester la demande avec un bouton ou une page qui n'existe pas encore",
        "concierge": "Simuler manuellement la feature pour valider avant d'automatiser",
        "smoke_test": "Landing page + pré-inscription pour mesurer l'intérêt avant développement"
     },
     "integration_agile": {
        "dual_track": "Track discovery (validation) parallèle au track delivery (développement)",
        "sprint_0": "Sprint dédié discovery avant chaque cycle de delivery",
        "story_hypothesis": "Chaque user story inclut l'hypothèse qu'elle teste et la métrique de validation"
     },
     "metriques_discovery": "Vélocité discovery : nombre d'hypothèses testées par semaine. Taux d'invalidation cible : 50-70% — si toutes les hypothèses sont validées, les tests ne sont pas assez challengeants"},
    [{"prompt": "Comment faire de la continuous discovery sans dédier une équipe entière à la recherche ?",
      "answer": "Commencer petit : un entretien utilisateur de 30 min par semaine par PM. C'est faisable même dans une petite équipe. Rituel : noter les insights dans un outil partagé (Notion, FigJam), partager le top 3 learnings de la semaine lors du daily ou standup. L'objectif n'est pas la recherche exhaustive — c'est de maintenir un contact régulier avec les utilisateurs réels pour éviter de construire dans le vide."},
     {"prompt": "Comment tester une idée de feature sans la développer ?",
      "answer": "Par ordre de coût croissant : 1) Prototype papier ou Figma cliquable — 2h de travail, testé avec 5 utilisateurs. 2) Wizard of Oz — simuler manuellement ce que la feature ferait. 3) Fake door — ajouter le bouton dans l'interface et mesurer les clics avant de construire la page. 4) Smoke test — landing page dédiée avec CTA \"intéressé\" pour mesurer la demande. La règle : valider avec le test le moins cher possible."}],
    {"tone": "pratique, Teresa Torres, Marty Cagan",
     "structure": ["cadence", "techniques", "intégration agile", "métriques"],
     "avoid": ["confondre discovery et research académique", "présenter comme nécessitant un budget énorme"]},
    ["continuous discovery", "product discovery", "hypothèses", "prototype", "Teresa Torres", "agile", "dual track"]
))

# 5 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/product_operating_model_advanced.json", ku(
    "knowledges.professional.product_management.advanced.product_operating_model_advanced",
    "Product Operating Model avancé — structurer une organisation produit",
    "medium",
    "Comment structurer une organisation produit efficace : modèles d'équipe (squads, tribes, guilds), interfaces avec le business, rôles et responsabilités, et évolution selon la taille.",
    "Le Product Operating Model (POM) avancé désigne le système organisationnel complet qui définit comment une organisation crée de la valeur produit : structure des équipes, interfaces avec les fonctions, processus de décision, rituels de coordination et mécanismes d'alignement stratégique.",
    {"modeles_equipes": {
        "squad": "Equipe pluridisciplinaire autonome (PM + design + dev) responsable d'un domaine produit",
        "tribe": "Regroupement de squads partageant un domaine business (ex : acquisition, rétention)",
        "chapter": "Regroupement fonctionnel des mêmes métiers à travers les squads (guild design, guild data)",
        "guild": "Communauté de pratique volontaire et transverse — partage de compétences"
     },
     "interfaces_business": {
        "pm_business": "Le PM traduit les objectifs business en outcomes produit — pas un order taker",
        "engineering": "Le PM et le tech lead co-propriétaires du backlog technique et produit",
        "design": "Embedded in squads — pas un service central qui reçoit des tickets"
     },
     "evolution_par_taille": {
        "1_10_personnes": "Pas besoin de structure formelle — une équipe, un PM, communication directe",
        "10_50": "Squads par domaine fonctionnel, tribe optionnelle, quelques guilds",
        "50_200": "Tribes + squads + chapters nécessaires pour éviter le chaos de coordination",
        "200_plus": "POM complet avec stream-aligned teams, platform teams, enabling teams (Team Topologies)"
     },
     "reference": "Spotify Model (squads/tribes/chapters/guilds) + Team Topologies (Skelton & Pais)"},
    [{"prompt": "Comment structurer notre équipe produit qui grossit vite ?",
      "answer": "La règle de Jeff Bezos : une équipe doit pouvoir être nourrie avec deux pizzas (6-8 personnes). Au-delà, la communication devient trop coûteuse. Structurer par domaine de valeur (pas par composant technique) : une squad responsable de l'acquisition, une de l'activation, une de la rétention. Chaque squad a son PM, son designer, ses devs — et une métrique dont elle est responsable. Les guilds gèrent les bonnes pratiques transverses."},
     {"prompt": "C'est quoi le Spotify Model et faut-il l'adopter ?",
      "answer": "Le Spotify Model (squads, tribes, chapters, guilds) a été publié en 2012 — et Spotify lui-même a évolué depuis. C'est une source d'inspiration utile, pas un blueprint à copier. Les principes qui tiennent : autonomie des équipes sur leur domaine, communautés de pratique pour partager l'expertise, ownership clair. Ce qui marche moins bien si copié bêtement : la structure ne remplace pas la culture — l'autonomie sans confiance donne du chaos."}],
    {"tone": "organisationnel, pragmatique, nuancé sur le Spotify Model",
     "structure": ["modèles d'équipes", "interfaces", "évolution", "références"],
     "avoid": ["présenter le Spotify Model comme universel", "ignorer les petites équipes"]},
    ["product operating model", "squads", "tribes", "Spotify Model", "Team Topologies", "organisation produit"]
))

# 6 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/roadmap_tradeoffs.json", ku(
    "knowledges.professional.product_management.advanced.roadmap_tradeoffs",
    "Arbitrages de roadmap — naviguer les tensions stratégiques",
    "high",
    "Comment arbitrer les tensions inévitables d'une roadmap produit : court terme vs long terme, dette technique vs nouvelles features, large vs niche, customer requests vs vision.",
    "Les arbitrages de roadmap sont les décisions difficiles qui définissent ce qu'on construit (et ce qu'on ne construit pas), en naviguant des tensions structurelles entre des priorités légitimes qui s'excluent mutuellement dans un horizon de temps donné.",
    {"tensions_classiques": {
        "court_long_terme": "Quick wins pour les clients actuels vs investissements pour la croissance future",
        "dette_features": "Rembourser la dette technique vs livrer de nouvelles fonctionnalités",
        "retention_acquisition": "Améliorer l'expérience des utilisateurs existants vs acquérir de nouveaux",
        "customer_requests_vision": "Demandes explicites des clients vs direction stratégique de l'équipe",
        "large_niche": "Servir le cas général vs les besoins spécialisés d'un segment à haute valeur"
     },
     "frameworks_arbitrage": {
        "ICE": "Impact × Confidence × Ease — quick scoring pour filtrer",
        "RICE": "Reach × Impact × Confidence / Effort — plus rigoureux",
        "now_next_later": "Horizon temporel simple — réduire la fausse précision du trimestre"
     },
     "processus_sain": [
        "Rendre les arbitrages explicites — les lister, pas les cacher",
        "Documenter ce qu'on ne fait PAS et pourquoi",
        "Revisiter les arbitrages quand le contexte change (nouvelles données, churn inattendu)"
     ],
     "communication": "Un arbitrage bien communiqué est aussi important que la décision elle-même — les stakeholders acceptent mieux un non expliqué qu'un non opaque"},
    [{"prompt": "Les clients demandent des features, la direction veut de l'innovation. Comment arbitrer ?",
      "answer": "Cadre en trois buckets : 30% requests clients (rétention, satisfaction), 30% réduction dette et efficience, 40% innovation et vision. Ajuster selon la phase : early growth → plus de requests pour valider PMF, mature → plus d'innovation pour la différenciation. Le plus important : communiquer explicitement le ratio choisi aux deux parties et le justifier avec des métriques (churn, NPS, pipeline)."},
     {"prompt": "On accumule de la dette technique mais on n'a jamais le temps de la résorber.",
      "answer": "Sans budget explicite pour la dette, elle ne sera jamais prioritaire face à de nouvelles features. Solution : réserver un pourcentage fixe du capacity (20% est commun) pour la dette technique chaque sprint — non-négociable. Présenter la dette au business non comme un choix technique mais comme un risque business : \"Sans ce travail, notre vélocité va baisser de X% dans 6 mois et le coût de chaque feature augmentera.\""}],
    {"tone": "stratégique, orienté décision et communication",
     "structure": ["tensions", "frameworks", "processus", "communication"],
     "avoid": ["recettes universelles", "ignorer la dimension stakeholder"]},
    ["roadmap", "arbitrage", "priorisation", "dette technique", "product management", "tension stratégique"]
))

# 7 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/service_blueprinting.json", ku(
    "knowledges.professional.product_management.advanced.service_blueprinting",
    "Service Blueprinting — cartographier l'expérience de service bout en bout",
    "medium",
    "Outil UX et service design pour visualiser l'expérience utilisateur (frontstage) et les processus internes (backstage) qui la soutiennent — révèle les points de friction invisibles.",
    "Le Service Blueprint est un outil de visualisation qui cartographie simultanément l'expérience de l'utilisateur (actions, touchpoints, émotions) et les processus internes de l'organisation qui la soutiennent (actions visibles du personnel, backstage, systèmes de support), révélant les décalages entre l'expérience voulue et l'expérience réelle.",
    {"couches": {
        "customer_actions": "Ce que fait le client à chaque étape du parcours",
        "frontstage": "Interactions visibles entre le client et le service (personnel, interfaces)",
        "line_of_visibility": "Frontière entre ce que voit le client et ce qui se passe en coulisses",
        "backstage": "Processus internes non visibles du client (logistique, systèmes)",
        "support_processes": "Systèmes et partenaires qui soutiennent le backstage"
     },
     "quand_utiliser": [
        "Diagnostiquer des points de friction dans un service existant",
        "Concevoir un nouveau service de bout en bout",
        "Aligner les équipes front et back sur l'expérience cible",
        "Identifier les opportunités d'automatisation ou d'amélioration"
     ],
     "vs_customer_journey_map": "CJM = centré sur l'expérience client uniquement. Service Blueprint = CJM + processus internes. Le blueprint révèle pourquoi l'expérience est ce qu'elle est, pas seulement ce qu'elle est.",
     "construction": ["Définir le scope du service à cartographier", "Recruter 5-8 parties prenantes (front, back, IT, ops)", "Workshop de 3-4h pour co-construire", "Valider avec des utilisateurs réels"]},
    [{"prompt": "C'est quoi un Service Blueprint et quand l'utiliser ?",
      "answer": "C'est une carte qui montre simultanément ce que vit le client et ce qui se passe en coulisses pour produire cette expérience. L'utiliser quand : tu as une expérience qui fonctionne mal sans savoir pourquoi (le blueprint révèle les gaps entre front et back), tu conçois un nouveau service impliquant plusieurs équipes, ou tu veux aligner front et back sur une expérience cible commune. Ce n'est pas un outil quotidien — c'est un outil de transformation de service."},
     {"prompt": "Quelle différence entre une Customer Journey Map et un Service Blueprint ?",
      "answer": "La CJM documente l'expérience du client : ses actions, ses émotions, ses points de contact — du point de vue de l'utilisateur. Le Service Blueprint ajoute en dessous la ligne de visibilité : ce que font les agents (visible par le client), ce que font les équipes back-office (invisible), et les systèmes de support. La CJM dit \"voilà ce que vit le client\". Le blueprint dit aussi \"voilà pourquoi c'est comme ça\" — et où intervenir pour l'améliorer."}],
    {"tone": "service design, UX, orienté workshop",
     "structure": ["couches", "quand utiliser", "vs CJM", "construction"],
     "avoid": ["confondre avec une simple CJM", "sous-estimer la complexité du backstage"]},
    ["service blueprint", "service design", "UX", "journey map", "backstage", "frontstage", "processus"]
))

# 8 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/stakeholder_alignment.json", ku(
    "knowledges.professional.product_management.advanced.stakeholder_alignment",
    "Alignement des parties prenantes — construire le consensus sans perdre le cap",
    "high",
    "Techniques pour aligner des parties prenantes aux intérêts divergents sur une vision ou une décision produit, sans tomber dans le consensus mou ou la paralysie.",
    "L'alignement des parties prenantes en product management est le processus de construction d'une compréhension et d'un accord suffisants autour d'une direction produit, entre des acteurs aux priorités différentes, pour permettre l'exécution sans blocage ni sabotage.",
    {"types_de_stakeholders": {
        "decideurs": "Ceux qui peuvent bloquer ou accélérer — à aligner en priorité",
        "influenceurs": "Ceux qui forment l'opinion des décideurs — à informer régulièrement",
        "utilisateurs": "Ceux qui utilisent le produit — source de vérité sur les besoins",
        "executants": "Celles et ceux qui construisent — à impliquer dans la faisabilité"
     },
     "techniques": {
        "stakeholder_map": "Cartographier pouvoir × intérêt pour prioriser l'engagement",
        "pre_alignment": "Rencontrer les parties prenantes clés avant les grandes réunions — pas de surprises",
        "working_backwards": "Partir de l'outcome client final, descendre vers les implications — met tout le monde sur la même base",
        "desaccord_documente": "\"Disagree and commit\" — le désaccord est nommé et documenté, mais l'équipe avance"
     },
     "pieges": [
        "Chercher le consensus complet — paralyse et dilue la vision",
        "Aligner sans écouter — le faux consensus se retourne en cours d'exécution",
        "Aligner les personnes mais pas les objectifs — repousse le conflit"
     ],
     "communication_continue": "L'alignement n'est pas un événement — c'est un processus de communication régulier. Weekly updates, visibilité sur les décisions prises et leur rationale."},
    [{"prompt": "Un stakeholder clé bloque notre roadmap. Comment débloquer ?",
      "answer": "Avant la réunion de déblocage : comprendre son vrai souci (souvent différent de son objection formulée). Rencontrer en bilatéral : \"J'ai l'impression que tu as un souci avec [X]. Aide-moi à comprendre.\" Souvent c'est une crainte de risque, de perte de contrôle ou d'impact sur son équipe. Une fois le vrai souci nommé, on peut y répondre directement — ou documenter explicitement le désaccord et avancer quand même si la décision ne lui appartient pas."},
     {"prompt": "Comment présenter une décision difficile aux stakeholders sans se faire détruire ?",
      "answer": "Règle des \"no surprises\" : ne jamais annoncer une décision difficile à froid en réunion. Avant : identifier les 2-3 personnes les plus susceptibles de bloquer, les rencontrer individuellement, comprendre leurs objections, ajuster si pertinent. En réunion : annoncer avec contexte (pourquoi cette décision, quelles alternatives ont été évaluées, pourquoi cette option), nommer proactivement les objections prévisibles et y répondre. La résistance en réunion collective est souvent une surprise — elle doit être traitée avant."}],
    {"tone": "politique et pragmatique, orienté exécution",
     "structure": ["types de stakeholders", "techniques", "pièges", "communication"],
     "avoid": ["naïf sur le consensus", "ignorer les dynamiques de pouvoir"]},
    ["stakeholders", "alignement", "parties prenantes", "consensus", "product management", "communication"]
))

# 9 ─────────────────────────────────────────────────────
save("professional/product_management/advanced/wsjf_prioritization.json", ku(
    "knowledges.professional.product_management.advanced.wsjf_prioritization",
    "WSJF — Weighted Shortest Job First pour prioriser le backlog",
    "high",
    "Framework de priorisation SAFe basé sur la valeur économique : WSJF = Coût du Délai / Durée du Job — favorise les items à haute valeur et courte durée.",
    "Le WSJF (Weighted Shortest Job First) est un framework de priorisation issu du Lean et popularisé par SAFe, qui classe les items du backlog selon le ratio Coût du Délai / Taille du Job — priorisant les items qui combinent une forte valeur urgente avec un faible effort.",
    {"formule": "WSJF = Coût du Délai (CoD) / Durée du Job (effort relatif)",
     "composantes_cod": {
        "valeur_business": "Impact économique ou stratégique si livré — et si retardé",
        "time_criticality": "Est-ce que la valeur diminue avec le temps ? Y a-t-il une deadline ?",
        "risk_reduction": "Réduit-il un risque majeur ou une opportunité de se différencier ?"
     },
     "scoring": {
        "echelle": "Fibonacci (1, 2, 3, 5, 8, 13, 21) pour les composantes et l'effort",
        "relatif": "Les scores sont relatifs, pas absolus — comparer les items entre eux",
        "exemple": "CoD = 8+5+3 = 16, Effort = 4, WSJF = 16/4 = 4.0"
     },
     "quand_utiliser": [
        "Backlog PI Planning (SAFe)",
        "Arbitrage entre epics ou features en compétition",
        "Quand les décisions purement intuitives sont contestées — WSJF apporte un cadre objectivable"
     ],
     "limites": [
        "Les scores sont subjectifs malgré l'apparence de rigueur",
        "Complexe à maintenir sur un grand backlog",
        "Favorise les quick wins — peut négliger les investissements long terme"
     ]},
    [{"prompt": "Comment utiliser le WSJF pour prioriser mon backlog ?",
      "answer": "Processus en 4 étapes : 1) Lister les items à prioriser. 2) Pour chaque item, noter en relatif (Fibonacci) : valeur business, criticité temporelle, réduction de risque. Somme = Coût du Délai. 3) Estimer l'effort relatif en story points ou T-shirt sizing. 4) WSJF = CoD / Effort. Trier par WSJF décroissant. L'important : le scoring doit se faire en groupe avec les bonnes personnes (PM + tech + business), pas seul dans son coin."},
     {"prompt": "WSJF vs RICE — lequel choisir ?",
      "answer": "RICE (Reach × Impact × Confidence / Effort) est meilleur pour les produits B2C à large base utilisateurs où le reach est quantifiable. WSJF est meilleur dans un contexte Lean/SAFe, pour des epics et features à forte composante économique ou de risque, et dans des organisations qui utilisent déjà le PI Planning. Pour une startup early stage : ni l'un ni l'autre — le gut feeling guidé par les données utilisateurs est souvent plus rapide et aussi fiable."}],
    {"tone": "analytique, SAFe/Lean, orienté application",
     "structure": ["formule", "composantes", "scoring", "quand utiliser", "limites"],
     "avoid": ["présenter comme objectif alors que subjectif", "ignorer les alternatives"]},
    ["WSJF", "priorisation", "SAFe", "Lean", "coût du délai", "backlog", "product management"]
))

print("\n=== product_management/advanced stubs : 9 KU sauvegardés ===")
