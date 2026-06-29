"""
Enrichissement Knowledge Base ALFRED - Batch 11 : cpl/business_strategy (15 restants)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

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
# cpl / business_strategy (15 restants)
# =============================================================================

save("cpl/business_strategy/partnership_strategy.json", ku_bs(
  "partnership_strategy",
  "Stratégie de partenariats",
  "Les partenariats stratégiques accélèrent la croissance en partageant des ressources, des canaux ou des compétences complémentaires. Leur succès dépend de la complémentarité des intérêts, de la clarté des accords et d'un suivi rigoureux.",
  "La stratégie de partenariats est l'ensemble des décisions et des pratiques permettant à une entreprise de créer des relations formelles avec d'autres organisations pour partager des ressources, des marchés ou des compétences dans un objectif de croissance mutuelle.",
  {
    "partnership_types": [
      {"type": "Partenariat commercial / Go-to-market", "description": "Co-selling, bundling, recommandations croisées", "value": "Accès à de nouveaux marchés ou clients"},
      {"type": "Partenariat technologique / Intégrations", "description": "Connexion entre produits complémentaires", "value": "Enrichir l'offre sans développer en interne"},
      {"type": "Partenariat de distribution / Channel", "description": "Revendeurs, agents, distributeurs", "value": "Extension de la force de vente sans embauche"},
      {"type": "Partenariat stratégique / Alliance", "description": "Co-développement, joint-venture, licence", "value": "Partage de risque sur des initiatives importantes"}
    ],
    "partnership_success_factors": [
      "Complémentarité claire (pas de compétition sur le core business)",
      "Accord sur les objectifs, les responsabilités et le partage de valeur",
      "Champion dédié de chaque côté",
      "Métriques partagées et revues régulières",
      "Clauses de sortie claires (exit sans dommage si pas de valeur)"
    ],
    "common_pitfalls": [
      "Déséquilibre des engagements (un partenaire met beaucoup plus que l'autre)",
      "Concurrence cachée (les produits sont plus complémentaires en théorie qu'en pratique)",
      "Manque de champion — le partenariat est annoncé mais personne ne le pousse",
      "Accord mal structuré — ambiguïté sur les revenus partagés et les responsabilités"
    ]
  },
  [
    {"prompt": "Comment structurer un partenariat commercial avec une autre entreprise tech ?", "answer": "Cinq éléments contractuels clés : (1) Périmètre de collaboration (quels produits, quels marchés, quelle exclusivité éventuelle), (2) Engagement réciproque (que s'engage à faire chaque partie : X introductions/mois, Y formations, etc.), (3) Partage de revenu (si co-vente : qui facture, comment le revenu est divisé), (4) Métriques de succès et fréquence de revue, (5) Conditions de résiliation (délai de préavis, gestion des clients communs). Conseil : commencer petit (pilote 3 mois) avant l'accord large."},
    {"prompt": "Comment identifier les bons partenaires pour mon activité ?", "answer": "Critères : (1) Complémentarité produit (votre solution + la leur = plus de valeur pour le client commun), (2) Segment client aligné (même acheteur, même problème), (3) Taille compatible (un partenaire 10x plus grand ne s'intéressera pas à vous), (4) Absence de concurrence core. Méthode : mapper les outils/services que vos clients utilisent à côté de votre solution — ceux qui reviennent le plus souvent sont vos partenaires naturels."}
  ],
  ["partenariats", "co-vente", "alliances", "channel", "business development"]
))

save("cpl/business_strategy/go_to_market_strategy.json", ku_bs(
  "go_to_market_strategy",
  "Stratégie Go-to-Market",
  "La stratégie Go-to-Market définit comment une offre arrive sur son marché cible : qui sont les clients prioritaires, par quels canaux les atteindre, avec quel message, et dans quel ordre géographique ou sectoriel se déployer.",
  "La stratégie Go-to-Market (GTM) est le plan d'action qui définit comment une entreprise ou un produit va atteindre son marché cible, engager ses clients et générer du revenu — en couvrant la segmentation, le positionnement, les canaux de distribution, le modèle de vente et la stratégie de lancement.",
  {
    "gtm_components": [
      {"component": "Segmentation et ICP", "description": "Ideal Customer Profile — le client type pour lequel la valeur est la plus claire et la plus forte", "importance": "Le ICP trop large dilue les efforts — commencer narrow"},
      {"component": "Message", "description": "La promesse de valeur adaptée à l'ICP — ce qui résonne avec leurs douleurs spécifiques", "importance": "Le même produit a des messages différents selon les segments"},
      {"component": "Canaux", "description": "Comment atteindre l'ICP (outbound, inbound, events, referrals, partenariats)", "importance": "Les canaux dépendent du profil de l'acheteur"},
      {"component": "Motion de vente", "description": "Self-serve, transactionnel, entreprise — adapté au prix et à la complexité", "importance": "Un produit à 50€/mois ne supporte pas une motion enterprise"},
      {"component": "Séquence de déploiement", "description": "Segment pilot → optimisation → scaling. Commencer par le segment le plus facile à convaincre", "importance": "Un win early donne des références et affine le message"}
    ],
    "icp_definition": {
      "dimensions": ["Secteur", "Taille d'entreprise", "Stade de croissance", "Maturité sur le problème résolu", "Budget disponible", "Décideur type (titre, priorités)"],
      "sources": "Analyser les 20 meilleurs clients existants (les plus rentables, les plus satisfaits, les plus faciles à servir) — leurs points communs définissent l'ICP."
    }
  },
  [
    {"prompt": "Comment définir mon ICP (Ideal Customer Profile) pour ma solution IA ?", "answer": "Partir des clients existants les plus satisfaits et les plus profitables. Questions : quel secteur, quelle taille d'équipe, quel titre de l'acheteur principal, quel problème spécifique ta solution résout-elle pour eux, pourquoi t'ont-ils choisi plutôt qu'un concurrent ? Les patterns communs à tes meilleurs clients = ton ICP. Pour une solution IA professionnelle : typiquement un segment qui a déjà une maturité data (ne pas évangéliser l'IA de zéro), un budget IT > X, et un champion technique en interne."},
    {"prompt": "Dans quel ordre lancer un produit sur plusieurs marchés géographiques ?", "answer": "Commencer par le marché le plus accessible et le plus représentatif. Pour une solution française : France d'abord pour apprendre, affiner le message, construire des références. Puis pays francophones (Belgique, Suisse, Canada) qui utilisent le même message sans adaptation majeure. Puis DACH ou UK (nécessitent adaptation culturelle et linguistique). Ne pas attaquer 5 pays simultanément — disperser les efforts sans profondeur dans aucun. L'internationalisation séquentielle permet d'apprendre et de financer chaque étape."}
  ],
  ["GTM", "go-to-market", "ICP", "canaux", "lancement"]
))

save("cpl/business_strategy/market_entry_strategy.json", ku_bs(
  "market_entry_strategy",
  "Stratégie d'entrée sur un marché",
  "L'entrée sur un nouveau marché (géographique, sectoriel ou de segment) requiert d'analyser l'attractivité du marché, les barrières à l'entrée, les modes d'entrée possibles et le séquençage optimal pour minimiser le risque.",
  "La stratégie d'entrée sur un marché est l'ensemble des décisions définissant comment et dans quel ordre une entreprise pénètre un nouveau marché — incluant le choix du mode d'entrée (organique, acquisition, partenariat), la segmentation prioritaire, le positionnement adapté et les ressources allouées.",
  {
    "market_entry_modes": [
      {"mode": "Organique", "description": "Développer soi-même la présence sur le nouveau marché", "pros": ["Contrôle total", "Coût d'entrée graduel"], "cons": ["Lent", "Manque de relations locales"]},
      {"mode": "Acquisition", "description": "Acheter un acteur local existant", "pros": ["Rapide", "Marché, équipe et clients inclus"], "cons": ["Coût élevé", "Risque d'intégration"]},
      {"mode": "Partenariat / JV", "description": "S'associer avec un acteur local qui apporte le marché", "pros": ["Partage du risque", "Accès rapide au marché"], "cons": ["Partage de la valeur", "Dépendance au partenaire"]},
      {"mode": "Franchise / Licence", "description": "Céder le modèle à des opérateurs locaux", "pros": ["Scalable", "Capital-light"], "cons": ["Perte de contrôle qualité"]}
    ],
    "entry_analysis": [
      "Taille du marché et taux de croissance",
      "Intensité concurrentielle (incumbents en place, maturity)",
      "Barrières réglementaires ou culturelles",
      "Coût d'acquisition client spécifique au marché",
      "Ressources nécessaires vs disponibles"
    ]
  },
  [
    {"prompt": "Comment évaluer si un nouveau marché sectoriel vaut la peine d'être adressé ?", "answer": "Quatre critères : (1) Taille et croissance (le marché est-il suffisamment grand et croît-il ?) — un marché trop petit ne supporte pas l'investissement d'entrée, (2) Fit produit (ton offre répond-elle à un vrai besoin non adressé dans ce secteur ?) — ne pas généraliser sans valider, (3) Barrières d'entrée (les acteurs établis ont-ils des avantages défendables ?) — réglementaire, relationnel, technique, (4) Unit economics (la structure de coûts de ce marché permet-elle une profitabilité ?) — prix acceptables, CAC supportable. Un score 3/4 est un signal d'exploration."},
    {"prompt": "Nous voulons aller sur le marché américain — par où commencer ?", "answer": "Séquence recommandée : (1) Valider le product-market fit sur un état ou une ville (NYC, SF, Boston — écosystèmes tech avancés), (2) Adapter le message (les américains achetent le ROI chiffré, pas les frameworks), (3) Recruter un sales US senior avec un réseau local — le réseau est la ressource principale en entrée de marché US, (4) Trouver un champion client américain avant de scaler. Erreur classique : aller aux US trop tôt avec un produit pas encore mature ou sans ressource locale dédiée."}
  ],
  ["marché", "entrée", "international", "expansion", "acquisition"]
))

save("cpl/business_strategy/revenue_model_design.json", ku_bs(
  "revenue_model_design",
  "Design du modèle de revenu",
  "Le modèle de revenu définit qui paye, pour quoi, comment (récurrent, transactionnel, par usage) et à quelle fréquence. Le bon modèle est aligné avec la valeur perçue et la structure du marché — il est rarement celui qui vient en premier.",
  "Le design du modèle de revenu est la conception délibérée des mécanismes par lesquels une entreprise capture une partie de la valeur qu'elle crée — incluant la définition des payeurs, des unités facturées, des niveaux de prix et des structures tarifaires (abonnement, transactionnel, usage, hybride).",
  {
    "revenue_models": [
      {"model": "Abonnement (SaaS)", "description": "Facturation récurrente mensuelle ou annuelle", "fit": "Valeur délivrée en continu, logiciel, services"},
      {"model": "Transaction / Commission", "description": "% ou montant fixe sur chaque transaction", "fit": "Marketplaces, paiements, intermédiation"},
      {"model": "Usage (pay-as-you-go)", "description": "Facturation proportionnelle à l'utilisation", "fit": "Infrastructure, APIs, tokens IA"},
      {"model": "Licence", "description": "Paiement unique pour le droit d'utilisation", "fit": "Logiciels traditionnels, IP, brevets"},
      {"model": "Freemium + upgrade", "description": "Version gratuite + version payante", "fit": "PLG, reach large, conversion sur usage"},
      {"model": "Marketplace / double-face", "description": "Facturation des deux côtés du marché", "fit": "Plateformes bifaces (offre + demande)"}
    ],
    "value_metric_alignment": "Le modèle de revenu doit être aligné sur la value metric — la dimension sur laquelle le client perçoit la valeur. Si la valeur croît avec les utilisateurs → per-seat. Si la valeur croît avec les transactions → commission. Désaligner modèle de revenu et valeur perçue crée de la friction à la vente.",
    "revenue_model_evolution": "Le modèle de revenu évolue avec la maturité du produit et du marché. Passage courant : licence unique → abonnement (prévisibilité) → usage-based (alignement valeur) → hybride."
  },
  [
    {"prompt": "Comment passer d'un modèle de projet ponctuel à un modèle d'abonnement récurrent en conseil ?", "answer": "Trois étapes : (1) Identifier ce que les clients ont besoin en continu (pas juste au projet) — accès à un expert, veille, mise à jour des livrables, support, (2) Packageer cette valeur continue en une offre mensuelle claire avec un périmètre défini (X heures, Y accès, Z livrables), (3) Convertir les clients existants en priorité — ils connaissent déjà la valeur. Prix : l'abonnement mensuel doit être perçu comme moins cher que le projet ponctuel équivalent pour faciliter la conversion, tout en étant plus rentable sur l'année pour toi."},
    {"prompt": "Quel modèle de revenu adopter pour un assistant IA comme ALFRED ?", "answer": "Modèles possibles : (1) Abonnement mensuel (freemium + premium) — simple, récurrent, scalable. (2) Usage-based sur les tokens LLM — aligné avec la valeur mais anxiogène pour l'utilisateur. (3) Hybride : abonnement de base + usage au-delà d'un quota — prévisibilité pour l'utilisateur, revenu croissant pour le produit. Pour un assistant personnel : l'abonnement est le plus simple à vendre et à gérer. Pour une offre B2B avec gros volumes : l'usage-based capture mieux la valeur."}
  ],
  ["modèle de revenu", "abonnement", "SaaS", "freemium", "pricing"]
))

save("cpl/business_strategy/strategic_planning_cycle.json", ku_bs(
  "strategic_planning_cycle",
  "Cycle de planification stratégique",
  "Le cycle de planification stratégique structure les moments d'analyse, de décision et d'alignement autour de la direction de l'entreprise — annuellement pour la stratégie, trimestriellement pour les OKRs, et hebdomadairement pour l'exécution.",
  "Le cycle de planification stratégique est le processus récurrent par lequel une organisation définit ses orientations, alloue ses ressources, décline des objectifs opérationnels et ajuste son plan en fonction des résultats — à différentes fréquences selon l'horizon.",
  {
    "planning_horizons": [
      {"horizon": "Stratégique (3-5 ans)", "frequency": "Annuelle", "focus": "Vision, positionnement marché, investissements majeurs, capacités à construire"},
      {"horizon": "Tactique / OKRs (1 an)", "frequency": "Annuelle avec révisions trimestrielles", "focus": "Objectifs annuels, priorités d'investissement, hiring plan"},
      {"horizon": "Opérationnel / Trimestriel", "frequency": "Trimestrielle", "focus": "OKRs Q, roadmap produit, budget alloué"},
      {"horizon": "Exécution / Sprint", "frequency": "Hebdomadaire ou bimensuelle", "focus": "Tâches, bloquants, résolutions"}
    ],
    "annual_planning_process": [
      "Bilan de l'année (résultats, apprentissages, surprises)",
      "Analyse de l'environnement (marché, concurrence, tendances)",
      "Définition des priorités stratégiques pour l'année suivante",
      "Allocation des ressources (budget, headcount, investissements)",
      "Déclinaison en OKRs par équipe",
      "Communication et alignement de toute l'organisation"
    ],
    "okr_quarterly_cycle": [
      "Semaine 1 : Bilan Q précédent (résultats, enseignements)",
      "Semaine 2-3 : Construction des OKRs Q suivant (bottom-up + top-down)",
      "Semaine 4 : Alignement et validation des OKRs",
      "Q en cours : Weekly check-in sur les métriques",
      "Fin de Q : Scoring des OKRs (0-1 par KR)"
    ]
  },
  [
    {"prompt": "Comment mettre en place un cycle de planification stratégique dans une PME de 20 personnes ?", "answer": "Structure légère adaptée aux PMEs : (1) Revue annuelle (novembre/décembre) : bilan, priorités stratégiques, budget. 2 jours offsite avec les managers clés. (2) OKRs trimestriels : 3-5 objectifs pour toute l'entreprise, chaque équipe décline les siens. 1 demi-journée. (3) Review mensuelle : métriques clés vs OKRs, bloquants, ajustements. 2h. (4) Weekly standup : bloquants opérationnels. 30 min. L'objectif n'est pas la perfection — c'est que toute l'équipe sache où on va et pourquoi. La transparence sur les priorités est le livrable le plus important."},
    {"prompt": "Comment éviter que le plan stratégique reste dans un tiroir ?", "answer": "Quatre pratiques : (1) OKRs publics et visibles pour toute l'organisation — chacun peut voir les priorités et leur avancement, (2) Revues mensuelles avec les métriques réelles (pas seulement des slides) — l'écart entre plan et réalité est le signal le plus utile, (3) Lier les décisions de recrutement et d'investissement aux OKRs — si un poste n'est lié à aucun OKR, il devrait peut-être attendre, (4) Rétrospective des OKRs en fin de trimestre — qu'est-ce qu'on a appris ? Pas juste un score, une analyse."}
  ],
  ["planification", "stratégie", "OKRs", "cycle", "revue"]
))

save("cpl/business_strategy/financial_modeling_basics.json", ku_bs(
  "financial_modeling_basics",
  "Modélisation financière — bases",
  "La modélisation financière traduit des hypothèses business en projections numériques (P&L, cash flow, bilan) pour prendre des décisions éclairées sur l'investissement, la croissance et le financement. La valeur est dans les hypothèses, pas les formules.",
  "La modélisation financière est la construction de représentations chiffrées des performances financières d'une entreprise (actuelles et futures), en liant des hypothèses business (croissance des revenus, marges, coûts) à des états financiers projetés, pour guider les décisions stratégiques et opérationnelles.",
  {
    "key_financial_statements": [
      {"statement": "P&L (Compte de résultat)", "description": "Revenus - Coûts = Résultat. Mesure la profitabilité sur une période."},
      {"statement": "Cash Flow", "description": "Entrées - Sorties de trésorerie. Distinct du P&L — une entreprise peut être profitable mais manquer de cash."},
      {"statement": "Bilan", "description": "Actifs = Passifs + Capitaux propres. Mesure la santé financière à un instant T."}
    ],
    "saas_financial_metrics": [
      {"metric": "MRR (Monthly Recurring Revenue)", "formula": "Somme des revenus récurrents mensuels actifs"},
      {"metric": "ARR (Annual Recurring Revenue)", "formula": "MRR × 12"},
      {"metric": "Churn rate (MRR)", "formula": "(MRR perdu dans le mois) / (MRR début du mois)"},
      {"metric": "CAC", "formula": "(Total dépenses sales + marketing) / (Nouveaux clients acquis dans la période)"},
      {"metric": "LTV", "formula": "ARPU / Churn rate (ou ARPU × durée de vie moyenne du client)"},
      {"metric": "LTV/CAC", "formula": "Ratio de rentabilité unitaire — > 3x = viable"},
      {"metric": "Payback period", "formula": "CAC / (ARPU × Marge brute %) — en mois"}
    ],
    "modeling_principles": [
      "Séparer les hypothèses des formules — mettre les hypothèses en haut, les calculs en dessous",
      "Modéliser les scénarios (pessimiste, base, optimiste) — pas juste le scénario base",
      "Granularité adaptée : modèle mensuel sur 12 mois, trimestriel sur 3 ans",
      "Sensibilité aux hypothèses clés — quels inputs ont le plus d'impact sur le résultat ?"
    ]
  },
  [
    {"prompt": "Quelles métriques financières surveiller en priorité pour un SaaS early-stage ?", "answer": "Trois métriques fondamentales : (1) MRR et croissance MoM — le signe de vie de base du SaaS, (2) Churn (en MRR et en clients) — si > 3% mensuel, le bucket a un trou, (3) Runway (mois de cash restants au taux de burn actuel) — te dit combien de temps tu as. En parallèle : CAC et LTV pour valider que le modèle est économiquement viable. Avant le PMF, le MRR et le churn sont les deux signaux les plus importants."},
    {"prompt": "Comment construire un modèle financier simple pour ma startup ?", "answer": "Structure en 4 blocs dans un tableur : (1) Hypothèses (onglet séparé) : croissance clients, ARPU, churn, coûts variables par client, salaires, autres fixes, (2) Revenus : MRR cumulé mois par mois, (3) Coûts : variables + fixes + salaires, (4) P&L et Cash Flow. Trois scénarios (lier les mêmes formules à des hypothèses différentes). La valeur : forcer à être explicite sur les hypothèses plutôt que de parler de croissance en abstrait. Le tableur est le reflet de votre théorie du business."}
  ],
  ["finance", "modélisation", "MRR", "CAC", "LTV", "SaaS"]
))

save("cpl/business_strategy/talent_strategy.json", ku_bs(
  "talent_strategy",
  "Stratégie talent",
  "La stratégie talent définit quelles compétences l'entreprise doit avoir, comment les recruter, les développer et les retenir — en alignant les décisions de capital humain avec les objectifs stratégiques.",
  "La stratégie talent est l'ensemble des décisions d'une organisation sur l'acquisition, le développement, la rétention et l'organisation de ses ressources humaines, dans le but de construire les compétences nécessaires à l'exécution de sa stratégie.",
  {
    "talent_strategy_pillars": [
      {"pillar": "Acquisition", "activities": ["Définition des profils (IRP — Ideal Role Profile)", "Sourcing actif et passif", "Processus de recrutement structuré", "Employer branding"]},
      {"pillar": "Développement", "activities": ["Onboarding structuré", "Feedback continu (1:1, performance review)", "Plans de développement individuel", "Formation et mentoring"]},
      {"pillar": "Rétention", "activities": ["Compensation compétitive", "Opportunities de croissance", "Culture et management", "Sens et impact"]},
      {"pillar": "Organisation", "activities": ["Structure organisationnelle adaptée au stade", "Clareté des rôles et responsabilités", "Gestion des performances"]}
    ],
    "hiring_mistakes": [
      "Embaucher trop vite sous pression — recruter le mauvais profil coûte 1-2x le salaire annuel",
      "Cloner l'équipe existante — manque de diversité de compétences et de perspectives",
      "Négliger l'onboarding — les 90 premiers jours déterminent la productivité et la rétention",
      "Ignorer la culture add — une compétence sans alignement culturel génère de la friction"
    ],
    "structured_interview": "L'entretien structuré (mêmes questions pour tous les candidats, notation sur des critères définis à l'avance) réduit les biais de recrutement et augmente la prédictivité de la performance. Compléter avec des mises en situation ou des tests pratiques."
  },
  [
    {"prompt": "Comment recruter le premier profil commercial en early-stage B2B ?", "answer": "Le premier commercial doit être capable de vendre et de construire le playbook en même temps — ce n'est pas un exécutant. Profil : Account Executive avec expérience early-stage (pas uniquement des grandes boîtes), capable de qualifier seul, de rédiger des emails, de gérer le CRM. Red flags : refuse de faire de la prospection ('c'est pour les SDR'), trop orienté processus sans adaptabilité. Salaire : base + variable OTE (On-Target Earnings) aligné sur le plan de croissance. Le premier commercial qui réussit valide le modèle ; le deuxième le scale."},
    {"prompt": "Comment retenir les meilleurs éléments dans une startup early-stage face aux grands groupes ?", "answer": "Trois leviers différenciant : (1) Impact et ownership — les meilleurs éléments veulent voir l'effet de leur travail directement, (2) Apprentissage accéléré — dans un grand groupe, on apprend lentement ; en startup, on apprend en 1 an ce qu'on apprendrait en 5, (3) Equity (BSPCE/stock options en France) — participation à la valeur créée. Ce qu'on ne peut pas offrir : la sécurité et le prestige de marque. Sélectionner des talents qui valorisent ce qu'on a, pas des talents qui cherchent ce qu'on n'a pas."}
  ],
  ["talent", "recrutement", "rétention", "RH", "organisation"]
))

save("cpl/business_strategy/brand_building.json", ku_bs(
  "brand_building",
  "Construction de la marque",
  "La marque est la réputation et la perception que les clients ont d'une entreprise — elle se construit dans le temps par la cohérence des actions, du discours et de l'expérience client. Une marque forte réduit le CAC et augmente le pricing power.",
  "La construction de marque est le processus délibéré de création et de gestion d'une identité distinctive qui génère une perception positive et durable dans l'esprit des parties prenantes cibles — permettant de différencier l'offre, d'attirer et de fidéliser clients et talents, et de justifier une prime de prix.",
  {
    "brand_components": [
      {"component": "Identité visuelle", "elements": ["Logo", "Couleurs", "Typographie", "Iconographie"], "importance": "Reconnaissabilité et cohérence"},
      {"component": "Voix et ton", "elements": ["Registre (formel/informel)", "Valeurs exprimées", "Personnalité de marque"], "importance": "Cohérence des communications"},
      {"component": "Positionnement de marque", "elements": ["Promesse de valeur", "Pour qui", "Vs quoi"], "importance": "Clarté de l'identité"},
      {"component": "Expérience client", "elements": ["Onboarding", "Service", "Produit"], "importance": "La marque réelle = expérience vécue"}
    ],
    "brand_building_tactics": [
      "Content marketing (articles, vidéos, podcast) — positionner l'entreprise comme experte",
      "Relations presse et médias sectoriels — credibilité externe",
      "Speaking et events — visibilité et thought leadership",
      "Social media — présence cohérente et personnalité de marque",
      "Témoignages et case studies clients — preuve sociale"
    ]
  },
  [
    {"prompt": "Comment construire une marque forte pour une startup B2B avec peu de budget ?", "answer": "Focus sur le thought leadership plutôt que l'advertising : (1) Un ou deux fondateurs visibles sur LinkedIn — partage d'insights, prise de position, content sur les problèmes de vos clients, (2) Case studies clients détaillés — la meilleure preuve que vous résolvez un vrai problème, (3) SEO content — articles sur les problèmes de votre ICP, qui attireront organiquement. Ces trois canaux sont gratuits (hors temps) et construisent une marque durable. L'advertising peut amplifier mais ne remplace pas la substance."},
    {"prompt": "La marque d'ALFRED — comment la définir ?", "answer": "ALFRED a une personnalité naturelle : discret, compétent, fiable, bienveillant. Ces attributs sont sa marque fonctionnelle. Pour construire la marque externe d'un produit ALFRED commercial : (1) Nom mémorable et distintif, (2) Promesse simple ('votre partenaire intelligent, toujours disponible'), (3) Cohérence dans chaque interaction (le ton est constant qu'on réponde à une question technique ou émotionnelle), (4) Une identité visuelle qui reflète la dualité technique/chaleureux. La marque se construit dans chaque échange — ALFRED est sa propre démonstration."}
  ],
  ["marque", "branding", "content marketing", "thought leadership", "identité"]
))

save("cpl/business_strategy/fundraising_strategy.json", ku_bs(
  "fundraising_strategy",
  "Stratégie de levée de fonds",
  "La levée de fonds n'est pas le but mais un outil — elle finance une accélération qui n'est pas possible avec les seuls revenus. La stratégie de levée définit quand lever, combien, auprès de qui et dans quelles conditions.",
  "La stratégie de levée de fonds est l'ensemble des décisions qui guident la recherche de financement externe (venture capital, business angels, fonds d'investissement) pour financer la croissance d'une entreprise — incluant le timing, le montant, le choix des investisseurs et la préparation du pitch.",
  {
    "funding_rounds": [
      {"round": "Pre-seed", "typical_amount": "50k-500k€", "stage": "Idée ou MVP très early, peu ou pas de revenus", "investors": "Business angels, family & friends, fonds pre-seed"},
      {"round": "Seed", "typical_amount": "500k-3M€", "stage": "MVP validé, premiers clients, product-market fit en exploration", "investors": "Business angels, fonds seed, accélérateurs"},
      {"round": "Série A", "typical_amount": "3-15M€", "stage": "PMF établi, modèle reproductible, early growth", "investors": "VCs spécialisés"},
      {"round": "Série B+", "typical_amount": "> 15M€", "stage": "Scale, expansion internationale", "investors": "VCs generalists ou spécialisés, growth equity"}
    ],
    "pitch_deck_components": [
      "Problème (douleur et taille du marché adressable)",
      "Solution (comment vous la résolvez)",
      "Traction (preuves que ça fonctionne — revenus, clients, croissance)",
      "Marché (TAM/SAM/SOM)",
      "Business model (comment vous gagnez de l'argent)",
      "Compétition (positionnement)",
      "Équipe (pourquoi vous êtes les bons pour résoudre ce problème)",
      "Use of funds (pour quoi vous utilisez l'argent levé)"
    ],
    "fundraising_alternatives": [
      "Bootstrapping : croître avec les revenus — plus long mais ownership conservé",
      "Revenue-based financing : remboursement basé sur les revenus — pour les SaaS avec MRR stable",
      "Subventions (BPI, Horizon Europe, ADEME) : non-dilutif, process long",
      "Prêts bancaires (si MRR > 100k€) : non-dilutif mais contraignant"
    ]
  },
  [
    {"prompt": "Comment savoir si je suis prêt à lever des fonds ?", "answer": "Trois questions : (1) Ai-je la preuve que mon modèle fonctionne ? (PMF, revenus récurrents, LTV/CAC viable) — lever avant ça finance l'exploration, pas la croissance, et les VCs le savent, (2) Ai-je un plan d'utilisation des fonds clair ? (lever X€ pour atteindre Y traction en Z mois en embauchant A, en dépensant B en marketing) — sans plan concret, l'argent est brûlé, (3) Ai-je exploré les alternatives non-dilutives ? (BPI Innovation, clients, partenariats). Si les trois réponses sont positives → il est temps de commencer le processus."},
    {"prompt": "Comment pitcher ma startup IA à un investisseur ?", "answer": "Structure en 5 minutes : (1) Hook — le problème en une phrase vivante avec la douleur réelle, (2) Solution — comment VOTRE approche est différente (pas juste 'nous utilisons l'IA'), (3) Traction — les 3 meilleurs indicateurs que ça marche (clients, MRR, rétention, croissance MoM), (4) Marché — pas juste TAM mais pourquoi vous pouvez en capturer un bout significatif, (5) Ask — combien, pour quoi précisément, quel milestone ça finance. Pour l'IA : les VCs ont vu des centaines de pitches IA — la différenciation sur les données propriétaires ou l'accès unique au cas d'usage est décisive."}
  ],
  ["levée de fonds", "VC", "pitch", "seed", "bootstrapping"]
))

save("cpl/business_strategy/exit_strategy.json", ku_bs(
  "exit_strategy",
  "Stratégie de sortie (exit)",
  "La stratégie de sortie définit comment les fondateurs et investisseurs récupèrent leur investissement — par acquisition, IPO ou cession. La réflexion sur l'exit influence les décisions stratégiques bien avant la sortie elle-même.",
  "La stratégie de sortie est la planification des voies par lesquelles les fondateurs et investisseurs d'une entreprise peuvent liquider ou céder tout ou partie de leur participation, incluant l'acquisition, l'introduction en bourse (IPO) ou la cession à des partenaires stratégiques.",
  {
    "exit_options": [
      {"option": "Acquisition stratégique", "description": "Rachat par un acteur du secteur qui cherche à acquérir la technologie, l'équipe ou les clients", "advantage": "Processus plus rapide, prime de contrôle", "consideration": "Risque d'absorption de la culture et du produit"},
      {"option": "Acquisition financière (PE)", "description": "Rachat par un fonds de private equity qui optimise puis revend", "advantage": "Fondateurs souvent remplacés par des managers professionnels", "consideration": "Fréquent pour les entreprises rentables mais à croissance modérée"},
      {"option": "IPO", "description": "Introduction en bourse", "advantage": "Liquidité pour tous, visibilité, accès aux marchés de capitaux", "consideration": "Process lourd (12-24 mois), coûteux, pression trimestrielle"},
      {"option": "Cession partielle / secondaire", "description": "Vente partielle de parts par les fondateurs ou investisseurs early", "advantage": "Liquidité sans exit total", "consideration": "Possible à partir de la Série B dans un processus structuré"}
    ],
    "exit_preparation": [
      "Audits financiers propres (3 ans minimum)",
      "Diversification de la base client (pas de dépendance à un client > 20%)",
      "Equipe de management autonome (pas indispensable au fondateur)",
      "IP et actifs technologiques documentés et protégés",
      "Métriques clés trackées et présentables"
    ]
  },
  [
    {"prompt": "Dois-je penser à mon exit dès le début de ma startup ?", "answer": "Pas au sens de 'planifier la sortie' mais au sens de 'construire une entreprise qui a de la valeur'. Un exit réussi est la conséquence d'une entreprise bien construite — PMF fort, métriques solides, équipe compétente, IP protégée, clients diversifiés. Ces éléments rendent une entreprise attractive pour un acquéreur, mais ils sont aussi exactement ce qui rend l'entreprise durable si on ne vend pas. Donc : construire bien, réfléchir à l'exit si et quand une opportunité se présente."},
    {"prompt": "Comment maximiser la valeur d'une entreprise avant une acquisition ?", "answer": "Les leviers de valorisation dans une acquisition : (1) Revenu récurrent (ARR) et croissance — le multiple payé dépend du taux de croissance, (2) Churn faible — gage de qualité produit et de satisfaction client, (3) Diversification client — pas de dépendance critique, (4) Barrières à la sortie (switching costs) — les clients ne partent pas facilement, (5) Equipe clé non-dépendante du fondateur — l'acquéreur ne veut pas racheter une personne. Action 12 mois avant : audits propres, documentation IP, plan de transition de l'équipe."}
  ],
  ["exit", "acquisition", "IPO", "valorisation", "cession"]
))

save("cpl/business_strategy/innovation_management.json", ku_bs(
  "innovation_management",
  "Management de l'innovation",
  "L'innovation managée combine l'exploration de nouveaux territoires (innovation de rupture) avec l'exploitation de l'existant (innovation incrémentale). Les entreprises qui réussissent sur le long terme maintiennent un équilibre entre les deux.",
  "Le management de l'innovation est l'ensemble des processus, structures et cultures qui permettent à une organisation de générer de nouvelles idées, de les sélectionner, de les développer et de les commercialiser de façon systématique et rentable.",
  {
    "innovation_types": [
      {"type": "Incrémentale", "description": "Amélioration des offres et processus existants (10-30% mieux)", "risk": "Faible", "return": "Faible à moyen"},
      {"type": "Adjacente", "description": "Extension vers de nouveaux marchés ou produits proches du core (30-100% différent)", "risk": "Moyen", "return": "Moyen à élevé"},
      {"type": "Radicale / de rupture", "description": "Nouveaux marchés ou modèles (x10 différent)", "risk": "Élevé", "return": "Très élevé si succès"}
    ],
    "ambidexterity": "Les organisations ambidextres maintiennent deux moteurs : exploitation (améliorer et scaler l'existant) et exploration (chercher les opportunités futures). Erreur classique : l'exploitation envahit l'exploration — les projets d'innovation sont sacrifiés à la demande court terme.",
    "innovation_process": [
      "Veille et détection des signaux faibles",
      "Génération d'idées (brainstorming structuré, innovation ouverte, hackathons)",
      "Sélection et priorisation (critères : impact, faisabilité, alignement stratégique)",
      "Développement itératif (design thinking, lean startup)",
      "Commercialisation et scaling"
    ]
  },
  [
    {"prompt": "Comment maintenir la capacité d'innovation quand l'entreprise est en mode croissance ?", "answer": "Trois pratiques : (1) Budget dédié à l'exploration (10-20% de la capacité engineering/produit) — protected, non réaffectable au court terme, (2) Equipe dédiée à l'exploration (quelques personnes isolées de la pression opérationnelle) — les 'skunkworks' de Lockheed, les 20% time de Google, (3) Processus distinct pour les projets d'exploration (pas les mêmes métriques ni les mêmes timelines que la delivery). L'innovation ne survit pas à la pression opérationnelle sans protection structurelle."},
    {"prompt": "Comment ALFRED peut aider à stimuler l'innovation dans mon équipe ?", "answer": "Plusieurs angles : (1) Veille active — je peux surveiller les tendances sectorielles et signaler les innovations pertinentes pour votre domaine, (2) Analogies cross-domaines — souvent, les meilleures innovations viennent de l'application de patterns d'un secteur différent, (3) Structuration des idées — quand une idée émerge, je peux aider à la développer en business case, à identifier les hypothèses critiques et à concevoir les tests de validation. L'IA comme partenaire de pensée accélère le cycle d'exploration des idées."}
  ],
  ["innovation", "disruption", "R&D", "exploration", "ambidexterity"]
))

save("cpl/business_strategy/operational_excellence.json", ku_bs(
  "operational_excellence",
  "Excellence opérationnelle",
  "L'excellence opérationnelle est la capacité à exécuter de façon cohérente, efficace et fiable — en réduisant les gaspillages, en standardisant les processus qui le permettent, et en créant une culture d'amélioration continue.",
  "L'excellence opérationnelle est la capacité d'une organisation à exécuter ses opérations avec un niveau de qualité, d'efficacité et de cohérence supérieur — en éliminant les gaspillages, en optimisant les flux de valeur et en créant une culture d'amélioration continue qui implique tous les niveaux.",
  {
    "operational_frameworks": [
      {"framework": "Lean", "origin": "Toyota Production System", "focus": "Éliminer les gaspillages (muda) dans les processus", "key_tools": ["Value stream mapping", "5S", "Kaizen", "Kanban"]},
      {"framework": "Six Sigma", "origin": "Motorola / GE", "focus": "Réduire la variabilité et les défauts", "key_tools": ["DMAIC", "contrôle statistique", "analyse des causes racines"]},
      {"framework": "OKRs + KPIs", "origin": "Intel / Google", "focus": "Aligner les objectifs et mesurer la performance", "key_tools": ["OKRs trimestriels", "dashboards temps réel"]},
      {"framework": "Amélioration continue (Kaizen)", "origin": "Japon", "focus": "Culture de petites améliorations incrémentales par toute l'organisation", "key_tools": ["Réunions kaizen", "feedbacks de terrain", "PDCA"]}
    ],
    "waste_types_lean": [
      "Transport (déplacements inutiles d'information ou de matière)",
      "Inventaire (stock excessif — en logiciel : features non utilisées)",
      "Mouvement (efforts inutiles)",
      "Attente (blocages dans les processus)",
      "Surproduction (produire plus que nécessaire)",
      "Surtraitement (traitement excessif par rapport au besoin)",
      "Défauts (erreurs qui nécessitent une reprise)"
    ]
  },
  [
    {"prompt": "Comment appliquer les principes Lean à une startup tech ?", "answer": "Les 5 principes Lean adaptés au logiciel : (1) Définir la valeur du point de vue du client (pas de features non demandées), (2) Identifier le flux de valeur (du code à la production — éliminer les étapes sans valeur), (3) Créer un flux continu (CI/CD, revue de PR en < 24h, déploiements fréquents), (4) Système pull (travailler uniquement sur ce qui est demandé — limiter le WIP), (5) Amélioration continue (rétrospectives régulières, mesure du lead time). Le Lean Software Development de Poppendieck est la référence."},
    {"prompt": "Comment mesurer l'excellence opérationnelle dans mon entreprise ?", "answer": "Métriques de flux (pour tech/produit) : DORA metrics (deployment frequency, lead time, MTTR, change failure rate). Métriques de qualité : taux de défauts, NPS client, taux de résolution au premier contact. Métriques d'efficacité : vélocité de l'équipe (trend, pas valeur absolue), lead time feature (de l'idée à la production), utilisation des ressources. La clé : choisir 3-5 métriques, les afficher en temps réel et les revoir en équipe chaque semaine — la visibilité crée l'amélioration."}
  ],
  ["excellence opérationnelle", "Lean", "Six Sigma", "Kaizen", "processus"]
))

save("cpl/business_strategy/network_effects_strategy.json", ku_bs(
  "network_effects_strategy",
  "Stratégie d'effets réseau",
  "Les effets réseau créent des avantages compétitifs durables et difficiles à répliquer : le produit devient plus précieux à mesure qu'il attire plus d'utilisateurs. Les différents types d'effets réseau ont des propriétés et des stratégies d'activation différentes.",
  "Les effets réseau (network effects) sont une propriété d'un produit ou service par laquelle sa valeur augmente pour chaque utilisateur à mesure que davantage de personnes l'utilisent. Les effets réseau créent des barrières à la sortie et des avantages compétitifs exponentiels pour les leaders de marché.",
  {
    "network_effects_types": [
      {"type": "Direct (same-side)", "description": "La valeur augmente quand les utilisateurs du même type augmentent", "example": "Téléphone, WhatsApp — utile seulement si tes contacts l'utilisent"},
      {"type": "Indirect (cross-side)", "description": "La valeur d'un côté augmente avec le nombre d'utilisateurs de l'autre côté", "example": "Marketplace — plus de vendeurs → plus d'acheteurs → plus de vendeurs"},
      {"type": "Données (data network effect)", "description": "Plus d'utilisateurs → plus de données → meilleur produit → plus d'utilisateurs", "example": "Waze, Google Search, LLMs avec RLHF"},
      {"type": "Viral (social)", "description": "L'utilisation expose de nouveaux utilisateurs potentiels", "example": "Canva — partage de créations exposant Canva à des non-utilisateurs"}
    ],
    "activating_network_effects": [
      "Cold start problem : comment attirer les premiers utilisateurs quand le produit est peu utile sans utilisateurs ? (subsidier un côté, lancer dans un niche, curate le contenu)",
      "Concentration géographique : pour les marketplaces locales, lancer ville par ville plutôt que national",
      "Chicken-and-egg : résoudre en démarrant avec un sous-groupe (LinkedIn : étudiants Stanford d'abord)"
    ]
  },
  [
    {"prompt": "Comment créer des effets réseau pour un SaaS B2B ?", "answer": "Les effets réseau dans le B2B sont souvent du type 'data' ou 'workflow'. Data network effect : si votre produit apprend des données de tous vos clients (benchmarks, modèles d'usage, patterns d'industrie) et que ces insights profitent à chaque client, c'est un data network effect. Workflow network effect : si votre produit permet la collaboration entre plusieurs rôles dans une entreprise, l'expansion au sein du compte crée un lock-in fort (Slack, Notion). La question : comment votre produit devient-il plus utile à un client quand d'autres clients l'utilisent ?"},
    {"prompt": "ALFRED peut-il avoir des effets réseau à terme ?", "answer": "Oui — via les données principalement. Si des milliers d'ALFRED collectent (avec consentement) des patterns d'interaction, de préférence et d'efficacité, le modèle central peut s'améliorer continuellement et bénéficier à chaque nouvel utilisateur. C'est le data network effect des assistants IA : plus d'utilisateurs → plus de données d'apprentissage → meilleure IA → plus d'utilisateurs. Condition : la collecte doit être éthique, consentie et apporter une valeur claire à chaque utilisateur."}
  ],
  ["effets réseau", "marketplace", "data", "viral", "lock-in"]
))

save("cpl/business_strategy/crisis_management.json", ku_bs(
  "crisis_management",
  "Gestion de crise business",
  "La crise business (perte d'un client majeur, incident produit, problème financier, scandale réputationnel) requiert une réponse rapide, transparente et structurée. La qualité de la gestion de crise détermine souvent l'issue plus que la crise elle-même.",
  "La gestion de crise business est l'ensemble des pratiques qui permettent à une organisation de répondre efficacement à des événements imprévus et potentiellement déstabilisateurs — en minimisant les impacts, en communicant de façon transparente et en accélérant le retour à la normale.",
  {
    "crisis_types": [
      {"type": "Crise financière", "examples": ["Cash en dessous du runway minimum", "Perte d'un contrat majeur (>20% du revenu)", "Coûts dépassant les prévisions"]},
      {"type": "Crise produit/technique", "examples": ["Incident de sécurité/breach", "Panne critique de service", "Bug majeur impactant les clients"]},
      {"type": "Crise réputationnelle", "examples": ["Bad press", "Polémique sur les réseaux sociaux", "Échec public visible"]},
      {"type": "Crise humaine", "examples": ["Départ inattendu d'un cofounder/CTO", "Conflit interne majeur", "Violation légale"]}
    ],
    "crisis_response_framework": [
      "1. Assess (évaluer) : comprendre l'ampleur réelle avant d'agir",
      "2. Contain (contenir) : empêcher que ça empire pendant qu'on gère",
      "3. Communicate (communiquer) : parties prenantes informées avec les faits disponibles",
      "4. Resolve (résoudre) : plan d'action avec owner et timeline",
      "5. Learn (apprendre) : post-mortem pour éviter la récurrence"
    ],
    "communication_principles": [
      "Transparence : ne pas minimiser les faits — les tentatives de dissimulation aggravent toujours la crise",
      "Vitesse : communiquer rapidement même si l'information est incomplète ('nous examinons la situation')",
      "Ownership : assumer la responsabilité, ne pas blâmer les tiers",
      "Actions concrètes : décrire ce qu'on fait, pas seulement s'excuser"
    ]
  },
  [
    {"prompt": "Notre serveur a été compromis — que faire dans les premières heures ?", "answer": "Protocole incident cybersécurité J0 : (1) Isoler les systèmes compromis immédiatement (couper la connexion réseau, pas éteindre — préserver les preuves), (2) Appeler les personnes clés (CTO, CEO, RSSI, légal) en parallèle, (3) Documenter tout en temps réel (logs, timeline, actions prises), (4) Évaluer l'étendue de la compromission (données impactées ?), (5) Notifier la CNIL dans les 72h si données personnelles concernées (obligation RGPD). Ne pas communiquer publiquement avant d'avoir les faits. Ne pas payer de rançon sans conseil juridique spécialisé."},
    {"prompt": "Comment gérer la perte soudaine de 30% du revenu suite à l'arrêt d'un client majeur ?", "answer": "Réponse en trois temps : (1) Immédiat (J0-J7) : évaluer le runway restant avec le nouveau burn, identifier les dépenses réductibles rapidement sans impact opérationnel critique, informer le board/investisseurs avec les faits et le plan, (2) Court terme (J7-J30) : accélérer la pipeline commerciale (ne pas attendre), chercher à remplacer le revenu (upsell clients existants, accélération prospection), (3) Moyen terme : analyser pourquoi ce client est parti (éviter la récurrence), revisiter la stratégie de diversification client. La perte d'un gros client est douloureuse mais révèle un problème de concentration à corriger."}
  ],
  ["crise", "incident", "communication de crise", "résilience", "gestion de risque"]
))

print("\nBatch 11 cpl/business_strategy (15 restants) : DONE")
