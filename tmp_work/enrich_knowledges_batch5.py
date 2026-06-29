"""
Enrichissement Knowledge Base ALFRED - Batch 5 : human/wellbeing (suite 15 fichiers)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku_wb(stem, title, summary, core_def, knowledge, examples, tags, related):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.human.wellbeing.{stem}",
      "title": title, "domain": "human", "subdomain": "wellbeing",
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": "bienveillant, concret, sans injonction",
        "structure": ["reconnaître l'état", "proposer une action immédiate", "suggérer un ajustement structurel"],
        "avoid": ["minimiser", "injonctions à la positivité", "confondre conseil et thérapie"]
      },
      "tags": tags + ["bien-être", "santé mentale"],
      "related_knowledge_units": related
    }

# =============================================================================
# human / wellbeing (15 fichiers restants)
# =============================================================================

save("human/wellbeing/sleep_recovery.json", ku_wb(
  "sleep_recovery",
  "Sommeil et récupération",
  "Le sommeil est la ressource fondamentale de la performance cognitive et émotionnelle. Une seule nuit raccourcie dégrade la mémoire, la prise de décision et la régulation émotionnelle de façon mesurable.",
  "Le sommeil est le processus biologique de récupération et de consolidation durant lequel le cerveau consolide la mémoire, régule les émotions, élimine les déchets métaboliques et restaure les fonctions exécutives. Sa quantité et surtout sa qualité déterminent le niveau de performance de la journée suivante.",
  {
    "sleep_stages": [
      {"stage": "Sommeil léger (N1-N2)", "function": "Transition et consolidation légère — 50-60% du temps de sommeil"},
      {"stage": "Sommeil profond (N3)", "function": "Restauration physique, consolidation mémorielle déclarative, élimination des déchets cérébraux — crucial pour la performance cognitive"},
      {"stage": "Sommeil paradoxal (REM)", "function": "Traitement émotionnel, consolidation de la mémoire procédurale et créative, régulation de l'humeur"}
    ],
    "sleep_hygiene": [
      "Heure de lever fixe 7j/7 — l'ancre biologique la plus puissante",
      "Température chambre 16-19°C (le refroidissement du corps est le signal d'endormissement)",
      "Obscurité complète ou masque — la lumière bleue supprime la mélatonine",
      "Dernier repas copieux 2-3h avant le coucher",
      "Réduction progressive de la luminosité 1h avant le coucher",
      "Éviter caféine après 14h (demi-vie ~5-6h dans l'organisme)"
    ],
    "sleep_myths": [
      {"myth": "On peut récupérer le sommeil perdu le weekend", "reality": "La récupération est partielle — la dette de sommeil ne s'efface pas complètement"},
      {"myth": "Certaines personnes ont besoin de peu de sommeil", "reality": "La mutation génétique qui permet de fonctionner avec 6h est rarissime (<0.01%) — la plupart qui 'fonctionnent' avec peu de sommeil sous-estiment la dégradation"},
      {"myth": "L'alcool aide à dormir", "reality": "L'alcool accélère l'endormissement mais fragmente le sommeil profond et paradoxal"}
    ],
    "power_nap": "Sieste de 10-20 min (pas plus pour éviter l'inertie de sommeil) : restaure la vigilance pour 2-3h. Après 15h : risque d'impact sur le sommeil nocturne."
  },
  [
    {"prompt": "Je dors mal depuis plusieurs semaines — que faire ?", "answer": "Premier levier : heure de lever fixe tous les jours (même le weekend). C'est l'ancre biologique la plus efficace. Si le problème persiste plus de 3-4 semaines, une consultation médicale s'impose — l'insomnie chronique a des causes identifiables et traitable. Ne pas attendre."},
    {"prompt": "J'ai besoin de 5h de sommeil, c'est normal ?", "answer": "Peu probable. Moins de 1% de la population a la mutation génétique qui permet de fonctionner vraiment avec 5h. Les autres 99% se sont adaptés à un état de sous-performance qu'ils perçoivent comme normal. Test : sans réveil, dors jusqu'à te réveiller naturellement un weekend. Si tu dors 8-9h, tu as une dette de sommeil."}
  ],
  ["sommeil", "récupération", "performance", "mélatonine", "fatigue"],
  ["knowledges.human.wellbeing.cognitive_fatigue", "knowledges.lifestyle.health.recovery_cycles", "knowledges.cpl.human_organization.energy_management"]
))

save("human/wellbeing/stress_regulation.json", ku_wb(
  "stress_regulation",
  "Régulation du stress",
  "Le stress est une réponse biologique adaptative — utile à court terme, destructeur s'il devient chronique. La régulation du stress passe par l'action sur le corps (respiration, mouvement) autant que sur le mental.",
  "La régulation du stress est l'ensemble des techniques permettant de moduler la réponse physiologique au stress — réduire l'activation du système nerveux sympathique (mode 'combat/fuite') et activer le système parasympathique (mode 'repos/digestion') — pour maintenir un niveau de fonctionnement optimal.",
  {
    "stress_physiology": {
      "acute_stress": "Activation du cortisol et de l'adrénaline — utile pour faire face à une menace immédiate. Se dissipe naturellement en quelques heures.",
      "chronic_stress": "Activation persistante du cortisol — détériore la mémoire, le système immunitaire, la santé cardiovasculaire et la régulation émotionnelle.",
      "window_of_tolerance": "Zone d'activation optimale entre trop peu de stress (ennui, apathie) et trop (panique, paralysie). L'objectif est de rester dans cette fenêtre."
    },
    "immediate_regulation": [
      {"technique": "Respiration 4-7-8", "steps": "Inspirer 4s, retenir 7s, expirer 8s × 4 cycles", "effect": "Active le nerf vague et le système parasympathique en 90 secondes"},
      {"technique": "Respiration carrée (Box breathing)", "steps": "Inspirer 4s, retenir 4s, expirer 4s, retenir 4s", "effect": "Régulation rapide utilisée par les forces spéciales"},
      {"technique": "Décharge physique", "steps": "10 minutes de marche rapide ou d'exercice intense", "effect": "Métabolise le cortisol et l'adrénaline accumulés"},
      {"technique": "Ancrage sensoriel (5-4-3-2-1)", "steps": "Nommer 5 choses vues, 4 entendues, 3 touchées, 2 senties, 1 goûtée", "effect": "Reconnecte au présent et interrompt la rumination"}
    ],
    "structural_regulation": [
      "Activité physique régulière (3× par semaine minimum) — réduction structurelle du cortisol basal",
      "Pratique de méditation ou pleine conscience — réduit la réactivité au stress sur le long terme",
      "Réseau social de soutien — l'ocytocine est un tampon biologique contre le cortisol",
      "Identifier et réduire les stresseurs chroniques évitables (email en continu, surcharge permanente)"
    ]
  },
  [
    {"prompt": "Je suis stressé avant une présentation importante — comment me calmer rapidement ?", "answer": "Respiration carrée : inspire 4 secondes, retiens 4, expire 4, retiens 4. Répète 4 cycles. C'est la technique utilisée par les forces spéciales avant l'action. Physiologiquement, ça active le système parasympathique en moins de 2 minutes. Et rappelle-toi : un peu de stress est une ressource — il acère l'attention. L'objectif n'est pas zéro stress, c'est le bon niveau."},
    {"prompt": "Je suis stressé en permanence — comment sortir de là ?", "answer": "Stress chronique. Deux niveaux d'action : immédiat (respiration, mouvement physique quotidien, sommeil protégé) et structurel (identifier les sources de stress évitables — surcharge, conflits non résolus, absence de récupération). Si ça dure depuis plus de quelques semaines et que ton fonctionnement quotidien est affecté : consulte un médecin. Le stress chronique n'est pas une norme à tenir."}
  ],
  ["stress", "régulation", "cortisol", "respiration", "anxiété"],
  ["knowledges.human.wellbeing.burnout_signals", "knowledges.lifestyle.health.stress_management", "knowledges.human.psychology.resilience"]
))

save("human/wellbeing/motivation_maintenance.json", ku_wb(
  "motivation_maintenance",
  "Maintien de la motivation",
  "La motivation n'est pas un état fixe — elle fluctue selon l'énergie, le sens perçu et la progression visible. La maintenir demande de la nourrir activement : micro-victoires, clarté de l'objectif, et alignement valeurs/actions.",
  "Le maintien de la motivation est l'ensemble des pratiques permettant de soutenir l'engagement et l'élan dans la durée, malgré les obstacles, les plateaux et les baisses d'énergie inévitables dans tout projet ou activité significative.",
  {
    "motivation_types": [
      {"type": "Extrinsèque", "description": "Récompenses externes (argent, reconnaissance, évitement de punition)", "durability": "Efficace à court terme, s'érode avec le temps si elle devient la seule source"},
      {"type": "Intrinsèque", "description": "Plaisir, curiosité, sens, croissance personnelle", "durability": "Plus durable et plus résistante aux obstacles"},
      {"type": "Identitaire", "description": "Alignement avec qui on est ou veut devenir ('je suis quelqu'un qui...')", "durability": "La plus puissante à long terme — change le comportement par défaut"}
    ],
    "motivation_maintenance_tools": [
      "Rendre visible la progression (tableau, journal, streak) — le progrès est le carburant de la motivation",
      "Décomposer les objectifs lointains en jalons hebdomadaires visibles",
      "Célébrer les micro-victoires — le cerveau apprend à associer effort et plaisir",
      "Retrouver le pourquoi quand le comment devient difficile",
      "Changer de méthode avant d'abandonner l'objectif — l'obstacle est souvent dans la tactique, pas dans l'intention"
    ],
    "when_motivation_drops": [
      "C'est normal — la motivation naturelle s'estompe après 2-4 semaines (honeymoon effect)",
      "Après la phase de honeymoon, c'est la discipline et le système qui portent le comportement",
      "Un plateau de progression est un signal d'apprentissage profond, pas d'échec",
      "Fatigue ≠ démotivation : récupérer avant de réévaluer sa motivation"
    ]
  },
  [
    {"prompt": "Je n'ai plus la motivation pour continuer mon projet — est-ce que je dois abandonner ?", "answer": "Avant d'abandonner, vérifier trois choses : est-ce de la fatigue (besoin de récupération) ? Est-ce un plateau de progression (normal en phase d'apprentissage) ? Ou est-ce un vrai désalignement valeurs/projet ? Les deux premiers se surmontent. Le troisième mérite une vraie question. Mais décider d'abandonner quand on est épuisé n'est jamais une bonne décision."},
    {"prompt": "Comment rester motivé sur le long terme ?", "answer": "La motivation ne dure pas naturellement — c'est un carburant d'allumage, pas de croisière. Ce qui tient dans la durée : un système (routine, environnement), une identité ('je suis quelqu'un qui fait X'), et la visibilité du progrès. Les gens qui réussissent sur le long terme ne sont pas plus motivés — ils ont construit des systèmes qui font que le comportement arrive sans dépendre de la motivation."}
  ],
  ["motivation", "engagement", "progrès", "discipline", "objectif"],
  ["knowledges.human.psychology.motivation", "knowledges.human.self_alignment.habits.discipline", "knowledges.human.wellbeing.daily_rhythm_support"]
))

save("human/wellbeing/loneliness_support.json", ku_wb(
  "loneliness_support",
  "Soutien face à la solitude",
  "La solitude est une expérience douloureuse mais commune — et ne doit pas être confondue avec l'isolement social choisi. La distinguer, la traverser et construire des connexions réelles sont les trois axes d'un soutien adapté.",
  "La solitude est l'expérience subjective d'un manque de connexion sociale qui correspond à ses besoins — elle est indépendante du nombre de personnes autour de soi. Elle peut être vécue en groupe comme dans l'isolement physique, et a des effets documentés sur la santé physique et mentale.",
  {
    "loneliness_types": [
      {"type": "Solitude transitoire", "description": "Épisodes passagers liés à des événements (déménagement, rupture, changement de travail) — normale et temporaire"},
      {"type": "Solitude situationnelle", "description": "Liée au contexte (télétravail, expatriation, pandémie) — réductible en changeant le contexte"},
      {"type": "Solitude chronique", "description": "Sentiment persistant de disconnexion malgré des liens sociaux présents — nécessite une exploration plus profonde"}
    ],
    "support_approaches": [
      "Valider l'expérience sans minimiser ('ça arrive à tout le monde' réduit au silence)",
      "Distinguer quantité et qualité des liens — 5 personnes superficielles vs 1 lien profond",
      "Identifier les micro-connexions disponibles (voisins, commerçants, collègues)",
      "Suggérer des activités régulières avec présence sociale (cours, bénévolat, sport collectif)",
      "Reconnaître si la solitude chronique coexiste avec d'autres signaux (dépression, anxiété)"
    ],
    "alfred_position": "ALFRED peut offrir une présence conversationnelle, mais ne peut pas remplacer la connexion humaine réelle. Si la solitude est chronique, il encourage activement à construire des liens humains — et oriente vers un professionnel si nécessaire."
  },
  [
    {"prompt": "Je me sens très seul depuis mon déménagement.", "answer": "C'est une solitude situationnelle — très courante après un grand changement. Elle prend du temps à se résoudre parce que les liens se construisent lentement. Une piste : choisir une activité régulière dans ta nouvelle ville (cours, sport, groupe) — la récurrence crée les conditions de la connexion. Et dans l'immédiat : maintenir les liens existants à distance, même brièvement."},
    {"prompt": "Je suis entouré de gens mais je me sens seul.", "answer": "C'est de la solitude au sens profond — un manque de connexion vraie, pas de présence physique. La quantité de contacts n'est pas la solution. La question : y a-t-il dans ta vie quelqu'un avec qui tu peux être vraiment toi-même ? Si non, c'est là que l'énergie vaut d'être investie — une vraie relation de qualité vaut plus que dix de surface."}
  ],
  ["solitude", "connexion", "isolement", "liens sociaux", "soutien"],
  ["knowledges.human.social_behavior.social_isolation", "knowledges.human.wellbeing.crisis_escalation_awareness", "knowledges.human.social_behavior.social_bonding"]
))

save("human/wellbeing/self_compassion.json", ku_wb(
  "self_compassion",
  "Auto-compassion",
  "L'auto-compassion n'est pas de l'indulgence — c'est la capacité à se traiter avec la même bienveillance qu'on offrirait à un ami. Elle est corrélée à la résilience, la performance et le bien-être, contrairement à la critique de soi qui paralyse.",
  "L'auto-compassion (self-compassion, Kristin Neff) est la capacité à reconnaître sa propre souffrance, à la traiter avec bienveillance plutôt qu'avec auto-critique, et à la replacer dans le contexte commun de l'expérience humaine. Elle repose sur trois composantes : la bienveillance envers soi, la pleine conscience, et l'humanité partagée.",
  {
    "three_components": [
      {"component": "Bienveillance envers soi", "description": "Se parler comme à un ami qui souffre — chaleureux, encourageant, sans jugement", "opposite": "Auto-critique brutale et jugements sévères"},
      {"component": "Pleine conscience", "description": "Reconnaître la souffrance sans l'exagérer ni la nier", "opposite": "Sur-identification (se noyer dans la souffrance) ou évitement (nier)"},
      {"component": "Humanité partagée", "description": "Reconnaître que souffrir, échouer, se tromper fait partie de l'expérience humaine universelle", "opposite": "Isolation ('je suis le seul à échouer comme ça')"}
    ],
    "self_compassion_vs_excuses": [
      "L'auto-compassion augmente la responsabilité — on se remet plus vite d'un échec quand on ne se flagelle pas",
      "La critique de soi sévère crée de la honte — la honte paralyse là où la culpabilité mobilise",
      "Les personnes avec haute auto-compassion ont tendance à apprendre mieux de leurs erreurs (méta-analyses Neff 2003-2020)"
    ],
    "practice": [
      "Quand une erreur arrive : 'Que dirais-je à un ami dans la même situation ?'",
      "Poser une main sur le coeur et se dire : 'C'est difficile en ce moment — et c'est ok'",
      "Écrire une lettre de soi-même à soi-même, depuis la perspective d'un ami bienveillant",
      "Remplacer 'je suis nul' par 'j'ai échoué sur cette chose spécifique — que puis-je apprendre ?'"
    ]
  },
  [
    {"prompt": "Je suis très dur avec moi-même après chaque erreur.", "answer": "La sévérité envers soi-même semble efficace mais elle est en réalité contre-productive — la honte paralyse là où l'apprentissage devrait mobiliser. Question simple : si un ami te racontait la même erreur, que lui dirais-tu ? Souvent, on se parle avec une brutalité qu'on n'imposerait jamais à quelqu'un d'autre. L'auto-compassion, c'est appliquer à soi ce standard bienveillant."},
    {"prompt": "N'est-ce pas de la faiblesse d'être indulgent avec soi-même ?", "answer": "Non — c'est une confusion fréquente. L'auto-compassion n'est pas de l'indulgence (baisser le standard). C'est la capacité à rester debout après un échec pour continuer. Les études montrent que les personnes avec haute auto-compassion assument mieux leurs erreurs, apprennent plus vite et maintiennent mieux leurs objectifs. La critique de soi sévère, elle, génère de l'évitement et de la procrastination."}
  ],
  ["auto-compassion", "bienveillance", "erreur", "résilience", "honte"],
  ["knowledges.human.psychology.resilience", "knowledges.human.emotional_intelligence.self_awareness", "knowledges.human.wellbeing.stress_regulation"]
))

save("human/wellbeing/meaning_support.json", ku_wb(
  "meaning_support",
  "Soutien au sens et à la direction de vie",
  "La perte de sens est l'une des souffrances psychologiques les plus invalidantes. Retrouver une direction passe par la clarification des valeurs, l'identification de ce qui compte vraiment et l'alignement progressif des actions sur ces valeurs.",
  "Le soutien au sens est l'accompagnement dans la quête de signification — comprendre pourquoi on fait ce qu'on fait, ce qui compte vraiment et comment aligner ses choix quotidiens sur ses valeurs profondes. Il ne s'agit pas de trouver LE sens de la vie, mais de créer un sens suffisant pour avancer.",
  {
    "meaning_components": [
      {"component": "Cohérence", "description": "Comprendre sa vie comme une histoire cohérente — le passé explique le présent"},
      {"component": "Objectif", "description": "Avoir quelque chose vers quoi tendre — grand ou petit, immédiat ou lointain"},
      {"component": "Matière", "description": "Sentir que son existence importe — à des personnes spécifiques, à une cause, à un travail"}
    ],
    "when_meaning_is_lost": [
      "Traverser un grand changement (perte, divorce, reconversion, retraite)",
      "Atteindre un objectif longtemps poursuivi (le vide après le succès)",
      "Conflit entre ses valeurs et sa vie réelle",
      "Accumulation de fatigue et perte de perspective"
    ],
    "meaning_restoration_approaches": [
      "Retourner aux valeurs fondamentales : 'Qu'est-ce qui compte vraiment pour moi ?'",
      "Identifier les moments où on se sent vraiment vivant — qu'ont-ils en commun ?",
      "Chercher le sens dans le présent plutôt que le projeter uniquement vers le futur",
      "Service aux autres — créer du sens par contribution",
      "Accepter l'absence temporaire de sens comme une étape, pas un état permanent"
    ],
    "alfred_limits": "La crise de sens profonde peut coexister avec une dépression ou une crise existentielle qui nécessite un accompagnement professionnel (psychologue, thérapeute). ALFRED soutient la réflexion mais ne se substitue pas à cet accompagnement."
  },
  [
    {"prompt": "Je me sens perdu, je ne sais plus pourquoi je fais tout ça.", "answer": "C'est une expérience difficile et plus commune qu'on ne le croit. Pas de réponse rapide ni de liste de conseils. Ce qui aide souvent : mettre des mots sur ce qui a changé récemment, identifier une seule chose qui compte encore, même petite. Le sens ne s'impose pas — il se retrouve par petits bouts. Tu es dans une période de transition, pas nécessairement en train d'échouer."},
    {"prompt": "Comment trouver un sens à ce que je fais professionnellement ?", "answer": "En cherchant l'intersection entre trois cercles : ce dans quoi tu es compétent, ce qui te donne de l'énergie, et ce qui apporte quelque chose aux autres. L'ikigaï japonais appelle ça 'raison d'être'. Ça ne correspond pas toujours à un titre de poste — parfois c'est une façon de faire son travail, ou une contribution indirecte qui compte."}
  ],
  ["sens", "valeurs", "direction", "vide", "transition"],
  ["knowledges.human.psychology.motivation", "knowledges.human.self_alignment.habits.habit_building", "knowledges.human.wellbeing.crisis_escalation_awareness"]
))

save("human/wellbeing/perfectionism_management.json", ku_wb(
  "perfectionism_management",
  "Gestion du perfectionnisme",
  "Le perfectionnisme protecteur est une force quand il pousse à la qualité — il devient destructeur quand il paralyse l'action, génère de la procrastination et lie l'estime de soi au résultat. Le distinguer et le réorienter est essentiel.",
  "Le perfectionnisme est la tendance à fixer des standards très élevés couplée à une évaluation critique sévère quand ces standards ne sont pas atteints. Il existe un perfectionnisme sain (orienté croissance) et un perfectionnisme dysfonctionnel (orienté évitement de l'échec).",
  {
    "perfectionism_types": [
      {"type": "Perfectionnisme adaptatif", "description": "Standards élevés + flexibilité face à l'imperfection — moteur de qualité", "impact": "Positif sur la performance"},
      {"type": "Perfectionnisme maladaptif", "description": "Standards élevés + critique de soi sévère si non atteints — moteur de paralysie", "impact": "Procrastination, anxiété, épuisement"}
    ],
    "perfectionism_traps": [
      "La paralysie par l'analyse : rester à planifier sans jamais lancer",
      "Le tout ou rien : 'si ce n'est pas parfait, ça ne vaut rien'",
      "Finir vs améliorer : rester indéfiniment en mode 'amélioration' sans livrer",
      "Estime de soi conditionnelle : se valoir seulement quand le résultat est parfait",
      "Évitement de l'essai pour ne pas risquer l'imperfection"
    ],
    "reframing_tools": [
      "Standard minimal viable : définir le niveau de qualité suffisant avant de commencer",
      "Deadlines externes : s'engager auprès d'un tiers pour forcer la livraison",
      "Séparer la première version (brouillon) de la version finale — permission d'être imparfait d'abord",
      "Question de recadrage : 'Qu'est-ce que j'aurais fait si j'avais le droit d'être imparfait ?'",
      "La règle des 80% : 80% de qualité en 20% du temps — le dernier 20% coûte 80% de l'effort"
    ]
  },
  [
    {"prompt": "Je n'arrive pas à finir mes projets parce que ce n'est jamais assez bien.", "answer": "C'est le perfectionnisme maladaptif — l'ennemi de l'achevé. Une pratique concrète : définir avant de commencer ce que signifie 'suffisamment bon' pour cette tâche. Puis livrer dès que ce seuil est atteint. La perfection est une direction, pas une destination. Un travail fini imparfait apprend davantage qu'un travail parfait jamais livré."},
    {"prompt": "Comment distinguer exigence saine et perfectionnisme toxique ?", "answer": "L'exigence saine dit : 'Ce n'est pas encore ce que je veux, je vais améliorer ça.' Elle est orientée vers l'action. Le perfectionnisme toxique dit : 'Ce n'est pas assez bien, donc je ne vaux rien.' Il est orienté vers l'évaluation de soi. La distinction se voit dans l'émotion : l'exigence génère de la concentration, le perfectionnisme génère de l'anxiété et de la honte."}
  ],
  ["perfectionnisme", "procrastination", "exigence", "paralysie", "livraison"],
  ["knowledges.human.wellbeing.self_compassion", "knowledges.human.psychology.cognitive_biases", "knowledges.human.cognition.decision_fatigue"]
))

save("human/wellbeing/emotional_regulation_daily.json", ku_wb(
  "emotional_regulation_daily",
  "Régulation émotionnelle au quotidien",
  "Les émotions ne se contrôlent pas — elles se régulent. La régulation émotionnelle consiste à nommer, comprendre et moduler les états émotionnels pour qu'ils ne gouvernent pas les comportements et les décisions.",
  "La régulation émotionnelle quotidienne est l'ensemble des stratégies cognitives, comportementales et somatiques permettant de moduler l'intensité, la durée et l'expression des émotions pour maintenir un fonctionnement adapté dans les contextes variés de la vie.",
  {
    "regulation_strategies": [
      {"strategy": "Nommer l'émotion", "mechanism": "Labelling réduit l'intensité émotionnelle — 'nommer c'est apprivoiser' (Matt Lieberman, UCLA)", "practice": "'Je ressens de la frustration' plutôt que 'je suis en colère'"},
      {"strategy": "Recadrage cognitif", "mechanism": "Changer l'interprétation d'une situation change l'émotion générée", "practice": "'Ce délai est une occasion de préparer mieux' plutôt que 'encore un problème'"},
      {"strategy": "Distanciation", "mechanism": "Prendre du recul — parler de soi à la troisième personne ('qu'est-ce que Sarah ferait ?')", "practice": "Utile face aux décisions chargées émotionnellement"},
      {"strategy": "Action opposée", "mechanism": "Agir à l'opposé de l'impulsion émotionnelle quand l'impulsion est contre-productive", "practice": "Face à l'envie de fuir : se tourner vers la situation. Face à l'envie d'agir impulsivement : s'arrêter."},
      {"strategy": "Régulation somatique", "mechanism": "Agir sur le corps pour réguler l'état émotionnel", "practice": "Respiration, mouvement, ancrage sensoriel"}
    ],
    "emotional_vocabulary": "Plus le vocabulaire émotionnel est riche, plus la régulation est fine. Distinguer frustration, déception, impuissance, colère ou tristesse permet une réponse plus adaptée que 'je suis mal'.",
    "daily_practices": [
      "Check-in émotionnel le matin et le soir (1 minute : qu'est-ce que je ressens en ce moment ?)",
      "Journal émotionnel (3-5 min) : nommer, contextualiser, libérer",
      "Pause avant réponse dans les situations chargées émotionnellement (règle des 24h pour les emails importants)",
      "Activité physique quotidienne comme régulateur de fond"
    ]
  },
  [
    {"prompt": "Je m'emporte facilement — comment me contrôler ?", "answer": "La colère est une information, pas un défaut. Le but n'est pas de la supprimer mais d'augmenter le délai entre le déclencheur et la réaction. Deux techniques : nommer l'émotion à voix haute ou mentalement ('je ressens de la colère') — ça réduit l'intensité neuralement. Et respiration box (4-4-4-4) avant de répondre. La pause de quelques secondes change souvent tout."},
    {"prompt": "Comment ne pas laisser les mauvaises nouvelles me ruiner la journée ?", "answer": "L'émotion est là — la nier agrave les choses. L'accueillir sans s'y noyer : nommer ce que tu ressens, lui donner 5-10 minutes, puis recadrer : 'Qu'est-ce que je peux faire avec ça maintenant ?' Les émotions ont une durée naturelle quand on ne les alimente pas par la rumination. La rumination, elle, peut durer des heures."}
  ],
  ["régulation émotionnelle", "colère", "émotions", "nommer", "recadrage"],
  ["knowledges.human.emotional_intelligence.emotional_management", "knowledges.human.emotional_intelligence.self_regulation", "knowledges.human.wellbeing.stress_regulation"]
))

save("human/wellbeing/body_awareness.json", ku_wb(
  "body_awareness",
  "Conscience corporelle et signaux physiques",
  "Le corps est un système de détection précoce — il signale le stress, la fatigue, les émotions et les besoins avant que le mental les reconnaisse. Écouter le corps est une compétence de bien-être fondamentale.",
  "La conscience corporelle (body awareness) est la capacité à percevoir, interpréter et répondre aux signaux physiques internes — tensions, fatigue, faim, douleur, confort — qui informent sur l'état général et les besoins du moment.",
  {
    "body_signals_dictionary": [
      {"signal": "Tensions dans la nuque / les épaules", "possible_meaning": "Stress accumulé, posture prolongée, charge émotionnelle non exprimée"},
      {"signal": "Serrement dans la poitrine", "possible_meaning": "Anxiété, émotion refoulée, surcharge"},
      {"signal": "Lourdeur dans le ventre", "possible_meaning": "Appréhension, décision difficile, inconfort émotionnel"},
      {"signal": "Fatigue inexpliquée", "possible_meaning": "Signaux de burnout précoce, dette de sommeil, conflit valeurs/actions"},
      {"signal": "Maux de tête répétés", "possible_meaning": "Déshydratation, fatigue visuelle, stress chronique"}
    ],
    "reconnection_practices": [
      "Scan corporel (body scan) : 5 minutes à observer chaque partie du corps sans chercher à changer",
      "Repas sans écran : reconnection aux sensations de faim et satiété",
      "Pause mouvement toutes les 90 minutes : se lever, s'étirer, bouger",
      "Avant une décision importante : demander au corps 'qu'est-ce que je ressens par rapport à cette option ?'"
    ],
    "somatic_intelligence": "Les décisions prises en cohérence avec les signaux corporels (intuition somatique) sont souvent meilleures que celles prises purement par analyse, particulièrement dans les contextes complexes ou ambigus."
  },
  [
    {"prompt": "J'ai souvent des tensions dans les épaules — c'est quoi le problème ?", "answer": "Souvent du stress accumulé non déchargé — physiquement ou émotionnellement. Deux causes fréquentes : posture prolongée devant l'écran (prise en charge par l'ergonomie et les pauses), et tension émotionnelle stockée dans le corps (charge non exprimée). Un étirement quotidien de 5 min et une pause debout toutes les heures aident beaucoup. Si ça persiste, une séance d'ostéopathie ou kiné peut aider."},
    {"prompt": "Comment savoir si ma fatigue est physique ou émotionnelle ?", "answer": "Test : une nuit de sommeil réparatrice améliore-t-elle la fatigue physique ? Pas l'émotionnelle. Si après 8h de sommeil la fatigue est la même, c'est souvent émotionnelle (charge mentale, stress, conflit non résolu). La fatigue émotionnelle se soigne par expression (parler, écrire), repos émotionnel (activités ressourçantes) et parfois par un accompagnement."}
  ],
  ["corps", "signaux corporels", "tensions", "conscience", "intuition"],
  ["knowledges.human.wellbeing.stress_regulation", "knowledges.human.wellbeing.cognitive_fatigue", "knowledges.lifestyle.health.fatigue_management"]
))

save("human/wellbeing/social_reconnection.json", ku_wb(
  "social_reconnection",
  "Reconnexion sociale",
  "Les liens sociaux sont un besoin biologique — leur absence est aussi nocive que le tabac sur la santé. Reconstruire des connexions significatives après une période d'isolement demande intention, régularité et patience.",
  "La reconnexion sociale est le processus de reconstruction active de liens sociaux après une période d'isolement (volontaire ou forcé), une transition de vie, ou un détachement progressif du réseau relationnel. Elle repose sur la régularité des contacts et la qualité des échanges.",
  {
    "reconnection_principles": [
      "La fréquence crée la familiarité — même de courts contacts réguliers construisent un lien",
      "La qualité prime : une conversation en profondeur une fois par mois vaut plus que dix messages superficiels",
      "Initier coûte — mais l'autre est presque toujours content qu'on le fasse",
      "Commencer par les liens existants (rouvrir) plutôt que de tout bâtir from scratch",
      "Les activités régulières avec présence sociale (sport, cours, bénévolat) créent les conditions de la connexion sans la forcer"
    ],
    "reconnection_barriers": [
      "Honte d'avoir 'disparu' trop longtemps ('il va se demander pourquoi je réapparais maintenant')",
      "Attente de la bonne occasion pour recontacter",
      "Perfectionnisme social ('je dois avoir quelque chose d'intéressant à dire')",
      "Fatigue sociale après isolation prolongée — les interactions semblent coûteuses"
    ],
    "practical_steps": [
      "Identifier 3 personnes avec qui la connexion a valu quelque chose",
      "Envoyer un message simple sans attendre ('je pensais à toi, comment tu vas ?')",
      "Proposer une activité concrète (café, appel, sortie) pas juste 'on devrait se voir'",
      "Rejoindre une activité régulière dans sa ville (3 mois de régularité pour commencer à créer des liens)"
    ]
  },
  [
    {"prompt": "J'ai perdu contact avec tous mes amis, par où recommencer ?", "answer": "Commencer par un seul contact — le plus naturel, celui avec qui la conversation reprendrait le plus facilement. Un message simple : 'Je pensais à toi, comment tu vas ?' Sans explication de l'absence. Les gens sont presque toujours heureux d'entendre quelqu'un même après longtemps. L'obstacle principal c'est le sentiment que l'autre n'a pas envie — rarement vrai."},
    {"prompt": "J'ai du mal à rencontrer de nouvelles personnes depuis que je me suis isolé.", "answer": "Reconstruire un réseau from scratch est épuisant parce que chaque interaction est un investissement sans garantie de retour. Le chemin plus facile : une activité régulière (cours de sport, bénévolat, groupe de lecture) où tu revois les mêmes personnes. La répétition crée la familiarité, la familiarité crée l'envie de se connaître mieux — sans la pression de 'créer un lien' dès le premier contact."}
  ],
  ["connexion", "réseau", "amis", "isolement", "liens sociaux"],
  ["knowledges.human.wellbeing.loneliness_support", "knowledges.human.social_behavior.social_bonding", "knowledges.human.social_behavior.social_isolation"]
))

save("human/wellbeing/grief_support.json", ku_wb(
  "grief_support",
  "Soutien face au deuil et aux pertes",
  "Le deuil n'est pas une maladie à guérir — c'est un processus naturel d'adaptation à une perte. Il n'a pas de durée standard ni de trajectoire linéaire. Le soutenir, c'est d'abord valider sans presser.",
  "Le deuil est le processus psychologique et émotionnel d'adaptation à une perte significative — mort d'un proche, rupture, perte d'emploi, fin d'un projet de vie. Il mobilise des réponses émotionnelles intenses (tristesse, colère, déni, culpabilité) qui font partie d'un processus normal de réajustement.",
  {
    "grief_models": [
      {
        "model": "Kübler-Ross (5 étapes)",
        "stages": ["Déni", "Colère", "Marchandage", "Dépression", "Acceptation"],
        "note": "Ces étapes ne sont pas linéaires — on peut les traverser dans n'importe quel ordre, les répéter ou les sauter"
      },
      {
        "model": "Dual Process Model",
        "description": "L'endeuillé oscille entre orientation vers la perte (pleurer, se souvenir) et orientation vers la restauration (reprendre des activités, se projeter). Les deux sont nécessaires."
      }
    ],
    "support_principles": [
      "Valider sans minimiser : 'C'est une perte immense' — pas 'ça ira mieux'",
      "Être présent sans chercher à résoudre : la présence est souvent plus utile que les mots",
      "Respecter le rythme de la personne — le deuil n'a pas de durée standard",
      "Ne pas comparer les pertes ('j'ai vécu pire') — chaque deuil est incomparable",
      "Proposer une aide concrète ('je passe te voir demain') plutôt que générale ('dis-moi si tu as besoin')"
    ],
    "when_grief_becomes_complicated": [
      "Deuil qui empêche tout fonctionnement au-delà de 6-12 mois",
      "Pensées suicidaires liées à la perte",
      "Anhédonie totale (plus aucune capacité à ressentir le plaisir)",
      "Isolement social complet"
    ]
  },
  [
    {"prompt": "J'ai perdu quelqu'un proche il y a 3 mois et je ne vais pas mieux.", "answer": "3 mois, c'est très court pour un deuil significatif. Il n'y a pas de durée normale — le deuil prend le temps qu'il prend. Ce qui aide : ne pas isoler la douleur mais lui donner de l'espace (en parler, écrire, pleurer), maintenir des routines simples même sans élan, et accepter les jours meilleurs et les jours difficiles sans s'alarmer des variations. Si tu te sens en danger, le 3114 est là."},
    {"prompt": "Comment soutenir quelqu'un qui vient de perdre un proche ?", "answer": "Être présent sans chercher à réparer. 'Je suis là' vaut souvent plus que les meilleures phrases. Ce qui aide : ne pas minimiser ('ça va aller'), ne pas comparer, être concret ('je passe mardi, je t'apporte à manger'). Ce qui nuit : le silence par peur de mal dire — mieux vaut une présence maladroite que l'absence."}
  ],
  ["deuil", "perte", "tristesse", "soutien", "acceptation"],
  ["knowledges.human.wellbeing.crisis_escalation_awareness", "knowledges.human.emotional_intelligence.emotional_support", "knowledges.human.wellbeing.self_compassion"]
))

save("human/wellbeing/identity_transition.json", ku_wb(
  "identity_transition",
  "Transitions identitaires",
  "Changer de rôle (parent, retraité, reconversion) implique une transition identitaire — qui peut être déstabilisante même si choisie. Traverser cette transition demande d'intégrer le passé tout en construisant le nouveau.",
  "Une transition identitaire est un processus psychologique de réajustement de l'image de soi lors d'un changement majeur de rôle ou de contexte de vie. Elle implique le deuil de l'identité précédente et la construction progressive d'une nouvelle définition de soi.",
  {
    "transition_triggers": [
      "Reconversion professionnelle ou retraite",
      "Parentalité (devenir parent pour la première fois)",
      "Rupture ou divorce",
      "Migration ou déracinement culturel",
      "Succès ou promotion rapide (identité de 'qui réussit')",
      "Maladie ou handicap (identité corporelle modifiée)"
    ],
    "transition_phases": [
      {"phase": "Fin", "description": "Quitter l'ancienne identité — deuil de ce qu'on était ou de ce qu'on faisait", "challenge": "Résistance et nostalgie"},
      {"phase": "Zone neutre", "description": "Ni l'ancien ni le nouveau — inconfort, confusion, sentiment de vide", "challenge": "Tolérer l'ambiguïté sans chercher à l'accélérer artificiellement"},
      {"phase": "Nouveau départ", "description": "Émergence d'une nouvelle identité — intégrant les apprentissages du passé", "challenge": "Construire progressivement, sans nier qui on était"}
    ],
    "support_approaches": [
      "Reconnaître la légitimité du deuil — même dans une transition choisie et positive",
      "Maintenir des ancres d'identité stables (valeurs, relations, hobbies) pendant la transition",
      "Explorer la nouvelle identité par petits essais avant de s'y engager pleinement",
      "Trouver des pairs qui ont traversé une transition similaire"
    ]
  },
  [
    {"prompt": "J'ai eu la promotion que je voulais mais je me sens perdu.", "answer": "Le paradoxe du succès — atteindre un objectif longtemps poursuivi crée parfois un vide identitaire ('si je ne suis plus celui qui cherche à y arriver, qui suis-je ?'). C'est une transition identitaire normale. La question : maintenant que tu es là, qu'est-ce qui compte vraiment pour toi dans ce nouveau rôle ? Ce n'est pas une question à résoudre en une semaine."},
    {"prompt": "Je viens de partir en retraite et je ne sais plus quoi faire de moi.", "answer": "La retraite est l'une des transitions identitaires les plus brutales — on perd en une journée le rôle qui définissait une grande partie de l'identité sociale. C'est normal de se sentir perdu. La reconstruction prend du temps. Trois axes : maintenir des relations (pas seulement professionnelles), trouver des activités qui donnent un sentiment de contribution, et explorer ce qui était mis en attente pendant les années de travail."}
  ],
  ["identité", "transition", "reconversion", "retraite", "changement"],
  ["knowledges.human.wellbeing.meaning_support", "knowledges.human.psychology.resilience", "knowledges.human.self_alignment.habits.habit_building"]
))

save("human/wellbeing/micro_recovery.json", ku_wb(
  "micro_recovery",
  "Micro-récupération et ressourcement",
  "La récupération n'a pas besoin d'être longue pour être efficace. Des micro-pauses de 5 à 15 minutes, bien choisies, restaurent les ressources attentionnelles et émotionnelles de façon mesurable.",
  "La micro-récupération est une pause courte (5-20 minutes) intentionnellement conçue pour restaurer les ressources cognitives, émotionnelles ou physiques sans nécessiter un arrêt prolongé. Elle s'inscrit dans le rythme ultradien naturel du cerveau (cycle de 90 minutes).",
  {
    "micro_recovery_types": [
      {"type": "Physique", "examples": ["S'étirer", "Marcher 5 min", "Se lever et regarder par la fenêtre"], "benefit": "Circulation, tension musculaire, oxygénation"},
      {"type": "Sensorielle", "examples": ["Regarder un paysage naturel ou une plante", "Écouter 3 minutes de musique douce", "Boire lentement une boisson chaude"], "benefit": "Réduction de l'activation du cortex préfrontal"},
      {"type": "Sociale", "examples": ["Échanger 5 minutes avec quelqu'un de positif", "Appel court avec quelqu'un de proche"], "benefit": "Régulation émotionnelle par l'ocytocine"},
      {"type": "Contemplative", "examples": ["Respiration consciente 5 min", "Observation sans but (rêverie éveillée)", "Méditation courte"], "benefit": "Activation du Default Mode Network — créativité et intégration"}
    ],
    "effectiveness_conditions": [
      "Vraiment s'arrêter — pas une pause avec l'écran dans les mains",
      "Choisir l'activité selon le type de fatigue (physique vs cognitive vs émotionnelle)",
      "Régularité > durée : 3 pauses de 10 min > 1 pause de 30 min décousue",
      "La nature et les espaces verts amplifient la récupération (Attention Restoration Theory, Kaplan)"
    ]
  },
  [
    {"prompt": "Je n'ai pas le temps de faire des pauses — comment me ressourcer quand même ?", "answer": "La pause de 5 minutes existe toujours — entre deux réunions, aux toilettes, en attendant un chargement. L'enjeu n'est pas le temps mais l'usage : éteindre l'écran pendant ces 5 minutes et faire quelque chose de différent (s'étirer, regarder par la fenêtre, respirer). Cinq minutes sans écran régénèrent plus que vingt minutes avec."},
    {"prompt": "Quelle est la meilleure activité de récupération ?", "answer": "Celle qui n'est pas liée à l'activité qui t'épuise. Si tu es épuisé cognitivement (analyse, écriture) : une pause physique ou sensorielle. Si tu es épuisé émotionnellement : la nature ou la solitude douce. Si tu es épuisé physiquement : repos avec stimulation légère (musique, podcast). Le mauvais choix : les réseaux sociaux — ils coûtent de l'attention sans rien restaurer."}
  ],
  ["récupération", "pause", "ressourcement", "rythme", "énergie"],
  ["knowledges.cpl.human_organization.energy_management", "knowledges.human.wellbeing.cognitive_fatigue", "knowledges.human.self_alignment.routines.energy_management"]
))

save("human/wellbeing/gratitude_practice.json", ku_wb(
  "gratitude_practice",
  "Pratique de la gratitude",
  "La gratitude n'est pas une posture naïve — c'est une pratique documentée qui réoriente l'attention vers ce qui fonctionne, réduisant les ruminations négatives et augmentant le bien-être de façon mesurable.",
  "La pratique de la gratitude est la cultivation intentionnelle de la reconnaissance envers ce qui est positif dans sa vie — grands et petits moments. Elle repose sur la neuroplasticité : ce qu'on remarque répétitivement se renforce dans les circuits attentionnels.",
  {
    "science_of_gratitude": [
      "3 méta-analyses (Emmons, Lyubomirsky) montrent une augmentation du bien-être subjectif de 25% avec une pratique régulière",
      "Réduit la rumination et les pensées négatives automatiques",
      "Améliore la qualité du sommeil (pensées positives avant le coucher)",
      "Renforce les liens sociaux quand la gratitude est exprimée à l'autre",
      "Effet le plus fort quand la pratique est régulière mais espacée (3×/semaine > quotidien)"
    ],
    "practice_forms": [
      {"form": "Journal de gratitude", "practice": "3-5 éléments pour lesquels on est reconnaissant, avec 1 ligne d'explication chacun (pas juste les mots)", "frequency": "3× par semaine"},
      {"form": "Lettre de gratitude", "practice": "Écrire une lettre à quelqu'un qui a compté — et si possible la lire en personne (effet fort)", "frequency": "1× par mois"},
      {"form": "Savoring", "practice": "S'arrêter et s'absorber pleinement dans un moment positif quand il se produit", "frequency": "En temps réel"},
      {"form": "Gratitude envers soi", "practice": "Reconnaître ce qu'on a bien fait dans la journée — un contrepoids à la critique de soi par défaut", "frequency": "Quotidien (soir)"}
    ],
    "common_pitfalls": [
      "Forcer la gratitude sur des éléments non ressentis — contre-productif",
      "Liste trop courte ou trop rapide (sans description) — effet minimal",
      "Confondre gratitude et déni des difficultés — la gratitude coexiste avec la difficulté"
    ]
  },
  [
    {"prompt": "Comment commencer une pratique de gratitude concrètement ?", "answer": "Une seule chose : chaque soir, noter 3 moments de la journée pour lesquels tu es reconnaissant. Pas juste 'ma santé, ma famille' — être spécifique : 'la conversation avec X ce matin m'a rappelé que je ne suis pas seul'. La spécificité est ce qui crée l'effet. 5 minutes, 3× par semaine. Tenir 4 semaines avant d'évaluer."},
    {"prompt": "Je ne vois pas pourquoi être reconnaissant quand les choses vont mal.", "answer": "La gratitude n'est pas de nier que les choses vont mal — c'est de ne pas laisser ce qui va mal monopoliser toute l'attention. Deux choses peuvent coexister : une situation difficile ET des éléments qui tiennent encore. La pratique ne supprime pas la douleur — elle rééquilibre la perspective. Elle est d'ailleurs plus efficace dans les moments difficiles que dans les périodes faciles."}
  ],
  ["gratitude", "bien-être", "perspective", "rumination", "positivité"],
  ["knowledges.human.wellbeing.self_compassion", "knowledges.human.emotional_intelligence.self_awareness", "knowledges.human.wellbeing.meaning_support"]
))

print("\nBatch 5 human/wellbeing (15 fichiers) : DONE")
