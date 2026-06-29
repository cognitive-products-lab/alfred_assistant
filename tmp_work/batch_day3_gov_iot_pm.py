"""
Enrichissement day3 — governance_ai (6) + iot (8) + product_management/advanced (4) = 18 KU
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

def ku(id_, title, domain, subdomain, priority, summary, core_def, knowledge, examples, guidance, tags):
    return {"schema_version": "1.2", "type": "knowledge_unit", "id": id_, "title": title,
            "domain": domain, "subdomain": subdomain, "status": "validated", "metadata": meta(),
            "priority": priority, "summary": summary, "core_definition": core_def,
            "knowledge": knowledge, "example_answers": examples, "response_guidance": guidance,
            "tags": tags, "related_knowledge_units": []}

# ═══════════════════════════════════════════════════════
# PROFESSIONAL / GOVERNANCE_AI (6 KU)
# ═══════════════════════════════════════════════════════

save("professional/governance_ai/compliance_monitoring.json", ku(
    "knowledges.professional.governance_ai.compliance_monitoring",
    "Monitoring de conformité IA — surveiller l'alignement continu des systèmes",
    "professional", "governance_ai", "high",
    "Comment mettre en place une surveillance continue de la conformité des systèmes IA aux réglementations, aux politiques internes et aux engagements éthiques — au-delà de l'audit ponctuel.",
    "Le monitoring de conformité IA est le processus continu de surveillance des systèmes d'intelligence artificielle pour vérifier qu'ils respectent les exigences réglementaires (EU AI Act, RGPD), les politiques internes et les principes éthiques définis lors de leur conception, en détectant les dérives avant qu'elles causent des dommages.",
    {"dimensions": {
        "technique": "Performance, biais, dérive des données (data drift), robustesse",
        "reglementaire": "Conformité EU AI Act, RGPD, sectorielles (médical, finance)",
        "ethique": "Équité, transparence, non-discrimination",
        "operationnel": "Disponibilité, latence, taux d'erreur"
     },
     "metriques_cles": {
        "biais": "Mesure de l'équité selon différents groupes démographiques",
        "derive": "Écart entre la distribution des données d'entraînement et les données de production",
        "explicabilite": "Capacité à expliquer les décisions aux parties prenantes",
        "incidents": "Taux et gravité des incidents IA détectés"
     },
     "outils": ["Tableaux de bord de monitoring ML (MLflow, Evidently, WhyLogs)", "Alertes automatiques sur seuils", "Rapports de conformité périodiques", "Registre d'incidents"],
     "frequence": "Monitoring en continu pour les systèmes critiques, revue mensuelle pour les systèmes à risque moyen, audit annuel minimum pour tous"},
    [{"prompt": "Comment surveiller qu'un système IA reste conforme dans le temps ?", "answer": "Trois niveaux : 1) Monitoring automatisé en temps réel sur les métriques techniques (performance, dérive des données, taux d'erreur). 2) Revue périodique humaine sur les métriques éthiques et réglementaires (biais, équité, conformité RGPD). 3) Audit indépendant annuel. Sans monitoring continu, la conformité initiale ne garantit rien — les modèles dérivent, les usages évoluent, les réglementations changent."},
     {"prompt": "Qu'est-ce que la dérive de données dans un système IA ?", "answer": "La dérive (data drift) se produit quand la distribution des données en production s'éloigne de celle utilisée pour l'entraînement. Exemple : un modèle entraîné sur des données 2022 voit arriver des comportements utilisateurs 2024 différents — ses prédictions se dégradent progressivement. La détection nécessite de comparer régulièrement la distribution des entrées actuelles à la distribution de référence, et de ré-entraîner ou recalibrer quand l'écart dépasse un seuil."}],
    {"tone": "technique, orienté mise en pratique", "structure": ["dimensions", "métriques", "outils", "fréquence"], "avoid": ["trop théorique", "ignorer les systèmes en production"]},
    ["conformité", "monitoring", "IA", "data drift", "biais", "EU AI Act", "gouvernance"]
))

save("professional/governance_ai/decision_transparency.json", ku(
    "knowledges.professional.governance_ai.decision_transparency",
    "Transparence des décisions IA — rendre les choix algorithmiques intelligibles",
    "professional", "governance_ai", "high",
    "Méthodes et obligations pour rendre compréhensibles les décisions prises ou assistées par des systèmes IA — pour les utilisateurs, les régulateurs et les parties affectées.",
    "La transparence des décisions IA désigne la capacité d'un système à expliquer, de manière compréhensible pour des non-experts, comment et pourquoi il est parvenu à une décision, une recommandation ou une classification particulière.",
    {"niveaux": {
        "global": "Comment le modèle fonctionne en général (architecture, données d'entraînement, objectif)",
        "local": "Pourquoi cette décision spécifique pour cet individu",
        "contrefactuel": "\"Qu'est-ce qui aurait changé si X avait été différent ?\""
     },
     "obligations_legales": {
        "RGPD_art22": "Droit à l'explication pour les décisions automatisées impactant significativement",
        "EU_AI_Act": "Systèmes à haut risque : documentation, traçabilité, logs obligatoires",
        "sectorielles": "Finance (MiFID), médical (MDR), RH (EEOC aux USA)"
     },
     "outils_xai": {
        "SHAP": "Valeurs de Shapley — contribution de chaque feature à la décision",
        "LIME": "Approximation locale linéaire pour expliquer une prédiction spécifique",
        "attention_maps": "Pour les transformers — zones d'attention visualisées",
        "counterfactuals": "\"Si votre revenu était X, la décision aurait été Y\""
     },
     "communication": "L'explication doit être adaptée à l'audience : technique pour les auditeurs, naturelle pour les utilisateurs affectés"},
    [{"prompt": "Mon système IA prend des décisions mais je ne peux pas expliquer pourquoi. Est-ce un problème ?", "answer": "Oui, potentiellement un problème légal et éthique. Si ces décisions affectent des personnes (crédit, emploi, santé, sécurité), le RGPD article 22 impose un droit à l'explication, et l'EU AI Act exige la traçabilité pour les systèmes à haut risque. Même hors obligation légale, un système qu'on ne peut pas expliquer est un système dont on ne peut pas détecter les biais ni auditer les erreurs."},
     {"prompt": "Comment expliquer une décision IA à un client non-technique ?", "answer": "Format contrefactuel : il est plus compréhensible que les scores de contribution. \"Votre demande a été refusée parce que votre ancienneté est inférieure à 2 ans. Si votre ancienneté avait été de 3 ans, la décision aurait été favorable.\" C'est actionnable et compréhensible sans mathématiques. Les valeurs SHAP sont pour les auditeurs — pas pour les utilisateurs finaux."}],
    {"tone": "juridique et technique, équilibré", "structure": ["niveaux", "obligations", "outils XAI", "communication"], "avoid": ["jargon pur", "ignorer la dimension légale"]},
    ["transparence", "XAI", "explicabilité", "RGPD", "EU AI Act", "décision IA", "gouvernance"]
))

save("professional/governance_ai/eu_ai_act_basics.json", ku(
    "knowledges.professional.governance_ai.eu_ai_act_basics",
    "EU AI Act — les fondamentaux du règlement européen sur l'IA",
    "professional", "governance_ai", "critical",
    "Présentation des éléments clés de l'EU AI Act : classification par risque, obligations par catégorie, calendrier d'application et impact pour les organisations qui développent ou utilisent de l'IA.",
    "L'EU AI Act (Règlement UE 2024/1689) est le premier cadre réglementaire mondial contraignant sur l'intelligence artificielle, adopté en 2024 et applicable progressivement jusqu'en 2027. Il classe les systèmes IA par niveau de risque et impose des obligations proportionnelles.",
    {"classification_risques": {
        "inacceptable": "Interdit : manipulation subliminale, score social, reconnaissance faciale en temps réel dans l'espace public (sauf exceptions), exploitation de vulnérabilités",
        "haut_risque": "Obligations strictes : infrastructures critiques, éducation, emploi, services essentiels, law enforcement, migration, justice",
        "risque_limite": "Obligations de transparence : chatbots (dire que c'est une IA), deepfakes (labellisation)",
        "risque_minimal": "Libre : filtres spam, IA dans jeux vidéo, recommandations non-critiques"
     },
     "obligations_haut_risque": [
        "Système de management du risque",
        "Gouvernance des données",
        "Documentation technique",
        "Transparence et information utilisateurs",
        "Contrôle humain (human oversight)",
        "Robustesse, précision et cybersécurité",
        "Enregistrement dans la base de données EU"
     ],
     "calendrier": {
        "2024": "Entrée en vigueur (août 2024)",
        "2025-02": "Interdictions applicables (systèmes inacceptables)",
        "2025-08": "GPAI models applicables",
        "2026-08": "Systèmes haut risque (Annexe III)",
        "2027-08": "Systèmes haut risque (Annexe I)"
     },
     "modeles_fondation": "Les GPAI (General Purpose AI) comme GPT, Claude, Gemini ont des obligations spécifiques de transparence et d'évaluation des risques systémiques si > 10^25 FLOPS"},
    [{"prompt": "Mon application utilise de l'IA pour le recrutement. Suis-je concernée par l'EU AI Act ?", "answer": "Oui — le recrutement est explicitement listé en Annexe III comme système IA à haut risque. Tu dois : mettre en place un système de management du risque, documenter le système, assurer la transparence envers les candidats, maintenir des logs, et garantir un contrôle humain sur les décisions finales. Les obligations s'appliquent à partir d'août 2026. Ne pas attendre — la mise en conformité prend du temps."},
     {"prompt": "C'est quoi concrètement un système IA à haut risque ?", "answer": "L'EU AI Act liste 8 catégories : infrastructures critiques (eau, énergie), éducation et formation professionnelle, emploi et gestion RH, services essentiels (crédit, assurance), law enforcement, migration et contrôle aux frontières, administration de la justice, démocratie. Si ton système IA prend ou assiste des décisions dans ces domaines, il est à haut risque — peu importe la technologie utilisée."}],
    {"tone": "juridique accessible, orienté conformité pratique", "structure": ["classification", "obligations", "calendrier", "GPAI"], "avoid": ["jargon juridique pur", "alarmisme", "ignorer le calendrier"]},
    ["EU AI Act", "réglementation", "IA", "conformité", "haut risque", "gouvernance", "Europe"]
))

save("professional/governance_ai/explainability_xai.json", ku(
    "knowledges.professional.governance_ai.explainability_xai",
    "Explicabilité IA (XAI) — méthodes et mise en pratique",
    "professional", "governance_ai", "high",
    "Tour d'horizon des méthodes d'explicabilité des systèmes IA (SHAP, LIME, attention, counterfactuals) avec leurs cas d'usage, limites et comment les intégrer dans un projet.",
    "L'explicabilité des systèmes IA (XAI — eXplainable AI) regroupe les méthodes techniques permettant de comprendre, interpréter et communiquer les décisions prises par des modèles d'apprentissage automatique, en réponse aux exigences de transparence des régulateurs, des utilisateurs et des équipes internes.",
    {"methodes_principales": {
        "SHAP": {
            "principe": "Valeurs de Shapley issues de la théorie des jeux — contribution marginale de chaque feature",
            "avantages": "Cohérent, applicable à tout modèle, global et local",
            "limites": "Coûteux en calcul pour de grands datasets"
        },
        "LIME": {
            "principe": "Approximation locale par un modèle linéaire interprétable",
            "avantages": "Intuitif, rapide",
            "limites": "Instable — deux runs peuvent donner des explications différentes"
        },
        "attention": {
            "principe": "Visualisation des poids d'attention dans les transformers",
            "avantages": "Natif aux LLM et modèles vision",
            "limites": "L'attention n'est pas toujours l'explication — corrélation, pas causalité"
        },
        "counterfactuals": {
            "principe": "\"Qu'est-ce qui aurait dû changer pour obtenir un résultat différent ?\"",
            "avantages": "Très compréhensible pour les non-experts, actionnable",
            "limites": "Peut trouver des counterfactuals non réalistes"
        }
     },
     "intrinsec_vs_post_hoc": {
        "intrinsec": "Modèles nativement interprétables : arbres de décision, régression linéaire, règles",
        "post_hoc": "SHAP, LIME appliqués à un modèle boîte noire après coup"
     },
     "choix_methode": "Dépend du contexte : audit réglementaire → SHAP global. Explication individuelle → counterfactual. Débogage → attention maps + SHAP local."},
    [{"prompt": "Comment savoir quelle méthode XAI utiliser ?", "answer": "Trois questions : 1) Pour qui ? (auditeur, utilisateur final, data scientist) — les niveaux de technicité sont différents. 2) Global ou local ? (comprendre le modèle en général vs expliquer une décision spécifique). 3) Modèle accessible ou boîte noire ? Si le modèle est accessible, SHAP est souvent le meilleur choix. Pour l'explication utilisateur final, les counterfactuals sont les plus compréhensibles."},
     {"prompt": "L'attention d'un transformeur explique-t-elle vraiment ses décisions ?", "answer": "Pas toujours — c'est un débat actif. Des études (Jain & Wallace 2019) montrent que l'attention n'est pas toujours corrélée à l'importance des inputs pour la décision finale. Elle dit \"sur quoi le modèle a porté son attention\" pas nécessairement \"pourquoi il a décidé ça\". Pour l'explicabilité réglementaire, SHAP post-hoc est plus robuste que l'attention seule."}],
    {"tone": "technique, nuancé sur les limites", "structure": ["méthodes", "intrinsèque vs post-hoc", "guide de choix"], "avoid": ["présenter XAI comme une solution complète", "ignorer les limites de chaque méthode"]},
    ["XAI", "explicabilité", "SHAP", "LIME", "attention", "counterfactuals", "IA", "gouvernance"]
))

save("professional/governance_ai/gdpr_ai_intersection.json", ku(
    "knowledges.professional.governance_ai.gdpr_ai_intersection",
    "RGPD et IA — obligations spécifiques à l'intersection des deux",
    "professional", "governance_ai", "high",
    "Points de friction et obligations à l'intersection du RGPD et des systèmes IA : licéité du traitement, minimisation, droit à l'explication, DPIA, et données d'entraînement.",
    "L'intersection RGPD-IA couvre les obligations légales spécifiques qui émergent quand des systèmes d'IA traitent des données personnelles — en particulier les exigences de licéité, de minimisation, de transparence et de droits des personnes concernées appliquées aux modèles ML.",
    {"points_cles": {
        "licéité": "La base légale du traitement doit être définie avant l'entraînement — consentement, intérêt légitime ou contrat",
        "minimisation": "N'utiliser que les données nécessaires — challenge pour le ML qui performe souvent mieux avec plus de données",
        "finalité": "Les données collectées pour un usage ne peuvent pas être utilisées pour entraîner un modèle à une autre finalité sans base légale supplémentaire",
        "droit_explication": "Art. 22 RGPD : droit à ne pas faire l'objet d'une décision automatisée significative sans intervention humaine",
        "droit_effacement": "Droit à l'oubli : complexe avec les modèles ML qui ont \"mémorisé\" des données d'entraînement"
     },
     "DPIA": "Data Protection Impact Assessment obligatoire pour les traitements à risque élevé — notamment les systèmes IA qui profiling à grande échelle ou décisions automatisées",
     "données_entrainement": {
        "données_publiques": "Pas nécessairement libres d'utilisation pour l'entraînement — droits d'auteur + RGPD si données personnelles",
        "données_syntetiques": "Alternative pour préserver la privacy — mais attention aux biais amplifiés",
        "pseudonymisation": "Réduit le risque mais ne supprime pas les obligations RGPD si re-identification possible"
     },
     "droit_a_l_oubli_ml": "Problème ouvert : les modèles ML peuvent avoir mémorisé des données individuelles (membership inference attacks). Machine unlearning = domaine de recherche actif."},
    [{"prompt": "Peut-on utiliser les données clients pour entraîner un modèle IA ?", "answer": "Ça dépend de la base légale du traitement initial. Si les données ont été collectées pour \"fournir le service X\", les utiliser pour entraîner un modèle est une nouvelle finalité — ce qui nécessite une base légale supplémentaire (nouveau consentement, ou intérêt légitime avec DPIA). Les mentions légales vagues de type \"améliorer nos services\" sont de plus en plus contestées. Consulter un DPO avant de procéder."},
     {"prompt": "Comment gérer le droit à l'effacement quand des données ont été utilisées pour entraîner un modèle ?", "answer": "C'est l'un des points les plus complexes du RGPD appliqué à l'IA. Le modèle peut avoir \"mémorisé\" les données — la suppression de la donnée source ne suffit pas. Les approches : 1) Differential privacy à l'entraînement (ajoute du bruit pour limiter la mémorisation). 2) Ré-entraînement sans la donnée demandée (coûteux). 3) Machine unlearning (technologie émergente). Documenter le problème et avoir un plan est déjà une bonne pratique RGPD."}],
    {"tone": "juridique accessible, orienté compliance", "structure": ["points clés", "DPIA", "données d'entraînement", "droit à l'oubli"], "avoid": ["juridique pur inaccessible", "ignorer les cas pratiques"]},
    ["RGPD", "GDPR", "IA", "données personnelles", "droit explication", "DPIA", "conformité"]
))

save("professional/governance_ai/traceability_principles.json", ku(
    "knowledges.professional.governance_ai.traceability_principles",
    "Traçabilité des systèmes IA — logs, audits et chaîne de responsabilité",
    "professional", "governance_ai", "high",
    "Principes et pratiques pour assurer la traçabilité complète des systèmes IA : logs des décisions, versioning des modèles, chaîne de responsabilité et auditabilité.",
    "La traçabilité IA est la capacité à reconstituer a posteriori comment un système IA a pris une décision donnée, quelles données il a utilisées, quelle version du modèle était active, et qui était responsable — exigence réglementaire pour les systèmes à haut risque et bonne pratique universelle.",
    {"dimensions": {
        "modele": "Versioning (MLflow, DVC), métadonnées d'entraînement, datasets utilisés",
        "decisions": "Logs structurés : input, output, timestamp, version modèle, identifiant utilisateur",
        "donnees": "Data lineage — d'où viennent les données, comment ont-elles été transformées",
        "humain": "Qui a approuvé le déploiement, qui peut l'arrêter, qui est notifié en cas d'incident"
     },
     "exigences_eu_ai_act": "Systèmes haut risque : logs automatiques, conservation minimum 6 mois post-cycle de vie, accès aux autorités de surveillance",
     "bonnes_pratiques": {
        "log_minimal": "Pour chaque décision : input hash, output, model_version, timestamp, user_id (anonymisé si besoin)",
        "versioning": "Toute modification de modèle = nouvelle version immutable avec metadata complète",
        "rollback": "Capacité à revenir à une version précédente en moins de X heures",
        "incident_trail": "Chaque incident doit pouvoir être retracé jusqu'à la cause racine"
     },
     "chain_responsabilite": "Clarifier : qui est responsable de chaque composant (fournisseur du modèle, développeur de l'application, déployeur, utilisateur final) — surtout critique avec les LLM tiers"},
    [{"prompt": "Quels logs minimaux dois-je tenir pour un système IA en production ?", "answer": "Pour chaque décision ou output : timestamp, identifiant de la requête, version du modèle, hash de l'input (ou l'input complet si pas de données personnelles), output, durée de traitement, et si applicable l'identifiant utilisateur (pseudonymisé). Pour les systèmes à haut risque EU AI Act : conservation minimum 6 mois, accès possible aux autorités. Stocker dans un système immuable (append-only) pour garantir l'intégrité."},
     {"prompt": "Comment gérer la traçabilité quand j'utilise un LLM externe (OpenAI, Anthropic) ?", "answer": "La traçabilité s'arrête à la frontière de l'API — tu n'as pas accès aux logs internes du LLM. Ce que tu peux contrôler : logger systématiquement les prompts envoyés et les réponses reçues (attention RGPD si données personnelles dans le prompt), versionner les prompts comme du code, et documenter la chaîne de responsabilité (toi comme déployeur, le fournisseur comme fournisseur de modèle). L'EU AI Act distingue ces responsabilités."}],
    {"tone": "technique, orienté conformité pratique", "structure": ["dimensions", "exigences légales", "bonnes pratiques", "responsabilité"], "avoid": ["trop abstrait", "ignorer les LLM tiers"]},
    ["traçabilité", "logs", "audit", "IA", "versioning", "EU AI Act", "responsabilité", "gouvernance"]
))

# ═══════════════════════════════════════════════════════
# PROFESSIONAL / IOT (8 KU)
# ═══════════════════════════════════════════════════════

save("professional/iot/iot_device_segmentation.json", ku(
    "knowledges.professional.iot.iot_device_segmentation",
    "Segmentation réseau IoT — isoler les objets connectés",
    "professional", "iot", "high",
    "Pourquoi et comment isoler les appareils IoT sur des segments réseau dédiés pour limiter la surface d'attaque et protéger le réseau principal.",
    "La segmentation réseau IoT est la pratique de placer les appareils connectés sur des segments réseau (VLAN) séparés du réseau principal, limitant leur capacité à communiquer avec d'autres systèmes et contenant les compromissions éventuelles.",
    {"pourquoi": {
        "surface_attaque": "Un appareil IoT compromis sur le réseau principal peut atteindre tous les systèmes",
        "firmware_non_maintenu": "Beaucoup d'appareils IoT ont des firmware non mis à jour avec des vulnérabilités connues",
        "credentials_par_defaut": "Identifiants d'usine souvent non changés — vecteur d'attaque trivial"
     },
     "architecture": {
        "vlan_iot": "VLAN dédié IoT — accès internet autorisé, accès au réseau principal bloqué",
        "vlan_management": "VLAN séparé pour la gestion des équipements réseau",
        "dmz": "Pour les appareils nécessitant un accès entrant depuis internet",
        "firewall_rules": "Whitelist : n'autoriser que les flux IoT strictement nécessaires"
     },
     "alfred_context": "ALFRED recommande une segmentation VLAN pour tous les appareils domotiques (Tuya, Google Home, caméras) — séparés du PC ALFRED et du réseau professionnel.",
     "mise_en_oeuvre": "Switch manageable (ex : SG108E) + routeur VLAN-capable (ex : ER605) — configuration minimum pour un usage domestique ou PME"},
    [{"prompt": "Pourquoi mettre les appareils IoT sur un VLAN séparé ?", "answer": "Principe de confinement : si une ampoule connectée ou une caméra est compromise (firmware vulnérable, mot de passe par défaut), elle ne doit pas pouvoir atteindre ton NAS, ton PC ou ton réseau professionnel. Sur un VLAN IoT isolé, la compromission reste dans le segment IoT. C'est le même principe que les zones réseau en entreprise — appliquer à la maison."},
     {"prompt": "Comment segmenter mon réseau domotique sans être expert réseau ?", "answer": "Avec un routeur moderne (Unifi, TP-Link ER605, Firewalla) : créer un VLAN IoT, y connecter tous les appareils domotiques (WiFi IoT séparé du WiFi principal), et configurer une règle firewall : IoT → Internet oui, IoT → réseau principal non. Les interfaces graphiques des routeurs modernes rendent ça faisable en 30-60 minutes sans ligne de commande."}],
    {"tone": "technique accessible, contextualisé ALFRED", "structure": ["pourquoi", "architecture", "mise en oeuvre"], "avoid": ["trop expert", "ignorer le contexte domestique"]},
    ["IoT", "VLAN", "segmentation réseau", "sécurité", "domotique", "ALFRED"]
))

save("professional/iot/iot_threat_basics.json", ku(
    "knowledges.professional.iot.iot_threat_basics",
    "Menaces IoT — panorama des risques des objets connectés",
    "professional", "iot", "high",
    "Cartographie des principales menaces pesant sur les appareils IoT : attaques de firmware, botnets, interceptions, accès non autorisés et déni de service.",
    "Les menaces IoT sont les risques de sécurité spécifiques aux objets connectés, aggravés par la diversité des fabricants, la faible mise à jour des firmwares, les ressources limitées pour la sécurité embarquée et la multiplication des points d'entrée sur le réseau.",
    {"menaces_principales": {
        "credential_stuffing": "Identifiants par défaut testés automatiquement — vecteur le plus commun",
        "firmware_vulnerabilities": "CVE sur les firmwares non mis à jour — souvent jamais patchés",
        "botnet_recrutement": "Appareils compromis recrutés dans des botnets (Mirai, Mozi)",
        "man_in_the_middle": "Interception des communications non-chiffrées entre l'appareil et le cloud",
        "physical_access": "Extraction de firmware ou credentials via port série/JTAG",
        "supply_chain": "Appareils livrés avec malware préinstallé — rare mais documenté"
     },
     "facteurs_aggravants": [
        "Cycle de vie long (10+ ans) avec support fabricant court (2-3 ans)",
        "Pas de mécanisme de mise à jour automatique fiable sur les appareils bon marché",
        "Protocoles propriétaires avec chiffrement faible ou absent",
        "Impossible de déployer un agent de sécurité sur la plupart des appareils"
     ],
     "exemples_reels": {
        "Mirai": "2016 — botnet de caméras IP compromises, DDoS à 620 Gbps",
        "Verkada": "2021 — 150 000 caméras de surveillance piratées",
        "Philips_Hue": "2020 — CVE permettant de pivoter vers le réseau via l'ampoule"
     }},
    [{"prompt": "Mes appareils domotiques sont-ils un risque de sécurité ?", "answer": "Oui, potentiellement. Les risques concrets : identifiants par défaut non changés (vérifier immédiatement), firmware jamais mis à jour (vérifier les mises à jour disponibles), et appareils sur le même réseau que tes données sensibles (corriger avec la segmentation VLAN). Les appareils bon marché de marques inconnues sont les plus risqués — firmware propriétaire opaque, peu ou pas de CVE patchés."},
     {"prompt": "Qu'est-ce que le botnet Mirai ?", "answer": "Mirai (2016) est le botnet IoT le plus connu : il a compromis des centaines de milliers de caméras IP et DVRs en testant des identifiants par défaut (admin/admin, root/root, etc.). Ces appareils ont été utilisés pour lancer une attaque DDoS de 620 Gbps contre Dyn (provider DNS) — coupant l'accès à Twitter, Netflix, Reddit pendant des heures. La leçon : des ampoules et caméras non sécurisées peuvent participer à des attaques mondiales."}],
    {"tone": "sécurité, factuel, concret avec exemples réels", "structure": ["menaces", "facteurs aggravants", "exemples"], "avoid": ["alarmisme sans solutions", "trop technique sans contexte"]},
    ["IoT", "sécurité", "menaces", "botnet", "Mirai", "firmware", "domotique"]
))

save("professional/iot/local_network_security.json", ku(
    "knowledges.professional.iot.local_network_security",
    "Sécurité du réseau local — défense en profondeur à domicile et PME",
    "professional", "iot", "high",
    "Mesures de sécurité pour protéger un réseau local contre les intrusions, les compromissions internes et les fuites de données — applicable au domicile comme en petite structure.",
    "La sécurité du réseau local désigne l'ensemble des mesures architecturales et de configuration qui protègent les systèmes et données d'un réseau privé contre les accès non autorisés, qu'ils proviennent d'internet, d'appareils compromis sur le réseau ou d'acteurs internes.",
    {"couches_defense": {
        "perimetre": "Firewall, NAT, IDS/IPS — filtrer le trafic entrant et sortant",
        "segmentation": "VLAN par type d'usage — IoT, invité, pro, serveurs",
        "acces": "WPA3, VPN pour accès distants, désactivation des services inutiles",
        "monitoring": "Logs réseau, alertes sur comportements anormaux, inventaire des appareils"
     },
     "bonnes_pratiques": {
        "wifi": "WPA3 ou WPA2-AES minimum, SSID non révélateur, réseau invité séparé",
        "routeur": "Firmware à jour, interface admin sur port non-standard, accès admin désactivé depuis WAN",
        "dns": "DNS filtrant (Pi-hole, NextDNS) — bloque pub, tracking, domaines malveillants",
        "upnp": "Désactiver UPnP — ouvre des ports automatiquement, source de vulnérabilités",
        "inventaire": "Connaître chaque appareil sur le réseau — les inconnus sont des signaux d'alerte"
     },
     "alfred_hardware_context": "Réseau ALFRED : ER605 (routeur) + SG108E (switch manageable) — architecture permettant VLAN IoT et isolation PC ALFRED. Configuration recommandée : VLAN 10 (Pro/ALFRED), VLAN 20 (IoT), VLAN 30 (Invité)."},
    [{"prompt": "Par où commencer pour sécuriser mon réseau à la maison ?", "answer": "Priorités par ordre d'impact : 1) Mot de passe admin du routeur — changer dès maintenant (pas admin/admin). 2) WiFi — WPA3 ou WPA2-AES, mot de passe fort. 3) Désactiver UPnP. 4) Firmware routeur — vérifier et mettre à jour. 5) Réseau invité séparé pour les visiteurs et les appareils IoT. Ces cinq points éliminent 80% des vecteurs d'attaque courants sur un réseau domestique."},
     {"prompt": "Comment détecter si quelqu'un est sur mon réseau WiFi ?", "answer": "Depuis l'interface admin du routeur (souvent 192.168.1.1 ou 192.168.0.1) : liste des appareils connectés (DHCP leases). Comparer à l'inventaire de tes appareils connus. Tout appareil inconnu mérite investigation. Pour une détection continue : Fing (app mobile) ou un Raspberry Pi avec nmap ou Angry IP Scanner peuvent monitorer le réseau et alerter sur les nouveaux appareils."}],
    {"tone": "pratique, sécurité, contextualisé ALFRED", "structure": ["couches", "bonnes pratiques", "contexte ALFRED"], "avoid": ["expert pur", "négliger le contexte domestique"]},
    ["réseau local", "sécurité", "WiFi", "routeur", "VLAN", "firewall", "ALFRED"]
))

save("professional/iot/offline_first_home_automation.json", ku(
    "knowledges.professional.iot.offline_first_home_automation",
    "Domotique offline-first — contrôle local sans dépendance cloud",
    "professional", "iot", "high",
    "Approche domotique privilégiant le contrôle local sur le contrôle cloud : avantages (privacy, résilience, latence), solutions (Home Assistant, Matter, tinytuya) et limites.",
    "La domotique offline-first est une architecture dans laquelle les appareils connectés sont contrôlés localement sur le réseau domestique, sans dépendance aux serveurs cloud des fabricants, préservant la confidentialité, améliorant la résilience et réduisant la latence.",
    {"avantages": {
        "privacy": "Les données domotiques (présence, comportements) ne quittent pas la maison",
        "resilience": "Fonctionne même si le cloud du fabricant est coupé ou arrêté",
        "latence": "Commandes locales < 100ms vs cloud 200-500ms",
        "perenite": "Indépendant des décisions commerciales du fabricant"
     },
     "solutions": {
        "home_assistant": "Plateforme open-source, 3000+ intégrations, local-first par défaut",
        "matter": "Standard universel (Apple, Google, Amazon, Samsung) — local first by design, depuis 2022",
        "tinytuya": "Bibliothèque Python pour contrôler les appareils Tuya en local (sans cloud)",
        "zigbee_zwave": "Protocoles RF locaux — pas de cloud, pas de WiFi, très fiables"
     },
     "limites": {
        "setup": "Plus complexe que le plug-and-play cloud",
        "support_fabricant": "Certains appareils résistent au contrôle local",
        "mises_a_jour": "À gérer manuellement"
     },
     "alfred_context": "ALFRED B14 IoT cible tinytuya (Tuya local) + Home Assistant comme hub local, avec pattern Adapter pour abstraction des protocoles."},
    [{"prompt": "Pourquoi contrôler ma domotique en local plutôt que via le cloud ?", "answer": "Trois raisons principales : 1) Privacy — tes habitudes de vie (réveil, présence, luminosité préférée) ne sont pas dans les serveurs du fabricant. 2) Fiabilité — si le cloud Tuya ou Google est en panne, ta maison continue de fonctionner. 3) Longévité — si le fabricant arrête son service dans 3 ans, tes appareils restent utilisables. Le trade-off : la configuration initiale est plus complexe."},
     {"prompt": "Comment utiliser des appareils Tuya sans passer par l'app cloud ?", "answer": "Deux options : 1) tinytuya — bibliothèque Python qui permet le contrôle local en découvrant les appareils sur ton réseau. Nécessite de récupérer les clés locales via l'API Tuya Developer (gratuit). 2) Home Assistant avec l'intégration Tuya locale — interface visuelle, automatisations, pas de code. Les deux nécessitent que l'appareil soit sur le même réseau local et que le port UDP 6668 soit accessible."}],
    {"tone": "technique accessible, contextualisé ALFRED", "structure": ["avantages", "solutions", "limites", "Alfred context"], "avoid": ["ignorer la complexité", "trop vendeur d'une solution"]},
    ["domotique", "offline", "local", "Home Assistant", "Tuya", "Matter", "tinytuya", "ALFRED"]
))

save("professional/iot/presence_detection.json", ku(
    "knowledges.professional.iot.presence_detection",
    "Détection de présence — technologies et cas d'usage domotique",
    "professional", "iot", "medium",
    "Panorama des technologies de détection de présence pour la domotique (PIR, mmWave, WiFi sensing, BLE) avec leurs précisions, délais, coûts et cas d'usage adaptés.",
    "La détection de présence domotique désigne les technologies permettant de détecter l'occupation d'un espace par une personne, afin de déclencher des automatisations (éclairage, chauffage, sécurité) sans interaction manuelle.",
    {"technologies": {
        "pir": {
            "principe": "Capteur infrarouge passif — détecte le mouvement thermique",
            "avantages": "Économique (1-5€), simple, fiable pour le mouvement",
            "limites": "Ne détecte pas quelqu'un d'immobile, faux positifs (animaux)"
        },
        "mmwave": {
            "principe": "Radar millimétrique (24/60 GHz) — détecte respiration et micro-mouvements",
            "avantages": "Détecte la présence même immobile, très précis",
            "limites": "Plus cher (20-50€), peut détecter à travers les murs"
        },
        "wifi_sensing": {
            "principe": "Analyse des perturbations du signal WiFi par la présence humaine",
            "avantages": "Pas de matériel supplémentaire si routeur compatible",
            "limites": "Précision limitée, dépend du routeur"
        },
        "ble_tracking": {
            "principe": "Détection des appareils Bluetooth (smartphone, beacon)",
            "avantages": "Identification de la personne spécifique (quel membre du foyer)",
            "limites": "Nécessite que la personne porte l'appareil, vie privée"
        }
     },
     "cas_usage": {
        "eclairage": "PIR suffisant — mouvement détecte bien",
        "hvac": "mmWave recommandé — détecte la présence immobile",
        "securite": "Combinaison PIR + caméra",
        "occupancy_desk": "mmWave pour détecter si quelqu'un est assis au bureau"
     },
     "alfred_context": "ALFRED peut utiliser la détection de présence pour adapter son comportement (mode actif/veille, réponses proactives) selon la présence de Céline."},
    [{"prompt": "Quelle technologie de présence choisir pour allumer les lumières automatiquement ?", "answer": "Pour l'éclairage : PIR classique suffit et coûte peu (3-5€ pour un capteur Zigbee). Si tu veux garder la lumière allumée quand tu travailles immobile à ton bureau : mmWave (LD2410 à ~15€ est un excellent rapport qualité/prix). Combinaison optimale : mmWave en zone de travail, PIR dans les couloirs et entrées."},
     {"prompt": "Comment savoir qui est à la maison avec la domotique ?", "answer": "BLE tracking via smartphone : Home Assistant détecte la présence de chaque téléphone sur le réseau WiFi ou via Bluetooth. Plus fiable avec l'app Home Assistant Companion sur chaque smartphone du foyer. Limites : fonctionne si le téléphone est avec la personne et le Bluetooth activé. Pour une maison partagée, c'est la solution la plus précise sans infrastructure complexe."}],
    {"tone": "technique accessible, orienté choix pratique", "structure": ["technologies", "cas d'usage", "Alfred context"], "avoid": ["exhaustif sans guide de choix", "négliger le budget"]},
    ["présence", "détection", "PIR", "mmWave", "domotique", "IoT", "ALFRED"]
))

save("professional/iot/room_state_modeling.json", ku(
    "knowledges.professional.iot.room_state_modeling",
    "Modélisation d'état de pièce — représenter le contexte domotique",
    "professional", "iot", "medium",
    "Comment modéliser l'état d'une pièce (présence, luminosité, température, activité) pour déclencher des automatisations intelligentes et contextuelle.",
    "La modélisation d'état de pièce est la représentation structurée de l'état courant d'un espace (qui est là, ce qu'il fait, les conditions ambiantes) permettant à un système domotique ou à ALFRED de déclencher des actions contextuellement appropriées.",
    {"dimensions_etat": {
        "presence": "Occupée/vide, qui (si identification possible), depuis combien de temps",
        "activite": "Travail, repos, réunion, repas — déduit des capteurs ou déclaré",
        "ambiance": "Luminosité (lux), température, humidité, CO2",
        "mode": "Jour/nuit, absent/présent, focus/relax"
     },
     "sources_donnees": ["Capteurs de présence (PIR, mmWave)", "Calendrier (réunion planifiée = activité connue)", "Heure (proxy pour l'activité probable)", "Déclaration explicite (\"ALFRED, je travaille\")"],
     "representation": {
        "state_machine": "Machine à états finis — transitions entre états définis",
        "probabiliste": "Probabilité de chaque état selon les capteurs — plus robuste aux faux positifs",
        "json_alfred": "{\"room\": \"bureau\", \"presence\": true, \"activity\": \"work\", \"since\": \"14:30\", \"lighting\": \"focus\"}"
     },
     "alfred_context": "ALFRED peut maintenir un modèle d'état de l'environnement de Céline pour adapter ses réponses (ne pas distraire en mode focus, proposer une pause selon la durée de travail détectée)."},
    [{"prompt": "Comment ALFRED peut savoir ce que je fais pour adapter ses réponses ?", "answer": "Plusieurs sources combinées : capteurs de présence (tu es là ou pas), calendrier (tu as une réunion = pas de distraction), déclaration explicite (\"je travaille en mode focus\"), et patterns temporels (14h-18h = probabilité de travail élevée). ALFRED peut maintenir un état de contexte et adapter son niveau de proactivité — silencieux en focus, disponible en mode ouvert."},
     {"prompt": "C'est quoi une machine à états pour la domotique ?", "answer": "Un ensemble d'états possibles (Absent / Présent-Actif / Présent-Repos / Réunion) et des règles de transition entre eux selon les événements (détection mouvement → Actif, calendrier réunion → Réunion, pas de mouvement 30 min → Repos). C'est plus robuste qu'une simple condition because les états ont de la mémoire — un \"pas de mouvement\" ne change pas l'état immédiatement, il faut une durée seuil."}],
    {"tone": "technique, contextualisé ALFRED", "structure": ["dimensions", "sources", "représentation", "Alfred context"], "avoid": ["trop abstrait", "ignorer les sources de données pratiques"]},
    ["état", "pièce", "modélisation", "domotique", "contexte", "ALFRED", "IoT"]
))

save("professional/iot/smart_alert_prioritization.json", ku(
    "knowledges.professional.iot.smart_alert_prioritization",
    "Priorisation intelligente des alertes IoT — réduire le bruit d'alertes",
    "professional", "iot", "medium",
    "Stratégies pour filtrer, prioriser et présenter les alertes domotiques de manière à maximiser la valeur de l'information sans créer de fatigue d'alerte.",
    "La priorisation des alertes IoT est le processus de filtrage et de classification des événements générés par les appareils connectés selon leur urgence, leur pertinence contextuelle et leur impact, afin de ne présenter à l'utilisateur que les alertes qui méritent son attention.",
    {"probleme_alert_fatigue": "Un système qui génère trop d'alertes pousse l'utilisateur à les ignorer toutes — y compris les critiques",
     "criteres_priorisation": {
        "urgence": "Menace immédiate (incendie, intrusion) > dégradation lente (température haute)",
        "impact": "Sécurité > confort > information",
        "contexte": "Alerte différente si à la maison vs absent vs nuit",
        "frequence": "Première occurrence > répétition du même événement"
     },
     "patterns": {
        "debouncing": "Ne pas alerter sur la même condition pendant X minutes après la première alerte",
        "correlation": "Regrouper les alertes liées (3 fenêtres ouvertes = 1 alerte, pas 3)",
        "hysteresis": "La condition doit durer un seuil de temps avant d'alerter — évite les faux positifs",
        "escalade": "Alerte non acquittée → escalade au canal suivant (push → SMS → appel)"
     },
     "alfred_context": "ALFRED filtre les alertes IoT selon le contexte de Céline : en mode focus, seules les alertes critiques passent. En mode disponible, toutes les alertes sont visibles."},
    [{"prompt": "Mon système domotique m'envoie trop de notifications et je les ignore toutes.", "answer": "C'est de la fatigue d'alerte — un problème de signal/bruit. Solution : 1) Classer tes alertes par catégorie (sécurité, confort, info). 2) Désactiver toutes les alertes \"info\" sur mobile — les rendre visibles uniquement sur tableau de bord. 3) Ajouter un délai de debounce (ex : mouvement détecté pendant 30 secondes avant alerte). 4) Une alerte par événement, pas une par capteur impliqué."},
     {"prompt": "Comment alerter seulement quand c'est vraiment important ?", "answer": "Définir explicitement ce qui est critique (incendie, intrusion, dégâts des eaux) et le configurer sur tous les canaux (push, SMS). Tout le reste : visible sur tableau de bord uniquement, avec une revue hebdomadaire si besoin. La règle : si l'alerte n'exige pas d'action dans l'heure, elle ne devrait pas couper le fil de ta journée."}],
    {"tone": "pratique, orienté expérience utilisateur", "structure": ["problème", "critères", "patterns", "ALFRED"], "avoid": ["technique pure", "ignorer l'aspect humain de la fatigue d'alerte"]},
    ["alertes", "IoT", "priorisation", "fatigue alerte", "domotique", "notification", "ALFRED"]
))

save("professional/iot/smart_home_basics.json", ku(
    "knowledges.professional.iot.smart_home_basics",
    "Domotique — fondamentaux et écosystèmes",
    "professional", "iot", "medium",
    "Introduction aux concepts fondamentaux de la domotique : protocoles, écosystèmes, architecture et points d'entrée pour un déploiement progressif.",
    "La domotique (smart home) désigne l'ensemble des technologies permettant d'automatiser et de contrôler les équipements d'un logement (éclairage, chauffage, sécurité, électroménager) via des protocoles de communication et des interfaces unifiées.",
    {"protocoles": {
        "wifi": "Universel, simple, consomme plus d'énergie, dépendant du router",
        "zigbee": "Mesh, faible consommation, local, nécessite un hub (Philips Hue Bridge, Conbee, Sonoff Zigbee)",
        "zwave": "Similaire à Zigbee, fréquences différentes, très fiable",
        "matter": "Standard universel 2022 — WiFi + Thread, local first, interopérable",
        "bluetooth_ble": "Courte portée, pour capteurs et présence"
     },
     "ecosystemes": {
        "google_home": "Voix (Google Assistant), large compatibilité, cloud-dependent",
        "apple_homekit": "Très sécurisé, local-first, écosystème Apple uniquement",
        "amazon_alexa": "Large compatibilité, cloud-dependent, moins privacy-friendly",
        "home_assistant": "Open source, local-first, 3000+ intégrations, courbe d'apprentissage"
     },
     "architecture_recommandee": "Hub local (Home Assistant sur Raspberry Pi ou NAS) + appareils Zigbee/Matter pour le contrôle local, avec intégration Google Home/Apple HomeKit pour la voix",
     "entree_progressive": ["1. Commencer par l'éclairage connecté (Zigbee)", "2. Ajouter des prises connectées pour l'énergie", "3. Capteurs (température, présence)", "4. Hub centralisé (Home Assistant)", "5. Automatisations complexes"]},
    [{"prompt": "Par où commencer en domotique sans se ruiner ni se perdre ?", "answer": "Entrée douce recommandée : quelques ampoules Zigbee (Ikea TRÅDFRI, Sengled) avec un hub Zigbee USB (Sonoff Zigbee Dongle Plus à ~20€). Zigbee = local, fiable, économique. Une fois que tu maîtrises l'éclairage, ajouter Home Assistant (Raspberry Pi ou VM) pour centraliser. Ne pas commencer par Matter — encore en maturation. Ne pas commencer par un écosystème propriétaire fermé."},
     {"prompt": "Quelle différence entre Zigbee et WiFi pour la domotique ?", "answer": "Zigbee : fréquence dédiée (2.4 GHz), réseau mesh (les appareils se relaient), très basse consommation (piles durables), nécessite un hub, local par défaut. WiFi : chaque appareil se connecte directement à la box, pas de hub supplémentaire, mais consomme plus, ajoute de la charge sur le routeur, et dépend souvent du cloud fabricant. Pour une installation sérieuse : Zigbee ou Matter. Pour quelques appareils simples : WiFi acceptable."}],
    {"tone": "introductif, progressif, neutre sur les écosystèmes", "structure": ["protocoles", "écosystèmes", "architecture", "entrée progressive"], "avoid": ["trop avancé", "parti pris pour un écosystème"]},
    ["domotique", "smart home", "Zigbee", "Matter", "Home Assistant", "protocoles", "IoT"]
))

# ═══════════════════════════════════════════════════════
# PROFESSIONAL / PRODUCT_MANAGEMENT / ADVANCED (4 KU)
# ═══════════════════════════════════════════════════════

save("professional/product_management/advanced/product_governance.json", ku(
    "knowledges.professional.product_management.advanced.product_governance",
    "Gouvernance produit — structure de décision et accountability",
    "professional", "product_management_advanced", "high",
    "Comment structurer la prise de décision sur un produit : rôles, forums, processus d'arbitrage et mécanismes de redevabilité pour les produits complexes ou multi-équipes.",
    "La gouvernance produit est le système de règles, rôles et processus qui définissent comment les décisions relatives au produit sont prises, par qui, avec quelle fréquence et comment elles sont communiquées — garantissant cohérence, vitesse et accountability.",
    {"modeles": {
        "centralisee": "Un CPO ou PM lead décide — simple, rapide, risque de goulet d'étranglement",
        "federee": "Chaque équipe produit est autonome dans son domaine — nécessite coordination forte",
        "comite": "Décisions collectives — inclusive mais lente, risque de consensus mou"
     },
     "forums_cles": {
        "product_review": "Revue hebdomadaire ou bi-mensuelle des décisions tactiques (priorités sprint, scope)",
        "roadmap_planning": "Trimestrielle — alignement stratégique, arbitrages entre équipes",
        "architecture_board": "Décisions structurantes sur l'architecture technique et produit"
     },
     "responsabilites": {
        "qui_decide": "RACI clair : Responsable (fait), Approuve (valide), Consulté, Informé",
        "escalade": "Processus clair pour les décisions non résolues en équipe",
        "documentation": "Les décisions structurantes sont documentées avec le contexte et le raisonnement"
     },
     "signaux_gouvernance_dysfonctionnelle": ["Décisions qui reviennent sans cesse", "Flou sur qui a dit oui à quoi", "Roadmap changeant à chaque réunion avec les stakeholders"]},
    [{"prompt": "Comment savoir qui décide quoi sur notre produit ?", "answer": "RACI par type de décision : qui est Responsable (fait le travail), qui Approuve (peut dire non), qui est Consulté (doit être entendu), qui est Informé (doit savoir après). Le documenter pour les décisions fréquentes : priorités backlog, scope de sprint, changements d'architecture, communication client. Le flou sur \"qui a dit oui\" est souvent la source de dettes de décision qui reviennent en réunion."},
     {"prompt": "Notre roadmap change tout le temps selon les réunions. Comment stabiliser ?", "answer": "Symptôme de gouvernance manquante : tout le monde peut influencer la roadmap en réunion. Solution : définir un forum de roadmap (ex : revue trimestrielle) où les décisions sont prises, et une règle de changement (toute modification de roadmap validée nécessite une demande formelle et un arbitrage). Hors de ce forum, la réponse aux demandes ad hoc est : \"ça passe en revue trimestrielle\". La discipline est inconfortable au début — indispensable à l'échelle."}],
    {"tone": "management produit, orienté clarté organisationnelle", "structure": ["modèles", "forums", "responsabilités", "signaux"], "avoid": ["trop corporate", "ignorer les petites équipes"]},
    ["gouvernance produit", "décision", "RACI", "roadmap", "product management", "accountability"]
))

save("professional/product_management/advanced/product_health_monitoring.json", ku(
    "knowledges.professional.product_management.advanced.product_health_monitoring",
    "Santé produit — monitorer la vitalité d'un produit en production",
    "professional", "product_management_advanced", "high",
    "Framework pour surveiller la santé globale d'un produit en production : métriques d'usage, technique, satisfaction et économiques — et comment agir sur les signaux faibles.",
    "Le monitoring de santé produit est le système de métriques et d'alertes permettant de détecter précocement les dégradations de valeur, de performance ou de satisfaction d'un produit, afin d'intervenir avant qu'elles se traduisent par du churn ou des incidents.",
    {"dimensions": {
        "usage": "DAU/MAU, rétention J1/J7/J30, feature adoption rate, depth of usage",
        "technique": "Taux d'erreur, latence P95, disponibilité (uptime), dette technique",
        "satisfaction": "NPS, CSAT, tickets support (volume et nature), avis app stores",
        "economique": "MRR, churn rate, LTV, CAC, expansion revenue"
     },
     "signaux_alarme": {
        "leading": "Baisse d'engagement avant le churn (signaux précoces à surveiller)",
        "lagging": "Churn confirmé (trop tard pour agir sur ces clients)",
        "correlation": "Augmentation tickets support corrèle souvent avec une feature récente"
     },
     "tableau_de_bord": {
        "frequence": "Daily pour les métriques opérationnelles, weekly pour les métriques produit, monthly pour les économiques",
        "audience": "Équipe produit voit tout, management voit les résumés, board voit les économiques"
     },
     "acting_on_signals": "Un signal n'est pas une décision — investiguer la cause avant d'agir. La rétention J1 baisse : bug ? friction onboarding ? qualité utilisateurs acquis ?"},
    [{"prompt": "Quelles métriques pour savoir si mon produit est en bonne santé ?", "answer": "Minimum viable dashboard : 1) Engagement — DAU/MAU ratio (> 20% = bon signe). 2) Rétention — J7 et J30 (benchmarks varient par catégorie). 3) NPS ou CSAT — satisfaction perçue. 4) Taux d'erreur et latence — santé technique. 5) Churn MRR si SaaS. Ces cinq métriques donnent une vue 360. Les surveiller ensemble évite les angles morts (bon NPS mais churn technique élevé = problème à venir)."},
     {"prompt": "Notre NPS est bon mais le churn augmente. Contradiction ?", "answer": "Pas forcément. Le NPS mesure l'intention de recommander — pas l'intention de rester. Un client peut être satisfait mais partir si un concurrent offre plus de valeur pour le même prix, ou si son contexte change. Investiguer le churn directement : exit surveys, appels clients churned, analyse des patterns d'usage avant le départ. Les raisons de churn sont souvent différentes des raisons de satisfaction."}],
    {"tone": "analytique, orienté action", "structure": ["dimensions", "signaux", "dashboard", "acting"], "avoid": ["liste de métriques sans hiérarchie", "ignorer la dimension investigation"]},
    ["santé produit", "métriques", "monitoring", "churn", "NPS", "rétention", "product management"]
))

save("professional/product_management/advanced/product_kpi_frameworks.json", ku(
    "knowledges.professional.product_management.advanced.product_kpi_frameworks",
    "Frameworks KPI produit — HEART, NSM, AARRR et comment choisir",
    "professional", "product_management_advanced", "high",
    "Tour des principaux frameworks de KPI pour les produits digitaux (HEART de Google, North Star Metric, AARRR de Dave McClure) avec leurs forces, limites et critères de choix.",
    "Les frameworks KPI produit sont des structures d'organisation des métriques qui permettent de traduire les objectifs stratégiques d'un produit en indicateurs mesurables cohérents et hiérarchisés.",
    {"heart_google": {
        "description": "Happiness, Engagement, Adoption, Retention, Task success",
        "usage": "Évaluation UX et satisfaction — adapté aux produits à fort composant expérience",
        "limite": "Peu de lien avec les métriques économiques"
     },
     "north_star_metric": {
        "description": "Une seule métrique qui capture la valeur créée pour le client et le business",
        "exemples": {"spotify": "Temps d'écoute", "airbnb": "Nuits réservées", "slack": "Messages envoyés"},
        "usage": "Aligner toute l'organisation sur une direction",
        "limite": "Difficile à trouver, peut être manipulée si mal définie"
     },
     "aarrr": {
        "description": "Acquisition, Activation, Retention, Revenue, Referral (Pirate Metrics, Dave McClure)",
        "usage": "Startups et growth — identifier le maillon faible du funnel",
        "limite": "Linéaire — mal adapté aux produits non-funnel"
     },
     "comment_choisir": {
        "produit_early_stage": "AARRR — identifier le bottleneck du funnel",
        "produit_mature": "NSM + métriques de support par équipe",
        "ux_focus": "HEART — pour les revues UX et les décisions design"
     }},
    [{"prompt": "C'est quoi la North Star Metric et comment en définir une ?", "answer": "La NSM est la métrique qui capture le mieux la valeur que ton produit crée pour ses utilisateurs — et qui corrèle avec ta croissance. Critères d'une bonne NSM : 1) Elle mesure de la valeur réelle pour le client (pas juste du revenu). 2) Toutes les équipes peuvent l'influencer. 3) Sa croissance prédit la croissance du business. Pour la trouver : \"Quel est le moment où notre utilisateur réalise vraiment la valeur de notre produit ?\" — mesurer ça."},
     {"prompt": "AARRR ou HEART pour mon produit B2B SaaS ?", "answer": "Pour un SaaS B2B : commencer par AARRR pour identifier ton bottleneck de croissance. Si tu as un problème d'activation (les utilisateurs signent mais n'utilisent pas), passer à HEART pour investiguer l'expérience en détail. Les deux sont complémentaires — AARRR dit où est le problème, HEART aide à le diagnostiquer. La NSM en parallèle pour garder l'équipe alignée sur la valeur créée."}],
    {"tone": "analytique, orienté choix pratique", "structure": ["frameworks", "comment choisir", "comparaison"], "avoid": ["présenter comme mutuellement exclusifs", "ignorer le contexte d'usage"]},
    ["KPI", "métriques", "HEART", "North Star", "AARRR", "framework", "product management"]
))

save("professional/product_management/advanced/product_scaling_strategy.json", ku(
    "knowledges.professional.product_management.advanced.product_scaling_strategy",
    "Stratégie de scaling produit — passer de 0 à 1 puis de 1 à N",
    "professional", "product_management_advanced", "high",
    "Comment faire évoluer la stratégie produit selon la phase de maturité : exploration (0→1), croissance (1→10), scale (10→100) — avec les changements d'organisation, de process et de métriques associés.",
    "La stratégie de scaling produit est l'adaptation continue de l'organisation, des processus et de la stratégie produit aux différentes phases de maturité d'un produit, en reconnaissant que ce qui fonctionne pour valider un MVP ne fonctionne pas pour scaler à des millions d'utilisateurs.",
    {"phases": {
        "zero_a_un": {
            "objectif": "Trouver le product-market fit",
            "metriques": "Rétention et satisfaction d'un petit groupe de clients cibles",
            "organisation": "Petite équipe polyvalente, peu de process",
            "danger": "Scaler trop tôt avant PMF — gaspillage massif"
        },
        "un_a_dix": {
            "objectif": "Répliquer et accélérer ce qui marche",
            "metriques": "CAC, LTV, churn, NPS",
            "organisation": "Équipes fonctionnelles qui se forment, process légers",
            "danger": "Ne pas formaliser assez — perte de qualité à la croissance"
        },
        "dix_a_cent": {
            "objectif": "Efficience, plateformes, gouvernance",
            "metriques": "Unit economics, margin, market share",
            "organisation": "Squads autonomes, plateformes partagées, OKR",
            "danger": "Sur-process qui ralentit l'innovation"
        }
     },
     "signaux_changement_de_phase": ["PMF atteint quand > 40% des utilisateurs seraient très déçus sans le produit (Sean Ellis test)", "Prêt à scaler quand le CAC < LTV / 3 et la rétention est stable"],
     "anti_patterns": {
        "premature_scaling": "Embaucher et investir avant PMF — startup killer #1 selon CB Insights",
        "process_overload": "Introduire des process d'entreprise à une phase startup",
        "feature_factory": "Ajouter des features sans mesurer l'impact sur les métriques clés"
     }},
    [{"prompt": "On a trouvé notre product-market fit. Comment scaler maintenant ?", "answer": "Avant d'accélérer, vérifier les unit economics : CAC < LTV/3 ? Churn < 5% mensuel (SaaS) ? Rétention stable à J30 ? Si oui, identifier ton levier de croissance prioritaire (acquisition ? activation ? expansion ?) et concentrer les ressources là-dessus — pas sur les features. Le scaling nécessite aussi de commencer à formaliser : documentation, processus de décision, onboarding équipe. Trop tôt pour le process, trop tard c'est le chaos."},
     {"prompt": "Comment savoir si on a le product-market fit ?", "answer": "Sean Ellis test : envoyer à tes utilisateurs actifs la question \"Comment te sentirais-tu si tu ne pouvais plus utiliser [produit] ?\" — options : Très déçu / Déçu / Pas déçu. Si > 40% répondent \"Très déçu\", tu as probablement le PMF. Autres signaux : les clients reviennent sans qu'on les relance, le bouche à oreille génère des leads, le churn est bas et stable."}],
    {"tone": "stratégique, orienté phase de maturité", "structure": ["phases", "signaux", "anti-patterns"], "avoid": ["recette universelle", "ignorer le contexte de chaque phase"]},
    ["scaling", "product-market fit", "croissance", "stratégie", "product management", "PMF", "phase"]
))

print("\n=== governance_ai : 6 KU ===")
print("=== iot : 8 KU ===")
print("=== product_management/advanced : 4 KU ===")
print("=== TOTAL : 18 KU sauvegardés ===")
