"""
Enrichissement day3 — professional/engineering/reasoning/ (15 KU)
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
            "domain": "professional", "subdomain": "reasoning", "status": "validated",
            "metadata": meta(), "priority": priority, "summary": summary,
            "core_definition": core_def, "knowledge": knowledge, "example_answers": examples,
            "response_guidance": guidance, "tags": tags, "related_knowledge_units": []}

save("professional/engineering/reasoning/contradiction_detection.json", ku(
    "knowledges.professional.engineering.reasoning.contradiction_detection",
    "Détection de contradictions — identifier les incohérences dans un raisonnement",
    "high",
    "Méthodes pour repérer les contradictions logiques, factuelles ou contextuelles dans un discours, un document ou une conversation — compétence clé pour le fact-checking et la qualité du raisonnement.",
    "La détection de contradictions est la capacité à identifier des assertions mutuellement incompatibles dans un ensemble d'informations — qu'elles soient explicites (A et non-A) ou implicites (deux faits dont l'un invalide l'autre).",
    {"types": {"logique": "P et non-P simultanément vrais — violation de la loi de non-contradiction", "factuelle": "Deux faits qui ne peuvent coexister (\"il était à Paris et Tokyo le même jour\")", "temporelle": "Chronologie impossible (\"avant de commencer X, j'ai terminé X\")", "valeurs": "Principe affirmé et comportement incompatible"},
     "methodes": {"matrice": "Lister les assertions et croiser pour détecter les incompatibilités", "timeline": "Reconstruire la chronologie pour détecter les impossibilités", "hypothese_unique": "Chercher l'hypothèse qui rendrait toutes les assertions vraies — si impossible, contradiction"},
     "biais_cognitifs_associes": {"compartimentalisation": "Tenir des croyances contradictoires dans des contextes séparés", "motivated_reasoning": "Ignorer les contradictions qui menacent une conclusion voulue"},
     "en_pratique": "Dans ALFRED : détecter quand une demande contredit une décision précédente, ou quand une information contredit les données de contexte connues."},
    [{"prompt": "Comment vérifier qu'un argument est cohérent ?", "answer": "Trois étapes : 1) Isoler les affirmations clés. 2) Vérifier qu'aucune n'implique la négation d'une autre. 3) Chercher si les prémisses mènent réellement à la conclusion. La contradiction la plus fréquente : une conclusion qui dépasse ce que les prémisses permettent d'affirmer."},
     {"prompt": "Tu as dit X et maintenant tu dis le contraire.", "answer": "Tu as raison de le signaler. Laisse-moi vérifier : [X] et [Y] — est-ce qu'ils se contredisent vraiment ou s'appliquent-ils à des contextes différents ? Si c'est une vraie contradiction, je me suis trompé et je corrige."}],
    {"tone": "rigoureux, factuel, non-défensif", "structure": ["identifier", "analyser", "résoudre"], "avoid": ["défensivité", "ignorer le signal", "sur-complexifier"]},
    ["contradiction", "logique", "cohérence", "raisonnement", "fact-checking"]
))

save("professional/engineering/reasoning/fallback_reasoning.json", ku(
    "knowledges.professional.engineering.reasoning.fallback_reasoning",
    "Raisonnement de repli — que faire quand les données manquent",
    "high",
    "Stratégies pour raisonner de manière fiable quand l'information est incomplète, ambiguë ou absente. Inclut heuristiques, estimations raisonnées et gestion de l'incertitude.",
    "Le raisonnement de repli (fallback reasoning) désigne l'ensemble des stratégies cognitives activées quand les données nécessaires à un raisonnement complet sont indisponibles, permettant d'aboutir à une conclusion ou une action raisonnable malgré l'incertitude.",
    {"strategies": {"estimation_fermi": "Décomposer un problème inconnu en sous-problèmes estimables", "analogie": "Appliquer le raisonnement d'un cas connu à un cas inconnu", "pire_meilleur_cas": "Borner l'incertitude par les extrêmes pour décider malgré tout", "prior_bayesien": "Partir de la distribution de base et ajuster selon les indices disponibles"},
     "quand_s_arreter": "Savoir quand l'incertitude est trop grande pour décider — et le dire explicitement plutôt que de forcer une réponse",
     "declaration_d_incertitude": {"format": "\"Je ne sais pas X avec certitude, mais voici ce que je peux estimer : [raisonnement]\"", "calibration": "Ne pas surconfier une estimation — donner une fourchette réaliste"},
     "erreurs": ["Forcer une réponse précise quand seule une fourchette est honnête", "Appliquer une analogie sans vérifier sa pertinence", "Ignorer les données disponibles par excès de prudence"]},
    [{"prompt": "Je n'ai pas toutes les informations pour décider.", "answer": "Qu'est-ce qui manque exactement ? Souvent on peut distinguer l'information qui change vraiment la décision de celle qui serait juste confortable à avoir. Si l'info manquante est critique : attendre ou demander. Si elle n'est pas critique : décider avec ce qu'on a en nommant l'incertitude."},
     {"prompt": "Comment estimer quelque chose qu'on ne connaît pas ?", "answer": "Approche Fermi : décomposer en éléments qu'on peut estimer séparément, puis multiplier. Exemple — estimer le marché des livraisons de pizza en France : population × foyers × fréquence × part qui commande. Chaque estimation est imprécise, mais le produit converge souvent vers un ordre de grandeur utile."}],
    {"tone": "méthodique, honnête sur les limites", "structure": ["stratégie", "application", "limites"], "avoid": ["fausse précision", "refus de raisonner", "ignorer l'incertitude"]},
    ["incertitude", "estimation", "fallback", "Fermi", "raisonnement", "données manquantes"]
))

save("professional/engineering/reasoning/goal_alignment_reasoning.json", ku(
    "knowledges.professional.engineering.reasoning.goal_alignment_reasoning",
    "Raisonnement d'alignement des objectifs — vérifier la cohérence moyens-fins",
    "high",
    "Méthode pour s'assurer que les actions choisies mènent réellement aux objectifs visés — et détecter quand les moyens dérivient de la fin.",
    "Le raisonnement d'alignement des objectifs est le processus de vérification continue que les actions, ressources et décisions d'un système ou d'un acteur restent cohérentes avec les objectifs déclarés, en détectant les dérives et les substitutions d'objectifs (goal displacement).",
    {"concepts_cles": {"goal_displacement": "Quand le moyen devient la fin (optimiser le KPI au lieu de l'objectif réel)", "proximal_vs_distal": "Objectif immédiat (proximal) vs objectif final (distal) — aligner les deux", "criteria_drift": "Les critères de succès changent sans que l'objectif change — signal d'alarme"},
     "verification": {"backward_chaining": "\"Cet objectif proximal mène-t-il vraiment à l'objectif distal ?\"", "stakeholder_check": "Demander à chaque partie si elle comprend l'objectif de la même manière", "result_vs_activity": "Mesurer les résultats, pas seulement les activités"},
     "en_pratique_alfred": "Quand une demande arrive, vérifier si l'action demandée mène vraiment au besoin réel — pas juste à la formulation de la demande."},
    [{"prompt": "On fait beaucoup de réunions mais rien n'avance.", "answer": "C'est un signal classique de goal displacement : les réunions sont devenues la fin plutôt que le moyen. Question clé : chaque réunion produit-elle une décision, une action ou une information qui n'existait pas avant ? Si non, la réunion est une activité sans résultat. On peut refaire le design : moins de réunions, plus de livrables clairs avec owners et deadlines."},
     {"prompt": "Comment savoir si ce qu'on fait mène vraiment où on veut aller ?", "answer": "Backward chaining : partir de l'objectif final et remonter. \"Pour atteindre Z, il faut Y. Pour Y, il faut X. Est-ce qu'on fait vraiment X ?\" Souvent on découvre qu'on fait X' qui ressemble à X mais ne produit pas vraiment Y."}],
    {"tone": "stratégique, orienté résultats", "structure": ["concept", "vérification", "application"], "avoid": ["théorie sans exemple", "liste sans structure"]},
    ["objectifs", "alignement", "goal displacement", "stratégie", "KPI", "cohérence"]
))

save("professional/engineering/reasoning/hallucination_detection.json", ku(
    "knowledges.professional.engineering.reasoning.hallucination_detection",
    "Détection des hallucinations LLM — identifier et vérifier les confabulations",
    "critical",
    "Les LLM génèrent parfois des informations plausibles mais fausses (hallucinations). Savoir les détecter, les vérifier et les prévenir est essentiel pour une utilisation fiable de l'IA.",
    "Une hallucination LLM est une sortie générée qui est factuellement incorrecte, inventée ou non soutenue par les données d'entraînement, mais présentée avec le même degré de confiance qu'une information vraie. Elles sont particulièrement dangereuses car elles sont souvent syntaxiquement parfaites et stylistiquement convaincantes.",
    {"types": {"fabrication_factuelle": "Dates, chiffres, citations, noms inventés", "fabrication_de_references": "Articles, livres, URLs qui n'existent pas", "extrapolation": "Généralisations excessives depuis des données partielles", "confabulation_contextuelle": "Inventer des détails pour combler des lacunes du contexte"},
     "signaux_d_alerte": ["Références très précises (auteur, date, page) sur des sujets rares", "Cohérence interne parfaite mais non vérifiable", "Réponse trop rapide et trop complète à une question complexe", "Manque de \"je ne sais pas\""],
     "verification": {"sources_primaires": "Vérifier directement dans la source originale", "cross_check": "Confronter plusieurs sources indépendantes", "requete_inverse": "Demander au LLM de citer ses sources — l'absence ou la vague réponse est un signal"},
     "prevention": {"grounding": "Fournir les sources dans le prompt (RAG)", "temperature_basse": "Réduit la variabilité mais pas toujours les hallucinations", "self_consistency": "Poser la même question de plusieurs façons — les réponses incohérentes signalent l'incertitude"}},
    [{"prompt": "Comment savoir si tu inventes quelque chose ?", "answer": "Bonne question à me poser. Signaux à surveiller : si je cite des sources très précises sur un sujet obscur, si ma réponse est trop parfaite, si je n'exprime aucune incertitude sur un sujet qui devrait en générer. La règle générale : pour toute information factuelle importante (chiffres, citations, références), vérifier dans la source primaire. Je peux me tromper."},
     {"prompt": "Les LLM hallucinent beaucoup ?", "answer": "Ça dépend du type de tâche. Sur des tâches de raisonnement ou de structure : faible taux d'erreur. Sur des faits précis, surtout rares ou récents : taux d'hallucination significatif. Les références bibliographiques sont particulièrement risquées — les LLM \"inventent\" des articles plausibles. La bonne pratique : traiter les sorties LLM comme un brouillon à vérifier sur les faits critiques, pas comme une source primaire."}],
    {"tone": "transparent, factuel, orienté vérification", "structure": ["définir", "détecter", "vérifier"], "avoid": ["nier ses propres limites", "sur-promettre la fiabilité"]},
    ["hallucination", "LLM", "IA", "fact-checking", "fiabilité", "confabulation"]
))

save("professional/engineering/reasoning/memory_reasoning_links.json", ku(
    "knowledges.professional.engineering.reasoning.memory_reasoning_links",
    "Liens mémoire-raisonnement — comment la mémoire structure le raisonnement",
    "medium",
    "La mémoire et le raisonnement sont interdépendants : la mémoire fournit les prémisses, le raisonnement les utilise et les enrichit. Comprendre cette relation améliore la gestion de la connaissance.",
    "Les liens entre mémoire et raisonnement décrivent comment les différents systèmes de mémoire (de travail, épisodique, sémantique, procédurale) alimentent les processus de raisonnement, et comment le raisonnement encode de nouveaux souvenirs et modifie les représentations existantes.",
    {"systemes_memoire": {"travail": "Mémoire active — 4±1 chunks simultanément — limite directe du raisonnement complexe", "episodique": "Souvenirs d'événements vécus — contexte et exemples pour le raisonnement", "semantique": "Connaissances générales — prémisses du raisonnement déductif", "procedurale": "Savoir-faire — raisonnement implicite et automatique"},
     "limites_memoire_travail": {"impact_raisonnement": "Un raisonnement avec trop d'étapes dépasse la capacité — nécessite externalisation", "strategies": ["Écrire les étapes intermédiaires", "Chunking", "Utiliser des représentations visuelles (arbres, diagrammes)"]},
     "consolidation": "Le raisonnement consolide la mémoire — raisonner activement sur une information la mémorise mieux que la relire",
     "alfred_context": "ALFRED maintient un contexte de session (mémoire de travail étendue) et peut rappeler des éléments de sessions précédentes (mémoire épisodique) pour enrichir le raisonnement."},
    [{"prompt": "Pourquoi j'oublie mon raisonnement en milieu de processus ?", "answer": "La mémoire de travail a une capacité limitée — 4 éléments environ simultanément. Pour un raisonnement en plusieurs étapes, si tu ne notes pas les intermédiaires, ils s'écrasent. Solution : externaliser sur papier ou écran les étapes déjà faites pour libérer la mémoire de travail pour la suivante."},
     {"prompt": "Comment mémoriser quelque chose que je veux retenir longtemps ?", "answer": "Raisonner dessus plutôt que de le relire. La question \"pourquoi c'est vrai ?\" ou \"où est-ce que ça s'applique ?\" force un traitement actif qui encode bien mieux que la relecture passive. Combiner avec espacement (révision à J+1, J+7, J+30) pour la consolidation à long terme."}],
    {"tone": "cognitif, pédagogique", "structure": ["mécanisme", "limites", "stratégies"], "avoid": ["trop abstrait", "jargon sans définition"]},
    ["mémoire", "raisonnement", "mémoire de travail", "consolidation", "cognition"]
))

save("professional/engineering/reasoning/meta_reasoning_basics.json", ku(
    "knowledges.professional.engineering.reasoning.meta_reasoning_basics",
    "Méta-raisonnement — raisonner sur son propre raisonnement",
    "high",
    "La capacité à évaluer la qualité de son propre processus de raisonnement, à détecter ses biais et à choisir la stratégie adaptée à chaque problème.",
    "Le méta-raisonnement est le processus par lequel un agent évalue et régule son propre raisonnement : choix de la stratégie, détection des erreurs en cours, évaluation de la confiance dans les conclusions, et décision d'allouer plus ou moins de ressources cognitives à un problème.",
    {"composantes": {"monitoring": "Surveiller la progression du raisonnement — \"est-ce que je vais dans la bonne direction ?\"", "controle": "Décider de changer de stratégie si nécessaire", "calibration": "Évaluer correctement son niveau de certitude", "allocation": "Décider quand approfondir et quand s'arrêter"},
     "biais_a_detecter": {"overconfidence": "Se sentir certain sans le vérifier", "confirmation": "Chercher uniquement ce qui confirme", "sunk_cost": "Continuer un raisonnement erroné parce qu'on y a investi du temps", "premature_closure": "Conclure trop vite par anxiété de l'incertitude"},
     "pratiques": {"question_test": "\"Comment est-ce que je saurais si je me trompe ?\"", "devil_advocate": "Chercher activement les arguments contre sa propre conclusion", "calibration_check": "\"Sur une échelle de 0-100, à quel point suis-je sûr ?\" puis vérifier"}},
    [{"prompt": "Comment savoir si mon raisonnement est bon ?", "answer": "Trois questions à se poser : 1) \"Comment est-ce que je saurais si j'ai tort ?\" — si tu ne peux pas répondre, ton raisonnement n'est pas falsifiable. 2) \"Ai-je cherché les contre-arguments aussi sérieusement que les arguments ?\" 3) \"Mon niveau de confiance est-il justifié par les preuves ou par l'envie d'avoir raison ?\""},
     {"prompt": "Je me retrouve souvent à avoir tort alors que j'étais sûr.", "answer": "C'est de l'overconfidence — très commun, très humain. Ce qui aide : développer l'habitude de donner une probabilité à ses conclusions (\"je suis sûr à 80%\") plutôt qu'un binaire certain/incertain. Ça force l'introspection sur la vraie qualité des preuves, et ça permet de calibrer en comparant les prédictions aux résultats."}],
    {"tone": "réflexif, rigoureux, non-moralisateur", "structure": ["définir", "détecter", "pratiquer"], "avoid": ["académique sans application", "culpabiliser les erreurs"]},
    ["méta-cognition", "raisonnement", "biais", "calibration", "confiance", "épistémologie"]
))

save("professional/engineering/reasoning/multi_agent_reasoning.json", ku(
    "knowledges.professional.engineering.reasoning.multi_agent_reasoning",
    "Raisonnement multi-agents — coordination et division du travail cognitif",
    "medium",
    "Comment plusieurs agents (humains ou IA) peuvent diviser et coordonner un raisonnement complexe pour dépasser les limites individuelles, avec les défis de cohérence et d'intégration.",
    "Le raisonnement multi-agents désigne les systèmes dans lesquels plusieurs agents autonomes collaborent à un processus de raisonnement commun, en se répartissant les sous-problèmes, en partageant les conclusions intermédiaires et en intégrant les résultats.",
    {"architectures": {"parallelisation": "Agents travaillant simultanément sur des sous-problèmes indépendants", "pipeline": "Agent A produit pour Agent B qui produit pour Agent C — séquentiel", "debate": "Agents qui argumentent des positions opposées — un juge intègre", "mixture_of_experts": "Spécialistes sur des domaines, un router qui choisit"},
     "defis": {"coherence": "S'assurer que les conclusions des agents sont cohérentes entre elles", "communication": "Le format de transmission des conclusions intermédiaires est critique", "integration": "Comment combiner des raisonnements partiels en conclusion globale", "conflit": "Gérer quand deux agents arrivent à des conclusions opposées"},
     "applications": {"code_review": "Un agent génère, un autre critique", "fact_checking": "Un agent affirme, un autre vérifie les sources", "planification": "Un agent planifie, un autre simule les obstacles"},
     "alfred_context": "ALFRED peut orchestrer des sous-tâches de raisonnement et intégrer les résultats, ou travailler en coordination avec d'autres outils."},
    [{"prompt": "Comment fonctionne un système multi-agents ?", "answer": "Simplement : plusieurs agents IA (ou humains + IA) se répartissent un problème. Chacun travaille sur sa partie, les résultats sont intégrés. L'avantage : parallélisation et spécialisation. Le défi : la cohérence des interfaces entre agents est souvent le point de défaillance. En pratique, un agent orchestrateur qui distribue et intègre est plus robuste qu'une coordination décentralisée."},
     {"prompt": "Deux IA donnent des réponses contradictoires, laquelle croire ?", "answer": "Ni l'une ni l'autre sans vérification. Les contradictions entre LLM révèlent une zone d'incertitude — et c'est utile. Pour arbitrer : chercher la source primaire, vérifier laquelle cite des données plus récentes ou plus pertinentes, ou poser la question en demandant à chacun de justifier avec des sources. La contradiction est une invitation à investiguer, pas une réponse."}],
    {"tone": "technique, accessible", "structure": ["architecture", "défis", "applications"], "avoid": ["trop abstrait", "jargon LLM sans contexte"]},
    ["multi-agents", "IA", "orchestration", "coordination", "raisonnement distribué"]
))

save("professional/engineering/reasoning/probabilistic_reasoning_basics.json", ku(
    "knowledges.professional.engineering.reasoning.probabilistic_reasoning_basics",
    "Raisonnement probabiliste — penser en termes de probabilités",
    "high",
    "Raisonner avec des probabilités plutôt que des certitudes : biais courants, règle de Bayes, calibration et applications pratiques à la décision sous incertitude.",
    "Le raisonnement probabiliste est la capacité à quantifier et manipuler l'incertitude de manière cohérente, en utilisant des probabilités pour représenter des degrés de croyance et en les mettant à jour en fonction de nouvelles preuves (théorème de Bayes).",
    {"concepts_fondamentaux": {"probabilite_subjective": "Degré de croyance dans une proposition — pas une fréquence objective", "prior": "Probabilité avant de voir de nouvelles données", "likelihood": "Probabilité des données sachant l'hypothèse", "posterior": "Probabilité après mise à jour avec les données (Bayes)"},
     "biais_frequents": {"base_rate_neglect": "Ignorer la fréquence de base — erreur classique dans les tests médicaux", "conjunction_fallacy": "P(A et B) < P(A) — mais les gens pensent souvent le contraire", "availability_bias": "Surestimer la probabilité d'événements récents ou frappants"},
     "calibration": {"bien_calibre": "Quand on dit \"70% certain\", ça arrive 70% du temps", "pratique": "Tenir un journal de prédictions et vérifier la calibration"},
     "applications": ["Évaluation du risque", "Diagnostic médical", "Décision d'investissement", "Évaluation des preuves judiciaires"]},
    [{"prompt": "C'est quoi raisonner en probabilités ?", "answer": "C'est remplacer \"je suis sûr\" par \"je suis sûr à 85%\" — et traiter cette différence comme réelle. En pratique : avant de décider, estimer la probabilité des scénarios pertinents. Après avoir vu de nouvelles informations, mettre à jour ces probabilités. L'erreur la plus commune : ignorer la fréquence de base (ex : un test positif pour une maladie rare est souvent faux positif, même avec un bon test)."},
     {"prompt": "Je dois évaluer si un projet va réussir.", "answer": "Approche probabiliste : 1) Quel est le taux de base de succès pour ce type de projet ? 2) Quels facteurs spécifiques augmentent ou diminuent cette probabilité ici ? 3) Quels sont les 2-3 risques qui causeraient l'échec — et quelle est leur probabilité ? Ce n'est pas une réponse binaire, c'est une distribution."}],
    {"tone": "rigoureux, accessible, concret", "structure": ["concept", "biais à éviter", "application"], "avoid": ["formules sans intuition", "trop abstrait"]},
    ["probabilités", "Bayes", "incertitude", "calibration", "biais cognitifs", "décision"]
))

save("professional/engineering/reasoning/reasoning_failure_patterns.json", ku(
    "knowledges.professional.engineering.reasoning.reasoning_failure_patterns",
    "Patterns d'échec du raisonnement — erreurs systématiques à connaître",
    "high",
    "Les erreurs de raisonnement les plus fréquentes et dangereuses : sophismes, biais, pièges logiques. Les reconnaître chez soi et chez les autres est une compétence critique.",
    "Les patterns d'échec du raisonnement sont des erreurs systématiques et récurrentes dans le processus de raisonnement, classées en sophismes formels (structure logique invalide), sophismes informels (prémisses problématiques) et biais cognitifs (distorsions systématiques du jugement).",
    {"sophismes_formels": {"ad_hominem": "Attaquer la personne plutôt que l'argument", "pente_glissante": "A mène à B mène à Z sans justifier chaque étape", "homme_de_paille": "Réfuter une version déformée de l'argument adverse", "fausse_dichotomie": "Présenter deux options comme si elles étaient les seules"},
     "sophismes_informels": {"appel_autorite": "L'expert dit X donc X — sans évaluer la pertinence de l'autorité", "appel_popularite": "\"Tout le monde le fait\" comme justification", "petitio_principii": "La conclusion est dans les prémisses"},
     "biais_raisonnement": {"confirmation": "Chercher les preuves qui confirment", "hindsight": "\"Je le savais depuis le début\" post-hoc", "dunning_kruger": "Les moins compétents surestiment le plus leur compétence"}},
    [{"prompt": "Comment reconnaître un mauvais argument ?", "answer": "Trois questions rapides : 1) Est-ce que l'argument attaque la personne ou son idée ? (ad hominem) 2) Les prémisses soutiennent-elles vraiment la conclusion ou fait-on un saut ? 3) Y a-t-il des alternatives ignorées ? Les sophismes sont souvent émotionnellement convaincants et logiquement vides — la rhétorique peut faire passer n'importe quoi."},
     {"prompt": "Je remarque que je justifie souvent mes décisions après coup.", "answer": "C'est le biais de hindsight combiné à du motivated reasoning. Ce qui aide : noter les raisons d'une décision AVANT de connaître le résultat, puis comparer après. La différence entre ce qu'on pensait avant et ce qu'on dit après révèle l'ampleur du biais."}],
    {"tone": "analytique, sans condescendance", "structure": ["taxonomie", "exemples", "détection"], "avoid": ["académique pur", "lister sans expliquer"]},
    ["sophismes", "biais cognitifs", "raisonnement", "logique", "pensée critique"]
))

save("professional/engineering/reasoning/reasoning_orchestration.json", ku(
    "knowledges.professional.engineering.reasoning.reasoning_orchestration",
    "Orchestration du raisonnement — coordonner des raisonnements complexes",
    "high",
    "Comment structurer et séquencer des raisonnements complexes impliquant plusieurs étapes, sources ou agents pour aboutir à des conclusions fiables et traçables.",
    "L'orchestration du raisonnement est la capacité à concevoir et piloter un processus de raisonnement en plusieurs étapes, en déterminant l'ordre optimal des opérations, les points de vérification, les conditions de branchement et les mécanismes d'intégration des résultats intermédiaires.",
    {"schemas_d_orchestration": {"sequential": "Chaque étape prend le résultat de la précédente — simple mais fragile aux erreurs early", "parallel": "Étapes indépendantes exécutées simultanément — puis intégration", "conditional": "Le chemin dépend des résultats intermédiaires — adaptatif", "iteratif": "Raffinement progressif jusqu'à convergence"},
     "points_cles": {"checkpoints": "Vérifier la qualité à chaque étape avant de passer à la suivante", "rollback": "Pouvoir revenir en arrière si une étape produit un résultat invalide", "transparence": "Tracer les étapes pour auditabilité", "timeout": "Définir quand arrêter si la convergence n'est pas atteinte"},
     "en_pratique_alfred": "ALFRED orchestre : compréhension de la demande → recherche en mémoire → génération → vérification de cohérence → réponse. Chaque étape peut influencer les suivantes."},
    [{"prompt": "Comment structurer un raisonnement compliqué sans se perdre ?", "answer": "D'abord décomposer le problème en sous-questions indépendantes. Ensuite identifier les dépendances (A doit être résolu avant B). Traiter séquentiellement les dépendances, en parallèle ce qui est indépendant. Et écrire les conclusions intermédiaires — pas les garder en tête. Un raisonnement complexe qui reste dans la tête rate à cause de la mémoire de travail, pas de la capacité."},
     {"prompt": "Qu'est-ce qu'un pipeline de raisonnement dans une IA ?", "answer": "C'est la séquence d'opérations qu'un système IA exécute pour passer d'une entrée à une sortie. Exemple simple : parse la question → identifie l'intention → cherche le contexte pertinent → génère une réponse → vérifie la cohérence. Chaque étape a ses propres critères de qualité. Un bug dans le pipeline peut venir de n'importe quelle étape — d'où l'importance de tracer et de tester chaque étape séparément."}],
    {"tone": "technique, structuré", "structure": ["schéma", "points clés", "application concrète"], "avoid": ["trop théorique", "ignorer les contraintes pratiques"]},
    ["orchestration", "raisonnement", "pipeline", "IA", "séquençage", "coordination"]
))

save("professional/engineering/reasoning/retrieval_augmented_reasoning.json", ku(
    "knowledges.professional.engineering.reasoning.retrieval_augmented_reasoning",
    "RAG — Retrieval-Augmented Generation et raisonnement augmenté",
    "critical",
    "Comment le RAG améliore le raisonnement des LLM en ancrant les réponses dans des sources vérifiables, avec les mécanismes, les avantages et les limites de l'approche.",
    "Le Retrieval-Augmented Generation (RAG) est une architecture qui augmente les capacités d'un LLM en récupérant dynamiquement des informations pertinentes depuis une base de connaissances externe avant la génération, permettant des réponses plus précises, actualisées et vérifiables.",
    {"architecture": {"retriever": "Cherche les documents les plus pertinents pour la question (similarité vectorielle, BM25, hybride)", "reranker": "Classe les résultats du retriever par pertinence fine avant de les passer au LLM", "generator": "LLM qui génère la réponse en conditionnant sur les documents récupérés", "grounding": "Ancrage : la réponse est liée aux sources récupérées"},
     "avantages": ["Réduction des hallucinations", "Actualité (sources mises à jour sans ré-entraînement)", "Auditabilité (on peut voir quelles sources ont été utilisées)", "Domaine-spécifique sans fine-tuning"],
     "limites": ["Qualité dépend de la qualité des sources", "Le retriever peut rater les documents pertinents", "Le LLM peut ignorer ou mal interpréter les documents", "Latence augmentée"],
     "alfred_rag": "ALFRED utilise le RAG sur sa knowledge base : les KU sont indexés, la question de l'utilisateur trigge la recherche, les KU pertinents sont injectés dans le contexte avant génération."},
    [{"prompt": "C'est quoi le RAG et pourquoi c'est important ?", "answer": "RAG = Retrieval-Augmented Generation. Au lieu de répondre uniquement depuis sa mémoire d'entraînement, le LLM cherche d'abord les informations pertinentes dans une base de données, puis génère la réponse en s'appuyant sur ces documents. L'avantage principal : les réponses sont ancrées dans des sources vérifiables et peuvent être actualisées sans ré-entraîner le modèle. C'est ce qu'utilise ALFRED pour répondre depuis sa knowledge base."},
     {"prompt": "Pourquoi ALFRED utilise des fichiers JSON plutôt que de tout garder dans le LLM ?", "answer": "Trois raisons : 1) La knowledge base peut être mise à jour, enrichie et vérifiée indépendamment du modèle. 2) Les connaissances sont traçables — on sait exactement d'où vient chaque réponse. 3) La précision augmente quand le LLM a accès aux bons documents — il hallucine moins quand il est ancré dans un contexte vérifiable."}],
    {"tone": "technique mais accessible, contextualisé ALFRED", "structure": ["architecture", "avantages", "limites", "ALFRED context"], "avoid": ["trop abstrait", "acronymes sans explication"]},
    ["RAG", "retrieval", "LLM", "knowledge base", "grounding", "ALFRED", "IA"]
))

save("professional/engineering/reasoning/self_consistency_reasoning.json", ku(
    "knowledges.professional.engineering.reasoning.self_consistency_reasoning",
    "Auto-cohérence du raisonnement — vérifier ses propres conclusions",
    "high",
    "Technique qui génère plusieurs chaînes de raisonnement indépendantes sur le même problème et sélectionne la conclusion la plus fréquente — réduit les erreurs aléatoires du raisonnement.",
    "L'auto-cohérence (self-consistency) est une technique de raisonnement qui consiste à générer plusieurs trajectoires de raisonnement indépendantes pour le même problème, puis à sélectionner la réponse par vote majoritaire, en s'appuyant sur le principe que les erreurs aléatoires divergent tandis que les réponses correctes convergent.",
    {"principe": "Les erreurs de raisonnement sont souvent aléatoires (bruit) — si on raisonne plusieurs fois indépendamment, les bonnes réponses convergent et les erreurs s'annulent",
     "application_llm": {"chain_of_thought_multiple": "Générer N chaînes de raisonnement différentes (temperature > 0)", "vote": "La conclusion la plus fréquente est la plus robuste", "confiance": "La proportion de votes pour la réponse dominante estime la confiance"},
     "application_humaine": {"deliberation": "Reconsidérer un problème à un autre moment ou sous un autre angle avant de conclure", "peer_review": "Plusieurs personnes raisonnent indépendamment avant de comparer"},
     "limites": ["Ne corrige pas les biais systématiques — si le modèle est biaisé, toutes les trajectoires seront biaisées", "Coûteux en calcul pour les LLM", "Moins efficace si les trajectoires ne sont pas vraiment indépendantes"]},
    [{"prompt": "Comment être plus sûr de mes conclusions ?", "answer": "Raisonne deux fois indépendamment avant de comparer. Après avoir conclu, attends un moment puis reprends le problème à zéro sans relire ta première réponse. Si tu arrives au même endroit, ta confiance est justifiée. Si tu diverges, l'incertitude est réelle et mérite investigation."},
     {"prompt": "Pourquoi les LLM font parfois des erreurs sur des problèmes simples ?", "answer": "Les LLM génèrent de manière probabiliste — même problème, run différent, résultat parfois différent. La technique self-consistency y répond : générer la réponse plusieurs fois et prendre le vote majoritaire. Pour les problèmes critiques, c'est une bonne pratique de demander au modèle d'aborder le problème sous deux angles différents et de voir si les conclusions convergent."}],
    {"tone": "méthodique, concret", "structure": ["principe", "application", "limites"], "avoid": ["trop académique", "ignorer les limites"]},
    ["auto-cohérence", "raisonnement", "LLM", "chain-of-thought", "fiabilité", "vote majoritaire"]
))

save("professional/engineering/reasoning/task_decomposition_reasoning.json", ku(
    "knowledges.professional.engineering.reasoning.task_decomposition_reasoning",
    "Décomposition de tâches — diviser pour raisonner",
    "high",
    "Méthode fondamentale pour rendre les problèmes complexes tractables : décomposer en sous-problèmes indépendants ou séquentiels, résoudre chacun, puis intégrer.",
    "La décomposition de tâches est la stratégie de résolution de problèmes qui consiste à diviser un problème complexe en sous-problèmes plus simples, indépendants ou séquentiels, dont la résolution combinée permet d'aborder le problème original.",
    {"methodes": {"WBS": "Work Breakdown Structure — décomposition hiérarchique jusqu'aux tâches atomiques", "MECE": "Mutuellement Exclusif, Collectivement Exhaustif — sous-problèmes sans overlap ni oubli", "depends_graph": "Graphe de dépendances — identifier ce qui doit être résolu avant quoi"},
     "criteres_bonne_decomposition": ["Chaque sous-problème est plus simple que le tout", "La solution des sous-problèmes permet de résoudre le tout", "Les sous-problèmes sont aussi indépendants que possible"],
     "erreurs_frequentes": ["Décomposer trop finement (micro-management du raisonnement)", "Décomposer selon la structure du problème plutôt que selon les compétences disponibles", "Oublier l'étape d'intégration — les sous-solutions doivent se combiner"],
     "llm_et_decomposition": "Les LLM bénéficient massivement de la décomposition : \"Résous X\" → plus d'erreurs que \"Décompose X en étapes, résous chaque étape\""},
    [{"prompt": "Comment attaquer un projet qui me semble énorme ?", "answer": "Décomposer jusqu'à ce que la plus petite unité soit faisable en 30 min ou moins. Si tu ne sais pas par où commencer la décomposition : commencer par la fin (\"qu'est-ce qui doit exister à la fin ?\") et remonter (\"pour ça il faut Y, pour Y il faut X...\"). Une fois que tu as les briques, les ordonner par dépendances — ce qui bloque tout le reste va en premier."},
     {"prompt": "Mes demandes à une IA donnent des résultats médiocres.", "answer": "Essaie de décomposer ta demande. Au lieu de \"écris-moi un plan de communication\", essaie \"d'abord liste les publics cibles et leurs besoins spécifiques\", puis \"pour chaque public, propose 2-3 messages clés\", puis \"propose un calendrier de diffusion\". Les LLM raisonnent mieux sur des problèmes bornés — la décomposition fait le reste."}],
    {"tone": "structurant, concret, pragmatique", "structure": ["méthode", "critères", "erreurs", "pratique IA"], "avoid": ["trop théorique", "MECE sans exemple"]},
    ["décomposition", "tâches", "WBS", "MECE", "problème complexe", "planification", "LLM"]
))

save("professional/engineering/reasoning/tree_of_thoughts.json", ku(
    "knowledges.professional.engineering.reasoning.tree_of_thoughts",
    "Tree of Thoughts — exploration arborescente du raisonnement",
    "medium",
    "Technique de raisonnement qui explore plusieurs branches de pensée en parallèle, évalue leur promesse et choisit le meilleur chemin — comme un joueur d'échecs qui calcule plusieurs coups à l'avance.",
    "Le Tree of Thoughts (ToT) est une technique de raisonnement qui structure l'exploration du problème comme un arbre où chaque nœud est un état intermédiaire du raisonnement, les branches sont les continuations possibles, et un processus d'évaluation détermine quelles branches poursuivre.",
    {"structure": {"noeud": "État du raisonnement à un moment donné", "branche": "Continuation possible — une direction de pensée", "evaluation": "Évaluer la promesse de chaque branche avant d'aller plus loin", "pruning": "Abandonner les branches peu prometteuses tôt"},
     "vs_chain_of_thought": {"CoT": "Raisonnement linéaire — une seule chaîne", "ToT": "Raisonnement arborescent — plusieurs chemins explorés en parallèle"},
     "applications": {"problemes_creatifs": "Explorer plusieurs angles créatifs avant d'en développer un", "planification": "Évaluer plusieurs plans avant de s'engager", "debug": "Explorer plusieurs hypothèses de cause avant d'investiguer"},
     "implementation_pratique": "Demander explicitement au LLM : \"Génère 3 approches différentes, évalue chacune, puis développe la meilleure\""},
    [{"prompt": "Comment explorer un problème créatif sans se bloquer sur la première idée ?", "answer": "Tree of Thoughts pratique : générer 3 directions complètement différentes (même si certaines semblent mauvaises), évaluer brièvement chacune sur 2 critères, puis approfondir la plus prometteuse. L'erreur fréquente : évaluer pendant la génération — ça bloque la créativité. D'abord générer, ensuite évaluer."},
     {"prompt": "C'est quoi la différence entre chain-of-thought et tree-of-thoughts ?", "answer": "CoT : je raisonne étape par étape en une ligne droite. ToT : je génère plusieurs branches de raisonnement en parallèle, j'évalue leur promesse, et je poursuis la meilleure (comme aux échecs). ToT est plus robuste sur les problèmes où la première approche n'est pas toujours la bonne — mais plus coûteux en ressources."}],
    {"tone": "technique, imagé", "structure": ["concept", "comparaison CoT", "applications", "pratique"], "avoid": ["mathématique pur", "trop abstrait"]},
    ["tree of thoughts", "raisonnement", "LLM", "exploration", "créativité", "planification"]
))

save("professional/engineering/reasoning/uncertainty_reasoning.json", ku(
    "knowledges.professional.engineering.reasoning.uncertainty_reasoning",
    "Raisonnement sous incertitude — décider sans certitude",
    "high",
    "Cadres et pratiques pour prendre des décisions raisonnables quand l'information est incomplète, les probabilités sont inconnues, ou le contexte est ambigu.",
    "Le raisonnement sous incertitude est l'ensemble des méthodes permettant de structurer la prise de décision dans des contextes où les informations nécessaires sont partielles, les probabilités sont estimées plutôt que connues, et les conséquences sont difficiles à prévoir avec précision.",
    {"types_incertitude": {"risque": "Probabilités connues — casino, assurance", "incertitude_knightienne": "Probabilités inconnues — situations nouvelles", "ambiguite": "Même les options ne sont pas clairement définies", "complexite": "Les variables sont trop nombreuses et interdépendantes"},
     "strategies": {"maximin": "Choisir l'option dont le pire cas est le moins mauvais — stratégie défensive", "maximax": "Choisir l'option dont le meilleur cas est le plus attractif — stratégie offensive", "regret_minimax": "Minimiser le regret maximum possible", "options_preserving": "Préférer les décisions qui gardent des options ouvertes"},
     "pratiques": {"scénarios": "Construire 3 scénarios (pessimiste/réaliste/optimiste) et vérifier que la décision est robuste sur plusieurs", "premortem": "Imaginer que ça a échoué et chercher pourquoi — détecter les risques avant", "reversibilite": "Préférer les décisions réversibles quand l'incertitude est haute"}},
    [{"prompt": "Je dois décider mais je n'ai pas assez d'informations.", "answer": "Deux questions préalables : 1) Quelle information changerait vraiment ta décision si tu l'avais ? Si elle est obtainable, vaut-il le coût de l'attendre ? 2) Quelle est la réversibilité de chaque option ? Sous haute incertitude, préférer les options réversibles même si elles semblent moins bonnes. La premortem est aussi utile : imagine que tu as décidé et que ça a échoué dans 6 mois — qu'est-ce qui a causé l'échec ?"},
     {"prompt": "Comment ne pas regretter une décision prise dans le flou ?", "answer": "En changeant le critère d'évaluation : une bonne décision n'est pas une décision qui a bien tourné, c'est une décision bien prise avec les informations disponibles au moment de la décision. Si tu as suivi un processus raisonnable, la décision était bonne — même si le résultat est mauvais (le résultat dépend aussi du hasard). Tenir ce journal aide à calibrer le processus, pas à ruminer les résultats."}],
    {"tone": "structurant, non-anxiogène", "structure": ["types", "stratégies", "pratiques"], "avoid": ["théorie de la décision pure", "culpabiliser l'incertitude"]},
    ["incertitude", "décision", "risque", "scénarios", "premortem", "réversibilité"]
))

print("\n=== professional/engineering/reasoning : 15 KU sauvegardés ===")
