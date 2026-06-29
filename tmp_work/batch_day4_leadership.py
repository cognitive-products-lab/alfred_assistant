"""
Enrichissement day4 — professional/leadership (15 KU)
Domaine critique pour ALFRED CPL : styles, influence, feedback, conflit, vision, équipe.
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
            "domain": "professional", "subdomain": "leadership",
            "status": "validated", "metadata": meta(), "priority": priority,
            "summary": summary, "core_definition": core_def, "knowledge": knowledge,
            "example_answers": examples, "response_guidance": guidance,
            "tags": tags, "related_knowledge_units": []}

BASE = "professional/leadership"

# 1 ─ Styles de leadership
save(f"{BASE}/leadership_styles.json", ku(
    "knowledges.professional.leadership.leadership_styles",
    "Styles de leadership — du directif au servant leader",
    "high",
    "Vue d'ensemble des grands styles de leadership (transformationnel, situationnel, servant, directif, démocratique) et quand les appliquer selon le contexte et la maturité de l'équipe.",
    "Un style de leadership est l'approche relationnelle et décisionnelle adoptée par un leader pour mobiliser son équipe vers un objectif — chaque style a ses forces et ses limites selon le contexte.",
    {"styles": {
        "directif": "Donne des instructions claires et contrôle de près — efficace en crise ou avec débutants, épuisant sur la durée",
        "democratique": "Consulte l'équipe avant de décider — génère l'adhésion, ralentit les décisions urgentes",
        "transformationnel": "Inspire par la vision et le sens — développe les talents, demande de l'énergie émotionnelle constante",
        "servant_leader": "Met l'équipe au centre — supprime les obstacles, développe les personnes, efficace sur l'engagement long terme",
        "situationnel": "Adapte le style selon la maturité et la motivation de chaque personne — plus complexe à déployer mais le plus polyvalent",
        "laissez_faire": "Délègue entièrement — puissant avec des experts autonomes, désastreux avec des juniors sans cadre"
     },
     "modele_situationnel": {
        "reference": "Hersey & Blanchard",
        "matrice": "Compétence × Motivation → S1 (directif), S2 (coaching), S3 (soutien), S4 (délégation)",
        "principe": "Le meilleur style dépend de la personne ET de la tâche — pas d'un style unique"
     },
     "pieges": [
        "Rester bloqué dans un seul style par confort",
        "Appliquer le même style à tout le monde dans l'équipe",
        "Confondre style et personnalité — le style s'adapte, la personnalité est stable"
     ]},
    [{"prompt": "Mon équipe ne réagit pas à mon management. Quel style adopter ?",
      "answer": "Avant de changer de style, diagnostiquer la situation : est-ce un problème de compétence (la personne ne sait pas) ou de motivation (elle ne veut pas) ? Pour un manque de compétence sur une tâche spécifique : passer en mode coaching — expliquer, démontrer, superviser. Pour un manque de motivation : chercher la cause (charge, sens, relation ?) avant de décider. Le modèle situationnel de Hersey & Blanchard donne une grille simple : adapter le niveau de directive ET de soutien à la combinaison compétence × motivation de chaque personne."},
     {"prompt": "C'est quoi la différence entre un manager et un leader ?",
      "answer": "Le manager gère la complexité : planifie, organise, contrôle, résout des problèmes opérationnels. Le leader gère le changement : donne une direction, aligne les personnes, les motive. Dans la réalité, les deux rôles coexistent chez la même personne. La distinction de Kotter : le management produit de la cohérence et de la prévisibilité — le leadership produit du mouvement et de la transformation. Une organisation a besoin des deux."}],
    {"tone": "pragmatique, ancré dans la réalité managériale",
     "structure": ["styles", "modèle situationnel", "pièges"],
     "avoid": ["hiérarchiser les styles comme si l'un était supérieur", "ignorer le contexte"]},
    ["leadership", "styles de management", "situationnel", "transformationnel", "servant leader", "Hersey Blanchard"]
))

# 2 ─ Feedback efficace
save(f"{BASE}/feedback_efficace.json", ku(
    "knowledges.professional.leadership.feedback_efficace",
    "Donner et recevoir du feedback — outil de développement",
    "high",
    "Techniques pour donner un feedback constructif (SBI, DESC, sandwich inversé), créer une culture du feedback et recevoir le feedback sans défensivité.",
    "Le feedback efficace est une communication ciblée sur un comportement observable et son impact, formulée de façon à permettre à son destinataire de comprendre ce qui se passe et de choisir d'ajuster — sans attaquer la personne.",
    {"modeles": {
        "SBI": "Situation (contexte précis) → Behavior (comportement observable) → Impact (effet concret) — le plus clair et le moins menaçant",
        "DESC": "Décrire → Exprimer (ressenti) → Spécifier (attente) → Conséquences — utile pour les situations chargées émotionnellement",
        "sandwich": "Positif → Amélioration → Positif — souvent inefficace car l'amélioration est noyée, mais reste utile pour les profils très fragiles"
     },
     "principes": [
        "Donner le feedback rapidement après le comportement (pas 3 semaines après)",
        "Privé pour le négatif, public pour le positif — jamais l'inverse",
        "Centrer sur le comportement, pas la personne (\"tu as coupé la parole 3 fois\" pas \"tu es irrespectueux\")",
        "Un seul message clé par session — pas une liste de 7 points"
     ],
     "recevoir_feedback": {
        "regle": "Écouter complètement avant de répondre — résister à l'envie de se justifier",
        "questions_utiles": ["\"Peux-tu me donner un exemple précis ?\"", "\"Qu'est-ce que tu aurais préféré à la place ?\""],
        "apres": "Remercier indépendamment de l'accord — le feedback est un cadeau même désagréable"
     },
     "culture_feedback": "Des check-ins hebdomadaires de 15 min valent mieux qu'une revue annuelle — la fréquence réduit l'enjeu émotionnel de chaque échange"},
    [{"prompt": "Comment donner un feedback difficile sans démotiver la personne ?",
      "answer": "Utiliser le modèle SBI dans un contexte privé. Exemple : \"Lors de la présentation client de mardi (Situation), j'ai remarqué que tu as présenté les chiffres sans vérifier les données de la veille (Behavior) — le client a relevé l'erreur et ça a fragilisé notre crédibilité (Impact). Comment tu vois ça ?\" Finir par une question ouvre le dialogue. Ce qui démotive, c'est le flou (\"c'était pas top\") ou l'attaque sur la personne — le SBI évite les deux."},
     {"prompt": "Je reçois très peu de feedback de ma hiérarchie. Comment en obtenir ?",
      "answer": "Demander directement : \"J'aimerais avoir ton retour sur [contexte précis] — qu'est-ce qui a bien fonctionné et qu'est-ce que je pourrais améliorer ?\" Être spécifique dans la demande — \"tu as des retours ?\" donne souvent \"ça allait\". Proposer également des formats courts : \"Tu as 10 min vendredi pour qu'on fasse un point rapide sur mon travail de la semaine ?\" Les managers qui donnent peu de feedback le font souvent par manque de temps ou par peur de blesser — l'initiative de demander les soulage."}],
    {"tone": "concret, orienté pratique et bienveillance",
     "structure": ["modèles", "principes", "recevoir", "culture"],
     "avoid": ["moralisateur", "ignorer la dimension émotionnelle"]},
    ["feedback", "SBI", "DESC", "management", "développement", "communication managériale"]
))

# 3 ─ Gestion de conflits
save(f"{BASE}/gestion_conflits.json", ku(
    "knowledges.professional.leadership.gestion_conflits",
    "Gestion des conflits — transformer la tension en levier",
    "high",
    "Approches pour diagnostiquer, désamorcer et résoudre les conflits interpersonnels et d'équipe : styles de Thomas-Kilmann, médiation, communication non-violente.",
    "La gestion de conflits est l'ensemble des pratiques permettant à un leader de naviguer les désaccords et tensions — en distinguant le conflit de tâche (productif) du conflit relationnel (destructif) — pour maintenir la performance et la cohésion d'équipe.",
    {"types_conflits": {
        "tache": "Désaccord sur les idées, méthodes, priorités — PRODUCTIF si bien géré, stimule l'innovation",
        "relationnel": "Tension interpersonnelle, méfiance, ressentis négatifs — DESTRUCTIF, à désamorcer rapidement",
        "processus": "Désaccord sur qui fait quoi et comment — souvent un symptôme d'un problème de rôles ou de clarté"
     },
     "thomas_kilmann": {
        "reference": "Modèle TKI — 5 styles selon assertivité × coopération",
        "competitif": "Assertif + non coopératif — gagne le conflit, perd la relation",
        "collaboratif": "Assertif + coopératif — solution win-win, demande du temps",
        "compromis": "Mi-chemin — solution rapide mais personne n'est vraiment satisfait",
        "accommodant": "Cède — préserve la relation à court terme, crée du ressentiment long terme",
        "evitement": "Fuit — utile pour les conflits sans importance, toxique pour les sujets importants"
     },
     "processus_resolution": [
        "1. Séparer les personnes du problème (Fisher & Ury)",
        "2. Identifier les intérêts derrière les positions",
        "3. Générer des options avant de trancher",
        "4. Utiliser des critères objectifs pour décider"
     ],
     "cnv": "Communication Non-Violente (Rosenberg) : Observation → Sentiment → Besoin → Demande — désarme les défenses sans capituler"},
    [{"prompt": "Deux membres de mon équipe sont en conflit ouvert. Comment intervenir ?",
      "answer": "Trois étapes : d'abord voir chaque personne séparément — comprendre leur point de vue sans prendre parti. Ensuite réunir les deux en posant des règles (parler en je, pas d'interruptions) et en recentrant sur le problème concret plutôt que les personnes. Enfin co-construire un accord sur les comportements futurs — pas une décision imposée. Si le conflit est profond, envisager une médiation externe. Ce qu'il ne faut surtout pas faire : ignorer ou laisser l'équipe \"régler ça entre eux\" — un conflit non traité s'amplifie toujours."},
     {"prompt": "Je n'aime pas les conflits et j'ai tendance à éviter. Comment changer ?",
      "answer": "L'évitement préserve la paix à court terme et crée de la toxicité long terme — les non-dits s'accumulent. Commencer petit : adresser les micro-irritants dès qu'ils surviennent plutôt que d'attendre qu'ils deviennent des crises. Technique : formuler un désaccord avec \"j'ai une perspective différente\" suivi d'une question (\"Comment tu es arrivé à cette conclusion ?\") — ça engage le dialogue sans confrontation directe. Le conflit de tâche (\"je ne suis pas d'accord sur cette approche\") est normal et sain — c'est le conflit relationnel qu'il faut éviter."}],
    {"tone": "psychologique mais pragmatique, sans jugement",
     "structure": ["types", "TKI", "processus", "CNV"],
     "avoid": ["présenter l'évitement comme toujours mauvais", "ignorer la dimension émotionnelle"]},
    ["conflit", "Thomas-Kilmann", "médiation", "CNV", "gestion d'équipe", "leadership"]
))

# 4 ─ Vision et sens
save(f"{BASE}/vision_et_sens.json", ku(
    "knowledges.professional.leadership.vision_et_sens",
    "Vision et sens — donner une direction qui mobilise",
    "high",
    "Comment construire, formuler et communiquer une vision inspirante qui donne du sens au travail quotidien et aligne l'équipe sur une direction commune.",
    "La vision est une image claire et désirable d'un futur possible, formulée de façon à créer du sens pour celles et ceux qui y contribuent — elle répond à la question 'pourquoi on fait ça' avant de répondre à 'comment'.",
    {"composantes_vision": {
        "what": "Quel est le changement concret qu'on veut créer dans le monde ?",
        "why": "Pourquoi c'est important — pour qui, quel impact ?",
        "timeframe": "Sur quel horizon (2 ans, 5 ans, 10 ans) — assez loin pour inspirer, assez proche pour motiver",
        "ambitious_but_believable": "Suffisamment ambitieuse pour demander un effort, suffisamment crédible pour ne pas sembler délirante"
     },
     "golden_circle": {
        "reference": "Simon Sinek — Start With Why",
        "why": "Pourquoi on existe (mission, raison d'être)",
        "how": "Comment on fait — ce qui nous différencie",
        "what": "Ce qu'on produit concrètement",
        "principe": "Commencer par le Why mobilise — commencer par le What informe seulement"
     },
     "communiquer_la_vision": [
        "Répéter inlassablement — une vision entendue une fois est oubliée",
        "La connecter au travail quotidien : 'ce rapport qu'on prépare sert à...'",
        "Illustrer par des histoires concrètes — pas des slides abstraites",
        "Célébrer les petites victoires comme preuves que la vision avance"
     ],
     "sens_vs_vision": "La vision est collective (où va l'organisation). Le sens est individuel (pourquoi moi je viens travailler ici). Un bon leader connecte les deux."},
    [{"prompt": "Comment donner du sens à mon équipe dans un contexte de travail très opérationnel ?",
      "answer": "Trois niveaux : 1) Connecter les tâches à l'impact final — \"le rapport que tu prépares va permettre à notre client de prendre une décision qui touche 500 emplois\". 2) Créer de la progressivité visible — mesurer et partager les progrès collectifs même sur des indicateurs simples. 3) Personnaliser — comprendre ce qui motive chaque personne (apprentissage ? reconnaissance ? impact social ?) et créer des ponts avec le travail. Le sens se construit aussi dans la relation avec le manager — sentir qu'on est vu et considéré est en soi une source de sens."},
     {"prompt": "Ma vision d'équipe ne prend pas. Les gens l'entendent mais ça ne change rien.",
      "answer": "Deux causes fréquentes : 1) La vision est formulée en termes d'outputs (\"devenir le meilleur département\") plutôt que d'impact (\"permettre à nos clients de lancer plus vite\"). Reformuler avec le Golden Circle — commencer par le pourquoi. 2) Il y a un décalage entre la vision et le vécu quotidien — si les pratiques managériales contredisent la vision, personne ne la croit. La vision doit être incarnée dans les décisions du quotidien, pas seulement dans les présentations. Que décide-t-on différemment grâce à cette vision ?"}],
    {"tone": "inspirant mais pragmatique, ancré dans l'exécution",
     "structure": ["composantes", "Golden Circle", "communiquer", "sens individuel"],
     "avoid": ["trop abstrait", "confondre vision et slogan"]},
    ["vision", "sens", "Simon Sinek", "Why", "leadership", "mobilisation", "motivation"]
))

# 5 ─ Intelligence émotionnelle du leader
save(f"{BASE}/intelligence_emotionnelle_leader.json", ku(
    "knowledges.professional.leadership.intelligence_emotionnelle_leader",
    "Intelligence émotionnelle du leader — se connaître pour mieux guider",
    "high",
    "Les 5 dimensions de l'IE selon Goleman appliquées au leadership : conscience de soi, maîtrise de soi, motivation, empathie, compétences sociales — et comment les développer.",
    "L'intelligence émotionnelle (IE) du leader est la capacité à reconnaître, comprendre et gérer ses propres émotions et celles des autres pour prendre de meilleures décisions et créer des relations de confiance — composante qui différencie les managers techniques des leaders inspirants.",
    {"dimensions_goleman": {
        "conscience_soi": "Reconnaître ses émotions en temps réel et comprendre leur effet sur son comportement — la base de tout le reste",
        "maitrise_soi": "Réguler ses émotions pour ne pas réagir sous l'impulsion — créer de l'espace entre stimulus et réponse",
        "motivation": "Avoir une drive interne au-delà des récompenses externes — résilience face aux obstacles",
        "empathie": "Comprendre l'état émotionnel des autres et y répondre de façon appropriée — pas la même chose que la sympathie",
        "competences_sociales": "Gérer les relations, influencer, communiquer, gérer les conflits — la résultante des 4 dimensions précédentes"
     },
     "impact_leadership": {
        "ambiance": "Les émotions du leader sont contagieuses — un leader anxieux crée de l'anxiété collective",
        "decisions": "Les émotions non régulées biaisent les décisions — colère → décisions punitives, peur → évitement",
        "confiance": "L'empathie et la conscience de soi construisent la sécurité psychologique de l'équipe"
     },
     "developper_ie": [
        "Journal de bord émotionnel : noter ses réactions après les situations difficiles",
        "Feedback 360 sur les comportements en situation de stress",
        "Pause avant de répondre en situation de charge émotionnelle",
        "Coaching ou thérapie pour explorer les schémas récurrents"
     ]},
    [{"prompt": "Je perds souvent mon calme en réunion et ça nuit à mon autorité. Que faire ?",
      "answer": "D'abord identifier les déclencheurs : quelles situations, quels types de commentaires ou comportements déclenchent la réaction ? Tenir un journal après chaque incident. Ensuite créer de l'espace : technique simple — respiration 4-7-8 (inspirer 4s, retenir 7s, expirer 8s) active le système parasympathique en 30 secondes. En réunion : \"je vais prendre un moment\" est un signe de maturité, pas de faiblesse. Long terme : le coaching ou la supervision managériale aide à travailler les schémas récurrents — la maîtrise de soi se développe, elle n'est pas figée."},
     {"prompt": "Est-ce qu'un leader doit montrer ses émotions ?",
      "answer": "Oui — de façon calibrée. Cacher systématiquement ses émotions crée de la distance et réduit la confiance. Les montrer sans filtre crée de l'instabilité et de l'anxiété. L'équilibre : nommer l'émotion sans la laisser piloter le comportement. \"Je suis déçu par ce résultat et je veux qu'on comprenne ce qui s'est passé\" — c'est de la transparence émotionnelle, pas de la réactivité. L'authenticité émotionnelle du leader est l'un des prédicteurs les plus forts de la sécurité psychologique de l'équipe."}],
    {"tone": "psychologique, bienveillant, pragmatique",
     "structure": ["5 dimensions", "impact leadership", "développer"],
     "avoid": ["confondre empathie et faiblesse", "présenter l'IE comme innée"]},
    ["intelligence émotionnelle", "Goleman", "leadership", "empathie", "conscience de soi", "régulation émotionnelle"]
))

# 6 ─ Délégation efficace
save(f"{BASE}/delegation_efficace.json", ku(
    "knowledges.professional.leadership.delegation_efficace",
    "Délégation efficace — donner du pouvoir sans perdre le contrôle",
    "high",
    "Comment déléguer intelligemment : choisir quoi déléguer et à qui, fixer le cadre, suivre sans micro-manager, et développer l'autonomie de l'équipe.",
    "La délégation efficace est le transfert planifié d'une responsabilité à une personne avec le niveau d'autorité, les ressources et le contexte nécessaires pour réussir — en maintenant la redevabilité sans exercer de micro-management.",
    {"quoi_deleguer": {
        "pas_delegable": "Décisions stratégiques qui engagent l'organisation, feedback difficile sur la personne, situations de crise",
        "delegable": "Tâches récurrentes que quelqu'un peut faire aussi bien ou mieux, projets qui développent quelqu'un, décisions opérationnelles dans un périmètre clair"
     },
     "a_qui": {
        "criteres": "Compétence pour la tâche + motivation à faire + capacité disponible",
        "opportunite_dev": "Déléguer légèrement au-dessus du niveau actuel développe — déléguer trop au-dessus détruit la confiance"
     },
     "processus": [
        "1. Clarifier le résultat attendu (pas la méthode)",
        "2. Donner le contexte (pourquoi c'est important, qui est impacté)",
        "3. Définir les checkpoints — ni trop fréquents (micro-management) ni trop rares (perte de contrôle)",
        "4. Donner l'autorité nécessaire pour agir sans revenir demander à chaque étape"
     ],
     "pieges": {
        "delegation_inversee": "La personne revient avec chaque problème au lieu de décider — lui renvoyer la question : 'Qu'est-ce que tu recommanderais ?'",
        "micro_management": "Vérifier trop souvent détruit la motivation et la confiance — fixer des checkpoints et s'y tenir",
        "abandon": "Déléguer sans suivi ni soutien — la personne se retrouve seule face à des obstacles qu'elle ne peut pas surmonter"
     }},
    [{"prompt": "Comment déléguer sans que tout revienne sur mon bureau ?",
      "answer": "La délégation inversée (reverse delegation) est le problème le plus courant. La cause : la personne n'a pas assez de clarté sur son périmètre de décision, ou elle a appris que vous reprenez le dossier si elle attend. Solution : quand quelqu'un arrive avec un problème, poser systématiquement la question 'Qu'est-ce que tu recommanderais ?' avant de donner ton avis. Deuxièmement, définir explicitement les niveaux d'autorité : décide seul, décide et informe, propose et attends validation — clarifier quel niveau s'applique à chaque type de décision."},
     {"prompt": "J'ai du mal à lâcher le contrôle. Comment apprendre à faire confiance ?",
      "answer": "La difficulté à déléguer vient souvent d'une croyance implicite : 'personne ne fera aussi bien que moi'. C'est vrai à court terme — et ça crée un goulot d'étranglement sur vous à long terme. Pratique : commencer par déléguer des tâches à faible enjeu pour calibrer le niveau de confiance, puis augmenter progressivement. Chaque délégation réussie construit la confiance mutuellement. Se poser la question : 'Si je ne délègue pas ça, qu'est-ce que je ne fais pas à la place ?' — souvent la réponse est du travail stratégique qui attend."}],
    {"tone": "pragmatique, orienté autonomisation de l'équipe",
     "structure": ["quoi déléguer", "à qui", "processus", "pièges"],
     "avoid": ["trop théorique", "ignorer la dimension confiance"]},
    ["délégation", "autonomie", "management", "micro-management", "leadership", "développement équipe"]
))

# 7 ─ Motivation et engagement d'équipe
save(f"{BASE}/motivation_engagement_equipe.json", ku(
    "knowledges.professional.leadership.motivation_engagement_equipe",
    "Motivation et engagement d'équipe — comprendre et activer les leviers",
    "high",
    "Théories de la motivation (Maslow, Herzberg, autodétermination) et leviers pratiques pour maintenir l'engagement de l'équipe dans la durée.",
    "La motivation en contexte professionnel est l'ensemble des forces internes et externes qui déclenchent et maintiennent les comportements orientés vers un objectif — un leader qui comprend ces leviers peut créer les conditions de l'engagement sans avoir à 'motiver' artificiellement son équipe.",
    {"theories": {
        "maslow": "Pyramide des besoins — physiologique → sécurité → appartenance → estime → réalisation. En milieu pro : les besoins de base doivent être satisfaits pour que les supérieurs puissent être activés",
        "herzberg": "Facteurs d'hygiène (salaire, conditions) empêchent l'insatisfaction mais ne créent pas de motivation. Facteurs motivants (responsabilité, reconnaissance, progression) créent l'engagement",
        "autodetermination": "Deci & Ryan — 3 besoins universels : autonomie (choisir comment), compétence (progresser), appartenance (compter pour quelqu'un)"
     },
     "leviers_pratiques": {
        "autonomie": "Laisser de la flexibilité sur le comment, pas seulement le quoi",
        "maitrise": "Donner des défis légèrement au-dessus du niveau actuel — la zone proximale de développement",
        "sens": "Connecter les tâches à l'impact réel sur des personnes réelles",
        "reconnaissance": "Spécifique, rapide, sincère — pas un \"bon boulot\" générique",
        "appartenance": "Créer des rituels d'équipe, célébrer les victoires collectives, construire la confiance interpersonnelle"
     },
     "demotivateurs_a_eviter": [
        "Changer de direction sans expliquer",
        "Attribuer des succès à d'autres ou individualiser des échecs collectifs",
        "Ignorer les contributions",
        "Micro-manager sans raison apparente"
     ]},
    [{"prompt": "Mon équipe semble démotivée depuis quelques semaines. Par où commencer ?",
      "answer": "Diagnostiquer avant d'agir. Trois questions en entretien individuel : 1) 'Qu'est-ce qui te donne de l'énergie dans ton travail en ce moment ?' 2) 'Qu'est-ce qui te freine ou te pèse ?' 3) 'Qu'est-ce que tu aimerais que j'arrête, commence, ou continue ?' La démotivation collective a souvent une cause précise : changement organisationnel non expliqué, injustice perçue, manque de reconnaissance, ou simplement surcharge. Identifier la cause avant d'apporter une solution générique."},
     {"prompt": "La reconnaissance financière ne suffit plus à fidéliser mon équipe. Quels autres leviers ?",
      "answer": "Herzberg l'avait montré dès les années 60 : le salaire est un facteur d'hygiène — en-dessous d'un seuil il démotive, au-dessus il ne motive pas durablement. Les leviers qui créent l'engagement sont la progression (apprendre et maîtriser de nouvelles compétences), l'autonomie (avoir voix au chapitre sur comment travailler), le sens (voir l'impact de son travail), et la reconnaissance qualitative (être vu et nommé pour sa contribution spécifique). Concrètement : des 1:1 réguliers pour comprendre les aspirations de chacun, des missions qui font monter en compétence, et de la visibilité sur les succès."}],
    {"tone": "psychologique, fondé, orienté pratique",
     "structure": ["théories", "leviers pratiques", "démotivateurs"],
     "avoid": ["confondre satisfaction et motivation", "solutions gadget (baby-foot, pizza)"]},
    ["motivation", "engagement", "Herzberg", "autodétermination", "Maslow", "leadership", "rétention"]
))

# 8 ─ Communication du leader
save(f"{BASE}/communication_leader.json", ku(
    "knowledges.professional.leadership.communication_leader",
    "Communication du leader — adapter son message selon les contextes",
    "high",
    "Techniques de communication pour les leaders : pitcher une vision, annoncer une mauvaise nouvelle, conduire un 1:1, présenter à la direction et communiquer en période de changement.",
    "La communication du leader est l'art d'adapter son message, son canal et son registre selon l'interlocuteur et le contexte pour créer de la clarté, de la confiance et de l'alignement.",
    {"contextes_cles": {
        "vision_equipe": "Court, concret, inspirant — 3 points max. Terminer par 'Qu'est-ce qui vous préoccupe ?'",
        "mauvaise_nouvelle": "Directement et rapidement — ne pas faire durer l'incertitude. Contexte → fait → impact → étapes suivantes",
        "1_1": "Écouter d'abord (60% du temps) avant de partager → créer de la sécurité psychologique",
        "comite_direction": "Bottom line up front (BLUF) — la conclusion d'abord, les détails ensuite",
        "email_important": "Sujet = action attendue. Corps = contexte court + demande claire + deadline"
     },
     "ecoute_active": {
        "techniques": ["Reformuler avant de répondre", "Poser des questions ouvertes", "Résister à l'envie de compléter les phrases"],
        "signaux": "Croiser les bras, regarder son téléphone, répondre trop vite — signaux négatifs perçus immédiatement"
     },
     "communication_changement": {
        "courbe_changement": "Annonce → Choc → Résistance → Exploration → Intégration — chaque phase demande un message différent",
        "erreur_frequente": "Communiquer une seule fois et croire que c'est suffisant — répéter 7 fois dans des formats différents",
        "transparence": "Dire 'je ne sais pas encore' vaut mieux que de promettre ce qu'on ne peut pas tenir"
     }},
    [{"prompt": "Comment annoncer un changement difficile à mon équipe ?",
      "answer": "Structure en 4 temps : 1) Contexte — pourquoi ce changement maintenant, quelles forces l'ont rendu nécessaire. 2) Ce qui change concrètement — être précis, pas de langage euphémisé. 3) Ce qui ne change pas — l'équipe a besoin de points d'ancrage stables. 4) Étapes suivantes et comment l'équipe peut contribuer. Ensuite : ouvrir le dialogue. 'Quelles questions avez-vous ?' pas 'Des questions ?' Prévoir plusieurs sessions, pas une seule annonce. Les questions qui reviennent 3 semaines après sont normales — le changement se digère en plusieurs étapes."},
     {"prompt": "Je dois présenter à mon CODIR pour la première fois. Comment me préparer ?",
      "answer": "Règle BLUF (Bottom Line Up Front) : donner la conclusion en première phrase, pas à la fin. Format idéal : 'La situation est X. La décision que je vous soumets est Y. Les alternatives écartées sont Z1 et Z2 parce que [une ligne chacune]. Si vous approuvez, les prochaines étapes sont A et B.' Anticiper les 3 questions les plus probables et avoir les réponses prêtes. Le CODIR n'a pas le temps — donner d'abord ce qu'ils ont besoin de savoir pour décider, les détails viennent ensuite si on les demande."}],
    {"tone": "pratique, orienté situations concrètes",
     "structure": ["contextes clés", "écoute active", "communication changement"],
     "avoid": ["trop générique", "ignorer la dimension non-verbale"]},
    ["communication", "leadership", "BLUF", "1:1", "conduite du changement", "présentation"]
))

# 9 ─ Développement des talents
save(f"{BASE}/developpement_talents.json", ku(
    "knowledges.professional.leadership.developpement_talents",
    "Développement des talents — faire grandir son équipe",
    "high",
    "Stratégies pour identifier et développer les potentiels dans l'équipe : plans de développement individuels, mentoring, stretch assignments, gestion des hauts potentiels et des underperformers.",
    "Le développement des talents est la responsabilité du leader de créer les conditions pour que chaque membre de son équipe progresse — en combinant des défis adaptés, du feedback, du soutien et des opportunités d'apprentissage.",
    {"identifier_potentiel": {
        "haut_potentiel": "Performance actuelle élevée + capacité à performer à un niveau supérieur + aspiration à grandir — les trois réunis",
        "piege": "Confondre haute performance et haut potentiel — un expert technique excellent n'est pas forcément un futur leader"
     },
     "leviers_developpement": {
        "70_20_10": "70% apprentissage par l'expérience (stretch assignments), 20% par les autres (mentoring, feedback), 10% formation formelle",
        "stretch_assignment": "Donner une mission légèrement au-dessus du niveau actuel — crée de l'apprentissage, demande du soutien",
        "plan_dev_individuel": "Co-construit avec la personne : 1-2 objectifs de développement, actions concrètes, métriques, timeline 6 mois",
        "mentoring": "Différent du management — relation volontaire, agenda piloté par le mentoré, pas d'évaluation"
     },
     "underperformers": {
        "diagnostic": "Comprendre d'abord : manque de compétence (formation), de clarté (feedback), de motivation (conversation), ou de fit (réorientation)",
        "plan_amelioration": "PIP (Performance Improvement Plan) — objectifs précis, timeline court, suivi hebdomadaire — outil de soutien, pas de punition",
        "decision_finale": "Si après soutien sincère ça ne change pas : la décision de séparer est aussi un acte de leadership"
     }},
    [{"prompt": "Comment identifier qui a du potentiel dans mon équipe ?",
      "answer": "La matrice performance/potentiel (9-box) est un outil utile mais imparfait. Deux dimensions à distinguer : la performance actuelle (observable, mesurable) et le potentiel (capacité à performer dans un rôle plus complexe). Indicateurs de potentiel : apprend vite de nouvelles compétences hors de sa zone de confort, crée des solutions nouvelles plutôt que de reproduire ce qu'il sait faire, influence sans autorité formelle, cherche activement du feedback. Attention au biais de similarité : on a tendance à voir du potentiel chez ceux qui nous ressemblent."},
     {"prompt": "Un membre de mon équipe sous-performe depuis 2 mois. Que faire ?",
      "answer": "Diagnostic avant action : 1) Est-ce qu'il sait exactement ce qu'on attend de lui ? (clarté des objectifs — souvent la cause n°1). 2) A-t-il les ressources et compétences nécessaires ? (formation, soutien). 3) Est-ce qu'il le veut — y a-t-il un problème de motivation ou une situation personnelle ? Chaque cause appelle une réponse différente. Si les trois sont ok et que ça ne change pas : feedback direct, plan d'amélioration avec objectifs mesurables et timeline, puis décision. Ne pas attendre 6 mois — la sous-performance prolongée démotive le reste de l'équipe."}],
    {"tone": "développemental, pragmatique, bienveillant mais direct",
     "structure": ["identifier", "leviers", "underperformers"],
     "avoid": ["ignorer la dimension humaine", "confondre performance et potentiel"]},
    ["talent", "développement", "mentoring", "potentiel", "performance", "leadership", "70-20-10"]
))

# 10 ─ Leadership en période de crise
save(f"{BASE}/leadership_crise.json", ku(
    "knowledges.professional.leadership.leadership_crise",
    "Leadership en période de crise — guider quand tout est incertain",
    "high",
    "Comment un leader navigue les crises organisationnelles, projets ou humaines : décision rapide sous incertitude, communication, stabilisation émotionnelle et reconstruction.",
    "Le leadership en crise est la capacité à maintenir la direction et la confiance de l'équipe dans des situations d'incertitude, de pression extrême ou de danger — en équilibrant la rapidité de décision avec la communication et le soin aux personnes.",
    {"phases_crise": {
        "choc": "Première 24-48h — stabiliser, évaluer, communiquer rapidement même avec peu d'informations",
        "gestion": "Semaines suivantes — décisions sous incertitude, maintenir l'équipe focalisée",
        "reconstruction": "Après la crise — tirer les leçons, reconstruire la confiance, transformer en apprentissage"
     },
     "principes_leadership_crise": [
        "Présence physique et émotionnelle — pas l'heure du remote",
        "Transparence sur ce qu'on sait, ce qu'on ne sait pas, et quand on communiquera à nouveau",
        "Décision sans toutes les informations — accepter 70% de certitude pour agir plutôt qu'attendre 100%",
        "Protéger l'équipe de la surcharge d'informations anxiogènes",
        "Prendre soin de soi — un leader épuisé prend de mauvaises décisions"
     ],
     "communication_crise": {
        "frequence": "Plus souvent que d'habitude — combler le vide d'information crée des rumeurs",
        "format": "Court, factuel, ancré dans ce qu'on peut contrôler",
        "emotions": "Reconnaître l'anxiété de l'équipe sans l'amplifier — 'je comprends que c'est difficile, voilà ce qu'on fait'"
     },
     "erreurs_frequentes": [
        "Disparaître ou se sur-contrôler — les deux extrêmes",
        "Promettre ce qu'on ne peut pas garantir pour calmer",
        "Négliger les besoins émotionnels de l'équipe au profit du plan opérationnel"
     ]},
    [{"prompt": "Mon projet est en crise et l'équipe panique. Comment reprendre le contrôle ?",
      "answer": "Trois actions immédiates : 1) Réunir l'équipe pour nommer clairement la situation — pas d'euphémismes, pas de catastrophisme non plus. 2) Clarifier ce qu'on peut contrôler vs ce qu'on ne peut pas — focaliser toute l'énergie sur le premier. 3) Définir les prochaines 24-48h uniquement — en crise, l'horizon se raccourcit. La panique collective se calme quand les gens ont quelque chose de concret à faire. Désigner qui fait quoi ce soir et demain matin crée de l'ordre dans le chaos."},
     {"prompt": "Comment garder le moral de l'équipe sur un projet qui ne se passe pas bien ?",
      "answer": "Quatre leviers : 1) Communiquer honnêtement — l'équipe supporte mieux la vérité difficile que l'incertitude prolongée. 2) Célébrer les micro-victoires — dans les projets difficiles, les moments positifs doivent être amplifiés. 3) Protéger l'équipe de la pression venue du haut — amortir les turbulences plutôt que les retransmettre amplifiées. 4) Donner de la visibilité sur la fin — 'on sait qu'il reste X semaines difficiles, après quoi on aura une pause' crée de l'endurance. Le moral ne se manage pas directement — il se construit par la confiance, la clarté et la solidarité."}],
    {"tone": "calme, ancré, orienté action et soin aux personnes",
     "structure": ["phases", "principes", "communication", "erreurs"],
     "avoid": ["héroïsme fictif", "ignorer la dimension humaine"]},
    ["crise", "leadership", "incertitude", "communication de crise", "gestion de projet", "résilience"]
))

# 11 ─ Décision sous incertitude
save(f"{BASE}/decision_sous_incertitude.json", ku(
    "knowledges.professional.leadership.decision_sous_incertitude",
    "Décision sous incertitude — agir sans toutes les informations",
    "high",
    "Frameworks pour prendre des décisions rapides et réversibles en situation d'incertitude : OODA loop, decision journal, biais cognitifs à surveiller et techniques de prémortem.",
    "La décision sous incertitude est l'art de choisir une direction d'action acceptable en l'absence d'information complète, en minimisant les risques d'erreur irréversible tout en évitant la paralysie.",
    {"frameworks": {
        "OODA": "Observer → Orienter (interpréter) → Décider → Agir → reboucler. Développé par John Boyd pour les combats aériens — s'applique aux situations de haute incertitude et rapidité",
        "premortem": "Avant de décider, imaginer que la décision a échoué 1 an plus tard — lister toutes les causes possibles d'échec. Réduit l'optimisme biaisé",
        "reversibilite": "Distinguer les décisions réversibles (agir vite, corriger si nécessaire) des irréversibles (prendre le temps). Jeff Bezos : portes à une entrée vs portes à deux entrées",
        "70_percent_rule": "Amazone : si on a 70% des informations nécessaires, décider. Attendre 90% coûte plus cher que de corriger une décision imparfaite"
     },
     "biais_a_surveiller": {
        "confirmation": "Chercher des informations qui confirment la décision déjà prise",
        "ancrage": "Rester bloqué sur la première information reçue",
        "sunk_cost": "Continuer parce qu'on a déjà beaucoup investi — la meilleure décision future est indépendante du passé",
        "groupthink": "Le groupe converge vers une décision sans la challenger suffisamment"
     },
     "decision_journal": "Documenter les décisions importantes : contexte, options considérées, rationale, résultat attendu. Relire 6 mois après pour calibrer son jugement"},
    [{"prompt": "Je dois prendre une décision importante mais je n'ai pas assez d'informations. Que faire ?",
      "answer": "D'abord : est-ce une décision réversible ou irréversible ? Pour les décisions réversibles, activer rapidement — décider avec 60-70% des informations et corriger si nécessaire. Pour les irréversibles, investir dans l'information : quel serait le coût de 2 semaines supplémentaires d'analyse vs le coût d'une mauvaise décision irréversible ? Technique prémortem : imaginer que dans 1 an cette décision a mal tourné — qu'est-ce qui s'est passé ? Cette visualisation fait émerger les risques cachés avant d'agir."},
     {"prompt": "Comment éviter de mauvaises décisions dues à mes biais cognitifs ?",
      "answer": "Trois pratiques : 1) Devil's advocate — désigner quelqu'un dont le rôle est de challenger la décision avant d'aller de l'avant. 2) Pre-mortem avant chaque décision importante — imaginer l'échec et en lister les causes. 3) Decision journal — écrire le rationale de la décision au moment où on la prend, puis relire les résultats 6-12 mois après pour calibrer son intuition. Les biais ne disparaissent pas avec la conscience qu'on les a — les processus structurés qui forcent à les contourner sont plus efficaces que la seule vigilance mentale."}],
    {"tone": "analytique, fondé sur des frameworks éprouvés",
     "structure": ["frameworks", "biais", "journal"],
     "avoid": ["recettes magiques", "ignorer l'incertitude irréductible"]},
    ["décision", "incertitude", "OODA", "prémortem", "biais cognitifs", "leadership", "Jeff Bezos"]
))

# 12 ─ Construction et cohésion d'équipe
save(f"{BASE}/construction_cohesion_equipe.json", ku(
    "knowledges.professional.leadership.construction_cohesion_equipe",
    "Construction et cohésion d'équipe — les 5 dysfonctions et comment les éviter",
    "high",
    "Framework de Patrick Lencioni sur les 5 dysfonctions d'une équipe, et pratiques pour construire la confiance, la sécurité psychologique et la cohésion.",
    "La construction d'une équipe performante est un processus délibéré qui passe par la confiance interpersonnelle, le conflit sain, l'engagement collectif, la redevabilité mutuelle et l'attention collective aux résultats — dans cet ordre.",
    {"5_dysfonctions_lencioni": {
        "pyramide": "Les dysfonctions sont cumulatives — chaque niveau bloque les suivants",
        "1_manque_confiance": "Peur de la vulnérabilité — les gens cachent leurs faiblesses. Solution : exercices de vulnérabilité, histories personnelles",
        "2_peur_conflit": "Éviter les désaccords au profit de l'harmonie artificielle. Solution : nommer les désaccords, \"mineur\" ou \"majeur\"",
        "3_manque_engagement": "Sans débat, pas d'adhésion réelle — les décisions sont acceptées en réunion et sabotées après. Solution : clarifier les décisions en fin de réunion",
        "4_evitement_redevabilite": "Personne n'ose pointer les underperformers pour ne pas créer de tension. Solution : revues de performances par pairs",
        "5_inattention_resultats": "Prioriser l'ego et le statut individuel sur les résultats collectifs. Solution : scoreboard public, récompenses collectives"
     },
     "securite_psychologique": {
        "reference": "Amy Edmondson — Google Project Aristotle",
        "definition": "Sentiment que l'équipe est un endroit sûr pour prendre des risques interpersonnels — poser des questions, admettre des erreurs, exprimer des désaccords",
        "construire": ["Montrer sa propre vulnérabilité en premier", "Traiter les erreurs comme des apprentissages", "Remercier ceux qui soulèvent des problèmes"]
     },
     "rituels_cohesion": [
        "Rétrospective régulière (mensuelle) sur le fonctionnement de l'équipe",
        "Temps informel structuré (pas obligatoire, mais facilité)",
        "Célébration collective des succès — pas seulement individuelle"
     ]},
    [{"prompt": "Mon équipe manque de cohésion. Par où commencer ?",
      "answer": "Utiliser la pyramide de Lencioni comme diagnostic : est-ce que les gens de l'équipe se font confiance au niveau interpersonnel (vulnérabilité) ? Est-ce qu'ils débattent franchement des idées ? Est-ce qu'ils respectent les engagements mutuels ? Commencer par la base : la confiance. Activité simple : chaque personne partage 3 éléments sur son parcours personnel ou professionnel que les autres ne savent pas. Ça semble basique — mais l'humanisation des collègues réduit la méfiance plus vite qu'un team building artificiel."},
     {"prompt": "C'est quoi la sécurité psychologique et comment la créer ?",
      "answer": "Amy Edmondson (Google Project Aristotle) : la sécurité psychologique est le sentiment que l'équipe est un endroit sûr pour prendre des risques interpersonnels — poser une question 'stupide', admettre une erreur, proposer une idée non conventionnelle, exprimer un désaccord. Trois pratiques du leader pour la créer : 1) Montrer sa propre vulnérabilité en premier ('j'ai fait une erreur sur ce dossier, voilà ce que j'en tire'). 2) Traiter les erreurs comme des apprentissages collectifs plutôt que des fautes individuelles. 3) Remercier explicitement ceux qui soulèvent des problèmes avant qu'ils ne s'aggravent."}],
    {"tone": "fondé, ancré dans la recherche (Lencioni, Edmondson)",
     "structure": ["5 dysfonctions", "sécurité psychologique", "rituels"],
     "avoid": ["team building superficiel", "ignorer la dimension psychologique"]},
    ["cohésion", "équipe", "Lencioni", "sécurité psychologique", "confiance", "leadership", "Edmondson"]
))

# 13 ─ Influence sans autorité
save(f"{BASE}/influence_sans_autorite.json", ku(
    "knowledges.professional.leadership.influence_sans_autorite",
    "Influence sans autorité — convaincre sans pouvoir formel",
    "high",
    "Techniques pour influencer des pairs, des partenaires et la hiérarchie sans autorité directe : crédibilité, coalition, réciprocité, storytelling et principes de Cialdini.",
    "L'influence sans autorité est la capacité à obtenir la coopération et l'action d'autres personnes sans avoir de lien hiérarchique direct — en s'appuyant sur la crédibilité, la relation et la persuasion.",
    {"principes_cialdini": {
        "reciprocite": "Donner en premier — aide, information, reconnaissance — crée une obligation sociale naturelle",
        "credibilite": "Expertise + honnêteté = autorité perçue. Reconnaître ses limites augmente la crédibilité sur le reste",
        "coherence": "Les gens résistent à changer d'avis — obtenir un petit accord d'abord facilite l'accord plus grand",
        "preuve_sociale": "Montrer que d'autres ont adopté la même position — 'les équipes X et Y l'ont testé avec ce résultat'",
        "sympathie": "On est influencé par ceux qu'on apprécie — investir dans la relation avant d'avoir besoin d'influence",
        "rarete": "Ce qui est limité ou exclusif est perçu comme plus précieux"
     },
     "pratiques": {
        "comprendre_avant_convaincre": "Cartographier les intérêts de la personne — trouver le chevauchement avec les siens",
        "framing": "Présenter la même réalité selon le cadre de référence de l'interlocuteur",
        "coalition": "Construire des alliances avant la réunion décisive — pas de surprises",
        "storytelling": "Les données convainquent le rationnel, les histoires convainquent le tout"
     }},
    [{"prompt": "Je dois convaincre un pair d'une autre équipe de changer ses priorités. Par où commencer ?",
      "answer": "Avant de convaincre, comprendre. Quels sont ses objectifs à lui ? Quelle est la pression qu'il ressent ? L'influence commence par la compréhension des intérêts de l'autre — pas par l'exposition des siens. Trouver le chevauchement : comment ma demande peut-elle servir ses objectifs à lui aussi ? Ensuite : reciprocité — ai-je déjà donné quelque chose à cette personne (aide, information, visibilité) ? Si non, c'est le moment d'investir. La demande d'influence sur un compte à zero a peu de chances d'aboutir."},
     {"prompt": "Comment présenter une idée à la direction sans pouvoir formel ?",
      "answer": "SCQA (Situation → Complication → Question → Answer) — structure narrative qui crée la tension puis la résout. Commencer par ce que la direction sait déjà (Situation), introduire le problème nouveau (Complication), poser la question que ça soulève, puis présenter la réponse (votre idée). Avant la réunion : identifier qui dans la salle est potentiellement allié et lui parler en bilatéral pour prendre sa température. La preuve sociale est puissante : 'j'ai discuté avec X et Y, ils voient la même opportunité' — vous n'êtes plus seul à pousser."}],
    {"tone": "stratégique, ancré dans la psychologie sociale",
     "structure": ["Cialdini", "pratiques", "coalition"],
     "avoid": ["manipulation", "ignorer l'importance de la relation"]},
    ["influence", "persuasion", "Cialdini", "autorité", "leadership", "coalition", "storytelling"]
))

# 14 ─ Inclusion et diversité dans l'équipe
save(f"{BASE}/inclusion_diversite.json", ku(
    "knowledges.professional.leadership.inclusion_diversite",
    "Inclusion et diversité — créer un environnement où chacun peut contribuer",
    "medium",
    "Comment un leader crée activement un environnement inclusif : reconnaître les biais inconscients, amplifier les voix sous-représentées, et transformer la diversité en avantage de performance.",
    "L'inclusion est le sentiment de chaque membre de l'équipe d'être à sa place, valorisé et capable de contribuer pleinement — la diversité sans inclusion produit de la tension sans bénéfice de performance.",
    {"distinction": {
        "diversite": "Représentation — avoir des personnes avec des profils différents dans l'équipe",
        "inclusion": "Appartenance + valorisation — ces personnes contribuent pleinement et sont entendues",
        "equite": "Adapter les ressources et opportunités selon les besoins — pas traiter tout le monde identiquement"
     },
     "biais_inconscients": {
        "affinite": "Favoriser les personnes qui nous ressemblent",
        "attribution": "Attribuer les succès aux qualités des uns et les erreurs aux qualités des autres (selon le groupe)",
        "micro_agressions": "Commentaires apparemment anodins qui signalent une non-appartenance",
        "amplification": "Les idées des membres sous-représentés sont plus souvent attribuées à d'autres ou ignorées"
     },
     "pratiques_inclusives": [
        "Tour de table structuré en réunion — pas seulement les voix qui s'imposent",
        "Amplifier explicitement les contributions ('comme X l'a dit...')",
        "Mentorat inversé — apprendre des membres les moins expérimentés ou les plus différents",
        "Feedback 360 qui inclut une dimension inclusion",
        "Objectifs de recrutement et de promotion conscients et documentés"
     ]},
    [{"prompt": "Mon équipe est diverse sur le papier mais certains membres ne s'expriment jamais. Pourquoi ?",
      "answer": "Plusieurs causes possibles : barrière de la sécurité psychologique (peur d'être jugé), dynamique de réunion qui avantage les profils extravertis ou les personnes du groupe dominant, ou expériences passées où leurs contributions n'ont pas été prises en compte. Solutions concrètes : tour de table structuré en début de réunion (chacun a 2 min), envoyer l'ordre du jour à l'avance pour permettre la préparation, créer des moments de réflexion écrite avant la discussion orale — avantage les introvertis et les non-natifs de la langue de réunion."},
     {"prompt": "Comment traiter un commentaire inapproprié en réunion sans créer de conflit ?",
      "answer": "Technique du 'pause and name' : marquer une pause courte et nommer ce qui s'est passé calmement. 'Je veux qu'on s'arrête un instant — ce commentaire ne représente pas la façon dont on travaille ici.' Pas de longue explication, pas de honte publique — juste une ligne claire posée par le leader. Si le commentaire visait une personne, la vérifier en bilatéral après la réunion. Un leader qui ne dit rien en pareille situation envoie un signal très fort à l'ensemble de l'équipe sur ce qui est acceptable."}],
    {"tone": "pragmatique, sans idéologie excessive, orienté performance et équité",
     "structure": ["distinction", "biais", "pratiques"],
     "avoid": ["moralisateur", "trop abstrait", "confondre équité et égalité"]},
    ["inclusion", "diversité", "biais inconscients", "leadership", "équité", "sécurité psychologique"]
))

# 15 ─ Leadership à distance et hybride
save(f"{BASE}/leadership_distance_hybride.json", ku(
    "knowledges.professional.leadership.leadership_distance_hybride",
    "Leadership à distance et hybride — manager sans présence physique",
    "high",
    "Adaptation du leadership au travail à distance et hybride : maintenir la confiance, la cohésion et la performance sans présence physique quotidienne.",
    "Le leadership à distance est l'exercice des fonctions de leadership dans un contexte où les interactions sont principalement asynchrones et médiatisées par des outils numériques — demandant une sur-communication délibérée et une confiance fondée sur les résultats plutôt que la présence.",
    {"defis_specifiques": {
        "visibilite": "Les contributions sont moins visibles — risque d'oubli des profils moins proactifs",
        "cohesion": "Les liens informels ne se créent pas naturellement — doivent être orchestrés",
        "confiance": "Plus difficile à construire sans les signaux non-verbaux — demande plus de temps et de transparence",
        "sante_mentale": "Isolement, surcharge numérique, flou work/life — risques spécifiques au remote"
     },
     "pratiques_efficaces": {
        "1_1_reguliers": "Hebdomadaires, 30 min, agenda piloté par le collaborateur — ne jamais annuler",
        "sur_communication": "En remote, communiquer 3x plus qu'en présentiel sur les décisions, le contexte, les succès",
        "normes_equipe": "Définir collectivement : heures de disponibilité, temps de réponse attendu, outils par usage",
        "rituels_virtuels": "Stand-up quotidien optionnel, rétro mensuelle, célébrations vidéo — créer des points d'ancrage",
        "asynchrone_first": "Favoriser la documentation et les outils asynchrones — réduit la charge de réunions et les fuseaux horaires"
     },
     "hybride": {
        "equite": "Éviter le two-tier : les présentiels ne doivent pas avoir plus d'influence que les distants",
        "regle": "Si un est en remote, tous sont en remote — chacun sur sa propre caméra même si en salle",
        "temps_en_personne": "Réserver les moments physiques pour la cohésion, la créativité et les sujets complexes — pas pour le travail individuel"
     }},
    [{"prompt": "Comment maintenir la cohésion d'une équipe hybride ?",
      "answer": "Trois niveaux : 1) Rituels asynchrones — une mise à jour hebdomadaire partagée par écrit (\"ce que j'ai fait, ce que je fais, ce qui me bloque\") crée de la visibilité sans réunion. 2) Moments synchrones dédiés à la relation — 15 min en début de réunion pour un échange non-professionnel, sans agenda. 3) Temps en présentiel concentré sur ce que le remote ne peut pas faire : débats créatifs, cohésion, décisions complexes. Éviter le piège de l'équité de temps (même nombre de jours pour tout le monde) plutôt que l'équité d'impact (accès identique aux opportunités et à la visibilité)."},
     {"prompt": "Je ne sais jamais si mon équipe remote travaille vraiment. Comment gérer ?",
      "answer": "Si la question se pose, c'est souvent un symptôme d'un manque de clarté sur les outputs attendus — pas réellement un problème de présence. Solution : passer des inputs (heures, présence) aux outputs (résultats mesurables). 'Cette semaine, le livrable est X, la qualité attendue est Y' — si X est livré au niveau Y, peu importe les heures. Si le doute persiste malgré des livrables clairs, c'est une conversation de confiance à avoir directement, pas un contrôle à mettre en place. Surveiller les symptômes réels : délais, qualité en baisse, engagement en réunion — pas les signaux de présence."}],
    {"tone": "pragmatique, orienté résultats et bien-être équipe",
     "structure": ["défis", "pratiques", "spécificités hybride"],
     "avoid": ["présentéisme déguisé", "ignorer les enjeux de santé mentale"]},
    ["leadership", "remote", "hybride", "télétravail", "management à distance", "cohésion", "asynchrone"]
))

print(f"\n=== professional/leadership : 15 KU créés ===")
