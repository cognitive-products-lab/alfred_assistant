"""
Enrichissement day3 — cpl/business_strategy/ (15 KU)
"""
import json
from pathlib import Path
from datetime import date

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
TODAY = date.today().isoformat()

def meta():
    return {"created_at": TODAY, "validated_at": TODAY, "validated_by": "ALFRED enrichment pipeline",
            "enrichment_version": "day3", "schema_version": "1.2", "review_notes": "", "block": "b18"}

def save(path, data):
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(id_, title, priority, summary, core_def, knowledge, examples, guidance, tags):
    return {"schema_version": "1.2", "type": "knowledge_unit", "id": id_, "title": title,
            "domain": "cpl", "subdomain": "business_strategy", "status": "validated",
            "metadata": meta(), "priority": priority, "summary": summary,
            "core_definition": core_def, "knowledge": knowledge, "example_answers": examples,
            "response_guidance": guidance, "tags": tags, "related_knowledge_units": []}

save("cpl/business_strategy/consulting_governance.json", ku(
    "knowledges.cpl.business_strategy.consulting_governance",
    "Gouvernance du cabinet de conseil — structure et pilotage CPL",
    "high",
    "Cadre de gouvernance pour un cabinet de conseil indépendant : prise de décision, rôles, suivi des engagements clients, gestion des conflits d'intérêts et conformité.",
    "La gouvernance d'un cabinet de conseil désigne l'ensemble des mécanismes de pilotage, de contrôle et de responsabilité qui assurent que le cabinet fonctionne conformément à ses valeurs, ses engagements clients et ses obligations légales.",
    {"piliers": {"pilotage_strategique": "Vision, OKR annuels, revue trimestrielle", "gestion_clients": "Comités de suivi, reporting, escalade", "conformite": "RGPD, confidentialité, conflits d'intérêts", "finance": "Trésorerie, facturation, prévisionnel"},
     "outils_gouvernance": {"tableau_de_bord": "KPI clés : CA, taux utilisation, NPS client, pipeline", "comite_de_direction": "Fréquence mensuelle minimum pour cabinet solo ou small team", "charte_ethique": "Règles sur les conflits d'intérêts, la confidentialité client, les pratiques commerciales"},
     "specificite_cabinet_solo": "Pour un indépendant ou micro-cabinet, gouvernance = discipline personnelle + outils simples (tableau de suivi, agenda stratégique mensuel). Le risque principal : être 100% opérationnel et négliger le pilotage.",
     "cpl_context": "CPL = cabinet de conseil en management. La gouvernance inclut aussi la gestion de la marque professionnelle et de la réputation sectorielle."},
    [{"prompt": "Comment structurer la gouvernance de mon cabinet solo ?", "answer": "Pour un cabinet solo, trois rituels suffisent : 1) Revue mensuelle (2h) : finances, pipeline, clients actifs, une décision stratégique. 2) Revue trimestrielle (demi-journée) : positionnement, offres, développement. 3) Revue annuelle : cap stratégique, investissements, formation. L'outil importe peu — l'important c'est la régularité. Un Notion ou un tableur suffit largement."},
     {"prompt": "Comment gérer les conflits d'intérêts avec des clients concurrents ?", "answer": "Politique claire dès le départ : définir ce qu'on considère comme un conflit (même secteur ? même marché géo ? même type de mission ?), le documenter dans les contrats, et informer les clients concernés. Pour un cabinet solo, la clôture séquentielle (ne pas travailler simultanément pour deux concurrents directs) est souvent la règle la plus simple et la plus honnête."}],
    {"tone": "professionnel, pragmatique, contextualisé CPL", "structure": ["cadre", "outils", "cas solo"], "avoid": ["trop corporate", "ignorer la réalité indépendante"]},
    ["gouvernance", "cabinet conseil", "CPL", "pilotage", "conformité", "indépendant"]
))

save("cpl/business_strategy/customer_persona_business.json", ku(
    "knowledges.cpl.business_strategy.customer_persona_business",
    "Personas client B2B — construire et utiliser des profils décisionnaires",
    "high",
    "Méthode pour construire des personas acheteurs B2B (decision makers, influenceurs, utilisateurs) utilisés pour affiner le positionnement, les offres et les messages commerciaux.",
    "Un persona client B2B est une représentation semi-fictive d'un type d'acheteur ou de décisionnaire fondée sur des données réelles (entretiens, observations, données marché), décrivant ses responsabilités, ses objectifs, ses blocages et ses critères de décision.",
    {"composantes": {"role_et_contexte": "Poste, secteur, taille d'organisation, équipe", "objectifs": "Ce qu'il cherche à accomplir professionnellement", "blocages": "Ce qui l'empêche d'atteindre ses objectifs", "criteres_decision": "Sur quoi il évalue un prestataire (prix, références, expertise, rapidité)", "canaux": "Où il cherche l'information, qui il consulte"},
     "personas_b2b_typiques": {"acheteur_economique": "DAF ou DG — focus ROI et risque", "acheteur_technique": "DSI ou expert — focus faisabilité et intégration", "utilisateur": "Équipe opérationnelle — focus facilité d'usage", "champion": "Sponsor interne — focus alignement stratégique"},
     "construction": ["10-15 entretiens clients et prospects", "Analyser les objections commerciales récurrentes", "Croiser avec les données CRM (qui achète, qui n'achète pas)"],
     "utilisation": "Tester chaque message commercial, chaque offre, chaque canal contre le persona — \"est-ce que ça résonne pour lui ?\""},
    [{"prompt": "Comment créer un bon persona client pour mon cabinet ?", "answer": "Commence par 5-10 entretiens avec tes meilleurs clients actuels. Questions clés : qu'est-ce qui t'a amené à chercher un consultant ? Quel était ton problème exact ? Quels critères t'ont fait choisir (ou ne pas choisir) ? Qu'est-ce qui t'aurait fait partir ? Ensuite regroupe par patterns — tu découvriras 2-3 profils distincts, pas 10."},
     {"prompt": "Mon offre ne convertit pas, comment ajuster ?", "answer": "Revenir au persona : ton offre répond-elle au problème qu'il se formule lui-même, ou au problème que toi tu vois ? La différence est souvent là. Un diagnostic conseil qui résout \"comment améliorer vos processus\" convertit moins bien qu'un qui résout \"comment faire la même chose avec 20% d'effectif en moins\" — même si c'est le même travail."}],
    {"tone": "professionnel, orienté action", "structure": ["composantes", "types B2B", "construction", "utilisation"], "avoid": ["persona trop fictionnel", "ignorer le cycle d'achat B2B"]},
    ["persona", "B2B", "acheteur", "décisionnaire", "positionnement", "CPL"]
))

save("cpl/business_strategy/customer_retention.json", ku(
    "knowledges.cpl.business_strategy.customer_retention",
    "Fidélisation client en conseil — transformer un projet en relation longue",
    "high",
    "Stratégies pour transformer des missions ponctuelles en relations durables : extension de scope, récurrence, upsell, et entretien du lien entre missions.",
    "La fidélisation client en conseil désigne l'ensemble des pratiques qui transforment une relation transactionnelle (mission unique) en relation de confiance durable, génératrice de récurrence, d'extension et de recommandation.",
    {"leviers": {"excellence_operationnelle": "Dépasser les engagements — la base de toute fidélisation", "extension_scope": "Identifier les besoins adjacents pendant la mission en cours", "suivi_post_mission": "Contact à J+30, J+90, J+180 — maintenir le lien sans vendre", "valeur_ajoutee_continue": "Partager veille, insights, benchmarks entre les missions"},
     "signaux_d_opportunite": ["Client mentionne un nouveau projet", "Changement d'organisation chez le client", "Nouveau responsable qui ne te connaît pas — à rencontrer"],
     "erreurs_frequentes": ["Disparaître après la livraison", "Revenir uniquement pour vendre", "Ne pas systématiser le suivi"],
     "metriques": {"nps": "Taux de recommandation — indicateur leading de fidélisation", "recurrence": "% de CA venant de clients existants", "wallet_share": "Part du budget conseil du client que tu captes"},
     "cpl_specificite": "En conseil de management, le changement d'interlocuteur (turnover côté client) est un risque majeur — multiplier les liens dans l'organisation cible."},
    [{"prompt": "Comment rester dans l'esprit de mes clients entre deux missions ?", "answer": "Trois pratiques simples : 1) Relance structurée : J+30 pour un feedback, J+90 pour un point informel, J+180 pour une actualité pertinente. 2) Partage de valeur : un article, un benchmark, une info sectorielle — pas commercial, juste utile. 3) Connexion réseau : les mettre en relation avec d'autres contacts qui peuvent leur être utiles. La règle : 80% de valeur donnée, 20% de demande."},
     {"prompt": "Mon client est content mais ne renouvelle pas. Pourquoi ?", "answer": "Plusieurs hypothèses : 1) Le besoin n'est pas récurrent — vérifier s'il y a des sujets adjacents. 2) Il ne sait pas ce que tu fais d'autre — problème de visibilité de l'offre. 3) Il cherche chez les grands cabinets pour le politique interne — challenger en ROI et réactivité. 4) Ton prix est hors budget maintenant — explorer des formats plus légers (coaching, forfaits)."}],
    {"tone": "stratégique, orienté relation", "structure": ["leviers", "signaux", "métriques"], "avoid": ["techniques de vente agressives", "ignorer la qualité opérationnelle"]},
    ["fidélisation", "rétention", "clients", "récurrence", "conseil", "CPL", "NPS"]
))

save("cpl/business_strategy/delivery_quality_framework.json", ku(
    "knowledges.cpl.business_strategy.delivery_quality_framework",
    "Cadre qualité de livraison — standards et processus de delivery conseil",
    "high",
    "Framework pour garantir la qualité des livrables et des missions de conseil : revue qualité, gestion des attentes, communication client et gestion des aléas.",
    "Un cadre qualité de livraison en conseil définit les standards, processus et rituels qui assurent que chaque mission produit des livrables à la hauteur des engagements pris, dans les délais et le budget convenus, avec une expérience client positive tout au long.",
    {"piliers": {"cadrage_rigoureux": "Aligner les attentes dès le départ — scope, livrables, critères de succès, points de go/no-go", "jalons_intermediaires": "Partager des états d'avancement avant la livraison finale — pas de surprise", "revue_qualite": "Relecture critique avant livraison : \"Est-ce que ça répond vraiment à la question ?\"", "gestion_des_alea": "Protocole clair si retard ou changement de scope — communiquer tôt"},
     "livrables_qualite": {"structure": "Répondre à la question, pas à la question d'à côté", "synthese": "Executive summary en page 1 — le client lit peut-être que ça", "recommandations": "Actionnables, priorisées, avec risques identifiés"},
     "communication_client": {"rythme": "Point hebdomadaire minimum sur missions > 4 semaines", "escalade": "Remonter les risques dès détection — pas en dernière minute", "surprises": "La seule bonne surprise est une avance sur le planning"},
     "post_mission": "Debrief systématique : qu'est-ce qui a bien marché, qu'est-ce qu'on améliore la prochaine fois."},
    [{"prompt": "Comment garantir la qualité de mes livrables ?", "answer": "Trois pratiques non-négociables : 1) Cadrage écrit dès le début — ce qu'on livre, ce qu'on ne livre pas, les critères de succès. 2) Draft intermédiaire partagé avant la livraison finale — pas de surprise à la remise. 3) Question avant chaque livraison : \"Est-ce que ce document permet au client de prendre la décision qu'il cherche à prendre ?\" Si non, ce n'est pas encore fini."},
     {"prompt": "Un projet dérive, comment le gérer ?", "answer": "Communiquer tôt — dès que tu vois la dérive, pas quand elle est confirmée. Format simple : situation actuelle, cause, impact sur planning/budget, options pour corriger. Les clients acceptent presque toujours les aléas gérés de manière transparente. Ce qu'ils n'acceptent pas, c'est d'apprendre un problème au dernier moment."}],
    {"tone": "professionnel, orienté excellence opérationnelle", "structure": ["piliers", "standards livrables", "communication"], "avoid": ["trop processuel", "négliger la relation client"]},
    ["qualité", "livraison", "conseil", "livrables", "gestion de projet", "CPL"]
))

save("cpl/business_strategy/go_to_market_advanced.json", ku(
    "knowledges.cpl.business_strategy.go_to_market_advanced",
    "Go-to-Market avancé — lancer une nouvelle offre conseil",
    "high",
    "Stratégie complète pour lancer une nouvelle offre de conseil sur le marché : ciblage, positionnement, canaux, pricing, séquençage et métriques de validation.",
    "Un Go-to-Market (GTM) conseil est le plan d'introduction d'une nouvelle offre sur le marché, définissant à qui, comment, à quel prix et dans quel ordre l'offre sera présentée, avec des hypothèses à valider et des jalons de décision.",
    {"composantes": {"segment_cible": "ICP précis — secteur, taille, maturité, budget", "proposition_valeur": "Ce que l'offre résout que les alternatives ne résolvent pas", "canaux": "Comment atteindre l'ICP (réseau, contenu, événements, partenariats)", "prix": "Modèle et niveau — cohérent avec la valeur perçue par l'ICP", "sequencement": "Ordre de déploiement — souvent commencer par le réseau existant"},
     "hypotheses_a_tester": ["L'ICP a vraiment ce problème", "Il est prêt à payer pour le résoudre", "Notre approche est crédible pour lui", "Notre canal l'atteint"],
     "mvp_conseil": "Avant de formaliser l'offre : faire une mission pilote à prix réduit avec un client volontaire pour valider l'approche et produire une référence",
     "metriques_validation": {"traction": "Taux de conversion des premiers contacts en mission", "satisfaction": "NPS sur la mission pilote", "referral": "Est-ce que le client pilote recommande ?"}},
    [{"prompt": "Je veux lancer une nouvelle offre. Par où commencer ?", "answer": "Avant de créer l'offre formelle : faire une mission pilote. Propose à 2-3 clients existants ou prospects proches une mission expérimentale à tarif préférentiel contre feedback détaillé. Tu valides l'approche, tu crées une référence, et tu affines la proposition de valeur avant d'investir dans le marketing. C'est le chemin le plus court vers un GTM solide."},
     {"prompt": "Comment fixer le prix d'une nouvelle offre ?", "answer": "Trois ancrages : 1) Valeur créée pour le client (idéalement quantifiable). 2) Alternatives qu'il a (concurrents, faire en interne, ne rien faire). 3) Votre positionnement souhaité (premium, milieu, accessible). Pour une nouvelle offre sans référence : commencer par ancrer sur la valeur, puis calibrer par des conversations directes (\"est-ce que ce niveau de tarif serait envisageable pour vous ?\")."}],
    {"tone": "stratégique, orienté validation rapide", "structure": ["composantes", "hypothèses", "MVP", "métriques"], "avoid": ["trop théorique", "négliger la validation terrain"]},
    ["go-to-market", "lancement", "offre", "conseil", "positionnement", "CPL", "GTM"]
))

save("cpl/business_strategy/innovation_portfolio_management.json", ku(
    "knowledges.cpl.business_strategy.innovation_portfolio_management",
    "Gestion de portefeuille d'innovation — équilibrer exploration et exploitation",
    "medium",
    "Comment structurer et arbitrer entre initiatives d'innovation à différents horizons (core, adjacent, transformationnel) pour sécuriser la croissance à court terme tout en investissant dans le futur.",
    "La gestion de portefeuille d'innovation est le processus d'allocation stratégique des ressources entre des initiatives à différents niveaux de maturité et d'ambition, en maintenant un équilibre entre l'optimisation du business existant et l'exploration de nouvelles opportunités.",
    {"modele_horizons": {"h1": "Core — améliorer l'existant (70% des ressources en moyenne)", "h2": "Adjacent — étendre à des marchés ou offres proches (20%)", "h3": "Transformationnel — explorer des disruptions futures (10%)"},
     "arbitrages": {"risque": "H1 risque faible, H3 risque élevé — équilibrer selon la solidité du H1", "time_to_return": "H1 < 1 an, H2 1-3 ans, H3 3-10 ans", "indicateurs": "H1 : rentabilité / H2 : traction marché / H3 : apprentissages"},
     "pieges": {"surponderer_h1": "Optimiser uniquement l'existant — croissance court terme mais déclin long terme", "trop_h3": "Trop d'exploration sans rentabilité — cash drain", "oublier_h2": "H2 est souvent le meilleur chemin de croissance et le moins bien financé"},
     "pour_cabinet_conseil": "H1 = missions récurrentes dans le cœur de métier. H2 = nouvelles offres ou nouveaux secteurs adjacents. H3 = nouvelles modalités (produit, SaaS, formation)."},
    [{"prompt": "Comment trouver le temps pour innover quand on est à 100% en mission ?", "answer": "Le problème est structurel : si 100% du temps est en H1, il n'y a pas d'espace pour H2/H3. Solution : réserver explicitement un budget temps (1 jour/semaine ou une semaine par mois) pour l'innovation, et le traiter comme un engagement client — non-déplaçable. Sans cette réservation, l'opérationnel occupera toujours tout l'espace."},
     {"prompt": "On a trop d'idées d'innovation, comment prioriser ?", "answer": "Matrice simple : impact potentiel × probabilité de succès × time-to-value. Les idées H2 avec impact fort, bonne probabilité et retour < 2 ans passent en premier. Les H3 intéressantes mais lointaines : les noter, les surveiller, les lancer seulement quand le H1 est solide et le H2 en croissance."}],
    {"tone": "stratégique, équilibré", "structure": ["modèle", "arbitrages", "pièges", "cabinet conseil"], "avoid": ["jargon sans définition", "ignorer les contraintes de taille"]},
    ["innovation", "portefeuille", "horizons", "croissance", "exploration", "exploitation", "CPL"]
))

save("cpl/business_strategy/market_segmentation_strategy.json", ku(
    "knowledges.cpl.business_strategy.market_segmentation_strategy",
    "Segmentation de marché — choisir et prioriser ses segments cibles",
    "high",
    "Méthodes pour découper un marché en segments homogènes, évaluer l'attractivité de chacun et choisir sur lesquels concentrer ses ressources.",
    "La segmentation de marché est le processus de division d'un marché en groupes de clients homogènes selon des critères pertinents (besoins, comportements, caractéristiques), afin de cibler les segments les plus attractifs avec des propositions de valeur adaptées.",
    {"criteres_b2b": {"firmographiques": "Secteur, taille, localisation, maturité digitale", "comportementaux": "Fréquence d'achat, canaux utilisés, processus de décision", "besoins": "Problèmes prioritaires, critères de succès", "valeur": "Budget disponible, lifetime value potentielle"},
     "evaluation_attractivite": {"taille": "Marché suffisamment grand pour justifier l'effort", "accessibilite": "On peut l'atteindre avec nos canaux", "competitivite": "Pas trop encombré ou dominé par des acteurs indélogeable", "alignement": "Correspond à nos compétences distinctives"},
     "niche_vs_large": {"niche": "Offre spécialisée, prix premium, référence forte, moindre concurrence", "large": "Volume, prix compétitif, effort marketing élevé, différenciation difficile"},
     "recommandation_conseil": "Pour un cabinet indépendant : commencer par 1-2 segments très précis plutôt que viser large. L'expertise sectorielle est un avantage concurrentiel majeur en conseil."},
    [{"prompt": "Comment choisir sur quel marché se concentrer ?", "answer": "Croiser deux questions : où es-tu déjà crédible (références, expertise) ? Et où le besoin est fort et le marché accessible ? L'intersection est ton segment prioritaire. Erreur fréquente : choisir le segment le plus grand plutôt que celui où tu as le plus d'avantage. Mieux vaut 30% d'un petit segment que 1% d'un grand."},
     {"prompt": "Faut-il se spécialiser ou rester généraliste ?", "answer": "Pour un cabinet solo ou small team en conseil : spécialisation forte recommandée. La spécialisation permet un tarif premium (expertise rare), une prospection plus efficace (message clair), et une réputation qui se construit. La généralisation est un avantage pour les grands cabinets qui peuvent assembler des équipes — pas pour les indépendants qui sont eux-mêmes le produit."}],
    {"tone": "stratégique, orienté décision", "structure": ["critères", "évaluation", "niche vs large", "recommandation"], "avoid": ["trop académique", "ignorer la réalité d'un cabinet indépendant"]},
    ["segmentation", "marché", "ciblage", "niche", "spécialisation", "conseil", "CPL"]
))

save("cpl/business_strategy/pricing_psychology.json", ku(
    "knowledges.cpl.business_strategy.pricing_psychology",
    "Psychologie du prix en conseil — ancrer, positionner, défendre",
    "high",
    "Comment les biais cognitifs influencent la perception du prix en B2B, et comment les utiliser pour présenter, ancrer et défendre son tarif sans brader.",
    "La psychologie du prix en conseil désigne l'application des principes de psychologie cognitive et comportementale à la fixation, la présentation et la négociation du prix des missions, en reconnaissant que la valeur perçue est construite autant que réelle.",
    {"biais_a_connaitre": {"ancrage": "Le premier chiffre cité influence toute la négociation — toujours ancrer haut", "effet_de_contraste": "Présenter une option chère avant l'option cible la fait paraître raisonnable", "prix_ronds": "Les prix ronds (10 000€) signalent une estimation ; les prix précis (9 850€) signalent un calcul réel", "endowment": "Ce qu'on possède déjà on le survalue — ancrer sur le coût du statu quo"},
     "presentation": {"value_first": "Toujours présenter la valeur avant le prix — jamais le contraire", "options": "Proposer 3 options (petite, standard, premium) : la majorité choisit le milieu", "framing_investissement": "\"Cet investissement\" plutôt que \"ce coût\" — change la perception"},
     "defense_du_prix": {"ne_pas_baisser_d_emblee": "Une concession immédiate signale que le prix était gonflé", "contrer_par_la_valeur": "\"Qu'est-ce qui vous fait dire que c'est trop cher ?\" — ramener à la valeur", "baisser_le_scope": "Si pression forte : réduire le périmètre, pas le taux journalier"}},
    [{"prompt": "Mon prospect dit que c'est trop cher. Que répondre ?", "answer": "D'abord une question : \"Trop cher par rapport à quoi ?\" La réponse révèle si c'est un problème de budget (il n'a pas les moyens), de valeur perçue (il ne voit pas le ROI), ou de comparaison (il a un concurrent moins cher). Chaque cas a une réponse différente. Ne jamais baisser le prix avant de savoir lequel des trois c'est."},
     {"prompt": "Comment présenter mon tarif pour qu'il soit bien reçu ?", "answer": "Séquence : d'abord le problème (valider avec le client), ensuite l'impact chiffré si possible, ensuite l'approche, enfin le tarif. Jamais l'inverse. Et ancrer : si tu proposes 15K, mentionner d'abord ce que ça éviterait (coût du statu quo, coût de faire en interne, benchmark marché). Le chiffre qui vient après ces références paraît toujours plus raisonnable."}],
    {"tone": "pragmatique, orienté technique de négociation", "structure": ["biais", "présentation", "défense"], "avoid": ["manipulation excessive", "négliger la vraie valeur"]},
    ["prix", "négociation", "psychologie", "ancrage", "valeur", "conseil", "CPL"]
))

save("cpl/business_strategy/product_service_hybrid_model.json", ku(
    "knowledges.cpl.business_strategy.product_service_hybrid_model",
    "Modèle hybride produit-service — passer du conseil pur au productisé",
    "medium",
    "Comment un cabinet de conseil peut créer des offres productisées (formations, outils, templates, abonnements) à côté des missions traditionnelles pour diversifier et scalabiliser les revenus.",
    "Le modèle hybride produit-service désigne la stratégie par laquelle un prestataire de services intellectuels crée des actifs productisés (méthodes packagées, formations, outils, contenus premium) qui génèrent des revenus partiellement ou totalement décorrélés du temps passé.",
    {"types_offres_productisees": {"formation": "Programme structuré livré en présentiel, distanciel ou e-learning", "templates_methodes": "Documents, frameworks, outils packagés et vendus", "abonnement_conseil": "Accès à des heures de conseil ou à une communauté sur abonnement mensuel", "diagnostic_fixe": "Mission scoped à périmètre fixe et prix fixe — plus scalable que la régie"},
     "avantages": ["Revenus actifs vs revenus passifs", "Levier : vendre le même contenu plusieurs fois", "Crédibilité : l'IP matérialisée renforce la légitimité", "Entrée de gamme : permet aux clients à budget réduit d'accéder à la marque"],
     "sequencement": "1) Consolider un positionnement fort en service. 2) Identifier les éléments répétitifs de son travail. 3) Productiser d'abord ce qui a déjà été prouvé avec des clients réels. 4) Tester avec un petit groupe avant de lancer.",
     "risques": ["Cannibalisation du service premium", "Temps de création élevé vs revenus incertains", "Nécessite des compétences marketing et digitales différentes"]},
    [{"prompt": "Comment créer une formation à partir de mes missions conseil ?", "answer": "Partir de ce que tu expliques à chaque client : les concepts que tu réexpliques toujours, les frameworks que tu reconstruis à chaque fois, les erreurs que tu vois partout. C'est là que vit ta formation. Format minimal viable : 3-5 modules de 45 min, testés d'abord en live avec un groupe de 5-10 personnes, avant tout enregistrement."},
     {"prompt": "Je veux des revenus moins dépendants de mon temps. Par où commencer ?", "answer": "Deux chemins selon ton positionnement : 1) Le diagnostic packagé — mission à périmètre et prix fixes (ex : audit en 3 jours pour 5K€ avec livrable standard). Moins scalable mais plus simple à lancer. 2) La formation ou le contenu premium — plus de temps à créer mais peut générer des revenus récurrents. Commencer par le diagnostic packagé : tu testes le marché avec moins de risque."}],
    {"tone": "entrepreneurial, pragmatique", "structure": ["types d'offres", "avantages", "séquençage", "risques"], "avoid": ["trop ambitieux trop vite", "négliger les risques"]},
    ["productisation", "hybride", "service", "formation", "scalabilité", "revenus", "CPL"]
))

save("cpl/business_strategy/recurring_revenue_models.json", ku(
    "knowledges.cpl.business_strategy.recurring_revenue_models",
    "Modèles de revenus récurrents en conseil — abonnements et retainers",
    "high",
    "Comment structurer des modèles de revenus récurrents pour un cabinet de conseil : retainers, abonnements, forfaits mensuels — avec les conditions de succès et les erreurs à éviter.",
    "Les revenus récurrents en conseil désignent des modèles contractuels dans lesquels le client s'engage sur une durée (mensuelle, trimestrielle, annuelle) pour un accès ou un volume de services défini, créant une prévisibilité de revenus supérieure aux missions ponctuelles.",
    {"modeles": {"retainer_classique": "X jours/mois réservés, facturés qu'ils soient utilisés ou non — prévisibilité maximale", "retainer_flexible": "Accès sur demande jusqu'à un plafond mensuel — plus souple pour le client", "abonnement_conseil": "Accès à des sessions de conseil structurées sur abonnement — scalable", "forfait_maintenance": "Suivi de l'implémentation post-mission — prolonge naturellement la relation"},
     "conditions_de_succes": ["Le client a un besoin continu, pas ponctuel", "La valeur est perçue comme supérieure à des missions ad hoc", "Le scope est clair — ce qui est inclus et ce qui ne l'est pas", "Le client utilise réellement le service — sinon il annule"],
     "pricing_retainer": "Entre 50% et 80% du TJM habituel — compensation par la sécurité du revenu",
     "erreurs_frequentes": ["Retainer trop large sans scope clair — friction et dépassements", "Sous-pricer pour obtenir la signature — margin squeeze", "Ne pas renouveler activement — le retainer s'éteint par inertie"]},
    [{"prompt": "Comment proposer un retainer à un client ?", "answer": "Timing idéal : vers la fin d'une mission réussie, quand le client voit la valeur. Proposition naturelle : \"Pour maintenir ces gains et continuer à avancer, on pourrait structurer un accompagnement mensuel. X jours par mois me permettraient de [bénéfice concret].\" Toujours proposer un périmètre clair et une durée minimale (3-6 mois) — pas un engagement à vie."},
     {"prompt": "Un client annule son retainer, comment éviter ça ?", "answer": "Les retainers s'annulent quand le client ne voit plus la valeur. Mesures préventives : compte-rendu mensuel qui liste explicitement ce qui a été fait et son impact, point de renouvellement à 3 mois pour ajuster le scope si besoin, et toujours avoir une \"prochaine étape\" claire dans la relation. Un retainer sans momentum visible s'éteint."}],
    {"tone": "commercial, pragmatique", "structure": ["modèles", "conditions", "pricing", "erreurs"], "avoid": ["trop commercial", "négliger la valeur réelle pour le client"]},
    ["revenus récurrents", "retainer", "abonnement", "MRR", "conseil", "CPL", "fidélisation"]
))

save("cpl/business_strategy/resource_optimization.json", ku(
    "knowledges.cpl.business_strategy.resource_optimization",
    "Optimisation des ressources — faire plus avec moins en cabinet",
    "medium",
    "Méthodes pour maximiser l'efficience d'un cabinet de conseil : automatisation, délégation, priorisation des tâches à haute valeur, et élimination des activités à faible ROI.",
    "L'optimisation des ressources en cabinet de conseil est le processus d'allocation maximalement efficiente du capital humain, financier et temporel disponible, en éliminant les gaspillages, en automatisant les tâches répétitives et en concentrant l'effort là où la valeur créée est la plus haute.",
    {"levier_temps": {"time_tracking": "Mesurer où part le temps avant d'optimiser — sans données, pas d'amélioration", "high_value_activities": "Identifier les 20% d'activités qui génèrent 80% de la valeur — y concentrer", "elimination": "Supprimer les tâches à faible valeur — pas les déléguer, les éliminer"},
     "levier_automatisation": {"administratif": "Facturation, relances, templates, scheduling — automatisables", "contenu": "Réutilisation des livrables (templates, frameworks) — ne pas recréer à chaque fois", "outils": "CRM simple, gestion de projet, comptabilité — réduire la charge mentale"},
     "levier_delegation": {"sous_traitance": "Déléguer les tâches hors de son core (graphisme, mise en page, recherche)", "freelancers": "Réseau de spécialistes mobilisables selon le besoin"},
     "metriques": {"taux_facture": "% du temps vendu vs temps total disponible — objectif 60-70% pour préserver du temps développement", "cout_par_livrable": "Temps × TJM — comparer d'une mission à l'autre pour identifier les gains"}},
    [{"prompt": "J'ai l'impression de passer trop de temps sur des tâches non-facturables.", "answer": "D'abord mesurer pendant 2 semaines : note chaque activité par catégorie (mission, dev commercial, admin, formation, autre). Tu verras souvent que l'admin et la compta prennent 3-4x plus de temps que prévu. Ensuite : automatiser (comptabilité, facturation), supprimer ou déléguer (mise en page, recherche documentaire), batching (regrouper les emails et admin en 2 plages par semaine plutôt que tout le temps)."},
     {"prompt": "Comment facturer plus sans travailler plus ?", "answer": "Deux leviers sans augmenter les heures : 1) Augmenter le tarif — plus difficile sur les clients existants, plus simple sur les nouveaux. 2) Améliorer le mix : réduire les missions à faible marge (junior, administratif) au profit des missions à forte valeur ajoutée. L'optimisation des ressources crée l'espace pour ce shift."}],
    {"tone": "pragmatique, orienté résultats", "structure": ["leviers", "automatisation", "métriques"], "avoid": ["théorie sans application", "liste exhaustive"]},
    ["efficience", "ressources", "temps", "automatisation", "délégation", "cabinet", "CPL"]
))

save("cpl/business_strategy/saas_transition_strategy.json", ku(
    "knowledges.cpl.business_strategy.saas_transition_strategy",
    "Transition vers un modèle SaaS — du conseil au logiciel",
    "medium",
    "Stratégie pour un cabinet de conseil qui souhaite créer un produit logiciel (SaaS) à partir de sa méthodologie ou de ses outils — risques, séquençage et décisions critiques.",
    "La transition SaaS d'un cabinet de conseil est le processus par lequel une entreprise de services intellectuels crée un produit logiciel encodant tout ou partie de sa méthodologie, afin de générer des revenus scalables décorrélés du temps de livraison.",
    {"opportunites": ["Méthodologie reproductible et encodable", "Client qui a besoin de l'outil en autonomie", "Marché large pour un outil spécialisé", "IP différenciante qu'un logiciel protège mieux qu'un service"],
     "risques_majeurs": {"focus_split": "Gérer à la fois le conseil et le développement produit — rarement sustainable seul", "capital": "Le SaaS nécessite un investissement amont avant revenus", "competences": "Product management, développement, marketing SaaS ≠ conseil", "cannibalisation": "Le SaaS peut remplacer la demande de conseil"},
     "sequencement_recommande": ["Valider le problème avec le service conseil existant", "Productiser avec des outils no-code avant de coder", "Trouver des early adopters parmi les clients conseil", "Lever des fonds ou s'associer avec un CTO avant de scaler"],
     "modeles_hybrides": {"consulting_led": "Le conseil génère les revenus, le produit est un différenciateur", "product_led": "Le produit génère les revenus, le conseil est un upsell", "pur_saas": "Le conseil est abandonné ou marginalisé"}},
    [{"prompt": "Je veux créer un SaaS à partir de ma méthode conseil. Par où commencer ?", "answer": "Avant de coder quoi que ce soit : valider que des clients paieraient pour un outil (pas juste pour le conseil). Test rapide : créer une version manuelle ou no-code (Airtable, Notion, Google Sheets) et la vendre à 3-5 clients. Si ça marche et qu'ils veulent plus d'automatisation, tu as validé le marché. Si ça ne se vend pas en manuel, ça ne se vendra pas en SaaS."},
     {"prompt": "Faut-il arrêter le conseil pour lancer un SaaS ?", "answer": "Presque jamais au début. Le conseil finance le développement, génère des revenus pendant la phase de croissance du SaaS, et produit les insights produit. Arrêter trop tôt crée une pression financière qui force de mauvaises décisions produit. Le modèle consulting-led (conseil dominant, SaaS en développement) est le plus safe pour les 2-3 premières années."}],
    {"tone": "entrepreneurial, réaliste sur les risques", "structure": ["opportunités", "risques", "séquençage", "modèles"], "avoid": ["sur-romantiser le SaaS", "négliger les compétences nécessaires"]},
    ["SaaS", "logiciel", "transition", "productisation", "scalabilité", "conseil", "CPL"]
))

save("cpl/business_strategy/service_margin_management.json", ku(
    "knowledges.cpl.business_strategy.service_margin_management",
    "Gestion des marges en cabinet de conseil — analyser et améliorer la rentabilité",
    "high",
    "Comment analyser la rentabilité réelle d'une mission ou d'un client, identifier les leviers d'amélioration des marges et prendre des décisions éclairées sur le portefeuille missions.",
    "La gestion des marges en cabinet de conseil désigne le suivi et l'optimisation de la différence entre les revenus générés par les missions et les coûts directs et indirects associés, avec pour objectif de maintenir une rentabilité suffisante pour financer la croissance et rémunérer les associés.",
    {"calcul_marge_mission": {"revenus": "Honoraires facturés sur la mission", "cout_direct": "Temps consultant × coût horaire + frais refacturables", "marge_brute": "Revenus - coûts directs", "taux_marge_cible": "En conseil indépendant : 60-75% de marge brute est standard"},
     "leviers_amelioration": {"prix": "Augmenter le tarif — impact le plus fort mais le plus difficile", "efficience": "Réduire le temps de livraison sans réduire la qualité", "mix_clients": "Arbitrer vers les clients à meilleure marge"},
     "analyse_par_client": "Calculer régulièrement la marge par client — certains \"bons\" clients sont en réalité les moins rentables (demandes excessives, paiement lent, scope creep)",
     "danger_sous_estimation": "Les missions forfaitaires à prix fixe sont à risque — chaque heure supplémentaire grignote la marge. Suivi du temps même en forfait."},
    [{"prompt": "Comment savoir si une mission est vraiment rentable ?", "answer": "En tenant un compte de résultat par mission : honoraires - temps passé × ton coût horaire réel (y compris le temps de commercialisation) - frais. La surprise est souvent là : les missions qui semblent les plus rentables à la signature sont parfois les moins rentables à la livraison (scope creep, révisions non prévues). Tracker le temps même en forfait."},
     {"prompt": "Un client prend beaucoup de temps mais paie bien. Il est rentable ?", "answer": "Ça dépend du ratio temps/honoraires. Calcul : honoraires ÷ heures totales = taux horaire effectif. Compare à ton TJM cible. Si le taux effectif est inférieur à ton TJM / 8, la mission est sous-rentable malgré les honoraires élevés. Le volume ne compense pas toujours la demande."}],
    {"tone": "financier, concret, orienté décision", "structure": ["calcul", "leviers", "analyse client", "risques"], "avoid": ["trop comptable", "ignorer la dimension qualitative"]},
    ["marge", "rentabilité", "finances", "conseil", "CPL", "TJM", "mission"]
))

save("cpl/business_strategy/strategic_decision_framework.json", ku(
    "knowledges.cpl.business_strategy.strategic_decision_framework",
    "Cadre de décision stratégique — prendre des décisions d'entreprise importantes",
    "high",
    "Framework structuré pour prendre des décisions stratégiques majeures (lancer une offre, entrer sur un marché, recruter, investir) avec un processus reproductible et documenté.",
    "Un cadre de décision stratégique est un processus structuré qui guide la prise de décisions à fort enjeu en définissant les questions clés, les critères d'évaluation, les informations nécessaires et la logique de choix, réduisant le biais et améliorant la traçabilité.",
    {"etapes": {"1_definir": "Quelle est la vraie décision à prendre ? (souvent différente de la formulation initiale)", "2_criteres": "Sur quels critères on évalue ? Dans quel ordre de priorité ?", "3_options": "Quelles sont les options réalistes ? (inclure \"ne rien faire\")", "4_informations": "Quelles données manquent et sont critiques pour décider ?", "5_evaluation": "Évaluer chaque option sur chaque critère", "6_decision": "Décider et documenter le raisonnement"},
     "outils": {"matrice_decision": "Options en lignes, critères en colonnes, scores pondérés", "premortem": "Pour chaque option : imaginer l'échec dans 2 ans et identifier les causes", "reversibilite": "Évaluer si la décision est réversible — plus d'urgence sur l'irréversible"},
     "erreurs_frequentes": ["Décider avant de définir correctement les critères", "Ignorer l'option de ne rien faire", "Chercher la confirmation après avoir décidé"],
     "documentation": "Documenter les décisions stratégiques — raisons du choix, alternatives écartées, hypothèses. Revenir dans 6-12 mois pour valider."},
    [{"prompt": "Comment décider si je dois recruter ou rester solo ?", "answer": "Cadre simple pour cette décision : 1) Est-ce que le manque de ressource me fait perdre des missions ou de la qualité ? 2) Est-ce que j'ai un pipeline suffisamment stable pour financer un recrutement sur 12 mois ? 3) Est-ce que je veux gérer des personnes (pas seulement déléguer des tâches) ? Si les trois sont oui, le recrutement est logique. Si un seul est non, explorer d'abord la sous-traitance ponctuelle."},
     {"prompt": "Je dois prendre une décision importante et je tourne en rond.", "answer": "Signal que le processus n'est pas structuré. Essai : 1) Écris la décision en une phrase. 2) Liste les 3 critères les plus importants pour toi. 3) Pour chaque option, note 1-5 sur chaque critère. 4) Lis le résultat — si tu es tenté d'ignorer la note pour suivre ton intuition, c'est que tu as un critère implicite non listé. Expliciter ce critère résout souvent le blocage."}],
    {"tone": "structurant, orienté action", "structure": ["étapes", "outils", "erreurs", "documentation"], "avoid": ["trop académique", "listes sans logique de choix"]},
    ["décision", "stratégie", "framework", "priorisation", "conseil", "CPL", "leadership"]
))

save("cpl/business_strategy/value_based_pricing.json", ku(
    "knowledges.cpl.business_strategy.value_based_pricing",
    "Pricing basé sur la valeur — tarifer selon la valeur créée",
    "high",
    "Passage d'un tarif au temps passé (TJM) à un tarif basé sur la valeur créée pour le client — méthodes, conditions et conversation commerciale.",
    "Le value-based pricing est une stratégie de tarification dans laquelle le prix est fixé en fonction de la valeur créée pour le client (impact économique, risque évité, gain de temps) plutôt qu'en fonction du coût de production ou du temps passé.",
    {"fondement": "Si une mission de 5 jours permet au client d'économiser 200K€, le TJM ne reflète pas la valeur — la valeur potentielle justifie un prix bien supérieur",
     "methodes_calcul_valeur": {"gain_direct": "Chiffre d'affaires additionnel généré, coût évité, productivité gagnée", "risque_evite": "Coût potentiel d'un incident évité × probabilité", "cout_alternative": "Combien ça coûterait de le faire en interne ou avec un concurrent ?"},
     "conditions": ["Le client doit accepter de partager les données permettant de calculer la valeur", "L'impact doit être mesurable ou estimable", "Il faut une confiance suffisante pour avoir cette conversation"],
     "conversation_commerciale": {"question_cle": "\"Si on résout ce problème, quel impact ça aurait pour votre organisation ?\"", "ancrage": "Partir de l'impact chiffré avant de parler du prix", "partage": "\"Notre tarif est X€ — si l'impact est Y, c'est un ROI de Z\""},
     "risques": ["Surestimer la valeur perçue", "Client qui refuse la transparence sur l'impact", "Relation de confiance insuffisante pour avoir la conversation"]},
    [{"prompt": "Comment passer du TJM au value-based pricing ?", "answer": "Progressivement. Commencer par estimer la valeur en interne, sans le dire au client. Puis commencer à poser la question de l'impact dans la phase de cadrage : \"Si on réussit ça, quel effet sur votre business ?\" Ça prépare le terrain. Pour les prochaines propositions : présenter l'impact estimé avant le prix, et formuler le prix en ROI. La transition prend du temps — c'est un changement de posture, pas juste de calcul."},
     {"prompt": "Mon client ne veut pas parler d'impact, seulement de prix.", "answer": "Souvent signe que la relation de confiance n'est pas encore là, ou que l'acheteur est un purchasing manager sans lien avec la valeur business. Dans ce cas, travailler à faire monter la conversation au niveau du commanditaire réel (DG, DAF), qui lui parle naturellement d'impact. Avec un acheteur pur prix, le value-based pricing est difficile à appliquer."}],
    {"tone": "commercial, stratégique", "structure": ["fondement", "calcul valeur", "conversation", "risques"], "avoid": ["théorie sans la conversation commerciale", "ignorer les obstacles relationnels"]},
    ["pricing", "valeur", "TJM", "tarification", "ROI", "conseil", "CPL"]
))

print("\n=== cpl/business_strategy : 15 KU sauvegardés ===")
