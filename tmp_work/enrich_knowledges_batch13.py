"""
Enrichissement Knowledge Base ALFRED - Batch 13 : professional restants (16 fichiers)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(domain, subdomain, stem, title, summary, core_def, knowledge, examples, tags, tone="strategique, ancre dans la pratique"):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.{domain}.{subdomain}.{stem}",
      "title": title, "domain": domain, "subdomain": subdomain,
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": tone,
        "structure": ["contextualiser", "expliquer le concept", "proposer un angle actionnable"],
        "avoid": ["trop theorique", "ignorer le contexte"]
      },
      "tags": tags,
      "related_knowledge_units": []
    }

# =============================================================================
# professional / decision
# =============================================================================

save("professional/decision/decision_making.json", ku(
  "professional", "decision", "decision_making",
  "Prise de decision professionnelle",
  "La prise de decision professionnelle combine rigueur analytique (data, criteres explicites) et jugement (experience, intuition calibree). Les meilleures decisions sont celles dont le processus est solide, pas seulement celles dont le resultat est bon.",
  "La prise de decision professionnelle est le processus par lequel un individu ou une organisation identifie les options disponibles, evalue leurs impacts selon des criteres explicites, gere l'incertitude et choisit la voie d'action qui maximise la valeur dans les contraintes donnees.",
  {
    "decision_process": [
      "Definir la decision a prendre (souvent la partie la plus sous-estimee)",
      "Identifier les options (ne pas s'arreter a 2 options)",
      "Definir les criteres de succes et leur poids relatif",
      "Evaluer les options sur chaque critere",
      "Gerer l'incertitude (scenarios, probabilites)",
      "Decider et planifier l'implementation"
    ],
    "decision_types": [
      {"type": "Type 1 (irreversible, fort impact)", "approach": "Ralentir, analyser, impliquer les parties prenantes, consulter", "examples": ["Recruter un cofounder", "Lever des fonds", "Pivoter le produit"]},
      {"type": "Type 2 (reversible, impact limite)", "approach": "Decider vite, experimenter, corriger si besoin", "examples": ["Tester une feature", "Changer un processus interne", "Essayer un nouvel outil"]}
    ],
    "decision_biases": [
      "HIPPO (Highest Paid Person's Opinion) — l'autorite prime sur les donnees",
      "Sunk cost — continuer a cause des investissements passes",
      "Biais de confirmation — chercher les preuves qui confirment l'option preferee",
      "Groupthink — convergence artificielle vers le consensus"
    ]
  },
  [
    {"prompt": "Comment prendre une decision difficile quand les donnees sont insuffisantes ?", "answer": "Quatre etapes : (1) Identifier les hypotheses critiques (celles dont depend le plus le resultat), (2) Evaluer si on peut obtenir des donnees rapidement sur ces hypotheses (test, interview, recherche) — sinon aller a l'etape 3, (3) Estimer les probabilites avec ce qu'on sait (raisonnement bayesien, analogies historiques), (4) Choisir l'option la plus robuste sous l'incertitude (celle qui performe bien meme dans les scenarios pessimistes). Et documenter les hypotheses faites — pour apprendre de la decision plus tard."},
    {"prompt": "ALFRED peut-il m'aider a prendre une decision ?", "answer": "Oui — pas en decidant a ta place, mais en structurant ton processus de decision. Je peux t'aider a : clarifier la vraie decision (souvent differente de celle qu'on croit prendre), identifier les options qu'on n'avait pas envisagees, explicitur les criteres de succes, evaluer les options methodiquement, et reperer les biais qui pourraient biaiser le choix. Le jugement final reste le tien — tu as acces a des contextes et des valeurs que je ne maitrise pas."}
  ],
  ["decision", "processus", "biais", "criteres", "incertitude"]
))

save("professional/decision/prioritization.json", ku(
  "professional", "decision", "prioritization",
  "Priorisation professionnelle",
  "La priorisation professionnelle est l'art de choisir sur quoi concentrer ses ressources limitees pour maximiser l'impact. Elle necessite des criteres explicites, de la discipline pour dire non, et une mise a jour reguliere selon les nouvelles informations.",
  "La priorisation professionnelle est le processus systematique d'allocation des ressources (temps, attention, budget, energie) aux activites qui creent le plus de valeur dans les contraintes donnees, en utilisant des criteres explicites plutot que la reactivite ou la pression sociale.",
  {
    "prioritization_frameworks": [
      {"framework": "Matrice Eisenhower", "criteria": "Urgence x Impact", "use": "Gestion du temps quotidien"},
      {"framework": "RICE/ICE", "criteria": "Impact x Effort (x Confidence x Reach)", "use": "Priorisation produit"},
      {"framework": "MoSCoW", "criteria": "Must/Should/Could/Won't", "use": "Scope projet"},
      {"framework": "OKR alignment", "criteria": "Contribution aux objectifs prioritaires", "use": "Priorisation strategique"},
      {"framework": "Regret minimization", "criteria": "Ce que tu regretteras de ne pas avoir fait dans 10 ans", "use": "Decisions de vie/carriere"}
    ],
    "saying_no": "La priorisation efficace requiert de dire non — explicitement et poliment. Dire 'pas maintenant' est plus honnete que 'j'essaierai'. Un non donne avec le raisonnement est plus respectueux qu'un oui non tenu.",
    "prioritization_review": "Les priorites changent — revue hebdomadaire (qu'est-ce qui a change cette semaine qui devrait faire bouger mes priorites ?) et mensuelle (est-ce que ce qui consomme mon temps correspond a ce qui crée le plus de valeur ?)."
  },
  [
    {"prompt": "Comment decider entre 5 projets importants quand je n'ai le temps que d'en faire 2 ?", "answer": "Matrice de decision explicite : (1) Lister les 5 projets, (2) Definir 3-4 criteres de valeur (impact sur l'objectif principal, urgence, effort necessaire, dependances), (3) Scorer chaque projet sur chaque critere (1-5), ponderer les criteres si necessaire, (4) Les 2 projets avec le score le plus eleve sont les priorites. Et si le resultat ne semble pas juste : identifier quelle intuition est ignoree par les criteres et ajouter ce critere. La matrice ne remplace pas le jugement — elle le rend explicite."},
    {"prompt": "Comment gerer les demandes urgentes qui arrivent sans cesse et perturbent mes priorites ?", "answer": "Trois strategies : (1) Creneaux de 'feux de l'urgence' deja bloques dans l'agenda — absorber les urgences sans perturber le reste, (2) Triage explicite : toute 'urgence' est evaluee sur 'urgent pour qui ? Urgent par rapport a quoi ?' — beaucoup ne le sont pas vraiment, (3) Communication proactive sur tes priorites et ta disponibilite — les gens interrompent moins quand ils savent que tu es sur quelque chose d'important."}
  ],
  ["priorisation", "impact", "urgence", "dire non", "focus"]
))

save("professional/decision/problem_solving.json", ku(
  "professional", "decision", "problem_solving",
  "Resolution de problemes en contexte professionnel",
  "La resolution de problemes professionnels est un processus structure qui va de la definition precise du probleme au diagnostic des causes, a la generation de solutions et a l'implementation rigoureuse. La phase de definition est souvent la plus critique et la plus negligee.",
  "La resolution de problemes professionnels est l'application systematique de methodes analytiques et crEatives pour identifier les causes profondes d'un probleme, generer et evaluer des solutions, et implementer la meilleure option avec un suivi des resultats.",
  {
    "problem_definition": {
      "importance": "Un probleme mal defini genere des solutions a cote du vrai probleme",
      "techniques": [
        "Reformuler en termes d'ecart (situation actuelle vs situation souhaitee)",
        "Distinguer symptome et cause (5 Pourquoi)",
        "Identifier les contraintes (quelles solutions sont hors scope et pourquoi ?)",
        "Quantifier l'enjeu (combien le probleme coute-t-il ?)"
      ]
    },
    "structured_methods": [
      {"method": "Design Thinking", "phases": ["Empathize", "Define", "Ideate", "Prototype", "Test"], "strength": "Centering on user perspective"},
      {"method": "A3 Toyota", "phases": ["Contexte", "Situation actuelle", "Causes racines", "Cibles", "Plan d'action", "Suivi"], "strength": "Disciplined root cause analysis"},
      {"method": "Lean problem solving", "phases": ["Define", "Measure", "Analyze", "Improve", "Control (DMAIC)"], "strength": "Data-driven, reduction of variability"}
    ]
  },
  [
    {"prompt": "Nous avons un probleme recurrent dans notre equipe — les projets prennent toujours plus de temps que prevu. Comment resoudre ?", "answer": "Methode A3 appliquee : (1) Quantifier d'abord (de combien % en moyenne ? Sur quels types de projets ?) — ca definit l'ampleur reelle, (2) Cartographier les causes possibles (estimation initiale trop optimiste ? Scope creep ? Dependances non anticipees ? Interruptions ? Manque de capacite ?), (3) Les 5 Pourquoi sur la cause principale, (4) Solution ciblee : si l'estimation est le probleme, implemnter le cone d'incertitude (multiplier les estimations initiales par 1.5-2x). Si le scope creep, un processus de change request. Si les interruptions, des creneaux proteges."},
    {"prompt": "Comment ALFRED peut aider a resoudre un probleme complexe d'equipe ?", "answer": "Plusieurs roles : (1) Structurer le probleme (aide a formuler le probleme precisement avant de chercher des solutions), (2) Generer des hypotheses de causes qu'on n'aurait pas envisagees, (3) Preparer un atelier de resolution (agenda, questions, outils adaptes), (4) Synthetiser les informations existantes sur le probleme, (5) Evaluer les solutions envisagees sur des criteres explicites. ALFRED ne connait pas le contexte specifique de ton equipe — mais il peut structurer le raisonnement pour que tu et ton equipe arriviez plus vite a la solution."}
  ],
  ["resolution problemes", "A3", "5 pourquoi", "diagnostic", "causes racines"]
))

# =============================================================================
# professional / engineering / ai
# =============================================================================

save("professional/engineering/ai/llm_basics.json", ku(
  "professional", "engineering", "llm_basics",
  "Bases des LLMs (Large Language Models)",
  "Les LLMs sont des reseaux de neurones entraines sur de vastes corpus de texte pour predire le token suivant. Cette architecture simple mene a des capacites emergentes remarquables — mais aussi a des limites systematiques (hallucination, contexte fini, biais).",
  "Un Large Language Model (LLM) est un modele de deep learning base sur l'architecture Transformer, entraine sur de grands corpus de texte pour predire la probabilite du prochain token, et qui developpe en cours d'entrainement des capacites emergentes de comprehension et de generation du langage.",
  {
    "how_llms_work": [
      "Architecture Transformer (Vaswani et al., 2017) : encodage, mecanisme d'attention, decodage",
      "Pretraining : prediction du prochain token sur des milliards de textes",
      "RLHF (Reinforcement Learning from Human Feedback) : alignement sur les preferences humaines",
      "Inference : generation token par token, sampling probabiliste"
    ],
    "llm_capabilities": [
      "Generation de texte fluide et coherent",
      "Comprehension et reponse aux questions",
      "Raisonnement (ameliore par Chain of Thought)",
      "Traduction, resume, classification",
      "Code generation et debugging",
      "Dialogue multi-tour avec memoire de contexte"
    ],
    "llm_limitations": [
      "Hallucination : generation confiante de faits incorrects",
      "Contexte fini (8K-200K tokens selon le modele)",
      "Coupure des connaissances a une date (knowledge cutoff)",
      "Biais des donnees d'entrainement",
      "Pas d'acces aux informations en temps reel (sans outils)"
    ]
  },
  [
    {"prompt": "Comment fonctionnent les LLMs comme toi ?", "answer": "A l'essence : je suis entraine a predire quel token (fragment de mot) a le plus de chance de suivre les tokens precedents, sur des milliards de textes. Cet entrainement simple mene a des capacites emergentes — je 'comprends' le langage, je 'raisonne', je 'cree'. Mais ces guillemets sont importants : je ne pense pas comme un humain, je genere des sequences statistiquement plausibles. Mes 'connaissances' sont les patterns observes dans mes donnees d'entrainement. Mes erreurs viennent d'extrapolations incorrectes ou de donnees manquantes ou biaisees."},
    {"prompt": "Quelle difference entre GPT-4, Claude, Llama et Mistral ?", "answer": "Quatre familles principales : (1) GPT-4/GPT-4o (OpenAI) : le plus connu, fort en code et raisonnement, via API ou ChatGPT, (2) Claude (Anthropic) : focus securite et alignement, tres bon en analyse longue et raisonnement ethique, (3) Llama 3 (Meta) : open source, peut tourner en local via Ollama, bon rapport qualite/taille, (4) Mistral (Mistral AI, francais) : modeles efficaces et open source, tres bon rapport performance/taille. Pour ALFRED : Ollama avec Mistral ou Llama 3 pour l'execution locale, Claude ou GPT-4 pour les taches necessitant le maximum de qualite."}
  ],
  ["LLM", "transformer", "IA", "ChatGPT", "Claude", "Ollama"]
))

save("professional/engineering/ai/rag.json", ku(
  "professional", "engineering", "rag",
  "RAG — Retrieval-Augmented Generation",
  "Le RAG (Retrieval-Augmented Generation) augmente les LLMs avec des sources de donnees externes — resolvant les problemes de knowledge cutoff et d'hallucination sur des faits specifiques. Il combine une recherche vectorielle et la generation LLM.",
  "Le RAG (Retrieval-Augmented Generation) est une technique d'architecture IA qui ameliore les LLMs en les augmentant d'un mecanisme de retrieval : avant de generer une reponse, le systeme recherche dans une base de connaissances externe les passages les plus pertinents, et les injecte dans le contexte du LLM pour ancrer la generation dans des faits verifies.",
  {
    "rag_architecture": [
      {"step": "1. Indexation", "description": "Les documents sont decoupes en chunks, transformes en embeddings (vecteurs) et stockes dans une vector database"},
      {"step": "2. Retrieval", "description": "La question utilisateur est transformee en embedding, recherche de similarite dans la vector DB, les K chunks les plus pertinents sont recuperes"},
      {"step": "3. Generation", "description": "Les chunks recuperes sont injectes dans le contexte du LLM comme 'sources', le LLM genere une reponse ancree sur ces sources"}
    ],
    "rag_benefits": [
      "Reduction des hallucinations sur les faits specifiques",
      "Acces a des connaissances non incluses dans l'entrainement",
      "Sources citables et verifiables",
      "Mise a jour des connaissances sans re-entrainement du modele"
    ],
    "rag_challenges": [
      "Qualite du chunking (trop petit = contexte insuffisant, trop grand = bruit)",
      "Qualite des embeddings (les bons modeles d'embedding sont critiques)",
      "Pertinence du retrieval (parfois les mauvais chunks sont recuperes)",
      "Coherence de la generation (le LLM peut ignorer les sources)"
    ],
    "alfred_rag": "ALFRED utilise le RAG sur sa knowledge base pour ancrer ses reponses dans des connaissances structurees — plutot que de se fier uniquement a ses connaissances d'entrainement."
  },
  [
    {"prompt": "Comment implemente-t-on un RAG en Python ?", "answer": "Stack minimale : (1) Chunking et embedding : LangChain ou LlamaIndex pour le pipeline, sentence-transformers pour les embeddings (all-MiniLM-L6-v2 est un bon debut), (2) Vector DB : ChromaDB (local, simple) ou Qdrant (plus scalable), (3) LLM : Ollama local ou API OpenAI/Anthropic. Pipeline : documents → chunks (500-1000 tokens) → embeddings → vector DB. Au moment de la requete : question → embedding → similarity search (top 3-5 chunks) → prompt = system + chunks + question → LLM → reponse. LangChain a des pipelines RAG ready-to-use pour le prototypage rapide."},
    {"prompt": "RAG ou fine-tuning — quand choisir l'un plutot que l'autre ?", "answer": "RAG : pour acces a des connaissances specifiques et changeantes (docs internes, base de connaissances, actualite). Avantage : mise a jour facile, sources citables. Fine-tuning : pour changer le style, le comportement ou incorporer des competences de domaine tres specifiques dans les poids du modele. Avantage : plus rapide a l'inference (pas de retrieval), style plus coherent. Dans la pratique : commencer par le RAG (moins cher, plus flexible), envisager le fine-tuning uniquement si le RAG ne suffit pas apres optimisation."}
  ],
  ["RAG", "retrieval", "embeddings", "vector database", "LangChain"]
))

save("professional/engineering/ai/vector_database.json", ku(
  "professional", "engineering", "vector_database",
  "Bases de donnees vectorielles",
  "Les bases de donnees vectorielles stockent des embeddings (representations numeriques de texte, images, etc.) et permettent la recherche de similarite par proximite dans un espace vectoriel — fondamentales pour le RAG et la recherche semantique.",
  "Une base de donnees vectorielle est un systeme de stockage specialise qui indexe et interroge des vecteurs de haute dimension (embeddings) en utilisant la distance geometrique (cosinus, euclidienne) pour trouver les elements les plus similaires a une requete, permettant la recherche semantique plutot que la correspondance exacte.",
  {
    "vector_search_concept": {
      "embedding": "Representation numerique d'un texte ou d'une image dans un espace vectoriel de haute dimension — les textes semantiquement similaires ont des vecteurs proches",
      "similarity_search": "Trouver les N vecteurs les plus proches d'un vecteur requete — souvent par similarite cosinus ou distance euclidienne",
      "approximate_nearest_neighbor": "ANN (HNSW, IVF) — algorithmes qui approchent la recherche exacte en echange de vitesse beaucoup plus elevee"
    },
    "vector_db_comparison": [
      {"db": "ChromaDB", "type": "Open source, embarquable", "use": "Prototype, usage local, integration Python simple"},
      {"db": "Qdrant", "type": "Open source, haute performance", "use": "Production, recherche vectorielle avancee"},
      {"db": "Pinecone", "type": "SaaS managé", "use": "Production managee, pas d'infra a gerer"},
      {"db": "Weaviate", "type": "Open source, GraphQL", "use": "Recherche semantique + filtrage avance"},
      {"db": "pgvector", "type": "Extension PostgreSQL", "use": "Si deja sur PostgreSQL — integrer la recherche vectorielle sans infra supplementaire"}
    ]
  },
  [
    {"prompt": "Comment choisir une vector database pour mon projet RAG ?", "answer": "Pour commencer (prototype) : ChromaDB — installation en pip, zero infra, API Python simple. Pour la production locale : Qdrant — tres performant, Docker image disponible, API REST+gRPC. Pour la production managee : Pinecone si tu ne veux pas gerer l'infra. Si tu es deja sur PostgreSQL : pgvector — ajoute la recherche vectorielle sans une nouvelle DB. En 2025, les benchmarks montrent que Qdrant et Weaviate ont les meilleures performances sur les grands volumes."},
    {"prompt": "C'est quoi un embedding et comment ca marche ?", "answer": "Un embedding est la transformation d'un texte (ou d'une image, d'un son) en un vecteur numerique — par exemple 384 ou 1536 nombres. Les modeles d'embedding (sentence-transformers, OpenAI ada-002, Cohere) sont entraines pour que des textes semantiquement proches aient des vecteurs geometriquement proches. Exemple : 'chien' et 'animal de compagnie' ont des vecteurs plus proches que 'chien' et 'table'. La vector DB stocke ces vecteurs et les compare geometriquement pour trouver les textes similaires."}
  ],
  ["vector database", "embeddings", "ChromaDB", "Qdrant", "RAG", "recherche semantique"]
))

save("professional/engineering/ai/chunking_strategies.json", ku(
  "professional", "engineering", "chunking_strategies",
  "Strategies de chunking pour le RAG",
  "Le chunking (decoupage des documents en fragments) est une etape critique du pipeline RAG — des chunks trop petits perdent le contexte, trop grands introduisent du bruit. Les strategies avancees (semantique, hierarchique) ameliorent significativement la qualite du retrieval.",
  "Le chunking est la strategie de decoupage des documents sources en fragments (chunks) optimaux pour l'indexation vectorielle dans un systeme RAG, equilibrant la granularite (contexte suffisant par chunk) et la precision (pas de bruit irrelevant par chunk).",
  {
    "chunking_strategies": [
      {"strategy": "Fixed-size", "description": "Chunks de N tokens, avec overlap de M tokens entre chunks", "pros": ["Simple", "Reproductible"], "cons": ["Coupe parfois au milieu d'une idee"], "default": "500-1000 tokens, 100-200 tokens d'overlap"},
      {"strategy": "Sentence-based", "description": "Un chunk = N phrases", "pros": ["Preserve les unites de sens"], "cons": ["Taille variable, peut etre trop petit"]},
      {"strategy": "Recursive character splitting", "description": "Decoupe selon les separateurs semantiques (paragraphes, phrases, mots) dans cet ordre", "pros": ["Respect de la structure"], "use": "LangChain RecursiveCharacterTextSplitter — defaut recommande"},
      {"strategy": "Semantic chunking", "description": "Regroupe les phrases semantiquement similaires — utilise les embeddings pour trouver les frontieres", "pros": ["Meilleure coherence semantique"], "cons": ["Plus lent et couteux a calculer"]},
      {"strategy": "Hierarchical (parent-child)", "description": "Petits chunks pour le retrieval, grands chunks pour le contexte (Small-to-Big)", "pros": ["Precision + contexte"], "use": "LlamaIndex ParentDocumentRetriever"}
    ],
    "evaluation": "Evaluer la qualite du chunking via la qualite des reponses RAG (RAGAS framework : faithfulness, relevancy, context precision) plutot que par inspection manuelle."
  },
  [
    {"prompt": "Quelle taille de chunk utiliser pour mon RAG sur des documents techniques ?", "answer": "Point de depart : 512-1024 tokens avec 100-200 tokens d'overlap (RecursiveCharacterTextSplitter de LangChain). Pour des documents techniques avec beaucoup de formules ou de tables : plutot 256-512 tokens (les sections techniques sont denses). Pour des documents narratifs (articles, rapports) : 1024-2048 tokens pour garder le contexte. Et faire un test A/B : comparer la qualite des reponses RAG avec plusieurs tailles de chunk sur ton corpus specifique — le corpus dict le bon chunking."},
    {"prompt": "Comment ameliorer les reponses de mon RAG qui sont parfois hors sujet ?", "answer": "Diagnostic etape par etape : (1) Afficher les chunks recuperes pour chaque requete — les mauvaises reponses viennent souvent de mauvais chunks recuperes, (2) Si les chunks sont pertinents mais la reponse est mauvaise : le probleme est dans le prompt LLM ou la longueur du contexte, (3) Si les chunks recuperes sont irrelevants : ameliorer le chunking (plus petit pour plus de precision) ou l'embedding model (essayer des modeles specialises domaine), (4) Ajouter un re-ranking (cross-encoder) apres le retrieval initial pour re-classer les chunks par pertinence avant de les injecter dans le prompt."}
  ],
  ["chunking", "RAG", "LangChain", "embeddings", "tokenisation"]
))

# =============================================================================
# professional / engineering / systeme_design
# =============================================================================

save("professional/engineering/systeme_design/ai_system_design.json", ku(
  "professional", "engineering", "ai_system_design",
  "Design de systemes IA",
  "Le design de systemes IA integre les patterns specifiques a l'IA (pipelines de donnees, inference, monitoring de modele, drift detection) dans une architecture systeme robuste, deployable et maintenable.",
  "Le design de systemes IA est la discipline qui consiste a concevoir des architectures logicielles capables d'integrer des modeles d'intelligence artificielle en production de facon fiable, scalable et maintenable, en adressant les defis specifiques aux systemes IA (non-determinisme, derive des modeles, couts d'inference, ethique).",
  {
    "ai_system_components": [
      {"component": "Data pipeline", "description": "Ingestion, validation, transformation et stockage des donnees d'entrainement et d'inference"},
      {"component": "Feature store", "description": "Stockage et service des features partagees entre les modeles (online + offline)"},
      {"component": "Model serving", "description": "API d'inference rapide et scalable (REST, gRPC, streaming)"},
      {"component": "Model registry", "description": "Versioning et tracking des modeles (MLflow, Weights & Biases)"},
      {"component": "Monitoring", "description": "Performance du modele en production (precision, latence, drift des donnees, drift du modele)"},
      {"component": "Feedback loop", "description": "Collecte des labels des utilisateurs pour le retrainement continu"}
    ],
    "ai_specific_challenges": [
      "Non-determinisme : le meme input peut produire des outputs differents (temperature > 0)",
      "Derive du modele (model drift) : les performances se degradent quand la distribution des donnees change",
      "Couts d'inference : les LLMs sont chers a executer en production (latence, tokens, GPU)",
      "Explainabilite : les decisions doivent etre justifiables (reglementation, confiance utilisateur)",
      "Biais et equite : monitorer les disparites de performance entre groupes"
    ]
  },
  [
    {"prompt": "Comment structurer l'architecture d'un produit IA en production ?", "answer": "Architecture minimale viable : (1) API Layer : FastAPI pour exposer l'inference, avec rate limiting et authentification, (2) Inference : modele LLM via Ollama (local) ou API OpenAI/Anthropic (cloud), avec cache (Redis) pour les requetes frequentes, (3) RAG : vector DB (ChromaDB ou Qdrant) + pipeline de retrieval, (4) Logging : logger toutes les requetes avec inputs/outputs/latence/cout, (5) Monitoring : alertes si le temps de reponse depasse X ou si le cout/jour depasse Y. Cette architecture couvre 80% des cas pour un MVP IA."},
    {"prompt": "Comment monitorer un LLM en production ?", "answer": "Quatre dimensions : (1) Latence : temps de reponse par requete — alerter si P95 > seuil, (2) Cout : tokens consommes par requete et par jour — eviter les surprises de facturation, (3) Qualite : un panel d'evaluations periodiques (Golden set de Q&A avec evaluation automatique ou humaine), (4) Utilisateur : taux de regeneration, feedback negatif, taux d'abandon. Outils : LangSmith (LangChain ecosystem), Langfuse (open source), ou un pipeline custom avec des logs structurees dans InfluxDB/Grafana."}
  ],
  ["architecture IA", "MLOps", "LLM", "production", "monitoring"]
))

# =============================================================================
# professional / leadership
# =============================================================================

save("professional/leadership/decision_making_business.json", ku(
  "professional", "leadership", "decision_making_business",
  "Prise de decision en leadership",
  "La prise de decision en leadership combine l'analyse rigoureuse (donnees, criteres) et le jugement (experience, valeurs, intuition calibree). Le leader decide en acceptant l'incertitude, en assumant la responsabilite et en apprenant de l'erreur.",
  "La prise de decision en leadership est la capacite d'un dirigeant a choisir une voie d'action dans des situations complexes et incertaines, en combinant analyse rationnelle, sagesse pratique et courage d'assumer les consequences — et en creant les conditions pour que l'organisation apprenne de chaque decision.",
  {
    "leadership_decision_principles": [
      "Decider avec les informations disponibles — attendre la certitude, c'est decider de ne pas decider",
      "Distinguer les decisions reversibles des irreversibles — vitesse vs rigueur selon le type",
      "Assumer la responsabilite de la decision meme si elle est mauvaise — pas de blame shifting",
      "Creer des conditions de feedback — savoir si la decision a bien fonctionne",
      "Apprendre systematiquement de l'erreur — post-mortem sans blame"
    ],
    "team_decision_models": [
      {"model": "Consultatif", "description": "Le leader recueille les avis mais decide seul", "use": "Decisions d'impact fort sur l'equipe"},
      {"model": "Consensus", "description": "L'equipe decide collectivement", "use": "Decisions reversibles, forte adhesion requise"},
      {"model": "Delegue", "description": "Un membre de l'equipe decide apres briefing", "use": "Decisions dans son domaine d'expertise"},
      {"model": "Autocratique", "description": "Le leader decide sans consultation", "use": "Urgences, crises, expertise claire du leader"}
    ]
  },
  [
    {"prompt": "Comment prendre des decisions difficiles en tant que manager ?", "answer": "Processus : (1) Clarifier si c'est ta decision ou si tu dois la deleguer ou consulter, (2) Reunir les informations pertinentes sans attendre la perfection, (3) Identifier les options reelles (souvent plus que 2), (4) Evaluer selon les criteres qui comptent vraiment (impact, valeurs, reversibilite), (5) Decider et communiquer clairement avec le raisonnement — pas juste la decision, le pourquoi. Et apres : creer un checkpoint pour evaluer si la decision a bien fonctionne."},
    {"prompt": "Comment ne pas etre paralyse par la peur de faire le mauvais choix en tant que leader ?", "answer": "Deux reframes : (1) L'indecision est aussi une decision — souvent la pire. En postponant, on subit les evenements plutot qu'on les dirige. (2) Les 'mauvaises decisions' sont souvent des decisions correctes avec une information incomplete — la qualite du processus est separable de la qualite du resultat. Se juger sur le processus ('ai-je fait une analyse rigoureuse avec l'information disponible ?') plutot que seulement sur le resultat libere de la paralysie."}
  ],
  ["leadership", "decision", "management", "responsabilite", "incertitude"]
))

# =============================================================================
# professional / product_management (core)
# =============================================================================

save("professional/product_management/product_core.json", ku(
  "professional", "product_management", "product_core",
  "Fondamentaux du product management",
  "Le product management est le role qui consiste a definir quoi construire (la bonne chose) pour que l'engineering puisse construire la chose bien. Le PM est responsable de la vision produit, de la strategie, et des resultats de l'equipe produit.",
  "Le product management est la fonction d'une organisation qui consiste a identifier les besoins des utilisateurs et du marche, a definir et prioriser les solutions a construire, et a coordonner leur livraison avec les equipes d'ingenierie et de design pour maximiser la valeur delivrée.",
  {
    "pm_responsibilities": [
      "Comprendre les utilisateurs (interviews, donnees comportementales)",
      "Definir la vision et la strategie produit",
      "Prioriser les features et les initiatives",
      "Coordonner avec l'engineering et le design",
      "Mesurer les resultats et iterer",
      "Communiquer aux parties prenantes"
    ],
    "pm_vs_po": {
      "PM (Product Manager)": "Focus strategique — vision, marche, utilisateurs, roadmap long terme",
      "PO (Product Owner)": "Focus tactique — backlog, user stories, sprint, collaboration engineering"
    },
    "good_pm_traits": [
      "Curiosite insatiable pour les utilisateurs",
      "Pensee structuree et basee sur les donnees",
      "Communication claire avec des audiences tres differentes",
      "Influence sans autorite hierarchique directe",
      "Tolerance a l'ambiguite et la capacite a decider quand meme"
    ]
  },
  [
    {"prompt": "Quel est le role d'un bon product manager ?", "answer": "En une phrase : s'assurer qu'on construit la bonne chose pour les bons utilisateurs. En pratique : comprendre profondement les utilisateurs (interviews, usage data), traduire ce comprhenison en problemes a resoudre (pas en solutions), prioriser rigoureusement avec les contraintes engineering et business, et mesurer si ce qu'on a livre a cree de la valeur reelle. Le PM n'est pas un 'mini-CEO' — il n'a pas d'autorite hierarchique. Son influence vient de la qualite de sa comprhenison et de sa communication."},
    {"prompt": "Comment devenir product manager quand on vient d'un autre domaine ?", "answer": "Trois transitions courantes : (1) Depuis l'engineering : avantage technique fort, travailler sur la comprehension utilisateur et la communication business, (2) Depuis le design : empathie utilisateur forte, travailler sur la rigueur donnees et les criteres de prioritisation, (3) Depuis le business/conseil : rigueur analytique forte, travailler sur la comprhenison technique et le cycle de delivery produit. Dans tous les cas : commencer par apprendre le vocabulaire (JTBD, OKR, sprint, MVP), pratiquer sur un side-project ou dans un role adjacent (PO, growth), et lire 'Inspired' de Marty Cagan."}
  ],
  ["product management", "PM", "vision produit", "priorisation", "utilisateurs"]
))

save("professional/product_management/product_discovery.json", ku(
  "professional", "product_management", "product_discovery",
  "Product Discovery",
  "La product discovery est l'ensemble des activites qui permettent de valider qu'on construit la bonne chose avant de la construire — en testant les hypotheses sur les problemes utilisateurs et les solutions potentielles avec un investissement minimal.",
  "La product discovery est la phase d'un processus de developpement produit dans laquelle l'equipe valide que les problemes identifies sont reels et importants pour les utilisateurs, que les solutions envisagees les resolvent effectivement, et que les solutions sont techniquement faisables et viables pour le business.",
  {
    "discovery_questions": [
      "Le probleme est-il reel ? (interviews, donnees quantitatives)",
      "Le probleme est-il suffisamment important pour que les utilisateurs cherchent une solution ? (willingness to pay, comportement actuel)",
      "Notre solution resout-elle effectivement le probleme ? (prototype, test utilisateur)",
      "Les utilisateurs peuvent-ils utiliser la solution ? (tests d'usabilite)",
      "La solution est-elle techniquement faisable ? (spike technique)",
      "La solution est-elle viable pour le business ? (model economique, competence requise)"
    ],
    "discovery_techniques": [
      {"technique": "Interviews utilisateurs", "question": "Probleme reel ? Important ?", "cost": "Faible"},
      {"technique": "Prototype papier", "question": "La solution est-elle comprehensible ?", "cost": "Tres faible"},
      {"technique": "Prototype cliquable (Figma)", "question": "L'UX fonctionne-t-elle ?", "cost": "Moyen"},
      {"technique": "Smoke test / Landing page", "question": "Y a-t-il de l'interet ?", "cost": "Faible"},
      {"technique": "Wizard of Oz", "question": "La solution cree-t-elle de la valeur ?", "cost": "Moyen (manual)"},
      {"technique": "A/B test", "question": "Quelle option performe mieux ?", "cost": "Eleve (dev requis)"}
    ]
  },
  [
    {"prompt": "Comment valider mon idee produit avant de developper ?", "answer": "Sequence par hypotheses : (1) Hypothese probleme — est-ce un vrai probleme ? Interviews de 5-10 personnes de ton segment cible, ecoute sans pitcher. Si 7/10 decrivent activement ce probleme et cherchent une solution : valide. (2) Hypothese solution — est-ce qu'ils paient / s'inscrivent ? Landing page avec CTA (liste d'attente, pre-commande). 200 visiteurs, > 5% de conversion : signal positif. (3) Hypothese UX — peuvent-ils utiliser la solution ? Prototype Figma avec 5 utilisateurs en test d'usabilite. Ces 3 etapes coutent quelques jours et valident ou invalident avant d'investir dans le developpement."},
    {"prompt": "Pourquoi mes features ne sont-elles pas utilisees une fois livrees ?", "answer": "Symptome d'un probleme de discovery. Causes frequentes : (1) Le probleme est reel mais mineur — les utilisateurs ne changent pas leur comportement pour des ameliorations marginales, (2) La solution ne correspond pas a la facon dont les utilisateurs pensent au probleme — on a resolu le probleme 'tel qu'on le comprend', pas tel qu'ils le vivent, (3) L'onboarding de la feature est insuffisant — les utilisateurs ne savent pas qu'elle existe ou comment l'utiliser. Remediation : interviews utilisateurs sur les features non-utilisees (pas 'pourquoi vous n'utilisez pas X ?' mais 'racontez-moi comment vous gerez Y aujourd'hui ?')."}
  ],
  ["discovery", "validation", "prototype", "interviews", "hypotheses"]
))

save("professional/product_management/product_lifecycle.json", ku(
  "professional", "product_management", "product_lifecycle",
  "Cycle de vie produit",
  "Le cycle de vie d'un produit (introduction, croissance, maturite, declin) determine les strategies optimales de croissance, de pricing et d'investissement. Savoir ou en est son produit dans ce cycle oriente les decisions.",
  "Le cycle de vie d'un produit est la sequence des phases traversees par un produit depuis son introduction jusqu'a son retrait du marche — introduction, croissance, maturite et declin — chaque phase ayant des caracteristiques de marche, de competition et des strategies optimales specifiques.",
  {
    "lifecycle_phases": [
      {"phase": "Introduction", "characteristics": ["Croissance lente", "Couts eleves", "Competition faible"], "strategy": "Construire la notoriete, eduquer le marche, affiner le PMF"},
      {"phase": "Croissance", "characteristics": ["Croissance rapide", "Profitabilite amelioree", "Competition qui entre"], "strategy": "Maximiser la croissance, investir en marketing et sales, renforcer la differentiation"},
      {"phase": "Maturite", "characteristics": ["Croissance ralentie", "Competition intense", "Marge sous pression"], "strategy": "Optimiser les couts, defendre les segments cles, envisager l'innovation de rupture"},
      {"phase": "Declin", "characteristics": ["Decroissance des ventes", "Reduction des investissements"], "strategy": "Recolter (milking), pivoter, ou retirer le produit"}
    ],
    "extension_strategies": [
      "Nouveaux usages pour le produit existant",
      "Nouveaux segments de marche",
      "Nouvelles geographies",
      "Améliorations produit significatives",
      "Bundling avec d'autres produits"
    ]
  },
  [
    {"prompt": "Comment savoir ou en est mon produit dans son cycle de vie ?", "answer": "Regarder trois indicateurs : (1) Taux de croissance (accelere = introduction/croissance, ralentit = maturite, decline = declin), (2) Intensite concurrentielle (peu de concurrents = introduction, beaucoup et guerre des prix = maturite), (3) Comportement des utilisateurs (adoption active de nouveaux utilisateurs = croissance, surtout des renouvellements = maturite). Un produit SaaS B2B atteint souvent la maturite apres 5-8 ans sur un marche vertical."},
    {"prompt": "Mon produit est en maturite — que faire pour relancer la croissance ?", "answer": "Quatre leviers : (1) Nouveaux segments non adresses (marchés verticaux adjacents, nouvelles geographies), (2) Nouveaux cas d'usage pour les clients existants (features qui ouvrent de nouveaux workflows), (3) Montee en gamme (enterprise, services) ou descente en gamme (SMB, self-serve), (4) Innovation de rupture adjacente — soit un nouveau produit, soit une transformation profonde du produit actuel. La plupart des extensions de la maturite combinent 2-3 de ces leviers."}
  ],
  ["cycle de vie", "croissance", "maturite", "declin", "strategie produit"]
))

save("professional/product_management/product_metrics.json", ku(
  "professional", "product_management", "product_metrics",
  "Metriques produit fondamentales",
  "Les metriques produit mesurent la sante et la performance d'un produit selon plusieurs dimensions : acquisition, activation, retention, revenue, referral (AARRR). Les bonnes metriques sont actionables, fiables et alignees avec la valeur utilisateur reelle.",
  "Les metriques produit sont les indicateurs quantitatifs qui permettent de mesurer la performance d'un produit, d'identifier les opportunites d'amelioration et de prendre des decisions eclairees — en distinguant les metriques de sante (vanity metrics) des metriques qui revelent la valeur reelle pour les utilisateurs.",
  {
    "aarrr_framework": [
      {"metric": "Acquisition", "description": "Comment les utilisateurs decouvrent le produit", "examples": ["CAC", "Canaux d'acquisition", "Trafic par source"]},
      {"metric": "Activation", "description": "Premier moment de valeur pour l'utilisateur", "examples": ["Taux d'activation", "Time-to-value", "Completion onboarding"]},
      {"metric": "Retention", "description": "Les utilisateurs reviennent-ils ?", "examples": ["D1/D7/D30 retention", "DAU/MAU ratio", "Churn rate"]},
      {"metric": "Revenue", "description": "Le produit genere-t-il du revenu ?", "examples": ["MRR/ARR", "ARPU", "LTV", "Expansion MRR"]},
      {"metric": "Referral", "description": "Les utilisateurs recommandent-ils ?", "examples": ["NPS", "Taux de referral", "Coefficient viral K"]}
    ],
    "vanity_vs_actionable": {
      "vanity": "Impressionnant mais non actionnable — total d'inscriptions, pageviews, followers",
      "actionable": "Revele une action a prendre — taux d'activation J7, churn par cohorte, conversion par canal"
    },
    "metric_hierarchy": "North Star Metric (une seule) → Input metrics (3-5, les leviers de la NSM) → Guardrail metrics (a ne pas degrader) → Operational metrics (sante systeme)"
  },
  [
    {"prompt": "Quelles metriques suivre pour un nouveau SaaS B2B ?", "answer": "Phase early : (1) MRR et croissance MoM (vitale de base), (2) Churn MRR (> 3% mensuel = alarme), (3) Nombre de clients actifs et usage (est-ce qu'ils utilisent vraiment ?), (4) NPS ou CSAT (satisfaction), (5) Runway (mois de cash). Eviter de suivre trop de metriques trop tot — l'enjeu est de comprendre le comportement utilisateur, pas d'optimiser des KPIs. Les metriques se multiplient avec la maturite."},
    {"prompt": "Comment savoir si une metrique est bonne ou si c'est une vanity metric ?", "answer": "Test en 3 questions : (1) Est-ce que cette metrique change si le produit cree plus ou moins de valeur pour les utilisateurs ? (Si oui : bonne metrique. Si non : vanity.) (2) Est-ce qu'une action specifique peut ameliorer cette metrique ? (Les metriques actionnables ont des leviers clairs.) (3) Est-ce que l'amelioration de cette metrique se traduit en resultats business ? (NPS est bonne parce qu'il predit la retention et les referrals. Pageviews peuvent etre vides de sens.)"}
  ],
  ["metriques", "AARRR", "MRR", "churn", "retention", "KPI"]
))

# =============================================================================
# professional / strategy / product_strategy
# =============================================================================

save("professional/strategy/product_strategy/problem_framing.json", ku(
  "professional", "strategy", "problem_framing",
  "Cadrage du probleme (Problem Framing)",
  "Le problem framing est l'art de definir le bon probleme a resoudre avant de chercher des solutions. Un probleme bien cadre est deja a moitie resolu ; un probleme mal cadre genere des solutions a cote des besoins reels.",
  "Le problem framing est la technique strategique qui consiste a definir et formuler precisement un probleme — en identifiant le vrai probleme (pas le symptome), les contraintes, les parties prenantes impactees et les criteres de succes — pour s'assurer que les efforts de resolution vont dans la bonne direction.",
  {
    "framing_techniques": [
      "Distinction symptome/cause : '5 Pourquoi' pour remonter a la cause racine",
      "Reformulation : 'Le vrai probleme n'est pas X mais Y' — changer l'angle revele de nouvelles solutions",
      "Point de vue utilisateur : 'Qui a ce probleme ? Dans quelle situation ? Avec quelle frequence ?'",
      "Quantification : 'Quel est le cout ou l'impact du probleme non resolu ?'",
      "Contraintes explicites : 'Quelles solutions sont hors scope et pourquoi ?'"
    ],
    "design_thinking_define": "La phase 'Define' du Design Thinking formalise le problem framing : 'Comment pourrions-nous [faire quelque chose] pour [utilisateur] afin que [resultat]' — le 'Comment pourrions-nous' ouvre l'espace de solutions sans les forcer.",
    "reframe_examples": [
      "Probleme initial : 'Nos utilisateurs n'utilisent pas la feature X'. Reframe : 'Nos utilisateurs n'ont pas identifie le moment ou X leur serait utile'",
      "Probleme initial : 'Nous avons trop peu de leads'. Reframe : 'Notre entonnoir de conversion perd 80% des leads entre qualification et demo'"
    ]
  },
  [
    {"prompt": "Comment cadrer un probleme avant de le resoudre ?", "answer": "En 4 etapes : (1) Ecrire le probleme tel qu'il est percu actuellement — l'externaliser revele souvent des ambiguites, (2) Demander '5 Pourquoi' — a chaque niveau, le probleme se redefinit, (3) Reformuler : 'Si le vrai probleme etait [autre chose], quelles solutions seraient possibles ?' — le changement d'angle revele de nouvelles options, (4) Valider avec les personnes impactees : 'Est-ce que ce cadrage correspond a votre experience du probleme ?' Un cadrage valide par les personnes impactees est plus robuste qu'un cadrage construit en chambre."},
    {"prompt": "Mon equipe cherche des solutions mais on tourne en rond — que faire ?", "answer": "Signal que le probleme est mal cadre. Exercice : chaque membre de l'equipe ecrit sa definition du probleme en 1 phrase. Comparer — si les definitions sont tres differentes, vous ne cherchez pas a resoudre le meme probleme. Processus : reunir l'equipe, collecter les definitions, trouver les points communs et les divergences, converger vers une definition partagee et validee avec les utilisateurs. Ce travail de cadrage collectif peut prendre 1-2h mais il fait gagner des semaines de solutions a cote."}
  ],
  ["problem framing", "5 pourquoi", "cadrage", "design thinking", "strategie"]
))

save("professional/strategy/product_strategy/roadmap_prioritization.json", ku(
  "professional", "strategy", "roadmap_prioritization",
  "Priorisation de roadmap",
  "La priorisation de roadmap alloue les ressources limitees de developpement aux initiatives qui creent le plus de valeur — pour les utilisateurs et pour le business. Elle necessite des criteres explicites, une contribution aux OKRs, et un alignement des parties prenantes.",
  "La priorisation de roadmap est le processus par lequel une equipe produit selectionne et ordonne les initiatives a developper en fonction de leur impact attendu, de leur effort de realisation, de leur alignement strategique et des retours utilisateurs, pour maximiser la valeur delivree dans les contraintes de capacite.",
  {
    "prioritization_criteria": [
      {"criterion": "Impact utilisateur", "description": "Combien d'utilisateurs sont impactes ? A quelle intensite ?"},
      {"criterion": "Alignement OKR", "description": "Cette initiative contribue-t-elle directement aux objectifs strategiques ?"},
      {"criterion": "Effort engineering", "description": "Combien de temps et de ressources cette initiative requiert-elle ?"},
      {"criterion": "Urgence", "description": "Y a-t-il une contrainte temporelle (concurrence, client, regulation) ?"},
      {"criterion": "Risque", "description": "Quelle est la probabilite que l'initiative delivre la valeur attendue ?"},
      {"criterion": "Dependencies", "description": "Cette initiative necessite-t-elle d'autres elements non disponibles ?"}
    ],
    "roadmap_health_indicators": [
      "Le top 3 des initiatives de la roadmap est directement lie aux OKRs",
      "Les initiatives sont formulees en termes de problemes a resoudre, pas de features a livrer",
      "Il y a un equilibre entre valeur court terme et investissements long terme",
      "L'engineering a contribue aux estimations d'effort",
      "La roadmap a ete revue et ajustee dans les 30 derniers jours"
    ]
  },
  [
    {"prompt": "Comment convaincre les parties prenantes d'accepter ma priorisation de roadmap ?", "answer": "Trois approches : (1) Rendre visible le processus de decision — partager les criteres, les scores, le raisonnement. Quand les parties prenantes comprennent comment on decide, elles acceptent mieux les decisions qui ne vont pas dans leur sens, (2) Lier chaque decision aux OKRs partages — 'j'ai priorise X plutot que Y parce que X contribue directement a notre OKR Q1 de reduire le churn de 35% a 25%', (3) Montrer les trade-offs explicitement — 'si on fait Y maintenant, on ne fait pas X avant Q3'. Les choix de depiorisation sont aussi importants que les choix de priorite."},
    {"prompt": "Comment ne pas etre ecrase par les nouvelles demandes qui arrivent en cours de trimestre ?", "answer": "Processus de triage : (1) Toute nouvelle demande passe par un formulaire avec les champs : probleme a resoudre, utilisateurs impactes, impact estime, urgence, (2) Revue hebdomadaire de 30 min en equipe : trier les nouvelles entrees selon les criteres de roadmap, (3) Seuil de priorite : seule une demande qui depasse un certain score ou qui bloque un OKR actif est inseree dans le sprint courant. Tout le reste attend la prochaine revue de roadmap. La discipline du process protege l'equipe de la reactivite perpetuelle."}
  ],
  ["roadmap", "priorisation", "OKR", "parties prenantes", "produit"]
))

save("professional/strategy/product_strategy/value_proposition.json", ku(
  "professional", "strategy", "value_proposition",
  "Proposition de valeur",
  "La proposition de valeur est la promesse specifique qu'un produit ou service fait a ses utilisateurs cibles — ce qu'il fait pour eux, pourquoi c'est mieux que les alternatives, et pour qui. Elle est le coeur du positionnement et de la communication.",
  "La proposition de valeur est la declaration qui explique en quoi un produit ou service cree de la valeur pour un segment de clients specifique, comment il resout leurs problemes ou satisfait leurs besoins, et pourquoi il est preferable aux alternatives disponibles.",
  {
    "value_proposition_canvas": {
      "customer_jobs": "Ce que le client cherche a accomplir (fonctionnel, emotionnel, social)",
      "customer_pains": "Les frustrations, obstacles et risques que le client veut eviter",
      "customer_gains": "Les resultats positifs que le client desire obtenir",
      "products_services": "Les solutions que vous offrez",
      "pain_relievers": "Comment votre solution reduit les frustrations du client",
      "gain_creators": "Comment votre solution produit les resultats desires"
    },
    "vp_writing_tips": [
      "Specifique (pas 'nous aidons les entreprises' mais 'nous aidons les PMEs de 10-50 employes en B2B SaaS')",
      "Benefit-led (ce que le client gagne, pas les features)",
      "Differenciee (pourquoi vous plutot qu'un concurrent)",
      "Croyable (supportee par des preuves ou des garanties)"
    ],
    "testing_vp": "La proposition de valeur se teste sur le terrain : taux de clic sur les landing pages, taux de conversion en demo, verbatims des pourquoi les prospects ont choisi ou n'ont pas choisi votre solution."
  },
  [
    {"prompt": "Comment ecrire une proposition de valeur efficace pour mon produit IA ?", "answer": "Template : 'Pour [segment specifique] qui [probleme cle], [nom du produit] est un [categorie] qui [benefice principal]. Contrairement a [alternative principale], notre produit [differenciateur cle].' Exemple pour un assistant IA : 'Pour les consultants independants qui passent trop de temps a documenter et preparer leurs missions, ALFRED est un assistant IA personnel qui reduit de 40% le temps administratif. Contrairement aux outils generiques, ALFRED apprend votre facon de travailler et anticipe vos besoins.' Tester le message avec 5 prospects — si leur reaction est 'c'est exactement mon probleme' : bonne proposition."},
    {"prompt": "Ma proposition de valeur n'accroche pas les prospects — que faire ?", "answer": "Diagnostic en 3 etapes : (1) Interview 5-10 prospects qui n'ont pas converti — 'quand vous avez vu notre message, qu'est-ce que vous avez compris ?' et 'qu'est-ce qui ne vous parlait pas ?' Les malentendus sont revelatrices, (2) Comparer avec les verbatims des clients qui ont converti — quels mots utilisent-ils pour decrire le benefice ? Utiliser leurs mots, pas les votres, (3) Tester differentes formulations (A/B sur landing page ou campagne email) avec les mots clients. Souvent, le probleme n'est pas le produit — c'est le langage qu'on utilise pour le decrire."}
  ],
  ["proposition de valeur", "positionnement", "segmentation", "benefices", "message"]
))

print("\nBatch 13 professional restants (16 fichiers) : DONE")
