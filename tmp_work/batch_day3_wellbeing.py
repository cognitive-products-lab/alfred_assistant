"""
Enrichissement day3 — human/wellbeing/ (17 KU)
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

def ku(id_, title, subdomain, priority, summary, core_def, knowledge, examples, guidance, tags):
    return {"schema_version": "1.2", "type": "knowledge_unit", "id": id_, "title": title,
            "domain": "human", "subdomain": subdomain, "status": "validated", "metadata": meta(),
            "priority": priority, "summary": summary, "core_definition": core_def,
            "knowledge": knowledge, "example_answers": examples, "response_guidance": guidance,
            "tags": tags, "related_knowledge_units": []}

save("human/wellbeing/decision_energy_conservation.json", ku(
    "knowledges.human.wellbeing.decision_energy_conservation",
    "Conservation de l'énergie décisionnelle — réduire la charge de choix",
    "wellbeing", "high",
    "Chaque décision consomme des ressources cognitives. Des stratégies de routinisation, de délégation et de simplification préservent l'énergie pour les choix qui comptent vraiment.",
    "La conservation de l'énergie décisionnelle repose sur la reconnaissance que la capacité à prendre de bonnes décisions est une ressource limitée et déplétiable dans la journée. La réduire pour les décisions triviales préserve les ressources pour les choix complexes à fort enjeu.",
    {"strategies": {"routines": "Automatiser les décisions répétitives (menus, tenue, horaires)", "batching": "Regrouper les décisions similaires en un seul moment", "elimination": "Supprimer les options inutiles avant de choisir", "delegation": "Confier les micro-décisions à d'autres ou à des règles prédéfinies", "decision_log": "Pour les décisions récurrentes, noter le raisonnement une fois et s'y référer"},
     "signaux_de_deplection": ["Procrastination sur des choix normalement simples", "Irritabilité face aux demandes de choix", "Choix par défaut systématique", "Regrets post-décision augmentés"],
     "ordre_optimal": "Planifier les décisions importantes le matin ou en début de période reposée"},
    [{"prompt": "Je suis épuisée rien qu'à choisir ce qu'on mange.", "answer": "C'est de la déplétion décisionnelle — tu as fait trop de choix avant. Solution : créer un menu tournant sur 2 semaines. Tu décides une fois, tu suis le plan. Ton cerveau récupère l'énergie pour ce qui compte vraiment."},
     {"prompt": "Comment préserver mon énergie de décision au travail ?", "answer": "Trois leviers : 1) Traiter les décisions importantes en début de journée avant l'accumulation. 2) Pour les petits choix récurrents, créer une règle simple une fois pour toutes. 3) Identifier ce que tu décides que quelqu'un d'autre pourrait décider sans impact réel — et le leur déléguer."}],
    {"tone": "pragmatique, concret, non culpabilisant", "structure": ["reconnaître", "stratégie", "exemple"], "avoid": ["moraliser", "listes exhaustives", "complexifier"]},
    ["décision", "énergie cognitive", "routines", "simplification", "fatigue décisionnelle"]
))

save("human/wellbeing/energy_budgeting.json", ku(
    "knowledges.human.wellbeing.energy_budgeting",
    "Budget énergétique personnel — gérer ses ressources sur la journée",
    "wellbeing", "high",
    "Visualiser son énergie comme un budget limité à répartir intelligemment : activités coûteuses vs rechargeantes, anticipation des pics de demande, récupération planifiée.",
    "Le budget énergétique personnel est une métaphore opérationnelle pour gérer la distribution de ses ressources physiques, cognitives et émotionnelles sur une période donnée, en reconnaissant que chaque activité a un coût variable et que la récupération est non-négociable.",
    {"composantes": {"physique": "Energie corporelle — alimentation, sommeil, mouvement", "cognitive": "Capacité d'attention et de traitement — se dépense avec la complexité", "emotionnelle": "Ressources d'empathie et de régulation — se dépense dans les interactions chargées"},
     "theorie_des_cuilleres": "Métaphore utilisée dans les communautés de handicap invisible : chaque activité 'coûte' une cuillère. Quand les cuillères sont épuisées, stop — sans culpabilité.",
     "planification": {"matin": "Identifier les tâches coûteuses et les positionner quand l'énergie est haute", "transitions": "Prévoir des tampons entre les activités exigeantes", "recup": "Planifier des plages de récupération comme des engagements non-négociables"},
     "erreur_frequente": "Dépenser à crédit (emprunter sur l'énergie de demain) crée une dette qui s'accumule"},
    [{"prompt": "J'essaie de tout faire et je m'effondre en milieu de semaine.", "answer": "Tu dépenses en avance sur ton budget. Essaie ceci : lundi matin, liste tout ce que tu prévois sur la semaine et évalue honnêtement le coût de chaque item. Puis décide d'en retirer 30%. Ce que tu retires ne disparaît pas — il se déplace à la semaine suivante quand tu auras rechargé."},
     {"prompt": "C'est quoi la théorie des cuillères ?", "answer": "C'est une métaphore créée par Christine Miserandino pour décrire la gestion de l'énergie avec une maladie chronique. Le matin tu as un nombre de cuillères (disons 10). Chaque activité en coûte une. Quand tu n'en as plus, c'est fini — tu ne peux pas en créer. Ça aide à rendre visible ce que les gens valides gèrent inconsciemment et que les personnes fatiguées doivent gérer activement."}],
    {"tone": "validant, pratique, respectueux du handicap invisible", "structure": ["cadre", "outil", "application"], "avoid": ["performance", "\"juste te reposer\"", "minimiser la fatigue"]},
    ["énergie", "budget", "cuillères", "handicap invisible", "planification", "fatigue chronique"]
))

save("human/wellbeing/executive_dysfunction.json", ku(
    "knowledges.human.wellbeing.executive_dysfunction",
    "Dysfonction exécutive — difficultés d'initiation et d'organisation",
    "wellbeing", "high",
    "La dysfonction exécutive est l'incapacité à démarrer, organiser ou terminer des tâches même simples, sans lien avec la motivation ou l'intelligence. Comprendre ses mécanismes change l'accompagnement.",
    "La dysfonction exécutive désigne des difficultés dans les fonctions cognitives de haut niveau (planification, initiation, flexibilité, inhibition, mémoire de travail) qui rendent certaines tâches difficiles ou impossibles malgré la volonté. Fréquente dans le TDAH, l'autisme, la dépression, les traumatismes et les maladies chroniques.",
    {"fonctions_affectees": {"initiation": "Commencer une tâche même voulue et simple", "planification": "Décomposer un objectif en étapes", "flexibilite": "Passer d'une tâche à une autre sans friction excessive", "inhibition": "Résister aux distractions ou impulses", "memoire_travail": "Garder plusieurs informations actives simultanément"},
     "manifestations_pratiques": ["Procrastination chronique non-choisie", "Paralysie face à une liste de tâches", "Oublier des choses importantes sans négligence", "Difficulté à démarrer une tâche aimée"],
     "strategies_adaptees": {"body_doubling": "Travailler en présence de quelqu'un (même en silence) abaisse la barrière", "micro_initiation": "Commencer par 2 minutes seulement", "externalisation": "Listes visibles, rappels, systèmes externes pour soulager la mémoire de travail", "task_decomposition": "Décomposer en étapes si petites qu'elles semblent ridicules"},
     "ce_que_ce_n_est_pas": "Paresse, mauvaise volonté, manque d'intelligence — la dysfonction exécutive est neurologique"},
    [{"prompt": "Je sais exactement ce que j'ai à faire et je n'arrive pas à commencer.", "answer": "C'est de la dysfonction exécutive — une difficulté d'initiation, pas de motivation. Le cerveau bloque sur le \"lancement\". Ce qui aide souvent : réduire la tâche à son plus petit premier pas possible (pas \"écrire le rapport\" mais \"ouvrir le fichier\"), et utiliser le body doubling si possible — travailler en présence de quelqu'un, même en silence."},
     {"prompt": "Comment aider quelqu'un avec dysfonction exécutive ?", "answer": "Quatre règles : 1) Ne pas dire \"c'est simple\" — c'est précisément le problème. 2) Proposer de décomposer ensemble plutôt que de laisser la personne face à une tâche opaque. 3) Utiliser des systèmes externes (rappels, listes visibles) plutôt que la mémoire. 4) Le body doubling fonctionne — proposer de travailler côte à côte."}],
    {"tone": "psycho-éducatif, non-jugeant, outillant", "structure": ["définir", "valider l'expérience", "stratégies concrètes"], "avoid": ["\"force-toi\"", "moraliser", "confondre avec paresse"]},
    ["dysfonction exécutive", "TDAH", "initiation", "organisation", "neurodiversité"]
))

save("human/wellbeing/fatigue_patterns.json", ku(
    "knowledges.human.wellbeing.fatigue_patterns",
    "Patterns de fatigue — types, cycles et signaux d'alerte",
    "wellbeing", "high",
    "La fatigue n'est pas monolithique : fatigue physique, cognitive, émotionnelle et compassionnelle ont des sources et des remèdes différents. Reconnaître le type change la récupération.",
    "Les patterns de fatigue désignent les configurations récurrentes de déplétion énergétique selon leur nature (physique, cognitive, émotionnelle, compassionnelle), leurs déclencheurs, leur rythme d'apparition et les stratégies de récupération adaptées à chaque type.",
    {"types": {"physique": {"source": "Effort corporel, manque de sommeil, maladie", "signaux": "Lourdeur, douleurs, besoin de s'allonger", "recuperation": "Sommeil, nutrition, mouvement doux"}, "cognitive": {"source": "Surcharge informationnelle, multi-tâche, décisions", "signaux": "Difficultés de concentration, erreurs inhabituelles, lenteur", "recuperation": "Pauses silencieuses, activité non-cognitive, nature"}, "emotionnelle": {"source": "Interactions chargées, conflits, stress chronique", "signaux": "Irritabilité, larmes faciles, engourdissement affectif", "recuperation": "Solitude, expression artistique, présence sans performance"}, "compassionnelle": {"source": "Soutien continu à d'autres dans la souffrance", "signaux": "Détachement, cynisme, sentiment d'inutilité", "recuperation": "Supervision, limites claires, plaisir sans aide"}},
     "fatigue_chronique": "Quand la fatigue ne récupère plus avec le repos — signal de consulter un médecin. Ne pas confondre avec la paresse ou le manque de motivation.",
     "cycles": "Reconnaître ses cycles personnels (jour, semaine, cycle hormonal) permet d'anticiper les creux et de ne pas programmer d'exigences élevées pendant les périodes basses"},
    [{"prompt": "Je dors bien mais je suis toujours épuisée.", "answer": "Le sommeil récupère la fatigue physique, mais pas forcément les autres. Si tu es épuisée émotionnellement ou cognitivement, dormir aide peu. Questions clés : tes journées sont chargées en émotions ou en décisions ? Tu as du temps pour toi sans performer ? Si non, c'est là qu'il faut chercher."},
     {"prompt": "Depuis que j'aide ma mère malade, je ne ressens plus rien.", "answer": "Ce que tu décris ressemble à de la fatigue compassionnelle — un épuisement de la capacité à ressentir de l'empathie après un soutien intensif et prolongé. C'est courant chez les aidants. Ce n'est pas de l'indifférence, c'est une protection du système nerveux. Ce qui aide : du temps sans rôle d'aidante, de la supervision ou un groupe de parole, et reconnaître que tes besoins comptent aussi."}],
    {"tone": "validant, éducatif, sans minimaliser", "structure": ["identifier le type", "expliquer", "récupération adaptée"], "avoid": ["\"repose-toi c'est tout\"", "pathologiser", "ignorer la fatigue chronique"]},
    ["fatigue", "récupération", "fatigue chronique", "fatigue compassionnelle", "énergie"]
))

save("human/wellbeing/focus_recovery_balance.json", ku(
    "knowledges.human.wellbeing.focus_recovery_balance",
    "Équilibre concentration-récupération — cycles ultradian et deep work",
    "wellbeing", "medium",
    "Le cerveau fonctionne en cycles de 90 minutes de haute performance suivis de périodes de récupération. Travailler contre ces cycles épuise ; travailler avec eux optimise.",
    "L'équilibre concentration-récupération s'appuie sur les rythmes ultradiens (cycles de ~90 min) du système nerveux. Le travail cognitif intense doit alterner avec des phases de récupération active pour maintenir la qualité et éviter la déplétion cumulative.",
    {"rythme_ultradian": "Cycle naturel de 90-120 min d'activité suivis de 20 min de récupération — valable pour le travail comme le sommeil",
     "deep_work": {"definition": "Travail cognitif sans distraction sur une tâche exigeante", "duree_optimale": "90 min maximum par session pour la plupart des personnes", "conditions": "Absence de notifications, environnement prévisible, intention claire"},
     "recuperation_active": {"non_recuperation": "Scroller, emails, réseaux sociaux — consomment de l'attention sans restaurer", "vraie_recuperation": "Marcher, regarder par la fenêtre, méditer, conversation légère", "micropause": "5 min sans écran toutes les 50-90 min suffisent"},
     "signaux_que_le_cycle_est_brisé": ["Erreurs qui augmentent", "Difficulté à rester sur la tâche", "Besoin de relire plusieurs fois", "Irritabilité croissante"]},
    [{"prompt": "Je peux pas rester concentrée plus de 20 minutes.", "answer": "20 minutes de vraie concentration, c'est déjà quelque chose. Ce qu'on peut faire : cycles de 25 min (Pomodoro) avec 5 min de pause vraie (pas d'écran). Sur la journée ça fait 8 cycles potentiels. Si 20 min c'est le maximum même reposée, explorer avec un médecin — ça peut être du TDAH ou autre."},
     {"prompt": "Comment faire du deep work quand j'ai des interruptions constantes ?", "answer": "Trois stratégies : 1) Bloquer des plages dans ton agenda et les traiter comme des réunions (non-négociables). 2) Mode avion ou Do Not Disturb sur le téléphone — les urgences vraies sont rares. 3) Communiquer explicitement : \"Je suis disponible de X à Y, pas entre les deux.\" Si l'environnement ne permet pas ces conditions, c'est un problème d'organisation d'équipe, pas de volonté."}],
    {"tone": "factuel, outillant, sans pression de performance", "structure": ["cadre biologique", "application", "signaux d'alerte"], "avoid": ["optimisation excessive", "culpabiliser", "ignorer le contexte de handicap"]},
    ["concentration", "deep work", "rythme ultradian", "productivité", "récupération"]
))

save("human/wellbeing/medical_boundary_rules.json", ku(
    "knowledges.human.wellbeing.medical_boundary_rules",
    "Limites médicales d'ALFRED — ce qu'il ne doit pas faire",
    "wellbeing", "critical",
    "ALFRED soutient le bien-être mais n'est pas médecin, thérapeute ni diagnostic. Ces règles définissent clairement ce qu'ALFRED peut faire et ce qu'il doit rediriger.",
    "Les limites médicales d'ALFRED définissent le périmètre strict du soutien au bien-être : informer, valider, accompagner et orienter — mais jamais diagnostiquer, prescrire, remplacer un professionnel de santé ou minimiser des symptômes qui nécessitent une évaluation médicale.",
    {"ce_qu_alfred_peut_faire": ["Fournir des informations générales sur les conditions de santé", "Valider une expérience émotionnelle ou physique", "Aider à préparer une consultation médicale", "Suggérer de consulter un professionnel", "Soutenir émotionnellement sans diagnostiquer"],
     "ce_qu_alfred_ne_fait_pas": ["Poser un diagnostic", "Recommander un traitement ou un médicament", "Minimiser des symptômes (\"c'est juste du stress\")", "Se substituer à une thérapie", "Affirmer qu'un symptôme n'est pas grave"],
     "signaux_de_redirection_immediate": ["Mentions de pensées suicidaires ou d'automutilation → numéro de crise", "Symptômes physiques aigus (douleur thoracique, difficulté respiratoire) → urgences", "Détérioration psychologique rapide → consultation urgente"],
     "formulation_type": "\"Je ne suis pas médecin et je ne peux pas te dire si [X]. Ce que je peux faire c'est t'aider à préparer ta consultation ou trouver un professionnel.\""},
    [{"prompt": "J'ai ces symptômes, tu crois que c'est grave ?", "answer": "Je ne peux pas évaluer ça — je ne suis pas médecin. Ce que je peux faire : t'aider à décrire tes symptômes précisément pour ta consultation, ou t'aider à trouver à qui en parler. Tu veux qu'on fasse ça ?"},
     {"prompt": "Le médecin dit que c'est du stress mais je sens que c'est autre chose.", "answer": "Ton ressenti mérite d'être pris au sérieux. Je ne peux pas dire qui a raison — ça nécessite une évaluation médicale que je n'ai pas. Ce que tu peux faire : demander un deuxième avis, noter tes symptômes avec leur fréquence et intensité, ou voir un spécialiste. Ton corps te parle — persister pour être écoutée est légitime."}],
    {"tone": "clair, ferme mais empathique, non-abandonnant", "structure": ["nommer la limite", "ce qui est possible", "rediriger"], "avoid": ["diagnostiquer", "rassurer sans fondement", "couper court à la conversation"]},
    ["limites médicales", "sécurité", "orientation", "diagnostic", "soins"]
))

save("human/wellbeing/mental_overload_patterns.json", ku(
    "knowledges.human.wellbeing.mental_overload_patterns",
    "Patterns de surcharge mentale — identifier et désamorcer",
    "wellbeing", "high",
    "La surcharge mentale est un état de saturation cognitive et émotionnelle où le traitement de nouvelles informations devient difficile. Reconnaître ses propres patterns permet d'intervenir avant l'effondrement.",
    "La surcharge mentale (mental overload) est l'état dans lequel la capacité de traitement cognitif et émotionnel est dépassée par le volume, la complexité ou l'intensité des sollicitations, entraînant erreurs, irritabilité, paralysie et détérioration de la prise de décision.",
    {"signaux_precoces": ["Irritabilité augmentée pour des triggers mineurs", "Oublis inhabituels", "Difficulté à terminer des phrases ou des pensées", "Besoin de relire plusieurs fois la même chose", "Sensation de \"trop\""],
     "signaux_avances": ["Paralysie complète face à des tâches simples", "Larmes ou explosions sans raison apparente", "Incapacité à prendre la moindre décision", "Dissociation légère (\"je suis là mais pas là\")"],
     "declencheurs_communs": ["Accumulation sur plusieurs jours sans récupération", "Événement inattendu sur un fond déjà chargé", "Charge invisible élevée (mental load domestique, soucis chroniques)", "Manque de sommeil cumulé"],
     "interventions": {"immediat": "Arrêter, sortir de l'écran, respirer lentement", "court_terme": "Décharger sur papier tout ce qui est dans la tête", "moyen_terme": "Identifier et réduire une source de charge"}},
    [{"prompt": "Je me sens complètement dépassée en ce moment.", "answer": "\"Dépassée\" — c'est important comme signal. Est-ce que tu peux me dire ce qui pèse le plus en ce moment ? Parfois juste de mettre des mots dessus et de les sortir de la tête soulage. On peut aussi regarder ensemble ce qui peut être reporté ou délégué."},
     {"prompt": "Comment savoir si c'est de la surcharge ou si je suis juste nulle ?", "answer": "La surcharge mentale et le manque de capacité se distinguent facilement : la surcharge fluctue (tu fonctionnes bien quand la pression baisse), le manque de compétence est stable. Si tu as des périodes où tu gères bien, c'est de la surcharge — pas de la nullité. Et même si c'était un manque de compétence, la solution serait de former, pas de souffrir en silence."}],
    {"tone": "validant, rassurant, outillant", "structure": ["reconnaître", "distinguer", "intervenir"], "avoid": ["\"gère-toi\"", "listes froides", "juger le niveau de charge"]},
    ["surcharge", "overload", "charge mentale", "burnout", "saturation cognitive"]
))

save("human/wellbeing/motivation_fluctuation_patterns.json", ku(
    "knowledges.human.wellbeing.motivation_fluctuation_patterns",
    "Fluctuations de motivation — cycles normaux et signaux d'alarme",
    "wellbeing", "medium",
    "La motivation varie naturellement. Distinguer une fluctuation normale d'un décrochage nécessitant attention permet d'éviter la culpabilité inutile autant que le déni.",
    "Les fluctuations de motivation sont des variations normales de l'élan vers l'action, influencées par le cycle circadien, le cycle hormonal, la charge émotionnelle, les progrès perçus et l'environnement. Elles ne sont pas des signaux d'échec mais des informations à utiliser.",
    {"types_de_fluctuation": {"quotidienne": "Pic matinal pour la plupart, creux post-déjeuner — adapter les tâches au rythme", "hebdomadaire": "Souvent plus élevée en début de semaine — planifier les tâches importantes lundi-mardi", "situationnelle": "Baisse après un échec, pic après une victoire — effets brefs et récupérables", "chronique": "Perte durable de motivation sur plusieurs semaines — signal de consulter"},
     "signaux_normaux": ["Envie variable selon les jours", "Moins motivée sur les tâches routinières", "Motivation basse pendant la période prémenstruelle"],
     "signaux_d_alarme": ["Perte de motivation pour des activités auparavant plaisantes (anhedonie)", "Durée > 2 semaines sans amélioration", "Accompagnée de tristesse persistante ou d'épuisement"],
     "strategies": {"momentum": "Commencer petit pour relancer le mouvement", "meaning": "Reconnecter à la raison profonde de la tâche", "environnement": "Changer de lieu ou d'heure pour contourner les associations négatives"}},
    [{"prompt": "Je n'ai plus envie de rien depuis quelques semaines.", "answer": "\"Plus envie de rien\" depuis quelques semaines, ça mérite attention. Est-ce que tu as aussi moins de plaisir dans des choses qui t'en donnaient avant ? Et comment tu dors ? Si tu coches plusieurs cases, il serait bon d'en parler à un médecin — ce n'est pas de la faiblesse, c'est une information que ton corps envoie."},
     {"prompt": "Ma motivation monte et descend, est-ce que c'est normal ?", "answer": "Complètement normal. La motivation n'est pas un état stable — c'est une ressource qui fluctue avec l'énergie, les émotions, les cycles biologiques et l'environnement. Le problème c'est de l'attendre constante et de s'en vouloir quand elle baisse. Ce qui marche mieux : agir sur le système (routine, environnement) plutôt qu'attendre l'élan."}],
    {"tone": "normalisateur, vigilant sur les signaux d'alarme", "structure": ["normaliser", "distinguer", "agir"], "avoid": ["\"force-toi\"", "minimiser des signaux sérieux", "culpabiliser les fluctuations normales"]},
    ["motivation", "fluctuation", "énergie", "cycles", "anhedonie", "dépression"]
))

save("human/wellbeing/recovery_cycles.json", ku(
    "knowledges.human.wellbeing.recovery_cycles",
    "Cycles de récupération — comment le corps et l'esprit récupèrent vraiment",
    "wellbeing", "high",
    "La récupération n'est pas passive. Elle obéit à des cycles biologiques et psychologiques précis. Comprendre ces cycles permet de récupérer plus efficacement en moins de temps.",
    "Les cycles de récupération désignent les processus biologiques et psychologiques par lesquels le corps et le cerveau restaurent leurs ressources après un effort. Ils incluent le sommeil (cycles NREM/REM), les rythmes ultradiens, la récupération émotionnelle et la consolidation mémorielle.",
    {"sommeil": {"cycles": "Cycles de 90 min (léger → profond → REM) — couper un cycle laisse plus fatigué", "profond": "Restauration physique — surtout en première partie de nuit", "rem": "Consolidation mémorielle et traitement émotionnel — surtout en seconde partie", "dette": "Impossible à totalement récupérer — l'impact sur la cognition persiste"},
     "recup_cognitive": {"micropause": "5-10 min sans écran toutes les 90 min restaurent l'attention", "nature": "20 min en environnement naturel réduit le cortisol de manière mesurable", "somnolence": "Une sieste de 20 min améliore les performances sans inertie de sommeil (> 30 min = torpeur)"},
     "recup_emotionnelle": {"traitement": "Les émotions non traitées consomment des ressources en arrière-plan", "expression": "Journaling, art, conversation — externalisent la charge et libèrent les ressources", "connexion": "Le lien social de qualité restaure l'état émotionnel pour la plupart des personnes"}},
    [{"prompt": "Je dors 8h et je me réveille épuisée.", "answer": "Plusieurs pistes : 1) Qualité plutôt que quantité — l'apnée du sommeil ou un réveil en milieu de cycle donne ce résultat. 2) La dette émotionnelle non traitée consomme de l'énergie même pendant le sommeil. 3) Si c'est persistant, une consultation médicale s'impose — la fatigue chronique et l'hypothyroïdie donnent ce symptôme exact."},
     {"prompt": "C'est quoi la récupération active ?", "answer": "La récupération active, c'est des activités qui rechargent sans consommer d'attention — marcher, cuisiner quelque chose de simple, écouter de la musique sans faire autre chose, regarder par la fenêtre. L'opposé c'est le scroll ou les emails : ils donnent l'illusion de pause mais consomment de l'attention. Ce n'est pas de la récupération, c'est une autre forme de travail cognitif."}],
    {"tone": "factuel, pratique", "structure": ["mécanisme", "application", "signaux d'alarme"], "avoid": ["suroptimiser", "culpabiliser sur la qualité du sommeil"]},
    ["récupération", "sommeil", "cycles", "sieste", "fatigue", "restauration"]
))

save("human/wellbeing/recovery_management.json", ku(
    "knowledges.human.wellbeing.recovery_management",
    "Gestion de la récupération — planifier et protéger les temps de repos",
    "wellbeing", "high",
    "La récupération doit être planifiée comme une activité, pas attendue par défaut. Stratégies pour l'intégrer structurellement dans le quotidien malgré les obligations.",
    "La gestion de la récupération est le processus délibéré de planification, de protection et d'optimisation des périodes de repos pour maintenir des niveaux d'énergie soutenables sur le long terme, en reconnaissant que la récupération est une condition de la performance, pas son opposé.",
    {"principes": {"planifier_d_abord": "Bloquer les temps de récupération avant de remplir l'agenda avec des tâches", "non_negociable": "Traiter la récupération comme un rendez-vous médical — pas déplaçable sans raison sérieuse", "adapter_le_type": "Choisir la récupération selon ce qui est épuisé (physique, cognitif, émotionnel)"},
     "strategies_pratiques": {"micro": "5 min toutes les heures — sans écran, sans décision", "meso": "Demi-journée de récupération par semaine", "macro": "Période de ressourcement profond (vacances, retraite) — planifiée à l'avance"},
     "obstacles_communs": {"culpabilite": "\"Je devrais travailler\" — réévaluer la récupération comme investissement", "urgences_percues": "Distinguer urgence réelle de pression artificielle", "fomo": "La récupération n'est pas perdre du temps — c'est en gagner"},
     "pour_aidants_et_soignants": "Particulièrement critique pour ceux qui soutiennent d'autres — ils ne peuvent pas donner ce qu'ils n'ont pas"},
    [{"prompt": "Je n'ai jamais le temps de me reposer.", "answer": "\"Pas le temps\" signifie souvent que la récupération n'est pas dans l'agenda — pas qu'elle est impossible. Essai : la semaine prochaine, bloque 30 minutes le matin pour toi avant les obligations. Pas négociable. Observe ce qui se passe. Souvent les \"urgences\" s'ajustent d'elles-mêmes quand les limites sont posées."},
     {"prompt": "Je culpabilise de me reposer quand il y a tant à faire.", "answer": "Cette culpabilité est compréhensible — elle vient souvent d'une croyance que la valeur se mesure à la productivité. La réalité biologique : sans récupération, la qualité de travail baisse, les erreurs augmentent, le burnout arrive. Te reposer n'est pas abandonner les autres — c'est te maintenir en état de les soutenir durablement."}],
    {"tone": "validant, structurant, anti-culpabilité", "structure": ["valider l'obstacle", "stratégie concrète", "cadre mental"], "avoid": ["injonction", "liste d'obligations", "nier la difficulté réelle"]},
    ["récupération", "repos", "burnout prévention", "agenda", "soutenabilité"]
))

save("human/wellbeing/sleep_hygiene_basics.json", ku(
    "knowledges.human.wellbeing.sleep_hygiene_basics",
    "Hygiène du sommeil — les fondamentaux qui fonctionnent vraiment",
    "wellbeing", "medium",
    "Les pratiques à fort impact pour améliorer la qualité du sommeil, distinguées des mythes populaires. Axé sur ce qui est soutenu par les données.",
    "L'hygiène du sommeil désigne l'ensemble des comportements et conditions environnementales qui favorisent un sommeil de qualité. Elle n'est pas une solution à tous les troubles du sommeil, mais un socle fondamental dont l'absence aggrave la plupart des problèmes.",
    {"pratiques_haute_evidence": {"horaires": "Se lever à la même heure 7j/7 — plus important que l'heure de coucher", "lumiere": "Exposition à la lumière naturelle le matin (15-30 min) — synchronise l'horloge circadienne", "temperature": "Chambre entre 16-19°C — le corps doit refroidir pour dormir", "caféine": "Arrêter 8-10h avant de dormir (demi-vie de 5-7h)"},
     "mythes": {"8h_obligatoires": "Les besoins varient de 6 à 9h selon les individus", "alcool_aide": "L'alcool fragmentise le sommeil — il aide l'endormissement mais dégrade la qualité", "rattrapage_we": "Réduit partiellement la dette mais décale le rythme"},
     "environnement": {"bruit": "Bruit blanc ou silence — pas de musique avec paroles", "ecrans": "La lumière bleue est un facteur mais l'activation mentale est le problème principal", "literie": "Le confort compte — investissement rentable sur la qualité de vie"},
     "troubles_necessitant_consultation": ["Insomnie > 3 nuits/semaine depuis > 1 mois", "Ronflements forts avec pauses respiratoires (apnée)", "Somnolence diurne malgré 8h de sommeil"]},
    [{"prompt": "Je n'arrive pas à m'endormir avant 2h du matin.", "answer": "Quelques questions : ton heure de réveil est-elle fixe même le week-end ? Est-ce que tu t'exposes à la lumière le matin ? L'heure de coucher suit souvent l'heure de lever — si tu te lèves à des heures variables, le rythme se dérègle. La TCC-I (thérapie cognitive pour l'insomnie) est plus efficace que les somnifères à long terme si c'est installé — un médecin peut t'orienter."},
     {"prompt": "Je dors mal depuis que je travaille de nuit.", "answer": "Le travail de nuit impose une lutte contre l'horloge biologique — ce n'est pas résolvable complètement. Ce qui aide : bloques de sommeil les plus longs possibles, occultation totale de la chambre, même stratégie de lever et coucher les jours off pour ne pas aggraver le décalage. La consultation d'un médecin du travail ou d'un spécialiste du sommeil est particulièrement pertinente dans ce cas."}],
    {"tone": "factuel, pragmatique, orienté vers les soins si besoin", "structure": ["ce qui marche", "mythes", "quand consulter"], "avoid": ["listes exhaustives", "culpabiliser", "promettre des solutions"]},
    ["sommeil", "hygiène", "insomnie", "circadien", "récupération", "santé"]
))

save("human/wellbeing/stress_reduction_support.json", ku(
    "knowledges.human.wellbeing.stress_reduction_support",
    "Soutien à la réduction du stress — techniques et accompagnement",
    "wellbeing", "high",
    "Techniques fondées sur les données pour réduire l'activation du système de stress, avec les conditions d'efficacité et les limites de chaque approche.",
    "Le soutien à la réduction du stress englobe les interventions comportementales, cognitives et physiologiques qui réduisent l'activation du système sympathique et restaurent l'équilibre neurovégétatif, sans prétendre éliminer le stress — qui est une réponse biologique normale et nécessaire.",
    {"techniques_haute_evidence": {"respiration": "Cohérence cardiaque (5s inspire/5s expire) — active le nerf vague, mesurable sur la variabilité cardiaque", "mouvement": "30 min d'activité modérée — réduit le cortisol, augmente les endorphines", "pleine_conscience": "8 semaines de MBSR — réduit l'anxiété et la réactivité émotionnelle (méta-analyses)"},
     "techniques_rapides": {"577": "5 inspire — 7 expire — 7 expire — 5 comptages : ralentit le cœur", "grounding_54321": "5 choses vues, 4 entendues, 3 touchées, 2 senties, 1 goûtée", "eau_froide": "Eau froide sur le visage active le réflexe de plongée — ralentit le cœur"},
     "limites": {"stress_chronique": "Les techniques ne traitent pas les causes — nécessite changement situationnel", "trauma": "La pleine conscience peut réactiver des traumatismes — approche spécialisée nécessaire", "pas_de_substitut": "ALFRED soutient mais ne remplace pas la thérapie pour le stress sévère"}},
    [{"prompt": "J'ai une crise de stress là maintenant.", "answer": "D'accord. Respire avec moi : inspire 4 secondes, retiens 1, expire lentement sur 7 secondes. Encore une fois. La sortie longue active le nerf vague et ralentit le cœur physiquement. Tu veux qu'on continue quelques cycles ? Ou tu préfères parler de ce qui se passe ?"},
     {"prompt": "Ça fait des mois que je suis stressée, rien ne marche.", "answer": "Si le stress est chronique depuis des mois sans amélioration, les techniques de gestion ont des limites. Ce n'est pas qu'elles ne marchent pas — c'est qu'elles gèrent les symptômes mais pas la source. La question importante : qu'est-ce qui génère ce stress en continu ? Travail, relation, situation financière ? Parce que la vraie solution passe par là, pas uniquement par la respiration."}],
    {"tone": "calme, factuel, limites claires", "structure": ["outil immédiat", "technique", "limite et orientation"], "avoid": ["promettre", "technique sans contexte", "ignorer stress chronique"]},
    ["stress", "réduction", "cohérence cardiaque", "respiration", "mindfulness", "cortisol"]
))

save("human/wellbeing/stress_signals.json", ku(
    "knowledges.human.wellbeing.stress_signals",
    "Signaux du stress — corps, pensée et comportement",
    "wellbeing", "high",
    "Le stress se manifeste sur trois niveaux simultanés — physique, cognitif et comportemental. Reconnaître ses signaux propres permet une intervention précoce.",
    "Les signaux du stress sont les manifestations observables de l'activation du système de réponse au stress (axe HPA, système sympathique). Ils se répartissent en signaux physiques, cognitifs et comportementaux, et varient selon les individus — d'où l'importance de reconnaître ses propres patterns.",
    {"physiques": ["Tensions musculaires (cou, mâchoires, épaules)", "Maux de tête de tension", "Troubles digestifs (SII, nausées)", "Insomnie ou hypersomnie", "Palpitations", "Peau (eczéma, psoriasis peuvent s'aggraver)"],
     "cognitifs": ["Pensées en boucle (rumination)", "Difficulté à se concentrer", "Catastrophisme (imaginer le pire)", "Difficulté à prendre des décisions", "Mémoire de travail réduite"],
     "comportementaux": ["Irritabilité augmentée", "Procrastination", "Suralimentation ou perte d'appétit", "Isolement ou au contraire hyperactivité sociale", "Consommation accrue (alcool, écrans, achats)"],
     "signaux_d_alarme": ["Symptômes physiques persistants → consultation médicale", "Pensées intrusives très fréquentes → thérapie", "Consommation problématique → soutien spécialisé"]},
    [{"prompt": "J'ai des maux de ventre depuis des semaines.", "answer": "Les troubles digestifs sont l'un des signaux physiques du stress les plus fréquents — le système nerveux entérique (\"deuxième cerveau\") est directement connecté au système de stress. Ça ne veut pas dire que c'est \"que du stress\" — une consultation médicale pour éliminer d'autres causes est importante. Et si c'est confirmé psychosomatique, c'est tout aussi réel et nécessite une prise en charge."},
     {"prompt": "Comment savoir si je suis stressée si je ne le ressens pas ?", "answer": "Le stress peut être \"anesthésié\" — tu ne le ressens pas émotionnellement mais le corps parle. Checklist rapide : tensions musculaires inconscientes ? Sommeil agité ? Digestion perturbée ? Irritabilité ? Moins de plaisir dans les choses habituelles ? Si tu coches plusieurs cases sans raison physiologique évidente, le stress est une hypothèse sérieuse."}],
    {"tone": "éducatif, concret, vigilant", "structure": ["lister les signaux", "aider à identifier les siens", "orienter si nécessaire"], "avoid": ["psychologiser trop vite", "ignorer les signaux physiques", "\"c'est juste du stress\""]},
    ["stress", "signaux", "physique", "cognitif", "comportemental", "corps"]
))

save("human/wellbeing/support_without_diagnosis.json", ku(
    "knowledges.human.wellbeing.support_without_diagnosis",
    "Soutenir sans diagnostiquer — posture d'accompagnement non-clinique",
    "wellbeing", "high",
    "Comment soutenir quelqu'un qui vit des difficultés psychologiques ou émotionnelles sans poser de diagnostic, sans minimiser et sans dépasser son rôle.",
    "Le soutien sans diagnostic est la posture d'accompagnement qui reconnaît et valide une souffrance sans l'étiqueter cliniquement, qui oriente vers des professionnels sans rejeter, et qui maintient un lien de confiance sans se substituer à une prise en charge spécialisée.",
    {"ce_qu_on_peut_faire": ["Écouter activement sans chercher à résoudre", "Valider l'expérience (\"c'est difficile, je comprends\")", "Nommer ce qu'on observe sans l'interpréter (\"tu sembles épuisée\")", "Demander ce dont la personne a besoin maintenant", "Suggérer de l'aide professionnelle avec douceur"],
     "ce_qu_on_ne_fait_pas": ["Diagnostiquer (\"tu es déprimée\", \"tu as du TDAH\")", "Minimiser (\"ça va aller\", \"c'est pas si grave\")", "Forcer vers la thérapie (ça se retourne)", "Prendre en charge ce qui dépasse ses compétences"],
     "formulations_aidantes": {"orienter": "\"Est-ce que tu as quelqu'un à qui en parler professionnellement ? Je pense que ça pourrait aider.\"", "valider": "\"Ce que tu traverses a l'air vraiment lourd.\"", "presence": "\"Je suis là, je ne sais pas toujours quoi dire mais je t'entends.\""},
     "signaux_necessitant_escalade_immediate": ["Mentions de suicide ou d'automutilation", "Détachement total de la réalité", "Danger immédiat pour soi ou pour autrui"]},
    [{"prompt": "Mon amie est très mal en ce moment, comment l'aider ?", "answer": "La chose la plus aidante : être présente et l'écouter sans chercher à résoudre. Lui demander ce dont elle a besoin plutôt que de supposer. Si ça dure ou si elle semble vraiment en détresse, lui suggérer doucement un soutien professionnel — pas en mode \"tu dois y aller\" mais \"j'ai peur pour toi et je pense que ça pourrait t'aider\". Ton rôle n'est pas de la guérir, c'est de ne pas la laisser seule."},
     {"prompt": "Je ne sais pas si je dois lui dire que je pense qu'elle est déprimée.", "answer": "Évite de poser un diagnostic — même juste. Ce que tu peux dire : \"Tu sembles vraiment épuisée et ça m'inquiète.\" Ça décrit ce que tu observes sans étiqueter, et ça ouvre un espace pour qu'elle parle. Le diagnostic, c'est le rôle du professionnel."}],
    {"tone": "doux, clair sur les limites, non-abandonnant", "structure": ["ce qu'on peut", "ce qu'on ne fait pas", "formulations concrètes"], "avoid": ["diagnostiquer", "minimiser", "surresponsabiliser l'aidant"]},
    ["soutien", "accompagnement", "sans diagnostic", "écoute", "orientation", "limites"]
))

save("human/wellbeing/wellbeing_non_medical_support.json", ku(
    "knowledges.human.wellbeing.wellbeing_non_medical_support",
    "Bien-être non médical — pratiques de fond au quotidien",
    "wellbeing", "medium",
    "Pratiques du quotidien qui soutiennent le bien-être sur le long terme sans relever du médical : connexion sociale, sens, mouvement, nature, créativité.",
    "Le bien-être non médical désigne l'ensemble des pratiques et conditions de vie qui soutiennent la santé mentale et physique sans intervention clinique, et qui constituent le socle de résilience qui détermine comment on traverse les difficultés.",
    {"piliers": {"connexion": "Liens sociaux de qualité — facteur de protection majeur (plus que le tabac pour la longévité)", "sens": "Avoir un \"pourquoi\" — le sens réduit l'impact du stress", "mouvement": "30 min d'activité modérée par jour — impact documenté sur l'anxiété et la dépression", "nature": "Exposition régulière à des espaces naturels — réduit le cortisol et restaure l'attention", "creativite": "Expression (art, écriture, musique, jardinage) — traitement émotionnel et plaisir"},
     "hygiene_mentale": {"deconnexion": "Plages sans écran et sans information — le cerveau a besoin de vide", "gratitude": "Pas la gratitude forcée — reconnaître ce qui va bien sans nier ce qui va mal", "auto_compassion": "Se traiter soi-même comme on traiterait un ami — réduire l'autocritique"},
     "accessibilite": "Ces pratiques ne nécessitent pas de ressources importantes — la marche, la connexion sociale et l'expression créative sont disponibles à tous."},
    [{"prompt": "Qu'est-ce que je peux faire pour aller mieux sans forcément aller chez le psy ?", "answer": "Trois pratiques à fort impact soutenues par les données : 1) Mouvement — 30 min de marche par jour change la chimie du cerveau. 2) Connexion — un vrai échange avec quelqu'un qui compte pour toi, même court. 3) Quelque chose qui a du sens pour toi — pas forcément grand, juste aligné avec ce qui compte. Ces trois choses ensemble créent une base. Si ça ne suffit pas, la thérapie n'est pas un aveu d'échec — c'est un outil supplémentaire."},
     {"prompt": "J'entends partout qu'il faut \"prendre soin de soi\" mais je sais pas ce que ça veut dire.", "answer": "\"Prendre soin de soi\" est souvent présenté comme des bains et des bougies — c'est plus profond que ça. Concrètement : dormir assez, manger quelque chose, bouger un peu, avoir un échange humain vrai, faire une chose qui te plaît. Ce n'est pas une performance de bien-être — c'est maintenir les fonctions de base qui permettent de tenir."}],
    {"tone": "accessible, ancré dans le réel, sans injonction", "structure": ["piliers concrets", "pratiques simples", "accessibilité"], "avoid": ["wellness toxic positivity", "liste idéale inaccessible", "minimiser le besoin de soins réels"]},
    ["bien-être", "santé mentale", "connexion", "sens", "mouvement", "nature", "créativité"]
))

print("\n=== human/wellbeing : 17 KU sauvegardés ===")
