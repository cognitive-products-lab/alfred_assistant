"""
Nouveau domaine : knowledges/cognition/systeme_pensee/
Systeme de pensee a 2 vitesses (Kahneman) + heuristiques, biais, metacognition
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(stem, subdomain, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.cognition.{subdomain}.{stem}",
      "title": title,
      "domain": "cognition",
      "subdomain": subdomain,
      "status": "validated",
      "summary": summary,
      "core_definition": core_def,
      "knowledge": knowledge,
      "example_answers": examples,
      "response_guidance": {
        "tone": "intellectuellement rigoureux, concret et applique — liens directs avec la vie quotidienne et les decisions",
        "structure": ["expliquer le mecanisme", "illustrer avec un exemple vecu", "donner une technique de protection ou d'utilisation"],
        "avoid": ["trop academique", "ignorer les implications pratiques", "reduire la complexite a un simple slogan"]
      },
      "tags": tags + ["cognition", "psychologie"],
      "related_knowledge_units": []
    }

# ── 1. systeme_pensee / system1_system2 ──────────────────────────────────────
save("cognition/systeme_pensee/system1_system2.json", ku(
  "system1_system2", "systeme_pensee",
  "Systeme 1 et Systeme 2 — Penser vite et lentement (Kahneman)",
  "Daniel Kahneman distingue deux modes de pensee : le Systeme 1, rapide, automatique et intuitif ; et le Systeme 2, lent, delibere et analytique. Comprendre leurs interactions explique la majorite de nos erreurs de jugement et de nos biais.",
  "Le modele Systeme 1 / Systeme 2, formalise par Daniel Kahneman dans 'Thinking, Fast and Slow' (2011), distingue deux modes cognitifs : le Systeme 1 (rapide, automatique, intuitif, peu coûteux en effort) et le Systeme 2 (lent, delibere, analytique, coûteux en energie cognitive). Nos decisions resultent de l'interaction — souvent biaisee — de ces deux modes.",
  {
    "system1_characteristics": {
      "nature": "Automatique, rapide, inconscient",
      "triggers": "Perceptions directes, schemas familiés, emotions, heuristiques",
      "strengths": [
        "Tres rapide (< 200ms)",
        "Peu coûteux en energie cognitive",
        "Efficace pour les situations familières",
        "Tres bon en reconnaissance de schemas"
      ],
      "weaknesses": [
        "Sensible aux biais et aux illusions cognitives",
        "Confond facilite de traitement avec verite",
        "Mauvais en statistiques et probabilites",
        "Cree des impressions qui contaminent le Systeme 2"
      ],
      "examples": ["Reconnaitre un visage", "2+2 = ?", "Peur instantanee devant un serpent", "Lire une phrase simple"]
    },
    "system2_characteristics": {
      "nature": "Delibere, lent, conscient, coûteux",
      "triggers": "Demandes cognitives elevees, novices, situations de doute",
      "strengths": [
        "Peut analyser en profondeur",
        "Peut appliquer des regles logiques complexes",
        "Peut overrider le Systeme 1"
      ],
      "weaknesses": [
        "Paresseux — evite de se mobiliser si possible",
        "Ressource limitee (ego depletion)",
        "Souvent se contente de valider le Systeme 1 plutot que de verifier"
      ],
      "examples": ["Resoudre 17 x 24", "Remplir une declaration d'impots", "Analyser un contrat complexe", "Apprendre a conduire"]
    },
    "kahneman_key_insights": [
      "Le Systeme 2 se croit maitre mais est souvent ratificateur du Systeme 1",
      "La cognitive ease (facilite de traitement) fait croire a la verite — si c'est facile a lire, ca semble vrai",
      "Le Systeme 1 ne peut pas etre eteint — on peut seulement apprendre a le reconnaitre",
      "La fatigue cognitive degrade le Systeme 2 et nous laisse plus exposes aux biais"
    ]
  },
  [
    {"prompt": "Comment savoir si je suis en train de penser avec le Systeme 1 ou le Systeme 2 ?", "answer": "Signal cle : effort ressenti. Si la reponse vient immediatement sans effort — Systeme 1. Si tu dois vous concentrer, tenir plusieurs informations en tete, raisonner etape par etape — Systeme 2. Mais attention : le Systeme 1 donne ses reponses avec la meme confiance qu'elles soient correctes ou non. La confiance n'est donc pas un bon indicateur de fiabilite. Pour les decisions importantes, la question a se poser est 'est-ce que j'ai vraiment verifie ca ou j'ai juste eu l'impression que c'etait vrai ?'"},
    {"prompt": "Pourquoi est-ce qu'on fait souvent des erreurs evidentes apres coup ?", "answer": "Parce que 'evident apres coup' est du Systeme 2 en retrospective — mais au moment de la decision, le Systeme 1 avait deja produit une reponse rapide et le Systeme 2 l'a ratifiee sans verifier. C'est le biais de retrospection ('j'aurais du savoir'). En temps reel, sous pression ou sous charge cognitive, le Systeme 2 est paresseux ou epuise. Il cede a l'impression du Systeme 1. La seule protection : ralentir deliberement avant les decisions importantes, meme si la reponse semble evidente."}
  ],
  ["Kahneman", "Systeme 1", "Systeme 2", "intuition", "pensee rapide", "pensee lente"]
))

# ── 2. systeme_pensee / heuristiques ─────────────────────────────────────────
save("cognition/systeme_pensee/heuristiques.json", ku(
  "heuristiques", "systeme_pensee",
  "Heuristiques cognitives",
  "Les heuristiques sont des raccourcis mentaux que le Systeme 1 utilise pour produire des jugements rapides. La plupart du temps efficaces, elles echouent systematiquement dans certains contextes et produisent des biais predictibles.",
  "Les heuristiques cognitives sont des strategies mentales simplificatrices utilisees par le cerveau pour produire rapidement des jugements et des decisions, en substituant une question facile a une question difficile. Si elles sont efficaces en moyenne, elles introduisent des biais systematiques et predictibles dans les situations complexes ou statistiques.",
  {
    "major_heuristics": [
      {
        "name": "Heuristique de disponibilite",
        "mechanism": "Juger la probabilite d'un evenement par la facilite avec laquelle des exemples viennent en tete",
        "bias_produced": "Surestimation des evenements recents, frequemment reportes ou emotionnellement marques (crash avion vs mort en voiture)",
        "example": "Apres un reportage sur les requins, les gens surestiment le risque d'attaque"
      },
      {
        "name": "Heuristique de representativite",
        "mechanism": "Juger par similarite avec un prototype, en negligeant les probabilites de base",
        "bias_produced": "Neglect of base rate — trouver 'typique' prime sur 'probable'",
        "example": "Steve est timide et aime l'ordre — biblIOthecaire ou fermier ? On dit bibliothécaire mais il y a 20x plus de fermiers"
      },
      {
        "name": "Heuristique d'ancrage",
        "mechanism": "Partir d'un chiffre initial (l'ancre) et ajuster insuffisamment",
        "bias_produced": "Decisions fortement influencees par le premier chiffre entende",
        "example": "Negociation : le premier prix annonce influence massivement le resultat final"
      },
      {
        "name": "Heuristique d'affect",
        "mechanism": "Juger via la resonance emotionnelle — si ca semble bien, c'est probablement bon",
        "bias_produced": "Confusion entre ce qui est agreable et ce qui est vrai ou bon",
        "example": "Un medicament 'naturel' semble plus sur qu'un equivalent chimique"
      }
    ],
    "practical_implications": [
      "En marketing : l'ancrage prix explique pourquoi le premier prix affiche influence tout",
      "En recrutement : la disponibilite explique le favoritisme pour les candidats visuellement similaires a des succes passes",
      "En securite : la disponibilite explique la mauvaise allocation des budgets (reagir aux incidents recents, pas aux risques statistiques)"
    ]
  },
  [
    {"prompt": "Pourquoi j'ai plus peur de prendre l'avion que de conduire alors que la voiture est plus dangereuse ?", "answer": "C'est l'heuristique de disponibilite combinee au biais d'affect. Les crashs d'avion : (1) sont des evenements exceptionnels donc tres reportes, (2) genèrent des images dramatiques et emotionnellement intenses. Ces images viennent facilement en tete, donc le cerveau (Systeme 1) conclut 'c'est frequent'. Les accidents de voiture sont communs, diffus, peu dramatiques dans les medias — donc peu disponibles cognitivement meme s'ils tuent 70x plus. La solution n'est pas de 'forcer' la peur de la voiture — c'est de reconnaitre que ton sentiment de risque n'est pas calibre sur les statistiques."},
    {"prompt": "Comment le biais d'ancrage affecte mes negociations et comment m'en proteger ?", "answer": "Le biais d'ancrage est un des plus forts et des plus resiliants — meme quand on sait qu'il existe, on y est soumis. Protection : (1) Donner le premier chiffre (celui qui ancre prend l'avantage — choisir une ancre haute avec justification), (2) Si l'autre a ancre en premier : noter explicitement que tu rejettes son ancre avant de contreproposer ('votre point de depart ne correspond pas a ma valorisation — voici le mien'), (3) Faire une recherche independante avant la negociation pour avoir une ancre interne solide. L'ajustement sera toujours insuffisant — donc ancre haut si tu vends."}
  ],
  ["heuristiques", "biais", "disponibilite", "representativite", "ancrage", "affect"]
))

# ── 3. systeme_pensee / cognitive_biases_extended ────────────────────────────
save("cognition/systeme_pensee/cognitive_biases_extended.json", ku(
  "cognitive_biases_extended", "systeme_pensee",
  "Biais cognitifs — catalogue pratique",
  "Les biais cognitifs sont des ecarts systematiques et predictibles entre la pensee rationnelle ideale et la pensee reelle. Connaitre les principaux biais ne les elimine pas, mais permet de concevoir des strategies et des environnements qui les attenuent.",
  "Un biais cognitif est un ecart systematique, non aleatoire et predictible entre le raisonnement normatif (logique, statistique) et le jugement reel d'un individu, produit par les mecanismes heuristiques du Systeme 1. Les biais cognitifs sont universels, mais leur ampleur varie selon le contexte, la fatigue cognitive et l'expertise dans le domaine.",
  {
    "social_biases": [
      {"name": "Biais de confirmation", "description": "Rechercher et privilegier les informations qui confirment nos croyances existantes", "counter": "Demander explicitement : 'Qu'est-ce qui pourrait prouver que j'ai tort ?'"},
      {"name": "Biais d'attribution fondamentale", "description": "Expliquer les comportements des autres par leur caractere, le sien par les circonstances", "counter": "Se demander : 'Dans quelles circonstances j'aurais fait pareil ?'"},
      {"name": "Effet de halo", "description": "Une qualite positive (ou negative) colore le jugement de toutes les autres qualites", "counter": "Evaluer chaque dimension independamment"},
      {"name": "Biais endogroupe", "description": "Favoriser les membres de son groupe d'appartenance", "counter": "Diversifier les sources de recrutement et de validation"}
    ],
    "decision_biases": [
      {"name": "Biais du statu quo", "description": "Preference pour la situation actuelle meme si une alternative serait meilleure", "counter": "Reformuler : 'Est-ce que je choisirais activement le statu quo ?'"},
      {"name": "Cout irrecuperable (sunk cost)", "description": "Continuer une action parce qu'on a deja investi (argent, temps), meme si la continuer n'a plus de sens", "counter": "Se demander : 'Si je n'avais pas encore investi, est-ce que je commencerais ce projet aujourd'hui ?'"},
      {"name": "Biais d'optimisme", "description": "Sous-estimer systematiquement les risques et les delais, suestimer les benefices", "counter": "Reference class forecasting : regarder les taux historiques pour des projets similaires"},
      {"name": "Dunning-Kruger", "description": "Les experts sous-estiment leur competence ; les novices la surestiment", "counter": "Feedback externe regulier, calibration avec des experts"}
    ],
    "memory_biases": [
      {"name": "Biais de retrospection (hindsight)", "description": "Apres un evenement, croire qu'on aurait du le prevoir", "counter": "Documenter ses predictions AVANT les evenements"},
      {"name": "Peak-end rule", "description": "On se souvient d'une experience par son moment le plus intense et sa conclusion — pas sa moyenne", "counter": "Designer les fins d'experience avec soin (service client, reunions, formations)"}
    ]
  },
  [
    {"prompt": "Comment eviter le biais de confirmation dans mes analyses ?", "answer": "Quatre pratiques : (1) Red team delibere — chercher activement les arguments contre ta these avant de conclure ('Pre-mortem' de Gary Klein : imagine que ton projet a echoue dans 1 an — pourquoi ?'), (2) Sources heterogenes — lire des perspectives contradictoires, pas seulement les sources qui confirment, (3) Steel man, pas straw man — formuler l'argument adverse dans sa version la plus forte avant de le refuter, (4) Critere de falsifiabilite — 'qu'est-ce qui me ferait changer d'avis ?' Si tu ne peux pas repondre a cette question, c'est une croyance, pas une analyse."},
    {"prompt": "Je continue un projet qui va mal parce que j'ai deja beaucoup investi — qu'est-ce que je dois faire ?", "answer": "Tu es probablement victime du sunk cost fallacy. Test de clarification : 'Si je n'avais encore rien investi sur ce projet, est-ce que je le lancerais aujourd'hui ?' Si la reponse est non — l'investissement passe ne devrait pas entrer en compte dans ta decision. L'argent depense est parti, que tu continues ou non. La vraie question : est-ce que les gains futurs esperees justifient les coûts futurs encore a engager ? Si non, continuer pour 'ne pas avoir perdu pour rien' garantit de perdre encore plus. La decision difficile est souvent la bonne."}
  ],
  ["biais cognitifs", "confirmation", "sunk cost", "Dunning-Kruger", "retrospection"]
))

# ── 4. systeme_pensee / decision_making_cognitive ────────────────────────────
save("cognition/systeme_pensee/decision_making_cognitive.json", ku(
  "decision_making_cognitive", "systeme_pensee",
  "Prise de decision — approche cognitive",
  "La prise de decision efficace consiste a mobiliser le bon mode cognitif (Systeme 1 ou 2) selon le type de decision, a debiaser le processus, et a accepter que l'incertitude est irreductible. Les meilleures decisions ne garantissent pas les meilleurs resultats.",
  "La prise de decision cognitive est l'etude des processus mentaux par lesquels un individu choisit une action parmi plusieurs options, en examinant comment les biais, les heuristiques, l'incertitude et les cadres cognitifs influencent ces choix, et quels processus et structures permettent d'ameliorer la qualite des decisions.",
  {
    "decision_types": [
      {"type": "Reversible / low stakes", "best_mode": "Systeme 1 — aller vite, corriger en route", "examples": "Quel outil utiliser, quel restaurant choisir"},
      {"type": "Irreversible / high stakes", "best_mode": "Systeme 2 delibere — prendre le temps, debiaser", "examples": "Recruter, investir, changer de metier"},
      {"type": "Expertise domain", "best_mode": "Intuition d'expert (S1 calibre par l'experience)", "examples": "Medecin diagnostiquant une pattern connue, chess grandmaster"}
    ],
    "bezos_2x2": {
      "source": "Jeff Bezos, lettre aux actionnaires Amazon 1997",
      "type1": "Decisions de type 1 : irreversibles, consequentes — prendre beaucoup de temps",
      "type2": "Decisions de type 2 : reversibles, peu consequentes — decider vite et corriger"
    },
    "debiasing_techniques": [
      "Pre-mortem (Klein) : imaginer l'echec avant de commencer et identifier pourquoi",
      "Distanciation : 'Qu'est-ce que je conseilerais a un ami dans cette situation ?'",
      "Consider the opposite : forcer le generation d'arguments contra",
      "Reference class forecasting : regarder les taux de base historiques",
      "10-10-10 rule (Suzy Welch) : comment je verrai cette decision dans 10 min / 10 mois / 10 ans ?"
    ]
  },
  [
    {"prompt": "Comment mieux gerer les decisions importantes sous pression de temps ?", "answer": "Sequence : (1) Typer la decision — type 1 (irreversible) ou type 2 (reversible) ? Si type 2 : decider vite et ajuster, (2) Identifier si c'est vraiment urgent ou si l'urgence est perçue. 'Aujourd'hui' et 'maintenant' sont rarement vrais, (3) Pre-mortem express de 5 min : 'Si cette decision est mauvaise dans 6 mois, pourquoi ?', (4) Distanciation : 'Qu'est-ce que je conseillerais a un collegue dans la meme situation ?' Cette question bypass l'ego et le biais d'implication personnelle. La plupart des decisions 'urgentes' peuvent attendre 24h sans consequence reelle."},
    {"prompt": "Quand faire confiance a mon intuition et quand m'en mefier ?", "answer": "Regle de Kahneman : l'intuition est fiable dans deux conditions simultanees — (1) le domaine est regulier (meme patterns se repetent) ET (2) tu as eu un feedback rapide et clair sur tes decisions passees. Experts valides : pompiers, anesthesistes, joueurs d'echecs. Intuition non fiable : predictions politiques, recrutement, diagnostics medicaux rares, marches financiers. Si tu ne peux pas citer les dizaines ou centaines de cas similaires sur lesquels ton intuition a ete calibree — c'est du Systeme 1 non calibre, pas de l'expertise. Utiliser le Systeme 2 en complement."}
  ],
  ["decision", "Kahneman", "pre-mortem", "irreversible", "intuition", "expertise"]
))

# ── 5. systeme_pensee / mental_models ────────────────────────────────────────
save("cognition/systeme_pensee/mental_models_toolkit.json", ku(
  "mental_models_toolkit", "systeme_pensee",
  "Modeles mentaux — boite a outils",
  "Les modeles mentaux sont des representations simplifiees du fonctionnement du monde. Avoir une large bibliothèque de modeles mentaux —issue de disciplines diverses— permet de voir les situations sous plusieurs angles et d'eviter les erreurs de pensee mono-disciplinaire.",
  "Un modele mental est une representation interne simplifiee d'un systeme ou d'un processus, utilisee pour comprendre, predire et agir sur le monde. La force d'un individu ou d'une organisation vient de la diversite et de la qualite des modeles mentaux disponibles — un modele seul produit une pensee biaisee par son cadre de reference.",
  {
    "core_models": [
      {"name": "Premiers principes (first principles)", "domain": "Physique / philosophie", "use": "Decomposer un probleme en ses elements fondamentaux et repartir de zero plutot que d'analogiser", "example": "Elon Musk sur les batteries : decomposer le cout par composant chimique plutot que le prix du marche"},
      {"name": "Raisonnement par l'inverse (inversion)", "domain": "Mathematiques / stoicisme", "use": "Reflechir a ce qu'on veut eviter plutot que ce qu'on veut atteindre — 'comment echouer a coup sur ?' — puis faire l'inverse", "example": "Charlie Munger : 'Si je savais ou j'allais mourir, je n'irais jamais la'"},
      {"name": "Second-order thinking", "domain": "Systemes complexes", "use": "Penser aux consequences des consequences — pas seulement l'effet immediat mais l'effet sur les acteurs qui reagissent", "example": "Baisser les prix attire des clients (effet 1) mais peut declencher une guerre des prix (effet 2)"},
      {"name": "Marge de securite", "domain": "Ingenierie / investissement", "use": "Integrer un buffer delibere pour absorber les erreurs d'estimation et les imprévus", "example": "Warren Buffett : acheter un actif a 60% de sa valeur estimee pour absorber les erreurs d'estimation"},
      {"name": "Le rasoir d'Occam", "domain": "Philosophie / science", "use": "A explicabilite egale, la theorie la plus simple est probablement la vraie", "example": "Avant de conclure a une conspiracy complexe, verifier les explications simples"},
      {"name": "Pensee en systemes", "domain": "Cybernetique / ecologie", "use": "Voir les boucles de retroaction, les stocks et les flux, les points de levier dans un systeme complexe", "example": "Une intervention sur un element d'un systeme produit souvent des effets non voulus ailleurs"},
      {"name": "Pareto 80/20", "domain": "Economie / statistiques", "use": "20% des causes produisent 80% des effets — concentrer l'energie sur les facteurs a fort levier", "example": "20% des clients font 80% du chiffre — concentrer la retention sur ces 20%"},
      {"name": "Fenetre d'Overton", "domain": "Sciences politiques", "use": "Les idees politiquement acceptables occupent une fenetre — on change les politiques en deplacant la fenetre, pas en proposant directement des idees hors cadre", "example": "Les reformes radicales sont precedees par des idees marginales qui deplacent le Overton window"}
    ]
  },
  [
    {"prompt": "Quels sont les modeles mentaux les plus utiles au quotidien ?", "answer": "Cinq a haut rendement : (1) Inversion — avant tout projet, demander 'comment echouer a coup sur ?' et eviter ces erreurs, (2) Second-order thinking — pour toute decision, noter aussi les consequences des consequences, pas seulement l'effet immediat, (3) Marges de securite — toujours estimer les delais et les coûts puis multiplier par 1.5, (4) Premiers principes — quand une situation semble bloquee, reconstruire le raisonnement depuis la base, (5) 80/20 — regulierement auditer son temps et ses efforts pour identifier les 20% a fort levier. Ces cinq modeles se pratiquent — pas seulement se lisent."},
    {"prompt": "Comment developper de meilleurs modeles mentaux ?", "answer": "La methode Munger : lire largement hors de son domaine de specialite. Les meilleurs modeles mentaux viennent de la physique (premiers principes, entropie), de la biologie (evolution, competition), de l'economie (incitations, couts d'opportunite), de la psychologie (biais, motivations), des mathematiques (probabilites, statistiques). L'objectif n'est pas de tout savoir mais d'avoir un modele solide dans 15-20 disciplines. Quand un modele d'une discipline eclaire un probleme dans une autre — c'est de la pensee a haut levier (ce que Munger appelle 'lattice of mental models')."}
  ],
  ["modeles mentaux", "premiers principes", "inversion", "Munger", "systemes"]
))

# ── 6. systeme_pensee / metacognition ─────────────────────────────────────────
save("cognition/systeme_pensee/metacognition_practice.json", ku(
  "metacognition_practice", "systeme_pensee",
  "Metacognition — penser sur sa pensee",
  "La metacognition est la capacite a observer ses propres processus de pensee — ses biais, ses angles morts, sa qualite de raisonnement. C'est le fondement de l'apprentissage autonome et de l'amelioration continue de la pensee.",
  "La metacognition est la conscience et le controle de ses propres processus cognitifs — savoir ce qu'on sait et ne sait pas, reconnaitre comment on raisonne, identifier quand le raisonnement est biaise, et ajuster deliberement ses strategies cognitives en fonction.",
  {
    "metacognitive_skills": [
      {"skill": "Calibration", "description": "Aligner sa confiance subjective avec la probabilite objective d'avoir raison", "practice": "Tenir un journal de predictions avec niveaux de confiance et verifier le taux de succes par niveau"},
      {"skill": "Thinking about thinking", "description": "Identifier le mode cognitif actif (S1/S2), reconnaitre les heuristiques en action", "practice": "Pause deliberee avant les decisions importantes : 'Comment est-ce que je pense en ce moment ?'"},
      {"skill": "Learning how to learn", "description": "Connaitre ses propres strategies d'apprentissage efficaces vs inefficaces", "practice": "Distinguer learning (nouvelles connexions) de revision (solidification) et varier les formats"},
      {"skill": "Error monitoring", "description": "Detecter ses propres erreurs en temps reel ou en retrospective", "practice": "Journal d'erreurs — documenter les erreurs, les causes et ce qu'on fera differemment"}
    ],
    "deliberate_reflection_practices": [
      "Evening review (15 min) : qu'est-ce que j'ai pense/decide aujourd'hui ? Y avait-il des biais actifs ?",
      "Pre-mortem avant les decisions importantes",
      "Journal de predictions avec niveaux de confiance",
      "Peer review de raisonnements critiques",
      "Question systematique : 'Qu'est-ce qui me prouverait que j'ai tort sur ce point ?'"
    ]
  },
  [
    {"prompt": "Comment mieux reconnaitre mes propres biais dans le moment ?", "answer": "La difficulte : les biais se produisent en dehors de la conscience deliberee — c'est leur nature. Ce qui fonctionne : (1) Creer des 'tripwires' cognitifs — des situations triggers ou tu te rappelles de ralentir ('chaque fois que je prends une decision sous pression de temps, je fais une pause'), (2) Identifier tes biais personnels predominants — certains ont plus le biais de confirmation, d'autres le sunk cost. Connaitre son profil permet des alertes personnalisees, (3) Avoir un 'devil's advocate' dans ton equipe qui a le mandat de challenger — externaliser la fonction de verification du Systeme 2."},
    {"prompt": "Comment devenir plus conscient de la qualite de mon raisonnement ?", "answer": "Pratique de calibration : pendant 2 semaines, noter chaque prediction que tu fais avec un niveau de confiance (70%, 90%, etc.) et revenir verifier le resultat. Les gens bien calibres ont raison 70% du temps quand ils disent '70%'. La plupart sont overconfidents — raison 50% du temps quand ils disent '90%'. Ce feedback quantitatif transforme l'intuition floue ('je pense que j'ai raison') en donnee exploitable. Philip Tetlock (Superforecasting) a montre que cette pratique ameliore significativement la qualite des predictions sur 6 mois."}
  ],
  ["metacognition", "calibration", "Tetlock", "retrospection", "apprentissage"]
))

# ── 7. systeme_pensee / flow_state ─────────────────────────────────────────────
save("cognition/systeme_pensee/flow_state.json", ku(
  "flow_state", "systeme_pensee",
  "Etat de flow (Csikszentmihalyi)",
  "Le flow est l'etat de concentration et d'absorption complete dans une activite — productivite maximale, pas de conscience de soi, pas de temps. Il se produit a l'intersection du defi et de la competence, et peut etre culture deliberement.",
  "Le flow, theorise par Mihaly Csikszentmihalyi, est un etat optimal d'experience et de performance caracterise par une concentration totale, une perte de la conscience de soi et du temps, un sentiment de maitrise et d'harmonie avec la tache, qui survient quand le niveau de defi est en adequation avec le niveau de competence de l'individu.",
  {
    "flow_conditions": [
      "Defi a la limite superieure de la competence (ni trop facile — ennui ; ni trop difficile — anxiete)",
      "Objectif clair et feedback immediat",
      "Absence d'interruptions (le flow prend 15-20 min a s'etablir et disparait instantanement a l'interruption)",
      "Motivation intrinseque (la tache a de la valeur en elle-meme)"
    ],
    "flow_killers": [
      "Notifications et interruptions",
      "Multitasking",
      "Objectifs flous",
      "Ecart trop grand entre defi et competence",
      "Anxiete sociale ou evaluation externe"
    ],
    "creating_flow_conditions": [
      "Creneaux de deep work de 90-120 min sans interruption",
      "Telephone en mode avion, notifications coupees",
      "Tache unique, objectif specifique",
      "Augmenter incrementalement la difficulte des taches",
      "Rituel d'entree (meme environnement, meme playlist si applicable) — signal au cerveau"
    ],
    "flow_and_learning": "Le flow est aussi le meilleur etat pour l'apprentissage profond — la retention est maximale quand l'engagement est maximal. Les activites qui induisent facilement le flow pour toi sont aussi probablement tes zones d'apprentissage optimal."
  },
  [
    {"prompt": "Comment entrer plus facilement dans un etat de flow au travail ?", "answer": "Protocol : (1) Creer les conditions — creneau de 90 min, telephone en mode avion, une seule tache, (2) Rituel de debut — les memes 5 actions avant de commencer (ouvrir les bons fichiers, mettre le casque, ecrire l'objectif du creneau). Le rituel conditionne le cerveau, (3) Augmenter le defi — si une tache te semble trop facile, te fixer une contrainte supplementaire (delai plus court, qualite plus haute). Sans defi suffisant, le flow ne s'installe pas, (4) Proteger les 15 premieres minutes — le flow s'etablit progressivement, ne pas s'interrompre avant d'avoir traverse la 'zone de friction' initiale."},
    {"prompt": "Est-ce qu'ALFRED peut m'aider a entrer en flow ?", "answer": "De facon indirecte : je peux t'aider a clarifier l'objectif de ta session de travail avant de commencer (ce qui est une condition du flow), a decouper un projet complexe en taches au bon niveau de defi, et a gerer les interruptions en prenant en charge les questions que tu m'enverrais plutot que de les laisser te sortir du travail. Je peux aussi te proposer un check-in en fin de session pour evaluer la qualite du focus et ajuster les conditions."}
  ],
  ["flow", "Csikszentmihalyi", "concentration", "deep work", "performance"]
))

# ── 8. systeme_pensee / critical_thinking ─────────────────────────────────────
save("cognition/systeme_pensee/critical_thinking.json", ku(
  "critical_thinking", "systeme_pensee",
  "Pensee critique",
  "La pensee critique est la capacite a evaluer les arguments et les evidences de facon rigoureuse et impartiale — en distinguant les faits des opinions, en identifiant les sophismes et en calibrant la confiance sur les preuves disponibles.",
  "La pensee critique est un processus intellectuel disciplinE d'analyse, d'evaluation et de synthese d'informations, d'arguments et d'evidences, guidE par des criteres epistemiques (logique, coherence, evidence) plutot que par l'intuition, l'autorite ou l'affiliation identitaire.",
  {
    "critical_thinking_skills": [
      {"skill": "Analyse d'arguments", "description": "Identifier la conclusion, les premises, et les hypotheses implicites d'un argument"},
      {"skill": "Evaluation des preuves", "description": "Distinguer la preuve anecdotique, correlationelle et causale — et comprendre les limites de chacune"},
      {"skill": "Detection des sophismes", "description": "Reconnaitre les arguments fallacieux (homme de paille, appel a l'autorite, fausse dichotomie, etc.)"},
      {"skill": "Calibration de la certitude", "description": "Exprimer ses croyances en probabilites et les mettre a jour face aux nouvelles preuves"},
      {"skill": "Steelmanning", "description": "Formuler l'argument adverse dans sa version la plus forte avant de le refuter"}
    ],
    "common_fallacies": [
      {"fallacy": "Ad hominem", "description": "Attaquer la personne, pas l'argument"},
      {"fallacy": "Homme de paille", "description": "Refuter une version deformee et plus faible de l'argument"},
      {"fallacy": "Fausse dichotomie", "description": "Presenter deux options comme les seules possibles alors qu'il en existe d'autres"},
      {"fallacy": "Appel a l'autorite", "description": "Valider un argument par l'identite de celui qui le soutient, pas par ses merites"},
      {"fallacy": "Post hoc ergo propter hoc", "description": "Confondre correlation et causalite — parce que A precede B, A cause B"},
      {"fallacy": "Generalisation abusive", "description": "Conclure sur la totalite depuis un echantillon non representatif"}
    ]
  },
  [
    {"prompt": "Comment evaluer si une information est fiable ?", "answer": "Checklist en 5 points : (1) Source primaire — qui l'a dit a l'origine ? Est-ce cite ou deforme ?, (2) Expertise dans le domaine — l'autorite est specifique : un prix Nobel de physique n'est pas une autorite en epidemiologie, (3) Consensus ou cas isole ? — une etude seule ne prouve rien, un consensus de meta-analyses est robuste, (4) Interet — qui beneficie de cette information etant crue ?, (5) Falsifiabilite — peut-on imaginer ce qui prouverait que c'est faux ? Si non, ce n'est pas empirique. Ces 5 points prennent 2 minutes et filtrent 90% de la desinformation."},
    {"prompt": "Comment debattre sans tomber dans les sophismes ?", "answer": "Regles du debat productif : (1) Steelmanner l'argument adverse — formuler la version la plus forte de ce qu'il dit avant de le refuter. Si tu ne peux pas le faire, tu ne le comprends pas assez, (2) Distinguer 'j'ai tort' de 'tu as raison' — les deux ne sont pas synonymes. Un argument peut etre refute sans que l'alternative soit correcte, (3) Mettre a jour explicitement — 'tu as un bon point sur X, j'ajuste ma position', (4) Attaquer les arguments, jamais les motivations supposees. L'ad hominem est le signal que l'argument est epuise."}
  ],
  ["pensee critique", "sophismes", "logique", "evidence", "epistemologie"]
))

# ── 9. systeme_pensee / learning_how_to_learn ────────────────────────────────
save("cognition/systeme_pensee/learning_how_to_learn.json", ku(
  "learning_how_to_learn", "systeme_pensee",
  "Apprendre a apprendre",
  "Les techniques d'apprentissage les plus repandues (relire, surligner, ecouter des cours) sont parmi les moins efficaces. Les methodes validees par la science cognitive — rappel actif, repetition espacee, interleaving — produisent une retention 2 a 5 fois superieure.",
  "Apprendre a apprendre est la meta-competence qui consiste a connaitre et appliquer les strategies d'apprentissage scientifiquement validees pour maximiser la retention a long terme, la comprehension profonde et le transfert des connaissances a de nouveaux contextes.",
  {
    "most_effective_techniques": [
      {
        "technique": "Rappel actif (retrieval practice)",
        "description": "Tenter de se rappeler l'information AVANT de la relire",
        "implementation": "Questions flash, tester sa memoire sans regarder les notes, expliquer a quelqu'un",
        "science": "Renforce les traces mnemoniques a chaque rappel — 'testing effect' (Roediger & Karpicke)"
      },
      {
        "technique": "Repetition espacee",
        "description": "Reviser a des intervalles croissants (aujourd'hui, demain, dans 3 jours, dans 1 semaine...)",
        "implementation": "Anki, SuperMemo, ou systeme de fiches papier 5 boites",
        "science": "Exploite l'effet d'espacement — le cerveau renforce ce qu'il croit etre important (revisite plusieurs fois)"
      },
      {
        "technique": "Elaboration",
        "description": "Expliquer POURQUOI quelque chose fonctionne ainsi, pas juste ce que c'est",
        "implementation": "Apres chaque point : pourquoi est-ce vrai ? Comment se connecte-t-il a ce que je sais deja ?",
        "science": "Cree des connexions riches qui facilitent le rappel"
      },
      {
        "technique": "Interleaving",
        "description": "Melanger les types de problemes plutot que de les regrouper par type",
        "implementation": "Mixer les sujets dans les sessions d'entrainement au lieu de bloquer par theme",
        "science": "Plus difficile mais produit un meilleur transfert et une meilleure discrimination"
      }
    ],
    "least_effective_techniques": [
      "Relire les notes — produit de la familiarite, pas du rappel",
      "Surligner sans traiter — illusion d'apprentissage",
      "Ecouter passivement — sans engagement actif, retention < 10% apres 48h",
      "Apprendre par blocs (massed practice) — oubli rapide"
    ],
    "feynman_technique": {
      "source": "Richard Feynman",
      "steps": [
        "1. Choisir un concept",
        "2. L'expliquer comme si tu l'enseignais a un enfant de 12 ans",
        "3. Identifier les lacunes et retourner a la source",
        "4. Simplifier encore plus et utiliser des analogies"
      ],
      "insight": "Si tu ne peux pas l'expliquer simplement, tu ne le comprends pas vraiment"
    }
  },
  [
    {"prompt": "Comment memoriser plus efficacement ce que j'apprends ?", "answer": "Remplacer les 3 mauvaises habitudes par les 3 bonnes : (1) Au lieu de relire : tester sa memoire d'abord — fermer le livre, ecrire ce dont on se souvient, PUIS verifier. Chaque rappel renforce la trace, (2) Au lieu de tout reviser en bloc : reviser en sessions espacees avec Anki ou un systeme equivalent. 20 minutes sur 3 jours vaut mieux que 60 minutes la veille, (3) Au lieu d'etre passif : elaborer — apres chaque point appris, se demander 'pourquoi ? comment ca se connecte a ce que je sais ? dans quel contexte reel je l'utiliserais ?'. Ces 3 pratiques changent completement l'efficacite de l'apprentissage."},
    {"prompt": "J'ai du mal a retenir ce que je lis — que faire ?", "answer": "La lecture passive ne produit presque pas de retention (< 20% apres 24h sans traitement). Trois interventions : (1) Lire par questions — avant de lire, noter 3 questions auxquelles le texte devrait repondre. Ca cree un contexte actif, (2) Pause active toutes les 20 pages — fermer le livre, ecrire de memoire les points principaux, (3) Review immediate puis espacee — revoir ses notes le soir meme, puis dans 3 jours. Ces trois pratiques sont compatibles avec la lecture de plaisir — les appliquer pour ce qu'on veut vraiment retenir."}
  ],
  ["apprentissage", "Feynman", "rappel actif", "repetition espacee", "memorisation"]
))

# ── 10. systeme_pensee / attention_focus ─────────────────────────────────────
save("cognition/systeme_pensee/attention_focus.json", ku(
  "attention_focus", "systeme_pensee",
  "Attention et gestion du focus",
  "L'attention est la ressource cognitive la plus rare et la plus precieuse. La capacite a diriger et maintenir son attention deliberement — malgre les distractions exterieures et interieures — est le super-pouvoir de notre epoque de surinformation.",
  "L'attention est la capacite selective du systeme cognitif a allouer ses ressources de traitement vers des stimuli, des pensees ou des taches specifiques, en excluant les autres. La gestion deliberee de l'attention est la competence de la placer volontairement, de la maintenir et de la recuperer apres distraction.",
  {
    "types_of_attention": [
      {"type": "Attention focalisee", "description": "Concentration intense sur un seul point — mode deep work"},
      {"type": "Attention diffuse", "description": "Mode ouvert et relaxe — traitement en arriere-plan, creativite, connexions inattendues"},
      {"type": "Attention partagee", "description": "Multi-tache apparent — en realite, commutation rapide entre foyers d'attention avec coûts de commutation"}
    ],
    "attention_economics": {
      "deep_work_cal_newport": "Le travail profond (Deep Work) est l'etat de concentration sans distraction sur une tache cognitivement exigeante — c'est la ou se cree la vraie valeur cognitive. Cal Newport (Deep Work, 2016)",
      "attention_residue": "Chaque fois qu'on switch de tache, une partie de l'attention reste sur la tache precedente — Sophie Leroy. Ca explique pourquoi 2h ininterrompues > 4x 30 min",
      "smartphone_effect": "La simple presence d'un telephone sur un bureau (meme eteint) reduit la capacite cognitive disponible — Ward et al., 2017"
    },
    "protecting_attention": [
      "Time blocking — planifier des blocs de deep work dans le calendrier comme des RDV",
      "Environnement de travail dedie (si possible) signal contextuel pour le cerveau",
      "Protocol digital : checker emails/messages a des horaires fixes, pas en continu",
      "Pratique de pleine conscience — entraine le muscle de la conscience attentionnelle",
      "Single-tab / single-app en deep work"
    ]
  },
  [
    {"prompt": "Comment arreter d'etre distrait par mon telephone quand je travaille ?", "answer": "Tactique la plus efficace : mettre le telephone dans une autre piece. Pas juste le retourner ou le mettre en silence — une autre piece. L'etude Ward (2017) montre que la capacite cognitive est plus haute quand le telephone est absent du champ de vision. Second levier : sessions de travail avec objectifs ecrits avant — tu sais exactement quoi faire, donc la tentation de combler le vide avec le telephone diminue. Troisieme : definir tes 'fenêtres de consultation' (ex: 9h, 12h, 16h) et notifier les gens de ces horaires. La plupart des 'urgences' peuvent attendre 3h."},
    {"prompt": "Comment developper une meilleure concentration en general ?", "answer": "La concentration se developpe comme un muscle — par une pratique deliberee. Trois leviers : (1) Meditation de pleine conscience — 10 min par jour entraine le muscle de retour attentionnel (amener l'attention de retour sur l'objet apres une distraction — le meme muscle qu'en deep work), (2) Sessions de deep work progressives — commencer par 25 min (Pomodoro), etendre a 45, 60, 90 min sur quelques semaines, (3) Proteger les dimanches de l'hyperconnexion — les periodes de desengagement restaurent la capacite attentionnelle. La concentration souffre autant du manque de repos que du manque de pratique."}
  ],
  ["attention", "focus", "deep work", "Cal Newport", "distraction", "meditation"]
))

print("\n=== Domaine 'cognition/systeme_pensee' : 10 fichiers crees ===")
