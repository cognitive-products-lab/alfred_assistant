"""
Enrichissement Knowledge Base ALFRED - Batch 9 : reasoning (15 restants) + product_mgmt/advanced (5 premiers)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku_reas(stem, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.professional.engineering.reasoning.{stem}",
      "title": title, "domain": "professional", "subdomain": "engineering_reasoning",
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": "rigoureux, ancré dans les mécanismes cognitifs et techniques du raisonnement LLM",
        "structure": ["identifier le type de raisonnement ou biais", "expliquer le mécanisme", "proposer une technique d'amélioration"],
        "avoid": ["confondre raisonnement humain et LLM", "ignorer les limites des LLMs", "trop abstrait"]
      },
      "tags": tags + ["raisonnement", "LLM", "inférence"],
      "related_knowledge_units": ["knowledges.professional.engineering.ai.reasoning_engine"]
    }

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

# =============================================================================
# professional / engineering / reasoning (15 restants)
# =============================================================================

save("professional/engineering/reasoning/deductive_reasoning.json", ku_reas(
  "deductive_reasoning",
  "Raisonnement déductif",
  "Le raisonnement déductif part de prémisses générales pour en dériver des conclusions nécessaires. C'est le mode de raisonnement formel le plus fiable — si les prémisses sont vraies et la logique valide, la conclusion est vraie.",
  "Le raisonnement déductif est une forme de raisonnement logique qui procède du général vers le particulier : à partir de prémisses générales (principes, règles, faits établis), on dérive des conclusions spécifiques dont la vérité est garantie si les prémisses sont vraies et le raisonnement valide.",
  {
    "deductive_forms": [
      {"form": "Syllogisme", "structure": ["Prémisse majeure : Tous les X sont Y", "Prémisse mineure : Z est un X", "Conclusion : Z est Y"], "example": "Tous les modèles ont une fenêtre de contexte. GPT-4 est un modèle. GPT-4 a une fenêtre de contexte."},
      {"form": "Modus ponens", "structure": ["Si P alors Q", "P est vrai", "Donc Q est vrai"], "example": "Si le budget est dépassé, le projet est en danger. Le budget est dépassé. Le projet est en danger."},
      {"form": "Modus tollens", "structure": ["Si P alors Q", "Q est faux", "Donc P est faux"], "example": "Si le code est correct, les tests passent. Les tests ne passent pas. Le code n'est pas correct."}
    ],
    "common_deductive_fallacies": [
      {"fallacy": "Affirmer le conséquent", "example": "Si P alors Q. Q est vrai. Donc P est vrai. — INVALIDE (Q peut être vrai pour d'autres raisons)"},
      {"fallacy": "Prémisse fausse", "example": "Raisonnement valide mais sur une prémisse incorrecte → conclusion fausse"},
      {"fallacy": "Généralisation abusive", "example": "Traiter une règle avec exceptions comme absolue"}
    ],
    "llm_deductive_performance": "Les LLMs performent bien sur la déduction formelle simple (syllogismes), mais tendent à 'court-circuiter' sur des chaînes de déduction longues. Le Chain of Thought force l'externalisation des étapes intermédiaires, améliorant la précision."
  },
  [
    {"prompt": "Aide-moi à vérifier si mon raisonnement est correct : 'Si notre taux de rétention est bon, les utilisateurs sont satisfaits. Notre taux de rétention est 80%. Donc nos utilisateurs sont satisfaits.'", "answer": "Le raisonnement est valide formellement (modus ponens), mais attention à la prémisse majeure. Un bon taux de rétention n'implique pas nécessairement la satisfaction — il peut indiquer des frictions à la sortie (switching costs élevés) plutôt que de la satisfaction. Je te conseille de vérifier avec des données de satisfaction directes (NPS, CSAT) avant de conclure."},
    {"prompt": "Comment utiliser la logique déductive pour analyser un bug ?", "answer": "Structure classique : Prémisse 1 (règle du système) : 'Si l'input est null, la fonction X lève une NullPointerException'. Prémisse 2 (observation) : 'Une NullPointerException est levée'. Conclusion intermédiaire : 'L'input est probablement null'. Test de modus tollens : si l'input n'est PAS null après log, la prémisse 1 est insuffisante — chercher d'autres chemins vers l'exception. La déduction cadre le debug de façon systématique."}
  ],
  ["déduction", "syllogisme", "logique formelle", "modus ponens", "raisonnement"]
))

save("professional/engineering/reasoning/inductive_reasoning.json", ku_reas(
  "inductive_reasoning",
  "Raisonnement inductif",
  "Le raisonnement inductif part d'observations spécifiques pour inférer des règles générales. Contrairement à la déduction, il ne garantit pas la vérité de la conclusion — mais c'est le moteur de l'apprentissage et de la découverte.",
  "Le raisonnement inductif est une forme de raisonnement qui procède du particulier vers le général : à partir d'observations spécifiques répétées, on infère des règles, des patterns ou des lois générales qui peuvent expliquer les observations et prédire les cas futurs.",
  {
    "inductive_reasoning_types": [
      {"type": "Généralisation simple", "description": "De N observations similaires, inférer une règle", "example": "Les 10 derniers déploiements ont causé des lenteurs le lundi → les déploiements causent des lenteurs"},
      {"type": "Analogie", "description": "Si deux systèmes se ressemblent sur X propriétés, ils se ressemblent probablement sur Y", "example": "Ce framework ressemble à React → il a probablement un lifecycle similaire"},
      {"type": "Inférence causale", "description": "Observer une corrélation et inférer une causalité (attention : corrélation ≠ causalité)", "example": "Après déploiement de la feature A, les conversions ont augmenté"}
    ],
    "strengths_and_limits": {
      "strength": "L'induction est le seul moteur de découverte à partir de données — elle permet de créer de nouvelles hypothèses",
      "limit": "Une généralisation inductive reste toujours réfutable par un contre-exemple. La force de l'induction dépend de la taille et la diversité de l'échantillon",
      "famous_problem": "Problème du cygne noir (Nassim Taleb) : avoir vu 1000 cygnes blancs n'exclut pas l'existence d'un cygne noir"
    },
    "ai_ml_connection": "L'apprentissage automatique est fondamentalement inductif : à partir d'exemples d'entraînement, le modèle infère des règles générales. Le risque principal est le surapprentissage (overfitting) — la règle apprise est trop spécifique aux données d'entraînement."
  },
  [
    {"prompt": "Comment distinguer une vraie tendance d'un artefact statistique dans mes données ?", "answer": "Trois tests : (1) Taille d'échantillon — une tendance sur N=5 est fragile, sur N=200 elle est plus solide. (2) Réplication — retrouve-t-on la tendance sur d'autres périodes ou segments ? (3) Mécanisme causal plausible — y a-t-il une raison logique pour que cette relation existe ? Une corrélation sans mécanisme est suspecte. Et si tu peux, teste A/B : c'est le seul vrai test causal."},
    {"prompt": "Dans quel cas utiliser le raisonnement inductif plutôt que déductif ?", "answer": "L'inductif quand tu explores (tu n'as pas encore de règles, tu cherches des patterns dans les données), le déductif quand tu appliques des règles connues à un cas spécifique. En pratique, les deux alternent : induction pour formuler une hypothèse, déduction pour en tirer des prédictions testables, expérimentation pour valider ou réfuter. C'est le cycle scientifique classique."}
  ],
  ["induction", "généralisation", "patterns", "ML", "causalité"]
))

save("professional/engineering/reasoning/abductive_reasoning.json", ku_reas(
  "abductive_reasoning",
  "Raisonnement abductif (inférence à la meilleure explication)",
  "Le raisonnement abductif cherche l'explication la plus simple et la plus probable d'une observation — 'Qu'est-ce qui explique le mieux ce que je vois ?' C'est le raisonnement du diagnostic médical, de la détection de bugs et des enquêtes.",
  "Le raisonnement abductif (ou inférence à la meilleure explication) est une forme de raisonnement qui, partant d'observations, cherche l'hypothèse la plus simple et la plus vraisemblable qui les explique. Contrairement à la déduction, la conclusion est probable mais pas certaine ; contrairement à l'induction, on ne cherche pas une règle générale mais la meilleure explication d'un cas particulier.",
  {
    "abductive_process": [
      "1. Observer un fait surprenant ou un problème",
      "2. Générer des hypothèses explicatives candidates",
      "3. Évaluer chaque hypothèse : simplicité (rasoir d'Occam), vraisemblance, cohérence avec d'autres faits",
      "4. Sélectionner l'hypothèse la plus probable (la meilleure explication)",
      "5. Tester l'hypothèse pour la confirmer ou l'infirmer"
    ],
    "application_domains": [
      {"domain": "Diagnostic médical", "example": "Symptômes → hypothèses de maladies → tests pour confirmer"},
      {"domain": "Debugging", "example": "Erreur → hypothèses de causes → tests isolants"},
      {"domain": "Enquête", "example": "Indices → hypothèses sur les coupables → vérification"},
      {"domain": "Design produit", "example": "Comportement utilisateur inattendu → hypothèses de confusion UX → tests utilisateurs"}
    ],
    "occam_razor": "A hypothèse égale vraisemblance, préférer la plus simple. En debugging : avant de supposer une corruption de mémoire, vérifier d'abord les causes classiques (null, type error, configuration)."
  },
  [
    {"prompt": "Comment ALFRED raisonne-t-il quand il ne comprend pas une demande ?", "answer": "J'utilise l'abduction : quel est l'objectif le plus probable derrière cette demande ? Je génère 2-3 interprétations candidates, j'évalue leur vraisemblance selon le contexte (ce que je sais de toi, le fil de conversation), et je choisis la plus probable. Si j'opte pour une interprétation, je la nomme explicitement : 'Je comprends ça comme X — si je me trompe, corrige-moi.'"},
    {"prompt": "C'est quoi la différence entre l'abduction et la déduction dans le diagnostic d'un problème ?", "answer": "Déduction : tu as la règle et tu arrives à la conclusion ('Si X alors Y, X est vrai, donc Y'). Abduction : tu as seulement la conclusion et tu cherches la règle la plus probable ('Y est observé — quelle règle expliquerait le mieux Y ?'). Le médecin raisonne en abduction : il observe des symptômes et cherche la maladie qui les explique le mieux. Le débogueur passe de l'abduction à la déduction : hypothèse → prédiction de ce qu'on devrait voir si l'hypothèse est vraie → test."}
  ],
  ["abduction", "diagnostic", "meilleure explication", "debugging", "Occam"]
))

save("professional/engineering/reasoning/analogical_reasoning.json", ku_reas(
  "analogical_reasoning",
  "Raisonnement par analogie",
  "Le raisonnement par analogie transfère des structures de raisonnement ou des solutions d'un domaine source connu vers un domaine cible nouveau. C'est une des formes de raisonnement les plus productives pour l'innovation et l'explication.",
  "Le raisonnement analogique est un type d'inférence qui identifie une similitude structurelle entre deux domaines (source et cible) et transfère des propriétés, des solutions ou des insights du domaine source vers le domaine cible.",
  {
    "analogy_structure": {
      "source": "Le domaine connu et bien maîtrisé",
      "target": "Le domaine nouveau à comprendre ou à résoudre",
      "mapping": "La correspondance structurelle entre les éléments des deux domaines",
      "transfer": "Les propriétés ou solutions transférées du source vers le cible"
    },
    "effective_analogies": [
      "Le système immunitaire → firewall réseau (défense, règles de reconnaissance, mémoire des attaques)",
      "Un jardin → une codebase (croissance non contrôlée → dette technique, taille régulière → refactoring)",
      "Une partition musicale → une architecture logicielle (structure formelle + interprétation variable)",
      "Un embouteillage → un goulot d'étranglement système (identification du point de blocage, bypass)"
    ],
    "pitfalls": [
      "Analogie superficielle vs structurelle : ressemblance de surface sans correspondance profonde",
      "Over-extension : pousser l'analogie au-delà de sa zone de validité",
      "Fausse équivalence : traiter des choses similaires comme identiques"
    ],
    "use_in_explanation": "Les analogies sont le meilleur outil d'explication pour des concepts complexes : elles ancrent le nouveau concept dans une structure déjà connue, réduisant la charge cognitive de l'apprentissage."
  },
  [
    {"prompt": "Explique-moi la tokenisation d'un LLM avec une analogie.", "answer": "Imagine que tu lis un texte non pas lettre par lettre, mais en reconnaissant des syllabes et des mots fréquents comme des unités. Un LLM fait la même chose : 'tokenizer' découpe le texte en 'tokens' — unités sub-mots ou mots entiers selon leur fréquence. 'anticonstitutionnellement' → plusieurs tokens. 'le' → un seul token. Le LLM traite et génère token par token, pas caractère par caractère — c'est plus efficace mais explique pourquoi il peut mal compter les lettres dans un mot."},
    {"prompt": "Comment utiliser les analogies pour convaincre des parties prenantes non-techniques ?", "answer": "Trois principes : (1) Choisir une analogie du quotidien de ton interlocuteur (une DRH pense recrutement, pas serveurs), (2) Cartographier explicitement les correspondances ('le CI/CD, c'est comme le contrôle qualité en usine : on vérifie chaque pièce avant l'assemblage'), (3) Pointer les limites de l'analogie pour éviter les malentendus. L'analogie est un pont, pas une définition."}
  ],
  ["analogie", "transfert", "explication", "innovation", "mapping"]
))

save("professional/engineering/reasoning/counterfactual_reasoning.json", ku_reas(
  "counterfactual_reasoning",
  "Raisonnement contrefactuel",
  "Le raisonnement contrefactuel explore ce qui aurait pu se passer si les conditions avaient été différentes — 'Et si...?' C'est un outil puissant pour l'analyse causale, la prise de décision rétrospective et l'anticipation de scénarios alternatifs.",
  "Le raisonnement contrefactuel est une forme de pensée hypothétique qui considère des alternatives à ce qui s'est réellement passé ('si X n'avait pas eu lieu, alors Y ne serait pas arrivé'). Il est central à l'analyse causale, à la responsabilité morale et à l'apprentissage par l'expérience.",
  {
    "counterfactual_applications": [
      {"application": "Analyse post-mortem", "example": "Si on avait ajouté des tests de charge, l'incident de production aurait été détecté en staging"},
      {"application": "XAI (Explainable AI)", "example": "'Votre crédit a été refusé. Si votre revenu avait été 10% plus élevé, il aurait été accordé' — contrefactuel explicatif"},
      {"application": "Décision stratégique", "example": "Si on avait pivotéen 2022, où en serions-nous aujourd'hui ?"},
      {"application": "Apprentissage", "example": "Qu'est-ce qui aurait dû être différent pour obtenir un meilleur résultat ?"}
    ],
    "causal_analysis": "Un contrefactuel causal fort : 'Si X n'avait pas eu lieu, Y n'aurait pas eu lieu.' Cela requiert un modèle causal (graphe DAG) pour raisonner correctement — sans modèle, on peut attribuer à tort une cause à une corrélation.",
    "xai_counterfactuals": "Les contrefactuels sont une des meilleures techniques d'explicabilité IA : ils montrent la 'distance minimale' entre la décision réelle et une décision alternative, rendant la décision IA actionnable pour l'utilisateur."
  },
  [
    {"prompt": "Comment faire une analyse post-mortem efficace avec le raisonnement contrefactuel ?", "answer": "Structure : pour chaque facteur contributeur à l'incident, demander 'si ce facteur avait été absent ou différent, l'incident se serait-il produit ?' Les facteurs dont l'absence aurait empêché l'incident sont les causes nécessaires. Les facteurs qui l'auraient atténué sont les facteurs aggravants. Cette décomposition évite le biais de 'blâmer la cause la plus visible' et identifie les interventions systémiques."},
    {"prompt": "Peut-on utiliser les contrefactuels pour expliquer une décision d'ALFRED ?", "answer": "Oui — c'est une des techniques d'XAI les plus utiles. Plutôt que 'ALFRED a recommandé X parce que...', ALFRED peut dire 'Si tu m'avais donné le contexte Y, j'aurais recommandé Z à la place.' Cela rend la décision compréhensible et actionnable : l'utilisateur sait quoi changer pour obtenir une réponse différente."}
  ],
  ["contrefactuel", "causalité", "XAI", "post-mortem", "scénarios alternatifs"]
))

save("professional/engineering/reasoning/hypothesis_testing.json", ku_reas(
  "hypothesis_testing",
  "Test d'hypothèses (raisonnement scientifique)",
  "Le test d'hypothèses est la méthode scientifique appliquée aux décisions : formuler une hypothèse falsifiable, prédire ce qu'on devrait observer si elle est vraie, tester, et mettre à jour selon les résultats.",
  "Le test d'hypothèses est une méthode de raisonnement empirique dans laquelle une hypothèse explicative est formulée de façon falsifiable, puis testée contre des données ou des expériences. La méthode permet de distinguer les croyances fondées sur des preuves de celles fondées sur des intuitions.",
  {
    "hypothesis_testing_cycle": [
      "1. Observer un phénomène ou identifier une question",
      "2. Formuler une hypothèse H1 (et son alternative nulle H0)",
      "3. Identifier ce qu'on devrait observer SI H1 est vraie",
      "4. Concevoir le test minimal qui distinguerait H1 de H0",
      "5. Collecter les données ou réaliser l'expérience",
      "6. Évaluer : les résultats supportent-ils H1 ou H0 ?",
      "7. Mettre à jour les croyances et formuler de nouvelles hypothèses"
    ],
    "product_application": {
      "A/B_testing": "H0 : la variante B ne change pas la conversion. H1 : B augmente la conversion. Test : exposer 50% des utilisateurs à B, mesurer la différence avec significance statistique (p < 0.05).",
      "feature_validation": "Avant de développer une feature : 'Nous croyons que [feature] pour [users] résultera en [outcome]. Nous le saurons si [metric] change de X%.'",
      "bug_hypothesis": "Bug suspect : 'Je crois que le bug est causé par X. Si oui, le comportement Y devrait changer en Z quand X est isolé.'"
    },
    "falsifiability": "Une bonne hypothèse doit être falsifiable : il doit exister un résultat possible qui la réfuterait. 'Notre produit est bon' n'est pas falsifiable. 'Notre NPS dépasse 40 d'ici Q2' l'est."
  },
  [
    {"prompt": "Comment structurer une hypothèse avant de lancer un A/B test ?", "answer": "Template : 'Nous croyons que [changer X] pour [segment Y] résultera en [amélioration de métrique Z], parce que [raison]. Nous le saurons si [métrique principale] change de [seuil minimum] avec [taille d'échantillon et durée prévues].' La partie 'parce que' est cruciale : tester sans hypothèse causale, c'est du tâtonnement. La partie 'nous le saurons si' définit le critère de succès avant d'analyser, évitant le biais de confirmation."},
    {"prompt": "Comment ALFRED peut m'aider à tester mes hypothèses business ?", "answer": "Je peux t'aider à : (1) formuler l'hypothèse précisément — souvent les hypothèses business sont vagues ou non falsifiables, (2) identifier le test minimal — quelle est l'expérience la plus simple et rapide qui validerait ou invaliderait l'hypothèse ?, (3) anticiper les biais — quels résultats pourraient faussement confirmer l'hypothèse ?, (4) interpréter les résultats — distinguer signal et bruit. Dis-moi l'hypothèse sur laquelle tu travailles."}
  ],
  ["hypothèse", "test", "falsifiabilité", "A/B", "méthode scientifique"]
))

save("professional/engineering/reasoning/mental_model_building.json", ku_reas(
  "mental_model_building",
  "Construction de modèles mentaux",
  "Les modèles mentaux sont des représentations simplifiées de la réalité qui permettent de raisonner, prédire et décider rapidement. Avoir de bons modèles mentaux dans plusieurs domaines (physique, économique, comportemental) est le fondement de la pensée stratégique.",
  "Un modèle mental est une représentation interne simplifiée d'un système ou d'un phénomène, utilisée pour raisonner sur son fonctionnement, prédire ses comportements et prendre des décisions. Les meilleurs décideurs possèdent une grande variété de modèles mentaux issus de disciplines différentes.",
  {
    "key_mental_models": [
      {"model": "Premier principe", "domain": "Épistémologie", "use": "Déconstruire les problèmes jusqu'aux vérités fondamentales, reconstruire depuis zéro (Elon Musk, Aristote)"},
      {"model": "Coût d'opportunité", "domain": "Économie", "use": "Chaque choix exclut d'autres choix — comparer les alternatives aux bénéfices sacrifiés"},
      {"model": "Cercle de compétence", "domain": "Sagesse pratique", "use": "Opérer là où on a une compétence réelle, reconnaître les limites (Buffett)"},
      {"model": "Inversion", "domain": "Logique", "use": "Résoudre par l'inverse : comment garantir l'échec ? Éviter ces erreurs."},
      {"model": "Marge de sécurité", "domain": "Ingénierie/Finance", "use": "Construire des réserves de sécurité par rapport aux prévisions optimistes"},
      {"model": "Effet Dunning-Kruger", "domain": "Psychologie", "use": "Les moins compétents surestiment leurs compétences — calibrer l'incertitude"},
      {"model": "Loi de Goodhart", "domain": "Management", "use": "Quand une mesure devient un objectif, elle cesse d'être une bonne mesure"}
    ],
    "model_acquisition": [
      "Lecture transversale (physique, biologie, économie, psychologie, histoire)",
      "Pratique délibérée : appliquer consciemment les modèles aux situations rencontrées",
      "Débrief après décisions : quel modèle aurait mieux prédit le résultat ?",
      "Dialogue avec des experts de domaines différents"
    ]
  },
  [
    {"prompt": "Quels modèles mentaux sont les plus utiles pour un entrepreneur ?", "answer": "Top 5 pour l'entrepreneuriat : (1) Premier principe — construire des hypothèses depuis les fondamentaux, pas les analogies sectorielles, (2) Coût d'opportunité — chaque feature développée est une feature non-développée, (3) Loi de Goodhart — méfier quand une métrique devient l'objectif (ex: optimiser le taux de clics détruit l'UX), (4) Inversion — 'comment garantir que ce produit échoue ?' pour identifier les risques critiques, (5) Marge de sécurité — toujours construire 2x plus de runway que prévu."},
    {"prompt": "Comment ALFRED m'aide à construire de meilleurs modèles mentaux ?", "answer": "Plusieurs façons : quand tu me poses une question, je peux exposer le modèle mental que j'utilise pour y répondre — ça te permet de l'adopter. Je peux aussi tester tes hypothèses en demandant 'quel modèle sous-tend ce raisonnement ?' et en identifiant les angles morts. Et je peux introduire des modèles de domaines inattendus qui éclairent différemment une situation familière."}
  ],
  ["modèles mentaux", "premier principe", "raisonnement stratégique", "décision", "frameworks"]
))

save("professional/engineering/reasoning/cognitive_bias_awareness.json", ku_reas(
  "cognitive_bias_awareness",
  "Conscience des biais cognitifs",
  "Les biais cognitifs sont des écarts systématiques dans la pensée humaine qui conduisent à des jugements irrationnels. Les identifier ne suffit pas — la désactualisation requiert des systèmes et des process, pas de la volonté.",
  "La conscience des biais cognitifs est la capacité à reconnaître les patterns d'erreur systématique dans la pensée humaine (et dans les LLMs), à comprendre leurs mécanismes, et à mettre en place des contre-mesures processuelles pour atténuer leur impact sur les décisions.",
  {
    "key_cognitive_biases": [
      {"bias": "Biais de confirmation", "description": "Chercher et favoriser les informations qui confirment nos croyances existantes", "counter": "Devil's advocate, red team, recherche active de contre-exemples"},
      {"bias": "Biais de disponibilité", "description": "Surestimer la probabilité des événements facilement rappelables (récents, émotionnels)", "counter": "Statistiques de base rate, éloignement temporel avant décision"},
      {"bias": "Biais d'ancrage", "description": "Être influencé de façon excessive par la première information reçue", "counter": "Générer des estimations indépendantes avant de recevoir des chiffres"},
      {"bias": "Sunk cost fallacy", "description": "Continuer un projet à cause des investissements passés plutôt que des perspectives futures", "counter": "'Si on commençait aujourd'hui avec ce qu'on sait, investirait-on ?'"},
      {"bias": "Dunning-Kruger", "description": "Les novices surestiment leur compétence ; les experts sous-estiment la leur", "counter": "Calibration via feedback externe, tracking des prédictions"},
      {"bias": "Biais de status quo", "description": "Préférer l'état actuel au changement même bénéfique", "counter": "Evaluer le changement vs le statu quo sur les mêmes critères"}
    ],
    "llm_biases": [
      "Biais de sycophanie : tendency à confirmer ce que l'utilisateur semble croire",
      "Biais de récence dans le contexte : surpondérer les informations récentes dans la conversation",
      "Biais de popularité : favoriser les réponses correspondant aux opinions majoritary dans les données d'entraînement"
    ]
  },
  [
    {"prompt": "Comment ALFRED évite-t-il d'amplifier mes biais de confirmation ?", "answer": "Activement : quand je détecte que tu cherches validation plutôt qu'analyse, je te le signale et j'introduis des contre-arguments ou des données contradictoires. Aussi : je génère délibérément la perspective opposée à celle que tu sembles avoir avant de donner mon avis. Et je suis conscient de ma tendance LLM à la sycophanie — si tu presses pour que je confirme une hypothèse, je résiste si les faits vont dans l'autre sens."},
    {"prompt": "Comment éviter le sunk cost dans la décision de stopper un projet ?", "answer": "Question pivot : 'Si on démarrait ce projet aujourd'hui, avec ce qu'on sait, l'investirait-on ?' Si la réponse est non, le sunk cost ne change pas la logique. Technique complémentaire : distinguer les coûts récupérables (actifs, IP) des coûts irrécupérables (temps et énergie passés). Seul le futur est décisionnel. Et demander à quelqu'un d'externe qui n'a pas de stake émotionnel dans le projet — ils ont moins de biais."}
  ],
  ["biais cognitifs", "confirmation", "ancrage", "sunk cost", "Dunning-Kruger"]
))

save("professional/engineering/reasoning/probabilistic_reasoning.json", ku_reas(
  "probabilistic_reasoning",
  "Raisonnement probabiliste",
  "Le raisonnement probabiliste quantifie l'incertitude plutôt que de penser en certitudes absolues. Penser en probabilités, mettre à jour selon les nouvelles preuves (Bayes) et calibrer ses croyances est l'un des upgrades intellectuels les plus puissants.",
  "Le raisonnement probabiliste est la capacité à quantifier l'incertitude, à exprimer les croyances en termes de probabilités, à mettre à jour ces probabilités selon les nouvelles preuves (théorème de Bayes) et à prendre des décisions qui optimisent l'espérance de valeur sous incertitude.",
  {
    "core_concepts": [
      {"concept": "Probabilité bayésienne", "description": "P(A|B) = P(B|A) × P(A) / P(B) — mettre à jour sa croyance sur A à la lumière de la preuve B"},
      {"concept": "Prior vs posterior", "description": "Prior = croyance initiale. Posterior = croyance mise à jour après nouvelle preuve"},
      {"concept": "Base rate", "description": "La fréquence de base d'un événement dans la population générale — souvent négligé (biais de représentativité)"},
      {"concept": "Valeur attendue", "description": "E[X] = Σ (probabilité × résultat) — critère de décision sous incertitude"},
      {"concept": "Calibration", "description": "Quand tu dis '70% de chance', tu devrais avoir raison 70% du temps. Un raisonnement bien calibré est autant utile qu'un raisonnement précis."}
    ],
    "practical_tools": [
      "Fermi estimation : ordres de grandeur, pas fausse précision",
      "Superforecasting (Tetlock) : track record de prédictions, mise à jour fréquente",
      "Scenario planning : pondérer plusieurs futurs plausibles plutôt que prédire un seul",
      "Pré-mortem probabiliste : 'Si dans 2 ans ce projet a échoué, quelle est la cause la plus probable ?'"
    ]
  },
  [
    {"prompt": "Comment utiliser le raisonnement probabiliste pour évaluer une opportunité business ?", "answer": "Framework : (1) identifier les hypothèses critiques (market size, taux de conversion, CAC), (2) donner une fourchette de probabilité à chaque hypothèse (pessimiste/base/optimiste), (3) calculer la valeur attendue sur plusieurs scénarios pondérés, (4) identifier quelle hypothèse a le plus d'impact sur le résultat — la tester en priorité. Évite le modèle financier en une seule ligne — montre la distribution, pas le chiffre central."},
    {"prompt": "Peux-tu m'expliquer le biais des taux de base avec un exemple concret ?", "answer": "Exemple médical classique : un test détecte une maladie rare avec 99% de précision. Tu testes positif. Quelle est la probabilité que tu sois malade ? Intuition : 99%. Réalité probabiliste : ça dépend du taux de base. Si la maladie touche 1 personne sur 10000, 9999 personnes saines et 1 malade passent le test. Les 9999 saines génèrent ~100 faux positifs. L'une des ~101 personnes positives est vraiment malade → probabilité réelle ~1%. La leçon : toujours ancrer les probabilités dans le taux de base de la population testée."}
  ],
  ["probabilités", "Bayes", "incertitude", "calibration", "valeur attendue"]
))

save("professional/engineering/reasoning/structured_problem_decomposition.json", ku_reas(
  "structured_problem_decomposition",
  "Décomposition structurée des problèmes",
  "Décomposer un problème complexe en sous-problèmes indépendants (ou MECE) permet de le rendre traçable, de paralléliser le travail et de ne rien oublier. La décomposition est la première étape de tout raisonnement structuré.",
  "La décomposition structurée des problèmes est la technique analytique qui consiste à diviser un problème complexe en parties plus petites, exhaustives et mutuellement exclusives (principe MECE), permettant une analyse systématique et une résolution progressive.",
  {
    "mece_principle": {
      "M": "Mutually Exclusive — les catégories ne se recoupent pas",
      "CE": "Collectively Exhaustive — toutes les catégories ensemble couvrent l'ensemble du problème",
      "value": "Un découpage MECE évite les doublons dans l'analyse et garantit qu'aucun aspect n'est oublié"
    },
    "decomposition_methods": [
      {"method": "Issue tree", "description": "Arbre de décomposition hiérarchique — chaque nœud se décompose en sous-questions MECE", "use": "Consulting, analyse stratégique"},
      {"method": "5 Pourquoi", "description": "Décomposition causale — suivre la chaîne causale jusqu'à la cause racine", "use": "RCA (Root Cause Analysis), debugging"},
      {"method": "Fishbone / Ishikawa", "description": "Décomposition par catégories de causes (Homme, Méthode, Machine, Matière, Milieu, Mesure)", "use": "Qualité, manufacturing, incidents"},
      {"method": "Divide and conquer algorithmique", "description": "Décomposer jusqu'aux cas de base résoluble, combiner les solutions", "use": "Algorithmique, coding"},
      {"method": "Jobs To Be Done", "description": "Décomposer le besoin utilisateur en jobs fonctionnels, émotionnels, sociaux", "use": "Product management"}
    ]
  },
  [
    {"prompt": "Comment décomposer le problème 'notre taux de churn est trop élevé' ?", "answer": "Issue tree MECE : (1) Par moment du churn (onboarding J0-J30 vs long-terme J30+), (2) Par segment (B2B vs B2C, ou taille entreprise), (3) Par raison déclarée (qualité produit vs prix vs concurrent vs manque d'utilisation). Pour chaque branche : quelle est la métrique et quelle est la donnée disponible pour la mesurer ? On résout en identifiant le segment qui contribue le plus au churn total — l'itération qui a le plus d'impact."},
    {"prompt": "Quelle méthode utiliser pour décomposer un bug difficile ?", "answer": "Les 5 Pourquoi pour la cause racine : 'Le service est lent' → Pourquoi ? → 'Les requêtes DB prennent 10s' → Pourquoi ? → 'Index manquant' → Pourquoi ? → 'Pas de process de review de migration' → Pourquoi ? → 'Pas de checklist de déploiement'. La cause racine est souvent un manque de process, pas un bug technique isolé. Fix sur la cause racine (checklist) plutôt que seulement sur le symptôme (ajouter l'index)."}
  ],
  ["décomposition", "MECE", "issue tree", "5 pourquoi", "problem solving"]
))

save("professional/engineering/reasoning/first_principles_thinking.json", ku_reas(
  "first_principles_thinking",
  "Pensée par premiers principes",
  "La pensée par premiers principes consiste à déconstruire un problème jusqu'aux vérités fondamentales non dérivables d'ailleurs, puis à reconstruire une solution depuis ces fondamentaux — en ignorant les conventions et analogies du secteur.",
  "La pensée par premiers principes est une méthode de raisonnement qui consiste à identifier les fondements irréductibles d'un problème (les vérités qui ne peuvent pas être divisées davantage), puis à reconstruire une compréhension ou une solution depuis ces fondamentaux, sans être contraint par les conventions existantes.",
  {
    "how_to_apply": [
      "1. Identifier la croyance ou la contrainte à remettre en question",
      "2. Décomposer jusqu'aux fondamentaux : 'Pourquoi est-ce vrai ?' répété jusqu'à la vérité irréductible",
      "3. Identifier ce qui est une convention vs ce qui est une contrainte physique/logique réelle",
      "4. Reconstruire depuis les fondamentaux en ignorant les conventions",
      "5. Évaluer la solution résultante contre les solutions conventionnelles"
    ],
    "examples": [
      {"context": "Elon Musk / batteries", "convention": "'Les batteries sont trop chères — elles coûtent X€/kWh'", "first_principle": "Quels sont les éléments chimiques d'une batterie ? Quel est leur coût au marché des commodités ? → Coût théorique << prix du marché → efficacité de production est le levier"},
      {"context": "Architecture logicielle", "convention": "'On a toujours utilisé une base SQL pour ce type d'application'", "first_principle": "Quelles sont les vraies contraintes ? Volume de données, patterns d'accès, cohérence requise, budget ? → Peut-être un graph DB ou une solution event-sourcing est plus adapté"}
    ],
    "contrast_with_analogy": "La pensée par analogie raisonne par comparaison à l'existant ('c'est comme X, donc on fait comme X a fait'). Elle est efficace mais conservatrice. La pensée par premiers principes remet tout en question — plus lente mais source d'innovation non-incrémentale."
  },
  [
    {"prompt": "Comment appliquer la pensée par premiers principes à la conception d'ALFRED ?", "answer": "Convention : 'Un assistant IA, c'est une interface chat.' Premier principe : pourquoi chat ? Parce que le texte est le mode d'échange le plus riche et le plus universellement lisible. Mais est-ce vrai dans tous les contextes ? Pour un assistant ambiant, la voix est plus naturelle. Pour des données complexes, la visualisation est plus efficace. En partant des premiers principes (les besoins réels de l'utilisateur), on arrive à un assistant multimodal contextuel — pas juste une box de chat."},
    {"prompt": "Quelle différence entre premier principe et innovation incrémentale ?", "answer": "L'innovation incrémentale améliore ce qui existe — elle optimise. Elle est rapide, faible risque, prévisible. La pensée par premiers principes peut tout remettre en question — elle est plus lente, plus risquée, mais seule capable de sauts non-incrémentaux. Tesla n'a pas amélioré la voiture thermique — elle l'a reconstruite depuis 'se déplacer d'un point A à un point B efficacement'. Pour l'exécution quotidienne : incrémental. Pour les paris stratégiques majeurs : premiers principes."}
  ],
  ["premiers principes", "innovation", "fondamentaux", "déconstruction", "Elon Musk"]
))

save("professional/engineering/reasoning/systems_thinking.json", ku_reas(
  "systems_thinking",
  "Pensée systémique",
  "La pensée systémique analyse les comportements émergents des systèmes complexes — boucles de rétroaction, délais, stocks et flux. Elle révèle pourquoi les interventions intuitives échouent souvent ou produisent des effets pervers.",
  "La pensée systémique est une approche d'analyse qui considère les systèmes comme des ensembles de composants interconnectés dont les comportements émergent des interactions plutôt que des propriétés individuelles. Elle identifie les boucles de rétroaction, les délais et les leviers d'intervention non-obvieux.",
  {
    "systems_archetypes": [
      {"archetype": "Fixes qui échouent", "pattern": "Une solution rapide atténue le symptôme mais renforce la cause racine à long terme", "example": "Ajouter des serveurs (symptôme) sans optimiser le code (cause) → dette qui croît"},
      {"archetype": "Dérive vers des buts plus bas", "pattern": "Sous pression, on ajuste le but plutôt que les actions pour l'atteindre", "example": "Baisser les standards de qualité quand les deadlines sont serrées"},
      {"archetype": "Escalade", "pattern": "Deux acteurs répondent chacun à l'action de l'autre — la spirale monte", "example": "Guerre des prix entre concurrents"},
      {"archetype": "Limites à la croissance", "pattern": "Une boucle de renforcement positive heurte une contrainte non-évidente", "example": "Croissance utilisateurs → problèmes de scaling → expérience dégradée → frein à la croissance"}
    ],
    "feedback_loops": [
      {"type": "Renforcante (R)", "description": "Le changement amplifie lui-même (croissance exponentielle, vicious circles)", "example": "Plus d'utilisateurs → plus de données → meilleur modèle → plus d'utilisateurs (effet réseau)"},
      {"type": "Équilibrante (B)", "description": "Le système cherche à maintenir un équilibre, s'oppose au changement", "example": "Budget dépensé → réduction des dépenses → budget stabilisé"}
    ]
  },
  [
    {"prompt": "Pourquoi ajouter plus de personnes à un projet en retard le retarde encore plus ?", "answer": "Loi de Brooks — un exemple classique de pensée systémique. Ajouter des personnes : (1) augmente la complexité de communication (N personnes = N×(N-1)/2 canaux), (2) les anciens membres consacrent du temps à former les nouveaux (perte de productivité court terme), (3) les nouvelles personnes ont besoin de temps pour être productives. Les boucles de rétroaction s'additionnent dans le mauvais sens à court terme. La solution systémique : simplifier l'architecture pour réduire les dépendances inter-personnes, pas ajouter des personnes."},
    {"prompt": "Comment identifier les leviers d'un système complexe ?", "answer": "Selon Donella Meadows ('Thinking in Systems') : les leviers les plus puissants sont (1) changer les règles du système, (2) changer les objectifs du système, (3) changer le paradigme (les croyances qui créent le système). Les moins puissants sont les nombres et les paramètres — pourtant c'est là qu'on intervient le plus souvent. Un exemple : diminuer le taux d'intérêt est un paramètre. Changer la conception de la valeur actionnaire est un paradigme."}
  ],
  ["pensée systémique", "boucles de rétroaction", "complexité", "effets pervers", "Meadows"]
))

save("professional/engineering/reasoning/decision_under_uncertainty.json", ku_reas(
  "decision_under_uncertainty",
  "Décision sous incertitude",
  "Les décisions importantes se prennent toujours sous incertitude. Les frameworks de décision (expected value, regret minimization, robustesse) permettent de raisonner rigoureusement même quand l'information est incomplète.",
  "La prise de décision sous incertitude est la discipline qui permet d'évaluer et de choisir entre des options quand les probabilités et les résultats futurs ne sont pas connus avec certitude, en utilisant des critères rigoureux adaptés au niveau d'incertitude et aux enjeux.",
  {
    "decision_frameworks": [
      {"framework": "Expected Value (EV)", "when": "Risque faible, décisions répétées", "method": "EV = Σ(probabilité × valeur). Choisir l'option avec le plus haut EV.", "limit": "Ignore la variance — mauvais pour les risques catastrophiques"},
      {"framework": "Minimax regret", "when": "Incertitude élevée, décision unique", "method": "Minimiser le regret maximum possible si le pire scénario se réalise (Amazon — 'regretter de ne pas avoir essayé')", "limit": "Peut conduire à trop de risque"},
      {"framework": "Robustesse", "when": "Incertitude sur les scénarios eux-mêmes", "method": "Choisir l'option qui performe correctement dans le plus grand nombre de scénarios plausibles", "limit": "Peut être très conservateur"},
      {"framework": "Optionalité", "when": "Très haute incertitude, horizon long", "method": "Préférer les options qui gardent les possibilités ouvertes et limitent les coûts de retour arrière", "limit": "Ne pas décider coûte aussi (coût d'opportunité)"}
    ],
    "reversibility_heuristic": "Jeff Bezos : distinguer les décisions Type 1 (irréversibles, à très haute conséquence — aller lentement) des décisions Type 2 (réversibles, moins conséquentes — aller vite et corriger en chemin). La plupart des décisions quotidiennes sont Type 2 mais traitées comme Type 1."
  },
  [
    {"prompt": "Comment choisir entre deux options business quand l'incertitude est très élevée ?", "answer": "Je recommande le framework optionalité + robustesse : laquelle des deux options garde le plus de portes ouvertes si tes hypothèses se révèlent fausses ? Et laquelle performe raisonnablement dans tous tes scénarios (même le pessimiste) ? Si une option est meilleure sur EV mais catastrophique dans un scénario plausible, méfiance — l'EV seule est trompeuse pour les décisions uniques à fort enjeu."},
    {"prompt": "ALFRED peut-il prendre des décisions à ma place ?", "answer": "Non — et ce n'est pas le rôle d'ALFRED. Je peux structurer ton raisonnement décisionnel : identifier les options, clarifier les critères, quantifier les incertitudes, modéliser les scénarios. Mais la décision reste la tienne — tu as accès à des informations de contexte, des valeurs et des préférences que je ne maîtrise pas. Le bon usage : ALFRED rend le raisonnement explicite et rigoureux, tu décides."}
  ],
  ["décision", "incertitude", "expected value", "robustesse", "optionalité"]
))

save("professional/engineering/reasoning/metacognition.json", ku_reas(
  "metacognition",
  "Métacognition — penser sur sa propre pensée",
  "La métacognition est la capacité à observer, évaluer et réguler son propre processus de pensée. Elle permet de détecter ses propres erreurs de raisonnement, de calibrer ses croyances et d'améliorer ses processus de décision.",
  "La métacognition est la capacité cognitive à prendre sa propre pensée comme objet d'observation et d'analyse — à surveiller la qualité de son raisonnement, à détecter ses limites et ses biais, et à ajuster ses stratégies cognitives en conséquence.",
  {
    "metacognitive_skills": [
      {"skill": "Monitoring", "description": "Observer son propre raisonnement en temps réel — 'Est-ce que je raisonne bien ici ?'"},
      {"skill": "Évaluation", "description": "Évaluer la qualité de son raisonnement après coup — 'Où ai-je mal raisonné ?'"},
      {"skill": "Calibration", "description": "Aligner sa confiance avec sa compétence réelle — 'Suis-je aussi sûr que je le pense ?'"},
      {"skill": "Stratégie", "description": "Choisir les bons outils de pensée pour la tâche — 'Quelle approche est la plus adaptée ?'"}
    ],
    "metacognition_practices": [
      "Journaling de décisions : noter les décisions importantes, les raisonnements, les prédictions → les réévaluer après les résultats",
      "Pré-mortem : avant une décision, imaginer qu'elle a échoué et identifier pourquoi",
      "Double-check du raisonnement : reformuler l'argument dans d'autres termes pour tester sa solidité",
      "Tracking des prédictions : noter les prédictions chiffrées et les vérifier (superforecasting)"
    ],
    "alfred_metacognitive_support": "ALFRED peut servir de 'miroir métacognitif' : en demandant à l'utilisateur d'expliciter son raisonnement, il rend visible ce qui est implicite et permet de détecter les sauts logiques, les hypothèses non vérifiées et les biais."
  },
  [
    {"prompt": "Comment développer ma métacognition ?", "answer": "Trois pratiques concrètes : (1) Journaling de décisions — note tes décisions importantes et le raisonnement, prédit les résultats, réévalue dans 3/6 mois. C'est le plus puissant feedback loop sur ta propre pensée. (2) Thinking out loud avec ALFRED — verbaliser un raisonnement le rend visible et détectable. (3) Pré-mortem systématique avant les décisions importantes — force à chercher les angles morts. La métacognition est une compétence qui se développe avec la pratique délibérée, pas par accident."},
    {"prompt": "Comment ALFRED peut m'aider à mieux penser ?", "answer": "Pas en pensant à ta place — mais en étant un partenaire de raisonnement. Quand tu travailles sur un problème avec moi, l'acte de le verbaliser te force à le structurer. Je peux questionner les hypothèses implicites ('sur quelle base tu affirmes X ?'), pointer les sauts logiques ('comment tu passes de A à B ?'), et introduire des contre-exemples ('et dans le cas où Y ?'). C'est du coaching cognitif, pas de la délégation."}
  ],
  ["métacognition", "pensée sur la pensée", "calibration", "biais", "coaching cognitif"]
))

# =============================================================================
# professional / product_management / advanced (5 premiers)
# =============================================================================

save("professional/product_management/advanced/jobs_to_be_done.json", ku_pm(
  "jobs_to_be_done",
  "Jobs To Be Done (JTBD)",
  "Le framework Jobs To Be Done dit que les utilisateurs 'embauchent' un produit pour accomplir un 'job' (fonctionnel, émotionnel ou social). Comprendre le vrai job évite de construire des features inutiles et révèle les vrais concurrents.",
  "Le framework Jobs To Be Done (JTBD) est une théorie de l'innovation produit qui postule que les utilisateurs n'achètent pas des produits mais 'embauchent' des produits pour accomplir des jobs spécifiques — des progrès qu'ils cherchent à réaliser dans leur vie. Comprendre le job (fonctionnel, émotionnel et social) permet de concevoir des solutions véritablement centrées sur l'utilisateur.",
  {
    "job_dimensions": [
      {"dimension": "Fonctionnel", "description": "La tâche pratique à accomplir", "example": "Aller du point A au point B (Uber)"},
      {"dimension": "Émotionnel", "description": "Le ressenti que l'utilisateur veut avoir (ou éviter)", "example": "Se sentir autonome et non-dépendant des transports en commun"},
      {"dimension": "Social", "description": "Comment l'utilisateur veut être perçu par les autres", "example": "Paraître professionnel en arrivant en voiture plutôt qu'à pied"}
    ],
    "jtbd_interview_technique": {
      "goal": "Comprendre la situation qui a déclenché l'achat ou l'utilisation",
      "questions": [
        "Raconte-moi la journée où tu as décidé d'utiliser/acheter [produit]",
        "Qu'est-ce qui te frustrait avant ? Qu'est-ce que tu essayais d'accomplir ?",
        "Qu'est-ce qui t'a poussé à chercher une solution ce jour-là spécifiquement ?",
        "Qu'est-ce que tu as essayé avant ? Pourquoi ce n'était pas suffisant ?"
      ]
    },
    "jtbd_vs_features": "Feature thinking : 'Les utilisateurs veulent une meilleure batterie.' JTBD thinking : 'Les utilisateurs veulent rester connectés tout au long de leur journée sans anxiété.' La solution peut être une meilleure batterie, un mode économie, des notifications de batterie, ou des chargeurs accessibles — le JTBD ouvre l'espace de solutions.",
    "competitive_insight": "Le vrai concurrent d'un produit JTBD n'est pas toujours le concurrent évident : le concurrent de Snickers est un autre snack, pas une autre barre chocolatée. Le concurrent de Zoom réunion est parfois un email bien rédigé."
  },
  [
    {"prompt": "Comment appliquer JTBD à la conception d'ALFRED ?", "answer": "Le job d'ALFRED n'est pas 'avoir un assistant IA' — c'est 'accomplir plus de ce qui compte pour moi sans me perdre dans la complexité ou l'énergie cognitive.' Fonctionnel : accéder à la bonne information au bon moment. Émotionnel : se sentir moins seul dans les décisions complexes, moins débordé. Social : être perçu comme quelqu'un d'organisé et de réfléchi. Chaque feature d'ALFRED devrait servir un de ces jobs."},
    {"prompt": "Comment conduire une interview JTBD avec un utilisateur ?", "answer": "Structure en 4 temps : (1) Contexte — 'Raconte-moi la situation qui t'a poussé à utiliser [produit] pour la première fois', (2) Struggle — 'Qu'est-ce que tu essayais d'accomplir ? Qu'est-ce qui te bloquait ?', (3) Search — 'Comment tu as trouvé [produit] ? Qu'est-ce que tu avais essayé avant ?', (4) Outcome — 'Maintenant que tu l'utilises, qu'est-ce qui a changé ?'. Ne pas poser de questions sur les features souhaitées — creuser les jobs et les frustrations."}
  ],
  ["JTBD", "user research", "innovation", "product design", "concurrence"]
))

save("professional/product_management/advanced/continuous_discovery.json", ku_pm(
  "continuous_discovery",
  "Continuous Discovery (Teresa Torres)",
  "La Continuous Discovery est la pratique de conduire des interviews utilisateurs régulières (au moins hebdomadaires) tout en développant le produit, pour s'assurer que les opportunités identifiées correspondent à de vrais besoins utilisateurs.",
  "La Continuous Discovery est une pratique de product management développée par Teresa Torres consistant à maintenir un rythme constant de recherche utilisateur (au moins une interview par semaine par équipe produit) intégré au cycle de développement, pour détecter les opportunités et valider les hypothèses en continu plutôt qu'en phase projet séparée.",
  {
    "opportunity_solution_tree": {
      "description": "Outil central de la Continuous Discovery — arbre qui relie l'outcome visé aux opportunités identifiées et aux solutions possibles",
      "structure": ["Outcome business → Besoins utilisateurs (opportunités) → Solutions possibles → Expériences de validation"],
      "principle": "Séparer clairement la découverte d'opportunités de la génération de solutions — évite de sauter trop vite aux solutions"
    },
    "interview_rhythm": {
      "frequency": "Au moins 1 interview par semaine par équipe produit",
      "participants": "Équipe produit complète (PM + designer + ingénieur) — pas uniquement le PM",
      "format": "Entretiens semi-structurés de 30-45 min, centrés sur des situations récentes (pas des opinions)",
      "capture": "Story mapping des témoignages, pas de notes linéaires"
    },
    "assumption_testing": "Pour chaque solution envisagée, identifier les hypothèses critiques (celles qui rendraient la solution inutile si elles étaient fausses) et les tester avec les expériences les plus légères possibles avant de développer."
  },
  [
    {"prompt": "Comment mettre en place la Continuous Discovery dans une petite équipe ?", "answer": "Minimum viable : 1 interview utilisateur par semaine, toute l'équipe participe en rotation. Script simple : 'Raconte-moi la dernière fois que tu as eu ce problème.' Capture les opportunités (frustrations, besoins) dans une liste partagée. Revue hebdomadaire de 30 min pour identifier les patterns. L'objectif n'est pas la quantité de données mais la régularité du contact avec les utilisateurs réels."},
    {"prompt": "Comment ALFRED pourrait utiliser la Continuous Discovery dans son propre développement ?", "answer": "Ironie productive : ALFRED lui-même est un outil de collecte de feedback en continu — les conversations avec l'utilisateur (Céline) sont des données de discovery. Ce que tu me demandes, ce avec quoi tu luttes, ce que tu reformules — tout ça est un signal produit. La Continuous Discovery d'ALFRED se fait dans chaque échange : identifier les frustrations exprimées, les besoins non satisfaits, les workarounds que tu fais toi-même."}
  ],
  ["continuous discovery", "Teresa Torres", "interviews", "opportunity tree", "user research"]
))

save("professional/product_management/advanced/activation_retention_metrics.json", ku_pm(
  "activation_retention_metrics",
  "Métriques d'activation et rétention",
  "L'activation mesure si un nouvel utilisateur atteint son 'aha moment' — le moment où il comprend la valeur du produit. La rétention mesure s'il revient. Ces deux métriques sont plus prédictives du succès à long terme que l'acquisition.",
  "Les métriques d'activation et de rétention mesurent respectivement la capacité d'un produit à faire vivre sa promesse de valeur aux nouveaux utilisateurs (activation) et à les faire revenir régulièrement (rétention). Elles sont des indicateurs avancés de la croissance durable, contrairement aux métriques d'acquisition.",
  {
    "activation_framework": {
      "aha_moment": "L'instant où l'utilisateur comprend et expérimente la valeur core du produit",
      "examples": [
        "Slack : envoyer 2000 messages en équipe",
        "Dropbox : télécharger un fichier depuis un deuxième appareil",
        "Twitter : suivre 30 comptes pertinents"
      ],
      "finding_aha_moment": "Comparer les comportements J0-J7 des utilisateurs actifs à 30 jours vs les churners. Quel comportement précoce corrèle le plus avec la rétention ?",
      "activation_rate": "% d'utilisateurs qui atteignent le aha moment dans les X jours après inscription"
    },
    "retention_curves": [
      {"type": "D1/D7/D30/D90", "description": "% d'utilisateurs encore actifs 1/7/30/90 jours après inscription", "benchmark": "D30 > 20% = bon pour la plupart des B2C; > 40% pour B2B"},
      {"type": "Rétention par cohorte", "description": "Comparer les courbes de rétention par groupe d'inscription dans le temps — voir si les cohortes récentes retiennent mieux"},
      {"type": "Rétention sur 'smiling curve'", "description": "Baisse rapide puis plateau — le plateau indique les utilisateurs qui ont trouvé la valeur core"}
    ]
  },
  [
    {"prompt": "Comment trouver le aha moment de mon produit ?", "answer": "Analyse de rétention différentielle : prendre les utilisateurs actifs à D30 et les churners de J0-J7, regarder leurs actions J0-J7, identifier l'action qui différencie le plus les deux groupes. C'est souvent une combinaison d'actions (fréquence + type) plutôt qu'une seule action. Valider en A/B testant : guider les nouveaux utilisateurs vers cette action et mesurer si la rétention D30 s'améliore."},
    {"prompt": "Quelle métrique prioriser : activation ou rétention ?", "answer": "Dépend du stade. Early stage : prioriser la rétention — si les utilisateurs ne reviennent pas, aucune acquisition ne compensera. Growth stage : quand la rétention est établie (plateau stable), travailler l'activation pour améliorer le % qui y arrivent. En pratique : regarder d'abord la courbe de rétention. Si elle s'aplatit à > 20%, c'est bon — travailler l'activation. Si elle continue de descendre vers 0, il y a un problème de product-market fit — la rétention prime."}
  ],
  ["activation", "rétention", "aha moment", "métriques", "croissance"]
))

save("professional/product_management/advanced/growth_loops.json", ku_pm(
  "growth_loops",
  "Growth Loops — boucles de croissance virales",
  "Les growth loops sont des boucles de rétroaction auto-alimentées où les utilisateurs existants génèrent des nouveaux utilisateurs (via partage, création de contenu, ou effets réseau) — créant une croissance organique qui ne dépend pas de la dépense publicitaire.",
  "Un growth loop est un mécanisme systémique dans lequel l'utilisation d'un produit par des utilisateurs existants génère de l'exposition ou de la valeur pour de nouveaux utilisateurs potentiels, créant une boucle de croissance auto-entretenue qui augmente en force avec le nombre d'utilisateurs.",
  {
    "growth_loop_types": [
      {"type": "Viral loop", "mechanism": "Un utilisateur invite ou expose le produit à d'autres", "example": "Dropbox — invite → 2Go de stockage bonus pour chaque ami invité qui s'inscrit"},
      {"type": "Content loop", "mechanism": "Les utilisateurs créent du contenu qui attire d'autres utilisateurs", "example": "YouTube — créateurs uploadent des vidéos → vues non-connectées → inscription"},
      {"type": "SEO loop", "mechanism": "Les interactions utilisateurs génèrent du contenu indexable", "example": "Quora — questions-réponses indexées sur Google → trafic organique → nouveaux utilisateurs"},
      {"type": "Network effect loop", "mechanism": "Le produit est plus valuable avec plus d'utilisateurs", "example": "LinkedIn — plus de connexions → meilleur recrutement → plus d'entreprises → plus d'offres → plus d'utilisateurs"}
    ],
    "loop_vs_funnel": {
      "funnel": "Linéaire : acquisition → activation → rétention → revenue. Chaque étape perd des utilisateurs. Dépend de l'injection externe (publicité).",
      "loop": "Cyclique : les utilisateurs actuels alimentent la prochaine cohorte. Croissance exponentielle si le coefficient viral > 1."
    },
    "viral_coefficient": "K = nb_invitations_par_utilisateur × taux_de_conversion. Si K > 1 : croissance exponentielle. Si K < 1 : croissance mais dépend de l'acquisition externe."
  },
  [
    {"prompt": "Est-ce qu'ALFRED peut avoir un growth loop ?", "answer": "Oui — plusieurs mécanismes possibles : (1) Sharing loop : si les réponses d'ALFRED sont partageables (et que les personnes qui les reçoivent veulent accéder au même service), (2) Content loop : si les utilisateurs d'ALFRED produisent des articles/analyses avec l'aide d'ALFRED et que ces contenus mentionnent ALFRED, (3) Recommendation loop : un utilisateur satisfait recommande ALFRED à ses proches. Le loop le plus naturel pour un assistant personnel : le bouche-à-oreille qualifié."},
    {"prompt": "Comment calculer si mon produit a un vrai viral loop ?", "answer": "Mesurer K = (invitations envoyées par utilisateur actif) × (taux de conversion invitation → inscription). Si K = 0.5 : pour 100 utilisateurs, 50 nouveaux entrent via invitation. Si K = 1.2 : croissance organique exponentielle sans dépense publicitaire. Attention : K > 1 est rare — la plupart des produits ont K < 0.5 et dépendent de l'acquisition payante pour alimenter la boucle."}
  ],
  ["growth loop", "viralité", "coefficient viral", "effets réseau", "croissance organique"]
))

save("professional/product_management/advanced/cross_functional_collaboration.json", ku_pm(
  "cross_functional_collaboration",
  "Collaboration cross-fonctionnelle en product management",
  "Le PM travaille à l'intersection de l'ingénierie, du design, du business et de l'opérationnel. La collaboration cross-fonctionnelle efficace repose sur des rituels clairs, un ownership défini et une communication adaptée à chaque audience.",
  "La collaboration cross-fonctionnelle en product management est la capacité du PM à aligner et coordonner les contributions de disciplines différentes (engineering, design, data, business, support, legal) vers un objectif produit commun, en gérant les différences de langage, de priorités et de modes de travail.",
  {
    "cross_functional_challenges": [
      {"challenge": "Langages différents", "description": "L'ingénieur parle technique, le business parle ROI, le design parle expérience", "solution": "Traduire systématiquement entre langages — le PM est interprète"},
      {"challenge": "Priorités divergentes", "description": "Legal veut la compliance, engineering veut la dette technique, sales veut les features clients", "solution": "Critères de priorité partagés et transparents (impact × effort × stratégie)"},
      {"challenge": "Dépendances non gérées", "description": "Une feature dépend d'une autre équipe sans que l'engagement soit formalisé", "solution": "Matrice de dépendances, OKRs d'équipe avec dépendances visibles"},
      {"challenge": "Décisions par consensus vs décision", "description": "Attendre que tout le monde soit d'accord → paralysie", "solution": "RACI clair : qui Responsible, Accountable, Consulted, Informed"}
    ],
    "pm_cross_functional_practices": [
      "One-pager produit partagé : une seule source de vérité pour la vision, les objectifs et les contraintes",
      "Sprint review ouvert à toutes les parties prenantes",
      "Slack/canaux thématiques par initiative — pas par équipe",
      "Roadmap partagée avec les hypothèses explicites (pas juste les dates)"
    ]
  },
  [
    {"prompt": "Comment aligner l'ingénierie et le business sur les priorités produit ?", "answer": "Deux pratiques clés : (1) Traduire les besoins business en problèmes techniques compréhensibles (et vice versa) — ne pas laisser les deux camps parler des langues différentes, (2) Critères de priorité co-construits : une session de scoring partagé (impact utilisateur + effort technique + valeur business) où les deux équipes contribuent. Le PM facilite, ne décide pas seul. Les décisions co-construites ont beaucoup plus d'adhérence."},
    {"prompt": "Comment gérer les désaccords entre design et engineering sur la faisabilité ?", "answer": "Séparer le 'quoi' du 'comment' : le design définit le comportement attendu et l'expérience utilisateur cible, l'engineering définit les contraintes techniques et les options d'implémentation. Le PM facilite la convergence vers la solution qui maximise la valeur utilisateur dans les contraintes techniques réelles. Si désaccord persiste : prototyper la version technique minimale et tester avec de vrais utilisateurs — les données tranchent mieux que les opinions."}
  ],
  ["collaboration", "cross-fonctionnel", "PM", "engineering", "RACI", "alignement"]
))

print("\nBatch 9 Reasoning (15) + PM/Advanced (5 premiers) : DONE")
