"""
Enrichissement day4 — professional/strategy (12 KU)
Compléter les 3 KU existants avec les frameworks stratégiques essentiels.
"""
import json
from pathlib import Path
from datetime import date

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
TODAY = date.today().isoformat()

def meta():
    return {"created_at": TODAY, "validated_at": TODAY,
            "validated_by": "ALFRED enrichment pipeline",
            "enrichment_version": "day4", "schema_version": "1.2",
            "review_notes": "", "block": "b18"}

def save(path, data):
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(id_, title, priority, summary, core_def, knowledge, examples, guidance, tags):
    return {"schema_version": "1.2", "type": "knowledge_unit", "id": id_, "title": title,
            "domain": "professional", "subdomain": "strategy",
            "status": "validated", "metadata": meta(), "priority": priority,
            "summary": summary, "core_definition": core_def, "knowledge": knowledge,
            "example_answers": examples, "response_guidance": guidance,
            "tags": tags, "related_knowledge_units": []}

BASE = "professional/strategy"

# 1
save(f"{BASE}/analyse_swot_pestel.json", ku(
    "knowledges.professional.strategy.analyse_swot_pestel",
    "SWOT et PESTEL — analyser l'environnement stratégique",
    "high",
    "Deux outils complémentaires d'analyse stratégique : SWOT (interne + externe) et PESTEL (macro-environnement) — comment les utiliser ensemble et éviter leurs pièges.",
    "Le SWOT (Forces, Faiblesses, Opportunités, Menaces) et le PESTEL (Politique, Économique, Social, Technologique, Environnemental, Légal) sont des cadres d'analyse stratégique permettant de structurer la compréhension du contexte interne et externe d'une organisation.",
    {"swot": {
        "forces": "Avantages internes distinctifs vs la concurrence",
        "faiblesses": "Désavantages internes à corriger ou compenser",
        "opportunites": "Tendances ou événements externes à saisir",
        "menaces": "Forces externes qui peuvent nuire",
        "utilisation": "TOWS matrix : combiner SO (exploiter), ST (se protéger), WO (rattraper), WT (éviter)"
     },
     "pestel": {
        "usage": "Alimenter la partie externe du SWOT — scanner le macro-environnement avant de zoomer sur l'entreprise",
        "politique": "Régulations, stabilité, politique commerciale",
        "economique": "Croissance, inflation, taux, pouvoir d'achat",
        "social": "Démographie, valeurs, modes de vie",
        "technologique": "Innovation, disruption, digitalisation",
        "environnemental": "Climat, ressources, ESG",
        "legal": "Droit du travail, propriété intellectuelle, compliance"
     },
     "pieges": [
        "Lister sans prioriser — tout mettre dans chaque case sans identifier les éléments décisifs",
        "SWOT statique — prendre une photo sans dater ni actualiser",
        "Biais de confirmation — mettre ce qu'on veut voir plutôt que ce qui est"
     ]},
    [{"prompt": "Comment faire un SWOT utile et pas juste un exercice de remplissage ?",
      "answer": "Quatre règles : 1) Prioriser — garder les 3-5 éléments vraiment distinctifs par quadrant, pas une liste exhaustive. 2) Être honnête sur les faiblesses — les organisations tendent à les minimiser, ce qui rend le SWOT inutile. 3) Combiner avec une TOWS matrix : les croisements SO/ST/WO/WT génèrent les vraies pistes stratégiques. 4) Mettre une date et réviser régulièrement — un SWOT de 3 ans est souvent obsolète. Partir du PESTEL pour alimenter les Opportunités et Menaces : c'est plus rigoureux que de les inventer."},
     {"prompt": "C'est quoi la différence entre SWOT et PESTEL ?",
      "answer": "PESTEL analyse le macro-environnement externe (tendances politiques, économiques, sociales, technologiques, environnementales, légales) — ce sur quoi l'organisation n'a pas de prise directe. SWOT intègre à la fois l'interne (Forces/Faiblesses) et l'externe (Opportunités/Menaces). Le bon enchaînement : PESTEL d'abord pour scanner le contexte macro, puis SWOT pour positionner l'organisation dans ce contexte. Les Opportunités et Menaces du SWOT sont souvent directement issues du PESTEL."}],
    {"tone": "méthodologique, orienté application",
     "structure": ["SWOT", "PESTEL", "utilisation combinée", "pièges"],
     "avoid": ["remplissage de tableau sans analyse", "présenter comme suffisant pour une stratégie complète"]},
    ["SWOT", "PESTEL", "analyse stratégique", "environnement", "diagnostic", "TOWS"]
))

# 2
save(f"{BASE}/porter_5_forces.json", ku(
    "knowledges.professional.strategy.porter_5_forces",
    "Les 5 forces de Porter — analyser l'attractivité d'un secteur",
    "high",
    "Framework de Michael Porter pour évaluer la rentabilité structurelle d'un secteur et les pressions concurrentielles : nouveaux entrants, fournisseurs, clients, substituts, concurrence interne.",
    "Le modèle des 5 forces de Porter est un cadre d'analyse sectorielle qui évalue l'intensité compétitive d'un secteur et sa rentabilité potentielle à travers cinq dimensions de pression : rivaux existants, entrants potentiels, substituts, pouvoir des fournisseurs et pouvoir des clients.",
    {"5_forces": {
        "rivalite_interne": "Intensité de la concurrence entre les acteurs existants — concentration, croissance du marché, différenciation",
        "nouveaux_entrants": "Menace de nouveaux concurrents — barrières à l'entrée : capital, marque, régulations, effets réseau",
        "substituts": "Produits d'un autre secteur qui remplissent la même fonction — capent les prix et les marges",
        "fournisseurs": "Pouvoir de négociation des fournisseurs — concentration, coût de changement, différenciation des inputs",
        "clients": "Pouvoir de négociation des acheteurs — concentration, information, coût de changement, sensibilité prix"
     },
     "interpretation": {
        "secteur_attractif": "5 forces faibles → marges élevées structurellement (ex : logiciels avec effets réseau)",
        "secteur_difficile": "5 forces fortes → marges structurellement basses (ex : compagnies aériennes low cost)",
        "usage": "Choisir où jouer, identifier les leviers pour modifier les forces à son avantage"
     },
     "evolution": "Porter a ajouté plus tard la 6e force : le rôle des complémenteurs (acteurs qui augmentent la valeur de votre produit) — concept popularisé par Brandenburger & Nalebuff"},
    [{"prompt": "Comment utiliser les 5 forces de Porter pour ma stratégie ?",
      "answer": "Trois usages : 1) Diagnostic — comprendre pourquoi un secteur est rentable ou non (les forces structurent les marges). 2) Positionnement — identifier les forces les plus faibles (là où on a de la marge) et les plus fortes (là où il faut innover pour les contourner). 3) Choix d'entrée — évaluer l'attractivité d'un nouveau segment avant d'y investir. Exemple : une startup SaaS qui cible un marché où les clients sont très concentrés (fort pouvoir clients) doit se différencier sur la valeur pour ne pas être coincée sur les prix."},
     {"prompt": "Les 5 forces de Porter sont-elles encore pertinentes à l'ère digitale ?",
      "answer": "Oui, avec des adaptations. L'ère digitale a modifié l'intensité des forces mais pas leur logique : les effets réseau créent des barrières à l'entrée massives (force nouveaux entrants diminuée), la digitalisation réduit les coûts de changement pour les clients (force clients augmentée), et les plateformes créent de nouveaux substituts à vitesse accélérée. La 6e force des complémenteurs devient centrale dans les écosystèmes numériques. Le cadre reste utile — il faut juste l'actualiser selon les dynamiques digitales du secteur analysé."}],
    {"tone": "analytique, fondé sur Porter, orienté application",
     "structure": ["5 forces", "interprétation", "évolution"],
     "avoid": ["appliquer mécaniquement sans contextualiser", "présenter comme un outil statique"]},
    ["Porter", "5 forces", "secteur", "concurrence", "stratégie", "analyse sectorielle"]
))

# 3
save(f"{BASE}/strategie_ocean_bleu.json", ku(
    "knowledges.professional.strategy.strategie_ocean_bleu",
    "Stratégie Océan Bleu — créer un marché sans concurrence",
    "high",
    "Framework de Kim & Mauborgne pour sortir de la concurrence frontale en créant un nouvel espace de marché — canevas stratégique, matrice ERAC et exemples.",
    "La stratégie Océan Bleu est une approche qui consiste à créer une nouvelle demande dans un espace de marché non contesté (l'océan bleu) plutôt que de se battre pour des parts de marché dans un secteur existant saturé (l'océan rouge).",
    {"concepts_cles": {
        "ocean_rouge": "Secteur existant — concurrence frontale, différenciation sur les mêmes axes, marges comprimées",
        "ocean_bleu": "Espace de marché nouveau — courbe de valeur différente, compétition non pertinente",
        "innovation_valeur": "Réduire les coûts ET augmenter la valeur simultanément — pas un compromis"
     },
     "matrice_ERAC": {
        "eliminer": "Quels facteurs du secteur considérés acquis peuvent être éliminés ?",
        "reduire": "Quels facteurs peuvent être réduits bien en-dessous du standard secteur ?",
        "augmenter": "Quels facteurs peuvent être augmentés bien au-dessus du standard ?",
        "creer": "Quels facteurs jamais offerts dans le secteur peuvent être créés ?"
     },
     "canevas_strategique": "Graphique comparant la courbe de valeur de l'entreprise vs les concurrents sur les facteurs clés du secteur — visualise l'océan bleu potentiel",
     "exemples": {
        "cirque_soleil": "Éliminé : animaux, stars. Réduit : humour, danger. Augmenté : décor. Créé : thème narratif, production artistique. Résultat : prix 5x supérieur au cirque classique",
        "nintendo_wii": "Créé un marché de non-joueurs plutôt que de concurrencer PlayStation sur les specs"
     }},
    [{"prompt": "Comment identifier un océan bleu pour mon business ?",
      "answer": "Point de départ : la matrice ERAC appliquée à votre secteur. Lister tous les facteurs sur lesquels la concurrence se bat. Demander pour chacun : peut-on l'éliminer complètement ? Le réduire drastiquement ? En augmenter certains au-delà de la norme ? Et surtout : qu'est-ce qu'on peut créer que personne n'offre encore ? Chercher les 'non-clients' — les personnes qui n'achètent pas dans le secteur et pourquoi. C'est souvent là que se cachent les océans bleus : Cirque du Soleil a ciblé les adultes qui avaient abandonné le cirque, pas les amateurs existants."},
     {"prompt": "La stratégie Océan Bleu est-elle applicable à une PME ou une startup ?",
      "answer": "Particulièrement adaptée — les PME et startups ont moins de ressources pour gagner une guerre frontale dans un océan rouge. Le risque est réel : créer un marché qui n'existe pas encore demande de convaincre des clients de changer de comportement. Deux mitigation : 1) Commencer par un segment de non-clients proches (ceux qui ont utilisé le secteur mais ont arrêté) plutôt que de viser les non-clients absolus. 2) Valider la demande rapidement avec un MVP avant d'investir massivement. La matrice ERAC reste un excellent outil de questionnement même sans application totale de la théorie."}],
    {"tone": "stratégique, inspirant, ancré dans des exemples",
     "structure": ["concepts", "ERAC", "canevas", "exemples"],
     "avoid": ["trop abstrait", "promettre que ça marche toujours"]},
    ["océan bleu", "Kim Mauborgne", "innovation valeur", "ERAC", "stratégie", "marché"]
))

# 4
save(f"{BASE}/business_model_canvas.json", ku(
    "knowledges.professional.strategy.business_model_canvas",
    "Business Model Canvas — cartographier et innover son modèle d'affaires",
    "high",
    "Outil d'Osterwalder pour décrire, analyser et transformer un modèle d'affaires en 9 blocs — utilisé pour créer, pitcher et améliorer un business.",
    "Le Business Model Canvas (BMC) est un outil visuel de management stratégique qui représente la logique de création, livraison et capture de valeur d'une organisation en 9 blocs interconnectés sur une seule page.",
    {"9_blocs": {
        "proposition_valeur": "Ce qu'on offre et pourquoi les clients le choisissent — le cœur du BMC",
        "segments_clients": "Pour qui on crée de la valeur — définir précisément les segments cibles",
        "canaux": "Comment on atteint et sert les segments — distribution, communication, vente",
        "relations_clients": "Type de relation : self-service, communauté, assistance personnelle, automatisation",
        "sources_revenus": "Comment on monétise la proposition de valeur — abonnement, transaction, freemium, publicité",
        "ressources_cles": "Assets nécessaires pour fonctionner — humains, physiques, intellectuels, financiers",
        "activites_cles": "Ce qu'on doit absolument bien faire — production, plateforme, résolution de problèmes",
        "partenaires_cles": "Qui fournit ce qu'on ne fait pas nous-mêmes — réduire risques et coûts",
        "structure_couts": "Tous les coûts pour faire fonctionner le modèle — orientation cost vs value"
     },
     "lecture": "Droite = valeur et revenus. Gauche = efficience et coûts. Centre = proposition de valeur qui relie les deux",
     "lean_canvas": "Version startup de Maurya — remplace partenaires/ressources/activités par problème/solution/métriques clés/avantage injuste",
     "usage": ["Pitcher un investisseur", "Analyser un concurrent", "Détecter les incohérences de son modèle", "Explorer des variantes de monétisation"]},
    [{"prompt": "Comment remplir un Business Model Canvas pour ma startup ?",
      "answer": "Commencer par la Proposition de Valeur et le Segment Clients — ce sont les deux blocs les plus importants et ils se définissent mutuellement. Puis les Canaux (comment atteindre ce segment), la Relation Client (quelle expérience), les Sources de Revenus (comment monétiser). Ensuite le côté gauche : Ressources Clés (ce qu'on doit avoir), Activités Clés (ce qu'on doit faire), Partenaires Clés (qui fait ce qu'on ne fait pas). Finir par la Structure de Coûts. Conseil : faire 3 versions du BMC avec des modèles de monétisation différents avant de choisir — ça force à explorer."},
     {"prompt": "Quelle différence entre Business Model Canvas et Lean Canvas ?",
      "answer": "Le BMC (Osterwalder) est adapté aux organisations établies ou aux business qui ont déjà un modèle défini. Le Lean Canvas (Ash Maurya) est conçu pour les startups en phase de découverte : il remplace Partenaires/Ressources/Activités Clés par Problème/Solution/Métriques clés/Avantage Injuste (ce que personne ne peut copier). Le Lean Canvas force à articuler le problème et la solution dès le départ — essentiel quand le business model n'est pas encore validé. Pour une startup pre-PMF : Lean Canvas. Pour une organisation plus mature : BMC."}],
    {"tone": "pratique, orienté startups et business development",
     "structure": ["9 blocs", "lecture", "Lean Canvas", "usages"],
     "avoid": ["trop théorique", "ignorer les interdépendances entre blocs"]},
    ["Business Model Canvas", "BMC", "Osterwalder", "Lean Canvas", "startup", "modèle d'affaires", "stratégie"]
))

# 5
save(f"{BASE}/okr_strategie.json", ku(
    "knowledges.professional.strategy.okr_strategie",
    "OKR — lier stratégie et exécution par les objectifs",
    "high",
    "Framework OKR (Objectives & Key Results) pour aligner l'organisation sur des objectifs ambitieux et mesurables — définition, cascading, cadences et pièges à éviter.",
    "Les OKR (Objectives & Key Results) sont un système de définition et suivi des objectifs qui associe un objectif qualitatif inspirant (O) à 3-5 résultats mesurables qui prouvent son atteinte (KR) — conçu pour aligner et mobiliser, pas seulement mesurer.",
    {"structure": {
        "objective": "Qualitatif, inspirant, ambitieux — 'Devenir la référence européenne en IA responsable'. Répond à 'Où va-t-on ?'",
        "key_results": "Mesurables, time-bound, prouvent que l'Objective est atteint — pas des actions. 'Atteindre NPS 70 fin T3'"
     },
     "principes": {
        "ambitieux": "OKR calibrés à 70% d'atteinte — si on atteint 100%, c'était trop facile",
        "transparent": "Tous les OKR visibles dans l'organisation — alignement horizontal et vertical",
        "cadence": "Trimestriel pour les teams, annuel pour la vision stratégique",
        "pas_des_KPI": "Les KPI mesurent la santé opérationnelle (uptime, satisfaction). Les OKR mesurent le progrès vers le changement"
     },
     "pieges": [
        "Trop d'OKR (max 3-5 par niveau) — dilue le focus",
        "KR = liste de tâches ('lancer la feature X') plutôt que résultats mesurables",
        "Connecter les OKR à la rémunération — tue la prise de risque et l'ambition",
        "OKR imposés du haut sans participation — résistance et désengagement"
     ],
     "cascading": "Les OKR stratégiques de l'organisation inspirent (sans dicter) les OKR des équipes — bottom-up pour les KR, top-down pour la direction"},
    [{"prompt": "Comment définir de bons Key Results ?",
      "answer": "Test en 3 questions : 1) Est-ce mesurable avec un chiffre ? ('améliorer la satisfaction' n'est pas un KR, 'atteindre CSAT 4.2/5 en T2' en est un). 2) Est-ce que ça prouve que l'Objective est atteint, ou juste qu'on a travaillé ? ('lancer 3 features' = tâche, 'réduire le churn de 15% à 10%' = résultat). 3) L'équipe peut-elle influer dessus — ou est-ce une métrique sur laquelle elle n'a pas de levier ? Un bon KR est ambitieux mais atteignable avec un vrai effort — si on pense le faire à 100% facilement, c'est trop faible."},
     {"prompt": "OKR vs KPI — quelle différence et peut-on avoir les deux ?",
      "answer": "KPI = indicateurs de santé du business (chiffre d'affaires, NPS, coût d'acquisition) — à surveiller en continu. OKR = buts de transformation ambitieux sur un trimestre — à atteindre en mode projet. Les deux coexistent : les KPI indiquent si le moteur tourne bien, les OKR indiquent si on progresse vers la destination. Un KPI peut devenir un KR si on cherche à le faire bouger spécifiquement ce trimestre. Erreur fréquente : transformer tous les KPI en OKR — surcharge et perte de sens."}],
    {"tone": "stratégique et opérationnel, ancré dans John Doerr et Google",
     "structure": ["structure", "principes", "pièges", "cascading"],
     "avoid": ["confondre tâches et résultats", "présenter comme une solution magique"]},
    ["OKR", "objectifs", "Key Results", "stratégie", "John Doerr", "Google", "alignement organisationnel"]
))

# 6
save(f"{BASE}/strategie_croissance.json", ku(
    "knowledges.professional.strategy.strategie_croissance",
    "Stratégies de croissance — Ansoff et les 4 voies d'expansion",
    "high",
    "Matrice d'Ansoff et autres frameworks pour choisir sa stratégie de croissance : pénétration, développement produit, développement marché, diversification.",
    "Une stratégie de croissance définit comment une organisation va augmenter son chiffre d'affaires ou sa taille en combinant différemment ses produits existants ou nouveaux avec ses marchés existants ou nouveaux.",
    {"matrice_ansoff": {
        "penetration_marche": "Produits existants × Marchés existants — vendre plus aux clients actuels. Moindre risque, croissance limitée",
        "developpement_marche": "Produits existants × Nouveaux marchés — exporter, internationaliser, cibler un nouveau segment",
        "developpement_produit": "Nouveaux produits × Marchés existants — innover pour la base cliente actuelle",
        "diversification": "Nouveaux produits × Nouveaux marchés — risque maximal, potentiel maximal"
     },
     "autres_voies": {
        "croissance_organique": "Par le développement interne — prévisible, lente, préserve la culture",
        "croissance_externe": "Acquisition, fusion — rapide, risquée, complexité d'intégration",
        "partenariat": "Alliance, JV — accès à un marché ou une technologie sans y aller seul"
     },
     "growth_hacking": "Approche startup : boucles de croissance virale, optimisation du funnel acquisition/activation/rétention — complémentaire aux stratégies classiques",
     "choisir": {
        "maturite_marche": "Marché mature → pénétration + produit. Marché émergent → développement marché + diversification",
        "ressources": "La diversification nécessite des ressources importantes — piège pour les PME sous-capitalisées"
     }},
    [{"prompt": "Comment choisir entre développer un nouveau produit ou aller sur un nouveau marché ?",
      "answer": "Deux questions décisives : 1) Où est la force ? Si votre avantage est la technologie/produit, le développer sur votre marché existant préserve cet avantage (vous connaissez vos clients). Si votre avantage est la relation client et la distribution, répliquer sur de nouveaux marchés avec le produit existant est plus naturel. 2) Où est l'opportunité ? Si votre marché actuel stagne, aller sur un nouveau marché est plus urgent. Si votre marché croît mais que vos clients demandent plus, le développement produit s'impose. La matrice d'Ansoff n'est pas un oracle — c'est un cadre de questionnement."},
     {"prompt": "Notre croissance organique plafonne. Faut-il acquérir une entreprise ?",
      "answer": "Avant de décider : diagnostiquer pourquoi la croissance organique plafonne. C'est une question de marché saturé (vraie limite structurelle) ou d'exécution (problème de go-to-market, produit, équipe) ? L'acquisition ne résout pas un problème d'exécution. Si c'est une vraie limite marché : évaluer 3 questions clés : 1) La cible acquisition adresse-t-elle vraiment la contrainte (nouveau marché, nouvelle technologie, nouvelle équipe) ? 2) L'intégration est-elle réaliste (culture, systèmes, talent) ? 3) Le prix payé est-il justifié par les synergies identifiées — pas les synergies espérées. 70% des fusions-acquisitions détruisent de la valeur — principalement à cause de l'intégration surestimée."}],
    {"tone": "stratégique, fondé, pragmatique sur les risques",
     "structure": ["Ansoff", "autres voies", "growth hacking", "comment choisir"],
     "avoid": ["présenter la diversification comme l'option la plus ambitieuse donc la meilleure", "ignorer le risque M&A"]},
    ["Ansoff", "croissance", "pénétration marché", "diversification", "stratégie", "acquisition", "growth"]
))

# 7
save(f"{BASE}/avantage_concurrentiel.json", ku(
    "knowledges.professional.strategy.avantage_concurrentiel",
    "Avantage concurrentiel — construire et défendre une position unique",
    "high",
    "Sources d'avantage concurrentiel durable : différenciation, domination par les coûts, focalisation (Porter), effets réseau, moats et capacités distinctives.",
    "Un avantage concurrentiel est une caractéristique ou capacité qui permet à une organisation de créer plus de valeur que ses concurrents de façon durable — soit en offrant quelque chose d'unique (différenciation), soit en étant plus efficiente (coût).",
    {"strategies_generiques_porter": {
        "domination_couts": "Produire au coût le plus bas du secteur — IKEA, Ryanair. Nécessite des économies d'échelle massives",
        "differenciation": "Être perçu comme unique sur des attributs valorisés — Apple, LVMH. Permet des prix premium",
        "focalisation": "Servir un segment spécifique mieux que personne — niche où on est imbattable"
     },
     "moats_durables": {
        "effets_reseau": "Plus de valeur quand plus d'utilisateurs — Facebook, LinkedIn, Airbnb",
        "couts_de_changement": "Coût (temps, argent, effort) de changer de fournisseur — Salesforce, SAP, ERP",
        "economies_echelle": "Coûts unitaires qui baissent avec le volume — Amazon logistics",
        "actifs_intangibles": "Marque, brevets, licences, données propriétaires",
        "avantage_reseau": "Accès aux meilleures ressources, talents, ou localisations"
     },
     "tester_lavantage": [
        "Est-ce que des concurrents ont essayé de le répliquer et échoué ?",
        "Est-ce que les clients payent un premium ou restent fidèles sans raison de prix ?",
        "Est-ce que l'avantage se renforce avec le temps plutôt que de s'éroder ?"
     ]},
    [{"prompt": "Comment identifier l'avantage concurrentiel de mon entreprise ?",
      "answer": "Trois questions : 1) Pourquoi les clients nous choisissent-ils plutôt que la concurrence — pas la réponse marketing, la vraie raison (prix, relation, produit, localisation, habitude). 2) Qu'est-ce qui nous a permis de résister à des concurrents qui ont essayé de prendre notre place ? 3) Quel aspect de notre modèle serait le plus difficile à répliquer pour un nouveau concurrent avec les mêmes ressources ? L'avantage concurrentiel réel est souvent différent de l'avantage perçu — les clients et les concurrents le voient mieux que nous."},
     {"prompt": "Notre avantage concurrentiel s'érode. Comment le défendre ou le renouveler ?",
      "answer": "Deux stratégies : défendre ou transformer. Défendre : renforcer les barrières existantes — investir dans les effets réseau si c'est votre moat, accroître les coûts de changement, déposer des brevets, accélérer l'acquisition de données. Transformer : si l'avantage est structurellement menaçé (disruption technologique), mieux vaut se cannibaliser soi-même que d'attendre que quelqu'un d'autre le fasse. Kodak avait inventé l'appareil photo numérique en 1975 et n'a pas osé le lancer pour protéger ses pellicules — cas d'école de l'inaction face à la disruption."}],
    {"tone": "stratégique, fondé sur Porter et les moats de Buffett",
     "structure": ["stratégies génériques", "moats", "tester"],
     "avoid": ["confondre avantage temporaire et durable", "ignorer la dynamique de disruption"]},
    ["avantage concurrentiel", "Porter", "moat", "différenciation", "effets réseau", "stratégie", "disruption"]
))

# 8
save(f"{BASE}/gestion_portefeuille_strategique.json", ku(
    "knowledges.professional.strategy.gestion_portefeuille_strategique",
    "Gestion de portefeuille stratégique — BCG matrix et arbitrage des activités",
    "medium",
    "Outils d'analyse de portefeuille d'activités (BCG, McKinsey-GE) pour décider où investir, maintenir, ou désinvestir dans un portefeuille d'activités.",
    "La gestion du portefeuille stratégique est l'art d'allouer les ressources d'une organisation entre ses différentes activités (business units, produits, marchés) pour maximiser la création de valeur globale sur le long terme.",
    {"matrice_bcg": {
        "reference": "Boston Consulting Group — 2×2 part de marché relative × croissance du marché",
        "etoiles": "Forte croissance + forte part — investir pour maintenir la position",
        "vaches_a_lait": "Faible croissance + forte part — extraire les cash flows pour financer les étoiles",
        "dilemmes": "Forte croissance + faible part — décider si on investit pour gagner ou si on abandonne",
        "poids_morts": "Faible croissance + faible part — désinvestir ou maintenir sans investir"
     },
     "limites_bcg": [
        "Trop simpliste — part de marché ne détermine pas toujours la rentabilité",
        "Statique — ne capture pas les dynamiques de disruption",
        "Auto-réalisateur — les 'poids morts' sont sous-investis puis deviennent réellement des poids morts"
     ],
     "matrice_mckinsey_ge": "9 cases (attractivité secteur × forces de l'entreprise) — plus nuancée que BCG mais plus complexe à construire",
     "allocation_ressources": {
        "principe": "Les ressources vont là où elles créent le plus de valeur — pas là où les managers les plus influents opèrent",
        "processus": "Revue annuelle du portefeuille : quelles activités accélérer, maintenir, désinvestir ?"
     }},
    [{"prompt": "Comment décider si on doit abandonner une ligne de produits ?",
      "answer": "Quatre critères : 1) Profitabilité actuelle et tendance — est-elle en baisse structurelle ou cyclique ? 2) Usage des ressources — cette ligne mobilise-t-elle des ressources (capital, talents, attention) disproportionnées par rapport à sa contribution ? 3) Cohérence stratégique — contribue-t-elle à la vision et aux compétences distinctives, ou crée-t-elle de la dispersion ? 4) Alternatives — ces ressources libérées permettraient-elles une croissance supérieure ailleurs ? Un désinvestissement bien exécuté libère de l'énergie pour les activités à fort potentiel."},
     {"prompt": "C'est quoi la matrice BCG et comment l'utiliser ?",
      "answer": "La BCG classe les activités selon deux axes : part de marché relative (votre force vs le leader) et croissance du marché. Quatre quadrants : Étoiles (fort potentiel, investir), Vaches à lait (cash flows stables, extraire), Dilemmes (décider d'investir ou d'abandonner), Poids morts (désinvestir). Usage pratique : visualiser l'équilibre du portefeuille — un portefeuille sain a des Vaches qui financent des Étoiles. Limite principale : trop simpliste — des facteurs comme la rentabilité, les synergies et les compétences core ne sont pas capturés."}],
    {"tone": "stratégique, nuancé sur les limites des outils",
     "structure": ["BCG", "limites", "McKinsey-GE", "allocation"],
     "avoid": ["appliquer mécaniquement la BCG", "présenter le désinvestissement comme facile"]},
    ["BCG", "portefeuille", "stratégie", "allocation ressources", "désinvestissement", "McKinsey"]
))

# 9
save(f"{BASE}/execution_strategie.json", ku(
    "knowledges.professional.strategy.execution_strategie",
    "Exécution de la stratégie — le gouffre entre la vision et les résultats",
    "high",
    "Comment transformer une stratégie en actions concrètes et résultats mesurables : cascade stratégique, gouvernance, gestion du changement et facteurs d'échec.",
    "L'exécution stratégique est le processus de traduction d'une stratégie en initiatives, ressources, processus et comportements qui créent effectivement les résultats attendus — c'est là que la plupart des stratégies échouent.",
    {"statistique": "70% des stratégies bien conçues échouent à l'exécution (Harvard Business Review)",
     "causes_echec": [
        "Manque de clarté sur les priorités — trop d'initiatives simultanées",
        "Ressources non allouées à la stratégie — le budget reste sur l'existant",
        "Leaders intermédiaires non engagés — ils exécutent l'ancien modèle",
        "Absence de boucle de feedback — pas d'ajustement quand les hypothèses sont infirmées",
        "Culture incompatible avec la stratégie — 'culture eats strategy for breakfast' (Drucker)"
     ],
     "facteurs_succes": {
        "cascade": "Chaque niveau de l'organisation traduit la stratégie en objectifs concrets pour son niveau",
        "gouvernance": "Revue stratégique mensuelle/trimestrielle — pas annuelle",
        "quick_wins": "Premières victoires rapides pour créer la croyance et l'élan",
        "capacity_to_change": "Évaluer et développer les compétences nécessaires avant de lancer"
     },
     "balanced_scorecard": "Kaplan & Norton — 4 perspectives : financière, clients, processus internes, apprentissage. Traduit la stratégie en indicateurs mesurables à chaque niveau"},
    [{"prompt": "Notre stratégie est bonne sur le papier mais rien ne change sur le terrain. Pourquoi ?",
      "answer": "Diagnostic en 4 questions : 1) Les managers intermédiaires comprennent-ils la stratégie — pas juste ses termes mais ce qu'elle implique concrètement pour leur équipe ? (souvent non). 2) Les ressources (budget, headcount) ont-elles vraiment bougé vers les nouvelles priorités ou sont-elles restées sur l'existant ? 3) Les indicateurs mesurés quotidiennement reflètent-ils la stratégie ou l'ancien modèle ? 4) La culture — les comportements qui 'marchent' dans l'organisation sont-ils alignés sur la stratégie ou en contradiction ? La stratégie ne vit que si elle change les décisions du quotidien, pas seulement les présentations."},
     {"prompt": "Comment assurer que toute l'organisation tire dans la même direction ?",
      "answer": "Deux mécanismes complémentaires : 1) Cascade stratégique — chaque niveau traduit les priorités en termes concrets pour son périmètre. L'équipe direction définit les 3 priorités stratégiques de l'année. Chaque département définit comment il y contribue. Chaque équipe définit ses OKR trimestriels en conséquence. 2) Gouvernance du changement — réunion mensuelle dédiée au suivi stratégique (pas opérationnel) : où en sommes-nous sur les initiatives clés, quelles hypothèses ont été infirmées, faut-il ajuster. La stratégie qui n'est pas revue régulièrement est une stratégie oubliée."}],
    {"tone": "pragmatique, orienté action et obstacles réels",
     "structure": ["statistique", "causes d'échec", "facteurs de succès", "Balanced Scorecard"],
     "avoid": ["trop théorique", "ignorer la dimension culturelle"]},
    ["exécution stratégie", "stratégie", "cascade", "Balanced Scorecard", "OKR", "changement organisationnel"]
))

# 10
save(f"{BASE}/analyse_concurrentielle.json", ku(
    "knowledges.professional.strategy.analyse_concurrentielle",
    "Analyse concurrentielle — comprendre le paysage compétitif",
    "high",
    "Méthodes pour cartographier, analyser et surveiller la concurrence : benchmarking, war gaming, analyse des mouvements concurrentiels et positionnement.",
    "L'analyse concurrentielle est le processus systématique de collecte et d'interprétation des informations sur les concurrents pour informer les décisions stratégiques — identifier où se battre, comment gagner et anticiper les réactions des adversaires.",
    {"cadre_analyse": {
        "qui_surveiller": "Concurrents directs (même offre, même cible), indirects (besoin similaire), substituts (autre solution au même problème), entrants potentiels",
        "que_analyser": "Positionnement, modèle économique, forces/faiblesses, stratégie observée, ressources, culture et talent",
        "sources": ["Sites, rapports annuels, offres d'emploi (révèlent les priorités)", "Entretiens clients", "Conférences", "LinkedIn pour les mouvements de talents", "G2/Capterra/Trustpilot pour les produits digitaux"]
     },
     "war_gaming": {
        "principe": "Simuler les réponses concurrentielles avant d'agir — 'si on fait X, que vont-ils faire ?'",
        "processus": "Diviser l'équipe en groupes jouant chaque concurrent + votre entreprise. Simuler 2-3 trimestres."
     },
     "positionnement": {
        "carte_perceptuelle": "Axe X × Axe Y selon 2 critères clés du marché — visualise les espaces occupés et vides",
        "differentiation": "Identifier sur quels axes on peut gagner sans se battre frontalement"
     },
     "veille_concurrentielle": "Process continu, pas ponctuel — alertes Google, suivi LinkedIn, newsletters secteur, revue trimestrielle des mouvements"},
    [{"prompt": "Comment faire une analyse concurrentielle sans budget d'étude de marché ?",
      "answer": "Sources gratuites ou low-cost : 1) Offres d'emploi des concurrents — révèlent leurs priorités stratégiques (si ils recrutent massivement en data science, ils pivotent vers la donnée). 2) Avis clients sur G2, Capterra, App Store — sources directes de faiblesses et forces perçues. 3) LinkedIn — qui recrutent-ils, qui partent, qui arrivent en leadership. 4) Leurs contenus marketing et blogs — ce qu'ils mettent en avant révèle leur positionnement. 5) Entretiens de 30 min avec des prospects qui ont aussi évalué les concurrents — source d'or sur les critères de comparaison réels."},
     {"prompt": "Un concurrent majeur vient d'annoncer une initiative qui ressemble à notre roadmap. Que faire ?",
      "answer": "Avant de réagir : distinguer annonce et réalité. Les grandes annonces concurrentielles précèdent souvent l'exécution de 12-18 mois. Analyser : est-ce qu'ils ont les ressources et compétences pour exécuter ? Est-ce que ça valide votre hypothèse de marché (bonne nouvelle) ou menace directement votre différenciation ? Si menace directe : identifier 2-3 axes sur lesquels vous pouvez gagner qu'eux ne peuvent pas répliquer rapidement (données propriétaires, relations clients, vitesse d'itération). Ne pas changer de direction en réaction panique — souvent la meilleure réponse est d'accélérer, pas de pivoter."}],
    {"tone": "analytique, orienté décision, pragmatique sur les ressources",
     "structure": ["cadre", "war gaming", "positionnement", "veille"],
     "avoid": ["obsession concurrentielle au détriment du focus client", "ignorer les substituts"]},
    ["analyse concurrentielle", "benchmarking", "war gaming", "positionnement", "veille", "stratégie", "concurrence"]
))

# 11
save(f"{BASE}/transformation_numerique.json", ku(
    "knowledges.professional.strategy.transformation_numerique",
    "Transformation numérique — stratégie et conduite du changement digital",
    "high",
    "Comment conduire une transformation numérique : définir la vision, prioriser les initiatives, gérer la résistance et mesurer la maturité digitale.",
    "La transformation numérique est le réalignement stratégique d'une organisation pour exploiter les capacités digitales (données, automatisation, IA, plateformes) afin de créer de la valeur nouvelle et d'améliorer l'expérience client — c'est autant un changement organisationnel que technologique.",
    {"dimensions": {
        "experience_client": "Redéfinir les points de contact et parcours clients via le digital",
        "operations": "Automatiser et optimiser les processus internes",
        "modele_business": "Créer de nouvelles sources de revenus ou de nouveaux marchés via le digital",
        "culture": "Développer les compétences digitales, l'agilité et la culture data-driven"
     },
     "maturite_digitale": {
        "niveaux": ["Analogique (peu ou pas de digital)", "Digital partiel (outils isolés)", "Digital connecté (données intégrées)", "Digital avancé (IA, prédiction)", "Digital natif (data & IA core business)"],
        "diagnostic": "Evaluer chaque dimension (expérience client, ops, modèle, culture) séparément"
     },
     "facteurs_succes": [
        "Portage par la direction — pas seulement un projet IT",
        "Commencer par les quick wins pour créer la croyance",
        "Donnée comme fondation — sans données fiables, l'IA et l'analytique ne fonctionnent pas",
        "Compétences internes — ne pas tout externaliser"
     ],
     "erreurs": [
        "Digitaliser des processus cassés plutôt que de les repenser",
        "Acheter la technologie avant d'avoir défini le problème",
        "Sous-estimer la conduite du changement — la technologie est 20% du défi, l'humain est 80%"
     ]},
    [{"prompt": "Par où commencer une transformation digitale dans une PME ?",
      "answer": "Trois premières étapes : 1) Diagnostic honnête — où en sommes-nous réellement (pas où on voudrait être) ? Regarder 3 dimensions : expérience client (canaux, friction), opérations (processus manuels, données en silos), données (qualité, accessibilité). 2) Choisir un périmètre restreint pour commencer — une quick win tangible (ex : CRM pour la force de vente, ou portail client) plutôt qu'une transformation globale. 3) Construire la compétence en interne — au moins une personne qui comprend le digital profondément et qui porte le changement dans l'équipe. Le risque de tout externaliser est de ne jamais développer la compétence interne."},
     {"prompt": "Nos équipes résistent à la transformation digitale. Comment changer ça ?",
      "answer": "La résistance est rationnelle — les gens résistent quand ils ne comprennent pas le 'pourquoi', quand ils craignent pour leur emploi, ou quand ils ont déjà vécu des projets IT qui ont échoué. Trois approches : 1) Rendre le 'pourquoi' concret et personnel — pas 'digitaliser nos processus' mais 'ça va vous libérer de 2h de saisie manuelle par semaine'. 2) Co-construire — impliquer les équipes terrain dans la conception, pas seulement dans l'adoption. 3) Célébrer les early adopters — créer des ambassadeurs internes qui embarquent leurs pairs. La formation seule ne suffit pas — il faut du sens et de la participation."}],
    {"tone": "stratégique et humain, pragmatique sur les obstacles",
     "structure": ["dimensions", "maturité", "facteurs de succès", "erreurs"],
     "avoid": ["techno-centrisme", "ignorer la dimension humaine et culturelle"]},
    ["transformation numérique", "digital", "IA", "stratégie", "conduite du changement", "maturité digitale"]
))

# 12
save(f"{BASE}/diagnostic_strategique.json", ku(
    "knowledges.professional.strategy.diagnostic_strategique",
    "Diagnostic stratégique — évaluer la situation avant de décider",
    "high",
    "Comment conduire un diagnostic stratégique complet : analyser externe (PESTEL, Porter), interne (chaîne de valeur, ressources), identifier les enjeux clés et formuler les options stratégiques.",
    "Le diagnostic stratégique est la phase analytique préalable à toute décision stratégique — il vise à comprendre la situation réelle de l'organisation dans son environnement pour identifier les enjeux fondamentaux et les options disponibles.",
    {"etapes": {
        "1_externe": "Analyser l'environnement macro (PESTEL) et sectoriel (Porter 5 forces) — comprendre les opportunités et menaces",
        "2_interne": "Analyser les ressources, compétences et processus — identifier les forces et faiblesses",
        "3_chaine_valeur": "Décomposer les activités créatrices de valeur (Porter) — identifier où on est différencié ou désavantagé",
        "4_synthese": "Croiser externe et interne — SWOT, enjeux clés, tensions stratégiques",
        "5_options": "Générer des scénarios stratégiques alternatifs avant de converger"
     },
     "chaine_valeur_porter": {
        "activites_primaires": "Logistique entrante → Production → Logistique sortante → Marketing/Ventes → Service",
        "activites_support": "Infrastructure, RH, R&D, Achats",
        "usage": "Identifier les activités où on est meilleur (à renforcer) et celles où on est moins bon (à externaliser ou améliorer)"
     },
     "questions_cles": [
        "Quel est le vrai problème ou la vraie opportunité ?",
        "Quelles hypothèses implicites guidons-nous et sont-elles valides ?",
        "Qu'est-ce qu'on ne voit pas parce qu'on est trop dedans ?"
     ],
     "biais_a_eviter": "Biais de confirmation (ne voir que ce qui confirme nos croyances), HIPPO (Highest Paid Person's Opinion), ancrage sur la stratégie précédente"},
    [{"prompt": "Comment conduire un diagnostic stratégique de mon entreprise ?",
      "answer": "Structure en 3 temps : 1) Externe — PESTEL (quelles tendances macro nous affectent dans 2-5 ans ?) puis Porter (comment est structurée la concurrence dans notre secteur ?). 2) Interne — quelles sont nos vraies compétences distinctives ? Où perdons-nous de l'argent ou de l'énergie ? La chaîne de valeur de Porter aide à décomposer les activités. 3) Synthèse — SWOT construit à partir des 2 premières étapes, puis identification des 3-5 enjeux stratégiques clés. L'enjeu stratégique, c'est la question fondamentale à laquelle la stratégie doit répondre — pas le symptôme mais la cause."},
     {"prompt": "On fait des diagnostics stratégiques chaque année mais les conclusions ne changent pas. Pourquoi ?",
      "answer": "Deux causes fréquentes : 1) Le processus est dominé par les personnes qui ont le plus d'ancienneté (HIPPO) — leurs biais survivent au diagnostic. Solution : inclure des voix externes (clients, experts sectoriels, consultants juniors sans historique) et des perspectives contre-intuitives. 2) Le diagnostic confirme la stratégie existante plutôt que de la remettre en question — biais de confirmation institutionnel. Solution : technique du 'pré-mortem' appliqué à la stratégie actuelle — 'dans 3 ans cette stratégie a échoué, qu'est-ce qui s'est passé ?'"}],
    {"tone": "méthodologique, analytique, orienté questionnement rigoureux",
     "structure": ["étapes", "chaîne de valeur", "questions clés", "biais"],
     "avoid": ["mécanisme sans pensée critique", "confondre diagnostic et décision"]},
    ["diagnostic stratégique", "SWOT", "Porter", "chaîne de valeur", "PESTEL", "stratégie", "analyse"]
))

print(f"\n=== professional/strategy : 12 KU créés ===")
