"""
Nouveau domaine : knowledges/communication/
20 knowledge units couvrant communication verbale, ecrite, non-verbale,
influence, prise de parole, ecoute, negociation, storytelling...
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
      "id": f"knowledges.communication.{subdomain}.{stem}",
      "title": title,
      "domain": "communication",
      "subdomain": subdomain,
      "status": "validated",
      "summary": summary,
      "core_definition": core_def,
      "knowledge": knowledge,
      "example_answers": examples,
      "response_guidance": {
        "tone": "clair, ancre dans la pratique, avec des exemples concrets",
        "structure": ["expliquer le principe", "illustrer par un exemple", "proposer une technique actionnable"],
        "avoid": ["jargon academique sans traduction", "trop theorique", "ignorer le contexte de l'interlocuteur"]
      },
      "tags": tags + ["communication"],
      "related_knowledge_units": []
    }

# ── 1. verbal / active_listening ────────────────────────────────────────────
save("communication/verbal/active_listening.json", ku(
  "active_listening", "verbal",
  "Ecoute active",
  "L'ecoute active est une presence totale a l'interlocuteur — signaux d'attention, reformulation, questions ouvertes — qui cree la confiance et fait emerguer le sens reel derriere les mots.",
  "L'ecoute active est une competence de communication consistant a etre pleinement present a son interlocuteur, a signaler cette presence par des comportements verbaux et non-verbaux, et a reflechir le contenu et l'emotion entendue pour confirmer la comprehension et approfondir le dialogue.",
  {
    "techniques": [
      {"technique": "Reformulation", "description": "Redire avec ses propres mots ce qu'on a compris", "effet": "Valide la comprehension, invite la correction"},
      {"technique": "Miroir verbal", "description": "Repeter les 2-3 derniers mots cles de l'interlocuteur", "effet": "Encourage a approfondir sans diriger"},
      {"technique": "Question ouverte", "description": "'Qu'est-ce que tu veux dire par... ?', 'Comment vis-tu ca ?'", "effet": "Ouvre l'espace sans forcer la direction"},
      {"technique": "Silence actif", "description": "Laisser un silence apres une reponse — ne pas le remplir", "effet": "L'interlocuteur souvent ajoute l'essentiel dans ce silence"},
      {"technique": "Signaux d'attention", "description": "Hochements de tete, 'je vois', 'mmh', contact visuel", "effet": "Signal que tu es present et que tu ecoutes"}
    ],
    "blockers": [
      "Formuler sa reponse pendant que l'autre parle",
      "Interrompre pour finir les phrases",
      "Juger ou conseiller avant que l'autre ait termine",
      "Ramener a sa propre experience ('moi aussi j'ai...')"
    ],
    "levels": [
      {"level": 1, "name": "Ecoute cosmétique", "description": "On entend mais on ne traite pas"},
      {"level": 2, "name": "Ecoute selective", "description": "On capte ce qui nous interesse"},
      {"level": 3, "name": "Ecoute attentive", "description": "On suit le contenu activement"},
      {"level": 4, "name": "Ecoute empathique", "description": "On capte le contenu ET l'emotion — ecoute active profonde"}
    ]
  },
  [
    {"prompt": "Comment mieux ecouter en reunion quand j'ai tendance a penser a autre chose ?", "answer": "Deux pratiques : (1) Prendre des notes a la main — l'ecriture physique force l'attention et reduit le mind-wandering, (2) Chercher activement une chose nouvelle ou surprenante dans ce que dit l'autre. Cette mission cognitive occupe l'esprit et empeche la divagation. Et si tu perds le fil : 'Peux-tu reformuler la partie sur X ?' — c'est honnete et ca relance l'echange."},
    {"prompt": "Comment montrer a quelqu'un que je l'ecoute vraiment ?", "answer": "Trois signaux forts : (1) Ne pas toucher son telephone, (2) Reformuler avant de repondre ('Si je comprends bien, tu dis que...'), (3) Poser une question sur ce qu'il vient de dire avant de changer de sujet. Ces trois comportements creent une experience d'ecoute perceptible — la plupart des gens ne les pratiquent pas, ce qui les rend tres remarquables quand tu le fais."}
  ],
  ["ecoute", "reformulation", "attention", "empathie", "verbal"]
))

# ── 2. verbal / assertive_communication ─────────────────────────────────────
save("communication/verbal/assertive_communication.json", ku(
  "assertive_communication", "verbal",
  "Communication assertive",
  "L'assertivite est la capacite a exprimer ses besoins, opinions et limites de facon claire et respectueuse — sans agressivite ni passivite. C'est le point d'equilibre entre s'effacer et ecraser.",
  "La communication assertive est le style de communication dans lequel une personne exprime ses pensees, besoins et limites de facon directe, honnete et respectueuse, en prenant soin de ses propres droits sans empieter sur ceux des autres.",
  {
    "styles_comparison": [
      {"style": "Passif", "behaviour": "Evite le conflit, ne dit pas ce qu'il pense, s'efface", "consequence": "Frustration, ressentiment accumule, manque de respect de soi"},
      {"style": "Agressif", "behaviour": "Impose son point de vue, coupe la parole, intimide", "consequence": "Conflits, peur des autres, relation degradee"},
      {"style": "Passif-agressif", "behaviour": "Exprime son mecontentement de facon indirecte (sarcasme, silence)", "consequence": "Confusion, confiance erodee, tension latente"},
      {"style": "Assertif", "behaviour": "Dit ce qu'il pense clairement, respecte l'autre, pose ses limites", "consequence": "Respect mutuel, confiance, relations authentiques"}
    ],
    "desc_model": {
      "D": "Decrire la situation objectivement ('Quand tu envoies un email a toute l'equipe sans m'en informer...')",
      "E": "Exprimer l'emotion ressentie ('...je me sens mis de cote...')",
      "S": "Specifier le besoin ('...j'ai besoin d'etre inclus dans ces decisions...')",
      "C": "Consequence positive ('...ce qui nous permettrait de mieux collaborer')"
    },
    "assertiveness_phrases": [
      "Je comprends ton point de vue, et voici le mien...",
      "Je ne suis pas disponible pour ca — je peux t'aider sur X a la place.",
      "J'ai besoin qu'on revoit ca ensemble avant de continuer.",
      "Ce que tu as dit m'a blesseE. Voici pourquoi."
    ]
  },
  [
    {"prompt": "Comment dire non au travail sans etre impoli ?", "answer": "Template : (1) Reconnaitre la demande ('Je comprends que c'est urgent pour toi'), (2) Exprimer ta contrainte ('En ce moment je suis sur X jusqu'a vendredi — je ne peux pas livrer de qualite si je prends ca en plus'), (3) Proposer une alternative ('Je peux t'aider lundi, ou orienter vers [personne] si c'est vraiment urgent'). Un non avec explication et alternative est toujours mieux recu qu'un oui qui ne tient pas."},
    {"prompt": "Je n'ose pas contredire mon manager meme quand j'ai raison — comment faire ?", "answer": "Reframe d'abord : contredire n'est pas disrespecteux — c'est de la valeur ajoutee si c'est bien amene. Formule : 'J'ai une perspective differente que j'aimerais partager — est-ce qu'on peut en parler ?' Puis : faits d'abord, opinion ensuite ('Les donnees montrent X, ce qui m'amene a penser Y'). Un manager solide apprecie les gens qui osent dire des choses difficiles avec respect. Si ton manager sanctionne les opinions differentes respectueuses, c'est une information importante sur l'environnement."}
  ],
  ["assertivite", "limites", "non", "respect", "DESC"]
))

# ── 3. verbal / difficult_conversations ─────────────────────────────────────
save("communication/verbal/difficult_conversations.json", ku(
  "difficult_conversations", "verbal",
  "Conversations difficiles",
  "Les conversations difficiles (feedback negatif, annonce mauvaise nouvelle, desaccord profond) se preparent, se cadrent et se conduisent selon des principes specifiques — elles ne s'improvisent pas sous peine de degats relationnels durables.",
  "Les conversations difficiles sont des echanges interpersonnels portant sur des sujets a forte charge emotionnelle ou a enjeux relationnels eleves, qui necessitent une preparation deliberee, un cadrage explicite et des techniques de communication adaptees pour etre productives sans deteriorer la relation.",
  {
    "preparation": [
      "Clarifier son intention : informer, corriger, maintenir la relation, changer un comportement ?",
      "Identifier les faits objectifs vs les interpretations",
      "Anticiper la reaction emotionnelle de l'autre et préparer sa propre regulation",
      "Choisir le bon moment et le bon lieu (prive, calme, moment non stresse)"
    ],
    "crucial_conversations_framework": {
      "source": "Kerry Patterson & al., Crucial Conversations (2002)",
      "start_with_heart": "Clarifier ce qu'on veut vraiment pour soi, l'autre et la relation",
      "safety": "Maintenir un climat de securite — si l'autre se ferme, reformuler l'intention",
      "STATE": "Share facts, Tell your story, Ask for their path, Talk tentatively, Encourage testing"
    },
    "hard_topic_scripts": {
      "feedback_negatif": "'J'ai remarque [fait] et ca m'a preoccupe parce que [impact]. J'aimerais comprendre ta perspective et voir comment on peut remedier a ca ensemble.'",
      "mauvaise_nouvelle": "'Je vais te dire quelque chose de difficile et je veux d'abord te dire que je tiens a toi/notre relation. [Nouvelle]. Je suis la pour en parler.'",
      "desaccord_profond": "'Je vois les choses differemment et j'aimerais qu'on prenne le temps d'explorer les deux perspectives avant de conclure.'"
    }
  },
  [
    {"prompt": "Comment donner un feedback negatif sans briser la relation ?", "answer": "Trois regles : (1) Prive, jamais devant d'autres, (2) Faits specifiques, pas jugements generaux ('tu arrives en retard aux reunions depuis 3 semaines' pas 'tu es irresponsable'), (3) Impact + curiosite ('ca cree des problemes de coordination — j'aimerais comprendre ce qui se passe pour toi'). Clore sur une question ouverte, pas une condamnation. Le feedback qui reste est celui qui respecte la personne tout en etant clair sur le probleme."},
    {"prompt": "J'ai une conversation difficile a avoir avec un ami — comment me preparer ?", "answer": "Avant : noter les faits objectifs (pas les interpretations), clarifier ce que tu veux que la relation devienne apres cette conversation, et choisir un moment ou vous etes tous les deux calmes et non presses. Debut de conversation : 'J'ai quelque chose d'important a te dire et c'est parce que notre amitie compte pour moi.' Pendant : ecouter sa reponse sans te defendre immediatement — il a peut-etre une perspective que tu n'as pas. Apres : resumer ce sur quoi vous avez avance."}
  ],
  ["feedback", "conversations difficiles", "conflit", "relation", "courage"]
))

# ── 4. verbal / questioning_techniques ──────────────────────────────────────
save("communication/verbal/questioning_techniques.json", ku(
  "questioning_techniques", "verbal",
  "Art du questionnement",
  "Les questions sont les outils les plus puissants de la communication — elles dirigent l'attention, ouvrent ou ferment l'espace de reponse, et revelent ce qui n'est pas dit. Maitriser les types de questions change radicalement la qualite des echanges.",
  "Le questionnement est l'art d'utiliser les questions de facon strategique pour explorer, comprendre, guider ou challenger — en distinguant les questions ouvertes (qui elargissent), les questions fermees (qui confirment), les questions de recadrage (qui changent la perspective) et les questions de Socrate (qui conduisent a la decouverte).",
  {
    "question_types": [
      {"type": "Ouverte", "function": "Elargir, explorer", "examples": ["Qu'est-ce que tu veux dire ?", "Comment tu vis ca ?", "Qu'est-ce qui te preoccupe le plus ?"]},
      {"type": "Fermee", "function": "Confirmer, preciser", "examples": ["Est-ce que tu es d'accord ?", "As-tu recu mon email ?"]},
      {"type": "Miroir", "function": "Approfondir sans diriger", "examples": ["[Repeter 2-3 mots cles de ce qu'on vient de dire]"]},
      {"type": "Hypothetique", "function": "Explorer des scenarios", "examples": ["Et si on essayait X, que se passerait-il ?", "Qu'est-ce qui changerait si... ?"]},
      {"type": "Recadrage", "function": "Changer la perspective", "examples": ["Comment pourrait-on voir ca differemment ?", "Et si c'etait une opportunite ?"]},
      {"type": "Socratique", "function": "Conduire a la decouverte par l'interlocuteur", "examples": ["Sur quoi bases-tu cette affirmation ?", "Qu'est-ce qui prouve ca ?", "Et si c'etait faux, que se passerait-il ?"]}
    ],
    "power_questions": [
      "'Qu'est-ce que tu veux vraiment ?' — touche le besoin profond, pas la demande de surface",
      "'Qu'est-ce qui t'en empeche ?' — identifie le vrai blocage",
      "'Si tu savais deja la reponse, ca serait quoi ?' — contourne la peur de 'ne pas savoir'",
      "'Qu'est-ce qui serait possible si ce probleme n'existait plus ?' — oriente vers les solutions"
    ]
  },
  [
    {"prompt": "Comment poser de meilleures questions en entretien de recrutement ?", "answer": "Eviter les questions fermees ('Tu travailles bien en equipe ?') — elles appellent un oui automatique. Privilegier : (1) Comportementales ('Decris-moi une situation ou tu as eu un conflit avec un collegue — comment tu l'as gere ?'), (2) Situationnelles ('Si tu arrivais et que tu trouvais X probleme, qu'est-ce que tu ferais ?'), (3) Projectives ('Qu'est-ce qui te donnerait l'impression d'avoir reussi dans ce poste dans 6 mois ?'). Et ecouter vraiment — pas formuler la prochaine question pendant que l'autre repond."},
    {"prompt": "Comment aider quelqu'un qui tourne en rond sur un probleme sans lui donner la reponse ?", "answer": "Mode coaching : (1) 'Qu'est-ce que tu as deja essaye ?' — inventorie sans juger, (2) 'Qu'est-ce qui serait different si le probleme etait resolu ?' — oriente vers la solution, (3) 'Si tu devais choisir une prochaine etape, ce serait quoi ?' — responsabilise sans decider pour lui. Ces questions conduisent la personne a trouver sa propre reponse — bien plus puissant que de la donner."}
  ],
  ["questions", "questionnement", "coaching", "Socrate", "exploration"]
))

# ── 5. written / email_writing ───────────────────────────────────────────────
save("communication/written/email_writing.json", ku(
  "email_writing", "written",
  "Ecriture d'emails efficaces",
  "Un email efficace respecte le temps du lecteur : BLUF (Bottom Line Up First), objet precis, une seule action demandee, longueur adaptee a l'enjeu. La plupart des emails professionnels sont trop longs et trop flous.",
  "L'ecriture d'emails efficaces est la capacite a communiquer par email de facon claire, concise et actionnable, en adaptant la structure, le ton et la longueur au contexte et a l'interlocuteur pour maximiser la comprehension et faciliter la reponse ou l'action souhaitee.",
  {
    "email_structure": {
      "objet": "Specifique et actionnable — 'Decision requise : budget Q3' ou 'Info : report de la reunion du 15'",
      "BLUF": "La conclusion ou la demande en premier — le 'pourquoi lire' est immediat",
      "corps": "Contexte minimal necessaire pour comprendre le BLUF",
      "call_to_action": "Une seule action claire avec deadline si applicable",
      "longueur": "< 150 mots pour les emails simples, < 400 pour les complexes"
    },
    "email_anti_patterns": [
      "Objet vague ('Reunion', 'Question') — le lecteur ne sait pas si c'est urgent",
      "Contexte avant la demande — perdre le lecteur avant d'arriver au sujet",
      "Plusieurs demandes dans un email — une seule action par email",
      "Ton ambigu (peut etre lu comme passif-agressif)",
      "Email quand un message Slack ou un appel de 2 min suffirait"
    ],
    "tone_calibration": {
      "formel": "Nouveau contact, hierarchie, client, situation tendue",
      "professionnel": "Collegues, partenaires reguliers",
      "direct": "Equipe proche, manager avec qui on travaille bien"
    }
  },
  [
    {"prompt": "Peux-tu m'aider a ecrire un email pour relancer un client qui n'a pas repondu depuis 2 semaines ?", "answer": "Voici un template : Objet : 'Suite a notre echange du [date] — next step ?'\n\nBonjour [Prenom],\n\nJe reviens vers toi suite a notre conversation du [date] sur [sujet].\n\nQuestion directe : est-ce que [proposition / demo / document] est toujours d'actualite pour toi, ou les priorites ont change ?\n\nPas de pression — j'ai juste besoin de ta reponse pour savoir si je dois planifier la suite ou passer le dossier en attente.\n\nBonne journee, [Signature]\n\nCe format respecte son temps, ne culpabilise pas, et donne une sortie facile — ce qui paradoxalement augmente le taux de reponse."},
    {"prompt": "Comment ecrire un email a mon manager pour signaler un probleme sans avoir l'air de me plaindre ?", "answer": "Structure : (1) Contexte bref ('Suite au projet X'), (2) Fait + impact ('J'ai remarque Y qui cree Z'), (3) Ce que j'ai deja fait ('J'ai essaye A, ca n'a pas suffi'), (4) Ce dont j'ai besoin ('J'aurais besoin de ton aide sur B / de ta decision sur C'). Ne pas commencer par l'emotion — commencer par le fait. Finir par la solution ou la question, pas par la plainte."}
  ],
  ["email", "ecrit professionnel", "BLUF", "communication", "productivite"]
))

# ── 6. written / storytelling ────────────────────────────────────────────────
save("communication/written/storytelling.json", ku(
  "storytelling", "written",
  "Storytelling",
  "Le storytelling est l'art de structurer une communication sous forme narrative pour capter l'attention, creer de l'emotion et ancrer un message dans la memoire. Une histoire bien construite est retenue 22 fois mieux qu'un fait brut.",
  "Le storytelling est la technique de communication qui consiste a presenter une information, une idee ou un argument sous la forme d'un recit structure — avec des personnages, une tension et une resolution — pour exploiter la predisposition du cerveau humain a traiter et retenir les informations narratives.",
  {
    "story_structures": [
      {"structure": "Heros'journey (Campbell)", "arc": "Monde ordinaire → appel → refus → mentor → epreuves → apogee → retour transform", "use": "Pitches, recits de transformation, fondateur story"},
      {"structure": "Problem-Solution-Benefit", "arc": "Il existait un probleme X. Nous avons fait Y. Resultat : Z.", "use": "Cas clients, presentations produit"},
      {"structure": "Avant-Apres-Pont", "arc": "Avant : situation initiale. Apres : monde ideal. Pont : comment y arriver.", "use": "Marketing, pitch de valeur"},
      {"structure": "STAR (Situation-Tache-Action-Resultat)", "arc": "Contexte → role → ce que j'ai fait → resultat mesurable", "use": "Entretiens, leadership stories"}
    ],
    "storytelling_elements": [
      "Un protagoniste auquel on s'identifie",
      "Un probleme/tension (sans tension, pas de recit)",
      "Une transformation visible",
      "Des details sensoriels specifiques (pas 'il faisait froid' mais 'mes mains tremblaient')",
      "Une conclusion qui revient au message cle"
    ],
    "business_storytelling": "Les donnees convainquent l'esprit rationnel ; les histoires convainquent les deux hemispheres. Un pitch qui combine une histoire de client + les chiffres est plus persuasif que les chiffres seuls."
  },
  [
    {"prompt": "Comment rendre ma presentation produit plus captivante ?", "answer": "Commencer par une histoire de client — pas par les features. '(Prenom du client) avait ce probleme specifique. Voici ce qui se passait pour elle. Puis elle a essaye notre solution. Voici ce qui a change.' Ensuite seulement : comment notre produit rend ca possible, avec les chiffres en support. Le changement de sequence (histoire d'abord, features ensuite) transforme une presentation technique en experience emotionnelle."},
    {"prompt": "Comment pitcher mon projet en 2 minutes de facon marquante ?", "answer": "Structure AAP (Avant-Apres-Pont) : (1) Avant : 'Aujourd'hui, [personne cible] a ce probleme tres concret — [description vivante]', (2) Apres : 'Imagine un monde ou [benefice principal] — ca changerait quoi pour elle', (3) Pont : 'C'est exactement ce qu'on a construit avec [nom] : [description minimaliste]. Nous avons deja [preuves : utilisateurs, clients, MRR].' Finir par l'appel a action. La structure prend 90 secondes — les 30 restantes pour les questions."}
  ],
  ["storytelling", "recit", "persuasion", "pitch", "narrative"]
))

# ── 7. nonverbal / body_language ─────────────────────────────────────────────
save("communication/nonverbal/body_language.json", ku(
  "body_language", "nonverbal",
  "Langage corporel",
  "Le langage corporel represente 55-65% de l'impact d'un message en face-a-face. Les signaux non-verbaux (posture, contact visuel, gestes, expressions) transmettent les emotions et les intentions souvent plus fidelement que les mots.",
  "Le langage corporel est l'ensemble des signaux de communication non-verbale transmis par la posture, les gestes, les expressions faciales, le contact visuel, la distance interpersonnelle et le toucher, qui complementent, reinforcement ou contredisent le message verbal.",
  {
    "key_signals": [
      {"signal": "Contact visuel", "meaning_open": "Engagement, confiance, sincerite", "meaning_avoidance": "Malaise, mensonge, soumission ou desinterêt"},
      {"signal": "Posture ouverte", "meaning": "Bras non croises, corps oriente vers l'autre, tete droite — signale ouverture et confiance"},
      {"signal": "Posture fermee", "meaning": "Bras croises, corps oriente en retrait — peut signaler defense, froid ou inconfort"},
      {"signal": "Mirroring", "meaning": "Reproduire inconsciemment la posture de l'autre — signe de rapport et de connexion"},
      {"signal": "Micro-expressions", "meaning": "Expressions faciales involontaires tres breves (< 1/5 seconde) — revelent les emotions vraies avant la regulation"},
      {"signal": "Proxemique", "meaning": "Distance intime (< 45cm), personnelle (45-120cm), sociale (1.2-3.5m), publique (> 3.5m)"}
    ],
    "congruence": "La congruence verbale/non-verbale est le marqueur de l'authenticite. Quand les mots et le corps disent la meme chose, le message est cru. Quand ils divergent, le cerveau de l'interlocuteur croit le corps, pas les mots.",
    "improving_body_language": [
      "Ancrer ses pieds au sol — reduit l'agitation nerveuse",
      "Ralentir les gestes — les gestes lents et deliberes inspirent confiance",
      "Amy Cuddy : power pose de 2 min avant une situation de stress (debattu scientifiquement mais utile comme rituel de preparation)"
    ]
  },
  [
    {"prompt": "Comment lire le langage corporel lors d'une negociation ?", "answer": "Signaux positifs (accord, interet) : inclinaison vers l'avant, sourcils legerement leves, contact visuel maintenu, tete penchee. Signaux negatifs (reticence, fermeture) : recul du corps, bras croises, regards de cote, pincement des levres. Signal ambigu critique : toucher la nuque ou le cou — signale generalement un stress ou une incertitude. Regle : observer les clusters (plusieurs signaux ensemble), pas les signaux isoles — un bras croise seul peut etre juste du froid."},
    {"prompt": "Comment etre plus percutant physiquement lors d'une prise de parole ?", "answer": "Trois leviers haute impact : (1) Pauses deliberees — les orateurs les plus puissants parlent lentement et font des pauses marquees avant les points importants. Contre-intuitif : la pause semble plus longue pour toi que pour l'audience, (2) Ancrage physique — ne pas bouger les pieds au hasard. Bouger avec intention ou rester ancre, (3) Regard individuel — parler a une personne a la fois (3-4 secondes), pas scanner la salle. Cette technique cree l'impression d'une conversation intime meme en grand groupe."}
  ],
  ["langage corporel", "non-verbal", "posture", "expressions", "communication"]
))

# ── 8. nonverbal / vocal_impact ──────────────────────────────────────────────
save("communication/nonverbal/vocal_impact.json", ku(
  "vocal_impact", "nonverbal",
  "Impact vocal — voix et ton",
  "La voix est un instrument. Son debit, son volume, sa hauteur, ses pauses et sa resonance transmettent l'autorite, l'emotion et la conviction. Un contenu excellent delivre avec une voix monotone perd 80% de son impact.",
  "L'impact vocal est la capacite a moduler les caracteristiques vocales (debit, volume, hauteur, resonance, pauses) pour transmettre un message avec l'energie emotionnelle appropriee, renforcer les points cles et maintenir l'attention de l'interlocuteur.",
  {
    "vocal_elements": [
      {"element": "Debit", "impact": "Rapide = energie/urgence. Lent = gravite/autorite. Varier = maintenir l'attention", "default_error": "Debit trop rapide sous le stress — compresse les pauses"},
      {"element": "Volume", "impact": "Fort = assurance/importance. Doux (inattendu) = atteint l'attention paradoxalement", "default_error": "Volume uniforme = monotonie"},
      {"element": "Hauteur (pitch)", "impact": "Grave = autorite/credibilite. Aigu sous stress = perception d'insecurite", "default_error": "Intonation montante sur les affirmations ('uptalk') — semble hesitant"},
      {"element": "Resonance", "impact": "Voix qui vient du thorax = chaleur et autorite vs voix nasale ou de gorge", "practice": "Humming exercises, parler de la poitrine"},
      {"element": "Pauses", "impact": "La pause avant un point cle l'amplifie. La pause apres une question laisse respirer.", "default_error": "Remplir les silences avec 'euh', 'donc', 'voila'"}
    ],
    "filler_words_reduction": "Les 'euh', 'donc', 'voila', 'en fait' viennent de l'inconfort avec le silence. Exercice : lire un texte a haute voix avec interdiction de remplir les pauses — juste s'arreter. Apres 2 semaines, les fillers diminuent significativement."
  },
  [
    {"prompt": "J'ai l'habitude de parler tres vite quand je suis stresse — comment corriger ca ?", "answer": "Deux techniques : (1) Avant : lire un texte lentement a voix haute pendant 5 min avant une prise de parole importante — ca 'calibre' le debit, (2) Pendant : choisir 2-3 mots par phrase sur lesquels tu vas deliberement ralentir et appuyer. Cette selection force a controler le debit globalement sans y penser constamment. Et utiliser les pauses comme respirations — elles sont naturelles pour l'audience meme si elles semblent interminables pour toi."},
    {"prompt": "Comment rendre ma voix plus autoritaire et moins hesitante ?", "answer": "Trois ajustements : (1) Intonation descendante sur les affirmations — finir les phrases en baissant le ton (comme une declaration), pas en montant (qui sonne comme une question), (2) Parler de la poitrine, pas de la gorge — exercice : poser la main sur la cage thoracique et sentir la resonance, (3) Supprimer l'uptalk ('en fait... ?' 'donc... ?' avec ton montant) — remplacer par des affirmations completes et declaratives. Ces trois points transforment la perception de confiance tres rapidement."}
  ],
  ["voix", "debit", "pauses", "autorite", "prise de parole"]
))

# ── 9. influence / persuasion_principles ─────────────────────────────────────
save("communication/influence/persuasion_principles.json", ku(
  "persuasion_principles", "influence",
  "Principes de persuasion (Cialdini)",
  "Les 7 principes de persuasion de Robert Cialdini (reciprocite, engagement, preuve sociale, autorite, sympathie, rarete, unite) expliquent la plupart des mecanismes d'influence — en connaitre les ressorts permet de les utiliser ethiquement et de s'en proteger.",
  "Les principes de persuasion sont les mecanismes psychologiques fondamentaux qui influencent les decisions et comportements humains, identifies et formalises par Robert Cialdini dans 'Influence' (1984) et 'Pre-suasion' (2016), applicable a la vente, la negociation, la communication et le leadership.",
  {
    "cialdini_principles": [
      {"principle": "Reciprocite", "mechanism": "On se sent oblige de rendre ce qu'on a recu", "application": "Offrir avant de demander — contenu gratuit, aide, service", "ethical_use": "Etre sincere dans ce qu'on offre, pas manipulatoire"},
      {"principle": "Engagement et coherence", "mechanism": "On agit coheremment avec ses engagements passes, meme petits", "application": "Faire commencer par un petit oui avant le grand oui", "ethical_use": "Utilisez pour des engagements qu'on croit vraiment benefiques"},
      {"principle": "Preuve sociale", "mechanism": "On se refere a ce que font les autres pour decider", "application": "Temoignages, chiffres d'utilisateurs, logos clients", "ethical_use": "Preuves reelles, pas fabriquees"},
      {"principle": "Autorite", "mechanism": "On fait confiance aux experts et aux figures d'autorite", "application": "Credentials, citations d'experts, expertise visible", "ethical_use": "Autorite legitime dans le domaine"},
      {"principle": "Sympathie", "mechanism": "On dit plus facilement oui aux gens qu'on aime ou qui nous ressemblent", "application": "Points communs, sincere compliment, similarite", "ethical_use": "Connexion authentique, pas feinte"},
      {"principle": "Rarete", "mechanism": "On desire plus ce qui est rare ou limite", "application": "Offres limitees dans le temps ou le nombre", "ethical_use": "Rarete reelle, pas artificiellement creee"},
      {"principle": "Unite (7e principe)", "mechanism": "L'identite partagee cree une persuasion forte ('nous')", "application": "Appartenance a un groupe, identite commune", "ethical_use": "Communautes authentiques"}
    ]
  },
  [
    {"prompt": "Comment utiliser les principes de Cialdini dans ma communication client ?", "answer": "Application concrete par principe : (1) Reciprocite — offrir du contenu de valeur (guide, audit gratuit) avant de proposer l'offre payante, (2) Preuve sociale — mettre en avant les temoignages de clients similaires a votre prospect, (3) Autorite — citer les resultats concrets et les cas clients chiffres, (4) Rarete — etre honnete sur tes disponibilites reelles ('je peux prendre un client de plus ce mois-ci'). L'ethique est cle : chaque principe manipule ou utilise a tort retourne contre toi a long terme."},
    {"prompt": "Comment reconnaitre quand quelqu'un essaie de me manipuler ?", "answer": "Signaux d'alerte : (1) Urgence artificielle ('seulement jusqu'a ce soir') — la vraie rarete ne se crie pas, (2) Flatterie excessive avant une demande — reciprocite pre-chargee, (3) Engagement progressif sur des petites choses pour arriver a une grande demande ('foot-in-the-door'), (4) Autorite sans substance ('les experts disent...' sans citation). Contre-mesure : pause deliberee avant toute decision sous pression. 'Je peux vous repondre demain' est toujours une option legitime."}
  ],
  ["persuasion", "Cialdini", "influence", "reciprocite", "preuve sociale"]
))

# ── 10. influence / negotiation ───────────────────────────────────────────────
save("communication/influence/negotiation.json", ku(
  "negotiation", "influence",
  "Negociation",
  "La negociation efficace cherche les solutions a somme positive — pas la victoire sur l'autre. La methode Harvard (interets vs positions) et les techniques du FBI (Chris Voss) offrent des frameworks complementaires pour des contextes differents.",
  "La negociation est le processus de communication par lequel deux parties ayant des interets partiellement divergents cherchent a atteindre un accord mutuellement satisfaisant, en explorant les besoins sous-jacents plutot que les positions declarees.",
  {
    "harvard_method": {
      "source": "Fisher & Ury, Getting to Yes (1981)",
      "principles": [
        "Separer les personnes du probleme",
        "Se concentrer sur les interets, pas les positions",
        "Inventer des options pour un gain mutuel",
        "Insister sur l'utilisation de criteres objectifs"
      ],
      "positions_vs_interests": "Position : 'Je veux 50k€ de salaire.' Interet sous-jacent : 'J'ai besoin de me sentir valorise et de couvrir mes charges.' L'interet ouvre plus de solutions (avantages, flexibilite, titre) que la position n'en laisse."
    },
    "chris_voss_techniques": {
      "source": "Chris Voss, Never Split the Difference (2016)",
      "tactical_empathy": "Comprendre et verbaliser le point de vue de l'autre AVANT de presenter le sien",
      "mirroring": "Repeter les 2-3 derniers mots — encourage l'autre a continuer et revele ses priorites",
      "labeling": "'Ca ressemble a... / On dirait que tu te preoccupes de...' — nomme l'emotion de l'autre",
      "calibrated_questions": "'Comment je suis cense faire ca ?' ou 'Qu'est-ce qui vous manque pour avancer ?' — questions en Comment/Quoi qui impliquent l'autre dans la solution",
      "no_as_start": "Le non n'est pas une fin — c'est un debut. 'Qu'est-ce qui m'empeche de dire non ?' revele ce qui manque."
    }
  },
  [
    {"prompt": "Comment negocier mon salaire sans me sentir mal a l'aise ?", "answer": "Reframe : tu ne mendies pas, tu negocies la valeur que tu apportes. Preparation : (1) Ancre — donner le premier chiffre (celui qui donne le premier ancre l'espace de negociation), citer le haut de la fourchette du marche, (2) Justification — 3 arguments factuels (pas emotionnels) qui justifient le chiffre, (3) Silence — apres avoir annonce ton chiffre, ne pas le remplir. Le premier qui parle souvent cede. Et si la reponse est non : 'Qu'est-ce qui devrait se passer pour que ce soit possible ?' — transforme le refus en roadmap."},
    {"prompt": "Comment negocier un prix avec un fournisseur difficile ?", "answer": "Sequence Voss : (1) Miroir — repeter les termes qu'il utilise pour le faire developper, (2) Label — 'Ca ressemble a une contrainte importante pour vous sur le delai', (3) Question calibree — 'Comment vous envisagez qu'on puisse trouver une solution qui marche pour les deux ?'. Cette sequence evite le jeu de positions et invite l'autre a participer a la solution. Alternative : avoir une BATNA (Best Alternative To a Negotiated Agreement) solide — savoir ce qu'on fait si la negociation echoue change le rapport de force."}
  ],
  ["negociation", "Harvard", "Chris Voss", "BATNA", "interets vs positions"]
))

# ── 11. influence / public_speaking ──────────────────────────────────────────
save("communication/influence/public_speaking.json", ku(
  "public_speaking", "influence",
  "Prise de parole en public",
  "La prise de parole en public est une competence acquise, pas un talent inne. Elle se structure (contenu), se repete (delivrance) et se gere emotionnellement (trac). Les meilleurs orateurs sont ceux qui ont pratique le plus, pas les plus doues.",
  "La prise de parole en public est la capacite a delivrer un message de facon claire, engagante et memorable devant une audience, en combinant une structure de contenu solide, une presence physique maitrisee et une gestion appropriee du stress.",
  {
    "preparation_framework": [
      "Definir l'objectif unique ('A la fin, mon audience doit penser/faire/ressentir X')",
      "Structurer en 3 parties max (plus = perte d'attention)",
      "Ouvrir avec un hook fort (question, statistique surprenante, histoire, silence)",
      "Un message cle par section — pas de slideshow de bullets",
      "Fermer avec le rappel du message et l'appel a l'action"
    ],
    "managing_anxiety": [
      "Le trac est physiologiquement identique a l'excitation — le reframer ('je suis excite' pas 'je suis stresse')",
      "Preparer 10x plus que necessaire — la sur-preparation reduit l'incertitude",
      "Arriver tot et apprivoiser l'espace physiquement",
      "Respiration physiologique 2 min avant (inspire-inspire-expire longue)",
      "Commencer par regarder une personne bienveillante dans l'audience"
    ],
    "common_mistakes": [
      "Lire ses slides — l'audience peut lire plus vite que toi",
      "S'excuser d'etre la ('je ne suis pas un expert...')",
      "Trop d'information — une idee forte vaut mieux que 10 mediocres",
      "Ignorer l'audience — l'oratoire est un dialogue, meme sans questions"
    ]
  },
  [
    {"prompt": "Comment surmonter le trac avant une presentation importante ?", "answer": "Protocol en 3 temps : (1) Preparation — repeter a voix haute (pas juste relire), idealement en conditions reelles (debout, dans l'espace si possible), (2) Veille — pas d'alcool, sommeil suffisant, repas leger avant, (3) J-day : arriver 15 min en avance pour apprivoiser l'espace, 2 min de respiration physiologique dans un endroit prive, regarder les premiers mots de ton intro ecrits sur une carte si tu peux bloquer. Le trac ne disparait pas — il se transforme en energie si on le laisse sans le combattre."},
    {"prompt": "Comment structurer un discours de 10 minutes pour qu'il reste en tete ?", "answer": "Regel de 3 : (1) Une seule idee principale, (2) Trois points pour la soutenir, (3) Chaque point illustre par une histoire ou un exemple — pas de bullets. Structure : Hook (30s) → Annonce de l'idee principale (30s) → Point 1 + exemple (2.5 min) → Point 2 + exemple (2.5 min) → Point 3 + exemple (2.5 min) → Rappel de l'idee principale + call to action (30s). Le tout = 9 min, 1 min de marge. Ce que l'audience retient : l'histoire, pas le bullet."}
  ],
  ["prise de parole", "presentation", "trac", "orateur", "discours"]
))

# ── 12. influence / cross_cultural_communication ─────────────────────────────
save("communication/influence/cross_cultural_communication.json", ku(
  "cross_cultural_communication", "influence",
  "Communication interculturelle",
  "La communication interculturelle reconnait que les codes de communication (directe/indirecte, hierarchie, rapport au temps, emotions) varient selon les cultures. Ignorer ces differences cree des malentendus involontaires; les connaitre ouvre des relations plus riches.",
  "La communication interculturelle est la capacite a communiquer efficacement avec des personnes issues de cultures differentes en reconnaissant et adaptant sa communication aux differences culturelles de fond en ce qui concerne la directivite, la hierarchie, le rapport au temps, l'expressivite emotionnelle et les codes de politesse.",
  {
    "cultural_dimensions": [
      {"dimension": "Communication directe / indirecte", "examples": {"direct": "Pays-Bas, Allemagne, Israël", "indirect": "Japon, Chine, monde arabe, France (plus indirect qu'on ne le pense)"}},
      {"dimension": "Distance hierarchique", "examples": {"haute": "Asie du Sud-Est, Afrique, Amerique latine", "faible": "Scandinavie, Australie, Pays-Bas"}},
      {"dimension": "Rapport au temps (monochronique / polychronique)", "examples": {"mono": "Suisse, Allemagne, USA — un sujet a la fois, ponctualite cruciale", "poly": "Pays mediterraneens, Inde, Mexique — multi-taches, ponctualite flexible"}},
      {"dimension": "Individualism / Collectivisme", "examples": {"individuel": "USA, Royaume-Uni", "collectif": "Japon, Chine, Coree"}}
    ],
    "erin_meyer_culture_map": "Erin Meyer ('The Culture Map') cartographie 8 dimensions culturelles des affaires — outil de reference pour les equipes internationales.",
    "practical_tips": [
      "Ne pas supposer que l'absence de 'non' = oui (cultures indirectes disent non autrement)",
      "Valider la comprehension sans demander 'tu as compris ?' (perdant pour l'interlocuteur)",
      "Adapter le niveau de formalite — observation d'abord, ajustement ensuite",
      "Le silence a des significations tres differentes (reflexion, gene, accord implicite)"
    ]
  },
  [
    {"prompt": "Comment adapter ma communication pour des clients japonais ?", "answer": "Cinq adaptations cles : (1) La patience — les decisions sont collectives (nemawashi) et prennent du temps, (2) Le silence est positif — ne pas le remplir, (3) 'Peut-etre' ou 'c'est difficile' signifie souvent non — ne pas insister, (4) La hierarchie est visible — s'adresser en premier aux personnes les plus seniores, (5) L'echange de cartes de visite (meishi) est un rituel : recevoir a deux mains, lire avant de poser devant soi. Eviter les confrontations directes — les desaccords se traitent en coulisses."},
    {"prompt": "Comment eviter les malentendus avec une equipe americaine depuis la France ?", "answer": "Trois ajustements : (1) Directivite — les Americains sont plus directs que les Francais dans les reunions professionnelles. 'I disagree' est acceptable; la critique implicite ou le silence ne l'est pas, (2) Positivite visible — commencer par ce qui fonctionne avant de critiquer ('great start, here's how we could improve...'), (3) Follow-up ecrit — apres chaque reunion, un email de recap avec les decisions et les prochaines etapes. La culture americaine valorise l'action visible — l'ambiguite est perque comme de l'inefficacite."}
  ],
  ["interculturel", "Erin Meyer", "culture", "adaptation", "international"]
))

# ── 13. digital / social_media_communication ─────────────────────────────────
save("communication/digital/social_media_communication.json", ku(
  "social_media_communication", "digital",
  "Communication sur les reseaux sociaux",
  "La communication sur les reseaux sociaux suit des codes specifiques a chaque plateforme (LinkedIn, X/Twitter, Instagram). L'authenticite, la regularite et la valeur apportee surpassent la production de contenu parfait.",
  "La communication sur les reseaux sociaux est l'ensemble des pratiques d'expression, de partage et d'engagement en ligne qui permettent de construire une presence, une reputation et une communaute sur les plateformes numeriques, en adaptant le format, le ton et le rythme aux specificites de chaque reseau.",
  {
    "platform_codes": [
      {"platform": "LinkedIn", "tone": "Professionnel, authentique, story-driven", "format": "Posts texte longs avec hook fort, eventuellement carrousels", "algorithm": "Engagement rapide dans la 1ere heure cle — commenter sur d'autres posts avant de publier"},
      {"platform": "X / Twitter", "tone": "Direct, opinionated, informatif, avec humour possible", "format": "Threads pour le fond, tweets uniques pour la viralite", "algorithm": "Engagement et repost sont plus importants que les likes"},
      {"platform": "Instagram", "tone": "Visuel, aspirationnel, lifestyle ou expertise", "format": "Carousels pour la retention, Reels pour la decouverte", "algorithm": "Le temps de visionnage est le signal le plus fort"}
    ],
    "content_pillars": "Definir 3-4 themes de contenu sur lesquels on est crible — ca cree la coherence et l'expertise percue. Ex : un consultant IA pourrait avoir comme piliers 'cas concrets IA', 'outils pratiques', 'reflexions ethiques', 'coulisses du metier'.",
    "engagement_authentique": [
      "Repondre a chaque commentaire dans les 2h (surtout sur LinkedIn)",
      "Commenter avec substance sur les posts d'autres (pas juste des emojis)",
      "Partager les echecs autant que les succes — l'authenticite surpasse la perfection"
    ]
  },
  [
    {"prompt": "Comment commencer a construire ma presence sur LinkedIn sans avoir d'audience ?", "answer": "Phase 1 (semaines 1-4) : commenter avec valeur sur 10 posts par jour dans ton secteur — avant de publier. Ca construit la visibilite et un reseau initial. Phase 2 : publier 2-3 fois par semaine avec des posts authentiques (ce que tu as appris, un cas concret, une opinion). Phase 3 : analyser ce qui a le plus d'engagement et doubler dessus. La progression est lente au debut (quelques centaines de vues) puis exponentielle. La regularite sur 3 mois bat le post viral ponctuel."},
    {"prompt": "Quel type de contenu fonctionne le mieux sur LinkedIn en 2025 ?", "answer": "Ce qui performe : (1) Histoires personnelles authentiques avec une lecon (les 'J'ai fait X, voici ce que j'ai appris'), (2) Points de vue contre-intuitifs ou opinions assumees, (3) Cas concrets avec chiffres ('comment j'ai aide ce client a X en Y semaines'), (4) Carrousels pedagogiques sur un sujet de ton expertise. Ce qui ne performe plus : les posts generiques sur le 'mindset', les partages de citations sans valeur ajoutee, la perfection de production sans authenticite."}
  ],
  ["LinkedIn", "reseaux sociaux", "contenu", "personal branding", "audience"]
))

# ── 14. digital / remote_communication ───────────────────────────────────────
save("communication/digital/remote_communication.json", ku(
  "remote_communication", "digital",
  "Communication a distance (remote)",
  "La communication a distance amplifie les malentendus et reduit la richesse contextuelle. Des pratiques deliberees (documentation, asynchrone d'abord, video strategique) compensent ce que la communication en personne offre naturellement.",
  "La communication a distance est l'ensemble des pratiques et outils permettant de maintenir une collaboration efficace et des relations de confiance dans des equipes distribuees, en compensant deliberement la perte du non-verbal et du contexte informel propres a la cohabitation physique.",
  {
    "async_first_principles": [
      "Privilegier l'asynchrone par defaut — une reunion ne doit pas remplacer un document bien ecrit",
      "Documenter les decisions et le contexte (notion, confluence) — la memoire institutionnelle ne passe pas par l'oral",
      "Messages clairs et auto-suffisants — l'autre ne peut pas demander 'tu veux dire quoi ?' en temps reel",
      "Definir les plages de disponibilite et les respecter — eviter la 'always-on' culture"
    ],
    "video_when": [
      "Feedback sensible ou converstion difficile — jamais par email ou texte",
      "Onboarding d'un nouveau membre",
      "Session de brainstorm ou de decision complexe",
      "Reconnexion relationnelle (monthly team coffee)"
    ],
    "written_clarity_remote": [
      "Commencer chaque message par l'action requise (pas le contexte)",
      "Specifier les delais explicitement ('d'ici vendredi 18h' pas 'rapidement')",
      "Eviter le sarcasme et l'ironie — sans le ton vocal, c'est lu au premier degre",
      "Emoji strategique pour signaler le registre (💡 = idee, ✅ = valide, 🚨 = urgent)"
    ]
  },
  [
    {"prompt": "Comment maintenir la cohesion d'equipe a distance ?", "answer": "Trois niveaux : (1) Rituels reguliers — weekly standup (15 min max), monthly team retrospective, quarterly off-site si possible. Les rituels creent la previsibilite et la connexion, (2) Reconnaissance visible — feliciter publiquement dans les canaux d'equipe, (3) Espaces informels — canal Slack '#cafe' sans agenda, virtual coffee pairs mensuels (random pairings automatiques). La relation en remote se construit deliberement — elle ne se cree pas par accident comme au bureau."},
    {"prompt": "Comment eviter les malentendus dans les echanges ecrits avec mon equipe ?", "answer": "Cinq regles : (1) Relire avant d'envoyer avec la question 'comment cette personne peut-elle lire ca differemment ?', (2) Pour les sujets sensibles : video ou appel, jamais texte, (3) Nommer l'intention ('je te partage ca pour info / pour decision / pour feedback'), (4) Confirmer la comprehension sur les decisions importantes ('tu peux me confirmer ta comprenhenison de l'action attendue ?'), (5) Donner le benefice du doute — beaucoup de malentendus viennent d'une lecture trop rapide, pas d'une mauvaise intention."}
  ],
  ["remote", "asynchrone", "equipe distribuee", "communication", "teletravail"]
))

# ── 15. verbal / feedback_culture ────────────────────────────────────────────
save("communication/verbal/feedback_culture.json", ku(
  "feedback_culture", "verbal",
  "Culture du feedback",
  "Le feedback est le carburant de l'amelioration individuelle et collective. Une culture du feedback efficace le rend regulier, specifique, bidirectionnel et ancre dans un contexte de confiance et d'intention positive.",
  "La culture du feedback est l'ensemble des pratiques, normes et structures qui rendent le feedback — positif et constructif — fluide, regulier et sans menace dans une organisation ou une relation, en faisant de la retroaction un outil de croissance plutot qu'un evenement anxiogene.",
  {
    "feedback_models": [
      {"model": "SBI (Situation-Behavior-Impact)", "structure": "Situation (quand ?), Comportement (qu'est-ce que j'ai observe ?), Impact (qu'est-ce que ca a produit ?)", "use": "Feedback constructif factuel"},
      {"model": "COIN (Contexte-Observation-Impact-Next)", "structure": "Contexte, observation, impact, prochaine etape", "use": "Feedback en management"},
      {"model": "Radical Candor (Kim Scott)", "axes": ["Care Personally (se soucier sincèrement)", "Challenge Directly (challenger directement)"], "quadrants": ["Caring challenge = Radical Candor (ideal)", "No care + challenge = Obnoxious Aggression", "Care + no challenge = Ruinous Empathy", "No care + no challenge = Manipulative Insincerity"]}
    ],
    "receiving_feedback": [
      "Ecouter completement avant de repondre",
      "Ne pas se defendre immediatement — prendre le temps de distinguer ce qui est juste de ce qui ne l'est pas",
      "Remercier — meme si le feedback est difficile, c'est un cadeau d'information",
      "Clarifier ce qu'on n'a pas compris avant de decider quoi faire"
    ]
  },
  [
    {"prompt": "Comment instaurer une culture du feedback dans mon equipe qui n'en a pas l'habitude ?", "answer": "Sequence : (1) Commencer par toi — donner du feedback regulier et specifique a tes collaborateurs (pas seulement en fin d'annee), (2) Demander du feedback explicitement ('qu'est-ce que je peux ameliorer dans ma facon de te manager ?'), (3) Ritualiser — retro mensuelle avec une question 'qu'est-ce qu'on pourrait faire mieux ?', (4) Reagir positivement quand du feedback difficile est donne — si tu te fermes, personne ne recommencera. La culture se cree par les comportements du leader, pas par les politiques RH."},
    {"prompt": "Comment reagir quand je recois un feedback tres dur que je trouve injuste ?", "answer": "En 3 temps : (1) Dans le moment — ecouter sans se defendre ('merci de me dire ca, j'ai besoin de temps pour y reflEchir'), (2) Dans les heures suivantes — distinguer la forme (etait-ce dit correctement ?) du fond (y a-t-il une part de verite meme mal exprimee ?), (3) En retour — partager ta perspective apres reflexion ('j'ai reflechi a ce que tu m'as dit. Sur X, je pense que tu as raison. Sur Y, voici ma perspective.' La maturite dans la reception du feedback est une competence distincte de la reception du feedback)."}
  ],
  ["feedback", "Radical Candor", "SBI", "culture", "management"]
))

# ── 16. verbal / meeting_facilitation ────────────────────────────────────────
save("communication/verbal/meeting_facilitation.json", ku(
  "meeting_facilitation", "verbal",
  "Facilitation de reunions",
  "Une reunion efficace a un objectif clair, un facilitateur, un agenda et produit des decisions documentees. La plupart des reunions echouent sur l'un de ces quatre points. Faciliter c'est servir l'objectif de groupe, pas imposer sa vision.",
  "La facilitation de reunions est la capacite a creer les conditions d'une conversation productive en groupe, en clarifiant l'objectif, structurant le temps, impliquant tous les participants et en conduisant vers des decisions ou des sorties claires.",
  {
    "meeting_types": [
      {"type": "Information (update)", "purpose": "Partager, pas decider", "alternative": "Remplacer par un document asynchrone dans 80% des cas"},
      {"type": "Alignment", "purpose": "S'assurer que tout le monde comprend la meme chose", "best_format": "Court (15-30 min), agenda pre-envoye"},
      {"type": "Decision", "purpose": "Decider collectivement ou consulter avant que le decideur tranche", "best_format": "Preparation des options en amont, decision documentee"},
      {"type": "Brainstorm", "purpose": "Generer des idees en groupe", "best_format": "Silent brainstorm d'abord, partage ensuite (evite le groupthink)"},
      {"type": "Retrospective", "purpose": "Apprendre et ameliorer", "best_format": "Structure (Start-Stop-Continue ou Mad-Sad-Glad)"}
    ],
    "facilitation_techniques": [
      "1-2-4-All : reflechir seul (1 min), en duo (2 min), en quatuor (4 min), partage (tout le monde) — maximise la participation",
      "Dot voting : chaque participant a X votes pour prioriser des options",
      "Silence delibere : poser une question et laisser 60s de silence avant d'accepter les reponses (casse le reflexe des personnes qui parlent en premier)",
      "Timeboxing : chaque point de l'agenda a un temps explicite — le facilitateur est gardien du temps"
    ]
  },
  [
    {"prompt": "Comment rendre mes reunions d'equipe moins ennuyeuses et plus productives ?", "answer": "Checklist en 4 points : (1) Objectif sur l'invitation ('Cette reunion vise a [decider X] / [aligner sur Y]') — si tu ne peux pas le formuler, annule la reunion, (2) Agenda envoye 24h avant avec le temps par point, (3) Silent brainstorm pour les idees — personne ne parle pendant les 5 premieres minutes, tout le monde ecrit, puis partage. Ca evite que les voix fortes dominent, (4) Recap de decisions en fin de reunion ('on a decide X, Y fait Z avant vendredi'). Ces 4 elements transforment la plupart des reunions."},
    {"prompt": "Comment gerer une personne qui monopolise la parole en reunion ?", "answer": "Techniques de facilitation non confrontationnelles : (1) Intervention de temps : 'Merci [Prenom], pour rester dans le timing je vais donner la parole a quelqu'un d'autre sur ce point.' (2) Round robin force : 'Je voudrais entendre l'opinion de chacun sur ce point, on commence par [Prenom silencieux].' (3) Parking lot : 'C'est un point important que je mets dans le parking lot pour qu'on puisse y revenir si le temps le permet.' Ces interventions preservent la relation tout en redistribuant la parole."}
  ],
  ["reunions", "facilitation", "agenda", "decision", "management"]
))

# ── 17. written / synthesis_writing ──────────────────────────────────────────
save("communication/written/synthesis_writing.json", ku(
  "synthesis_writing", "written",
  "Ecriture de syntheses",
  "Une bonne synthese capture l'essentiel d'un corpus d'information en preservant la structure logique et les nuances, sans reproduction mot-a-mot. Elle necessite de comprendre avant d'ecrire — paraphraser sans comprendre produit de la longueur sans valeur.",
  "L'ecriture de syntheses est la competence qui consiste a condenser et reorganiser des informations multiples et complexes en un document clair, structure et autonome, qui preserve l'essentiel du sens tout en etant significativement plus court que les sources originales.",
  {
    "synthesis_process": [
      "1. Lire les sources en totalite avant d'ecrire quoi que ce soit",
      "2. Identifier les idees principales et les points de convergence/divergence",
      "3. Construire un plan de la synthese (themes, pas sources)",
      "4. Ecrire la synthese sans avoir les sources sous les yeux (force la paraphrase reelle)",
      "5. Verifier avec les sources : rien de manque, rien de deforme"
    ],
    "structure_types": [
      {"type": "Thematique", "description": "Organiser par themes transversaux — ideal quand les sources traitent le meme sujet sous differents angles"},
      {"type": "Dialectique", "description": "Thesis, antithesis, synthesis — ideal pour des sujets controverses"},
      {"type": "Chronologique", "description": "Evolution temporelle d'un sujet"},
      {"type": "Probleme-solution", "description": "Identifier le probleme commun aux sources, puis les solutions proposees"}
    ],
    "pitfalls": [
      "Le copier-coller devalue : citer sans paraphraser",
      "La juxtaposition : 'Auteur A dit X. Auteur B dit Y.' sans lien analytique",
      "L'exhaustivite : vouloir tout inclure — la synthese choisit et hiErarchise",
      "L'opinion camoufeee : introduire son point de vue sans le signaler"
    ]
  },
  [
    {"prompt": "Comment synthEtiser 5 articles de recherche en 2 pages ?", "answer": "Methode : (1) Lire les 5 articles et surligner les 3 idees principales de chacun, (2) Cartographier les convergences ('4 articles sur 5 disent que...') et les divergences ('sur le point X, les auteurs se divisent entre...'), (3) Construire le plan autour des themes emergents, pas des articles, (4) Ecrire chaque section en paraphrasant — jamais de copier-coller. La synthese finale dit 'ce que la litterature sait sur ce sujet' et 'ce qui est encore debattu' — pas 'ce que chaque auteur a dit'."},
    {"prompt": "Peux-tu synthetiser nos echanges et le travail fait aujourd'hui ?", "answer": "Oui — c'est un des usages directs d'ALFRED. En fin de session de travail, je peux produire un recap structure : decisions prises, actions identifiees, questions ouvertes, et contexte a retenir pour la prochaine session. Tu peux aussi me donner un document ou un ensemble d'emails et je fournis une synthese thematique. Dis-moi le niveau de detail et le format souhaite."}
  ],
  ["synthese", "ecriture", "paraphrase", "recherche", "structure"]
))

# ── 18. written / professional_writing ───────────────────────────────────────
save("communication/written/professional_writing.json", ku(
  "professional_writing", "written",
  "Ecriture professionnelle",
  "L'ecriture professionnelle vise la clarte, la concision et l'impact. Elle utilise la structure pyramidale (conclusion d'abord), un vocabulaire precis et une longueur adaptee a l'enjeu. La bonne ecriture est une marque de respect du temps du lecteur.",
  "L'ecriture professionnelle est la production de documents ecrits (emails, rapports, propositions, memos) dans un contexte professionnel, en visant la clarte maximale, la concision et la lisibilite tout en adaptant le registre, la structure et le niveau de detail a l'audience et a l'objectif.",
  {
    "pyramid_principle": {
      "source": "Barbara Minto, The Minto Pyramid Principle",
      "structure": "Reponse → Argumentation → Developpement (du plus important au moins important)",
      "application": "Commencer par la conclusion (ce que le lecteur a besoin de savoir), puis les 3 arguments principaux, puis les details. L'inverse de la pensee naturelle mais optimal pour le lecteur."
    },
    "clarity_techniques": [
      "Une idee par phrase",
      "Verbes actifs ('nous avons decide' pas 'une decision a ete prise')",
      "Vocabulaire precis et simple — eviter le jargon quand un mot simple existe",
      "Phrases courtes (< 20 mots) pour les points importants",
      "Paragraphes courts (3-5 phrases max)"
    ],
    "document_types": [
      {"type": "Rapport executif", "format": "1 page max avec resume, conclusions et recommandations en haut"},
      {"type": "Proposition commerciale", "format": "Probleme client → notre solution → benefices → preuves → next steps"},
      {"type": "Note de decision", "format": "Contexte → options → recommandation → implications"},
      {"type": "Compte rendu de reunion", "format": "Decisions → actions (qui fait quoi avant quand) → questions ouvertes"}
    ]
  },
  [
    {"prompt": "Comment ecrire un rapport qui sera vraiment lu par le management ?", "answer": "La regle d'or : tout ce que le management a besoin de savoir tient sur la premiere page. Structure : (1) Executive summary (3-5 bullets : contexte, conclusions, recommandations), (2) Corps du rapport pour ceux qui veulent le detail. Mise en forme : titre de chaque section qui est une assertion ('Les resultats Q2 depassent les objectifs de 15%' pas juste 'Resultats Q2'). Longueur : retrancher 30% de ce qu'on a ecrit. Un rapport de 4 pages lu est plus utile qu'un rapport de 20 pages qui s'entasse."},
    {"prompt": "Comment ameliorer la clarte de mon ecriture professionnelle ?", "answer": "Test de lisibilite : apres avoir ecrit, relire en se demandant 'est-ce que quelqu'un qui ne connait pas le sujet comprendrait en une lecture ?' Quatre corrections les plus impactantes : (1) Supprimer les doublets ('en raison du fait que' → 'parce que'), (2) Remplacer les nominalisations par des verbes ('la prise de decision' → 'decider'), (3) Couper les phrases de plus de 30 mots en deux, (4) Verifier que chaque paragraphe commence par sa phrase cle — le lecteur presse ne lit que les premiers mots de chaque paragraphe."}
  ],
  ["ecriture", "rapport", "clarte", "Minto", "professionnel"]
))

# ── 19. verbal / conflict_resolution ─────────────────────────────────────────
save("communication/verbal/conflict_resolution.json", ku(
  "conflict_resolution", "verbal",
  "Resolution de conflits",
  "Le conflit bien gere est une opportunite d'approfondissement relationnel et d'innovation. Mal gere, il degrade la confiance et la performance. Les techniques de resolution (NVC, mediation, confrontation directe) s'adaptent selon la nature et l'intensite du conflit.",
  "La resolution de conflits est l'ensemble des processus et techniques permettant de transformer un desaccord ou une tension interpersonnelle en solution satisfaisante pour toutes les parties, en travaillant sur les besoins sous-jacents plutot que les positions declarees et en preservant la relation.",
  {
    "conflict_levels": [
      {"level": 1, "name": "Desaccord sur les faits", "resolution": "Clarification et information — souvent resolve par une conversation directe"},
      {"level": 2, "name": "Desaccord sur les methodes", "resolution": "Exploration des criteres de decision, compromis ou delegation du choix"},
      {"level": 3, "name": "Desaccord sur les valeurs", "resolution": "Le plus difficile — reconnaissance des differences, accord sur un 'meta-accord' de coexistence"},
      {"level": 4, "name": "Conflit de personnes", "resolution": "Mediation tierce, separation si possible"}
    ],
    "nvc_framework": {
      "source": "Marshall Rosenberg, Communication Non-Violente",
      "steps": [
        "Observation (faits, pas jugements) : 'Quand j'entends / vois...'",
        "Sentiment : '...je me sens...'",
        "Besoin : '...parce que j'ai besoin de...'",
        "Demande : '...pourrais-tu...?'"
      ],
      "key_insight": "Distinguer les besoins universels (appartenance, autonomie, securite, respect) des strategies pour y repondre — le conflit est sur les strategies, rarement sur les besoins"
    },
    "de_escalation_steps": [
      "Baisser le ton et ralentir — l'escalade suit l'autre si on ne la suit pas",
      "Nommer l'emotion ('je vois que tu es en colere — qu'est-ce qui se passe ?')",
      "Pause si l'intensite est trop haute ('revenons-y dans 30 minutes')",
      "Chercher les points de commun avant les desaccords"
    ]
  },
  [
    {"prompt": "Comment gerer un conflit avec un collaborateur sans aggraver les choses ?", "answer": "Sequence : (1) Choisir le bon moment — ni a chaud, ni en public, (2) Commencer par l'observation factuelle sans jugement ('J'ai remarque que depuis X, Y s'est passe'), (3) Partager l'impact sans accuser ('Ca m'a affecte parce que...'), (4) Ecouter sa perspective completement avant de repondre, (5) Chercher ensemble une solution ('Comment on peut faire pour que ca fonctionne mieux ?'). Le piege le plus frequent : commencer par l'accusation ('tu fais toujours...') — ca declenche la defense et ferme le dialogue."},
    {"prompt": "Deux membres de mon equipe sont en conflit — comment intervenir en tant que manager ?", "answer": "Mediation en 3 etapes : (1) Individuel d'abord — rencontrer chacun separement pour comprendre sa perspective sans l'autre. Ecouter sans prendre parti, (2) Session commune — faciliter l'echange avec regles claires : parler de soi (pas de l'autre), faits (pas interpretations), une personne parle a la fois, (3) Accord sur les prochaines etapes — qu'est-ce que chacun s'engage a faire differemment ? Quand veriifie-t-on ? Ne pas forcer une reconciliation artificielle — viser un accord de travail fonctionnel."}
  ],
  ["conflit", "NVC", "mediation", "resolution", "management"]
))

# ── 20. influence / trust_building ────────────────────────────────────────────
save("communication/influence/trust_building.json", ku(
  "trust_building", "influence",
  "Construction de la confiance",
  "La confiance se construit par la coherence (faire ce qu'on dit), la competence (etre capable), la bienveillance (les intentions perçues) et la vulnerabilite (oser montrer ses limites). Elle se gagne lentement et se perd vite.",
  "La construction de la confiance est le processus delibere d'etablissement d'une relation dans laquelle les parties ont la certitude que l'autre est fiable, competent, bienveillant et integre — permettant une collaboration plus ouverte, plus creative et plus productive.",
  {
    "trust_equation": {
      "source": "Maister, Green & Galford, The Trusted Advisor",
      "formula": "Confiance = (Credibilite + Fiabilite + Intimite) / Auto-orientation",
      "credibility": "Est-ce que cette personne sait de quoi elle parle ?",
      "reliability": "Est-ce qu'elle fait ce qu'elle dit ?",
      "intimacy": "Est-ce que je me sens en securite pour etre vulnerables avec elle ?",
      "self_orientation": "Cherche-t-elle son propre interet ou le mien ? (denominateur — plus c'est eleve, moins la confiance est haute)"
    },
    "trust_building_behaviours": [
      "Tenir ses engagements, meme les petits — la fiabilite s'accumule dans les details",
      "Reconnaitre ses erreurs explicitement et sans minimisation",
      "Partager des informations difficiles plutot que de les taire",
      "Etre coherent public/prive — ne pas dire une chose en 1-1 et une autre en groupe",
      "Montrer de l'interet genuiin pour l'autre (ses projets, ses defis) au-dela du travail"
    ],
    "vulnerability_and_trust": "Brene Brown : la vulnerabilite est le berceau de la connexion. Montrer ses doutes, ses erreurs et ses zones d'apprentissage (de facon adaptee au contexte) renforce la confiance — ca signale une relation reelle plutot qu'une facade."
  },
  [
    {"prompt": "Comment rebatir la confiance avec un collegue apres un desaccord difficile ?", "answer": "Quatre etapes : (1) Nommer ce qui s'est passe directement ('Notre echange de la semaine derniere etait tendu — j'aimerais qu'on en parle'), (2) Reconnaitre ta part sans minimiser ni maximiser ('Sur X, j'aurais pu faire mieux'), (3) Ecouter sa perspective sans se defendre, (4) Proposer un accord concret pour la suite ('Comment on fait pour que ca se passe mieux la prochaine fois ?'). La confiance ne se rebatit pas par le temps seul — elle se rebatit par des actes de courage conversationnel."},
    {"prompt": "Comment inspirer rapidement confiance a un nouveau client ?", "answer": "Les 5 premiers signaux qui creent la confiance rapide : (1) Arriver prepare — avoir fait ses devoirs sur le client avant la rencontre, (2) Ecouter plus que parler en premier echange, (3) Admettre ce qu'on ne sait pas ('je ne connais pas ce secteur specifique — laissez-moi investiguer et revenir avec des donnees solides'), (4) Tenir le premier micro-engagement (envoyer ce qu'on a promis, dans le delai promis), (5) Parler des interets du client avant les siens. Le point 3 est contre-intuitif mais tres puissant — l'honnEtetE sur les limites cree plus de confiance que la simulation d'omniscience."}
  ],
  ["confiance", "fiabilite", "credibilite", "relation", "leadership"]
))

print("\n=== Domaine 'communication' : 20 fichiers crees ===")
