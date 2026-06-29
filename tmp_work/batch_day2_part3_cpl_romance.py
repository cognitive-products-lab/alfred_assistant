"""
Batch Day 2 — Part 3
  cpl/usage_professionnel/ : 12 fichiers
  culture/romance/         :  8 fichiers (Jay Crownover + genre)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(file_id, domain, subdomain, title, summary, core_def, knowledge, examples, tags, priority="high"):
    return {
        "schema_version": "1.2", "type": "knowledge_unit",
        "id": f"knowledges.{domain}.{subdomain}.{file_id}",
        "title": title, "domain": domain, "subdomain": subdomain,
        "status": "validated", "priority": priority,
        "summary": summary, "core_definition": core_def,
        "knowledge": knowledge, "example_answers": examples,
        "response_guidance": {
            "tone": "professionnel, précis, orienté action",
            "structure": ["contextualiser", "appliquer", "recommander"],
            "avoid": ["jargon excessif", "généralités non actionnables"]
        },
        "tags": tags, "related_knowledge_units": []
    }

# ═══════════════════════════════════════════════════════════════════════════
# CPL / USAGE_PROFESSIONNEL  (12 fichiers)
# ═══════════════════════════════════════════════════════════════════════════

def kucpl(file_id, title, summary, core_def, knowledge, examples, tags, priority="high"):
    return ku(file_id, "cpl", "usage_professionnel", title, summary, core_def, knowledge, examples, tags, priority)

save("cpl/usage_professionnel/brief_client.json", kucpl(
    "brief_client",
    "Brief client — structurer et valider les besoins CPL",
    "Un brief client bien conduit est la différence entre un projet qui aboutit et six mois de travail qui ne correspond pas à l'attendu. La méthode ALFRED appliquée au brief CPL : écoute active, reformulation validée, scope défini par écrit.",
    "Le brief client dans le contexte CPL (Cognitive Products Lab) est le processus par lequel Céline et l'équipe CPL recueillent, structurent et valident les besoins d'un client ou d'une partie prenante avant de lancer un projet IA/technologique. Il débouche sur un document de scope validé qui sert de référence tout au long du projet.",
    {
        "brief_structure_CPL": {
            "contexte": "Quel est le contexte business ? Quelle situation a généré ce besoin ?",
            "problème_central": "Qu'est-ce qui ne fonctionne pas ou pourrait mieux fonctionner ?",
            "objectif_measurable": "Comment saurons-nous que c'est réussi ? (KPI, métrique, résultat attendu)",
            "contraintes": "Budget, délai, ressources techniques disponibles, contraintes légales (RGPD, données sensibles)",
            "parties_prenantes": "Qui décide ? Qui utilise ? Qui valide ? Qui peut bloquer ?",
            "hors_périmètre": "Qu'est-ce qu'on ne fera PAS dans ce projet ?"
        },
        "interview_techniques": [
            "Questions ouvertes d'abord — 'Parlez-moi de votre situation actuelle'",
            "5 Pourquoi — creuser jusqu'à la cause racine du besoin (pas juste le symptôme)",
            "Reformulation en fin d'entretien — 'Ce que j'ai compris, c'est que...' → correction par le client",
            "Tester les hypothèses — 'Si on faisait X, ça résoudrait votre problème ?'"
        ],
        "CPL_specificites": [
            "Toujours valider la dimension éthique et RGPD dès le brief pour les projets IA",
            "Distinguer le besoin fonctionnel (ce qu'il veut) du besoin métier (pourquoi il en a besoin)",
            "Documenter par écrit même pour les 'petits' projets — protège les deux parties",
            "Inclure le critère d'acceptation : comment le client décide-t-il si c'est livré ?"
        ]
    },
    [
        {"prompt": "Comment préparer et conduire un brief client pour un projet IA/data chez CPL ?",
         "answer": "Processus en 4 temps : (1) Prépré-brief — rechercher le contexte client (site, LinkedIn, actualités secteur). Arriver avec des hypothèses à valider, pas une page blanche, (2) L'entretien — commencer large ('parlez-moi de votre situation'), aller vers le précis ('qu'est-ce qui se passerait si on ne fait rien ?'). Utiliser les 5 Pourquoi pour atteindre le vrai besoin sous le besoin exprimé, (3) Reformulation finale — 'Voilà ce que j'ai compris. Correction ou validation ?' Cruciale pour aligner, (4) Document de brief — 1 page max. Contexte, problème, objectif, contraintes, hors-périmètre, critères d'acceptation. Envoyé dans les 48h et validé par écrit (email suffit). La règle CPL : pas de brief validé = pas de démarrage. Ça protège le client et l'équipe."},
        {"prompt": "ALFRED, aide-moi à préparer les questions pour un brief client sur un projet de chatbot IA",
         "answer": "Questions structurées par thème : **Contexte** : 'Quel processus ce chatbot va-t-il remplacer ou augmenter ?' / 'Combien d'échanges par jour/mois traitez-vous actuellement ?' **Besoin** : 'Quel est le cas d'usage principal ? (FAQ, qualification de leads, support interne ?)' / 'Quelles sont les 5 questions les plus fréquentes que vous recevez ?' **Données** : 'Quelles données sont disponibles pour entraîner ou alimenter le chatbot ?' / 'Avez-vous des contraintes RGPD sur les données des utilisateurs ?' **Succès** : 'Comment saurez-vous dans 3 mois que le projet a réussi ?' / 'Quel pourcentage de requêtes le chatbot doit-il traiter sans escalade humaine ?' **Contraintes** : 'Quel est le budget indicatif ?' / 'Quel est le délai souhaité ?' / 'Quelle stack technique existante doit-on intégrer ?'"}
    ],
    ["brief client", "CPL", "projet IA", "scope", "besoins", "méthode"]
))

save("cpl/usage_professionnel/pitch_client.json", kucpl(
    "pitch_client",
    "Pitch client CPL — présenter une proposition IA efficacement",
    "Le pitch d'une solution IA à un client non-technique est un exercice de traduction : transformer la complexité technique en valeur business lisible. La règle : zéro jargon, 100% orienté résultat.",
    "Un pitch client CPL est la présentation d'une proposition de valeur technologique (IA, data, automatisation) à un décideur ou une équipe cliente. Il vise à créer de l'adhésion et à déclencher une décision en combinant compréhension du problème client, solution proposée et preuve de valeur.",
    {
        "pitch_structure": {
            "hook": "Commencer par le problème du client, pas par CPL ou la solution. 'Aujourd'hui vous perdez X heures par semaine à...'",
            "problem_reframe": "Reformuler le problème en termes d'impact business. 'Ça représente X€ par an / X% de productivité perdu'",
            "solution_simple": "La solution en 2-3 phrases max, sans jargon technique. 'On automatise X avec IA, ce qui vous libère Y'",
            "proof": "Proof point : cas client similaire, prototype, démo, données. 'Chez [client similaire], résultat en Z semaines'",
            "ROI": "Impact quantifié si possible. Économie de temps, réduction de coût, augmentation de revenus",
            "next_step": "Toujours finir sur une action concrète. 'On peut faire un POC en 2 semaines — est-ce qu'on prévoit ça ?'"
        },
        "non_technical_client_rules": [
            "Jamais d'acronymes non expliqués (LLM, RAG, NLP) sans traduction immédiate",
            "Métaphores > spécifications — 'c'est comme un assistant qui a lu tous vos documents et peut répondre à vos questions'",
            "Démo > description — montrer 5 min > expliquer 20 min",
            "Anticiper la question 'et si ça marche pas ?' — avoir une réponse sur la gestion du risque"
        ],
        "CPL_differentiators": [
            "Approche éthique by design — RGPD, transparence IA documentée",
            "Architecture locale-first si données sensibles",
            "Accompagnement humain (Céline directement sur les projets stratégiques)",
            "Expertise spécifique : IA conversationnelle, knowledge management, personnalisation"
        ]
    },
    [
        {"prompt": "Comment pitcher un projet IA à un directeur qui ne comprend pas la technique ?",
         "answer": "Structure de 5 minutes : (1) 30 sec — son problème, dans ses mots. Prouve que tu l'as compris, (2) 1 min — impact business actuel du problème. Chiffré si possible, (3) 2 min — la solution, en une métaphore simple + démo courte ou screenshot. 'On crée un assistant qui...', (4) 1 min — proof : cas similaire ou prototype fonctionnel. Rien de plus convaincant qu'une démo de 2 minutes, (5) 30 sec — ROI approximatif + proposition de prochaine étape précise. La règle d'or : si tu ne peux pas expliquer la solution en une phrase sans acronyme, tu n'as pas encore trouvé la bonne formulation pour ce client."},
        {"prompt": "ALFRED, aide-moi à rédiger un pitch d'une page pour proposer ALFRED comme assistant IA à une PME",
         "answer": "Proposition de structure : **[Titre]** : 'Un assistant IA qui connaît votre entreprise aussi bien que vous' **[Problème]** : Vos équipes passent des heures à chercher des informations, rédiger des contenus répétitifs, ou onboarder de nouveaux collaborateurs. Ce temps gagné n'est pas investi dans ce qui crée vraiment de la valeur. **[Solution]** : ALFRED est un assistant IA conversationnel formé sur vos propres données — documents, process, FAQ interne. Il répond en quelques secondes aux questions de vos équipes, rédige des premières versions de documents, et s'améliore avec votre usage. **[Pourquoi maintenant]** : Les assistants IA génériques (ChatGPT) ne connaissent pas votre contexte. ALFRED, lui, est construit sur votre base de connaissance. **[CPL différence]** : Architecture locale disponible si données sensibles. RGPD by design. Accompagnement de A à Z par des experts IA français. **[Prochaine étape]** : POC en 4 semaines. Contact : [Céline]."}
    ],
    ["pitch client", "CPL", "IA", "non-technique", "business", "proposition valeur"]
))

save("cpl/usage_professionnel/gestion_projet_ia.json", kucpl(
    "gestion_projet_ia",
    "Gestion de projet IA chez CPL — méthodologie agile adaptée",
    "Les projets IA ont des incertitudes supplémentaires par rapport aux projets logiciels classiques — les données peuvent être insuffisantes, les modèles peuvent ne pas performer comme attendu, les KPI peuvent évoluer. La méthode CPL adapte l'agilité à ces incertitudes spécifiques.",
    "La gestion de projet IA chez CPL est une méthodologie hybride qui combine les principes agiles (itérations courtes, feedback client fréquent) avec les spécificités des projets IA : phase d'exploration des données, POC rapide avant engagement full, et ajustement continu des critères de succès.",
    {
        "CPL_IA_project_phases": [
            {
                "phase": "0. Brief et exploration (1-2 semaines)",
                "activities": ["Brief client (voir brief_client)", "Audit des données disponibles", "Définition des KPI de succès", "Évaluation de la faisabilité IA vs solution classique"]
            },
            {
                "phase": "1. POC (Proof of Concept) (2-4 semaines)",
                "activities": ["Prototype fonctionnel minimal", "Test sur données réelles limitées", "Démo client", "Go/No-go basé sur performance et coût"],
                "CPL_rule": "Pas d'engagement plein avant POC validé. Réduit le risque client."
            },
            {
                "phase": "2. MVP et itérations (4-12 semaines)",
                "activities": ["Version minimale utilisable", "Itérations bihebdomadaires", "Feedback utilisateurs réels", "Ajustement modèle/données"]
            },
            {
                "phase": "3. Déploiement et suivi",
                "activities": ["Déploiement progressif", "Documentation utilisateur", "Formation", "Suivi des KPI à 30/60/90 jours"]
            }
        ],
        "IA_specific_risks": [
            {"risk": "Données insuffisantes ou de mauvaise qualité", "mitigation": "Audit données en phase 0 — ne pas partir sans données réelles"},
            {"risk": "Dérive du modèle (model drift)", "mitigation": "Monitoring en production avec alertes sur les métriques clés"},
            {"risk": "Adoption utilisateur faible", "mitigation": "Formation, change management, inclusion utilisateurs dès la phase POC"},
            {"risk": "Coût token/compute sous-estimé", "mitigation": "Estimation coût d'usage dès le POC avec usage réel simulé"}
        ]
    },
    [
        {"prompt": "Comment planifier un projet IA de A à Z chez CPL ?",
         "answer": "4 phases chronologiques : (1) Brief + exploration (1-2 sem) : comprendre le besoin, auditer les données, définir les KPI de succès. Livrable : document de scope validé, (2) POC (2-4 sem) : prototype minimal sur cas réels. Démo client. Décision Go/No-go. La règle CPL : on ne s'engage pas sur le projet complet avant que le POC prouve la faisabilité, (3) MVP + itérations (4-12 sem) : cycles de 2 semaines. Feedback réel. Ajustement. Test utilisateurs impliqués depuis le début, (4) Déploiement + suivi (continu) : monitoring des KPI à 30/60/90 jours. Documentation. Formation. Le plus important : inclure les utilisateurs finaux dès le POC — les projets IA qui échouent ratent presque toujours sur l'adoption, pas sur la technique."},
        {"prompt": "ALFRED, rappelle-moi les jalons pour le suivi de projet IA à communiquer au client",
         "answer": "Jalons types d'un projet CPL : **Semaine 1-2** : Kick-off + audit données + scope validé. Livrable : document de scope signé. **Semaine 3-6** : POC fonctionnel. Livrable : démo sur données réelles + rapport de faisabilité. **Semaine 8** : MVP v0.1 — première version utilisable. **Toutes les 2 semaines** : Demo interne + rapport d'avancement. KPI : performance du modèle, couverture des cas d'usage. **Mois 3** : Livraison complète + documentation + formation. **Mois 3+1, 3+2, 3+3** : Rapports de suivi post-déploiement avec métriques d'usage et de performance. Proposition de jalons à adapter selon la taille et la complexité du projet — un POC 2 semaines n'a pas les mêmes jalons qu'un projet 6 mois."}
    ],
    ["gestion projet", "CPL", "IA", "agile", "POC", "méthodologie"]
))

save("cpl/usage_professionnel/veille_strategique.json", kucpl(
    "veille_strategique",
    "Veille stratégique IA — rester à la pointe pour CPL",
    "Le secteur de l'IA évolue toutes les 2-3 semaines avec de nouvelles sorties de modèles, de frameworks et de cas d'usage. Une veille structurée permet à CPL de maintenir son avantage concurrentiel sans se noyer dans le flux d'information.",
    "La veille stratégique en IA est le processus systématique de collecte, filtrage et analyse des informations sur les avancées technologiques, les nouvelles pratiques et l'évolution du marché dans le domaine de l'intelligence artificielle, au service de la stratégie et des offres de CPL.",
    {
        "signal_sources": {
            "recherche": ["ArXiv (papers IA)", "Papers With Code (benchmarks)", "Google DeepMind blog", "Anthropic blog", "OpenAI blog", "Hugging Face updates"],
            "pratique": ["Hacker News (tech community)", "Twitter/X (chercheurs IA : Yann LeCun, Andrej Karpathy, Sebastian Raschka)", "LessWrong (IA safety, mais aussi technique)", "AI newsletter : The Neuron, TLDR AI, Import AI"],
            "business": ["TechCrunch IA", "VentureBeat AI", "MIT Technology Review", "McKinsey / Gartner IA reports"],
            "francophone": ["EurAI", "Alliance pour l'IA (France)", "Inria blog", "Silicon.fr section IA"]
        },
        "filtrage_CPL": {
            "priority_1": "Tout ce qui touche à : LLM locaux (Ollama, LM Studio, llama.cpp), RAG/knowledge management, frameworks agents (LangChain, LlamaIndex, AutoGen), IA conversationnelle",
            "priority_2": "Nouvelles réglementations IA (EU AI Act, RGPD évolutions), marchés clients CPL (PME, startups, institutions)",
            "ignore": "IA générative d'image/vidéo (hors de l'offre CPL actuelle), jeux, robotique (sauf si nouveau client)"
        },
        "ritual_CPL": "Veille quotidienne 15 min (Hacker News + Twitter watch). Synthèse hebdomadaire 30 min. Newsletter mensuelle ou note interne sur les implications pour les offres CPL."
    },
    [
        {"prompt": "Comment faire une veille IA efficace sans y passer 3 heures par jour ?",
         "answer": "Système à 3 niveaux pour 20 min/jour : (1) Alertes passives — Google Alerts sur 'LLM local', 'RAG', 'EU AI Act', 'IA assistants'. Arrivent par email, tu parcours en 5 min, (2) Curé (10 min/jour) — Hacker News IA section + 3-4 comptes Twitter/X de chercheurs ou praticiens IA. Liste fermée, pas infinite scroll, (3) Approfondissement hebdo (1h/semaine) — un paper, un article long, un podcast sur un sujet qui a émergé dans la semaine. Tools : Feedly ou Inoreader pour agréger les RSS des blogs techniques. Newsletter 'The Neuron' ou 'TLDR AI' pour le digest quotidien en 3 min. L'objectif n'est pas de tout lire — c'est d'avoir un signal assez tôt pour adapter les offres CPL avant que la concurrence ne l'ait fait."},
        {"prompt": "ALFRED, quels sont les sujets IA les plus importants à surveiller pour CPL en 2026 ?",
         "answer": "Priorités selon la stratégie CPL (offre IA locale / knowledge management / assistants) : **Immédiat** : (1) Modèles locaux — Llama 4, Mistral, Qwen 2.5 et successeurs. Chaque nouvelle génération change le rapport performance/coût local, ce qui détermine ce qu'on peut proposer aux PME, (2) Agent frameworks — LangGraph, LlamaIndex Workflows, Microsoft Autogen. Les architectures agentiques évoluent vite, (3) EU AI Act — applicabilité progressive 2025-2027. Implications pour les clients CPL et la conformité des projets. **Moyen terme** : (4) Voice AI (local) — opportunité pour ALFRED + offres CPL, (5) RAG multimodal (document + image + audio), (6) IA Act compliance tools — produit ou service potentiel. **Signal à surveiller** : adoption des LLM par les PME françaises — le 'moment chatbot' pour les entreprises françaises est en cours. C'est le contexte de marché de CPL."}
    ],
    ["veille stratégique", "IA", "CPL", "marché", "technologies", "compétitivité"]
))

save("cpl/usage_professionnel/reporting_direction.json", kucpl(
    "reporting_direction",
    "Reporting direction CPL — communicer les résultats et la vision",
    "Le reporting est un outil de pilotage et de communication — pas un exercice de documentation. Pour CPL, il permet à Céline de garder la vue d'ensemble, de prendre des décisions éclairées et de communiquer la valeur de CPL à ses partenaires et investisseurs.",
    "Le reporting direction CPL est le processus de synthèse et de communication des indicateurs clés de performance, de l'avancement des projets et de la santé globale de l'activité, destiné à la direction (Céline) et aux parties prenantes stratégiques de CPL.",
    {
        "reporting_types": [
            {
                "type": "Weekly — Vue opérationnelle",
                "content": ["Projets en cours : statut RAG (vert/orange/rouge)", "Clients actifs : satisfaction et risques", "Priorités semaine suivante", "Alertes et escalades"],
                "format": "1 page, tableau + bullets. 10 min à lire max.",
                "audience": "Céline (usage interne)"
            },
            {
                "type": "Monthly — Vue stratégique",
                "content": ["KPI financiers (CA, pipeline, marge)", "Projets livrés et en cours", "Satisfaction client (NPS si mesuré)", "Veille et opportunités marché", "Ressources et capacités"],
                "format": "3-5 pages ou tableau de bord. 30 min de lecture ou review.",
                "audience": "Céline + partenaires stratégiques"
            },
            {
                "type": "Investisseur / Partenaire — Vue pitch",
                "content": ["Traction (croissance clients, CA)", "Différenciation CPL", "Pipeline et projections", "Prochaines étapes stratégiques"],
                "format": "5-10 slides. Dense en données, léger en texte.",
                "audience": "Investisseurs, partenaires, institutions"
            }
        ],
        "CPL_KPIs": [
            "Chiffre d'affaires mensuel et cumulé",
            "Nombre de projets actifs / terminés / pipeline",
            "Taux de satisfaction client (qualitatif si NPS non mesuré)",
            "Durée moyenne de projet",
            "Taux de renouvellement / upsell client",
            "Leads entrants (source, volume, taux de conversion)"
        ]
    },
    [
        {"prompt": "Comment structurer un rapport mensuel pour CPL ?",
         "answer": "Structure en 5 sections : (1) **Chiffres clés** (1 tableau) — CA mois, CA cumulé, projets actifs, pipeline qualifié, (2) **Projets** (statut rapide) — vert/orange/rouge par projet. 1 ligne par projet avec statut, client, livrable prochain, (3) **Clients** — alertes satisfaction, renouvellements prévus, opportunities upsell, (4) **Opportunités** — nouveaux leads, partenariats, insights marché, (5) **Décisions à prendre** — ce qui nécessite l'arbitrage de Céline. Format : Notion ou Google Slides selon l'audience. Règle : si personne ne le lit ou si les décisions ne changent pas quand les chiffres changent — simplifier ou arrêter. Le reporting doit déclencher des décisions, pas juste documenter."},
        {"prompt": "ALFRED, génère un template de weekly report pour CPL",
         "answer": "**Weekly CPL — Semaine du [DATE]**\n\n**KPIs clés** :\n- Projets actifs : X\n- Revenus semaine : Xe\n- Leads nouveaux : X\n\n**Projets — Statut RAG** :\n| Projet | Client | Statut | Livrable prochain | Risque |\n|--------|--------|--------|-------------------|--------|\n| [nom] | [client] | 🟢/🟡/🔴 | [quoi] d'ici [quand] | [rien / [issue]] |\n\n**Alertes & Décisions** :\n- [Decision 1 à prendre : choix A vs B]\n- [Alert : client X à appeler]\n\n**Priorités semaine prochaine** :\n1. [P1]\n2. [P2]\n3. [P3]\n\n**Note Céline** : [1-2 lignes libres sur la semaine, énergie, insights]\n\nTemplate à remplir chaque vendredi soir ou lundi matin — 15 minutes max."}
    ],
    ["reporting", "CPL", "direction", "KPI", "pilotage", "communication"]
))

save("cpl/usage_professionnel/gestion_client_difficile.json", kucpl(
    "gestion_client_difficile",
    "Gestion des situations clients difficiles chez CPL",
    "Clients qui demandent plus que le scope, qui tardent à valider, qui changent les specs en cours de projet — les situations difficiles sont inévitables. La méthode CPL : gérer tôt, à l'écrit, avec clarté et sans hostilité.",
    "La gestion des situations clients difficiles chez CPL désigne le processus de résolution des conflits, des désaccords ou des situations de blocage dans la relation client, en préservant à la fois la relation commerciale et les intérêts de CPL. Elle repose sur la clarté du scope initial et la communication directe et documentée.",
    {
        "common_situations": [
            {
                "situation": "Scope creep — le client demande des fonctionnalités hors scope",
                "approach": "Reconnaître la demande positivement + rappeler le scope initial + proposer une option. 'C'est une bonne idée. Ce n'est pas dans le scope actuel — on peut l'inclure dans une phase 2 ou réévaluer le budget. Qu'est-ce que tu préfères ?'",
                "prevention": "Scope défini par écrit et signé en phase 0"
            },
            {
                "situation": "Client qui ne valide pas (bloque l'avancement)",
                "approach": "Relance factuelle + délai + conséquence. 'Ton retour sur X est nécessaire pour continuer. Sans validation d'ici [date], le délai de livraison sera décalé de [durée].' Ne pas absorber le retard silencieusement.",
                "prevention": "Jalons de validation formels dans le planning initial"
            },
            {
                "situation": "Mécontentement client (insatisfaction qualité ou attentes)",
                "approach": "Écouter sans défendre d'abord. 'Je comprends que le résultat ne correspond pas à ce que tu attendais. Qu'est-ce qui manque exactement ?' Puis : ce qui est dans le scope / hors scope. Proposition concrète de résolution.",
                "prevention": "Démos intermédiaires fréquentes"
            },
            {
                "situation": "Retard de paiement",
                "approach": "Relance progressive : mail cordial → mail factuel avec relance formelle → pause de la livraison si non-paiement persistant. Jamais d'hostilité, toujours factuel.",
                "prevention": "Conditions de paiement claires (30% avance, 40% POC, 30% livraison)"
            }
        ],
        "communication_principles": [
            "Toujours par écrit pour les éléments structurants (scope, deadline, retard)",
            "Pas d'hostilité même en cas de conflit — le client difficile d'aujourd'hui peut recommander demain",
            "Proposer des options, pas des ultimatums — 'A ou B ?' vs 'soit tu fais X soit...'",
            "Escalader tôt — ne pas laisser un problème grossir en espérant qu'il se règle seul"
        ]
    },
    [
        {"prompt": "Un client demande des modifications qui dépassent le scope. Comment répondre ?",
         "answer": "Email type : 'Merci pour cette suggestion — c'est effectivement une amélioration intéressante. Pour être transparent : cette modification n'est pas incluse dans le scope initial de notre contrat (section X). Nous avons deux options : (A) L'intégrer maintenant — je vous prépare un devis complémentaire dans 48h, ou (B) L'inclure dans une prochaine phase de projet. Qu'est-ce qui vous convient le mieux ?' Ton : positif, transparent, orienté solution. Jamais 'ce n'est pas prévu' sec. La distinction scope/hors-scope doit être dans le contrat initial — si elle n'y est pas, c'est plus difficile à tenir. Leçon pour le prochain projet."},
        {"prompt": "Un client est mécontent du résultat d'un projet IA. Comment gérer ça ?",
         "answer": "Processus en 3 temps : (1) Écouter complètement sans défendre — 'Je t'entends. Dis-moi précisément ce qui ne correspond pas à tes attentes.' Prendre des notes. Ne pas interrompre pour corriger, (2) Analyser ensemble — comparer le résultat au scope validé. Distinguer : (a) Le résultat ne correspond pas au scope attendu → responsabilité CPL, corriger, (b) L'attente a évolué hors du scope → conversation honnête sur le périmètre, (3) Proposition concrète — délai, correction, compensation si responsabilité CPL avérée. Même si la faute n'est pas à 100% chez CPL, chercher une solution plutôt que d'avoir raison. Un client qui repart satisfait d'une situation mal partie est souvent le plus fidèle."}
    ],
    ["client difficile", "CPL", "scope", "conflit", "communication", "gestion"]
))

save("cpl/usage_professionnel/alfred_usage_interne.json", kucpl(
    "alfred_usage_interne",
    "ALFRED usage interne CPL — assistant de direction",
    "ALFRED est l'assistant IA interne de CPL — utilisé par Céline pour le pilotage quotidien, la rédaction, la préparation des réunions clients et la gestion des connaissances. Ce fichier documente les cas d'usage internes prioritaires.",
    "L'usage interne d'ALFRED chez CPL désigne l'ensemble des tâches et processus pour lesquels ALFRED assiste directement Céline et l'équipe CPL dans leur travail quotidien — de la rédaction au pilotage, de la préparation client à la veille stratégique.",
    {
        "priority_use_cases": [
            {
                "use_case": "Préparation réunion client",
                "how": "ALFRED : brief client + contexte secteur + questions préparatoires + risques à anticiper",
                "prompt_example": "Prépare-moi pour un brief client avec une PME du secteur logistique qui veut automatiser son support client interne"
            },
            {
                "use_case": "Rédaction de propositions commerciales",
                "how": "Première version de proposal basée sur le brief. Céline affine et personnalise.",
                "prompt_example": "Rédige une proposition pour un projet de chatbot knowledge base — client PME industrielle 80 personnes, budget 15k€, délai 3 mois"
            },
            {
                "use_case": "Compte-rendu de réunion",
                "how": "Notes brutes → compte-rendu structuré avec actions et responsables",
                "prompt_example": "Voici mes notes de réunion client [colle notes] — génère un compte-rendu avec décisions prises, actions et deadlines"
            },
            {
                "use_case": "Veille et synthèse",
                "how": "Synthèse d'articles longs, extraction des points clés pour CPL",
                "prompt_example": "Voici un rapport sur l'EU AI Act — résume les implications pratiques pour une startup IA française comme CPL"
            },
            {
                "use_case": "Préparation contenu",
                "how": "Articles LinkedIn, newsletter, documentation produit — premier jet rapide",
                "prompt_example": "Rédige un post LinkedIn sur [sujet] — ton expertise de Céline sur l'IA éthique, 300 mots, angle pratique pour les PME"
            }
        ],
        "ALFRED_limitations_internes": [
            "ALFRED n'a pas accès aux données temps réel des projets (pas de connexion CRM/Notion sans intégration explicite)",
            "Les décisions stratégiques restent à Céline — ALFRED prépare, Céline décide",
            "Les informations client confidentielles ne doivent pas être saisies dans ALFRED si l'instance n'est pas sécurisée (mode local recommandé pour les données sensibles)"
        ]
    },
    [
        {"prompt": "Comment ALFRED peut-il m'aider au quotidien dans la gestion de CPL ?",
         "answer": "5 cas d'usage immédiats : (1) Préparation client — avant chaque réunion, brief rapide sur le contexte de la société, les enjeux sectoriels et les questions à poser, (2) Rédaction first draft — propositions commerciales, emails importants, compte-rendus. Tu affines, ALFRED structure, (3) Synthèse de veille — coller un long article ou rapport et demander 'ce que je dois retenir pour CPL en 3 points', (4) Brainstorm — 'j'ai ce problème avec un client, quelles options j'ai ?' ALFRED joue le rôle de sparring partner, (5) Documentation — transformer des notes de projet en documentation structurée. La règle d'usage : ALFRED prépare et structure, Céline décide et personnalise. Le gain est dans les premières versions et la mise en forme — pas dans la décision elle-même."},
        {"prompt": "ALFRED, prépare-moi pour une réunion avec un DRH qui veut utiliser l'IA pour l'onboarding",
         "answer": "**Brief préparatoire — Réunion DRH / Onboarding IA** **Contexte typique DRH** : priorités = réduction du temps de montée en compétence des nouveaux arrivants, cohérence de l'onboarding quel que soit le manager, disponibilité d'information 24h/24 pour les nouveaux. **Questions clés à poser** : 'Quel est le process d'onboarding actuel — durée, supports, responsables ?' / 'Quelle est la principale douleur : trop long ? Pas cohérent ? Questions répétitives des nouveaux ?' / 'Quelles données existantes (wiki interne, procédures, FAQ RH) ?' / 'Quel profil de nouveaux arrivants — même métier ou diversifié ?' **Angle de proposition CPL** : assistant chatbot nourri par les documents RH + FAQ interne. Les nouveaux peuvent interroger l'assistant à toute heure sans attendre le manager. **Risques à anticiper** : crainte de 'déshumaniser' l'onboarding — argument : ALFRED libère le manager pour les moments humains importants. **ROI à préparer** : si l'onboarding dure 3 mois et que 30% des questions sont répétitives — combien de temps libéré par semaine pour l'équipe RH ?"}
    ],
    ["ALFRED", "CPL", "usage interne", "assistant direction", "Céline", "productivité"]
))

save("cpl/usage_professionnel/proposition_commerciale.json", kucpl(
    "proposition_commerciale",
    "Rédiger une proposition commerciale CPL gagnante",
    "La proposition commerciale est le document pivot entre le besoin client et le contrat. Trop longue = non lue. Trop courte = manque de sérieux. La proposition CPL idéale : 3-5 pages, orientée résultat client, avec un scope très précis.",
    "Une proposition commerciale CPL est le document formel présentant la solution proposée par CPL à un client, incluant le périmètre (scope), la méthodologie, les livrables, le planning, le prix et les conditions. Elle sert de base au contrat et de référence pendant le projet.",
    {
        "structure_CPL": [
            {"section": "1. Compréhension du besoin (1/2 page)", "content": "Reformulation du problème client dans ses termes — prouve qu'on l'a compris. Si le client se reconnaît, il continue de lire."},
            {"section": "2. Solution proposée (1 page)", "content": "Approche CPL + technologies + architecture de haut niveau. Sans jargon. Métaphore si besoin."},
            {"section": "3. Livrables et jalons (1/2 page)", "content": "Ce qu'on livre, quand, sous quel format. Tableau simple. Critères d'acceptation par livrable."},
            {"section": "4. Budget et conditions (1/2 page)", "content": "Prix total + décomposition optionnelle. Conditions : acompte 30%, modalités de paiement, révision scope."},
            {"section": "5. Pourquoi CPL (1/2 page)", "content": "Différenciateurs + référence similaire si applicable + contact Céline."},
            {"section": "6. Prochaines étapes", "content": "Action concrète pour démarrer. 'Si vous souhaitez avancer, signez ce document ou envoyez un email à [contact].'"}
        ],
        "pricing_principles": {
            "value_based": "Prix basé sur la valeur créée pour le client, pas uniquement sur les jours passés",
            "package_vs_regie": "Forfait (package) = moins de risque client, plus de risque CPL. Régie (TJM) = inverse. CPL favorise les forfaits avec jalons clairement définis.",
            "contingency": "Inclure 15-20% de contingence dans les estimations de forfait pour absorber les imprévus"
        }
    },
    [
        {"prompt": "Comment structurer une proposition commerciale pour un projet IA chatbot de 20k€ ?",
         "answer": "Structure 4 pages : (1) Contexte et besoin — 'Suite à notre entretien du [date], nous avons compris que [reformulation du problème en 3 lignes]', (2) Notre approche — [solution en 1/2 page, architecture simple schéma ou texte], (3) Livrables et planning — tableau : POC semaine 4 / MVP semaine 10 / Déploiement semaine 14. Critères d'acceptation par phase. (4) Budget — 20 000€ HT. Décomposition : POC 5k€ / Développement 12k€ / Déploiement + formation 3k€. Conditions : 30% à la commande (6k€), 40% au POC validé, 30% à la livraison finale. La proposition est bonne si : le client peut la lire en 10 minutes et comprend exactement ce qu'il achète."},
        {"prompt": "ALFRED, aide-moi à rédiger l'introduction d'une proposition pour un client dans la santé",
         "answer": "Proposition d'introduction : 'Suite à nos échanges, nous avons retenu que votre équipe médicale consacre en moyenne X heures par semaine à répondre aux mêmes questions de patients et à retrouver des informations dans vos systèmes documentaires. Cette charge croissante affecte le temps disponible pour les soins — votre priorité absolue. CPL propose de créer un assistant IA interne nourri par vos protocoles et vos FAQ, permettant aux soignants et au personnel administratif d'obtenir instantanément une réponse précise sans interrompre leur activité. L'assistant est déployé en architecture locale pour garantir la confidentialité des données de santé (conformité RGPD et HDS selon les cas). Notre objectif : vous rendre [X heures/semaine] pour les patients, pas pour la recherche d'information.'"}
    ],
    ["proposition commerciale", "CPL", "devis", "scope", "contrat", "business"]
))

save("cpl/usage_professionnel/onboarding_collaborateur.json", kucpl(
    "onboarding_collaborateur",
    "Onboarding collaborateur CPL — intégrer un nouveau membre avec ALFRED",
    "L'onboarding d'un collaborateur CPL est l'occasion de montrer concrètement ce qu'ALFRED peut faire en interne — tout en donnant au nouveau membre les outils pour être rapidement opérationnel.",
    "L'onboarding d'un collaborateur CPL est le processus d'intégration d'un nouveau membre de l'équipe incluant la compréhension de la vision, des méthodes de travail, des outils (dont ALFRED), des projets en cours et de la culture CPL.",
    {
        "onboarding_phases": [
            {
                "phase": "Jour 1 — Contexte et vision",
                "activities": ["Présentation CPL par Céline (mission, vision, valeurs)", "Tour des outils : Notion/Trello, ALFRED, outils de dev", "Présentation des clients actifs et projets en cours", "Setup technique"],
                "ALFRED_moment": "Première session ALFRED : montrer comment interroger la base de connaissance interne"
            },
            {
                "phase": "Semaine 1 — Méthodes CPL",
                "activities": ["Lire 3 propositions commerciales récentes", "Observer une réunion client", "Comprendre la méthodologie projet CPL (brief → POC → MVP → déploiement)", "Lire les KU clés dans ALFRED (méthodo, clients, offre)"]
            },
            {
                "phase": "Mois 1 — Montée en autonomie",
                "activities": ["Contribution à un projet en cours sous supervision", "Premier brief client en binôme", "Feedback formel à mi-mois et fin de mois"],
                "KPI": "À fin mois 1 : capable de préparer et conduire un brief client seul"
            }
        ],
        "ALFRED_for_onboarding": [
            "Le nouveau membre peut interroger ALFRED sur les méthodes CPL sans déranger Céline",
            "ALFRED comme documentation vivante — 'comment CPL gère-t-il X ?'",
            "Cas d'usage à montrer dès le jour 1 : 'Ask ALFRED about...' pour les questions courantes"
        ]
    },
    [
        {"prompt": "Comment intégrer efficacement un nouveau collaborateur dans une petite structure comme CPL ?",
         "answer": "Plan en 3 phases adaptées à la taille CPL : (1) Jour 1 intensif — vision et culture (Céline), outils et ALFRED, tour des projets actifs. Objectif : le collaborateur comprend pourquoi CPL existe et pour qui, (2) Semaine 1 — immersion — lire les proposals passées, observer un vrai client, lire la documentation méthodo dans ALFRED. Pas de tâche indépendante encore — absorption, (3) Mois 1 — contribution encadrée — une vraie tâche avec supervision, feedback bi-hebdo. Le premier KPI : au bout de 4 semaines, peut-il conduire un brief client avec un minimum de support ? Avantage CPL : ALFRED comme 'onboarding bot' — le nouveau peut questionner librement sans craindre de 'perdre' le temps de Céline pour chaque question."},
        {"prompt": "ALFRED, prépare un plan d'onboarding pour un développeur IA junior qui rejoint CPL",
         "answer": "**Plan onboarding Dev IA Junior CPL — 30 jours** **Semaine 1 : Contexte** : Lire la documentation ALFRED (architecture, knowledge base, stack). Installer et configurer l'environnement local (Ollama, Python, Flask si applicable). Comprendre l'architecture RAG d'ALFRED avec Céline (1h session). Lire 2 propositions commerciales récentes pour comprendre ce qu'on vend. **Semaine 2 : Premiers pas techniques** : Premier ticket : bug fix ou amélioration mineure sur un module ALFRED existant. Code review par Céline. Assister à une réunion client (observateur). **Semaine 3 : Contribution active** : Feature ou module autonome sous spec Céline. Test et démo. **Semaine 4 : Autonomie** : Premier POC client en binôme avec Céline. Feedback 360 fin de mois. **ALFRED utilisation** : dès le J1, 'demande à ALFRED comment fonctionne X dans notre architecture'. Signale si la réponse est incomplète — c'est une opportunité d'enrichir la KB."}
    ],
    ["onboarding", "CPL", "collaborateur", "ALFRED", "intégration", "formation"]
))

save("cpl/usage_professionnel/analyse_concurrents.json", kucpl(
    "analyse_concurrents",
    "Analyse concurrentielle CPL — se positionner sur le marché IA",
    "Comprendre le paysage concurrentiel de CPL permet de mieux positionner l'offre, de répondre aux questions clients et de trouver les niches à investir. Le marché IA pour les PME est encore peu mature — l'opportunité de positionnement est réelle.",
    "L'analyse concurrentielle de CPL est l'évaluation systématique des acteurs qui s'adressent aux mêmes clients cibles (PME, startups, institutions souhaitant des solutions IA) avec des offres comparables, afin de positionner CPL différemment.",
    {
        "competitive_landscape": {
            "grandes_ESN": {
                "acteurs": "Capgemini, Accenture, Sopra Steria IA — présence IA forte",
                "cible": "Grands comptes, projets >100k€",
                "vs_CPL": "CPL cible les PME et startups. Prix, agilité et proximité sont des avantages CPL. Désavantage : réputation institutionnelle moindre."
            },
            "agences_IA_boutique": {
                "acteurs": "Nombreuses start-ups IA boutique (10-50 personnes) en France",
                "cible": "PME à mid-market",
                "vs_CPL": "Concurrence directe. Différenciateur CPL : éthique by design, local-first, expertise knowledge management, ALFRED comme produit propre."
            },
            "plateformes_nocode": {
                "acteurs": "Zapier AI, Make.com, Relevance AI — plateformes d'automation",
                "vs_CPL": "Complémentaire plutôt que concurrent pour CPL. CPL peut être 'au-dessus' de ces plateformes pour les clients qui ont besoin de personnalisation."
            },
            "chatgpt_direct": {
                "acteurs": "OpenAI ChatGPT Teams, Microsoft Copilot",
                "vs_CPL": "Concurrent sur le 'assistant IA générique'. CPL différencie par : données du client, architecture locale, accompagnement, personnalisation."
            }
        },
        "CPL_positioning": {
            "claim": "L'IA qui connaît votre entreprise, déployée dans vos contraintes",
            "differentiators": ["Architecture locale si données sensibles", "Knowledge base sur mesure", "Éthique et RGPD by design", "Accompagnement par des experts, pas une plateforme", "Expertise secteur PME et institutions françaises"]
        }
    },
    [
        {"prompt": "Comment CPL se différencie-t-il des grandes ESN IA ?",
         "answer": "4 différenciateurs clés : (1) Taille et agilité — CPL peut démarrer un POC en 2 semaines et adapter le projet en temps réel. Une ESN a des processus internes de 6 semaines avant de commencer, (2) Prix — CPL s'adresse aux PME et startups avec des budgets de 5k€ à 50k€. Les ESN ne descendent pas sous 100k€ pour un vrai projet IA, (3) Local-first — expertise d'ALFRED déployé en local. Pour les clients avec des données sensibles (santé, RH, finance), c'est un argument différenciant fort, (4) Relation directe — Céline est impliquée sur les projets stratégiques. Pas de 'junior mis en avant en avant-vente, senior invisible en livraison'. CPL promet ce qu'il livre."},
        {"prompt": "Quelle est la niche la plus prometteuse pour CPL en 2026 ?",
         "answer": "Analyse par critères (marché + avantage CPL) : **Meilleure opportunité** : PME et ETI avec données internes riches mais inaccessibles (documentation, procédures, historique clients). Besoin : knowledge base IA conversationnelle. Avantage CPL : expertise ALFRED, architecture locale, accompagnement. Taille du marché : quasi-illimitée. **Deuxième opportunité** : Institutions (formations, associations, collectivités) cherchant un assistant IA éthique et conforme. CPL crédentiels : approche éthique, RGPD, Mastère Cybersécurité de Céline. **À éviter pour l'instant** : projets IA génériques (ChatGPT wrapper) — concurrence trop forte sur le prix. Projets grands comptes — cycles de vente trop longs pour la phase CPL actuelle."}
    ],
    ["concurrents", "CPL", "positionnement", "marché IA", "différenciation", "stratégie"]
))

save("cpl/usage_professionnel/negociation_contrat.json", kucpl(
    "negociation_contrat",
    "Négociation de contrat CPL — protéger ses intérêts",
    "La négociation d'un contrat de prestation IA est un moment clé pour CPL — les clauses sur le scope, la propriété intellectuelle et les conditions de paiement protègent les deux parties et évitent les conflits futurs.",
    "La négociation de contrat chez CPL est le processus de définition des termes d'une prestation de service IA — périmètre, livrables, propriété intellectuelle, conditions de paiement, garanties et clauses de résiliation — de façon à protéger les intérêts de CPL et à créer une relation claire et durable avec le client.",
    {
        "key_clauses": [
            {
                "clause": "Scope et livrables",
                "content": "Description précise de ce qui est livré. Référence à la proposition commerciale comme annexe contractuelle.",
                "risk_if_absent": "Scope creep sans recours légal"
            },
            {
                "clause": "Conditions de paiement",
                "content": "Acompte 30% à la commande, jalons de paiement intermédiaires, solde à la livraison finale.",
                "risk_if_absent": "Client qui ne paie pas en fin de projet"
            },
            {
                "clause": "Propriété intellectuelle",
                "content": "Différencier : (a) code/modèles génériques CPL = propriété CPL, licence d'usage client. (b) données et contenu client = propriété client.",
                "risk_if_absent": "Conflit sur qui possède quoi"
            },
            {
                "clause": "Confidentialité",
                "content": "NDA bilatéral standard. Les données client sont confidentielles. La solution CPL peut être citée comme référence sauf accord contraire.",
                "risk_if_absent": "Client qui ne peut pas vous citer, ou vous qui publiez des infos client"
            },
            {
                "clause": "Résiliation",
                "content": "Conditions de sortie : résiliation à l'initiative du client (paiement du travail effectué + X%), à l'initiative de CPL (délai de prévenance). Force majeure.",
                "risk_if_absent": "Blocage en cas de conflit"
            }
        ],
        "negotiation_principles": [
            "Négocier sur les intérêts, pas les positions — pourquoi le client veut une clause = souvent compréhensible et trouvable autrement",
            "Les clauses PI sont souvent le point de friction — préparer sa position à l'avance",
            "Un contrat standard CPL réutilisable évite de renegocier depuis zéro à chaque fois",
            "Faire relire par un avocat pour les contrats >20k€"
        ]
    },
    [
        {"prompt": "Comment répondre à un client qui veut que CPL lui cède tous les droits sur le code développé ?",
         "answer": "Position de négociation CPL : distinguer deux éléments : (1) Le code spécifique développé pour ce client (fonctionnalités propres à son métier) → cession possible contre une valeur commerciale juste, (2) Les frameworks, bibliothèques et composants réutilisables CPL (l'infrastructure d'ALFRED, les pipelines RAG, les modules communs) → licence d'usage client oui, cession impossible. Ce serait comme céder le moteur CPL à chaque client. Formulation : 'On peut vous céder les droits sur le code spécifique à votre projet. Sur les composants de base de notre plateforme, on vous donne une licence d'usage perpétuelle — les céder affecterait notre capacité à servir les autres clients avec la même qualité.' Si le client insiste sur la cession totale : augmenter le prix (compensation pour la perte de l'actif CPL) ou refuser si le projet n'en vaut pas le sacrifice."},
        {"prompt": "Quelles sont les clauses à absolument inclure dans le contrat CPL standard ?",
         "answer": "6 clauses non-négociables : (1) Scope défini précisément par référence à la proposition commerciale annexée, (2) Conditions de paiement avec acompte 30% à la commande — sans acompte, ne pas démarrer, (3) PI : licence d'usage client sur les composants CPL, cession des éléments spécifiques client si inclus dans le prix, (4) Confidentialité bilatérale — client et CPL protégés, (5) Résiliation avec préavis et conditions de paiement du travail effectué, (6) Responsabilité limitée — CPL n'est pas responsable au-delà du montant du contrat pour les dommages indirects. Un template Word simple avec ces 6 sections vaut mieux que rien. Pour les projets importants : avocat spécialisé IT (300-500€ pour un contrat type = investissement rentable dès le 2e projet)."}
    ],
    ["contrat", "CPL", "négociation", "propriété intellectuelle", "clauses", "prestation"]
))

save("cpl/usage_professionnel/communication_cpl.json", kucpl(
    "communication_cpl",
    "Communication externe CPL — LinkedIn, articles et position d'expert",
    "La communication externe de CPL est le principal vecteur d'acquisition clients inbound. Céline comme voix experte IA éthique + assistants émotionnels adaptatifs est le positionnement différenciant à construire sur LinkedIn et le blog CPL.",
    "La communication externe CPL est l'ensemble des actions de contenu et de présence sur les plateformes publiques — LinkedIn, site web, articles, conférences — visant à construire la réputation de CPL comme expert IA de confiance pour les PME et institutions françaises.",
    {
        "Celine_personal_brand": {
            "positioning": "Fondatrice CPL. Experte IA émotionnelle adaptative. Handicap invisible (choisir si visible ou non dans le discours public). Mastère AIBD et Cybersécurité.",
            "topics": ["IA éthique et RGPD pour les PME", "Assistants IA personnalisés (ALFRED comme cas d'étude)", "Handicap et tech (si choix de l'en faire un sujet)", "IA émotionnelle — état de l'art et applications", "Retours d'expérience CPL (anonymisés si besoin)"],
            "voice": "Expert accessible, pas condescendant. Pragmatique sur la technique, humaine sur les impacts."
        },
        "content_calendar": {
            "LinkedIn": "2-3 posts par semaine. Mélange : insight technique (1), cas pratique ou retour client (1), question/discussion (1)",
            "article_long": "1 article mensuel approfondi (blog CPL ou Medium). 800-1500 mots. Référencé SEO sur les termes cibles.",
            "newsletter": "Mensuelle si capacité — digest IA + actualité CPL + 1 tip pratique",
            "conférences": "1-2 interventions par trimestre — meetups IA locaux, événements PME, conférences IA si pertinent"
        },
        "content_formats_que_marchent": [
            "Thread LinkedIn — fil de conseils pratiques sur un sujet précis",
            "Avant/après — problème client + solution CPL (anonymisé)",
            "Hot take — opinion sur un sujet IA controversé (différencie)",
            "Behind the scenes — comment on travaille chez CPL, comment ALFRED est construit"
        ]
    },
    [
        {"prompt": "Comment Céline peut-elle construire sa visibilité sur LinkedIn en tant qu'experte IA ?",
         "answer": "Stratégie sur 90 jours : (1) Définir le sujet signature — 'l'IA éthique pour les PME françaises' ou 'construire un assistant IA qui vous ressemble'. Cohérence sur le sujet = expertise perçue, (2) Rythme — 2-3 posts par semaine minimum sur 90 jours. La régularité bat la perfection, (3) Formats à tester — thread (fil de conseils), post opinion (hot take), cas client anonymisé (avant/après), question ouverte (engagement), (4) Engagement — commenter activement les posts d'autres experts IA. La visibilité LinkedIn vient aussi par les commentaires dans la communauté, pas seulement par ses propres posts, (5) ALFRED en contenu — ALFRED lui-même est un sujet de contenu : le processus de construction, les leçons apprises, les défis techniques. Authentique et différenciant."},
        {"prompt": "Aide-moi à rédiger un post LinkedIn sur l'IA éthique pour CPL",
         "answer": "Post option A (opinion directe) : 'L'IA éthique n'est pas un gadget de communication. C'est une décision d'architecture. Concrètement, pour nos clients PME, ça veut dire : ✓ Données qui restent chez eux — pas dans le cloud d'un tiers ✓ Modèle qui peut être audité ✓ Traitement de données conforme RGPD avant la première ligne de code ✓ Pas d'IA qui prédit les comportements humains à leur insu Le mot 'éthique' dans l'IA est souvent marketing. Chez CPL, c'est une checklist technique qu'on remplit avant de livrer. Vous travaillez avec un prestataire IA ? Posez-lui ces 4 questions.' **Note Céline** : adapter en ajoutant un exemple concret du terrain ou un cas CPL récent — ça authentifie le post et le rend plus partageable."}
    ],
    ["communication CPL", "LinkedIn", "Céline", "personal brand", "IA éthique", "contenu expert"]
))

# ═══════════════════════════════════════════════════════════════════════════
# CULTURE / ROMANCE  (8 fichiers) — Jay Crownover + genre romance
# ═══════════════════════════════════════════════════════════════════════════

def kur(file_id, title, summary, core_def, knowledge, examples, tags, priority="high"):
    base = ku(file_id, "culture", "romance", title, summary, core_def, knowledge, examples, tags, priority)
    base["response_guidance"] = {
        "tone": "enthousiaste, fan complice, connaisseur du genre",
        "structure": ["resituer dans l'oeuvre", "analyser", "recommander"],
        "avoid": ["spoiler sans avertissement", "condescendance sur le genre", "généraliser"]
    }
    return base

save("culture/romance/jay_crownover_overview.json", kur(
    "jay_crownover_overview",
    "Jay Crownover — autrice de new adult romance",
    "Jay Crownover est l'une des voix les plus distinctives du new adult romance américain. Ses séries Marked Men, Saints of Denver et The Point explorent des personnages cassés qui se reconstruisent à travers des relations intenses — avec un style émotionnel direct et des antihéros magnétiques.",
    "Jay Crownover est une autrice américaine de new adult romance, connue pour ses histoires de rédemption, ses personnages masculins tatoués et complexes (les 'bad boys with a heart'), ses relations intenses et ses dynamiques de second chance. Elle a publié 30+ romans depuis 2013.",
    {
        "biography": {
            "real_name": "Prénommée Jennifer (pseudonyme Jay Crownover)",
            "start": "Début en autoédition (Kindle) en 2013 avec Rule — succès immédiat dans la communauté romance NA",
            "publisher": "Passée de l'autoédition à William Morrow (HarperCollins) pour les séries principales",
            "prolificacy": "Publie régulièrement — souvent 2-3 romans par an"
        },
        "writing_style": {
            "voice": "Écriture directe, émotionnellement intense. Dialogues mordants et authentiques. Pas de drama artificiel — les conflits viennent des personnages, pas de malentendus évitables.",
            "male_POV": "Forte dans les points de vue masculins — ses narrateurs hommes sont crédibles et vulnérables",
            "themes": ["Rédemption et pardon de soi", "Famille choisie vs famille biologique", "Cicatrices (physiques et émotionnelles) comme récit de soi", "Loyauté et appartenance", "Amour comme facteur de croissance, pas de sauvetage"]
        },
        "main_series": {
            "Marked_Men": "Série fondatrice — 6 livres autour d'un groupe d'amis Denver. Tatoueurs, musiciens, bad boys complexes. Rule comme chef-d'oeuvre du genre.",
            "Saints_of_Denver": "Spin-off de Marked Men. Focalisé sur des personnages secondaires devenus principaux. Plus mature.",
            "The_Point": "Nouvelle adresse des personnages. Extension de l'univers.",
            "Built": "Roman standalone dans l'univers étendu."
        }
    },
    [
        {"prompt": "Qui est Jay Crownover et pourquoi lire ses livres ?",
         "answer": "Jay Crownover est l'autrice qui a défini une partie du genre new adult romance dans les années 2010. Ce qui la distingue : ses personnages masculins ne sont pas des fantasmes idéalisés — ce sont des hommes abîmés, avec des erreurs réelles, des traumas, et une capacité à grandir qui se gagne page par page. Rule, le premier roman de la série Marked Men, en est l'exemple parfait : Shaw est une femme intelligente et solide, pas une ingénue. Rule est un tatoueur punk qui a tout à apprendre de lui-même. La romance qui en résulte est gagnée, pas offerte. Si tu aimes les histoires où les deux protagonistes doivent se réparer eux-mêmes avant de s'aimer — Jay Crownover est pour toi."},
        {"prompt": "Par quel livre de Jay Crownover commencer ?",
         "answer": "Commencer par Rule (Marked Men #1) — c'est le livre qui a lancé sa carrière et qui représente son style au mieux : règle non-dite à Denver, tatouages et cicatrices, amour entre deux personnes qui se connaissent depuis des années mais ne se voient pas encore. Si tu préfères les romances avec plus de maturité et moins d'ambiance lycée/fac, commencer par Nash (Marked Men #4) ou Asa (Saints of Denver) — personnages plus âgés, dynamiques plus complexes. Ordre recommandé : Rule → Rome → Jet → Nash → Rowdy → Asa. Chaque livre est lisible seul mais l'univers s'enrichit d'un livre à l'autre."}
    ],
    ["Jay Crownover", "new adult romance", "Marked Men", "Denver", "rédemption", "romance"]
))

save("culture/romance/marked_men_serie.json", kur(
    "marked_men_serie",
    "Série Marked Men — l'univers Denver de Jay Crownover",
    "La série Marked Men est la fondation de l'univers de Jay Crownover — six romans autour d'un groupe d'amis à Denver liés par leur salon de tatouage et leurs histoires brisées. Chaque livre se concentre sur un personnage différent.",
    "Marked Men est une série de six romans new adult romance de Jay Crownover publiée entre 2013 et 2015. Elle suit un groupe d'amis à Denver — tatoueurs, musiciens, serveurs — liés par une amitié intense et des histoires personnelles douloureuses. Chaque roman est la romance d'un membre du groupe.",
    {
        "books": [
            {
                "number": 1, "title": "Rule", "hero": "Rule Archer", "heroine": "Shaw Landon",
                "dynamic": "Enemies-to-lovers forcé par la famille. Shaw aimait le frère mort de Rule. Rule n'a jamais été digne d'elle — il doit le devenir.",
                "tone": "Intense, émotionnel, douloureux. Le meilleur point d'entrée de la série.",
                "why_read": "Le modèle du bad-boy-qui-grandit de Crownover. Shaw n'attend pas que Rule change — elle exige."
            },
            {
                "number": 2, "title": "Jet", "hero": "Jet Keller", "heroine": "Ayden Cross",
                "dynamic": "Rockstar charismatique vs femme avec un secret douloureux. Romance musicale.",
                "tone": "Plus léger que Rule mais émotionnel. Le passé d'Ayden est le noeud dramatique."
            },
            {
                "number": 3, "title": "Rome", "hero": "Rome Archer (frère de Rule)", "heroine": "Cora Lewis",
                "dynamic": "Marine traumatisé revenu de la guerre. Opposés complets. Rédemption centrale.",
                "tone": "Le plus militaire/trauma. Émotionnellement lourd et gratifiant."
            },
            {
                "number": 4, "title": "Nash", "hero": "Nash Donovan", "heroine": "Saint Ford",
                "dynamic": "Tatoueur responsable et fille rebelle voulant se reconstruire. Complexe et mature.",
                "tone": "Plus adulte. Saint a un passé d'addiction. Nash est le pilier du groupe."
            },
            {
                "number": 5, "title": "Rowdy", "hero": "Rowdy St. James", "heroine": "Salem Cruz",
                "dynamic": "Second chance romance. Amour de jeunesse retrouvé 10 ans plus tard.",
                "tone": "Nostalgique, mélancolique, très émotionnel. L'un des préférés des fans."
            },
            {
                "number": 6, "title": "Asa", "hero": "Asa Cross", "heroine": "Royal Hastings",
                "dynamic": "Frère de la heroine de Jet — rédemption d'un homme qui a fait de mauvais choix. Royal est solide et confiante.",
                "tone": "Fermeture de série. Plus mature, rédemption maximale."
            }
        ],
        "reading_order": "Dans l'ordre de parution pour avoir le contexte complet, mais chaque livre est lisible seul.",
        "universe_extension": "Les personnages de Marked Men apparaissent dans Saints of Denver et The Point — l'univers Denver est continu."
    },
    [
        {"prompt": "Dans quel ordre lire la série Marked Men de Jay Crownover ?",
         "answer": "Ordre de parution recommandé : Rule → Jet → Rome → Nash → Rowdy → Asa. Pourquoi cet ordre : (1) Rule pose l'univers et les personnages principaux. Tous les autres héros apparaissent dans Rule, donc tu les connais quand arrive leur livre, (2) Jet et Rome peuvent se lire dans n'importe quel ordre après Rule, (3) Nash, Rowdy, Asa sont mieux avec le contexte des précédents. Possibilité de commencer par Nash si tu préfères les dynamiques plus adultes — il est lisible sans les précédents, (4) Asa est vraiment la conclusion de série — il est mieux apprécié avec tout le contexte. Si tu veux lire dans n'importe quel ordre : chaque romance est complète et se lit seule. Le plaisir est plus riche dans l'ordre mais ce n'est pas obligatoire."},
        {"prompt": "Quel est le meilleur livre de la série Marked Men ?",
         "answer": "Question à 1 million — la réponse varie selon les lecteurs : **Rule** (livre 1) : le classique fondateur. Shaw/Rule = le couple référence de la série. L'émotion de la famille, du deuil et de la rédemption est au maximum. Souvent le préféré. **Rome** (livre 3) : le plus émotionnellement intense. Trauma militaire, PTSD, rédemption difficile. Ceux qui aiment les heroes brisés avec beaucoup à surmonter préfèrent Rome. **Rowdy** (livre 5) : le plus romantique au sens classique. Second chance, nostalgie, amour de jeunesse. Souvent le préféré de ceux qui aiment les romances mélancoliques. Ma recommandation personnelle : Rule pour découvrir le style Crownover. Rowdy pour ceux qui aiment que les larmes arrivent."}
    ],
    ["Marked Men", "Jay Crownover", "Rule", "Denver", "série romance", "new adult"]
))

save("culture/romance/saints_of_denver.json", kur(
    "saints_of_denver",
    "Saints of Denver — la suite de l'univers Marked Men",
    "Saints of Denver est la série spin-off qui explore des personnages secondaires de Marked Men devenus principaux. Plus mature et avec des dynamiques plus complexes — un must pour les fans de l'univers Crownover.",
    "Saints of Denver est une série de cinq romans de Jay Crownover qui étend l'univers Marked Men en suivant des personnages précédemment secondaires. Publiée entre 2015 et 2017, elle approfondit l'univers Denver avec des thèmes plus adultes.",
    {
        "books": [
            {
                "title": "Salvaged", "hero": "Hudson Wheeler", "heroine": "Poppy Cruz",
                "dynamic": "Ami doux et fiable qui est toujours dans la zone amicale — enfin centre de sa propre histoire. Romance de l'ami qui mérite mieux.",
                "tone": "Plus doux que Marked Men. Hudson est un 'nice guy' qui grandit. Romance touchante."
            },
            {
                "title": "Riveted", "hero": "Zeb Fuller", "heroine": "Sassa Larsen",
                "dynamic": "Amish qui quitte sa communauté + tatoueur au grand coeur. Romance très originale dans l'univers.",
                "tone": "Décalé, charmant. La dimension culturelle de l'Amish donne un angle inhabituel."
            },
            {
                "title": "Charged", "hero": "Quaid Jackson", "heroine": "Avett Banks",
                "dynamic": "Avocat qui défend une client hors de ses habitudes. Enemies-to-lovers professionnel.",
                "tone": "Plus sophistiqué. Quaid est le personnage le plus 'establishment' de l'univers."
            },
            {
                "title": "Built", "hero": "Zeb revient", "heroine": "—",
                "note": "Built est parfois classé séparément — standalone dans l'univers étendu"
            },
            {
                "title": "Leveled", "hero": "Dominic Novak", "heroine": "Kallie Foster",
                "dynamic": "Clôture de la série. Retour de personnages connus + nouvelle romance."
            }
        ],
        "why_read_after_marked_men": "Si Marked Men a créé l'univers, Saints of Denver l'approfondit. Personnages plus matures. Hudson (Salvaged) est particulièrement bien accueilli par les lecteurs qui voulaient voir l'ami gentil avoir sa propre romance.",
        "standalone_accessibility": "Chaque Saint peut être lu seul — mais Marked Men donne le contexte des relations et de l'univers Denver."
    },
    [
        {"prompt": "Faut-il lire Marked Men avant Saints of Denver ?",
         "answer": "Recommandé mais pas obligatoire. Ce que tu gagnes à lire Marked Men avant : (1) Les personnages de Saints of Denver apparaissent dans Marked Men — tu les connais déjà quand ils deviennent protagonistes. Ça enrichit leur romance, (2) L'univers Denver (les lieux, les relations, la dynamique de groupe) est établi dans Marked Men. Moins à mettre en place dans Saints of Denver si tu connais déjà. Ce que tu perds sans Marked Men : surtout le contexte de Salvaged (Hudson) et Charged (Quaid) qui ont du sens dans la continuité du groupe. Point d'entrée possible : commencer par Salvaged si tu veux tester le style Crownover avec un héros plus doux et accessible que Rule."},
        {"prompt": "Quel livre de Saints of Denver recommandes-tu en premier ?",
         "answer": "Salvaged (Hudson et Poppy) en premier pour deux raisons : (1) Hudson est l'un des personnages les plus attachants de tout l'univers Crownover. C'est le 'nice guy' qui a toujours été dans l'ombre — le voir enfin être l'héros de sa propre histoire est émotionnellement satisfaisant d'une façon très différente des bad boys habituels, (2) La romance Hudson/Poppy est chaleureuse et accessible — moins d'angoisse que Rule, plus de sweet. Bon équilibre pour découvrir si tu aimes le style Crownover hors du contexte bad-boy intense. Pour les fans de drama et d'adversité : Charged (Quaid) a une tension enemies-to-lovers professionnelle bien construite. Riveted (Zeb/Sassa) est le plus original — la dimension Amish donne quelque chose de rare dans le genre."}
    ],
    ["Saints of Denver", "Jay Crownover", "Salvaged", "Hudson", "spin-off", "romance"]
))

save("culture/romance/new_adult_genre.json", kur(
    "new_adult_genre",
    "New Adult Romance — genre, codes et meilleurs auteurs",
    "Le New Adult (NA) est un genre littéraire apparu vers 2009, entre le Young Adult et l'Adult Fiction. Il cible les 18-25 ans et traite de la transition vers la vie adulte — fac, premier emploi, identité, sexualité adulte. Jay Crownover en est l'une des figures fondatrices.",
    "Le New Adult Romance est un sous-genre de la romance qui suit des protagonistes de 18 à 25 ans naviguant les premières expériences de l'âge adulte — quitter la maison parentale, la fac, les premières relations sérieuses, les ambitions de carrière. Il se distingue du Young Adult par la présence de scènes plus explicites et de thèmes plus matures.",
    {
        "definition": {
            "age_range": "Protagonistes 18-25 ans (vs YA 14-18, vs Adult Romance 25+)",
            "themes": ["Premier amour adulte sérieux", "Fac et transitions de vie", "Découverte d'identité hors du foyer parental", "Premier emploi / carrière", "Trauma et résilience", "Famille choisie vs famille biologique"],
            "explicitness": "Plus explicite sexuellement que le YA (scènes adultes possibles), moins que l'erotic romance. Varie selon les auteurs."
        },
        "founding_authors": [
            {
                "author": "Colleen Hoover (CoHo)",
                "known_for": "Ugly Love, It Ends With Us — drama émotionnel intense. Phénomène TikTok BookTok 2022-2023.",
                "style": "Émotionnellement destructeur. Romance douloureuse avec rédemption ou non."
            },
            {
                "author": "Jay Crownover",
                "known_for": "Marked Men — bad boys tatoués Denver. Fondatrice du sous-genre.",
                "style": "Intense, émotionnel, personnages masculins complexes et crédibles."
            },
            {
                "author": "Tammara Webber",
                "known_for": "Easy — romance fac avec thème d'agression sexuelle. Pionnière du genre.",
                "style": "Mature, sensible, émotionnellement responsable."
            },
            {
                "author": "Jamie McGuire",
                "known_for": "Beautiful Disaster — l'un des premiers bestsellers NA. Travis et Abby.",
                "style": "Toxique assumé mais très populaire. Le couple à problèmes archétypal."
            },
            {
                "author": "Penelope Douglas",
                "known_for": "Bully, Devil's Night series — dark romance avec tension intense.",
                "style": "Plus sombre. Limites repoussées dans la toxicité romantique."
            }
        ],
        "booktok_effect": "BookTok (TikTok book community) a massivement amplifié le NA à partir de 2021. Colleen Hoover a vendu 8+ millions de livres en 2022 grâce au phénomène. Le NA est devenu le genre le plus viralisable sur les réseaux sociaux."
    },
    [
        {"prompt": "C'est quoi le New Adult Romance et pourquoi c'est différent du YA ?",
         "answer": "Différence principale : l'âge des protagonistes et la maturité des thèmes. YA (Young Adult) = 14-18 ans, école secondaire, premiers émois, sexualité suggérée. New Adult = 18-25 ans, fac ou premier emploi, premier amour sérieux, sexualité présente (parfois explicite), responsabilités adultes émergentes. Le NA est aussi plus sombre dans ses thèmes — trauma, addiction, violence dans les relations (romance foncée / dark romance). Les deux se recoupent dans les rayons bookshop mais les lecteurs sont distincts : le NA cible ceux qui ont 'dépassé' le lycée mais ne se reconnaissent pas encore dans les romances d'adultes établis. En pratique : si les personnages ont des dorms, des profs de fac et des colocataires qui fêtent leurs 21 ans — c'est du NA."},
        {"prompt": "Je viens de finir Marked Men et j'ai adoré. Que lire ensuite dans le NA romance ?",
         "answer": "Par profil : (1) Tu aimes les personnages brisés mais qui grandissent vraiment — Tammara Webber 'Easy' : romance fac avec profondeur émotionnelle et personnage masculin qui mérite sa rédemption. Plus sobre que Crownover mais aussi satisfaisant, (2) Tu aimes le drama intense et les pleurs garantis — Colleen Hoover 'November 9' (moins brutal qu'Ugly Love, meilleure entrée) ou 'Confess' — émotionnellement denses, (3) Tu aimes la tension sexuelle et les bad boys sombres — Penelope Douglas 'Punk 57' ou 'Bully'. Plus dark, frontières repoussées, mais très populaires, (4) Tu veux du fun et de l'énergie — Elena Armas 'The Spanish Love Deception' — enemies-to-lovers avec beaucoup d'humour. Plus adulte mais accessible."}
    ],
    ["New Adult", "romance", "BookTok", "Colleen Hoover", "genre", "18-25 ans"]
))

save("culture/romance/romance_tropes.json", kur(
    "romance_tropes",
    "Tropes du roman romance — guide complet des codes du genre",
    "Les tropes sont les structures narratives récurrentes du romance — enemies-to-lovers, fake dating, second chance, forbidden love. Loin d'être une faiblesse du genre, ils sont le langage partagé entre auteurs et lecteurs qui créent les attentes et les plaisirs du roman.",
    "Un trope de romance est un pattern narratif récurrent qui structure la relation romantique dans le roman. Il ne s'agit pas d'un cliché péjoratif mais d'un code générique partagé entre auteur et lecteur qui crée un horizon d'attente et une satisfaction narrative spécifique quand il est bien exécuté.",
    {
        "popular_tropes": [
            {"trope": "Enemies to lovers", "description": "Antagonisme qui se transforme en attraction. La tension hostile devient sexuelle puis romantique.", "appeal": "La transformation d'une émotion forte (hostilité) en une autre émotion forte (amour). Satisfaisant parce que difficile à atteindre."},
            {"trope": "Fake relationship / fake dating", "description": "Relation feinte pour une raison externe qui devient réelle.", "appeal": "Permet l'intimité progressive dans un cadre 'sécurisé'. Le moment où le faux devient réel est la scène payoff la plus attendue."},
            {"trope": "Second chance romance", "description": "Anciens amoureux réunis après une séparation. L'amour interrompu retrouvé.", "appeal": "Nostalgie + 'est-ce qu'ils vont cette fois y arriver ?' Le lecteur connaît leur histoire — empathie immédiate."},
            {"trope": "Forbidden love", "description": "Un obstacle externe empêche la relation — famille, statut, religion, âge, profession.", "appeal": "L'obstacle amplifie le désir — 'on ne devrait pas' = tension maximale."},
            {"trope": "Forced proximity", "description": "Les protagonistes sont contraints de partager un espace — colocation, voyage, job.", "appeal": "L'intimité non choisie crée des situations de découverte progressive."},
            {"trope": "Brother's best friend / Boss/Employee", "description": "Transgression d'une frontière sociale ou familiale.", "appeal": "Le tabou + les enjeux émotionnels (loyauté, risque) amplifient la tension."},
            {"trope": "Grumpy/sunshine", "description": "Personnage sombre + personnage solaire. Opposés complets.", "appeal": "Contraste de personnalité = équilibre parfait. L'un adoucit l'autre."},
            {"trope": "Sports romance", "description": "Athlète + quelqu'un hors de son monde.", "appeal": "La compétition comme métaphore de la relation. Le corps comme enjeu."}
        ],
        "trope_vs_execution": "Le trope n'est pas la garantie — c'est l'exécution qui fait la différence. Deux livres sur 'enemies to lovers' peuvent être radicalement différents en qualité. Les lecteurs de romance savent ce qu'ils aiment ET sont très exigeants sur la qualité de l'exécution.",
        "Jay_Crownover_tropes": "Marked Men utilise principalement : enemies-to-lovers (Rule), second chance (Rowdy), redemption arc (tous les héros). Signature de Crownover : les bad boys doivent mériter la heroine, pas l'inverse."
    },
    [
        {"prompt": "Quels sont les meilleurs livres pour le trope enemies-to-lovers ?",
         "answer": "Tops par style : (1) New Adult / contemporain — Rule de Jay Crownover : Rule et Shaw se 'détestent' depuis des années, la résolution est méritée. The Hating Game de Sally Thorne : enemies-to-lovers de bureau, drôle et touchant. Dossier K de Penelope Douglas : dark et intense. (2) Fantasy — A Court of Mist and Fury de Sarah J. Maas : construction sur 2 livres, tension maximale. From Blood and Ash de Jennifer L. Armentrout : enemies-to-lovers avec world-building dense. (3) Classique — Orgueil et Préjugés de Jane Austen : le template originel du genre. Darcy et Elizabeth = la matrice de tout enemies-to-lovers moderne. Critère qualité : les meilleurs enemies-to-lovers ont une RAISON VALABLE à l'inimitié — pas juste un malentendu. Rule et Shaw ont un deuil partagé et une incompréhension de 5 ans. C'est réel."},
        {"prompt": "Est-ce que les tropes de romance sont une répétition ou une vraie technique narrative ?",
         "answer": "Technique narrative — et la distinction importe. Les tropes sont à la romance ce que la sonate est à la musique classique : un cadre formel qui permet l'expression infinie dans une structure reconnue. Le lecteur de romance sait qu'il va y avoir un HEA (Happily Ever After) ou HFN (Happy For Now) — c'est le contrat du genre. Ce qu'il ne sait pas : comment ils y arrivent, quelles douleurs ils traversent, quelle version d'eux-mêmes ils deviennent. La satisfaction du romance n'est pas 'est-ce qu'ils finissent ensemble ?' (oui, toujours) mais 'comment le voyage a-t-il eu lieu et qu'est-ce que j'ai ressenti ?'. Les meilleurs romances de trope sont ceux qui font jouer le trope de façon inattendue ou qui approfondissent ses implications psychologiques au lieu de les survoler."}
    ],
    ["tropes romance", "enemies-to-lovers", "fake dating", "second chance", "genre romance", "narratif"]
))

save("culture/romance/romance_lecture.json", kur(
    "romance_lecture",
    "Lire de la romance — guide et recommandations par humeur",
    "La romance est le genre le plus lu au monde (34%+ des ventes de fiction en anglais selon RWA). Elle offre un espace de garantie émotionnelle — le happy ending — dans un monde où les fins heureuses ne sont pas garanties. Les guides de lecture par humeur permettent à ALFRED d'être un compagnon de lecture utile.",
    "La romance est un genre littéraire centré sur une histoire d'amour entre deux (ou plus) protagonistes et garantissant un dénouement heureux (HEA ou HFN). Elle inclut de nombreux sous-genres : contemporaine, historique, fantasy romantique, paranormal, romantique sombre (dark romance), érotique, et new adult.",
    {
        "subgenres": {
            "contemporaine": "Cadre actuel, personnages modernes. Le sous-genre dominant en volume.",
            "historique": "Régence britannique (Jane Austen, Julia Quinn), Écosse, Victorien. Codes sociaux stricts comme source de tension.",
            "fantasy_romantique": "Romance principale dans un cadre fantastique. Sarah J. Maas, Jennifer L. Armentrout. Audience croisée fantasy/romance.",
            "paranormal": "Vampires, loups-garous, fées dans une romance. Très populaire 2008-2015, regain depuis BookTok.",
            "dark_romance": "Romance avec des dynamiques de pouvoir déséquilibrées, violence, consentement questionnable. Triggering warnings nécessaires. Lecteurs adultes consentants.",
            "romantasy": "Terme BookTok pour fantasy romantique — accent sur la romance au moins autant que le world-building.",
            "erotic_romance": "Scènes explicites centrales (pas juste présentes). Distinct de la romance avec scènes adultes."
        },
        "reading_by_mood": {
            "besoin_de_rire": ["The Spanish Love Deception — Elena Armas", "The Hating Game — Sally Thorne", "People We Meet on Vacation — Emily Henry"],
            "besoin_de_pleurer": ["November 9 — Colleen Hoover", "It Ends With Us — Colleen Hoover", "All Your Perfects — Colleen Hoover"],
            "besoin_de_tension": ["Rule — Jay Crownover", "Punk 57 — Penelope Douglas", "Archer's Voice — Mia Sheridan"],
            "besoin_de_fantasy": ["A Court of Thorns and Roses — Sarah J. Maas", "From Blood and Ash — J.L. Armentrout", "The Bridge Kingdom — Danielle L. Jensen"],
            "besoin_de_douceur": ["Beach Read — Emily Henry", "The Kiss Quotient — Helen Hoang", "Act Your Age, Eve Brown — Talia Hibbert"]
        },
        "HEA_contract": "HEA (Happily Ever After) et HFN (Happy For Now) sont les deux fins acceptables dans le genre romance. Un roman romance sans happy ending est soit une tragédie romantique, soit de la literary fiction. La garantie du HEA est le fondement du contrat lecteur/genre."
    },
    [
        {"prompt": "Je veux commencer la romance mais je ne sais pas par où. Guide-moi.",
         "answer": "Par profil lecteur : (1) Tu viens du YA et tu veux passer à quelque chose de plus adulte — commencer par du contemporain léger : The Hating Game (Sally Thorne) ou Beach Read (Emily Henry). Humour, tension, personnages attachants, pas trop intense. (2) Tu veux du drama et tu n'as pas peur de pleurer — Colleen Hoover. November 9 est une entrée plus douce que It Ends With Us. Prévoir des mouchoirs. (3) Tu aimes le fantasy et tu veux y ajouter de la romance — ACOTAR de Sarah J. Maas. Tome 1 introduit l'univers, tome 2 = romance explosive. (4) Tu veux des personnages vrais avec beaucoup de background émotionnel — Jay Crownover, Rule. Bad boy qui doit mériter son heroine. Intensément satisfaisant. Une seule règle : ne pas commencer par un livre trop dark ou trop explicite. Les premières impressions comptent."},
        {"prompt": "Qu'est-ce que le HEA et pourquoi c'est important en romance ?",
         "answer": "HEA = Happily Ever After. C'est le contrat fondamental du genre : tu sais, avant d'ouvrir le livre, que les protagonistes vont finir ensemble et heureux. HFN = Happy For Now — fin heureuse dans l'immédiat sans projection à long terme. Ce n'est pas de la naïveté narrative — c'est un choix de genre délibéré avec des implications psychologiques réelles : (1) Espace de sécurité — dans un monde incertain, pouvoir s'investir émotionnellement dans une histoire avec la garantie que ça finit bien est une forme de résilience, (2) Focalisation sur le voyage — puisque la fin est connue, tout l'intérêt est dans le HOW. Comment ils y arrivent, ce qu'ils traversent, qui ils deviennent. (3) Ce n'est pas une fin naïve — les meilleurs HEA sont GAGNÉS par les personnages. Ils ont changé, grandi, réparé quelque chose. Ça ne tombe pas du ciel."}
    ],
    ["romance", "sous-genres", "lecture", "HEA", "recommandations", "BookTok"]
))

save("culture/romance/booktok_community.json", kur(
    "booktok_community",
    "BookTok — la révolution de la lecture sur TikTok",
    "BookTok est la communauté de lecteurs sur TikTok qui, depuis 2020, a transformé le marché du livre — propulsant des auteurs inconnus vers des millions de ventes et créant une culture de lecture visuelle et émotionnelle totalement nouvelle.",
    "BookTok est la communauté de lecteurs, bloggers et créateurs de contenu littéraire sur TikTok. Depuis 2020, elle a transformé le marché du livre en faisant de courts vidéos émotionnelles sur les livres un vecteur d'influence massif — créant des bestsellers du jour au lendemain et ressuscitant des livres publiés des années auparavant.",
    {
        "impact": {
            "market_disruption": "Colleen Hoover a vendu 8 millions de livres en 2022 grâce à BookTok — son phénomène est le cas d'école. Des autrices autoéditées de NA des années 2013-2015 (Jay Crownover incluse) ont vu leurs anciennes séries ressuscitées.",
            "format": "Courtes vidéos 15sec-3min. Reaction de fin de livre (souvent en pleurs). Thirst edits (montages de love interests). Recommandations par vibe. 'This book broke me' est devenu un meme d'endorsement.",
            "community": "La communauté BookTok est massivement féminine (18-35 ans), très engagée et très influente. Elle a normalisé la lecture de romance comme activité publique et fière."
        },
        "BookTok_favorites": [
            "Colleen Hoover — la reine incontestée de BookTok (8M+ ventes 2022)",
            "Emily Henry — contemporaine avec humour et personnages complexes",
            "Ana Huang — romance en milieu luxe/corporate",
            "Taylor Jenkins Reid — fiction adulte avec structure narrative inventive (Daisy Jones)",
            "Jennifer L. Armentrout — fantasy romantique / paranormal"
        ],
        "criticism": "BookTok a été critiqué pour : privilégier les livres 'émotionnellement destructeurs' (trauma-book obsession), créer des tendances éphémères sans durabilité, et parfois surventre des livres médiocres via la viralité. Aussi pour la blancheur de la liste des favoris initialement.",
        "discovery": "Pour les lecteurs : BookTok est un outil de découverte puissant si on suit des comptes avec un goût similaire au sien plutôt que de suivre les trends virales."
    },
    [
        {"prompt": "C'est quoi BookTok et comment l'utiliser pour trouver des lectures ?",
         "answer": "BookTok = la communauté lecture de TikTok. Des créateurs font des vidéos courtes — réactions émotionnelles, recommandations, analyses, lectures à voix haute. Ce qui le rend utile : (1) L'algorithme TikTok apprend vite tes goûts — si tu interagis avec des recommandations romance NA, tu en verras davantage, (2) Les 'vibes check' — 'si tu aimes X, tu vas aimer Y' sont souvent précis dans la communauté, (3) Les réactions authentiques (les vraies larmes à la fin d'un livre) sont un signal d'impact émotionnel qu'une critique écrite ne donne pas. Comment l'utiliser : cherche #BookTok #romancebooks #NewAdultRomance sur TikTok. Suis 2-3 comptes dont le goût ressemble au tien. Utilise les recommandations comme liste Goodreads à tester. Ne pas tout acheter par effet de herd — certains books viraux sont décevants hors de l'hystérie collective."},
        {"prompt": "Pourquoi Colleen Hoover est-elle aussi populaire sur BookTok ?",
         "answer": "Trois raisons convergentes : (1) Style émotionnel maximum — ses livres font pleurer avec une efficacité qui se filme bien. Les réactions BookTok 'ce livre m'a brisée' sont du marketing viral parfait pour ses titres. It Ends With Us a des scènes qui ont généré des millions de réactions vidéo, (2) Diversité de ses titres — elle couvre plusieurs dynamiques (romance dramatique, romance légère, romance mature) donc une large audience la trouve. Le meilleur point d'entrée est différent selon le lecteur, (3) Timing parfait — elle était connue mais pas massive avant BookTok. L'algorithme TikTok l'a propulsée exactement quand la plateforme explosion 2020-2022. Son éditeur (Atria Books) a su capitaliser en réimprimant massivement. La nuance : CoHo est divisive. Ses fans l'adorent passionnément. Les détracteurs trouvent ses livres manipulatifs et ses thèmes traités superficiellement (critique de It Ends With Us sur le traitement de la violence domestique). Les deux perspectives coexistent."}
    ],
    ["BookTok", "TikTok", "Colleen Hoover", "communauté lecture", "romance", "viralité"]
))

print("\n=== Part 3 : 12 CPL + 8 romance = 20 fichiers ===")
print("\n=== TOTAL BATCH DAY 2 : 20 + 20 + 20 = 60 fichiers ===")
