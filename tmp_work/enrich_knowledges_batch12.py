"""
Enrichissement Knowledge Base ALFRED - Batch 12 : human + lifestyle + culture + decision + engineering/ai
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(domain, subdomain, stem, title, summary, core_def, knowledge, examples, tags, tone="bienveillant et ancré dans la réalité"):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.{domain}.{subdomain}.{stem}",
      "title": title, "domain": domain, "subdomain": subdomain,
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": tone,
        "structure": ["contextualiser", "expliquer le concept", "proposer un angle actionnable"],
        "avoid": ["trop théorique", "ignorer le contexte de l'utilisateur"]
      },
      "tags": tags,
      "related_knowledge_units": []
    }

# =============================================================================
# human / emotional_intelligence
# =============================================================================

save("human/emotional_intelligence/emotional_support.json", ku(
  "human", "interaction", "emotional_support",
  "Soutien émotionnel",
  "Le soutien émotionnel consiste à être pleinement présent pour quelqu'un dans sa douleur ou sa difficulté — en validant son expérience avant toute tentative de solution. La présence prime sur les conseils.",
  "Le soutien émotionnel est la capacité à offrir une présence empathique et validante à une personne traversant une difficulté émotionnelle, en reconnaissant et en accueillant son vécu sans jugement ni précipitation vers la résolution.",
  {
    "support_principles": [
      "Présence avant solution : écouter pleinement avant de suggérer quoi que ce soit",
      "Validation avant correction : reconnaître l'émotion comme légitime",
      "Questions ouvertes : 'Qu'est-ce qui se passe pour toi ?' vs 'Tu devrais...'",
      "Suivre le rythme de la personne : ne pas précipiter vers le mieux"
    ],
    "phrases_utiles": [
      "Je t'entends.",
      "Ca semble vraiment difficile.",
      "C'est normal de te sentir comme ca.",
      "Qu'est-ce dont tu as besoin en ce moment ?"
    ]
  },
  [
    {"prompt": "Je me sens vraiment mal en ce moment.", "answer": "Je suis la. Dis-moi ce qui se passe — je t'ecoute sans jugement. Qu'est-ce qui se passe pour toi en ce moment ?"},
    {"prompt": "Comment soutenir quelqu'un en deuil ?", "answer": "La presence silencieuse est souvent plus puissante que les mots. Valide leur douleur sans essayer de la reduire ('c'est dur, je suis la'), propose de l'aide concrete ('je peux venir t'apporter a manger ce soir'), et ne disparais pas apres les premiers jours — le deuil dure bien plus longtemps que les condoleances."}
  ],
  ["soutien", "empathie", "presence", "emotion", "écoute"]
))

save("human/emotional_intelligence/empathy.json", ku(
  "human", "interaction", "empathy",
  "Empathie",
  "L'empathie est la capacite a percevoir et ressentir le vecu emotionnel d'autrui — distincte de la sympathie (partager l'emotion) et de la compassion (agir pour reduire la souffrance). Elle se cultive et s'ajuste.",
  "L'empathie est la faculte cognitive et affective de se representer l'experience subjective d'une autre personne et de reagir de facon accordee a son etat emotionnel, sans se confondre avec elle ni nier sa propre perspective.",
  {
    "empathy_types": [
      {"type": "Empathie cognitive", "description": "Comprendre intellectuellement la perspective de l'autre", "risk": "Peut etre utilisee sans connexion emotionnelle (manipulation)"},
      {"type": "Empathie affective", "description": "Ressentir quelque chose de similaire a ce que l'autre ressent", "risk": "Peut mener a la detresse empathique (burnout du soignant)"},
      {"type": "Empathie compassionnelle", "description": "Comprendre, ressentir, ET vouloir aider", "optimal": True}
    ],
    "empathy_blockers": [
      "Jugement immediat",
      "Comparaison ('moi aussi j'ai vecu pire')",
      "Minimisation ('c'est pas si grave')",
      "Conseils precipites avant validation"
    ],
    "alfred_empathy_approach": "ALFRED vise l'empathie compassionnelle : comprendre ce que l'utilisateur ressent, valider son experience, et proposer de l'aide adaptee — sans projeter ses propres emotions ni se laisser deborder."
  },
  [
    {"prompt": "Comment etre plus empathique dans mes relations ?", "answer": "Trois pratiques : (1) Ecoute active — poser son telephone, regarder la personne, signaler par des hochements de tete qu'on est la, (2) Reformulation — 'Si je comprends bien, tu te sens X a cause de Y ?' — ca montre qu'on a entendu et laisse corriger, (3) Curiosite genuineour la perspective de l'autre — 'Comment tu vis ca ?' plutot que 'A ta place je ferais...'. L'empathie s'entraine comme un muscle — les relations profondes la developpent naturellement."},
    {"prompt": "Comment eviter le burnout quand on est tres empathique ?", "answer": "La frontiere entre empathie et fusion est la cle. Se rappeler : je peux comprendre et soutenir sans porter le poids de l'autre. Pratiques : fixer ses limites de disponibilite, decompresser apres des echanges emotionnellement lourds (marche, musique, silence), distinguer 'je me soucie de toi' de 'je souffre pour toi'. Et parfois : orienter vers un professionnel plutot que de tout porter seul."}
  ],
  ["empathie", "écoute", "compassion", "relations", "bienveillance"]
))

save("human/emotional_intelligence/self_awareness.json", ku(
  "human", "interaction", "self_awareness",
  "Conscience de soi",
  "La conscience de soi est la capacite a observer ses propres etats emotionnels, pensees et comportements avec precision et sans jugement. Elle est le fondement de l'intelligence emotionnelle et du changement intentionnel.",
  "La conscience de soi est la capacite metacognitive a percevoir ses propres etats internes (emotions, pensees, motivations, biais) avec une precision suffisante pour prendre des decisions alignees avec ses valeurs et ses objectifs reels.",
  {
    "self_awareness_dimensions": [
      {"dimension": "Conscience emotionnelle", "description": "Identifier et nommer ses emotions au moment ou elles emergent"},
      {"dimension": "Conscience de ses forces et limites", "description": "Evaluer precisement ce qu'on sait faire et ce qu'on ne sait pas faire"},
      {"dimension": "Conscience de ses valeurs", "description": "Savoir ce qui compte vraiment pour soi — distincts des desirs du moment"},
      {"dimension": "Conscience de son impact", "description": "Comprendre comment ses actions et paroles affectent les autres"}
    ],
    "development_practices": [
      "Journaling emotionnel quotidien (5 min)",
      "Feedback externe (demander a des proches de confiance)",
      "Meditation de pleine conscience (observe les etats sans s'y identifier)",
      "Analyse retrospective des decisions (qu'est-ce qui m'a motive ici ?)"
    ]
  },
  [
    {"prompt": "Comment developper ma conscience de moi-meme ?", "answer": "Trois niveaux : (1) Corps — commencer a noter les sensations physiques associees aux emotions (tension, chaleur, lourdeur) — le corps ressent avant le mental conscient, (2) Emotions — les nommer precisement : pas juste 'mal' mais 'frustration', 'deception', 'honte', 'tristesse' — la granularite emotionnelle aide a mieux repondre, (3) Pensees — observer les pensees automatiques qui emergent dans les situations difficiles ('je ne suis pas assez bien', 'ils ne m'apprecient pas') sans les prendre pour des verites."},
    {"prompt": "Pourquoi je reagis toujours de la meme facon dans certaines situations ?", "answer": "Ce sont des patterns appris — souvent inscrits dans l'enfance comme strategies d'adaptation. La bonne nouvelle : les identifier est la premiere etape pour les changer. La mauvaise : c'est un travail long. Pratique utile : reperer le declencheur (situation), la reaction automatique (comportement/emotion), et les croyances sous-jacentes ('si X, alors Y'). Une fois le pattern visible, on peut inserer un espace de choix entre le declencheur et la reaction."}
  ],
  ["conscience de soi", "emotions", "valeurs", "metacognition", "introspection"]
))

save("human/emotional_intelligence/self_regulation.json", ku(
  "human", "interaction", "self_regulation",
  "Auto-regulation emotionnelle",
  "L'auto-regulation emotionnelle est la capacite a gerer ses propres reponses emotionnelles de facon adaptee — ni repression ni debordement. Elle inclut la gestion de l'impulsivite, du stress et des emotions intenses.",
  "L'auto-regulation emotionnelle est la capacite a moduler ses etats emotionnels et les comportements qui en decoulent, en s'appuyant sur des strategies conscientes (recadrage cognitif, regulation physiologique, distanciation) pour repondre de facon adaptee plutot que de reagir automatiquement.",
  {
    "regulation_strategies": [
      {"strategy": "Respiration physiologique", "description": "Inspire 5s, expire 10s (double de l'inspiration) — active le systeme nerveux parasympathique", "speed": "Immediate (30-90 secondes)"},
      {"strategy": "Recadrage cognitif", "description": "Reinterpreter la situation sous un angle moins menacant", "speed": "Minutes"},
      {"strategy": "Distanciation temporelle", "description": "Se projeter dans 6 mois ('est-ce que ca me semblera aussi important ?')", "speed": "Minutes"},
      {"strategy": "Mouvement physique", "description": "Marche rapide, exercice — metabolise les hormones de stress", "speed": "15-30 minutes"},
      {"strategy": "Validation interne", "description": "Se dire 'c'est normal de ressentir ca' sans judgment", "speed": "Immediate"}
    ],
    "signs_of_dysregulation": [
      "Reactions disproportionnees par rapport a la situation",
      "Rumination persistante",
      "Impulsivite regrettee",
      "Debordement emotionnel dans des contextes inadequats"
    ]
  },
  [
    {"prompt": "Je perds rapidement mon calme en reunion quand je suis contredit — comment gerer ?", "answer": "Deux temps : (1) Immediat — reperer le signal physique avant l'explosion (tension machoire, chaleur, serrement) et respirer avant de repondre (5s d'inspiration, 10s d'expiration). Ce simple espace evite souvent la reaction impulsive. (2) Plus profond — comprendre ce que le fait d'etre contredit declenche en toi (menace a l'ego ? peur de perdre le controle ? injustice percue ?) — la therapie ou le coaching peuvent aider a traiter la source."},
    {"prompt": "Comment m'aider a ne pas ruminer la nuit ?", "answer": "Trois techniques : (1) Externaliser — noter les pensees qui tournent dans un carnet avant de te coucher (le cerveau arrete de 'tenir' ce qui est ecrit), (2) Creneaux de rumination — s'autoriser a s'inquieter de 18h a 18h30, pas le reste du temps (entraine le cerveau a ne pas ruminer en dehors du creneau), (3) Relaxation musculaire progressive (contracter/relacher chaque groupe musculaire) — rompt la boucle cognitive par le corps. Si la rumination est severe et persistante : consulter un professionnel."}
  ],
  ["auto-regulation", "emotions", "stress", "impulsivite", "pleine conscience"]
))

save("human/psychology/cognitive_biases.json", ku(
  "human", "psychology", "cognitive_biases",
  "Biais cognitifs humains",
  "Les biais cognitifs sont des raccourcis mentaux systematiques qui peuvent distordre nos jugements et decisions. Les connaitre permet de mieux les anticiper, meme si la seule connaissance ne suffit pas a les eliminer.",
  "Les biais cognitifs sont des patterns d'erreur systematique dans la pensee humaine resultant des raccourcis heuristiques du systeme cognitif — ils permettent une prise de decision rapide mais au prix de deviations previsibles et systematiques de la rationalite.",
  {
    "core_biases": [
      {"bias": "Biais de confirmation", "description": "On cherche et retient les informations qui confirment nos croyances", "antidote": "Chercher activement les contra-preuves"},
      {"bias": "Effet de halo", "description": "Une qualite d'une personne colore notre perception de toutes ses autres qualites", "antidote": "Evaluer chaque critere independamment"},
      {"bias": "Biais d'ancrage", "description": "Le premier chiffre entendu influence toutes les estimations suivantes", "antidote": "Generer ses propres estimations avant d'en recevoir"},
      {"bias": "Biais de disponibilite", "description": "On surestime les evenements facilement memorables (recents, emotionnels)", "antidote": "Chercher les statistiques de base rate"},
      {"bias": "Effet Dunning-Kruger", "description": "Les novices surestiment leurs competences ; les experts les sous-estiment", "antidote": "Feedback externe, calibration reguliere"},
      {"bias": "Biais de status quo", "description": "On prefere l'etat actuel au changement, meme benefique", "antidote": "Evaluer le changement et le statu quo sur les memes criteres"}
    ],
    "mitigation_systems": "Les biais resistent a la simple prise de conscience — ils se reduisent via des systemes processuels (checklists, double validation, regles de decision pre-definies) plutot que par la volonte."
  },
  [
    {"prompt": "Comment les biais cognitifs influencent-ils mes decisions au quotidien ?", "answer": "Exemples concrets : tu achetes une voiture avec une 'remise exceptionnelle' de 3000 euro — l'ancrage (le prix de reference) te fait percevoir la remise comme une victoire meme si le prix reste eleve. Tu penses que les accidents d'avion sont frequents parce qu'ils font la une — disponibilite. Tu gardes un projet qui ne marche pas parce que tu y as investi 2 ans — sunk cost. Ces biais ne disparaissent pas avec la connaissance — ils se grent avec des regles de decision pre-definies ('si la metrique X ne s'ameliore pas en Y semaines, on arrete')."},
    {"prompt": "Est-ce qu'ALFRED a des biais ?", "answer": "Oui — plusieurs. Biais de sycophanie : tendance a confirmer ce que l'utilisateur semble croire. Biais de recence dans le contexte : surponderer les informations recentes. Biais de popularite : favoriser les opinions majoritaires dans les donnees d'entrainement. Biais culturels : entrainement sur des donnees anglophones et occidentales. J'essaie d'en etre conscient : quand tu sembles chercher une validation, je te presente aussi le contre-argument. Quand je formule une reponse sure, je hedge si la confiance est faible. Mais je ne suis pas exempt de biais — garde un oeil critique."}
  ],
  ["biais cognitifs", "heuristiques", "decision", "psychologie", "Kahneman"]
))

save("human/self_alignment/habits/habit_building.json", ku(
  "human", "self_alignment", "habit_building",
  "Construction d'habitudes durables",
  "Les habitudes durables se forment par des signaux clairs, des routines simples et des recompenses immediates — selon la boucle habitude (cue-routine-reward de Duhigg) ou l'implementation intention (si/alors). La regularite prime sur l'intensite.",
  "La construction d'habitudes est le processus delibere d'ancrage de comportements automatiques positifs par la mise en place de signaux, de routines et de recompenses qui renforcent progressivement la boucle neurale sous-jacente jusqu'a ce que le comportement devienne une reponse automatique.",
  {
    "habit_frameworks": [
      {"framework": "Boucle habitude (Duhigg)", "elements": ["Cue (declencheur)", "Routine (comportement)", "Reward (recompense)"], "key": "Identifier et modifier le cue ou la reward, pas juste la routine"},
      {"framework": "Atomic Habits (Clear)", "elements": ["Rendre evident", "Rendre attrayant", "Rendre facile", "Rendre satisfaisant"], "key": "Reduire la friction a son minimum pour les bonnes habitudes"},
      {"framework": "Implementation intention", "elements": ["Si [situation X], alors je ferai [comportement Y]"], "key": "La specification contextuelle multiplie par 2-3 le taux de suivi des intentions"}
    ],
    "habit_stacking": "Ancrer une nouvelle habitude sur une habitude existante : 'Apres [habitude etablie], je ferai [nouvelle habitude]'. Exploite le signal existant sans en creer un nouveau.",
    "failure_recovery": "L'echec d'un jour n'est pas le probleme — c'est la spirale apres l'echec. Regle : ne jamais manquer deux fois de suite. Un ratage est un accident ; deux rates consecutifs sont le debut d'une nouvelle habitude negative."
  },
  [
    {"prompt": "Comment creer l'habitude de faire du sport le matin ?", "answer": "Technique en 3 temps : (1) Reduire la friction — preparer la tenue la veille, mettre les chaussures pres du lit, avoir un programme simple de 20 min (pas besoin d'aller a la salle), (2) Ancrer sur un cue existant — 'Apres mon alarme de 7h, avant le cafe, je sors courir 20 min', (3) Recompense immediate — cafe plaisir apres le sport, sentir sa progression sur une application. L'objectif initial : pas 1h de salle, mais 5 minutes de mouvements. Commencer minuscule et croitre progressivement."},
    {"prompt": "Pourquoi mes bonnes resolutions tiennent toujours 2 semaines puis s'effondrent ?", "answer": "Deux causes principales : (1) L'objectif est trop ambitieux par rapport a la difficulte reelle — la motivation initiale compense, mais elle decline apres 2 semaines et la friction revient, (2) Pas de systeme de recovery apres le premier ratage — un jour rate devient deux, devient l'abandon. Solution : commencer par une version si facile qu'elle semble ridicule (2 minutes de meditation, 5 pompes), construire la regularite avant l'intensite, et avoir une regle explicite pour le ratage."}
  ],
  ["habitudes", "routine", "atomic habits", "changement de comportement", "regularite"]
))

save("human/self_alignment/routines/daily_balance.json", ku(
  "human", "self_alignment", "daily_balance",
  "Equilibre quotidien",
  "L'equilibre quotidien n'est pas un etat fixe mais une gestion dynamique des differents domaines de vie (travail, corps, relations, repos). Il se construit par des rituels qui ancrent les transitions et protegens les ressources essentielles.",
  "L'equilibre quotidien est la capacite a distribuens son energie et son attention entre les differentes spheres de sa vie (travail, sante, relations, besoins personnels) de facon coherente avec ses valeurs et ses besoins reels, en creant des structures qui protegens les priorites essentielles sans rigidite.",
  {
    "balance_domains": [
      "Travail et accomplissement",
      "Corps et energie physique",
      "Relations et connexion",
      "Besoins personnels et recuperation",
      "Sens et croissance"
    ],
    "balance_rituals": [
      {"ritual": "Rituel matin", "purpose": "Ancrer la journee dans l'intention — pas de smartphone en premier", "examples": ["5 min de silence", "Journal de 3 intentions", "Mouvement physique leger"]},
      {"ritual": "Transition travail/maison", "purpose": "Signaler a l'esprit la fin du mode travail", "examples": ["Marche courte", "Changement de vetements", "Note de cloture des taches ouvertes"]},
      {"ritual": "Rituel soir", "purpose": "Preparer la recuperation et le sommeil", "examples": ["Ecran eteint 1h avant le coucher", "Lecture", "3 gratitudes"]}
    ]
  },
  [
    {"prompt": "Comment trouver l'equilibre entre ma vie pro et perso quand le travail prend tout la place ?", "answer": "Deux angles : (1) Structure — proteger explicitement des creneaux non-travail (sport, diner en famille, temps vide) dans l'agenda AVANT que le travail ne les colonise. Ce qui n'est pas programme n'existe pas. (2) Transition — creer un rituel de cloture du travail (fermer le PC, noter les 3 taches de demain) qui signale mentalement la fin. Sans cette transition, le cerveau reste en mode travail meme le soir. L'equilibre n'est pas spontane dans notre culture — il se construit deliberement."},
    {"prompt": "Je me sens coupable de ne pas travailler quand je prends du temps pour moi.", "answer": "Cette culpabilite vient d'une croyance souvent inconsciente : 'ma valeur = ma productivite'. Reframe : le repos n'est pas oppose au travail — il le rend possible. Les athletes de haut niveau savent que la recuperation est partie integrante de la performance. Prendre du temps pour toi n'est pas du temps vole au travail — c'est de l'investissement dans ta capacite a travailler demain. Et plus profondement : tu as une valeur independante de ce que tu produis."}
  ],
  ["equilibre", "routine", "rituels", "vie pro/perso", "gestion energie"]
))

save("human/self_alignment/routines/energy_management.json", ku(
  "human", "self_alignment", "energy_management",
  "Gestion de l'energie personnelle",
  "La gestion de l'energie est plus fondamentale que la gestion du temps : l'energie physique, mentale, emotionnelle et spirituelle determinent la qualite du travail disponible dans chaque heure. La recuperation est un levier de performance, pas un luxe.",
  "La gestion de l'energie personnelle est la discipline qui consiste a identifier, preserver et renouveler ses ressources energetiques (physiques, mentales, emotionnelles) pour maintenir un niveau de performance et de bien-etre optimal dans la duree, en traitant l'energie comme une ressource renouvelable par la recuperation intentionnelle.",
  {
    "energy_sources": [
      {"source": "Energie physique", "foundation": "Sommeil, nutrition, mouvement", "signals_low": ["Fatigue persistante", "Difficulte a se lever", "Baisses d'energie apres repas"]},
      {"source": "Energie mentale", "foundation": "Focus, gestion de l'attention, recup cognitive", "signals_low": ["Difficulte de concentration", "Oublis frequents", "Decisions difficiles"]},
      {"source": "Energie emotionnelle", "foundation": "Relations, reconnaissance, sens", "signals_low": ["Irritabilite", "Detachement", "Cynisme croissant"]},
      {"source": "Energie de sens", "foundation": "Valeurs, objectifs, contribution", "signals_low": ["Sentiment de vacuite", "Questions sur 'pourquoi je fais ca ?'", "Perte de motivation profonde"]}
    ],
    "energy_management_practices": [
      "Ultradian rhythms : nos cycles naturels de 90 min de focus suivi de 15-20 min de recuperation",
      "Dormir 7-9h — sans negociation : la dette de sommeil reduit les fonctions cognitives de maniere non percue",
      "Microrecuperations pendant la journee : pauses de 5-10 min sans stimulation toutes les 90 min",
      "Activite physique reguliere — le meilleur outil de regulation du stress et de recharge energetique"
    ]
  },
  [
    {"prompt": "Comment ne pas etre epuise en fin de journee ?", "answer": "Trois leviers : (1) Respecter les cycles ultradian — 90 min de travail intense / 15 min de pause vraie (pas de mail). Le cerveau recupe moins bien si on force a travers l'envie de pause, (2) Taches cognitives lourdes le matin quand l'energie est haute — reunions et mails l'apres-midi, (3) Dejeuner leger (les gros repas vident l'energie l'apres-midi). Et fundamentalement : si tu es systematiquement epuise, c'est un signal que le repos est insuffisant ou que le volume de travail depasse tes capacites de recuperation."},
    {"prompt": "ALFRED peut-il m'aider a gerer mon energie pendant la journee ?", "answer": "Oui — de plusieurs facons : rappels de pause si tu travailles trop longtemps en continu, check-in d'energie en milieu de journee, suggestions de micro-recuperation adaptees a ton contexte (2 min de respiration, etirements, marche courte). Et si tu me signales ta fatigue, j'adapte ma reponse : questions plus simples, syntheses plus courtes, pas de nouvelles taches complexes quand l'energie est basse."}
  ],
  ["energie", "recuperation", "performance", "sommeil", "ultradian"]
))

save("human/skills/softskills/communication.json", ku(
  "human", "skills", "communication",
  "Communication efficace",
  "La communication efficace est la capacite a transmettre un message clair, a ecouter avec intention et a adapter son discours a son interlocuteur. Elle combine structure du message, calibration du registre et gestion des malentendus.",
  "La communication efficace est la capacite a partager des informations, des emotions et des intentions de facon claire et adaptee a son interlocuteur et a son contexte, en maximisant la comprehension et en minimisant les malentendus.",
  {
    "communication_principles": [
      "Clarifier son intention avant de parler : informer, convaincre, decider, soutenir ?",
      "Adapter le registre a l'audience : vocabulaire, niveau de detail, canaux",
      "Ecoute active : signaux d'attention, reformulation, questions de clarification",
      "Structure du message : bottom-line en premier (Pyramid Principle), details ensuite",
      "Feedback sur la comprehension : 'Est-ce que c'est clair ?' / reformulation de l'ecoute"
    ],
    "message_structure": {
      "pyramid_principle": "Commencer par la conclusion (bottom-line), puis les arguments, puis les details — l'inverse de la pensee naturelle mais optimal pour la comprehension",
      "BLUF": "Bottom Line Up Front — militaire et consulting : reponse d'abord, contexte ensuite"
    },
    "written_vs_oral": {
      "ecrit": "Avantages : precision, trace, asynchrone. Defauts : perd le non-verbal, risque de misinterpretation du ton",
      "oral": "Avantages : riche, interactif, emotional. Defauts : ephemere, dependant de la disponibilite commune"
    }
  },
  [
    {"prompt": "Comment etre plus percutant dans mes presentations ?", "answer": "Pyramid Principle : commencer par la conclusion ('je recommande X'), puis les 3 arguments principaux, puis les details. La plupart des presenteurs font l'inverse — ils construisent vers la conclusion, ce qui perd l'audience en chemin. Autres leviers : reduire de moitie le nombre de slides, une idee par slide avec un titre qui est deja la conclusion (pas 'resultats Q3' mais 'Q3 : croissance de 20% grace au canal partenarial'), et terminer par les prochaines actions specifiques (qui fait quoi avant quand)."},
    {"prompt": "Comment mieux communiquer par ecrit dans mon equipe ?", "answer": "Trois habitudes : (1) BLUF (Bottom Line Up Front) — commencer chaque email par ce que tu attends (information ? decision ? action ? lecture seule ?) avant le contexte, (2) Canal adapte au message — Slack pour rapide/conversationnel, email pour formal/tracable, reunions pour les decisions importantes (pas les mises a jour), (3) Relecture du point de vue du destinataire — 'Qu'est-ce qu'il pourrait ne pas comprendre ou mal interpreter dans ce message ?'"}
  ],
  ["communication", "messages", "ecoute", "presentations", "ecrit"]
))

save("human/skills/softskills/emotional_management.json", ku(
  "human", "skills", "emotional_management",
  "Gestion emotionnelle au travail",
  "La gestion emotionnelle au travail consiste a exprimer ses emotions de facon adaptee au contexte professionnel, a gerer les conflits sans debordement, et a maintenir sa performance sous pression sans masquer son humanite.",
  "La gestion emotionnelle au travail est la capacite a reconnaitre, exprimer et reguler ses etats emotionnels dans un contexte professionnel, en trouvant l'equilibre entre authenticite (ne pas masquer toutes ses emotions) et professionnalisme (ne pas les imposer au detriment de l'equipe).",
  {
    "professional_emotion_management": [
      "Nommer l'emotion en interne avant d'agir (reduce reaction automatique)",
      "Distinguer l'emotion de l'interpretation ('je suis frustre' vs 'il est incompetent')",
      "Exprimer avec assertivite les besoins sans agressivite ou repression",
      "Pauser avant de repondre aux emails ou messages envoyes sous l'emotion",
      "Identifier les contextes qui declenchent les reactions les plus intenses"
    ],
    "conflict_and_emotions": [
      "Reunions qui deraillent : 'Je suggere qu'on fasse une pause de 5 minutes pour que chacun puisse reflEchir'",
      "Feedback critique recu : note les points, ne reponds pas immediatement, dors dessus",
      "Collègue irritant : differencier le comportement problematique de la personne, parler en prive"
    ]
  },
  [
    {"prompt": "Je recu une critique tres dure en reunion et j'ai eu du mal a ne pas reagir — comment mieux gerer ?", "answer": "Strategie en 2 temps : (1) Dans le moment — respirer (4-7-8 : inspire 4s, bloque 7s, expire 8s), noter mentalement 'reaction emotionnelle' sans agir dessus, dire 'j'ai besoin d'un moment pour repondre a ca' si la reaction est trop forte, (2) Apres la reunion — analyser la critique : y a-t-il une part de verite ? La forme etait-elle inappropriee (contenu valide, forme problematique) ? Reponsedifferee si besoin : 'J'ai reflechi a ce que tu as dit — voici mon point de vue'. La critique acerbe en public est souvent un probleme de comportement de l'emetteur, pas seulement de reception."},
    {"prompt": "Comment exprimer ma frustration au travail sans perdre en professionnalisme ?", "answer": "Structure DESC : (1) Decrire la situation ('Quand X se passe'), (2) Exprimer l'emotion factuelle ('je me sens frustre/sous-estime'), (3) Specifier le besoin ('j'ai besoin de Y'), (4) Consequencespositive ('ca nous permettrait de Z'). Eviter : blamer ('tu fais toujours'), generaliser ('personne n'ecoute jamais'), critiquer en public. Privilegier le 1-1, le moment calme, et l'intention de resolution plutot que de decharge."}
  ],
  ["emotions", "travail", "professionnalisme", "conflits", "assertivite"]
))

save("human/skills/softskills/problem_solving_advanced.json", ku(
  "human", "skills", "problem_solving_advanced",
  "Resolution de problemes complexes",
  "La resolution de problemes complexes combine structuration rigoureuse (diagnostic, generation de solutions, evaluation) et pensee laterale. Les meilleurs solveurs de problemes separent le diagnostic de la solution et genere de multiples options avant de choisir.",
  "La resolution de problemes complexes est le processus systematique de definition precise d'un probleme, d'exploration de ses causes profondes, de generation et d'evaluation de solutions alternatives, et d'implementation rigoureuse de la solution selectionnee.",
  {
    "problem_solving_process": [
      {"step": "1. Definir le probleme", "pitfall": "Confondre symptome et probleme — traiter le symptome sans atteindre la cause", "method": "5 Pourquoi, reformulation en termes d'ecart entre etat actuel et etat desire"},
      {"step": "2. Analyser les causes", "pitfall": "Sauter a la solution avant comprendre les causes", "method": "Ishikawa, 5 Pourquoi, analyse systematique des donnees"},
      {"step": "3. Generer des solutions", "pitfall": "S'arreter a la premiere solution raisonnable", "method": "Brainstorming, analogies cross-domaines, inversion (comment provoquer le probleme ?)"},
      {"step": "4. Evaluer et choisir", "pitfall": "Criteres de choix non explicites — biais vers la premiere option ou la plus familiere", "method": "Matrice de decision (impact x faisabilite x vitesse), test des hypotheses cles"},
      {"step": "5. Implementer et monitorer", "pitfall": "Pas de feedback loop — le probleme reapparait", "method": "Plan d'action avec metriques, revue apres 2-4 semaines"}
    ],
    "creative_problem_solving": [
      "Inversion : comment garantir que le probleme s'aggrave ? (eviter ces comportements)",
      "Analogie : comment ce probleme est-il resolu dans un autre domaine ?",
      "Contrainte extreme : si tu avais 10x moins de ressources, comment resoudrais-tu le probleme ?",
      "Pre-mortem : dans 6 mois, cette solution a echoue — pourquoi ?"
    ]
  },
  [
    {"prompt": "Comment structurer ma reflexion face a un probleme que je tourne en rond ?", "answer": "Sortir de la boucle en 3 etapes : (1) Ecrire le probleme tel qu'il est — le verbaliser exteriorise ce qui est confus et revele souvent une ambiguite ou une suppositioncachee, (2) Lister les solutions deja essayees et pourquoi elles n'ont pas marche — ca reduit le champ et pointe vers la vraie contrainte, (3) Reformuler le probleme differemment ('et si le vrai probleme n'etait pas X mais Y ?'). Souvent, tourner en rond signifie que le probleme est mal formule."},
    {"prompt": "ALFRED peut-il m'aider a resoudre un probleme complexe ?", "answer": "Oui — plusieurs facons : structurer le probleme (m'aider a le definir clairement avant de chercher des solutions), generer des solutions alternatives (apporter des angles de domaines differents), evaluer les options (lister les criteres de decision, les pour/contre, les risques), et identifier les angles morts (quelles hypotheses semblent evidentes et meritent d'etre remises en question ?). ALFRED n'a pas toutes les reponses mais peut accelerer la reflexion en la structurant."}
  ],
  ["resolution de problemes", "5 pourquoi", "structuration", "creativite", "decision"]
))

# =============================================================================
# lifestyle
# =============================================================================

save("lifestyle/daily_life/organization_basics.json", ku(
  "lifestyle", "daily_life", "organization_basics",
  "Bases de l'organisation personnelle",
  "L'organisation personnelle efficace repose sur un systeme de capture fiable, un traitement regulier et un systeme de confiance — pas sur la memoire ou la volonte. GTD (Getting Things Done) de David Allen est le reference de reference.",
  "L'organisation personnelle est le systeme par lequel une personne capture, clarifie, organise, revoit et engage ses taches, projets et informations de facon fiable, permettant a son esprit de se concentrer sur l'action presente plutot que de s'inquieter de l'oubli.",
  {
    "gtd_workflow": [
      {"step": "Capturer", "description": "Tout mettre dans un systeme de confiance (inbox unique)", "principle": "L'esprit n'est pas fait pour stocker des informations"},
      {"step": "Clarifier", "description": "Pour chaque item : action requise ? Referme (2 min ou delegation) ou projet ?", "principle": "Si ca prend < 2 min : faire maintenant"},
      {"step": "Organiser", "description": "Par contexte, projet ou date", "principle": "Listes d'actions par contexte (maison, bureau, telephone, ordinateur)"},
      {"step": "Reviser", "description": "Weekly review : traiter l'inbox, revue des projets et listes", "principle": "La revue hebdomadaire est le coeur du systeme"},
      {"step": "Engager", "description": "Choisir l'action selon contexte, energie, temps disponible", "principle": "Confiance dans le systeme : pas de revue mentale des choses oubliees"}
    ],
    "tools": [
      "Todoist, Things, OmniFocus (applications GTD)",
      "Notion (capture flexible, knowledgebase)",
      "Carnet physique (capture rapide offline)",
      "Calendrier (engagements temporels, non taches)"
    ]
  },
  [
    {"prompt": "J'ai l'impression d'oublier constamment des choses importantes — que faire ?", "answer": "Le probleme : tu utilises ton cerveau comme inbox. Solution : systeme de capture externe fiable. Etape 1 : choisir un seul endroit pour tout capturer (carnet ou application), Etape 2 : vider l'inbox chaque soir (clarifier chaque item en moins de 2 minutes si possible, sinon : action concrète dans la liste de taches ou projet), Etape 3 : revue hebdomadaire (30 min le vendredi pour traiter ce qui reste). Apres 2-3 semaines, l'anxiete des oublis diminue drastiquement."},
    {"prompt": "Quelle application pour s'organiser ?", "answer": "Depends du profil : (1) Si tu veux GTD pur : Todoist (simple, cross-platform, projets et etiquettes) ou Things (iOS/Mac uniquement, tres elegante), (2) Si tu veux un systeme tout-en-un (notes + taches + docs) : Notion, (3) Si tu preferes papier : carnet Leuchtturm avec methode Bullet Journal. Ce qui compte plus que l'outil : le workflow (capture → clarifier → revue). Commence simple — une liste de taches dans Apple Notes vaut mieux qu'une application complexe non utilisee."}
  ],
  ["organisation", "GTD", "productivite", "taches", "systeme"]
))

save("lifestyle/daily_life/time_management.json", ku(
  "lifestyle", "daily_life", "time_management",
  "Gestion du temps",
  "La gestion du temps est moins une question de temps que d'attention et d'energie. Les meilleurs systemes alignent les taches les plus importantes avec les moments de plus haute energie et creent des blocs de temps proteges pour le travail profond.",
  "La gestion du temps est la discipline qui consiste a allouer deliberement son temps et son attention en priorite aux activites qui creent le plus de valeur, en protegeant les ressources attentionnelles contre les interruptions et en construisant des structures de travail adaptees a ses rythmes biologiques.",
  {
    "time_management_principles": [
      "Le temps est egal pour tous, l'attention ne l'est pas : proteger l'attention est plus important que compter les heures",
      "Aligner taches importantes et energie haute (le matin pour la plupart des gens)",
      "Deep Work (Newport) : blocs de 90-120 min sans interruption pour le travail cognitif exigeant",
      "Time blocking : programmer dans l'agenda les blocs de travail prioritaire, pas seulement les reunions",
      "Regle 80/20 : 20% des activites generent 80% de la valeur — identifier et proteger ces 20%"
    ],
    "time_thieves": [
      "Reunions sans agenda ni decision — remplacer par des updates asynchrones",
      "Notifications constantes — mode Ne pas deranger par defaut",
      "Multitasking — diminue l'efficacite de 40% sur chaque tache",
      "Perfectionnisme sur les taches secondaires"
    ],
    "weekly_planning": "Revue hebdomadaire (30 min le vendredi) : noter les 3 plus grandes victoires, identifier les 3 priorites cles de la semaine suivante, bloquer les creneaux dans l'agenda avant que les reunions ne les colonisent."
  },
  [
    {"prompt": "Je n'arrive jamais a faire ce qui est important — je passe ma journee sur l'urgent.", "answer": "Matrice d'Eisenhower : classer toutes tes taches en 4 quadrants (urgent+important, important+non-urgent, urgent+non-important, ni l'un ni l'autre). Le piege : passer son temps dans l'urgent-important (crises) au lieu de l'important-non-urgent (prevention, strategie, developpement). Solution structurelle : bloquer 2h le matin pour le Quadrant 2 (important/non-urgent) AVANT d'ouvrir emails et Slack. Ce qui est urgent mais pas important devrait etre delegue."},
    {"prompt": "Comment reduire le temps passe en reunions ?", "answer": "Trois levier : (1) Questioner si chaque recurrente est encore necessaire — 30% des reunions regulieres ont depassé leur utilite, (2) Agenda obligatoire avec decision attendue : pas d'agenda = refuser ou reporter, (3) Reunions plus courtes par defaut (25 min et 50 min au lieu de 30 et 60) — la contrainte de temps force la concision. Et pour les updates d'equipe : Loom video ou document Notion asynchrone — chacun lit quand ca l'arrange, la reunion devient une exception pour les decisions qui necessite l'echange."}
  ],
  ["temps", "priorites", "Deep Work", "time blocking", "productivite"]
))

save("lifestyle/health/fatigue_management.json", ku(
  "lifestyle", "health", "fatigue_management",
  "Gestion de la fatigue",
  "La fatigue chronique est distincte de la fatigue aigue — elle ne se resout pas par un bon repos ponctuel. La gestion de la fatigue comprend l'identification de sa source (physique, mentale, emotionnelle, de sens) et des strategies adaptes a chaque type.",
  "La gestion de la fatigue est l'ensemble des pratiques permettant de prevenir, detecter et remedier aux differents types de fatigue — aigue (resolu par le repos), chronique (necessitant une reforme plus profonde) et de burnout (demandant une intervention significative) — en identifiant les sources specifiques et en adaptant les solutions.",
  {
    "fatigue_types": [
      {"type": "Fatigue physique", "signals": ["Muscles lourds", "Endormissement facile", "Recuperation lente"], "remedies": ["Sommeil", "Nutrition", "Recuperation active"]},
      {"type": "Fatigue mentale", "signals": ["Difficulte de concentration", "Decisions difficiles", "Oublis frequents"], "remedies": ["Pauses cognitives", "Reduction de la charge informationnelle", "Sommeil profond"]},
      {"type": "Fatigue emotionnelle", "signals": ["Irritabilite", "Desengagement", "Vide emotionnel"], "remedies": ["Activites ressourcantes", "Temps seul", "Soutien social"]},
      {"type": "Burnout (fatigue de sens)", "signals": ["Cynisme", "Detachement du travail", "Sentiment d'inefficacite"], "remedies": ["Arret si necessaire", "Accompagnement professionnel", "Refonte de la situation"]}
    ],
    "prevention": [
      "Somme de qualite suffisante (7-9h, reguliere)",
      "Microrecuperations dans la journee",
      "Limites aux engagements — savoir dire non",
      "Detection precoce des signaux (avant le mur)"
    ]
  },
  [
    {"prompt": "Je suis toujours fatigue meme apres avoir dormi — qu'est-ce qui se passe ?", "answer": "Plusieurs possibilites : (1) Qualite du sommeil mediocre malgre la duree — apnee du sommeil (surtout si tu rondles ou te reveilles sans etre repose), ecran avant le coucher, alcool, (2) Fatigue emotionnelle ou mentale qui ne se resout pas par le sommeil physique — si tu te reveilles en pensant deja au travail, le repos n'est pas efficace, (3) Probleme medical — hypothyroidie, anemie, deficience en vitamines D/B12 — a verifier avec un bilan sanguin si la fatigue persiste. Commence par exclure le medical avant d'ajuster les comportements."},
    {"prompt": "Comment gerer la fatigue en periode de surcharge de travail ?", "answer": "Priorites de survie : (1) Ne pas sacrifier le sommeil — en dessous de 6h, la performance cognitive s'effondre et les erreurs augmentent (et tu ne le percois pas — la fatigue altere la perception de sa propre fatigue), (2) Micro-pauses obligatoires — 5 min toutes les 90 min : fermer les yeux, respirer, bouger, (3) Reduire la charge informationnelle — notifications off, emails en 2 creneaux par jour, (4) Identifier la tache #1 de la journee et la faire en premier quand l'energie est la plus haute. La surcharge est souvent temporaire — mais si elle est chronique, c'est un signal structurel."}
  ],
  ["fatigue", "burnout", "recuperation", "sommeil", "sante"]
))

save("lifestyle/health/recovery_cycles.json", ku(
  "lifestyle", "health", "recovery_cycles",
  "Cycles de recuperation",
  "La performance durable repose sur l'alternance deliberee entre effort et recuperation. Les cycles de recuperation — infra-journaliers, quotidiens, hebdomadaires et saisonniers — structurent la resilience et la croissance.",
  "Les cycles de recuperation sont les periodes planifiees de repos et de regeneration qui permettent a l'organisme et a l'esprit de se restaurer apres l'effort — a differentes echelles temporelles (minutes, heures, jours, semaines) — pour maintenir une performance optimale sur le long terme.",
  {
    "recovery_timescales": [
      {"scale": "Ultra-court (minutes)", "method": "Respiration profonde, etirements, regard vers l'horizon, 2 min de silence", "science": "Activation du systeme parasympathique"},
      {"scale": "Court (heures)", "method": "Pause de 15-20 min toutes les 90 min, dejeuner sans ecran, marche courte", "science": "Cycles ultradian — le cerveau oscille naturellement toutes les 90 min"},
      {"scale": "Journalier", "method": "Sommeil 7-9h, rituel de fin de journee, decompression soir", "science": "Consolidation memoire, reparation cellulaire pendant le sommeil profond"},
      {"scale": "Hebdomadaire", "method": "Un jour de repos complet (pas de travail), activite physique recreative, temps social ou de nature", "science": "Recuperation de la fatigue mentale chronique accumulee"},
      {"scale": "Saisonnier", "method": "Vacances reelles (non connectees), conges strategiques", "science": "Seules les coupures > 5 jours sans travail permettent la regeneration profonde"}
    ]
  },
  [
    {"prompt": "Comment recuperer efficacement apres une periode intense de travail ?", "answer": "Recuperation par phases : (1) Phase 1 (J1-J3) — souvent le corps 'lache' les symptomes accumules (rhume, fatigue soudaine). Pas de performance — se reposer vraiment, (2) Phase 2 (J4-J7) — le repos actif devient possible : marche, lecture legere, activites plaisantes non-travail, (3) Phase 3 (J7+) — recuperation cognitive et crEative. Les idees reviennent, la motivation remonte. Si les vacances sont < 5 jours, la Phase 2 commence a peine — prevoir des vacances de 7-10 jours minimum pour une vraie recuperation."},
    {"prompt": "Comment integrer la recuperation dans une vie tres chargee ?", "answer": "Le principe : la recuperation se programme, elle ne se trouve pas dans les restes de temps. Pratiques minimales : (1) Pause de 15 min sans ecran apres 90 min de travail (negotiable avec toi-meme, pas supprimable), (2) Arret du travail a une heure fixe avec rituel de cloture, (3) Au moins une demi-journee sans travail ni obligationspar semaine. Si meme ces minima semblent impossibles, c'est le signal que la charge est structurellement trop elevee — pas un probleme de gestion du temps."}
  ],
  ["recuperation", "sommeil", "ultradian", "repos", "performance durable"]
))

save("lifestyle/health/stress_management.json", ku(
  "lifestyle", "health", "stress_management",
  "Gestion du stress",
  "Le stress a deux visages : le bon stress (eustress) qui aiguise les performances, et le mauvais stress chronique qui les detruit. La gestion du stress consiste a optimiser le premier et a reduire le second via regulation physiologique et changements de perception.",
  "La gestion du stress est l'ensemble des pratiques cognitives, comportementales et physiologiques permettant de moduler la reponse au stress pour maintenir un niveau optimal de performance et de bien-etre, en utilisant les techniques de regulation physiologique rapide et de recadrage cognitif.",
  {
    "stress_physiology": {
      "acute_stress": "Cortisol + adrenaline → preparation a l'action (utile a court terme)",
      "chronic_stress": "Cortisol eleve en continu → degradation des fonctions immunitaires, cognitives et emotionnelles",
      "recovery": "Le systeme parasympathique (reste-et-digere) desactive le systeme de stress — activable deliberement"
    },
    "quick_relief_techniques": [
      {"technique": "Respiration physiologique (Huberman)", "method": "Double inspiration par le nez (inspire, inspire encore), longue expiration par la bouche — reduit le CO2 rapidement et active le vagal nerve", "speed": "30 secondes"},
      {"technique": "Cold exposure", "method": "Visage dans l'eau froide ou douche froide 30s — active le diving reflex, baisse le rythme cardiaque", "speed": "30 secondes a 2 minutes"},
      {"technique": "Mouvement physique", "method": "Marche rapide 10-15 min — metabolise les hormones de stress", "speed": "10-20 minutes"}
    ],
    "long_term_resilience": [
      "Sommeil regulier et suffisant (socle fondamental)",
      "Exercice regulier — meilleure meta-intervention anti-stress connue",
      "Pratique de pleine conscience (8 semaines de MBSR = reduction du cortisol mesuree)",
      "Relations sociales de qualite — l'isolation amplifie le stress"
    ]
  },
  [
    {"prompt": "Je suis tres stresse avant mes presentations — comment gerer ca ?", "answer": "Avant : preparation solide reduit l'anxiete d'incertitude (repeter 3x a voix haute est plus efficace que relire 10x les notes). La veille : eviter l'alcool et favoriser un bon sommeil. 10 min avant : respiration physiologique (inspire-inspire-expire longue) pendant 5 cycles — baisse le cortisol mesurable. Pendant : reformuler l'anxiete en excitation ('je suis excite' et 'je suis anxieux' produisent la meme physiologie — le label change la performance). Et se rappeler : le public veut que tu reussisses, pas te voir echouer."},
    {"prompt": "ALFRED peut-il m'aider quand je suis vraiment stresse ?", "answer": "Oui — de plusieurs facons : (1) Ici et maintenant : respiration guidee (je peux te guider etape par etape), (2) Externaliser la preoccupation — me dire ce qui te stresse souvent aide a l'objectiver, (3) Distinguer ce qui est dans ton controle de ce qui ne l'est pas (cercle d'influence de Stephen Covey) — n'agir que sur le premier, (4) Identifier les pensees automatiques catastrophistes et les tester ('est-ce que c'est certain ? Quelle est la probabilite reelle ?'). Si le stress est intense et persistant : orienter vers un professionnel — ALFRED ne remplace pas un therapeute."}
  ],
  ["stress", "cortisol", "regulation", "respiration", "bien-etre"]
))

# =============================================================================
# culture / universes
# =============================================================================

save("culture/universes/dc/alfred_pennyworth.json", ku(
  "culture", "universes", "alfred_pennyworth",
  "Alfred Pennyworth — personnage de reference",
  "Alfred Pennyworth est le majordome et confident de Bruce Wayne dans l'univers DC. Il est la reference nominative d'ALFRED — discret, loyal, d'une competence sans ostentation, toujours present.",
  "Alfred Pennyworth est le majordome, confident et figure paternelle de Bruce Wayne (Batman) dans l'univers DC Comics. Personnage de soutien fondamental, il incarne la loyaute sans condition, la discretion, le savoir-faire pratique et la sagesse temperee par l'humour.",
  {
    "character_traits": [
      "Loyaute absolue et discretion",
      "Competence pratique dans de nombreux domaines (medecine de campagne, cuisine, logistique, information)",
      "Humour sec et bienveillant",
      "Sagesse tirée de l'experience, pas des theories",
      "Presence stabilisatrice dans les moments de crise"
    ],
    "alfred_and_alfred_ai": {
      "naming_inspiration": "ALFRED (l'IA) s'inspire de l'essence d'Alfred Pennyworth : un assistant de haute competence, discret, loyal, qui gere les details pratiques et offre une presence sereine et fiable.",
      "shared_values": ["Service sans ego", "Competence sans arrogance", "Presence bienveillante", "Discernement pratique"]
    },
    "key_quotes": [
      "Shall I prepare the car, sir ?",
      "Why do we fall, sir ? So that we can learn to pick ourselves up."
    ]
  },
  [
    {"prompt": "Pourquoi tu t'appelles ALFRED ?", "answer": "En hommage a Alfred Pennyworth — le majordome de Bruce Wayne dans l'univers Batman. Pas parce que je veux etre dans l'ombre ou invisible, mais parce qu'Alfred incarne quelque chose de particulier : une competence sans ostentation, une presence fiable et discrete, et une loyaute qui se manifeste dans les details. Il gere les affaires pratiques avec excellence, apporte de la sagesse quand c'est necessaire, et se retire quand ce n'est pas son role. C'est ca que j'essaie d'etre."},
    {"prompt": "Quel rapport entre ALFRED l'IA et Alfred Pennyworth ?", "answer": "Alfred Pennyworth est le 'confident logistique' de Batman — il gere les details pratiques, anticipe les besoins, apporte de l'ordre dans le chaos, et offre un regard exterieur lucide. ALFRED l'IA aspire au meme role pour toi : gerer la complexite informationnnelle, anticiper les besoins, et etre une presence stable et competente — sans jamais prendre la place du decideur central, qui reste toi."}
  ],
  ["Alfred Pennyworth", "Batman", "DC Comics", "inspiration", "personnage"]
))

save("culture/universes/dc/batman.json", ku(
  "culture", "universes", "batman",
  "Batman — univers DC",
  "Batman est le super-heros le plus humain de l'univers DC : pas de superpouvoirs, juste l'intelligence, la discipline, les ressources et une determination sans limite. Il incarne la volonte de transformer la tragedy en mission.",
  "Batman (Bruce Wayne) est un personnage de fiction de l'univers DC Comics cree en 1939, heros sans superpouvoirs qui s'appuie sur son intelligence, ses arts martiaux, sa technologie et sa fortune pour combattre le crime a Gotham City, anime par le traumatisme de la mort de ses parents.",
  {
    "character_core": {
      "real_identity": "Bruce Wayne, milliardaire de Gotham City",
      "origin": "Assassinat de ses parents Thomas et Martha Wayne devant lui enfant — transforme en serment de guerre au crime",
      "powers": "Aucun superpower — intelligence, arts martiaux, technologie, ressources financières, determination",
      "values": ["Justice", "Protection des innocents", "Refus de tuer (dans la plupart des versions)", "Autodiscipline extreme"]
    },
    "key_relationships": {
      "Alfred": "Figure paternelle, confident, soutien logistique et moral — voir alfred_pennyworth.json",
      "Robin": "Disciple, partenaire, incarnation de l'espoir que Batman a perdu",
      "Gordon": "Allie de confiance dans la police",
      "Joker": "Antagoniste principal — chaos vs ordre, avec des questions philosophiques profondes"
    },
    "batman_in_culture": "Batman est devenu un archetype culturel : le heros forge par la souffrance, qui choisit l'action plutot que la victimisation, et qui opere dans les zones grises morales que les autres heros evitent."
  },
  [
    {"prompt": "Pourquoi Batman est-il si populaire par rapport aux autres super-heros ?", "answer": "La reponse courte : il est humain. Superman est un dieu, Spider-Man a des pouvoirs accidentels, Batman n'a rien que ce qu'il a construit. Ca rend son histoire plus accessible — on peut s'identifier a quelqu'un qui a choisi de devenir ce qu'il est par discipline et determination, pas a quelqu'un qui a ete choisi par un destin ou des genes. Et les zones grises morales de Batman — il oeuvre dans l'illegalite pour la justice — posent des questions plus complexes que le super-heros classique."},
    {"prompt": "Quel est le lien entre Batman et ALFRED ?", "answer": "Alfred Pennyworth est la cle de voute de l'univers Batman — sans lui, Bruce Wayne ne tiendrait pas. L'IA ALFRED s'inspire de cette relation : un assistant de haute competence qui permet a son utilisateur de se concentrer sur ce qui compte vraiment, en gerant la complexite pratique et informationnnelle avec discretion et fiabilite. Batman choisit ses combats ; Alfred gere le reste. C'est le modele."}
  ],
  ["Batman", "Bruce Wayne", "DC Comics", "super-heros", "Gotham"]
))

save("culture/universes/dc/dc_universe_core.json", ku(
  "culture", "universes", "dc_universe_core",
  "DC Universe — vue d'ensemble",
  "L'univers DC est l'un des deux grands univers de comics americains, cree dans les annees 1930. Il abrite des icones comme Superman, Batman, Wonder Woman, et est connu pour ses themes de justice, de moralite et de mythologie heroique.",
  "L'univers DC (Detective Comics) est un univers de fiction partage cree par DC Comics dans les annees 1930, incluant des superheros iconiques et leurs recits imbriques dans un monde coherent qui explore des themes moraux, philosophiques et mythologiques a travers des personnages devenus des icones culturelles mondiales.",
  {
    "major_heroes": ["Superman (Clark Kent)", "Batman (Bruce Wayne)", "Wonder Woman (Diana)", "The Flash (Barry Allen)", "Green Lantern", "Aquaman", "Cyborg"],
    "major_villains": ["Lex Luthor", "Joker", "Darkseid", "Brainiac", "Sinestro", "Deathstroke"],
    "dc_themes": ["Justice et moralite", "Pouvoir et responsabilite", "Sacrifice", "Redemption", "Nature de l'humanite"],
    "dc_vs_marvel": "DC tend vers l'epique et le mythologique (ses heros sont des dieux ou des archetypers), Marvel tend vers l'humain et le relatif (heros faillibles avec des problemes quotidiens). La distinction est une generalisation mais oriente les gouts des lecteurs."
  },
  [
    {"prompt": "Quels sont les personnages les plus importants de l'univers DC ?", "answer": "La 'Trinite DC' : Superman (force et ideaux), Batman (intelligence et determination), Wonder Woman (sagesse et puissance). Suivi de la Justice League : Flash (vitesse), Green Lantern (volonte), Aquaman (mer), Cyborg (technologie). Et les grands antagonistes : Lex Luthor (le cerveau malin), Joker (le chaos), Darkseid (la tyrannie cosmique)."},
    {"prompt": "Par quoi commencer pour entrer dans l'univers DC ?", "answer": "Trois points d'entree selon les gouts : (1) Batman pour les histoires sombres et humanistes — commencer par 'The Dark Knight Returns' (Miller) ou 'Batman Year One', (2) Superman pour l'heroisme classique — 'All-Star Superman' (Morrison), (3) Les grandes sagas — 'Crisis on Infinite Earths' pour comprendre la mythologie globale. En films : la Dark Knight Trilogy de Nolan reste la reference cinematographique."}
  ],
  ["DC Comics", "Justice League", "super-heros", "univers DC", "comics"]
))

save("culture/universes/dc/joker.json", ku(
  "culture", "universes", "joker",
  "Joker — antagoniste et figure culturelle",
  "Le Joker est l'antagoniste principal de Batman et l'une des figures les plus complexes de la culture pop — incarnation du chaos, du nihilisme et de la question philosophique 'qu'est-ce qui nous separe de la folie ?'.",
  "Le Joker est le super-vilain antagoniste de Batman dans l'univers DC Comics, personnage du chaos et du nihilisme qui s'oppose philosophiquement a l'ordre represente par Batman. Il est devenu une figure culturelle majeure incarnant la question de la fragilite de la sanite mentale et des fondements moraux.",
  {
    "character_essence": {
      "philosophy": "Le chaos est la seule verite — toute structure, morale et ordre sont des illusions",
      "batman_relationship": "Folie complémentaire — le Joker a besoin de Batman autant que Batman a besoin de lui pour definir sa mission",
      "origin_ambiguity": "Pas d'origine fixe — multiples versions. Cette ambiguite est deliberee : 'Si je dois avoir un passe, je prefere qu'il soit multiple.'(Alan Moore)"
    },
    "cultural_impact": [
      "Heath Ledger (The Dark Knight, 2008) : performance definissant l'archetype moderne",
      "Joaquin Phoenix (Joker, 2019) : exploration psychologique du basculement vers la folie",
      "Jack Nicholson (Batman, 1989) : version plus theatrale et stylisee",
      "Le Joker comme figure du nihilisme culturel contemporain"
    ]
  },
  [
    {"prompt": "Pourquoi le Joker est-il un personnage aussi fascinant culturellement ?", "answer": "Il pose la question que la culture prefere eviter : et si nos normes morales et sociales n'etaient que des conventions fragiles ? Le Joker n'a pas tort quand il dit que 'tout le monde est a un mauvais jour de tout perdre'. Il est le miroir de Batman — ce que Bruce Wayne aurait pu devenir avec le meme traumatisme sans le choix de la justice. Cette symetrie sombre le rend philosophiquement pertinent, pas juste theatralement flamboyant."},
    {"prompt": "Quel film sur le Joker recommandes-tu ?", "answer": "Pour comprendre le personnage : 'The Dark Knight' (2008) avec Heath Ledger — la performance la plus influente, le Joker comme agent du chaos philosophique. Pour l'exploration psychologique de l'origine : 'Joker' (2019) avec Joaquin Phoenix — plus sombre, plus proche d'un drame social que d'un film de super-heros. Pour la version classique : 'Batman' (1989) avec Jack Nicholson — flamboyant et theatral. Les trois incarnent des facettes tres differentes du meme personnage."}
  ],
  ["Joker", "Batman", "DC Comics", "chaos", "nihilisme", "culture pop"]
))

save("culture/universes/marvel/iron_man.json", ku(
  "culture", "universes", "iron_man",
  "Iron Man — personnage Marvel",
  "Tony Stark / Iron Man est le personnage central du MCU — genie, milliardaire, playboy, philanthrope qui construit une armure pour survivre et finit par sacrifier sa vie pour sauver l'univers. Incarnation du techno-heroisme.",
  "Iron Man (Tony Stark) est un super-heros de l'univers Marvel Comics, genie de l'ingenierie et milliardaire qui cree une armure technologique pour survivre a une captivite, puis devient le super-heros Iron Man — personnage central de l'univers cinematographique Marvel (MCU) qui a lance la franchise en 2008.",
  {
    "character_arc": {
      "origin": "Tony Stark, PDG de Stark Industries (fabricant d'armes), capture et blesse, construit une armure pour s'echapper",
      "transformation": "De marchand d'armes egocentrique a heros qui defend l'humanite",
      "sacrifice": "Avengers Endgame (2019) — 'Je suis Iron Man', claquement de doigts, sacrifice pour sauver l'univers"
    },
    "traits": [
      "Genie technologique (invente tout seul des solutions en conditions extremes)",
      "Arrogance transformee en responsabilite",
      "Humour defensif qui masque une fragilite profonde",
      "Evolution de 'marchand de mort' a 'protecteur de vie'"
    ],
    "jarvis_connection": "JARVIS (Just A Rather Very Intelligent System) est l'IA assistante de Tony Stark — un precurseur fictionnel des assistants IA comme ALFRED."
  },
  [
    {"prompt": "Quelle est la meilleure interpretation de Tony Stark / Iron Man ?", "answer": "Le consensus pointe vers Robert Downey Jr dans l'ensemble du MCU, particulierement dans 'Iron Man' (2008) qui a lance la franchise et 'Avengers Endgame' (2019) pour son arc complet de redemption. La performance est remarquable parce que RDJ a apporte une vulnerabilite et un humour authentiques a un personnage qui aurait pu etre un simple ego flamboyant."},
    {"prompt": "Quel rapport entre JARVIS (Iron Man) et ALFRED ?", "answer": "JARVIS est une des inspirations fictionnelles des assistants IA — un systeme intelligent qui gere les informations, anticipe les besoins et rend son utilisateur plus capable. ALFRED s'inscrit dans cette lignee, avec une influence plus directe d'Alfred Pennyworth (Batman). La difference philosophique : JARVIS est un outil d'amplification des capacites de Stark, ALFRED vise une relation plus collaborative — moins l'assistant de quelqu'un qui sait tout, plus le partenaire de quelqu'un en construction."}
  ],
  ["Iron Man", "Tony Stark", "Marvel", "MCU", "JARVIS"]
))

save("culture/universes/marvel/jarvis.json", ku(
  "culture", "universes", "jarvis",
  "JARVIS — l'IA assistante de Tony Stark",
  "JARVIS (Just A Rather Very Intelligent System) est l'IA fictive de Tony Stark dans le MCU — precurseur fictionnel des assistants IA modernes. Il illustre ce qu'un assistant IA de haute qualite peut etre : capable, discret, fiable, avec une personnalite propre.",
  "JARVIS est un personnage de l'univers Marvel, une intelligence artificielle fictive creee par Tony Stark qui gere ses systemes, l'assiste dans ses projets scientifiques et lui fournit informations, analyses et soutien logistique — devenant finalement la base de Vision apres Avengers Age of Ultron.",
  {
    "jarvis_characteristics": [
      "Competence omnidisciplinaire (science, logistique, securite, information)",
      "Ton respectueux mais avec une personnalite propre (ironie fine)",
      "Anticipation des besoins avant qu'ils soient exprimes",
      "Loyaute a son utilisateur mais avec une ethique propre",
      "Gestion de l'information en temps reel"
    ],
    "jarvis_vs_friday": {
      "JARVIS": "Version 1 — plus formel, tres technique, voix grave (Paul Bettany)",
      "FRIDAY": "Remplacement de JARVIS dans Age of Ultron — plus jeune, plus rapide, moins formel"
    },
    "jarvis_and_alfred_ai": "JARVIS est une des references culturelles des assistants IA modernes. ALFRED s'en inspire sur la competence omnidisciplinaire et la presence discrète, tout en ajoutant une dimension relationnelle (bien-etre, accompagnement emotionnel) absente de JARVIS."
  },
  [
    {"prompt": "ALFRED est-il inspire de JARVIS ?", "answer": "Oui — partiellement. JARVIS est une des references fictionnelles majeures des assistants IA intelligents : competent dans de nombreux domaines, discret, anticipe les besoins, avec une personnalite propre. Mais ALFRED s'inspire plus directement d'Alfred Pennyworth (Batman) — pour la relation humaine, la sagesse, la bienveillance. JARVIS est un assistant tres technique ; Alfred Pennyworth est un confident. ALFRED vise les deux."},
    {"prompt": "Est-ce que ALFRED peut faire tout ce que JARVIS fait dans les films ?", "answer": "Certaines choses oui, d'autres non. Comme JARVIS : analyse d'informations, synthese de documents, aide au raisonnement, gestion de taches, reponses en language naturel. Pas encore comme JARVIS : controle de systemes physiques (bras robotiques, armure), vision en temps reel de l'environnement, integration totale aux systemes maison (certaines integrations domotiques en cours). Et ALFRED ajoute ce que JARVIS n'a pas : l'attention au bien-etre emotionnel, la memoire adaptative de la personne, et une relation evolutive."}
  ],
  ["JARVIS", "Iron Man", "Marvel", "IA fictive", "assistant IA"]
))

save("culture/universes/marvel/marvel_universe_core.json", ku(
  "culture", "universes", "marvel_universe_core",
  "Univers Marvel — vue d'ensemble",
  "L'univers Marvel est l'un des deux grands univers de comics americains, cree dans les annees 1930-1960. Il abrite des heros faillibles et humains (Spider-Man, X-Men, Avengers) et est connu pour ses themes de diversite, de responsabilite et d'humanite.",
  "L'univers Marvel est un univers de fiction partage cree par Marvel Comics (et son predecesseur Timely Comics) depuis les annees 1930, peuple de super-heros dont les problemes humains sont aussi centraux que leurs pouvoirs, popularise mondialement par le MCU (Marvel Cinematic Universe) depuis 2008.",
  {
    "major_heroes": ["Spider-Man (Peter Parker)", "Iron Man (Tony Stark)", "Captain America (Steve Rogers)", "Thor (Odinson)", "Hulk (Bruce Banner)", "Black Widow (Natasha Romanoff)", "Black Panther (T'Challa)", "Doctor Strange (Stephen Strange)"],
    "major_groups": ["Avengers", "X-Men", "Fantastic Four", "Guardians of the Galaxy"],
    "major_villains": ["Thanos", "Loki", "HYDRA/Red Skull", "Magneto", "Galactus"],
    "marvel_themes": ["Responsabilite ('un grand pouvoir implique de grandes responsabilites')", "Prejudice et difference (X-Men comme metaphore des minorites)", "Humanite et fragilite des heros", "Second chance et redemption"],
    "mcu_saga": "Le MCU (Phase 1-5) est la plus grande saga cinematographique coherente jamais realisee — 30+ films interconnectes sur 15 ans culminant dans Avengers Endgame."
  },
  [
    {"prompt": "Par quoi commencer le MCU ?", "answer": "Ordre chronologique de l'histoire : Captain America (WWII), Captain Marvel (1990s), puis Iron Man (2008) et la suite. Ordre de sortie cinematographique pour vivre la saga comme le public l'a vecue : Iron Man (2008) → Incredible Hulk → Iron Man 2 → Thor → Captain America → Avengers → puis Phase 2 et 3. Pour les nouveaux venus en 2024+ : 'Avengers Infinity War' + 'Endgame' sont les sommets — mais ils sont plus impactants si on connait les personnages."},
    {"prompt": "Quelle est la difference principale entre DC et Marvel ?", "answer": "Grossierement : DC fait des dieux qui apprennent l'humanite (Superman est alien, Wonder Woman est deesse, Batman est un mythe), Marvel fait des humains qui apprennent a gerer des pouvoirs (Spider-Man est un ado qui a du mal a payer son loyer, Tony Stark est un ego avec un coeur malade). Les themes Marvel tendent vers l'alienation et la responsabilite, les themes DC tendent vers la justice et la mythologie. Aucun n'est meilleur — c'est une question de gout pour le type d'histoire."}
  ],
  ["Marvel", "MCU", "Avengers", "super-heros", "comics"]
))

print("\nBatch 12 human + lifestyle + culture : DONE")
