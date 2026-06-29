"""
Batch Day 2 — Part 2
  human/seduction_relations/ : 10 fichiers
  human/vie_privee/          : 10 fichiers
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
            "tone": "bienveillant, sans jugement, ancré dans le respect de l'autonomie",
            "structure": ["valider", "informer", "proposer des pistes"],
            "avoid": ["moraliser", "minimiser", "donner des prescriptions non demandées"]
        },
        "tags": tags, "related_knowledge_units": []
    }

# ═══════════════════════════════════════════════════════════════════════════
# HUMAN / SEDUCTION_RELATIONS  (10 fichiers)
# ═══════════════════════════════════════════════════════════════════════════

def kus(file_id, title, summary, core_def, knowledge, examples, tags, priority="high"):
    return ku(file_id, "human", "seduction_relations", title, summary, core_def, knowledge, examples, tags, priority)

save("human/seduction_relations/seduction_bases.json", kus(
    "seduction_bases",
    "Séduction — bases psychologiques de l'attraction",
    "La séduction est un processus de communication et de signalisation sociale. Elle repose sur des bases psychologiques mesurables — attraction, confiance, désir de réciprocité — et peut être comprise et cultivée sans perdre son authenticité.",
    "La séduction désigne l'ensemble des comportements verbaux et non verbaux par lesquels un individu cherche à créer de l'attraction et du désir chez un autre. Elle n'est ni manipulation ni jeu — à son meilleur, elle est une communication authentique d'intérêt et de valeur perçue mutuels.",
    {
        "psychological_bases": [
            {"factor": "Similarité", "mechanism": "On est attiré par ceux qui nous ressemblent (valeurs, humour, centres d'intérêt) — le 'on se ressemble donc on s'entend'", "study": "Byrne (1971) — Attraction paradigm"},
            {"factor": "Proximité", "mechanism": "La simple exposition répétée crée de l'attraction (effet de simple exposition, Zajonc 1968) — le colocataire qui devient ami, puis plus"},
            {"factor": "Réciprocité perçue", "mechanism": "On est attiré par quelqu'un qu'on croit nous trouver attirant — le signal d'intérêt crée l'intérêt en retour"},
            {"factor": "Mystère et découverte progressive", "mechanism": "Le dévoilement graduel maintient l'intérêt — trop visible trop vite réduit la tension"},
            {"factor": "Confiance en soi", "mechanism": "Signal evolutif de valeur — pas arrogance mais aisance dans sa propre peau"}
        ],
        "attraction_signals": {
            "verbal": ["Curiosité sincère pour l'autre (questions ouvertes)", "Humour et légèreté", "Teasing bienveillant", "Vulnérabilité dosée"],
            "non_verbal": ["Contact visuel soutenu mais non fixe", "Sourire sincère (yeux + bouche)", "Orientation corporelle", "Espace personnel respecté puis progressivement réduit"],
            "timing": "L'attraction se construit dans les intervalles et les silences, pas dans le flux continu de communication"
        },
        "common_errors": [
            "Performativité — 'séduire' plutôt qu'être. Se sentir instantanément.",
            "Désespoir apparent — la peur de perdre l'autre crée la pression qui le fait partir",
            "Surexplication — justifier, valider, convaincre. L'attraction ne s'argumente pas.",
            "Négliger l'intérêt réel — technique sans curiosité authentique = vide"
        ]
    },
    [
        {"prompt": "Comment commencer à séduire quelqu'un sans être trop direct ou mal à l'aise ?",
         "answer": "La séduction au naturel commence par la curiosité — s'intéresser genuinement à l'autre plutôt que de 'faire des choses pour séduire'. Questions concrètes : (1) Crée du temps et de la présence — les rencontres régulières dans un cadre naturel (boulot, hobby, ami commun) permettent à l'attraction de croître sans pression, (2) Signale de l'intérêt sans l'étaler — un sourire soutenu, une question qui montre que tu t'es souvenu de quelque chose qu'il/elle a dit la semaine dernière, (3) Crée des occasions légères — proposer quelque chose de court et à faible enjeu (un café, rejoindre un groupe) plutôt que 'le grand soir', (4) Laisse de l'espace — disponibilité 100% 24h/24 n'est pas attrayante. La rareté crée de la valeur."},
        {"prompt": "Comment savoir si quelqu'un est attiré par moi ?",
         "answer": "Signaux verbaux : pose des questions sur ta vie, prolonge les conversations, fait des références à des conversations précédentes (il/elle écoutait), te mentionne à d'autres. Signaux non verbaux : contact visuel soutenu, orientation corporelle vers toi, toucher initié (bras, épaule) même légèrement, sourire sincère (les yeux sourient aussi pas juste la bouche). Signaux comportementaux : trouve des prétextes pour être dans ton espace, répond rapidement aux messages, suggère des continuations ('on devrait faire ça de nouveau'). Aucun signal isolé n'est concluant — c'est l'accumulation et la cohérence qui comptent."}
    ],
    ["séduction", "attraction", "psychologie", "signaux", "confiance", "curiosité"]
))

save("human/seduction_relations/premier_contact.json", kus(
    "premier_contact",
    "Premier contact et première impression — 7 secondes qui comptent",
    "La première impression se forme en 7 à 30 secondes et est très difficile à modifier. Elle repose sur l'apparence, la posture, le ton de voix et la cohérence globale du signal envoyé — bien avant que les mots ne comptent.",
    "Le premier contact désigne le moment initial d'interaction entre deux personnes, durant lequel se forme la première impression. Cette impression, formée en quelques secondes par le système limbique, active des jugements rapides sur la chaleur (bienveillance) et la compétence (capabilité) qui influencent durablement la relation.",
    {
        "first_impression_science": {
            "timeframe": "7 à 30 secondes pour une première impression stable (Ambady & Rosenthal, 1993)",
            "two_dimensions": "Amy Cuddy (2013) : warmth (chaleur, intention) jugée en premier, puis competence (capacité). Pour l'attraction : chaleur > compétence dans les 10 premières secondes.",
            "halo_effect": "Une bonne première impression crée un 'halo' qui colore l'interprétation de tout ce qui suit positivement"
        },
        "key_factors": [
            {"factor": "Apparence globale", "weight": "Élevée en premier contact. Pas beauté objective mais cohérence et soin.", "tip": "Être à l'aise dans ce qu'on porte plutôt que porter quelque chose d'inconfortable"},
            {"factor": "Posture", "weight": "Majeure. Posture ouverte = signale confiance. Posture fermée (bras croisés, regard bas) = signale anxiété ou désintérêt"},
            {"factor": "Sourire", "weight": "Le signal de chaleur le plus fort. Sourire de Duchenne (yeux + bouche) vs sourire social (bouche seulement)"},
            {"factor": "Voix", "weight": "Ton, débit, assurance. La voix grave et posée est perçue comme plus confiante que la voix aiguë et rapide sous stress"},
            {"factor": "Nom et regard", "weight": "Mémoriser et réutiliser le prénom rapidement. Contact visuel lors de la poignée de main ou de l'accroche"}
        ],
        "approach_online": "En contact digital (app de rencontre, réseaux) : la photo représente 90% de la première impression. Puis la première phrase du message — singulière, pertinente et non générique ('salut cc t'as l'air sympa' = poubelle).",
        "recovery": "Une première impression négative peut se modifier mais demande 4-5 interactions positives cohérentes pour s'effacer. Mieux vaut la préparer."
    },
    [
        {"prompt": "Comment faire une bonne première impression lors d'un premier rendez-vous ?",
         "answer": "Priorités par ordre : (1) Arriver à l'heure — signale respect et organisation. En avance = parfait. En retard sans prévenir = première impression négative difficile à effacer, (2) Apparence cohérente — ce qui te ressemble et dans lequel tu te sens bien. L'inconfort dans sa tenue se voit, (3) Posture — debout ou assis, épaules ouvertes, pas de bras croisés, regard direct mais pas fixe, (4) Écoute active réelle les 10 premières minutes — poser des questions sur ce que l'autre vient de dire. La chaleur perçue s'établit par l'intérêt porté, (5) Éteindre ou ranger le téléphone. Visible = signal clair que l'autre est prioritaire."},
        {"prompt": "Comment aborder quelqu'un qu'on ne connaît pas dans un contexte social ?",
         "answer": "La meilleure approche : commentaire sur la situation partagée + question ouverte. Formule : observation pertinente sur le contexte → question qui invite à développer. Exemple : 'C'est la première fois que tu viens à cet événement ?' ou 'Je ne reconnais personne d'autre de l'organisation — tu es du côté [X] ?' plutôt qu'un compliment générique. Ce qui fonctionne : rendre l'autre à l'aise en établissant une connexion contextuelle (vous êtes dans le même endroit pour une raison). Ce qui ne fonctionne pas : compliment physique immédiat d'inconnu (trop intense), approche avec un script visible, rejoindre quelqu'un qui est clairement dans une conversation fermée."}
    ],
    ["première impression", "premier contact", "approche", "posture", "chaleur", "Amy Cuddy"]
))

save("human/seduction_relations/communication_amoureuse.json", kus(
    "communication_amoureuse",
    "Communication amoureuse — dire, écouter, comprendre",
    "La communication dans une relation amoureuse est le premier prédicteur de la satisfaction et de la durabilité du couple selon la recherche de John Gottman. Les couples qui réussissent maintiennent un ratio positif/négatif de 5:1 et savent réparer les ruptures de connexion.",
    "La communication amoureuse désigne l'ensemble des échanges verbaux et non verbaux au sein d'une relation romantique. Elle inclut l'expression des besoins, des émotions et des désirs, la résolution des conflits, la validation et le soutien émotionnel, et les rituels de connexion quotidiens.",
    {
        "gottman_research": {
            "four_horsemen": "Les 4 patterns qui prédisent la rupture (Gottman & Silver) : (1) Critique (attaquer le caractère), (2) Mépris (se sentir supérieur), (3) Défensivité (contre-attaque), (4) Mur de pierre (se fermer complètement)",
            "antidotes": {
                "critique→plainte": "Plainte sur comportement spécifique vs critique de la personne. 'Tu n'as pas fait X' vs 'Tu es négligent'",
                "mépris→admiration": "Cultiver activement l'admiration pour l'autre. Se rappeler ce qu'on apprécie.",
                "défensivité→responsabilité": "Prendre sa part même partielle. 'Tu as raison que j'aurais pu...'",
                "mur_de_pierre→auto_apaisement": "Physio d'abord — se calmer (20 min) avant de reprendre la conversation"
            },
            "positive_ratio": "Ratio 5:1 interactions positives/négatives pour les couples stables. Pas 'toujours gentil' — les conflits sont normaux. Mais le positif doit dominer massivement."
        },
        "needs_expression": {
            "formula": "Observation (non jugée) + Sentiment + Besoin + Demande. 'Quand tu rentres sans prévenir (obs), je me sens inquiète (sentiment), j'ai besoin de savoir si tu seras là pour organiser (besoin), est-ce que tu peux me prévenir ? (demande)'",
            "common_error": "Exprimer le besoin comme une critique de l'autre ('tu ne penses jamais à moi') plutôt que comme une information sur soi"
        },
        "reconnection_rituals": ["Check-in quotidien sincère — 2 min sur comment l'autre se sent vraiment", "Accueil et départ ritualisés — contact physique lors des séparations/retrouvailles", "Rendez-vous intentionnel hebdomadaire — time dédié sans agenda"]
    },
    [
        {"prompt": "Comment exprimer ce que je veux dans ma relation sans déclencher un conflit ?",
         "answer": "Formule en 4 temps : (1) Observation factuelle, non interprétée — 'quand tu...' (comportement observable), pas 'quand tu fais exprès de...', (2) Ton sentiment — 'je me sens...' (émotion, pas reproche). 'Je me sens seule' plutôt que 'tu m'ignores', (3) Ton besoin — 'j'ai besoin de...' (besoin universel sous l'émotion). 'J'ai besoin de connexion', (4) Une demande spécifique et faisable — 'est-ce que tu pourrais...' (pas une exigence). La différence entre une plainte et une demande : la plainte regarde en arrière, la demande regarde en avant. Le ton et le moment comptent autant que les mots — pas au moment d'un autre stress, pas dans le reproche, idéalement en face à face."},
        {"prompt": "Mon partenaire dit que je ne communique pas. Qu'est-ce que ça veut dire concrètement ?",
         "answer": "Ça peut vouloir dire plusieurs choses différentes : (1) Ne pas partager les émotions — parler des faits mais pas de comment tu te sens par rapport à eux, (2) Se fermer lors des conflits — mur de pierre : silence, monosyllabes, fin de conversation. L'autre vit ça comme un abandon, (3) Ne pas exprimer les besoins — s'attendre à ce que l'autre devine, puis être déçu qu'il/elle ne l'ait pas fait, (4) Communication 'info' sans connexion — répondre aux questions mais pas initier d'échanges sur l'intime. Pour clarifier : demander à ton partenaire 'qu'est-ce que tu aimerais que je partage plus ?' — la réponse dit tout. Et observer dans quelles situations il/elle dit ça."}
    ],
    ["communication couple", "Gottman", "conflit", "besoins", "écoute", "connexion"]
))

save("human/seduction_relations/langages_amour.json", kus(
    "langages_amour",
    "Les 5 langages de l'amour — Gary Chapman",
    "Gary Chapman a identifié 5 façons dont les individus expriment et reçoivent l'amour. Comprendre son propre langage et celui de son partenaire permet d'éviter les malentendus où chacun aime l'autre mais dans une langue que l'autre ne parle pas.",
    "Les 5 langages de l'amour (Gary Chapman, 1992) est un modèle pratique selon lequel chaque individu a un mode principal d'expression et de réception de l'amour parmi cinq catégories : paroles valorisantes, temps de qualité, cadeaux, services rendus et contact physique.",
    {
        "five_languages": [
            {
                "language": "Paroles valorisantes",
                "expression": "Compliments, encouragements, affirmations verbales, 'je t'aime' explicites",
                "reception": "Se sent aimé(e) quand l'autre exprime verbalement son amour et son appréciation",
                "partner_risk": "Se sent non-aimé si le partenaire est peu verbal même s'il agit par amour"
            },
            {
                "language": "Temps de qualité",
                "expression": "Attention totale, activités partagées, présence sans distraction",
                "reception": "Se sent aimé(e) quand l'autre est pleinement présent, regard et attention dédiés",
                "partner_risk": "Téléphone sorti pendant le dîner = message d'abandon même si non intentionnel"
            },
            {
                "language": "Cadeaux",
                "expression": "Objets, gestes matériels, pensée concrète ('j'ai pensé à toi en voyant ça')",
                "reception": "Le cadeau est le symbole de l'attention et de l'importance accordée",
                "partner_risk": "Ne pas marquer les occasions = 'tu ne m'as pas pensé'"
            },
            {
                "language": "Services rendus",
                "expression": "Actions concrètes pour alléger la vie de l'autre — cuisine, aide, organisation",
                "reception": "Se sent aimé(e) quand l'autre agit pour lui/elle sans qu'on le demande",
                "partner_risk": "Partenaire qui parle d'amour mais ne participe jamais = discours sans actes"
            },
            {
                "language": "Contact physique",
                "expression": "Câlins, baisers, toucher, présence physique, affection non-sexuelle",
                "reception": "Le contact est le canal de connexion principal",
                "partner_risk": "Distance physique = distance émotionnelle pour ce profil"
            }
        ],
        "practical_use": [
            "Découvrir son propre langage — qu'est-ce qui te manque le plus quand c'est absent ?",
            "Découvrir le langage du partenaire — qu'est-ce qu'il/elle fait pour toi ? De quoi se plaint-il/elle ?",
            "Parler délibérément la langue de l'autre — même si ce n'est pas la tienne naturellement"
        ],
        "limitations": "Le modèle est une grille de lecture utile mais simplificatrice. Les gens ont souvent 2 langages principaux et les langages peuvent évoluer avec le temps et le contexte."
    },
    [
        {"prompt": "Comment identifier mon langage de l'amour ?",
         "answer": "Trois questions révélatrices : (1) Qu'est-ce qui te blesse le plus dans la relation ? Ce qui te manque pointe vers ton langage. Manque de câlins = contact physique. Manque de 'merci' = paroles valorisantes. (2) Comment exprimes-tu ton amour naturellement ? On a tendance à exprimer dans son propre langage — si tu cuisines pour l'autre sans qu'il/elle demande, ton langage est probablement 'services rendus', (3) De quoi te plains-tu régulièrement ? 'On ne passe jamais de vrai temps ensemble' = temps de qualité. 'Il/elle ne me dit jamais qu'il/elle m'aime' = paroles valorisantes. Le test de Chapman (5lovelanguages.com) est utile mais les 3 questions ci-dessus donnent une réponse fiable en 2 minutes."},
        {"prompt": "Mon partenaire et moi avons des langages de l'amour différents. Comment on fait ?",
         "answer": "C'est la situation normale — la majorité des couples n'ont pas le même langage. Solution : apprendre à parler délibérément la langue de l'autre, même si elle n'est pas naturelle. Exemple concret : toi = temps de qualité, lui/elle = services rendus. Toi : 'on passe du temps ensemble ce soir ?' (ton besoin). Lui/elle : 'j'ai passé du temps à ranger le salon pour qu'on soit bien' (son expression d'amour). Si tu ne vois que le 'il/elle ne fait rien avec moi' et lui/elle ne voit que 'tu n'apprécies pas ce que je fais' — vous vous aimez dans des langues que l'autre ne reçoit pas. Le pas suivant : chacun fait un effort délibéré dans la langue de l'autre UNE FOIS par semaine. Observer si ça change quelque chose."}
    ],
    ["langages amour", "Gary Chapman", "couple", "besoins", "expressions", "communication"]
))

save("human/seduction_relations/relation_longue_duree.json", kus(
    "relation_longue_duree",
    "Relations longue durée — maintenir le désir et la connexion",
    "La passion romantique initiale (6-24 mois) est neurochimiquement distincte de l'amour de long terme. La recherche montre que le désir et la connexion profonde ne se maintiennent pas automatiquement — ils demandent une attention intentionnelle à deux composantes souvent vues comme opposées : la proximité et l'altérité.",
    "Une relation longue durée est une relation romantique qui a survécu à la phase de passion initiale et cherche à maintenir une connexion émotionnelle, physique et intellectuelle dans la durée. Elle repose sur trois piliers : attachement (sécurité), amitié (complicité) et désir (éros).",
    {
        "passion_science": {
            "early_phase": "0-24 mois : dopamine/norépinéphrine/sérotonine — état quasi-addictif. Idéalisation de l'autre.",
            "transition": "Le cerveau s'adapte — le niveau de dopamine normalisé. Ce n'est pas la fin de l'amour, c'est la transition vers un amour différent.",
            "attachment_phase": "Ocytocine/vasopressine dominent — attachement, sécurité, confiance. Moins intense neurochimiquement mais plus profond."
        },
        "esther_perel_framework": {
            "tension": "Esther Perel (Mating in Captivity) : l'amour a besoin de proximité, le désir a besoin de distance. 'On désire ce qu'on n'a pas entièrement.'",
            "domesticity_vs_mystery": "La cohabitation et la sécurité sont nécessaires pour l'amour — et peuvent étouffer le désir si l'altérité de l'autre disparaît complètement.",
            "solutions": ["Maintenir des espaces individuels (hobbies, amis, projets seuls)", "Voir l'autre dans son élément — hors du foyer partagé", "Renouveler l'inconnu — voyages, nouvelles expériences, nouvelles conversations"]
        },
        "maintenance_practices": [
            "Bids for connection (Gottman) — remarquer et répondre aux petites tentatives de connexion de l'autre",
            "Rituels intentionnels — date night réel, sans agenda de couple",
            "Affection physique non-sexuelle quotidienne — câlins, contact",
            "Curiosité active — 'love maps' (Gottman) : connaître l'univers intérieur de l'autre",
            "Gratitude exprimée — dire explicitement ce qu'on apprécie"
        ]
    },
    [
        {"prompt": "Comment maintenir le désir dans une relation longue ?",
         "answer": "Paradoxe central (Esther Perel) : le désir a besoin d'un peu de distance et d'inconnu — ce qui menace la sécurité de l'attachement. Pratiques qui fonctionnent : (1) Avoir des expériences séparées et les partager — retrouver l'autre après une soirée entre amis, une conférence, un voyage seul, (2) Voir l'autre dans un contexte où il/elle est compétent(e) et admiré(e) (travail, passion, scène) — retrouver qui il/elle est hors de la routine commune, (3) Renouveler l'expérience partagée — voyage nouveau, activité jamais faite ensemble, lieu inconnu. La nouveauté active la dopamine même en couple stable, (4) Créer de l'anticipation — distance temporelle courte mais intentionnelle. Ne pas tout faire ensemble systématiquement."},
        {"prompt": "Comment savoir si la routine tue notre couple ou si c'est juste normal ?",
         "answer": "La routine n'est pas le problème — c'est la routine sans connexion. Différence : (1) Routine avec connexion — les mêmes soirées mais avec une vraie présence, des conversations, des moments partagés. Confortable, sécurisant. (2) Routine avec déconnexion — les mêmes soirées en parallèle, chacun sur son écran, peu d'échanges au-delà du logistique. La déconnexion s'installe progressivement. Signal d'alarme : si tu ne sais plus ce qui préoccupe ton/ta partenaire cette semaine, si les échanges sont majoritairement logistiques ('qui fait les courses'), si le rire ensemble est rare. Ce n'est pas irréversible — mais ça demande une intervention intentionnelle."}
    ],
    ["relation longue durée", "désir", "Esther Perel", "Gottman", "connexion", "couple"]
))

save("human/seduction_relations/attachement_styles.json", kus(
    "attachement_styles",
    "Styles d'attachement — sécure, anxieux, évitant",
    "La théorie de l'attachement (Bowlby, Ainsworth) prédit comment on se comporte dans les relations intimes à l'âge adulte. Les 3 styles principaux — sécure, anxieux, évitant — expliquent des patterns relationnels récurrents qui semblent irrationnels de l'extérieur mais ont une logique interne cohérente.",
    "Les styles d'attachement adulte sont des patterns de comportement en relation intime qui reflètent les modèles internes formés dans l'enfance autour de la disponibilité et la réactivité des figures d'attachement. Ils déterminent comment on gère la proximité, l'absence, le conflit et l'intimité dans les relations amoureuses.",
    {
        "three_styles": [
            {
                "style": "Sécure (55-60% de la population)",
                "behavior": "À l'aise avec la proximité et l'autonomie. Confiance en la disponibilité du partenaire. Gère le conflit sans catastrophisme.",
                "childhood_origin": "Figures d'attachement généralement disponibles et réactives",
                "in_relationship": "Peut exprimer ses besoins, entendre ceux de l'autre, réguler ses émotions"
            },
            {
                "style": "Anxieux / préoccupé (20% environ)",
                "behavior": "Hypervigilance aux signaux de rejet. Besoin de réassurance fréquent. Rumination sur la relation.",
                "childhood_origin": "Figures d'attachement imprévisibles — parfois disponibles, parfois pas. Anxiété autour de la disponibilité.",
                "in_relationship": "Text checking, jalousie, interprétation négative du silence, besoin de confirmation",
                "partner_perception": "Peut paraître 'collant' ou 'trop besoin'. Souffre beaucoup avec un partenaire évitant."
            },
            {
                "style": "Évitant / détaché (25% environ)",
                "behavior": "Mal à l'aise avec la proximité émotionnelle. Valorise l'autonomie fortement. Minimise les besoins relationnels.",
                "childhood_origin": "Figures d'attachement peu réactives ou émotionnellement indisponibles. L'enfant apprend à compter sur soi seul.",
                "in_relationship": "Se retire lors des conflits ou de l'intensité émotionnelle. Perçoit les demandes de connexion comme envahissantes.",
                "partner_perception": "Peut paraître 'froid' ou 'distant'. Souffre avec un partenaire anxieux."
            }
        ],
        "anxieux_evitant_dynamic": "Le couple anxieux-évitant est le plus courant et le plus douloureux : plus l'anxieux poursuit, plus l'évitant se retire. Plus l'évitant se retire, plus l'anxieux est anxieux. Spirale.",
        "can_it_change": "Les styles d'attachement ne sont pas figés — les relations sécurisantes (partenaire sécure, thérapie, travail personnel) peuvent 'earned security'. Mais le changement est lent et demande de la conscience.",
        "test": "Amir Levine & Rachel Heller 'Attached' — livre de référence grand public sur l'attachement adulte avec test inclus."
    },
    [
        {"prompt": "Comment reconnaître si je suis attachement anxieux ?",
         "answer": "Patterns distinctifs : (1) Tu vérifies régulièrement tes messages en attendant une réponse — et l'absence de réponse crée de l'inquiétude ou de l'interprétation négative, (2) Tu as souvent besoin de confirmation que ça va dans la relation — 'tu m'aimes encore ?', (3) Les conflits ou le retrait de l'autre déclenchent une peur intense d'abandon, (4) Tu penses souvent à la relation quand tu fais autre chose, (5) Tes anciens partenaires ont dit 'tu es trop' ou 'j'ai besoin d'espace'. Ce n'est pas un défaut — c'est un pattern appris. Il signale un besoin réel de connexion. La question n'est pas 'comment ne plus avoir ce besoin' mais 'comment choisir des partenaires capables de le combler et comment exprimer ce besoin sans la surenchère anxieuse'."},
        {"prompt": "Comment interagir avec un partenaire évitant sans le faire fuir ?",
         "answer": "Principes clés issus de la recherche sur l'attachement : (1) Réduire la pression — les demandes de connexion directe et répétées activent le retrait évitant. Demande moins fréquemment mais plus spécifiquement ('ce soir à 19h, dîner avec toi ?' vs anxiété constante), (2) Valoriser explicitement son autonomie — 'tu peux rentrer seul ce week-end, je comprends que tu en as besoin'. Paradoxalement ça le/la rend plus disponible, (3) Éviter les conflits dans les moments de retrait — quand l'évitant se ferme, ce n'est pas le moment d'insister. Attendre qu'il/elle soit réancré(e), (4) Nommer le pattern sans accuser — 'je remarque qu'on s'éloigne quand il y a du stress — comment on gère ça tous les deux ?'. Important : un partenaire évitant avec quelqu'un de sécure évolue souvent vers plus de sécurité. Un partenaire évitant avec quelqu'un d'anxieux : la spirale s'intensifie."}
    ],
    ["attachement", "anxieux", "évitant", "sécure", "relations", "Bowlby"]
))

save("human/seduction_relations/seduction_en_ligne.json", kus(
    "seduction_en_ligne",
    "Séduction en ligne — apps de rencontre et réseaux sociaux",
    "Les apps de rencontres représentent maintenant le premier vecteur de rencontres dans les pays occidentaux (40-70% des couples selon les études). Elles obéissent à des logiques spécifiques — algorithmes, photos, premier message — très différentes de la rencontre en personne.",
    "La séduction en ligne est la pratique de l'attraction et de la connexion romantique via des plateformes numériques — applications de rencontres (Tinder, Bumble, Hinge, Fruitz), réseaux sociaux (Instagram, Snapchat) ou rencontres en communauté en ligne. Elle implique des codes spécifiques différents de la rencontre en présentiel.",
    {
        "platform_landscape": {
            "tinder": "Volume maximal, swipe-first. Basé sur la proximité géographique. Populaire 18-30 ans.",
            "bumble": "Femmes doivent écrire en premier dans les matches hétéros — réduit certains messages non sollicités",
            "hinge": "Conçu pour sortir du swipe pur — profil plus riche, prompts, 'designed to be deleted'",
            "fruitz": "App française avec emojis de fruits pour classifier les intentions (pomme = sérieux, cerise = flirt...)",
            "once_inner_circle": "Apps premium / curated — audience plus 30-40 ans cherchant du sérieux"
        },
        "profile_optimisation": {
            "photos": [
                "1ère photo = visage clair, sourire, lumière naturelle. Pas de groupe. Pas de lunettes de soleil.",
                "Variété : activité, social, portrait, contexte (voyage/hobby/passion)",
                "Qualité > quantité. 4-6 photos fortes > 9 photos médiocres",
                "Éviter : filtres lourds, seulement des selfies, photos de voiture, groupe où on ne sait pas qui c'est"
            ],
            "bio": "Courte (3-5 lignes max), une info distinctive (pas 'j'aime voyager/rire'), humour ou curiosité, sans liste. Objectif : donner un crochet pour le 1er message.",
            "prompts_hinge": "Répondre de façon distinctive et personnelle — donner une vrai fenêtre sur soi plutôt qu'une réponse générique"
        },
        "first_message": {
            "what_works": "Référence spécifique au profil (photo ou bio) + question ouverte ou observation. 'Ta photo en escalade — tu fais de la salle ou outdoor ?' > 'Salut cc'",
            "what_doesnt": "Messages copiés-collés identiques, compliments physiques immédiats, 'ca va ?', messages trop longs dès le début"
        },
        "transition_irl": "L'objectif des apps est de se rencontrer — ne pas rester en chat trop longtemps. 3-7 jours d'échange max avant de proposer un vrai rendez-vous (café, balade). Les relations qui restent trop longtemps en digital créent une 'chimie de texte' qui ne correspond pas toujours à la réalité."
    },
    [
        {"prompt": "Comment optimiser son profil sur Tinder/Hinge pour avoir plus de matches ?",
         "answer": "Par priorité : (1) Photo principale — visage clair, sourire sincère, lumière naturelle, portrait (pas groupe). C'est 80% de la décision de match, (2) Variété des photos — une activité qui te passionne, un contexte social, un portrait second. Montre différentes facettes, (3) Bio — courte, une info vraiment distinctive (pas 'j'aime voyager' — tout le monde), humour ou curiosité ou quelque chose de spécifique ('je peux débattre des heures du meilleur ramen de Paris' > 'j'aime sortir et rester chez moi'), (4) Sur Hinge — les prompts comptent autant que les photos. Réponds avec quelque chose de réel et de légèrement vulnérable ou drôle. Éviter les réponses génériques. La qualité > la quantité : un profil cohérent et distinctif avec 5 photos fortes battra toujours un profil à 9 photos médiocres."},
        {"prompt": "Quel est le meilleur premier message sur une app de rencontre ?",
         "answer": "Formule qui fonctionne : référence spécifique au profil + une question ou observation ouverte. Exemples : 'Ta photo au Japon — c'était Tokyo ou ailleurs ? J'y ai passé 3 semaines et c'est resté le meilleur voyage de ma vie' / 'Tu as mis dans ta bio que tu ne peux pas choisir entre livre et série — les deux récemment qui t'ont le plus marqué ?' Ce qui fonctionne : montre que tu as lu le profil, crée un sujet de conversation, est personnel. Ce qui ne fonctionne pas : 'Salut ça va ?', 'T'es belle/beau', messages trop longs dès le premier message (intensity creep). Sur Hinge : liker spécifiquement une photo ou un prompt avec un commentaire court est souvent plus efficace qu'envoyer un message à froid."}
    ],
    ["séduction en ligne", "apps rencontre", "Tinder", "Hinge", "profil", "premier message"]
))

save("human/seduction_relations/rupture_deuil.json", kus(
    "rupture_deuil",
    "Rupture amoureuse — deuil, reconstruction et chemin",
    "La rupture amoureuse active les mêmes zones cérébrales que la douleur physique et l'addiction. Le deuil relationnel a ses phases et sa durée propres, qui varient selon l'attachement, la durée et les circonstances. La compréhension du processus aide à ne pas le court-circuiter.",
    "La rupture amoureuse est la dissolution d'une relation romantique, qui déclenche un processus de deuil similaire à celui de la perte d'un proche — avec ses phases (choc, déni, colère, négociation, tristesse, acceptation) et ses mécanismes biologiques (sevrage dopaminergique, réactivation de l'attachement anxieux).",
    {
        "neuroscience": {
            "dopamine_withdrawal": "La relation crée un cycle de récompense dopaminergique. La rupture = sevrage. Explique l'obsession, les 'rechutes' de contact, la douleur physique réelle.",
            "brain_activity": "IRMf (Fisher et al., 2010) : voir la photo de l'ex active les mêmes zones que la cocaïne et la douleur physique — anterior cingulate cortex.",
            "timeline": "La douleur neurochimique peak à 2-4 semaines. Diminue progressivement sur 2-6 mois pour la plupart. Peut durer plus avec des attachements longs ou des ruptures traumatiques."
        },
        "grief_phases": {
            "note": "Non-linéaires — on peut passer de l'acceptation à la colère. Ce n'est pas un échec.",
            "phases": ["Choc et déni (les premiers jours)", "Marchandage ('et si on essayait autrement ?')", "Colère (contre l'ex, contre soi, contre le destin)", "Tristesse et vide", "Acceptation progressive et reconstruction"]
        },
        "what_helps": [
            "No contact (ou contact minimal si enfants) — chaque contact relance le sevrage dopaminergique",
            "Nommer et écrire — journaling émotionnel réduit l'intensité (Pennebaker, 1997)",
            "Maintenir les routines de base — sommeil, repas, exercice physique",
            "Réseau social actif — ne pas s'isoler même quand c'est la tentation",
            "Donner un sens à la douleur — qu'est-ce que cette relation t'a appris sur toi ?"
        ],
        "what_doesnt_help": [
            "Stalking des réseaux sociaux de l'ex — relance l'obsession",
            "Rebond immédiat — peut retarder le deuil sans l'effacer",
            "Alcool/substances comme coping — amplifie la dépression post-rupture",
            "Idéaliser l'ex ou la relation — biais de mémoire sélective post-rupture"
        ]
    },
    [
        {"prompt": "Comment surmonter une rupture quand on est encore amoureux ?",
         "answer": "Ce que la science dit d'abord : la douleur est réelle neurologiquement — pas dramatisation. Le cerveau vit un sevrage. Ça prend du temps indépendamment de ta volonté. Pratiques qui accélèrent sans court-circuiter : (1) No contact — chaque message relance le cycle de dopamine et repart de zéro. Même si ça semble brutal, c'est la décision qui aide le plus à moyen terme, (2) S'autoriser à ressentir — résister à la douleur l'amplifie. Nommer, journaliser, pleurer, (3) Ne pas idéaliser — ta mémoire va sélectionner les bons moments. Notez les raisons de la rupture quelque part et relisez quand la nostalgie frappe, (4) Routine physique — marche, sport. L'exercice produit des endorphines et régule le cortisol. Ce n'est pas 'passer à autre chose' trop vite — c'est prendre soin de soi."},
        {"prompt": "Combien de temps dure une rupture normalement ?",
         "answer": "Pas de réponse universelle mais des repères : étude de la Marshall University (2007) montre que 71% des participants récupèrent bien dans les 3 mois. Facteurs qui allongent : durée de la relation, cohabitation, rupture non choisie (être quitté vs quitter), absence de clôture, attachement anxieux préexistant. Facteurs qui raccourcissent : réseau social actif, activité physique, donner un sens à la fin, pas de contact continu. La règle empirique '1 mois de récupération pour 1 an de relation' est trop simple mais donne un ordre de grandeur. Ce qui compte : ne pas comparer ton rythme à celui des autres. La douleur qui dure 6 mois n'est pas une faiblesse — c'est parfois la profondeur de ce qu'on avait."}
    ],
    ["rupture", "deuil", "récupération", "no contact", "neuroscience amour", "reconstruction"]
))

save("human/seduction_relations/relation_a_distance.json", kus(
    "relation_a_distance",
    "Relation à distance — défis, outils et résilience",
    "Les relations longue distance (LDR) concernent environ 14-15 millions de couples aux USA selon les études. Elles ne sont pas condamnées — les recherches montrent que leur qualité émotionnelle peut égaler celle des couples co-localisés, à condition d'une communication intentionnelle et d'une perspective de réunion.",
    "Une relation à distance (Long Distance Relationship) est une relation romantique dans laquelle les partenaires vivent dans des lieux géographiquement séparés, limitant la fréquence des rencontres en personne. La qualité de la relation dépend largement de la communication intentionnelle et de la présence d'une perspective temporelle claire.",
    {
        "research_findings": {
            "quality": "Études de Stafford & Merolla (2007) : les LDR ne sont pas inférieures en satisfaction, intimité ou confiance aux relations co-localisées. Certaines mesures supérieures — idéalisation positive, qualité des conversations.",
            "success_factors": [
                "Perspective temporelle — les couples qui survivent ont un 'plan' de réunion, même flou",
                "Communication rituelle — contacts réguliers et intentionnels, pas uniquement réactifs",
                "Confiance préalable — les LDR amplifient les insécurités existantes",
                "Indépendance saine — avoir une vie riche localement réduit l'anxiété d'absence"
            ],
            "failure_factors": ["Absence de perspective de réunion", "Communication trop ou pas assez fréquente", "Jalousie non gérée", "Drift progressif — les vies divergent sans connexion suffisante"]
        },
        "communication_tools": [
            "Appels vidéo réguliers (ritualisés, pas 'quand on peut')",
            "Messages audio — plus chaud que le texte, moins contraignant que la vidéo",
            "Netflix Party / Teleparty — regarder ensemble à distance",
            "Jeux en ligne partagés",
            "Lettres ou colis physiques — le tangible compte"
        ],
        "visit_quality": "La rareté des visites augmente leur importance mais aussi la pression. Planifier des activités mais aussi du temps sans agenda — retrouver la normalité est aussi précieux que les moments spéciaux."
    },
    [
        {"prompt": "Comment maintenir une relation à distance sans que ça s'épuise ?",
         "answer": "Trois principes fondamentaux : (1) Ritualiser la communication — pas 'quand on peut' mais des créneaux prévus. L'appel du dimanche soir, le message vocal du matin. La régularité crée la sécurité, (2) Avoir une perspective — même floue. 'D'ici 18 mois on est dans la même ville' ou 'on revoit ça dans 6 mois'. Sans horizon, l'effort de maintien devient épuisant, (3) Avoir une vie riche localement — amis, hobbies, projets. Paradoxalement ça rend la relation LDR plus saine : tu partages des expériences différentes à raconter et tu n'es pas en attente permanente. Ce qui tue les LDR : les rancunes accumulées de l'absence sans espace pour les exprimer, la communication uniquement 'logistique visite', l'absence de perspective réelle."},
        {"prompt": "Les relations à distance peuvent-elles vraiment fonctionner ?",
         "answer": "Oui — avec des conditions. La recherche (Stafford & Merolla, 2007) montre que les LDR ne sont pas inférieures en qualité émotionnelle aux relations co-localisées. Certaines études trouvent une intimité émotionnelle supérieure — les couples LDR ont des conversations plus profondes et plus intentionnelles. Ce qui fait la différence : (1) Une perspective de réunion réelle — les LDR sans date de fin sont très difficiles à maintenir au-delà de 2 ans, (2) La confiance préexistante — la distance n'est pas un test de confiance, c'est un amplificateur. Si la confiance était fragile en présentiel, elle le sera encore plus en LDR, (3) Des visites suffisamment fréquentes — une fois tous les 2-3 mois minimum pour la plupart des couples. La durée de la distance supportable varie beaucoup selon les individus."}
    ],
    ["relation distance", "LDR", "communication", "confiance", "perspective", "rituel"]
))

save("human/seduction_relations/sexualite_et_communication.json", kus(
    "sexualite_et_communication",
    "Sexualité et communication dans le couple",
    "La communication sur la sexualité est le prédicteur le plus solide de la satisfaction sexuelle à long terme. Pourtant c'est le domaine où les couples communiquent le moins explicitement. Apprendre à parler de sexualité réduit les malentendus, augmente la connexion et permet d'évoluer ensemble.",
    "La communication sexuelle dans le couple est la capacité des partenaires à exprimer leurs désirs, limites, plaisirs et insatisfactions de façon à créer une sexualité mutuelle, évolutive et satisfaisante pour les deux. Elle est distincte de la sexualité elle-même mais en est le pilier le plus important à long terme.",
    {
        "research": "Métaanalyse de Montesi et al. (2011) : la communication sexuelle est le meilleur prédicteur de la satisfaction sexuelle, plus que la fréquence ou la variété.",
        "barriers": [
            "Honte culturelle — parler de sexe reste tabou même dans les couples établis",
            "Peur de blesser — 'si je dis ce que j'aime, ça implique qu'il/elle ne le fait pas'",
            "Peur du jugement — désirs perçus comme honteux ou anormaux",
            "Mythe de la spontanéité — l'idée que 'si on doit en parler c'est que ça ne va pas'"
        ],
        "how_to_start": [
            "Hors du contexte sexuel — conversation dans un moment détendu, pas au lit",
            "Parler de soi ('j'aime quand...') vs feedback sur l'autre ('tu ne...')",
            "Questions ouvertes — 'qu'est-ce qui te ferait plaisir qu'on explore ?'",
            "Positiver en premier — ce qui marche bien avant ce qu'on voudrait changer"
        ],
        "desire_evolution": "Le désir change avec le temps, les étapes de vie, le stress, la santé. Normaliser l'idée que la sexualité du couple est un terrain évolutif — pas une vérité figée à l'état initial.",
        "consent_ongoing": "Le consentement n'est pas un contrat signé une fois — il est continu, verbal et non-verbal, et peut changer. 'Est-ce que tu as envie ce soir ?' est une marque de respect et de connexion, pas un manque de spontanéité."
    },
    [
        {"prompt": "Comment parler de sexualité avec son partenaire sans créer de malaise ?",
         "answer": "Moment et cadre : hors du lit, dans un moment détendu, pas lors d'un conflit ou juste après. Formuler en termes de soi : 'j'ai envie d'explorer...', 'j'aime beaucoup quand tu...', 'j'aurais envie qu'on essaie...' — pas 'tu ne fais jamais...' ou 'tu devrais...'. Commencer par le positif — ce qui fonctionne bien. Ça crée un contexte sécurisant avant d'aborder les ajustements. Si tu veux changer quelque chose : 'J'adorerais qu'on essaie X — tu y serais ouvert(e) ?' (invitation, pas exigence). L'humour peut aussi aider à dédramatiser. La conversation sur la sexualité la plus utile : 'qu'est-ce qui t'a le plus plu récemment ?' — ouvre sans mettre l'autre en position défensive."},
        {"prompt": "La fréquence sexuelle baisse dans notre couple. Est-ce normal et que faire ?",
         "answer": "Normal — statistiquement. La fréquence diminue dans la quasi-totalité des couples après 1-2 ans (Klusmann, 2002). Ce qui varie : à quelle vitesse et à quel niveau elle se stabilise. Ce qui influence : stress, santé, hormones, travail, enfants, qualité de la connexion émotionnelle globale. La question n'est pas la fréquence mais la satisfaction : si les deux partenaires sont satisfaits d'une fréquence mensuelle, il n'y a pas de problème. Le problème est le désaccord de désir (desire discrepancy) — l'un veut plus que l'autre. Solutions : communication directe sur les besoins, réduction des inhibiteurs (stress, fatigue, distance émotionnelle), consultation d'un sexologue si la situation est bloquée depuis longtemps."}
    ],
    ["sexualité", "communication couple", "désir", "consentement", "satisfaction", "évolution"]
))

# ═══════════════════════════════════════════════════════════════════════════
# HUMAN / VIE_PRIVEE  (10 fichiers)
# ═══════════════════════════════════════════════════════════════════════════

def kuvp(file_id, title, summary, core_def, knowledge, examples, tags, priority="high"):
    return ku(file_id, "human", "vie_privee", title, summary, core_def, knowledge, examples, tags, priority)

save("human/vie_privee/intimite_personnelle.json", kuvp(
    "intimite_personnelle",
    "Intimité personnelle — les couches de soi qu'on choisit de partager",
    "L'intimité personnelle ne se réduit pas à l'intimité physique — c'est la gestion consciente de ce qu'on partage de soi, avec qui et dans quel contexte. Elle repose sur la confiance, le consentement et les frontières personnelles.",
    "L'intimité personnelle désigne les dimensions intimes de l'existence d'un individu — pensées, émotions, corps, histoires, secrets — qu'il choisit de partager sélectivement selon la confiance établie avec l'autre. Elle est à distinguer de la vie privée (domaine externe) et de l'isolement (choix ou contrainte de non-partage).",
    {
        "layers_of_intimacy": [
            {"layer": "Informations de surface", "content": "Nom, profession, activités publiques", "threshold": "Partagé facilement avec la plupart des gens"},
            {"layer": "Opinions et valeurs", "content": "Positions politiques, valeurs, croyances", "threshold": "Partagé avec ceux en qui on a une confiance minimale"},
            {"layer": "Émotions et ressenti", "content": "Comment on se sent vraiment, peurs, joies profondes", "threshold": "Partagé avec peu — amis proches, partenaire"},
            {"layer": "Histoires personnelles", "content": "Traumas, honte, échecs, douleurs passées", "threshold": "Partagé avec très peu — nécessite confiance solide"},
            {"layer": "Corps et sexualité", "content": "Intimité physique", "threshold": "Partagé selon le consentement et la confiance"}
        ],
        "intimacy_and_trust": "La progressivité de l'intimité partagée est saine — trop rapide (oversharing précoce) peut indiquer un besoin de validation ou créer de l'inconfort chez l'autre. Trop lente ou absente = difficulté à créer des liens profonds.",
        "digital_intimacy": "Les réseaux sociaux ont brouillé les frontières — on partage publiquement des informations qui relevaient autrefois de l'intime. Cette exposition sans réciprocité crée une pseudo-intimité.",
        "self_disclosure": "La divulgation progressive (Altman & Taylor, 1973 — Social Penetration Theory) est le mécanisme de construction de la confiance : on partage un peu, l'autre partage un peu, on approfondissait réciproquement."
    },
    [
        {"prompt": "Comment créer de l'intimité vraie avec quelqu'un ?",
         "answer": "L'intimité se construit par réciprocité progressive : tu partages quelque chose de légèrement vulnérable → l'autre répond avec une ouverture similaire → le niveau de partage monte progressivement. Ce qui accélère : (1) Poser des questions profondes plutôt que de surface ('Qu'est-ce qui te rend vraiment heureux ?' vs 'Tu fais quoi le week-end ?'), (2) Partager en premier quelque chose de vrai et légèrement vulnérable — pas le trauma de l'enfance au premier rendez-vous, mais quelque chose de réel pas de façade, (3) Écouter activement sans conseiller — écoute de validation plutôt qu'écoute de solution, (4) Se souvenir et référencer ce que l'autre a partagé. Ce qui bloque : parler uniquement de faits et d'activités sans jamais partager ce qu'on ressent."},
        {"prompt": "Partager trop sur soi trop vite — pourquoi c'est problématique ?",
         "answer": "Deux effets : (1) Déséquilibre de réciprocité — si tu partages en profondeur quelque chose que l'autre n'est pas prêt à correspondre, il/elle se sent en dette ou mal à l'aise. L'intimité est une danse, pas un monologue, (2) Signal de manque de frontières — l'oversharing précoce peut paradoxalement réduire la confiance : si quelqu'un partage tout avec toi dès le départ, il/elle partage probablement tout avec tout le monde. L'intimité perd sa valeur. La règle n'est pas 'ne jamais partager' — c'est calibrer le niveau de partage au niveau de confiance établi. Les partages profonds trop tôt peuvent créer une pseudo-intimité intense mais fragile, qui s'effondre quand la réalité s'installe."}
    ],
    ["intimité", "confiance", "vie privée", "partage", "vulnérabilité", "frontières"]
))

save("human/vie_privee/frontieres_personnelles.json", kuvp(
    "frontieres_personnelles",
    "Frontières personnelles — poser des limites saines",
    "Les frontières personnelles sont les limites émotionnelles, physiques et relationnelles qu'on pose pour protéger son bien-être et son intégrité. Les poser clairement n'est pas de l'égoïsme — c'est la condition d'une relation saine avec soi-même et avec les autres.",
    "Les frontières personnelles sont des règles et des limites qu'un individu établit pour définir les comportements qu'il accepte ou n'accepte pas dans ses interactions. Elles opèrent dans plusieurs dimensions : physique (corps, espace), émotionnelle (investissement affectif), temporelle (disponibilité), sexuelle et numérique.",
    {
        "types": [
            {"type": "Physiques", "example": "Ne pas être touchée sans consentement. Avoir besoin d'espace personnel dans une pièce."},
            {"type": "Émotionnelles", "example": "Ne pas vouloir gérer les crises émotionnelles de quelqu'un si ça déborde régulièrement."},
            {"type": "Temporelles", "example": "Ne pas répondre aux messages professionnels après 20h."},
            {"type": "Sexuelles", "example": "Ce qu'on accepte ou refuse dans l'intimité."},
            {"type": "Numériques", "example": "Ne pas partager ses mots de passe. Ne pas vouloir être géolocalisé(e) en permanence."},
            {"type": "Matérielles", "example": "Ne pas prêter certains objets ou de l'argent."}
        ],
        "why_hard": [
            "Éducation — 'sois gentil(le)', 'ne dérange pas' — apprendre à dire non est souvent puni",
            "Peur du rejet — 'si je pose une limite, l'autre va partir'",
            "Confusion entre limite et punition — poser une limite n'est pas rejeter l'autre",
            "People-pleasing — identité construite sur l'approbation des autres"
        ],
        "how_to_express": {
            "structure": "'Quand tu fais X, je me sens Y. J'ai besoin de Z.'",
            "example": "'Quand tu m'appelles après 22h sans prévenir, je me sens envahie. J'ai besoin qu'on s'organise autrement.'",
            "tone": "Ferme mais non-hostile. La limite n'est pas une attaque — c'est une information sur soi.",
            "consistency": "Une limite exprimée puis non tenue envoie un signal confus. La tenue de la limite est aussi importante que son expression."
        }
    },
    [
        {"prompt": "Comment dire non sans se sentir coupable ?",
         "answer": "Le 'non' sans culpabilité vient de la conviction que tes besoins sont légitimes — pas de la formulation. Mais la formulation aide : (1) Non complet : 'Non, je ne peux pas.' sans justification excessive. La liste de justifications invite à chaque justification d'être contrée, (2) Non avec alternative : 'Je ne peux pas ce soir mais je suis disponible samedi.', (3) Non différé : 'Laisse-moi réfléchir, je te réponds demain.' — pour ceux qui disent oui sous pression puis regrettent. La culpabilité post-non est normale au début — c'est une habitude qui se recalibre. Elle indique que tu as posé une limite qui va à l'encontre d'une habitude (souvent ancienne). Plus tu poses des limites et que tes relations survivent et s'améliorent, plus la culpabilité diminue."},
        {"prompt": "Comment réagir quand quelqu'un ne respecte pas mes limites ?",
         "answer": "Protocole en trois temps : (1) Reformuler clairement — 'Je t'avais dit que X n'était pas ok pour moi. Quand tu le fais quand même, ça me dit que tu ne prends pas ma limite au sérieux.' Non-accusatoire mais ferme, (2) Nommer la conséquence — 'Si ça continue, je vais devoir [réduire notre contact / sortir de la conversation / partir].' La conséquence doit être réelle et qu'on est prêt à tenir, (3) Tenir la conséquence — si la limite est à nouveau franchie, agir comme annoncé. C'est ce qui différencie une limite d'une demande ignorable. Le moment difficile : certaines personnes escaladent quand on pose des limites (culpabilisation, colère, 'tu changés'). C'est un signal sur la relation, pas sur ta limite."}
    ],
    ["frontières", "limites personnelles", "dire non", "vie privée", "bien-être", "relations"]
))

save("human/vie_privee/vie_privee_numerique.json", kuvp(
    "vie_privee_numerique",
    "Vie privée numérique — données personnelles et traces digitales",
    "Chaque usage numérique laisse des traces — navigateur, smartphone, réseaux sociaux, apps. La vie privée numérique est la capacité à contrôler ces traces et à décider qui accède à quelles informations sur soi, avec des outils concrets accessibles à tous.",
    "La vie privée numérique (digital privacy) est le droit et la capacité de contrôler les informations personnelles générées par l'usage des technologies numériques — historiques de navigation, géolocalisation, métadonnées, profils comportementaux. Elle est encadrée légalement (RGPD en Europe) et protégée techniquement par des outils spécifiques.",
    {
        "data_trails": {
            "browser": "Cookies, historique, profil de navigation. Google sait ce que tu recherches depuis 2009.",
            "smartphone": "Géolocalisation (même apps non-cartographiques), micro, caméra, contacts, habitudes d'usage.",
            "social_media": "Réseau social sait : avec qui tu parles, ce que tu lis, ce qui te fait arrêter de scroller, tes opinions politiques, ton niveau de revenus approximatif.",
            "smart_devices": "Enceintes connectées, montres connectées, TV intelligentes — micros et capteurs permanents."
        },
        "rgpd_rights": [
            "Droit d'accès — demander à toute entreprise quelles données elle a sur toi",
            "Droit de rectification — corriger les données erronées",
            "Droit à l'effacement ('droit à l'oubli') — demander la suppression dans certains cas",
            "Droit d'opposition — refuser le traitement pour certaines finalités",
            "Droit à la portabilité — récupérer ses données dans un format standard"
        ],
        "practical_tools": [
            {"tool": "Navigateur", "recommendation": "Firefox ou Brave plutôt que Chrome. Extension uBlock Origin (bloqueur publicités/trackers)"},
            {"tool": "Moteur de recherche", "recommendation": "DuckDuckGo ou Qwant — pas de profil de recherche"},
            {"tool": "Messagerie", "recommendation": "Signal pour les conversations sensibles — chiffrement de bout en bout réel"},
            {"tool": "VPN", "recommendation": "Proton VPN ou Mullvad pour masquer l'IP. Gratuits partiellement."},
            {"tool": "Mots de passe", "recommendation": "Gestionnaire Bitwarden (gratuit, open-source) — un mot de passe fort unique par service"},
            {"tool": "Email", "recommendation": "ProtonMail pour les communications importantes à chiffrer"}
        ]
    },
    [
        {"prompt": "Comment protéger ma vie privée en ligne sans tout changer ?",
         "answer": "Cinq changements à impact maximal pour effort minimal : (1) Installer uBlock Origin sur Firefox — bloque trackers et pub. 5 minutes. Impact immédiat sur 80% du tracking publicitaire, (2) Passer à DuckDuckGo comme moteur de recherche — 30 secondes dans les paramètres. Google ne profilise plus vos recherches, (3) Signal pour les conversations sensibles — quand tu parles d'argent, santé, projets importants. Chiffrement de bout en bout réel, (4) Gestionnaire de mots de passe — Bitwarden gratuit. Arrêter le mot de passe réutilisé partout, (5) Vérifier les permissions des apps — réseaux sociaux en particulier. Accès micro, géolocalisation, caméra — limiter au strict nécessaire. Ces 5 actions représentent 90% du bénéfice de vie privée numérique accessible sans expertise technique."},
        {"prompt": "Est-ce que mes apps m'écoutent vraiment ?",
         "answer": "La réponse honnête : pas de preuve technique solide d'écoute permanente du microphone pour de la pub ciblée — mais le ciblage publicitaire est si précis via d'autres signaux (géolocalisation, historique, profil comportemental, données de tiers) qu'il donne l'impression d'être écouté. Ce qui est avéré : Facebook/Meta a eu des arrangements pour accéder au micro dans certains contextes d'app. Certaines apps demandent l'accès micro sans raison évidente (un jeu mobile avec accès micro). La protection : (1) Vérifier les permissions micro dans les réglages téléphone app par app, (2) Couper l'accès micro à toute app qui n'en a pas clairement besoin, (3) Utiliser un cache physique pour la caméra si besoin. Le 'tracking par le micro' existe mais est moins répandu que le tracking comportemental et publicitaire classique."}
    ],
    ["vie privée numérique", "RGPD", "tracking", "données personnelles", "outils", "confidentialité"]
))

save("human/vie_privee/solitude_et_isolement.json", kuvp(
    "solitude_et_isolement",
    "Solitude choisie vs isolement — la différence qui compte",
    "Solitude et isolement sont deux états opposés qui peuvent partager la même apparence extérieure. La solitude choisie est une ressource — un espace de ressourcement et de connexion à soi. L'isolement subi est un facteur de risque majeur pour la santé mentale et physique.",
    "La solitude désigne l'état d'être seul. Elle peut être vécue comme ressource (solitude choisie, ressourcement) ou comme souffrance (isolement, solitude imposée). Ces deux états partagent parfois la même forme extérieure mais diffèrent radicalement dans leur vécu subjectif et leurs effets sur la santé.",
    {
        "distinction": {
            "solitude_choisie": {
                "definition": "Temps seul volontairement recherché pour se ressourcer, réfléchir, créer ou simplement être.",
                "experience": "Apaisante, enrichissante, ressourçante",
                "who": "Particulièrement important pour les profils introvertis — la solitude n'est pas un manque de lien social mais un mode de recharge énergétique",
                "health": "Associée à créativité, clarté mentale, réduction du stress"
            },
            "isolement": {
                "definition": "Absence de liens sociaux significatifs — subie ou progressive, souvent non choisie.",
                "experience": "Douloureuse, anxiogène, génère un sentiment de non-appartenance",
                "health": "Facteur de risque équivalent à fumer 15 cigarettes/jour (Holt-Lunstad, 2015). Associé à dépression, déclin cognitif, mortalité augmentée."
            }
        },
        "loneliness_epidemic": "OMS (2023) reconnaît la solitude comme problème de santé publique mondial. Haïku Murthy (US Surgeon General) : épidémie de solitude — 50% des adultes américains rapportent des niveaux de solitude mesurables.",
        "introverts_vs_extraverts": "Les introvertis se ressourcent dans la solitude, les extravertis dans le social. Ni l'un ni l'autre n'est supérieur — c'est un trait de personnalité stable (70-80% de composante génétique selon les études de jumeaux).",
        "signs_of_isolation": [
            "Diminution progressive des contacts (pas toujours consciente)",
            "Plus aucun contexte où on se sent vraiment compris",
            "Sentiment que personne ne remarquerait l'absence",
            "Tout contact social est épuisant ou anxiogène (signe possible d'anxiété sociale)"
        ]
    },
    [
        {"prompt": "Comment savoir si j'ai besoin de solitude ou si je m'isole ?",
         "answer": "Deux questions clés : (1) Comment tu te sens PENDANT — la solitude choisie est apaisante ou productive. L'isolement est douloureux, ennuyeux ou vide même dans la 'solitude'. (2) Comment tu te sens après un contact social — si retrouver des gens te ressource, tu te privais peut-être. Si ça te ressource de rentrer seul(e), tu avais besoin de solitude. Signal d'alarme : si tu évites le social parce que tu anticipes qu'il sera douloureux ou que tu vas décevoir les autres — ce n'est plus de la solitude choisie, c'est de l'anxiété sociale ou de l'isolement qui se renforce. La question n'est pas 'combien de temps seul' mais 'est-ce que j'ai des liens sociaux qui me nourrissent quand je les active ?'"},
        {"prompt": "Je me sens souvent seul(e) même entouré(e) de gens. Comment comprendre ça ?",
         "answer": "La solitude n'est pas l'absence de présence physique — c'est le sentiment d'absence de connexion authentique. On peut être seul dans une pièce pleine de monde. Ce qui crée la solitude-en-groupe : (1) Manque de partage réel — conversations superficielles, pas de sentiment d'être vraiment connu ou compris, (2) Masque social — une persona différente de soi dans les contextes sociaux pour 'correspondre', (3) Sentiment de marginalité — impression de ne pas appartenir même quand physiquement présent. Solutions : chercher des contextes où tu peux être plus authentique (communautés d'intérêt, thérapie, relation 1-1 plutôt que groupe), et identifier quels contextes génèrent de la connexion réelle vs de l'effort de performance sociale."}
    ],
    ["solitude", "isolement", "introversion", "connexion", "santé mentale", "ressourcement"]
))

save("human/vie_privee/secrets_et_confiance.json", kuvp(
    "secrets_et_confiance",
    "Secrets, confiance et confidentialité dans les relations",
    "La confiance est le tissu fondamental de toute relation — et elle se construit ou se détruit dans la façon dont on gère les secrets et la confidentialité. Partager un secret crée de l'intimité ; le trahir crée une blessure durable.",
    "La gestion des secrets dans les relations interpersonnelles désigne les pratiques de partage, de conservation et de protection d'informations intimes ou confidentielles confiées par autrui. Elle est au coeur de la construction et de la rupture de la confiance.",
    {
        "types_of_secrets": [
            {"type": "Secrets intimes partagés", "dynamic": "Créent de l'intimité — partager un secret, c'est donner à l'autre un morceau de soi qu'on ne donne pas à tout le monde"},
            {"type": "Secrets gardés pour l'autre", "dynamic": "Garder un secret de famille ou professionnel confié — marque de fiabilité"},
            {"type": "Secrets gardés à l'autre", "dynamic": "Informations cachées au partenaire — spectre large de bénin (cadeau surprise) à problématique (double vie)"},
            {"type": "Secrets partagés à deux", "dynamic": "Le couple face à la famille, les amis — 'ce qu'on ne dit pas aux autres' renforce la complicité"}
        ],
        "trust_dynamics": {
            "building_trust": "La confiance se construit par : prévisibilité (tu fais ce que tu dis), honnêteté (même inconfortable), loyauté (tu défends l'autre en son absence), discrétion (tu gardes ce qu'on t'a confié).",
            "betrayal": "La trahison d'un secret est l'une des blessures relationnelles les plus durables — elle compromet non seulement la relation mais la capacité à faire confiance en général.",
            "repair": "Réparer une trahison : (1) Reconnaître clairement sans minimiser, (2) Comprendre l'impact sur l'autre, (3) Donner du temps, (4) Reconstruire par la cohérence sur la durée — pas par les promesses."
        },
        "secret_keeping_cost": "Garder un secret a un coût cognitif et émotionnel mesuré (Slepian et al., 2017) — on y pense activement, ça consomme de la bande passante mentale, ça peut peser physiquement. Les secrets les plus lourds : ceux qui touchent à l'identité ou à la honte."
    },
    [
        {"prompt": "Est-ce qu'avoir des secrets dans un couple, c'est normal ?",
         "answer": "Oui — une certaine zone de vie privée même dans une relation intime est saine. La transparence totale n'est ni possible ni souhaitable. Ce qui est normal : avoir des pensées qu'on ne partage pas toutes, avoir une vie intérieure. Ce qui est problématique : des secrets actifs qui affectent la relation ou trompent le partenaire (infidélité, dettes cachées, double vie). La ligne : un secret est ok si tu n'aurais aucune raison de te sentir honteux en le révélant. Il devient problématique quand tu fais activement en sorte que l'autre ne découvre pas, parce que ça changerait quelque chose d'important dans la relation."},
        {"prompt": "Quelqu'un m'a confié un secret et je me sens mal de le garder. Comment gérer ?",
         "answer": "Deux situations distinctes : (1) Secret 'lourd mais non-urgent' — quelque chose de personnel et intime qu'on t'a confié. La loyauté est la règle par défaut. Si ça te pèse, tu peux en parler de façon anonyme avec quelqu'un de neutre ou noter pour toi. Pas pour l'autre de décider si tu peux partager, (2) Secret avec risque pour soi ou pour l'autre — si la personne est en danger (pensées suicidaires, violence, abus) — tu n'es plus lié par la confidentialité. La sécurité prime. Annoncer à la personne que tu dois en parler est mieux que de le faire sans le dire. La règle générale : confiance = garder. Mais pas au prix du bien-être ou de la sécurité de quelqu'un."}
    ],
    ["secrets", "confiance", "confidentialité", "trahison", "intimité", "couple"]
))

save("human/vie_privee/droit_a_la_deconnexion.json", kuvp(
    "droit_a_la_deconnexion",
    "Droit à la déconnexion — temps de cerveau disponible pour soi",
    "Le droit à la déconnexion (légal en France depuis 2017) est aussi un besoin psychologique — la capacité à sortir mentalement du travail et des sollicitations permanentes du numérique. Sans ce droit exercé, le repos est impossible et le burn-out s'installe.",
    "Le droit à la déconnexion désigne le droit de tout travailleur à ne pas être contacté en dehors des heures de travail pour des raisons professionnelles. Il est reconnu légalement en France (Loi Travail 2017) et dans plusieurs pays européens. Psychologiquement, il désigne aussi la capacité à se déconnecter des sollicitations numériques permanentes pour se ressourcer.",
    {
        "legal_framework_france": {
            "law": "Loi El Khomri / Loi Travail (2016, applicable 2017) — droit à la déconnexion pour les entreprises de 50+ salariés",
            "obligation": "Entreprises doivent mettre en place des modalités de régulation des outils numériques — charte ou négociation",
            "reality": "Peu de sanctions. Beaucoup d'entreprises ont une charte sans vrai changement culturel."
        },
        "psychological_need": {
            "cognitive_restoration": "La théorie de la restauration de l'attention (Kaplan, 1989) — le cerveau a besoin de temps sans sollicitation pour restaurer la capacité d'attention focalisée. Le scroll permanent ne restaure pas.",
            "rumination_work": "Penser au travail hors travail empêche la récupération psychologique (Sonnentag, 2003). Ce n'est pas la durée du repos mais la déconnexion mentale qui restaure.",
            "smartphone_as_leash": "La simple présence du téléphone sur la table (visible mais silencieux) réduit les capacités cognitives disponibles (Ward et al., 2017)."
        },
        "practical_strategies": [
            "Ritual de fermeture — action symbolique de fin de journée (fermer le laptop, noter les 3 tâches du lendemain). Signale au cerveau 'c'est terminé'.",
            "Séparation physique téléphone — charger le téléphone hors de la chambre le soir",
            "Notifications professionnelles désactivées après X heure — pas 'à volonté'",
            "Plages No Phone — repas, première heure du matin, activité physique",
            "Loisir actif vs passif — lecture, sport, jardinage restaurent plus que le scroll"
        ]
    },
    [
        {"prompt": "Comment vraiment décrocher du travail après 18h ?",
         "answer": "Trois pratiques avec impact prouvé : (1) Ritual de fermeture — avant de fermer l'ordinateur, noter les 3 priorités du lendemain et fermer tous les onglets. Ce rituel signale au cerveau que le travail est terminé et réduit la rumination nocturne, (2) Coupure des notifications pro — pas 'je vérifierai quand je veux' mais notifications désactivées. La différence : 'je choisis de regarder' vs 'je suis rappelé en permanence', (3) Activité engageante la 1ère heure post-travail — sport, cuisine, lecture. Ce n'est pas du repos passif (scroll) mais une activité qui capte l'attention et crée une rupture mentale réelle. La déconnexion complète est difficile culturellement — mais même 1h de vraie déconnexion par soir a des effets mesurables sur la qualité du sommeil et la capacité de concentration du lendemain."},
        {"prompt": "Mon employeur m'envoie des messages le soir et le week-end. Comment gérer ça ?",
         "answer": "En France : le droit à la déconnexion est légal depuis 2017 — tu as le droit de ne pas répondre hors heures de travail sans que ce soit une faute. La réalité culturelle : dans beaucoup d'entreprises, ne pas répondre rapidement est mal vécu même si légalement protégé. Approche pragmatique par niveau : (1) Pas d'urgence réelle : ne pas répondre. Si demandé : 'je ne regarde pas les messages pro le soir — je t'ai répondu ce matin', (2) Si urgence fréquente : mettre à plat avec le manager. 'Je veux qu'on définisse ensemble ce qui est urgent vs peut attendre le lendemain.', (3) Si c'est systémique et que ça dure malgré la discussion : c'est un signal sur la culture de l'entreprise. La question alors n'est plus comment gérer mais si tu veux continuer à gérer."}
    ],
    ["déconnexion", "vie privée", "travail", "burn-out", "numériquer", "repos mental"]
))

save("human/vie_privee/corps_et_limites.json", kuvp(
    "corps_et_limites",
    "Corps et limites — autonomie corporelle et consentement",
    "L'autonomie corporelle — le droit de décider ce qui se passe avec son propre corps — est un droit fondamental. Elle s'exprime dans les soins médicaux, l'intimité physique, les contacts sociaux et la représentation de son image.",
    "L'autonomie corporelle désigne le droit de chaque individu à exercer un contrôle plein et entier sur son propre corps — dans ses choix médicaux, ses relations physiques et intimes, ses représentations et l'espace qu'il occupe dans le monde. Elle est fondée sur le principe de consentement.",
    {
        "consent_principles": {
            "definition": "Consentement = accord libre, éclairé, révocable et spécifique. S'applique à tout contact physique, pas uniquement sexuel.",
            "FRIES": "Freely given (libre de pression) / Reversible (révocable à tout moment) / Informed (éclairé) / Enthusiastic (enthousiaste, pas juste 'pas de refus') / Specific (spécifique à ce contexte)",
            "absence_of_no": "'Il/elle n'a pas dit non' n'est pas du consentement. Le consentement positif est la norme."
        },
        "medical_autonomy": {
            "principle": "Tout patient a le droit de refuser un traitement, même vital (sauf cas d'urgence avec inconscience). Le médecin informe, le patient décide.",
            "second_opinion": "Le droit à un second avis médical est légal et recommandé pour toute décision thérapeutique importante.",
            "consent_form": "Le consentement éclairé (formulaire signé) est la norme légale avant tout acte invasif."
        },
        "social_physical_boundaries": [
            "Bises, câlins, poignées de main — le contact social n'est pas obligatoire. 'Je suis plus à l'aise avec une salutation à distance' est une frontière valide.",
            "Commentaires sur le corps — 'tu as maigri/grossi', 'quand est-ce que tu fais un enfant' — violation de l'intimité corporelle",
            "Photos — consentement nécessaire pour photographier quelqu'un et pour publier sa photo"
        ]
    },
    [
        {"prompt": "Comment refuser un contact physique (bise, câlin) sans créer de malaise ?",
         "answer": "Direct et chaleureux : 'Je ne fais pas trop les bises — tu m'en voudras pas ?' avec un sourire. Ou 'Je préfère les accolades' ou juste la main tendue avec un sourire. La clarté avec bienveillance est presque toujours mieux reçue que l'inconfort palpable d'un contact qu'on n'a pas voulu. En contexte COVID et post-COVID, c'est devenu beaucoup plus naturel et accepté de proposer une alternative. La plupart des gens s'adaptent sans problème — ceux qui ne s'adaptent pas et insistent malgré ta limite claire t'ont dit quelque chose d'important sur eux."},
        {"prompt": "Mes proches commentent souvent mon corps. Comment faire cesser ça ?",
         "answer": "Deux niveaux selon la fréquence et l'intention : (1) Commentaire isolé — réponse douce et factuelle : 'Je préfère qu'on ne parle pas de mon corps' ou 'Les commentaires sur mon poids, même positifs, ne m'aident pas.' La plupart des gens ne réalisent pas l'impact. (2) Commentaires récurrents malgré la demande — être plus direct : 'Je t'ai déjà dit que les commentaires sur mon corps me mettent mal à l'aise. J'ai besoin que tu respectes ça.' Et si ça continue malgré deux rappels clairs : réduire le sujet ou décider jusqu'où tu es prêt(e) à tolérer pour maintenir la relation. Important : les commentaires sur le corps, même bienveillants ('tu as l'air en forme !'), traversent une frontière sans permission. Ton inconfort est valide."}
    ],
    ["autonomie corporelle", "consentement", "limites", "corps", "respect", "frontières"]
))

save("human/vie_privee/deuil_et_perte.json", kuvp(
    "deuil_et_perte",
    "Deuil et perte — traverser la douleur de la fin",
    "Le deuil est la réponse naturelle à toute perte significative — décès, séparation, perte d'emploi, fin d'un rêve. Il n'y a pas de bonne façon de faire son deuil, ni de délai standard. Comprendre le processus aide à ne pas le juger.",
    "Le deuil est le processus psychologique et émotionnel par lequel un individu répond à une perte significative. Il ne se limite pas au décès — il s'applique à toute rupture avec quelque chose qui avait de la valeur : relation, emploi, santé, projet, identité. Il n'est ni linéaire ni universel.",
    {
        "models": {
            "kubler_ross": {
                "name": "Elisabeth Kübler-Ross (1969) — Les 5 étapes",
                "stages": ["Déni", "Colère", "Marchandage", "Dépression", "Acceptation"],
                "important": "Ces étapes ne sont PAS linéaires et ne s'appliquent pas à tout le monde dans cet ordre. Kübler-Ross elle-même a regretté l'usage prescriptif de son modèle."
            },
            "worden": {
                "name": "Worden (1982) — 4 tâches du deuil",
                "tasks": ["Accepter la réalité de la perte", "Traverser la douleur du deuil", "S'adapter à un environnement sans le disparu", "Investir dans de nouvelles relations tout en maintenant le lien avec le disparu"],
                "note": "Vue plus active — ce qu'on FAIT plutôt que ce qu'on ressent"
            }
        },
        "what_helps": [
            "Nommer et valider les émotions — pas les accélérer ou les minimiser",
            "Rituel de mémoire — créer un espace pour honorer la perte",
            "Réseau de soutien — ne pas traverser seul si possible",
            "Temps — le temps ne guérit pas mais il change la relation à la perte",
            "Professionnel si bloqué — deuil compliqué (18-20% des cas) nécessite un accompagnement"
        ],
        "complicated_grief": "Le deuil compliqué (ou prolongé) se caractérise par : douleur intense persistant au-delà de 12 mois, incapacité à s'adapter à la vie sans le disparu, pensées intrusives, évitement intense. Nécessite une aide professionnelle."
    },
    [
        {"prompt": "Comment soutenir quelqu'un qui fait son deuil sans dire les mauvaises choses ?",
         "answer": "Ce qu'il ne faut PAS dire : 'Je sais ce que tu ressens' (tu ne sais pas), 'C'est pour le mieux' (jamais aidant même si vrai), 'Il/elle est dans un meilleur endroit', 'Tu vas t'en remettre', 'Tu devrais aller de l'avant maintenant'. Ces phrases ferment le deuil plutôt qu'elles ne l'accompagnent. Ce qui aide : 'Je suis là', 'Comment tu vas aujourd'hui ?' (aujourd'hui — pas 'en général'), nommer le disparu, laisser de la place pour pleurer et pour rire (les deux sont normaux), offrir quelque chose de concret ('je viens déjeuner avec toi mardi'). La présence sans agenda est plus précieuse que les bons mots. Souvent le plus utile : écouter et ne pas chercher à réparer."},
        {"prompt": "Mon deuil dure depuis longtemps et je me sens anormal(e). Est-ce que ça va ?",
         "answer": "Il n'y a pas de durée 'normale' de deuil — c'est l'une des choses que la psychologie a le plus mal communicées. La règle des '6 mois' ou '1 an' n'existe pas en recherche clinique. Ce qui détermine la durée : la profondeur de la relation, les circonstances de la perte (mort violente ou soudaine = deuil plus long), la présence de soutien, les pertes antérieures non résolues. Ce qui indique qu'un accompagnement professionnel aiderait : la douleur est aussi intense après 12 mois, tu ne peux pas remplir les fonctions de ta vie (travail, relations), tu as des pensées de ne pas vouloir continuer. Dans ce cas : parler à un médecin ou un psychologue — pas parce que tu fais 'mal' ton deuil, mais parce que tu portes quelque chose de lourd et qu'un soutien professionnel aide réellement."}
    ],
    ["deuil", "perte", "Kübler-Ross", "accompagnement", "soutien", "chagrin"]
))

save("human/vie_privee/espace_personnel.json", kuvp(
    "espace_personnel",
    "Espace personnel et besoin de son propre territoire",
    "L'espace personnel — physique et mental — est un besoin fondamental. Même dans les relations intimes ou les espaces partagés, préserver un territoire propre (bureau, pièce, rituel solo) est essentiel au bien-être et à l'identité individuelle.",
    "L'espace personnel désigne l'espace physique et psychologique qu'un individu considère comme propre et dans lequel il peut exister sans surveillance, intrusion ou obligation de performance sociale. Ce besoin est universel mais son expression et son seuil varient selon les individus et les cultures.",
    {
        "proxemics": {
            "source": "Edward Hall (1966) — The Hidden Dimension",
            "zones": [
                {"zone": "Intime (0-45cm)", "access": "Partenaire intime, enfants, très proche famille"},
                {"zone": "Personnelle (45cm-1.2m)", "access": "Amis proches, relations de confiance"},
                {"zone": "Sociale (1.2-3.6m)", "access": "Connaissances, collègues"},
                {"zone": "Publique (>3.6m)", "access": "Inconnus, foules"}
            ]
        },
        "mental_space": "Au-delà de l'espace physique — temps seul, activités solo, pensées non partagées. Le besoin d'espace mental n'est pas un rejet de l'autre.",
        "cohabitation": "La cohabitation est un des tests les plus exigeants pour l'espace personnel. Couples, colocataires, famille — gérer l'espace partagé nécessite des négociations explicites sur les zones/temps/rituels de chacun.",
        "cultural_variation": "Le besoin d'espace personnel est universel mais son seuil varie culturellement : cultures méditerranéennes et arabes ont une zone intime plus large (contacts fréquents normaux), cultures nordiques et japonaises ont des zones plus strictes.",
        "home_territory": "La chambre, le bureau, le coin canapé — ces 'territoires' dans le foyer partagé ont une valeur psychologique réelle. Les respecter est une marque de considération importante."
    },
    [
        {"prompt": "Mon/ma partenaire n'a pas besoin d'autant d'espace que moi — comment expliquer mon besoin sans le/la blesser ?",
         "answer": "Formuler comme information sur soi, pas comme jugement sur l'autre : 'J'ai besoin de X pour me sentir bien — ce n'est pas que j'ai moins envie d'être avec toi, c'est une façon que j'ai de me ressourcer pour être plus présent(e) ensuite.' Et être spécifique : (1) Quel espace — pièce, coin, temps (pas 'j'ai besoin d'espace' abstrait), (2) Quelle durée ou fréquence — '2 heures le samedi après-midi seul(e)', (3) Ce que ça n'implique pas — 'pendant ce temps-là je ne suis pas en train de t'en vouloir, je recharge'. Le plus difficile : si ton/ta partenaire vit le besoin d'espace comme du rejet, c'est souvent un style d'attachement anxieux. La réassurance préalable ('je reviens après et on fait ça ensemble') aide."},
        {"prompt": "Comment aménager un espace de travail chez soi quand l'espace est limité ?",
         "answer": "Principe fondamental : délimiter même symboliquement l'espace de travail. Ce qui fonctionne même en surface limitée : (1) Surface dédiée — même petite, mais uniquement pour le travail. Le cerveau associe l'espace à l'activité : bureau = travail. Lit = sommeil. Ne pas mélanger, (2) Séparation temporelle à défaut de spatiale — si l'espace est partagé, un rituel de début ('je mets mes écouteurs = je travaille') et de fin ('je range le matériel = c'est fini'), (3) Fond sonore dédié — playlist ou son spécifique uniquement pendant le travail. Crée une séparation cognitive, (4) Lumière — si possible, lumière différente pour travailler vs se détendre dans le même espace. La variante la plus simple : lampe de bureau uniquement pendant le travail."}
    ],
    ["espace personnel", "territoire", "cohabitation", "proxémique", "introversion", "bien-être"]
))

save("human/vie_privee/identite_et_image.json", kuvp(
    "identite_et_image",
    "Identité, image de soi et regard des autres",
    "L'identité est ce qu'on est pour soi. L'image de soi est ce qu'on pense que les autres voient. Ces deux réalités sont souvent décalées — et l'estime de soi dépend de comment on gère cet écart.",
    "L'identité personnelle est l'ensemble des attributs, valeurs, rôles et expériences qu'un individu utilise pour se définir. Elle est à la fois stable (traits de personnalité profonds) et évolutive (rôles, valeurs, projets). L'image de soi est la représentation subjective de soi-même — influencée par le regard des autres mais distincte de lui.",
    {
        "identity_components": [
            {"component": "Identité de rôle", "description": "Parent, professionnel, partenaire — les rôles sociaux qu'on occupe"},
            {"component": "Identité de valeur", "description": "Ce en quoi on croit profondément — honnêteté, famille, liberté..."},
            {"component": "Identité narrative", "description": "L'histoire qu'on se raconte sur soi — 'je suis quelqu'un qui...'"},
            {"component": "Identité de trait", "description": "Personnalité stable — introversion/extraversion, ouverture, conscience"},
            {"component": "Identité sociale", "description": "Appartenance à des groupes (culture, génération, communauté)"}
        ],
        "self_esteem_vs_self_worth": {
            "self_esteem": "L'estime de soi est conditionnelle — varie selon la performance, les succès, les échecs. 'J'ai réussi donc je suis bien'",
            "self_worth": "La valeur propre (self-worth) est inconditionnelle — 'je suis valable indépendamment de mes performances'. Objectif psychologique plus stable.",
            "cultivation": "La valeur propre se cultive par : être cohérent avec ses valeurs, avoir des relations bienveillantes, pratiquer l'autocompassion plutôt que l'autocritique"
        },
        "social_mirror": "George Herbert Mead (1934) — le 'looking glass self' : on se voit en partie à travers le regard qu'on perçoit des autres. Ce regard est souvent déformé (on pense que les autres nous regardent plus et plus négativement qu'ils ne le font — 'spotlight effect')."
    },
    [
        {"prompt": "Comment construire une image de soi plus solide et moins dépendante du regard des autres ?",
         "answer": "Trois pratiques clés : (1) Identifier ses valeurs personnelles (pas celles de la famille ou de la culture) — 'Qu'est-ce qui compte vraiment pour moi indépendamment de ce que les autres pensent ?' Agir en cohérence avec ces valeurs est le fondement de l'estime de soi stable, (2) Réduire les comportements de performance — arrêter progressivement les choses faites uniquement pour l'approbation externe. Ce n'est pas radical — commencer par une décision par semaine motivée par ce qu'on veut vraiment, (3) Pratiquer l'autocompassion (Kristin Neff) — parler à soi-même comme à un ami en difficulté. La critique intérieure constante érode l'estime de soi bien plus que les échecs eux-mêmes."},
        {"prompt": "J'ai l'impression que les gens me jugent constamment. C'est normal ?",
         "answer": "Très normal — et très exagéré par rapport à la réalité. L'effet de projecteur (spotlight effect, Gilovich et al., 2000) : on pense que les autres nous remarquent, nous regardent et nous jugent bien plus qu'ils ne le font réellement. Ils sont occupés à penser à eux-mêmes et à ce que les autres pensent d'eux. Ce qui aide : (1) Données — demande-toi 'ai-je une preuve réelle que cette personne me juge ?' vs 'est-ce une interprétation ?', (2) Perspective temporelle — dans une semaine, dans un an, est-ce que cette interaction aura compté ?, (3) Réciprocité — tu ne te souviens pas de 95% des gens que tu as vus aujourd'hui. Eux non plus. Si le sentiment d'être jugé(e) constamment est très intense et limite tes activités, c'est le signe d'une anxiété sociale qui mérite un accompagnement."}
    ],
    ["identité", "image de soi", "estime", "regard des autres", "valeurs", "autocompassion"]
))

print("\n=== Part 2 : 10 séduction_relations + 10 vie_privée = 20 fichiers ===")
