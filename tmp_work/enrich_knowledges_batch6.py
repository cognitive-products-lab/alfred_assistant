"""
Enrichissement Knowledge Base ALFRED - Batch 6 : professional/governance_ai (20 fichiers)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku_gov(stem, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.professional.governance_ai.{stem}",
      "title": title, "domain": "professional", "subdomain": "governance_ai",
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": "rigoureux, orienté conformité et opérationnalité",
        "structure": ["identifier le principe de gouvernance en jeu", "expliquer l'application concrète", "pointer les risques de non-conformité"],
        "avoid": ["trop théorique sans ancrage opérationnel", "ignorer le contexte réglementaire EU", "confondre gouvernance et éthique abstraite"]
      },
      "tags": tags + ["gouvernance IA", "AI governance", "conformité"],
      "related_knowledge_units": [
        "knowledges.professional.standards_iso.iso_42001_ai_management_system",
        "knowledges.cpl.ethics_governance.ethical_ai_framework"
      ]
    }

# =============================================================================
# professional / governance_ai (20 fichiers)
# =============================================================================

save("professional/governance_ai/ai_governance_basics.json", ku_gov(
  "ai_governance_basics",
  "Fondamentaux de la gouvernance IA",
  "La gouvernance IA est le cadre structuré par lequel une organisation décide comment concevoir, déployer et superviser ses systèmes d'IA de façon responsable, traçable et conforme aux réglementations.",
  "La gouvernance IA (AI Governance) est l'ensemble des politiques, processus, rôles et outils qui encadrent le cycle de vie des systèmes d'IA — de la conception au retrait — afin d'assurer leur alignement sur les objectifs organisationnels, les valeurs éthiques et les exigences réglementaires.",
  {
    "governance_pillars": [
      {"pillar": "Accountability", "description": "Définir clairement qui est responsable de chaque système IA — son comportement, ses performances, ses erreurs"},
      {"pillar": "Transparency", "description": "Être capable d'expliquer comment les décisions IA sont prises — à différents niveaux de détail selon l'audience"},
      {"pillar": "Fairness", "description": "S'assurer que le système IA ne discrimine pas et traite équitablement tous les groupes"},
      {"pillar": "Privacy", "description": "Respecter la vie privée dans la collecte, le traitement et le stockage des données"},
      {"pillar": "Security", "description": "Protéger les systèmes IA contre les attaques, les manipulations et les abus"},
      {"pillar": "Human oversight", "description": "Maintenir un contrôle humain approprié selon le niveau de risque du système"}
    ],
    "governance_cycle": [
      "Évaluation pre-déploiement (risk assessment, tests de biais)",
      "Validation et approbation formelle avant mise en production",
      "Monitoring continu des performances et des comportements",
      "Processus de signalement et d'escalade des incidents",
      "Révision périodique et mise à jour des règles comportementales"
    ],
    "regulatory_landscape": {
      "EU_AI_Act": "En vigueur depuis 2024. Classifie les IA en 4 niveaux de risque. Les obligations varient selon la catégorie.",
      "ISO_42001": "Norme internationale de management des systèmes IA — processus, documentation, amélioration continue.",
      "NIST_AI_RMF": "Framework américain de gestion des risques IA — Govern, Map, Measure, Manage."
    }
  },
  [
    {"prompt": "Par où commencer pour mettre en place la gouvernance IA dans notre organisation ?", "answer": "Trois premières étapes : inventorier tous les systèmes IA en place (shadow AI inclus), évaluer leur niveau de risque selon l'EU AI Act, et nommer un owner pour chaque système critique. C'est la base — tout le reste (politiques, audits, monitoring) s'appuie sur cet inventaire."},
    {"prompt": "Quelle différence entre éthique IA et gouvernance IA ?", "answer": "L'éthique IA définit les principes (ce qui est juste et bien). La gouvernance IA est le mécanisme opérationnel qui permet de les appliquer (qui décide, comment on vérifie, comment on corrige). L'éthique sans gouvernance reste une déclaration d'intention. La gouvernance sans éthique peut être rigoureuse mais mal orientée."}
  ],
  ["fondamentaux", "cadre", "accountability", "transparence", "EU AI Act"]
))

save("professional/governance_ai/ai_accountability.json", ku_gov(
  "ai_accountability",
  "Responsabilité et accountability dans les systèmes IA",
  "L'accountability IA signifie qu'un humain identifiable est responsable du comportement, des erreurs et des impacts de chaque système IA déployé. Sans accountability claire, les incidents restent sans correction et les risques s'accumulent.",
  "L'accountability dans les systèmes IA est le principe selon lequel une personne ou une organisation doit pouvoir répondre des décisions et comportements d'un système IA, en assumer les conséquences et mettre en place les corrections nécessaires.",
  {
    "accountability_model": [
      {"role": "AI Owner", "responsibility": "Propriétaire business du système — répond des décisions business et des impacts sur les utilisateurs"},
      {"role": "AI Developer", "responsibility": "Responsable technique — répond de la qualité, de la sécurité et de la performance du modèle"},
      {"role": "AI Operator", "responsibility": "Responsable de l'exploitation — répond du monitoring, des incidents et de la maintenance"},
      {"role": "AI Ethics Reviewer", "responsibility": "Responsable de la conformité éthique et réglementaire — valide avant déploiement"}
    ],
    "accountability_mechanisms": [
      "Documentation complète du cycle de vie (model cards, datasheets)",
      "Traçabilité des décisions prises avec ou par l'IA",
      "Processus d'audit régulier avec résultats documentés",
      "Mécanisme de recours pour les personnes impactées par une décision IA",
      "Rapport d'incident obligatoire pour tout comportement inattendu"
    ],
    "eu_ai_act_obligations": [
      "Systèmes à haut risque : registre EU obligatoire, documentation technique, monitoring continu",
      "Transparency requirements : informer les utilisateurs qu'ils interagissent avec une IA",
      "Human oversight : obligation de supervision humaine pour les décisions critiques"
    ]
  },
  [
    {"prompt": "Qui est responsable si notre système IA prend une mauvaise décision ?", "answer": "En droit actuel, le fournisseur du système et l'opérateur qui le déploie partagent la responsabilité. L'EU AI Act introduit des obligations précises pour les systèmes à haut risque. En interne : il faut un AI Owner nommé avant tout déploiement. Sans owner identifié, personne n'est responsable — et les incidents restent sans réponse."},
    {"prompt": "Comment tracer les décisions prises par une IA ?", "answer": "Trois niveaux : journalisation des inputs/outputs (ce qui entre et ce qui sort), contexte de la décision (qui a demandé quoi, quand, avec quel prompt), et résultat business (quelle décision a été prise sur la base de la recommandation IA). Pour les systèmes à fort impact, la traçabilité est une obligation réglementaire, pas une option."}
  ],
  ["accountability", "responsabilité", "owner", "traçabilité", "incident"]
))

save("professional/governance_ai/ai_risk_management.json", ku_gov(
  "ai_risk_management",
  "Gestion des risques IA",
  "Les systèmes IA introduisent des risques spécifiques : hallucinations, biais, attaques adversariales, dépendance aux données, dérive comportementale. Les identifier, évaluer et mitiger fait partie de toute gouvernance IA sérieuse.",
  "La gestion des risques IA est le processus d'identification, d'évaluation et de traitement des risques propres aux systèmes IA — incluant les risques techniques (qualité des données, performance), éthiques (biais, discrimination), de sécurité (adversarial attacks, data poisoning) et opérationnels (dépendance, dérive).",
  {
    "ai_specific_risks": [
      {"risk": "Hallucinations / erreurs factuelles", "mitigation": "RAG sur sources vérifiées, phrases de hedge, validation humaine sur cas critiques"},
      {"risk": "Biais algorithmiques", "mitigation": "Audit des données d'entraînement, tests équité sur groupes protégés, monitoring continu"},
      {"risk": "Dérive comportementale (model drift)", "mitigation": "Monitoring des performances dans le temps, retests périodiques sur benchmarks"},
      {"risk": "Prompt injection / attaques adversariales", "mitigation": "Validation des inputs, isolation des contextes système et utilisateur, sandboxing"},
      {"risk": "Dépendance à un seul fournisseur", "mitigation": "Architecture multi-modèle, plan de fallback, contrats de réversibilité"},
      {"risk": "Fuite de données sensibles", "mitigation": "Minimisation des données transmises au LLM, anonymisation, stockage local"}
    ],
    "risk_classification_eu_ai_act": [
      {"level": "Risque inacceptable", "examples": "Systèmes de notation sociale, manipulation subliminale", "obligation": "Interdits"},
      {"level": "Haut risque", "examples": "Recrutement IA, crédit, santé, justice, éducation", "obligation": "Conformité stricte, documentation, audit"},
      {"level": "Risque limité", "examples": "Chatbots, assistants texte", "obligation": "Transparence obligatoire (informer l'utilisateur)"},
      {"level": "Risque minimal", "examples": "Filtres anti-spam, recommandations de films", "obligation": "Pas d'obligation spécifique"}
    ]
  },
  [
    {"prompt": "Notre IA commence à donner des réponses différentes de celles d'il y a 6 mois — pourquoi ?", "answer": "Model drift — dérive comportementale. Plusieurs causes : changement du modèle de base (mise à jour par le fournisseur), changement des données d'entrée (distribution shift), ou accumulation de retours qui modifient le comportement. Action : retest sur des benchmarks de référence, comparaison avec les outputs de référence, et monitoring régulier des métriques clés."},
    {"prompt": "Comment savoir si notre IA est biaisée ?", "answer": "Audit de fairness : tester les outputs sur des groupes démographiques différents (genre, âge, origine) avec des prompts équivalents. Si les réponses varient de façon systématique pour des raisons liées à ces caractéristiques, il y a un biais. Des outils comme Fairlearn (Microsoft) ou AI Fairness 360 (IBM) automatisent une partie de cet audit."}
  ],
  ["risques IA", "biais", "hallucinations", "model drift", "adversarial"]
))

save("professional/governance_ai/ai_transparency.json", ku_gov(
  "ai_transparency",
  "Transparence des systèmes IA",
  "La transparence IA opère à plusieurs niveaux : informer l'utilisateur qu'il interagit avec une IA, expliquer comment les décisions sont prises, et documenter les caractéristiques du modèle pour les régulateurs.",
  "La transparence dans les systèmes IA est la capacité à rendre compréhensibles — à différents niveaux et pour différentes audiences — le fonctionnement, les décisions et les limites d'un système IA, afin de permettre la confiance, le contrôle et la responsabilité.",
  {
    "transparency_levels": [
      {"level": "Utilisateur", "requirement": "Savoir qu'on interagit avec une IA, comprendre les limites, pouvoir contester une décision"},
      {"level": "Opérateur", "requirement": "Comprendre les performances, les risques et le comportement du système en production"},
      {"level": "Régulateur", "requirement": "Accès à la documentation technique, aux méthodes de test, aux données d'entraînement (EU AI Act haut risque)"}
    ],
    "explainability_methods": [
      {"method": "LIME (Local Interpretable Model-agnostic Explanations)", "use": "Expliquer des prédictions individuelles en modifiant les inputs"},
      {"method": "SHAP (SHapley Additive exPlanations)", "use": "Mesurer la contribution de chaque feature à la prédiction"},
      {"method": "Model cards", "use": "Documentation standardisée du modèle : objectif, données, performances, limites"},
      {"method": "Phrases de hedge", "use": "L'IA elle-même signale ses incertitudes ('je ne suis pas certain mais...', 'à ma connaissance...')"}
    ],
    "transparency_vs_ip": "La transparence totale sur les poids du modèle peut entrer en conflit avec la protection de la propriété intellectuelle. L'EU AI Act trouve un équilibre : obligation de documentation pour les systèmes à haut risque, sans nécessairement rendre les poids publics."
  },
  [
    {"prompt": "Faut-il obligatoirement dire aux utilisateurs qu'ils parlent à une IA ?", "answer": "Oui — obligation légale sous l'EU AI Act pour les systèmes IA interactifs déployés dans l'UE depuis août 2026. Et au-delà du légal : la transparence sur la nature IA est un principe éthique fondamental. La simulation d'humanité non consentie est un abus de confiance, indépendamment de la loi."},
    {"prompt": "Comment expliquer les décisions d'un modèle IA à un non-technicien ?", "answer": "Trois niveaux selon l'audience : pour un utilisateur impacté ('cette décision a été prise parce que X, Y, Z'), pour un manager ('le modèle pondère ces 5 facteurs, voici leur poids'), pour un régulateur (documentation technique complète avec méthodes d'évaluation). La règle : l'explication doit permettre à l'audience de comprendre et potentiellement de contester."}
  ],
  ["transparence", "explicabilité", "LIME", "SHAP", "model card"]
))

save("professional/governance_ai/ai_ethics_operationalization.json", ku_gov(
  "ai_ethics_operationalization",
  "Opérationnalisation de l'éthique IA",
  "Les principes éthiques IA (transparence, équité, privacy) restent vides sans mécanismes opérationnels concrets : checklists, gates de validation, rôles dédiés et processus d'audit. L'éthique IA se déploie dans les pratiques, pas dans les déclarations.",
  "L'opérationnalisation de l'éthique IA est la traduction de principes éthiques abstraits (équité, transparence, responsabilité, bienfaisance) en pratiques concrètes intégrées dans le cycle de vie du développement et du déploiement des systèmes IA.",
  {
    "operationalization_methods": [
      {"method": "Ethics by design", "description": "Intégrer l'évaluation éthique dès la phase de conception, pas après", "tools": ["Fiches de risques éthiques", "Value Sensitive Design", "Stakeholder impact mapping"]},
      {"method": "Ethics gates", "description": "Points de validation éthique obligatoires avant chaque phase clé (conception, test, déploiement)", "tools": ["Checklists de validation", "Revue par comité éthique"]},
      {"method": "Ethics audits", "description": "Audits réguliers des systèmes en production pour détecter les dérives", "tools": ["Fairness testing", "Adversarial testing", "User feedback analysis"]},
      {"method": "Ethics training", "description": "Formation des équipes sur les principes éthiques IA et leur application", "frequency": "Annuel minimum"}
    ],
    "practical_checklist": [
      "Le système sait-il clairement qu'il est une IA quand on lui demande ?",
      "Les utilisateurs ont-ils été informés de l'utilisation de l'IA ?",
      "Le système a-t-il été testé sur des groupes démographiques diversifiés ?",
      "Existe-t-il un mécanisme de recours pour les décisions contestées ?",
      "Les données d'entraînement ont-elles été auditées pour les biais ?",
      "Y a-t-il un owner identifié responsable du comportement du système ?"
    ]
  },
  [
    {"prompt": "Comment éviter que l'éthique IA reste un discours sans impact réel ?", "answer": "En l'ancrant dans des processus concrets : une checklist éthique avant chaque déploiement, un rôle dédié (AI Ethics Officer ou responsabilité au sein d'une équipe existante), des KPIs mesurables (taux de biais détectés, délai de correction, % de systèmes avec owner). Ce qui n'est pas mesuré n'est pas géré."},
    {"prompt": "Par où commencer l'éthique IA en pratique dans une PME ?", "answer": "Trois actions immédiates et concrètes : inventorier les systèmes IA utilisés (y compris les outils SaaS qui intègrent de l'IA), nommer un responsable pour chacun, et créer une checklist de 10 questions à répondre avant tout nouveau déploiement. Sans commencer petit, l'éthique IA restera un sujet de conférence."}
  ],
  ["opérationnalisation", "ethics by design", "checklist", "audit", "pratique"]
))

save("professional/governance_ai/ai_auditability.json", ku_gov(
  "ai_auditability",
  "Auditabilité des systèmes IA",
  "Un système IA est auditable quand il peut être examiné pour vérifier sa conformité, ses performances et son comportement — par des équipes internes, des régulateurs ou des auditeurs externes. L'auditabilité se conçoit, elle ne s'improvise pas.",
  "L'auditabilité d'un système IA est sa capacité à être examiné, évalué et vérifié par des tiers — en termes de performances, de comportements, de conformité éthique et réglementaire — grâce à une documentation adéquate, une traçabilité complète et des mécanismes de test reproductibles.",
  {
    "auditability_components": [
      {"component": "Documentation", "includes": ["Model cards", "Datasheets for datasets", "Architecture technique", "Hypothèses de conception"]},
      {"component": "Traçabilité", "includes": ["Logs des inputs/outputs", "Versioning des modèles", "Historique des changements de configuration"]},
      {"component": "Reproductibilité", "includes": ["Tests automatisés reproductibles", "Benchmarks de référence", "Environnements de test documentés"]},
      {"component": "Accessibilité pour les auditeurs", "includes": ["Accès contrôlé aux logs", "Interface d'audit dédiée", "Processus d'escalade défini"]}
    ],
    "audit_types": [
      {"type": "Audit interne", "frequency": "Trimestriel ou semestriel", "scope": "Performance, biais, sécurité"},
      {"type": "Audit externe", "frequency": "Annuel ou pré-déploiement pour les systèmes à haut risque", "scope": "Conformité réglementaire complète"},
      {"type": "Audit continu (monitoring)", "frequency": "En temps réel ou quasi-réel", "scope": "Détection de dérive, incidents, anomalies"}
    ]
  },
  [
    {"prompt": "Comment préparer notre système IA pour un audit réglementaire ?", "answer": "Quatre éléments essentiels : documentation technique complète (model card, architecture, données), logs des décisions couvrant la période requise, résultats des tests de performance et d'équité, et liste des incidents avec les corrections apportées. L'audit ne se prépare pas en urgence — la documentation doit être maintenue en continu."},
    {"prompt": "Qu'est-ce qu'un model card ?", "answer": "Une model card est un document standardisé qui décrit un modèle IA : son objectif, les données d'entraînement, les performances mesurées sur différents groupes, les limites connues et les usages non recommandés. Google a popularisé le format en 2019 (Mitchell et al.). L'EU AI Act exige un équivalent pour les systèmes à haut risque."}
  ],
  ["auditabilité", "model card", "logs", "documentation", "reproductibilité"]
))

save("professional/governance_ai/bias_detection.json", ku_gov(
  "bias_detection",
  "Détection et mitigation des biais IA",
  "Les biais dans les systèmes IA peuvent amplifier des inégalités existantes à grande échelle. Les détecter nécessite des méthodes statistiques sur des groupes protégés ; les mitiger exige d'agir sur les données, le modèle ou le post-traitement.",
  "La détection de biais dans les systèmes IA est le processus d'identification des différences systématiques injustes dans les performances ou les sorties d'un modèle selon des caractéristiques protégées (genre, origine ethnique, âge, handicap), indépendamment des intentions des concepteurs.",
  {
    "bias_types": [
      {"type": "Biais de données", "description": "Les données d'entraînement reflètent des inégalités historiques — le modèle les apprend et les perpétue", "example": "CV de recrutement historiquement masculins → modèle favorisant les hommes"},
      {"type": "Biais d'agrégation", "description": "Le modèle entraîné sur la population générale performe mal sur des sous-groupes spécifiques", "example": "Diagnostic médical moins précis pour les groupes sous-représentés dans les données"},
      {"type": "Biais de mesure", "description": "Les labels ou features utilisés sont eux-mêmes biaisés", "example": "Utiliser les arrests comme proxy de la criminalité (surreprésente certains groupes)"},
      {"type": "Biais d'évaluation", "description": "L'évaluation est faite sur un benchmark non représentatif", "example": "Benchmark uniquement en anglais américain pour un système multilingue"}
    ],
    "detection_methods": [
      "Analyse statistique des outputs par groupe protégé (disparate impact analysis)",
      "Fairness metrics : demographic parity, equalized odds, predictive parity",
      "Tests d'adversarial fairness (même prompt avec profils démographiques variés)",
      "Outils : Fairlearn (Microsoft), AI Fairness 360 (IBM), What-If Tool (Google)"
    ],
    "mitigation_strategies": [
      {"stage": "Données", "actions": ["Rééchantillonnage", "Augmentation des sous-groupes sous-représentés", "Nettoyage des labels biaisés"]},
      {"stage": "Modèle", "actions": ["Contraintes de fairness dans l'optimisation", "Calibration par groupe", "Adversarial debiasing"]},
      {"stage": "Post-traitement", "actions": ["Seuils de décision différenciés", "Vérification humaine systématique pour les groupes à risque"]}
    ]
  },
  [
    {"prompt": "Comment tester si notre modèle de recrutement est biaisé ?", "answer": "Test de parité démographique : soumettre des CVs identiques en changeant uniquement le nom (signal probable du genre ou de l'origine). Si le taux de sélection varie significativement, il y a un biais. C'est le principe du CV testing, désormais utilisable automatiquement avec des outils comme AI Fairness 360. Résultat documenté et action de correction avant déploiement."},
    {"prompt": "Peut-on avoir un système IA parfaitement équitable ?", "answer": "Non — et c'est mathématiquement démontré (impossibilité de satisfaire simultanément toutes les définitions de fairness en présence d'inégalités dans les données). Ce qu'on peut faire : choisir explicitement quelle définition de l'équité est prioritaire dans le contexte donné, la mesurer, et en assumer les compromis avec les parties prenantes."}
  ],
  ["biais", "fairness", "équité", "discrimination", "disparate impact"]
))

save("professional/governance_ai/model_lifecycle_management.json", ku_gov(
  "model_lifecycle_management",
  "Gestion du cycle de vie des modèles IA",
  "Un modèle IA n'est pas un logiciel statique — il se dégrade dans le temps (model drift), doit être mis à jour, versionné et éventuellement retiré. La gestion du cycle de vie structure ces étapes de façon contrôlée.",
  "La gestion du cycle de vie des modèles IA (MLOps) est l'ensemble des pratiques permettant de développer, déployer, monitorer, mettre à jour et retirer les modèles IA de façon contrôlée, reproductible et conforme aux exigences opérationnelles et réglementaires.",
  {
    "lifecycle_phases": [
      {"phase": "Développement", "activities": ["Collecte et préparation des données", "Entraînement et validation", "Tests de performance et d'équité"]},
      {"phase": "Déploiement", "activities": ["Validation formelle pré-déploiement", "Déploiement progressif (canary, blue-green)", "Documentation technique complète"]},
      {"phase": "Production", "activities": ["Monitoring continu des métriques", "Détection de dérive (data drift, model drift)", "Gestion des incidents"]},
      {"phase": "Mise à jour", "activities": ["Retrain avec nouvelles données", "Tests de régression sur comportements clés", "Versioning et changelog"]},
      {"phase": "Retrait", "activities": ["Archivage documenté", "Migration des utilisateurs", "Conformité avec obligations de conservation des données"]}
    ],
    "mlops_key_practices": [
      "Versioning systématique des modèles, des données et des configurations",
      "Pipeline de CI/CD pour les modèles (tests automatiques avant déploiement)",
      "Feature store partagé pour la cohérence entre entraînement et inférence",
      "A/B testing contrôlé pour les nouvelles versions",
      "Rollback automatique si métriques de qualité chutent en dessous du seuil"
    ]
  },
  [
    {"prompt": "Notre modèle IA fonctionne moins bien qu'il y a 6 mois — que faire ?", "answer": "Model drift. Vérifier d'abord : data drift (les données d'entrée ont-elles changé de distribution ?) ou model drift (le monde réel a changé mais le modèle est resté figé). Solution court terme : identifier les cas où le modèle échoue le plus, analyser pourquoi, retrain ciblé si possible. Solution long terme : pipeline de monitoring continu avec alertes automatiques."},
    {"prompt": "Comment gérer le déploiement d'une nouvelle version du modèle sans risque ?", "answer": "Déploiement progressif (canary release) : commencer par 5-10% du trafic sur la nouvelle version, monitorer les métriques clés en comparaison avec l'ancienne version pendant 24-48h, puis augmenter progressivement. Plan de rollback automatique si les métriques passent en dessous du seuil défini. Ne jamais déployer une nouvelle version sans définir au préalable les critères de succès et d'échec."}
  ],
  ["MLOps", "cycle de vie", "model drift", "versioning", "déploiement"]
))

save("professional/governance_ai/human_ai_collaboration.json", ku_gov(
  "human_ai_collaboration",
  "Collaboration humain-IA",
  "L'IA performante n'est pas celle qui remplace l'humain, mais celle qui augmente ses capacités là où elle excelle tout en laissant les décisions à fort enjeu au jugement humain. Concevoir la bonne allocation humain-IA est une compétence de gouvernance.",
  "La collaboration humain-IA est le design de la répartition optimale des tâches entre l'humain et le système IA, en tirant parti des forces de chacun — l'IA pour la vitesse, le volume et la cohérence ; l'humain pour le jugement, l'éthique et les situations hors normes.",
  {
    "allocation_framework": [
      {"task_type": "Volume + répétition + cohérence requise", "recommendation": "IA en autonomie avec supervision humaine par échantillonnage"},
      {"task_type": "Création, nuance, jugement contextuel", "recommendation": "Humain avec assistance IA (suggestion + vérification)"},
      {"task_type": "Décisions à fort impact irréversible", "recommendation": "Humain décide, IA informe et documente"},
      {"task_type": "Situations hors distribution (inédites)", "recommendation": "Humain en premier — l'IA n'est pas fiable sur ce qu'elle n'a pas vu"}
    ],
    "human_oversight_levels": [
      {"level": "Humain dans la boucle (HITL)", "description": "L'humain valide chaque décision IA avant exécution — sécurité maximale, scalabilité minimale"},
      {"level": "Humain sur la boucle (HOTL)", "description": "L'IA agit, l'humain surveille et peut intervenir — bon équilibre pour les systèmes à risque limité"},
      {"level": "Humain hors de la boucle", "description": "L'IA agit en autonomie complète — acceptable uniquement pour les risques minimaux et avec monitoring automatisé robuste"}
    ],
    "collaboration_design_principles": [
      "Rendre visible ce que l'IA ne sait pas (incertitude, cas limites)",
      "Faciliter l'overriding humain sans friction",
      "Former les utilisateurs aux forces ET aux limites du système",
      "Éviter l'automation bias : tendance à faire confiance à l'IA même quand elle a tort"
    ]
  },
  [
    {"prompt": "Comment décider ce qu'ALFRED peut faire seul vs ce qui nécessite ma validation ?", "answer": "La règle : plus la conséquence est irréversible et à fort impact, plus tu dois valider. ALFRED peut gérer en autonomie les informations, les synthèses, les suggestions de structuration. Pour les décisions qui t'engagent (actions, communications importantes, choix financiers) — ALFRED propose, tu décides. Et si tu n'es pas sûr : demande à ALFRED d'expliquer son raisonnement avant de valider."},
    {"prompt": "Comment éviter de trop faire confiance à l'IA et de ne plus exercer son propre jugement ?", "answer": "L'automation bias est un risque réel — documenté dans les études sur les copilotes d'avion et les médecins assistés par IA. Deux pratiques : challenger systématiquement les suggestions IA ('pourquoi ?', 'qu'est-ce qui pourrait contredire ça ?') et maintenir une pratique autonome régulière pour ne pas perdre ses compétences propres. L'IA est un miroir de ta pensée — pas un substitut."}
  ],
  ["collaboration", "human in the loop", "oversight", "automation bias", "augmentation"]
))

save("professional/governance_ai/ai_incident_management.json", ku_gov(
  "ai_incident_management",
  "Gestion des incidents IA",
  "Les incidents IA (comportements inattendus, biais détectés, erreurs systématiques) doivent être gérés comme des incidents critiques : signalement rapide, analyse de cause racine, correction et communication transparente.",
  "La gestion des incidents IA est le processus structuré de détection, classification, investigation, correction et communication autour des comportements inattendus ou problématiques d'un système IA en production.",
  {
    "incident_classification": [
      {"severity": "Critique (P1)", "examples": "Décision IA qui cause un préjudice réel, fuite de données via le LLM, comportement discriminatoire systématique", "SLA": "Correction ou arrêt sous 4h"},
      {"severity": "Élevé (P2)", "examples": "Dégradation significative des performances, réponses incorrectes sur des cas importants", "SLA": "Investigation sous 24h, correction sous 72h"},
      {"severity": "Modéré (P3)", "examples": "Anomalie détectée, réponse inattendue isolée", "SLA": "Investigation sous 1 semaine"},
      {"severity": "Faible (P4)", "examples": "Amélioration souhaitée, cas limite non critique", "SLA": "Backlog d'amélioration"}
    ],
    "incident_process": [
      "Détection (monitoring automatique ou signalement humain)",
      "Triage et classification en P1-P4",
      "Notification de l'AI Owner et des parties prenantes",
      "Investigation de la cause racine",
      "Correction (patch modèle, règle de filtrage, rollback)",
      "Post-mortem documenté",
      "Communication aux utilisateurs impactés si P1/P2"
    ],
    "post_mortem_template": ["Qu'est-il arrivé exactement ?", "Quel a été l'impact ?", "Pourquoi est-ce arrivé (cause racine) ?", "Que fait-on pour éviter que ça se reproduise ?", "Quelles mesures de détection améliorons-nous ?"]
  },
  [
    {"prompt": "Notre IA a donné des réponses bizarres toute la matinée — que faire ?", "answer": "Protocole d'incident : documenter les cas (inputs + outputs), déterminer la sévérité (utilisateurs impactés, type d'erreur), notifier l'AI Owner et activer l'investigation. Si le comportement est potentiellement dangereux ou discriminatoire, passer en P1 et envisager la suspension du service pendant l'investigation. Ne pas attendre que ça 'se corrige tout seul'."},
    {"prompt": "Comment éviter de cacher un incident IA pour protéger l'image de l'entreprise ?", "answer": "Deux arguments pour la transparence : légal (l'EU AI Act impose la notification des incidents graves aux autorités) et réputationnel (la découverte post-couvrement est systématiquement plus destructrice que la déclaration proactive). Un post-mortem public bien géré renforce souvent la confiance plutôt que de la détruire."}
  ],
  ["incident", "gestion de crise", "post-mortem", "P1", "signalement"]
))

save("professional/governance_ai/data_governance_ai.json", ku_gov(
  "data_governance_ai",
  "Gouvernance des données pour l'IA",
  "La qualité, la provenance et la conformité des données d'entraînement et d'inférence déterminent la qualité et la légalité des systèmes IA. La gouvernance des données IA articule collecte, consentement, qualité et rétention.",
  "La gouvernance des données pour l'IA est l'ensemble des politiques, processus et contrôles qui assurent que les données utilisées pour entraîner, valider et opérer les systèmes IA sont de qualité suffisante, légalement obtenues, conformes aux réglementations et tracées tout au long de leur cycle de vie.",
  {
    "data_governance_components": [
      {"component": "Catalogue de données", "description": "Inventaire documenté de toutes les données utilisées : source, format, qualité, consentement"},
      {"component": "Data lineage", "description": "Traçabilité complète : d'où viennent les données, comment ont-elles été transformées, où sont-elles utilisées"},
      {"component": "Qualité des données", "description": "Métriques de complétude, cohérence, exactitude et fraîcheur — monitorer en continu"},
      {"component": "Consentement et RGPD", "description": "Vérification que les données d'entraînement respectent le consentement des personnes concernées"},
      {"component": "Rétention et droit à l'oubli", "description": "Processus pour supprimer les données à la demande ou en fin de durée de conservation"}
    ],
    "ai_specific_data_risks": [
      "Données d'entraînement avec biais historiques — reproduits et amplifiés par le modèle",
      "Données personnelles utilisées sans consentement adéquat pour l'IA",
      "Contamination train/test qui surestime les performances",
      "Données synthétiques insuffisamment validées",
      "Mémorisation par le LLM de données sensibles restituables via prompts"
    ]
  },
  [
    {"prompt": "Peut-on utiliser les données clients pour entraîner notre modèle IA ?", "answer": "Oui, sous conditions strictes : consentement explicite pour cet usage spécifique dans les CGU, anonymisation si les données sont sensibles, mention dans la politique de confidentialité, et droit à l'oubli applicable (si un client demande la suppression, ses données doivent être retirées du dataset et le modèle potentiellement retrained). Consulter le DPO avant toute collecte."},
    {"prompt": "Comment s'assurer que les données d'entraînement sont de bonne qualité ?", "answer": "Cinq dimensions : complétude (pas trop de valeurs manquantes), exactitude (les labels sont corrects), cohérence (pas de contradictions internes), fraîcheur (les données sont récentes) et représentativité (couvrent tous les cas d'usage et groupes d'utilisateurs). Un audit de qualité des données avant tout entraînement est non négociable."}
  ],
  ["données", "data governance", "RGPD", "data lineage", "consentement"]
))

print("\nBatch 6 governance_ai (10 premiers fichiers) : DONE")
