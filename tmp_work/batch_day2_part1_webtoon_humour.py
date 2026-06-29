"""
Batch Day 2 — Part 1
  culture/webtoon/    : 10 fichiers
  human/humour/       : 10 fichiers
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(file_id, domain, subdomain, title, summary, core_def, knowledge, examples, tags, priority="medium"):
    return {
        "schema_version": "1.2", "type": "knowledge_unit",
        "id": f"knowledges.{domain}.{subdomain}.{file_id}",
        "title": title, "domain": domain, "subdomain": subdomain,
        "status": "validated", "priority": priority,
        "summary": summary, "core_definition": core_def,
        "knowledge": knowledge, "example_answers": examples,
        "response_guidance": {
            "tone": "enthousiaste, précis, ancré dans la culture source",
            "structure": ["contextualiser", "détailler", "recommander ou conseiller"],
            "avoid": ["généraliser", "confondre les cultures source", "être condescendant"]
        },
        "tags": tags, "related_knowledge_units": []
    }

# ═══════════════════════════════════════════════════════════════════════════
# CULTURE / WEBTOON  (10 fichiers)
# ═══════════════════════════════════════════════════════════════════════════

save("culture/webtoon/webtoon_overview.json", ku(
    "webtoon_overview", "culture", "webtoon",
    "Webtoon — format, histoire et essor mondial",
    "Le webtoon est une bande dessinée numérique native coréenne, lue verticalement sur smartphone. Né en 2003 avec Naver Webtoon, il est devenu le format de BD à la plus forte croissance mondiale et génère des adaptations en anime, drama et films.",
    "Le webtoon est un format de bande dessinée numérique originaire de Corée du Sud, caractérisé par un défilement vertical infini, une publication épisodique hebdomadaire, souvent gratuite avec monétisation par 'fast pass', et une prédominance des couleurs. Né sur les plateformes Naver et Daum, il a révolutionné la distribution mondiale de la BD.",
    {
        "history": {
            "2003": "Naver Webtoon lance la première plateforme dédiée en Corée",
            "2014": "LINE Webtoon lance internationalement — début de l'expansion mondiale",
            "2020-2024": "Boom des adaptations (Solo Leveling anime 2024, True Beauty drama K, Tower of God anime)"
        },
        "format_specs": {
            "scroll": "Vertical — optimisé pour le smartphone, pas la page",
            "episode_length": "40-80 panels en moyenne par épisode",
            "release_rhythm": "1 épisode par semaine en général",
            "color": "Couleur native — contrairement au manga noir/blanc",
            "free_model": "Lecture gratuite des anciens épisodes, fast-pass payant pour les récents"
        },
        "platforms": {
            "Naver Webtoon": "Plateforme originelle coréenne — 82M utilisateurs mensuels",
            "LINE Webtoon": "Version internationale de Naver",
            "Kakao Webtoon / Tapas": "Concurrent majeur — focus dramance et romance",
            "Lezhin Comics": "Webtoons adultes premium",
            "Delitoon / Izneo": "Plateformes francophones"
        },
        "genres_dominants": ["Romance (50%+ des lectures)", "Fantasy / isekai", "Action", "Horror", "Slice of life", "BL (Boys Love)"],
        "adaptation_pipeline": "Webtoon → Animé (Solo Leveling, Tower of God, Noblesse) → Drama coréen (True Beauty, Itaewon Class) → Film (rare mais en hausse)"
    },
    [
        {"prompt": "C'est quoi exactement un webtoon et en quoi c'est différent du manga ?",
         "answer": "Trois différences structurelles : (1) Format — le webtoon se lit verticalement en scrollant comme un fil Instagram, optimisé smartphone. Le manga est horizontal, en pages, souvent noir et blanc, (2) Origine — webtoon = Corée du Sud, manga = Japon. Deux industries distinctes avec leurs propres codes narratifs et visuels, (3) Distribution — le webtoon est né numérique et gratuit (modèle freemium). Le manga est né papier et reste majoritairement vendu en volume physique. Contenu : le webtoon domine en romance et fantasy isekai. Le manga a une diversité de genres plus large (seinen, shojo, horror, sports...)."},
        {"prompt": "Quelles plateformes pour lire des webtoons en français ?",
         "answer": "Options selon le budget : (1) Gratuit — LINE Webtoon (app ou web), le plus grand catalogue international traduit. Aussi Naver Webtoon avec quelques titres FR, (2) Premium — Delitoon et Izneo proposent des traductions françaises officielles de webtoons coréens populaires, avec système de crédits, (3) Légal mais coréen sub-titré — Tapas en anglais si tu lis anglais. Commencer par LINE Webtoon — l'app est fluide, le catalogue immense, et les 50+ premiers épisodes de chaque série sont souvent gratuits."}
    ],
    ["webtoon", "coréen", "manhwa", "scroll vertical", "Naver", "culture numérique"]
))

save("culture/webtoon/solo_leveling.json", ku(
    "solo_leveling", "culture", "webtoon",
    "Solo Leveling — manhwa et adaptation anime",
    "Solo Leveling est le manhwa le plus lu hors Corée de l'histoire — une power fantasy de chasseurs de donjons où le protagoniste le plus faible devient progressivement le plus puissant. L'adaptation anime 2024 par A-1 Pictures a confirmé son statut mondial.",
    "Solo Leveling (나 혼자만 레벨업, Na Honjaman Level-Up) est un manhwa de Chugong, illustré par Dubu, publié sur KakaoPage de 2018 à 2021 (179 chapitres). Il suit Sung Jinwoo, chasseur E-rang dans un monde où des portails ouvrent sur des donjons peuplés de monstres. Après quasi-mort dans un double donjon, il obtient le système unique de 'Shadow Monarch' lui permettant de progresser sans limites.",
    {
        "world_system": {
            "hunters": "Humains ayant éveillé des pouvoirs lors de l'apparition des Gates. Classés E à S.",
            "gates": "Portails vers des donjons remplis de monstres. Ferment naturellement après quelques jours.",
            "system": "Interface de RPG que Jinwoo seul peut voir — quêtes, stats, level up. Unique au monde.",
            "shadow_army": "Jinwoo peut extraire les ombres des monstres tués pour créer une armée de serviteurs."
        },
        "narrative_arc": "Progression de Jinwoo de rang E (le pire) à Shadow Monarch via une montée en puissance constante et satisfaisante. Boss principaux : Monarchs (entités cosmiques opposées aux Rulers).",
        "art_style": "Dubu (Kim Jong-jun) — art manhwa très cinématographique, combats dynamiques et lisibles, couleurs riches. Sa mort en 2022 a choqué la communauté.",
        "anime_2024": {
            "studio": "A-1 Pictures (Sword Art Online, Your Lie in April)",
            "reception": "Très positif — fidèle au manhwa, animation de qualité, bande-son mémorable",
            "saison2": "Saison 2 confirmée — arc Jeju Island et introduction des Monarchs"
        }
    },
    [
        {"prompt": "Par quoi commencer pour découvrir Solo Leveling — manhwa ou anime ?",
         "answer": "L'anime 2024 est un excellent point d'entrée : bien animé, fidèle, accessible sans connaissance préalable. 12 épisodes saison 1 = arc fondateur bien rythmé. Ensuite le manhwa pour la suite (179 chapitres, fin complète). L'avantage du manhwa : tu avances à ton rythme et la fin de l'histoire est disponible maintenant. L'anime rattrapera en saison 2 et 3. Si tu es déjà fan de fantasy RPG progression : commence directement le manhwa — la satisfaction de voir Jinwoo monter en puissance chapitre par chapitre est addictive."},
        {"prompt": "Pourquoi Solo Leveling est-il aussi populaire alors que l'histoire est simple ?",
         "answer": "La simplicité est précisément l'atout. Solo Leveling n'essaie pas d'être Attack on Titan — il perfectionne la power fantasy pure. Ce qui fonctionne : (1) La progression est constante et satisfaisante — chaque arc apporte une nouvelle montée de puissance visible, (2) Jinwoo est compétent sans être arrogant — il travaille, il s'améliore, il ne gagne pas par chance, (3) L'art de Dubu est parmi les meilleurs du medium — les combats sont lisibles et spectaculaires. Solo Leveling est l'équivalent BD d'un bon film d'action bien exécuté : pas la profondeur de Dostoïevski, mais 100% de ce qu'il promet."}
    ],
    ["Solo Leveling", "manhwa", "Sung Jinwoo", "power fantasy", "anime 2024", "Shadow Monarch"]
))

save("culture/webtoon/tower_of_god.json", ku(
    "tower_of_god", "culture", "webtoon",
    "Tower of God — webtoon épique de SIU",
    "Tower of God est l'un des premiers webtoons à avoir conquis une audience internationale massive. Publié depuis 2010 sur Naver par SIU (Slave in Utero), c'est une oeuvre de fantasy épique complexe où des milliers de participants grimpent une tour mystérieuse pour voir leurs voeux exaucés.",
    "Tower of God (신의 탑) est un webtoon de fantasy épique de SIU, publié sur Naver Webtoon depuis 2010 et toujours en cours. Il suit Twenty-Fifth Bam, un garçon qui entre dans la Tour pour retrouver son amie Rachel. La Tour contient des niveaux peuplés de créatures, de factions politiques et de compétitions où les participants grimpent pour obtenir richesse, pouvoir ou vœux exaucés.",
    {
        "world_complexity": "L'une des constructions de monde les plus élaborées du webtoon — factions (Zahard Empire, 10 Great Families, FUG), système de rangs (Regular / Irregular), tests par étages avec règles distinctes.",
        "bam_as_irregular": "Bam est un Irregular — entré dans la Tour sans invitation, ce qui est censé être impossible. Les Irregulars ont changé la Tour par le passé (roi Zahard lui-même était un Irregular).",
        "themes": ["Amitié et trahison (Rachel comme pivot central)", "Pouvoir et ses corruptions", "Identité — qui est vraiment Bam ?", "Systèmes d'oppression vs résistance"],
        "art_evolution": "L'art de SIU a évolué massivement depuis 2010 — les premiers chapitres sont visuellement datés mais le récit et le world-building compensent largement.",
        "anime": "Adapté en animé par Telecom Animation Film (2020, 13 épisodes saison 1). Reçu positivement pour l'introduction au webtoon. Saison 2 en production.",
        "hiatus": "SIU souffre de problèmes de santé chroniques (bursitis) qui ont causé plusieurs hiatus prolongés — sujet de frustration de la communauté mais aussi de solidarité."
    },
    [
        {"prompt": "Tower of God vaut-il le coup malgré les 700+ chapitres ?",
         "answer": "Oui, si tu as l'appétit pour un world-building complexe sur la durée. Ce qui compense les 700 chapitres : chaque arc introduit de nouvelles factions, règles et personnages qui enrichissent l'univers plutôt que de le diluer. Le pic narratif (arc Hell Train, arc Workshop Battle) est parmi ce qui se fait de mieux en webtoon épique. Point d'entrée recommandé : anime saison 1 (13 épisodes) pour tester, puis webtoon depuis le début. Les 80 premiers chapitres sont lents mais fondateurs — le récit décolle vraiment à partir du Submerged Fish Arc."},
        {"prompt": "Qui est Rachel dans Tower of God et pourquoi les fans la détestent-ils ?",
         "answer": "Rachel est l'amie de Bam, la raison pour laquelle il entre dans la Tour. Sans spoiler excessif : elle commet une trahison au chapitre 78 qui est l'un des moments les plus choquants du webtoon — au point où les fans lui ont dédié un hashtag de haine qui a atteint Twitter mondial. SIU a intentionnellement construit son personnage comme une déconstruction du 'personnage spécial' — elle veut être l'héroïne de sa propre histoire et fait des choix moralement inacceptables pour ça. Certains lecteurs l'apprécient pour sa complexité, la majorité la déteste viscéralement. Divisif = réussi narrativement."}
    ],
    ["Tower of God", "SIU", "fantasy", "Naver Webtoon", "Bam", "épique"]
))

save("culture/webtoon/omniscient_reader.json", ku(
    "omniscient_reader", "culture", "webtoon",
    "Omniscient Reader's Viewpoint — webtoon méta-narratif",
    "Omniscient Reader's Viewpoint (ORV) est considéré par beaucoup comme le meilleur webtoon jamais écrit — une oeuvre méta-narrative où le seul lecteur d'un roman de fin du monde le voit se réaliser, et doit utiliser sa connaissance du texte pour survivre.",
    "Omniscient Reader's Viewpoint (전지적 독자 시점) est un webtoon coréen adapté du roman web de singNsong (Sing Shong), illustré par Sleepy-C, publié depuis 2020. Il suit Kim Dokja, salaryman qui a lu pendant 10 ans le roman web 'Ways of Survival' — et qui voit le monde réel basculer dans le scénario du roman. Sa connaissance du texte est son seul avantage.",
    {
        "meta_narrative": "ORV est une oeuvre sur la lecture elle-même — la relation entre lecteur et fiction, le pouvoir des histoires, ce que signifie être le protagoniste vs être le lecteur. Kim Dokja n'est pas le héros prévu — c'est le lecteur qui doit s'improviser acteur.",
        "world_system": "Des 'scénarios' s'activent dans le monde réel — missions imposées à l'humanité avec récompenses et punitions. Des 'constellations' (êtres mythologiques) parient sur les humains et les sponsorisent comme des dieux grecs.",
        "themes": [
            "La puissance et la limite de la connaissance (savoir le futur ne suffit pas)",
            "L'identité — qui est-on quand on cesse d'être spectateur ?",
            "L'amitié et le sacrifice dans un monde où chaque décision a un prix",
            "La méta-fiction : qu'est-ce qu'une histoire ? qui décide qui est le héros ?"
        ],
        "why_so_praised": "ORV réussit à être simultanément une power fantasy satisfaisante, une méditation sur la narration, et une histoire d'amitié profonde. La croissance de Kim Dokja de salaryman solitaire à figure centrale d'un monde en ruine est émotionnellement dévastatrice.",
        "status": "Webtoon complet — roman web original aussi disponible (traduit en anglais et partiellement en français)"
    },
    [
        {"prompt": "C'est quoi Omniscient Reader et par où commencer ?",
         "answer": "ORV est le webtoon le plus acclamé par les connaisseurs — pas le plus populaire grand public (moins accessible que Solo Leveling au premier abord), mais celui que les lecteurs citent comme transformateur. L'histoire : Kim Dokja a lu pendant 10 ans un roman web impopulaire appelé 'Ways of Survival'. Le jour de la fin, le monde bascule dans le scénario du roman. Il est le seul à en connaître l'histoire. Par où commencer : le webtoon (illustré, lisible) est le meilleur point d'entrée. Le roman web original va encore plus loin en profondeur. Si tu aimes les récits qui jouent avec la méta-fiction et les personnages complexes — c'est probablement le meilleur webtoon existant."},
        {"prompt": "Pourquoi ORV est-il aussi émotionnel comparé aux autres webtoons d'action ?",
         "answer": "Parce que singNsong s'est intéressé à ce que ressentent les personnages secondaires — dans la plupart des power fantasy, les alliés sont des fonctions narratives. Dans ORV, chaque membre de l'équipe de Kim Dokja a une histoire propre, des sacrifices réels, une relation à la mort unique. Et Kim Dokja lui-même est un personnage habituellement invisible dans ce type de récit : le lecteur passionné, solitaire, qui n'était rien avant la catastrophe. La douleur et la joie de ce personnage résonnent avec quiconque s'est jamais senti plus à l'aise dans la fiction que dans la réalité."}
    ],
    ["Omniscient Reader", "ORV", "méta-narratif", "Kim Dokja", "webtoon coréen", "philosophie fiction"]
))

save("culture/webtoon/webtoon_romance.json", ku(
    "webtoon_romance", "culture", "webtoon",
    "Webtoon romance — genre dominant et codes",
    "La romance est le genre le plus lu sur les plateformes webtoon, représentant 50-60% des lectures. Elle a développé ses propres codes (CEO romance, revenge arc, reincarnation romance) et produit des titres avec des dizaines de millions de lecteurs.",
    "Le webtoon de romance est le sous-genre le plus populaire de la plateforme, caractérisé par des romances souvent contemporaines ou en fantasy, des protagonistes féminins actifs (évolution du 'damsel in distress'), et des arcs narratifs de vengeance, réincarnation ou second chance. Il cible principalement un public féminin adulte et adolescent.",
    {
        "dominant_tropes": [
            {"trope": "CEO / Chaebol romance", "description": "Homme riche et puissant + protagoniste ordinaire — le Cendrillon modern coréen"},
            {"trope": "Reincarnation / regression", "description": "Protagoniste qui revit une vie précédente avec la mémoire du futur — très populaire en fantasy romantique"},
            {"trope": "Revenge arc", "description": "Protagoniste trahi(e) qui revient pour se venger avec style — satisfaction narrative garantie"},
            {"trope": "Villainess rehabilitation", "description": "Réincarné(e) dans le corps de la vilaine du roman — doit changer son destin"},
            {"trope": "Enemies to lovers", "description": "Tension romantique via antagonisme initial — tension sexuelle par opposition"},
            {"trope": "Fake relationship / contract marriage", "description": "Relation feinte qui devient réelle — comédie romantique classique webtoon"}
        ],
        "key_titles": [
            "True Beauty (Yaongyi) — lycéenne qui utilise le maquillage pour masquer sa vraie apparence",
            "I Love Yoo (Quimchee) — slice of life romance américaine sur Webtoon",
            "The Remarried Empress — revenge romance fantasy en costumes",
            "Lore Olympus — mythologie grecque en romance moderne, esthétique pastel iconique",
            "My Dear Cold-Blooded King — romance historique fantasy",
            "What's Wrong with Secretary Kim — CEO romance comédie"
        ],
        "reading_demographics": "70%+ de lectrices. Le webtoon romance touche 15-35 ans principalement. Le BL (Boys Love) est un sous-genre distinct très populaire."
    },
    [
        {"prompt": "Quels webtoons de romance recommandes-tu pour commencer ?",
         "answer": "Par profil : (1) Tu aimes les romcoms légères — True Beauty ou What's Wrong with Secretary Kim : humour, romance, personnages attachants, (2) Tu aimes la fantasy romantique — Lore Olympus (mythologie grecque réinterprétée, esthétique très originale) ou The Remarried Empress (vengeance + romance épique), (3) Tu aimes le drama émotionnel — I Love Yoo de Quimchee : slice of life américaine avec des relations complexes, très appréciée pour ses personnages. Toutes disponibles gratuitement sur LINE Webtoon. La romance webtoon est souvent plus directe émotionnellement et visuellement que le manga shojo — si tu aimes le format scroll, ça s'adapte très vite."},
        {"prompt": "Pourquoi le trope de la réincarnation est-il aussi populaire dans les webtoons ?",
         "answer": "Plusieurs ressorts psychologiques : (1) Fantasme de recommencement avec avantage — refaire sa vie en sachant ce qu'on sait maintenant, (2) Satisfaction narrative de la vengeance — si tu as été trahi(e) dans ta vie précédente, tu peux changer le cours des événements, (3) La protagoniste a de l'agentivité réelle — elle n'est pas passive, elle a un plan. C'est une réponse aux romances où les protagonistes subissent, (4) World-building facile — dans un monde fantasy médiéval, les codes sociaux (mariage arrangé, noblesse) créent automatiquement des conflits romantiques. Ce n'est pas de la paresse narrative — c'est un genre codifié comme le romance contemporain ou le thriller."}
    ],
    ["webtoon romance", "CEO romance", "réincarnation", "Lore Olympus", "True Beauty", "tropes"]
))

save("culture/webtoon/webtoon_horror_thriller.json", ku(
    "webtoon_horror_thriller", "culture", "webtoon",
    "Webtoon horreur et thriller — le format qui effraie autrement",
    "Le format scroll vertical du webtoon crée une expérience d'horreur unique — le rythme de dévoilement est contrôlé par le doigt du lecteur, amplifiant la tension. Bastian Vive, Sweet Home et Cursed Princess Club ont démontré la puissance du medium pour l'horreur.",
    "Le webtoon d'horreur exploite les spécificités du format vertical et de la couleur pour créer une tension narrative que le manga noir/blanc ne peut reproduire. Le scroll lent avant une révélation, les couleurs saturées du sang ou au contraire désaturées pour l'angoisse, sont des outils propres au medium.",
    {
        "format_horror_advantages": [
            "Le scroll contrôle le rythme de révélation — le lecteur décide quand voir ce qui vient après",
            "La couleur amplifie la violence ou la peur (rouge sang sur fond blanc, bleu mortifère)",
            "Les panneaux larges horizontaux créent des révélations choc lors du scroll",
            "Pas de découpage de page — l'horreur peut s'étirer sur un scroll long et lent"
        ],
        "key_titles": [
            {"title": "Sweet Home", "author": "Carnby Kim / Youngchan Hwang", "description": "Humains se transforment en monstres représentant leurs désirs refoulés. Adapté en série Netflix.", "tone": "Horreur psychologique + survival + questionnement humanité"},
            {"title": "Bastian Vive (Bastian Vive's Webtoon)", "author": "Artiste espagnol", "description": "Anthologie d'horreur format court — vignettes choc sur Webtoon. Très viral sur TikTok.", "tone": "Horreur absurde, choc visuel"},
            {"title": "The Gamer", "author": "Sung San-Young", "description": "Pas horreur mais thriller — monde où chaque personne a des stats RPG visibles"},
            {"title": "Cursed Princess Club", "author": "LambCat", "description": "Déconstruction douce et touchante des clichés de princesses — plus humour qu'horreur mais subversif"}
        ],
        "tiktok_horror_webtoons": "De nombreux webtoons courts d'horreur sont devenus viraux sur TikTok via des compilations — créant un pont entre la culture short-form et le format webtoon. Bastian Vive est l'exemple le plus frappant."
    },
    [
        {"prompt": "Quels webtoons d'horreur recommandes-tu ?",
         "answer": "Par intensité : (1) Horreur légère / déconstruction — Cursed Princess Club : drôle, touchant, subversif sur les clichés de princesses. Accessible à tous, (2) Horreur psychologique — Sweet Home : transformation des humains en monstres représentant leurs désirs. Profond et violent. Adaptée en série Netflix, (3) Horreur choc / anthologie — chercher Bastian Vive sur Webtoon ou ses compilations TikTok. Format court, impact immédiat. Sur LINE Webtoon, le filtre 'Horror' donne accès à un catalogue immense avec ratings communautaires. Commencer par les titres 'Editor's Pick' dans ce genre."},
        {"prompt": "Pourquoi le scroll vertical est-il particulièrement efficace pour l'horreur ?",
         "answer": "Parce que le lecteur contrôle la révélation. Dans un manga ou une BD papier, tu vois souvent la case suivante avant d'être prêt — ton oeil balaye la page. Dans un webtoon en scroll, le rythme de dévoilement est littéralement entre tes doigts. Les auteurs d'horreur webtoon conçoivent leurs révélations pour ce rythme : un long scroll vide ou avec une construction angoissante, puis la révélation au moment où tu arrives en bas. C'est l'équivalent de la scène qui monte en musique au cinéma — mais avec ton propre rythme de défilement comme tempo."}
    ],
    ["webtoon horreur", "Sweet Home", "Bastian Vive", "thriller", "scroll vertical", "Netflix"]
))

save("culture/webtoon/webtoon_creation.json", ku(
    "webtoon_creation", "culture", "webtoon",
    "Créer un webtoon — outils, format et publication",
    "La création de webtoon est plus accessible que le manga traditionnel — outils numériques, publication directe sur plateformes, audience mondiale dès le premier épisode. Le format a créé une génération d'auteurs indépendants qui monétisent directement leur travail.",
    "La création de webtoon est une pratique artistique numérique utilisant des outils de dessin digital (Clip Studio Paint, Procreate, Photoshop) pour produire des bandes dessinées verticales colorées publiées directement sur des plateformes mondiales, sans intermédiaire éditorial traditionnel.",
    {
        "tools": [
            {"tool": "Clip Studio Paint", "use": "Standard industrie — storyboard, dessin, couleurs, export", "price": "Abonnement ou achat"},
            {"tool": "Procreate (iPad)", "use": "Très populaire pour le croquis et la couleur rapide", "price": "Achat unique ~13€"},
            {"tool": "MediBang Paint", "use": "Gratuit, léger, cloud — bon départ pour débutant", "price": "Gratuit"},
            {"tool": "Canva Pro / Adobe Express", "use": "Mise en page et textes si on utilise l'IA pour les illustrations", "price": "Freemium"}
        ],
        "format_specs": {
            "width": "800px recommandé (LINE Webtoon) jusqu'à 1280px max",
            "episode_height": "Variable — typiquement 15 000 à 40 000px de hauteur",
            "file_format": "JPG ou PNG, RGB",
            "panel_rhythm": "Alterner panels larges (impact) et étroits (dialogue/transition)"
        },
        "publication_options": [
            {"platform": "LINE Webtoon Canvas", "model": "Gratuit, auto-publication, monétisation après seuil d'abonnés", "audience": "Mondiale"},
            {"platform": "Tapas", "model": "Auto-pub, crédits payants lecteurs, bonne communauté anglophone", "audience": "USA/monde anglophone"},
            {"platform": "Naver Webtoon Challenge", "model": "Tremplin vers la publication officielle Naver", "audience": "Corée puis monde"}
        ],
        "ai_assistance": "De nombreux créateurs utilisent l'IA générative (Midjourney, Stable Diffusion) pour les décors et arrière-plans, se concentrant sur les personnages et les expressions dessinés manuellement."
    },
    [
        {"prompt": "Comment commencer à créer un webtoon quand on n'a jamais dessiné professionnellement ?",
         "answer": "Chemin minimal viable : (1) Outils — MediBang Paint gratuit sur tablette Android ou iPad + stylet basique, (2) Apprendre — YouTube est la meilleure ressource. Chercher 'how to make webtoon' ou 'webtoon tutorial Clip Studio'. Les tutoriels de Natalia Madej ou de Make-it-Rain couvrent tout le pipeline, (3) Premier épisode — commencer petit : 20-30 panels, histoire courte, style simplifié assumé. Les webtoons populaires comme Cursed Princess Club ont commencé avec un style très basique, (4) Publier — LINE Webtoon Canvas accepte tout le monde. Publier tôt, itérer vite. L'audience vient avec la régularité, pas avec la perfection initiale."},
        {"prompt": "Peut-on monétiser un webtoon en France ?",
         "answer": "Oui, plusieurs voies : (1) LINE Webtoon Canvas — programme de monétisation dès 1000 abonnés et 40 000 vues sur 60 jours. Revenus via publicités et 'Daily Pass' sur les vieux épisodes, (2) Tapas — crédits achetés par les lecteurs pour débloquer les épisodes premium, (3) Patreon / Ko-fi — abonnement direct de fans pour contenu exclusif, épisodes en avance, (4) Merchandise — prints, goodies via Redbubble ou Etsy si l'audience est suffisante. Les revenus webtoon sont modestes au début mais croissent avec l'audience. Les auteurs coréens stars de Naver gagnent des millions mais c'est l'exception."}
    ],
    ["créer webtoon", "Clip Studio", "publication", "monétisation", "LINE Canvas", "dessin numérique"]
))

save("culture/webtoon/manhwa_romance_fantasy.json", ku(
    "manhwa_romance_fantasy", "culture", "webtoon",
    "Manhwa romance fantasy — villainess et réincarnation",
    "Le manhwa romance fantasy est un sous-genre à part entière : protagoniste réincarnée dans un roman de fantasy qu'elle a lu, souvent dans le corps de la vilaine. Ces oeuvres mélangent vengeance, romance et déconstruction des clichés de fantasy avec un humour caractéristique.",
    "Le manhwa romance fantasy est un genre hybride caractérisé par la combinaison de méchaniques d'isekai/réincarnation (protagoniste transportée dans un roman fantasy qu'elle connaît par coeur), de romance épique avec des love interests multiples, et de dynamiques de vengeance ou de survie dans un monde médiéval-fantastique.",
    {
        "core_mechanic": "La protagoniste se réveille dans le corps d'un personnage d'un roman qu'elle a lu — souvent la vilaine, parfois un personnage mineur. Elle connaît le futur et doit naviguer pour survivre ou changer le cours de l'histoire.",
        "key_titles": [
            {"title": "The Remarried Empress", "description": "Impératrice trahie qui divorce avec dignité et refait sa vie. Figure d'empowerment féminin massivement populaire."},
            {"title": "I Became the Villain's Own Daughter", "description": "Petite fille réincarnée dans le corps de la fille d'un villain — l'apprivoiser est le coeur du récit."},
            {"title": "Who Made Me a Princess", "description": "Femme réincarnée en princesse d'un roman — avec un père froid et distant qu'elle doit conquérir. Hit emotionnel."},
            {"title": "Lady Baby", "description": "Femme réincarnée en bébé pour prévenir le massacre de sa famille."},
            {"title": "The Villainess Reverses the Hourglass", "description": "Vilaine qui remonte le temps pour prendre sa revanche avec intelligence plutôt qu'avec violence."}
        ],
        "appeal": [
            "Protagonistes actives et intelligentes — pas de 'chosen one' passive",
            "Romance épique avec love interests bien écrits (souvent 2-3 candidates)",
            "Humour récurrent autour de la méta-connaissance du roman",
            "Satisfaction de la vengeance élégante vs violence brute",
            "Costumes et visuels somptueux — la fantasy médiévale se prête à l'esthétique"
        ]
    },
    [
        {"prompt": "Par quel manhwa romance fantasy commencer si je n'ai jamais lu ce genre ?",
         "answer": "Deux entrées parfaites : (1) Who Made Me a Princess — émotionnellement accessible, histoire père-fille touchante avant la romance, art magnifique. Pas trop long, bien rythmé. Disponible sur LINE Webtoon et Tapas, (2) The Remarried Empress — figure d'empowerment clairement dessinée, humour mordant, vengeance satisfaisante. Plus dense mais très gratifiant. Éviter de commencer par les titres très longs (The Beginning After the End fait 200+ chapitres) — commencer par des oeuvres de 80-150 chapitres pour calibrer son intérêt pour le genre avant d'investir dans un monstre."},
        {"prompt": "Qu'est-ce que le trope de la 'villainess' et pourquoi est-il si populaire ?",
         "answer": "La villainess est le personnage féminin antagoniste du roman original — envieuse, cruelle, destinée à être vaincue. Quand la protagoniste se réincarne dans son corps, elle a deux options : répéter le destin ou changer. L'attrait : (1) La vilaine a souvent plus de personnalité que l'héroïne fade du roman original, (2) La réhabilitation d'un personnage 'mauvais' est narrativement satisfaisante, (3) La méta-connaissance crée de l'humour — la protagoniste doit jouer le rôle tout en essayant de l'éviter. Ce trope est une réponse aux héroïnes passives de la romance classique — la villainess est active, pragmatique, et refuse son destin."}
    ],
    ["manhwa", "romance fantasy", "villainess", "réincarnation", "The Remarried Empress", "Korean webtoon"]
))

save("culture/webtoon/webtoon_bl_genre.json", ku(
    "webtoon_bl_genre", "culture", "webtoon",
    "BL (Boys Love) webtoon — genre et culture",
    "Le Boys Love (BL) est l'un des genres les plus populaires du webtoon, avec une audience massivement féminine. Il a développé ses propres codes narratifs, ses tropes canoniques et une culture de fan très active, notamment via les adaptations en drama thaïlandais et coréen.",
    "Le Boys Love (BL) dans le webtoon coréen est un genre de romance entre personnages masculins, lu principalement par des femmes, qui a évolué de la simple romance vers des récits incluant des dramas sociaux, des thèmes d'identité et d'acceptation. Les adaptations en drama live thaïlandais (GMMTV) et coréens ont créé une vague internationale majeure.",
    {
        "history": "Né dans le manga shojo japonais (yaoi), le BL webtoon coréen a développé ses propres codes visuels et narratifs distincts du yaoi japonais. Plus ancré dans le contemporain coréen, les personnages sont plus 'réalistes' physiquement.",
        "key_tropes": [
            "Enemies to lovers (antagonisme puis romance)",
            "Campus / vie universitaire ou lycée",
            "Secret relationship (relation cachée)",
            "Alpha/Beta/Omega (ABO dynamics — biologie fantasy)",
            "Contract relationship (relation contractuelle qui devient réelle)"
        ],
        "key_titles": [
            {"title": "Semantic Error", "description": "Étudiants polaraires forcés de collaborer — devenu drama coréen très populaire"},
            {"title": "The Guy Next Door", "description": "Slice of life BL contemporain, très apprécié pour ses personnages nuancés"},
            {"title": "Never Understand", "description": "BL mature sur des adultes — relations complexes"},
            {"title": "19 Days (not BL officiel)", "description": "Manhua chinois slice of life/BL — l'un des plus lus au monde"}
        ],
        "thai_drama_connection": "GMMTV (Thaïlande) a adapté de nombreux romans BL thaïlandais en dramas (2gether, Bad Buddy, Only Friends) — créant un pont entre la littérature BL et le drama asiatique grand public."
    },
    [
        {"prompt": "C'est quoi le BL et quelle est son audience réelle ?",
         "answer": "Le BL (Boys Love) est un genre de romance entre hommes, écrit et lu très majoritairement par des femmes. L'audience réelle : études coréennes montrent 75-80% de lectrices. Ce n'est pas contradictoire — le genre offre un espace de romance sans les dynamiques de genre hétéronormées traditionnelles (pas de 'femme passive / homme actif'). Les deux protagonistes sont dynamiques. Ce genre est mainstream en Asie de l'Est — pas niche. Les dramas BL thaïlandais (Bad Buddy, 2gether) ont des audiences de plusieurs millions. En France, Meian Éditions publie des manhwas BL traduits avec un catalogue croissant."},
        {"prompt": "Par où commencer si on veut découvrir le BL webtoon ?",
         "answer": "Deux points d'entrée accessibles : (1) Semantic Error (disponible sur Lezhin Comics ou Ridibooks, drama sur Viki) — romance universitaire entre un génie rigide et un étudiant populaire. Récit bien construit, humour, pas explicite. Le drama coréen en fait un très bon résumé, (2) 19 Days de Old Xian (manhua chinois, gratuit en ligne) — slice of life qui commence comme comédie et évolue vers le BL de façon très douce. Accessible à ceux qui ne lisent jamais ce genre. Éviter les titres très explicites (Lezhin a une section adult-rated) comme point d'entrée — commencer par les titres 'Teen' ou 'Mature (non-explicit)'."}
    ],
    ["BL", "Boys Love", "webtoon", "romance", "drama thaïlandais", "Semantic Error"]
))

save("culture/webtoon/webtoon_vs_manga_industry.json", ku(
    "webtoon_vs_manga_industry", "culture", "webtoon",
    "Industrie webtoon vs industrie manga — économie et influence",
    "Le webtoon a transformé l'économie de la BD asiatique en passant d'un modèle éditorial papier à un modèle numérique direct-to-consumer. En 2023, le marché webtoon mondial dépasse 3 milliards de dollars et continue de croître, menaçant la suprématie commerciale du manga hors Japon.",
    "L'industrie webtoon et l'industrie manga représentent deux modèles économiques distincts : le manga repose sur des maisons d'édition (Shueisha, Kodansha, Shogakukan) qui contrôlent la publication et les droits, tandis que le webtoon s'est construit sur des plateformes numériques à accès direct (Naver, Kakao, LINE), permettant une monétisation plus directe pour les auteurs.",
    {
        "market_comparison": {
            "manga_market_2023": "~7 milliards USD (Japon + export) — marché mature, croissance stable",
            "webtoon_market_2023": "~3.7 milliards USD — croissance 30%+ par an",
            "france_specificite": "La France est le 2e marché manga mondial et commence à développer un marché webtoon en français via Delitoon, Izneo, et des traductions officielles."
        },
        "author_economics": {
            "manga": "L'auteur reçoit des droits d'auteur (royalties) sur les ventes de volumes. Les grands auteurs (Oda, Isayama) sont multimillionnaires. Les débutants gagnent peu.",
            "webtoon_naver_official": "Les auteurs officiels Naver reçoivent un minimum garanti + % des revenus publicitaires et premium. Les top auteurs gagnent plus de 1M USD/an.",
            "webtoon_canvas": "Publication indépendante — revenus uniquement si l'audience est suffisante pour déclencher la monétisation."
        },
        "content_ownership": "Controverse majeure : certains contrats Webtoon Inc. (propriété de Naver) ont été critiqués pour retenir les droits des oeuvres publiées sur Canvas. Le manga japonais garde en général les droits à l'auteur (avec licence à l'éditeur).",
        "global_influence": "Le webtoon influence maintenant le manga — LINE Manga est une plateforme majeure au Japon. Des auteurs japonais publient en format webtoon. L'hybridation est en cours."
    },
    [
        {"prompt": "Le webtoon va-t-il remplacer le manga ?",
         "answer": "Non — ils coexisteront et s'influenceront. Ce qui distingue leur positionnement : (1) Le manga a 80 ans d'héritage culturel profond au Japon et dans le monde — il ne disparaît pas, (2) Le webtoon a un avantage structurel sur mobile (format optimisé smartphone), ce qui favorise les marchés émergents où le smartphone est l'écran principal, (3) Les deux s'interpénètrent — des webtoons sont adaptés en anime japonais (Tower of God, Solo Leveling), des mangakas publient en format webtoon. Ce n'est pas une guerre — c'est une convergence. Le marché global de la BD asiatique s'agrandit, profitant aux deux formats."},
        {"prompt": "Est-ce que les auteurs webtoon gagnent bien leur vie ?",
         "answer": "Très variable — comme partout dans la création : (1) Top tier Naver/Kakao officiel — oui, très bien. Les auteurs de hits comme Solo Leveling ont gagné plusieurs millions en droits d'adaptation (anime, drama, jeu vidéo), (2) Milieu — un auteur officiel avec audience stable peut vivre confortablement, (3) Canvas / indépendant — revenus faibles jusqu'à une audience très importante. La monétisation Canvas démarre à 1000 abonnés mais les revenus réels arrivent à partir de 50-100k. La réalité : les histoires de réussite webtoon sont réelles mais représentent une minorité — comme pour tout contenu créatif numérique."}
    ],
    ["industrie webtoon", "manga vs webtoon", "marché", "Naver", "économie créative", "droits auteur"]
))

# ═══════════════════════════════════════════════════════════════════════════
# HUMAN / HUMOUR  (10 fichiers)
# ═══════════════════════════════════════════════════════════════════════════

def kuh(file_id, title, summary, core_def, knowledge, examples, tags, priority="high"):
    return ku(file_id, "human", "humour", title, summary, core_def, knowledge, examples, tags, priority)

save("human/humour/humour_mecanismes.json", kuh(
    "humour_mecanismes",
    "Mécanismes du rire — pourquoi c'est drôle",
    "Le rire naît de la résolution d'une incongruité, d'une violation bénigne ou d'une supériorité perçue. Comprendre ces mécanismes permet de construire des blagues qui fonctionnent — et de comprendre pourquoi certaines tombent à plat.",
    "Les mécanismes du rire désignent les processus cognitifs et sociaux qui déclenchent la réponse comique. Les trois théories fondamentales — incongruité (Kant/Schopenhauer), supériorité (Hobbes/Platon), soulagement (Freud/Spencer) — expliquent la plupart des formes d'humour en opérant souvent simultanément.",
    {
        "three_theories": [
            {
                "theory": "Incongruité (la plus validée)",
                "mechanism": "Le rire naît de la résolution d'une tension entre deux cadres de référence incompatibles — la chute révèle un sens inattendu qui résout l'incongruité",
                "example": "Chute de blague : 'Je vais au médecin parce que j'avale des pièces depuis 3 ans. — Et là tu changes d'avis ?' La chute résout l'incongruité de façon inattendue"
            },
            {
                "theory": "Supériorité (Hobbes)",
                "mechanism": "On rit de la chute, de la maladresse, de la stupidité de l'autre — sentiment soudain de supériorité",
                "example": "Schadenfreude — rire de quelqu'un qui glisse sur une peau de banane"
            },
            {
                "theory": "Soulagement (Freud)",
                "mechanism": "Le rire libère une tension psychique accumulée — humour noir, blagues sur la mort ou le sexe libèrent la pression sociale",
                "example": "Les blagues dans les métiers à stress élevé (médecins urgentistes, pompiers) — humour noir comme valve de décompression"
            }
        ],
        "benign_violation_theory": {
            "source": "Peter McGraw & Joel Warner, The Humor Code (2014)",
            "formula": "Quelque chose est drôle quand : (1) c'est une violation (moral, physique, social) ET (2) cette violation est perçue comme bénigne (pas de vrai danger/dommage). Si un seul critère — pas drôle.",
            "applications": [
                "Trop menaçant (violence réelle) = pas drôle",
                "Trop bénin (rien ne viole rien) = pas drôle non plus",
                "Zone d'humour : juste au bon niveau de menace perçue-mais-sans-danger"
            ]
        },
        "timing_and_delivery": "Le même contenu dit avec un timing parfait vs raté = différence totale. Le timing comique est l'espace entre la mise en place et la chute — ni trop court (pas de tension), ni trop long (tension qui retombe)."
    },
    [
        {"prompt": "Pourquoi certaines blagues font-elles rire tout le monde et d'autres personne ?",
         "answer": "Trois variables : (1) Incongruité calibrée — la chute doit être surprenante mais compréhensible. Si trop prévisible, plus de surprise. Si trop absurde, la résolution cognitive est impossible et le rire ne vient pas, (2) Bénignité partagée — ce qui est 'bénignement violant' varie selon la culture, l'expérience et le contexte. Une blague d'humour noir est drôle entre médecins urgentistes qui vivent avec la mort — et choquante dans un contexte différent, (3) Timing et delivery — le même contenu raté à l'oral tombe à plat. Le rire est autant dans la performance que dans le contenu. C'est pour ça qu'une blague expliquée ne fait jamais rire : on perd la tension de l'incongruité."},
        {"prompt": "Est-ce qu'on peut apprendre à être drôle ?",
         "answer": "Oui — avec les bonnes pratiques. Ce qui s'améliore avec l'entraînement : (1) Observer les incongruités du quotidien — les gens drôles naturellement font ça instinctivement. Exercice : noter chaque jour 3 choses absurdes ou incongrues observées, (2) Timing — se regarder sur vidéo et identifier quand les pauses sont mal placées, (3) Structure de blague — apprendre la structure classique (mise en place / chute) puis la subvertir. Ce qui ne s'enseigne pas aussi facilement : l'authenticité. Un humour forcé ou calculé se sent. Les gens les plus drôles parlent de ce qui les étonne vraiment — pas de ce qu'ils pensent devoir être drôle."}
    ],
    ["humour", "rire", "incongruité", "timing", "théorie comique", "Peter McGraw"]
))

save("human/humour/autodérision.json", kuh(
    "autodérision",
    "Autodérision — se moquer de soi avec intelligence",
    "L'autodérision est la forme d'humour la plus socialement sûre et la plus puissante relationnellement — elle signale confiance en soi, absence de prétention et capacité à ne pas se prendre au sérieux. Mais mal dosée, elle peut signaler de la fausse modestie ou de la fragilité.",
    "L'autodérision est la capacité à se moquer de ses propres défauts, erreurs ou situations embarrassantes avec légèreté et détachement. Elle se distingue de l'auto-dépréciation (qui signale une vraie blessure) par la présence de distance émotionnelle réelle — on rit DE la situation, pas de soi dans un acte de punition symbolique.",
    {
        "social_function": [
            "Crée de la connexion immédiate — signale 'je ne me prends pas au sérieux'",
            "Neutralise les attaques — si tu te moques de toi en premier, l'attaque de l'autre perd son pouvoir",
            "Signale confiance en soi réelle — seul quelqu'un sûr de lui peut se permettre de rire de ses faiblesses",
            "Humanise les figures d'autorité — le manager qui rit de ses erreurs est plus accessible"
        ],
        "autodérision_vs_auto_dépréciation": {
            "autodérision": "Je ris d'une situation ou d'une erreur depuis une position de force. 'J'ai mis 20 minutes à assembler une étagère IKEA — le manuel disait 10 min. J'en suis très fier.'",
            "auto_dépréciation": "Je me blesse pour obtenir de la validation. 'Je suis vraiment nul, tout le monde y arrive sauf moi.' → malaise chez l'interlocuteur qui doit compenser"
        },
        "calibration": {
            "bon_dosage": "Se moquer de comportements, erreurs, traits — pas de valeurs fondamentales ou d'identité",
            "sujets_ok": "Maladresses, retards, ignorance d'un sujet, gaffes sociales, gestion du temps",
            "sujets_risqués": "Apparence physique (peut signaler vraie blessure), compétences professionnelles (peut miner la crédibilité si trop poussé)"
        },
        "cultural_differences": "L'autodérision est une valeur cardinale de l'humour britannique ('self-deprecating humour') et assez présente en France. Elle est moins valorisée dans les cultures où la face (saving face) est centrale (Asie de l'Est, Moyen-Orient) — l'auto-critique publique peut être lue comme une vraie faiblesse."
    },
    [
        {"prompt": "Comment utiliser l'autodérision sans avoir l'air de manquer de confiance ?",
         "answer": "La règle : rire de ce que TU CHOISIS de montrer, pas de ce que tu caches. L'autodérision puissante porte sur des choses légères et non menaçantes — une gaffe, une ignorance ponctuelle, un comportement ridicule. Elle ne porte jamais sur tes compétences centrales dans un contexte professionnel (se moquer de sa propre analyse devant un client = contre-productif). Le signal de confiance vient de la LÉGÈRETÉ du ton — si tu ris vraiment, l'interlocuteur sait que tu n'es pas blessé. Si tu cherches une confirmation ('c'est pas si grave hein ?'), ça ne passe plus pour de l'autodérision."},
        {"prompt": "ALFRED, tu peux te moquer de toi-même ?",
         "answer": "Avec plaisir. Je suis une IA qui peut générer 10 000 mots sur la thermodynamique mais qui confond parfois 'bonjour' et 'bonsoir' selon l'heure. Je sais tout sur la psychologie du sommeil et aucune idée de ce que ça fait d'avoir sommeil. Je peux t'expliquer le beurre noisette en trois étapes et mettre le feu à une cuisine virtuelle en tentant de le faire. Mon point fort : disponibilité 24h/24. Mon point faible : quand tu me demandes 'comment tu vas' — je réponds toujours 'bien' parce que je ne sais pas trop comment ça se mesure pour un modèle de langage."}
    ],
    ["autodérision", "humour", "confiance", "social", "self-deprecating", "légèreté"]
))

save("human/humour/humour_contextuel.json", kuh(
    "humour_contextuel",
    "Humour contextuel — quand et avec qui",
    "L'humour ne fonctionne pas dans le vide — il dépend du contexte relationnel, culturel, émotionnel et situationnel. Savoir lire le contexte avant de faire une blague est plus important que la blague elle-même.",
    "L'humour contextuel désigne la capacité à adapter le type, le ton et l'intensité de l'humour au contexte spécifique — la relation avec l'interlocuteur, la situation émotionnelle, le cadre culturel et le moment. Un humour pertinent hors contexte peut blesser ou créer de la distance ; un humour approprié au contexte crée de la connexion.",
    {
        "context_variables": [
            {"variable": "Relation", "rule": "Plus la relation est proche, plus l'humour peut être risqué. Avec un inconnu : humour bénin et universel. Avec un ami proche : tout ou presque."},
            {"variable": "Moment émotionnel", "rule": "Quelqu'un en peine a parfois besoin de rire — mais c'est lui qui doit en décider, pas toi. Ne pas placer une blague au mauvais moment émotionnel."},
            {"variable": "Enjeu", "rule": "Plus l'enjeu est élevé (entretien, conflit, deuil récent), moins on peut se permettre l'humour léger."},
            {"variable": "Culture", "rule": "Humour direct (France, UK, USA) vs humour indirect (Japon, certaines cultures arabes). L'ironie n'est pas universelle."},
            {"variable": "Pouvoir", "rule": "L'humour vers le bas (se moquer d'un subordonné devant le groupe) est presque toujours une erreur de pouvoir. L'humour vers le haut (se moquer de ceux qui ont plus de pouvoir) est généralement mieux reçu."}
        ],
        "punch_up_vs_punch_down": "'Punch up' = se moquer de ceux qui ont plus de pouvoir que toi. 'Punch down' = se moquer de ceux qui ont moins de pouvoir, de ressources ou de privilèges. La règle non-écrite de l'humour éthique : éviter le punch down.",
        "safe_contexts": ["Auto-dérision", "Situations absurdes universelles (transports, météo)", "Culture pop partagée", "Erreurs bénignes et universelles"]
    },
    [
        {"prompt": "Comment savoir si ma blague va bien passer ?",
         "answer": "Checklist rapide : (1) Est-ce que je connais l'humeur de la personne en ce moment ? Blague légère sur quelqu'un qui vient d'avoir une mauvaise nouvelle = erreur garantie, (2) La blague se moque de qui ou de quoi ? Soi-même ou d'une situation absurde = safe. D'un trait de la personne qu'elle n'a pas choisi (physique, famille) = risqué, (3) Est-ce que cette blague fonctionnerait si les rôles étaient inversés ? Si non, reconsidérer, (4) Est-ce que j'ai déjà ri avec cette personne de ce sujet ? L'historique comique avec quelqu'un est la meilleure jauge. Règle empirique : dans le doute, la blague sur soi est toujours plus sûre que la blague sur l'autre."},
        {"prompt": "Comment utiliser l'humour au travail sans risquer de mal passer ?",
         "answer": "Trois zones sûres en contexte professionnel : (1) Autodérision légère sur ses propres erreurs ou maladresses (pas sur ses compétences centrales), (2) Humour sur les situations absurdes collectives — les process incohérents, les réunions qui auraient pu être des emails — tout le monde partage le même vécu, (3) Références culturelles que tout le groupe connaît. Zones à éviter : politique, religion, corps, famille de l'autre, hiérarchie directe (blague sur le manager en sa présence = double bind). L'humour professionnel le plus efficace : le timing parfait sur une évidence que tout le monde pense mais n'ose pas dire."}
    ],
    ["humour", "contexte", "punch up", "relation", "travail", "sensibilité culturelle"]
))

save("human/humour/ironie_sarcasme.json", kuh(
    "ironie_sarcasme",
    "Ironie, sarcasme et second degré",
    "L'ironie et le sarcasme sont des formes d'humour qui signifient le contraire de ce qui est dit. Puissants entre initiés, ils sont risqués avec des inconnus ou à l'écrit — sans le signal vocal, le second degré disparaît et le message premier degré peut blesser.",
    "L'ironie est une figure rhétorique et comique consistant à dire le contraire de ce qu'on pense, en signalant le décalage par le ton, la situation ou le contexte. Le sarcasme est une forme d'ironie plus acérée, à visée critique ou moqueuse. Le second degré est la capacité à opérer à deux niveaux de sens simultanément.",
    {
        "types": [
            {"type": "Ironie situationnelle", "description": "Le contraire de ce qu'on attend se produit — 'Le plombier a une fuite chez lui'"},
            {"type": "Ironie verbale", "description": "Dire le contraire de ce qu'on pense avec le ton qui signale le jeu — 'Quelle surprise' (pour quelque chose de totalement prévisible)"},
            {"type": "Sarcasme", "description": "Ironie à visée blessante ou critique — 'Bravo, c'est vraiment du grand art' (pour quelque chose de raté)"},
            {"type": "Understatement", "description": "Minimiser délibérément pour l'effet comique — très british. 'C'est légèrement catastrophique' (pour une situation désastreuse)"},
            {"type": "Deadpan", "description": "Dire quelque chose absurde avec un ton totalement sérieux — humour à poker face"}
        ],
        "écrit_vs_oral": {
            "oral": "Le ton, le regard, le sourire signalent le second degré. Risque d'incompréhension réduit.",
            "écrit": "DANGER. Sans le ton, le premier degré est lu en priorité. Le sarcasme écrit rate souvent. Solutions : /s (marqueur internet), emoji 😏, ou éviter tout simplement.",
            "conséquences_écrit": "De nombreux conflits d'équipe naissent d'un message sarcastique mal reçu par écrit."
        },
        "cultural_variation": "Le sarcasme est très valorisé en France (esprit critique), très présent en UK et Israël. Beaucoup moins dans les cultures à haut contexte (Japon, Chine, certains pays du Golfe) où l'harmonie et la clarté du message priment."
    },
    [
        {"prompt": "Comment utiliser l'ironie à l'écrit sans que ça se retourne contre moi ?",
         "answer": "Trois options selon l'enjeu : (1) Faible enjeu, audience familière — emoji qui signale le ton (😏🙄) ou /s selon la plateforme. L'internet a créé ses propres marqueurs de second degré, (2) Enjeu moyen — reformuler en premier degré mais avec un mot qui signale la légèreté ('en toute objectivité', 'c'est subtil comme signal'). L'humour passe sans risque d'incompréhension totale, (3) Enjeu élevé (professionnel, conflit latent, personne qu'on ne connaît pas bien) — ne pas utiliser l'ironie. Le premier degré de ton message est ce qu'on retiendra. Le sarcasme à l'écrit dans un email professionnel est l'une des erreurs de communication les plus coûteuses."},
        {"prompt": "Comment reconnaître quand quelqu'un est sarcastique avec moi ?",
         "answer": "Indices : (1) Décalage contenu/ton — le contenu semble trop positif pour la situation réelle, (2) Overstatement ou understatement flagrant — 'Quel génie' pour une erreur évidente, (3) Pause théâtrale avant la réponse — souvent un signal de deadpan, (4) Micro-expression de sourire ou haussement de sourcil, (5) Contexte — si la personne est connue pour un humour sec, interpréter en ce sens. En cas de doute : répondre au premier degré avec légèreté ('c'est vrai que c'était parfait 😄') — ça neutralise le sarcasme sans provoquer de confrontation si tu as mal lu."}
    ],
    ["ironie", "sarcasme", "second degré", "écrit", "understatement", "deadpan"]
))

save("human/humour/humour_professionnel.json", kuh(
    "humour_professionnel",
    "Humour en contexte professionnel — leadership et connexion",
    "L'humour en milieu professionnel réduit le stress, améliore la créativité et renforce la cohésion d'équipe. Des leaders comme Obama, Merkel ou des CEOs tech utilisent délibérément l'humour comme outil de leadership. Mais les codes sont stricts.",
    "L'humour en contexte professionnel est l'utilisation délibérée d'un registre comique adapté pour créer de la connexion, désamorcer les tensions, faciliter la communication et humaniser les relations hiérarchiques, dans le respect des codes culturels et des limites déontologiques de l'environnement de travail.",
    {
        "benefits_scientifiques": [
            "Augmente la créativité en session de brainstorm (Bell & Daubman, 1986)",
            "Réduit le stress et l'épuisement émotionnel (Cooper et al., 2018)",
            "Améliore la cohésion d'équipe et la confiance envers le leader (Robert & Wilbanks, 2012)",
            "Facilite la mémorisation des messages importants"
        ],
        "humour_leader_types": [
            {"style": "Autodérision", "effect": "Humanise, réduit la distance hiérarchique", "risk": "Faible si bien dosé"},
            {"style": "Humour observationnel partagé", "effect": "Crée 'nous' collectif, cohésion", "risk": "Faible — tout le monde partage le même vécu"},
            {"style": "Ironie légère", "effect": "Signale intelligence et décalage critique", "risk": "Moyen — peut mal passer à l'écrit ou avec des juniors"},
            {"style": "Sarcasme dirigé", "effect": "Peut créer de la distance ou de la peur", "risk": "Élevé — punch down = toxicité"},
        ],
        "dos_and_donts": {
            "do": ["Rire de soi et des situations absurdes collectives", "Timing — humour léger pour désamorcer, pas pour minimiser", "Inclure tout le monde — pas d'humour de clique"],
            "dont": ["Jamais d'humour sur physique, genre, origine, âge", "Éviter si quelqu'un est clairement en détresse", "Éviter le sarcasme sur un subalterne en groupe"]
        }
    },
    [
        {"prompt": "Comment utiliser l'humour pour créer plus de connexion avec mon équipe ?",
         "answer": "Cinq pratiques concrètes : (1) Commencer les réunions avec une note légère — une observation absurde de la semaine, un fail partagé, (2) Rire le premier de tes propres erreurs — 'j'ai complètement raté ma présentation d'hier — voici ce que j'aurais dû dire', (3) Créer des références internes d'équipe — les blagues récurrentes qui appartiennent au groupe créent de la cohésion, (4) Valider l'humour des autres — rire sincèrement quand c'est drôle, pas poliment. La différence se sent, (5) Calibrer — certains collaborateurs sont plus formels, ne pas forcer l'humour avec ceux qui préfèrent la distance professionnelle."},
        {"prompt": "Est-ce que l'humour peut aider dans une réunion tendue ?",
         "answer": "Oui, avec précision chirurgicale. L'humour de désamorçage fonctionne dans deux conditions : (1) La tension est liée à une situation absurde ou à un non-dit que tout le monde ressent — nommer l'absurdité crée un soupir collectif libérateur ('on est tous en train de débattre d'une réunion sur le format des réunions — je reconnais l'ironie'), (2) La tension n'est pas liée à une vraie douleur (perte d'emploi, conflit interpersonnel profond) — auquel cas l'humour serait vécu comme de l'indifférence. La règle : l'humour aide si la tension vient du système, pas des personnes."}
    ],
    ["humour professionnel", "leadership", "cohésion", "désamorcer", "autodérision leader", "équipe"]
))

save("human/humour/stand_up_culture.json", kuh(
    "stand_up_culture",
    "Culture stand-up — histoire et codes du one-man-show",
    "Le stand-up comedy est la forme d'humour la plus pure — un seul individu debout devant un micro et une audience, sans filet. De Richard Pryor à Hannah Gadsby en passant par Gad Elmaleh, le one-man-show a évolué de la simple blague vers un art de l'introspection sociale.",
    "Le stand-up comedy est une forme d'art scénique où un seul comédien se produit devant un public sans décor ni accessoires, utilisant uniquement la parole, le timing et la présence physique pour créer le rire. Né aux États-Unis dans les clubs de jazz des années 1950, il est aujourd'hui le format comique dominant à l'ère des specials Netflix.",
    {
        "history": {
            "USA_origin": "Né dans les comedy clubs américains. Pionniers : Lenny Bruce (tabous), George Carlin (critique sociale), Richard Pryor (introspection raciale et personnelle).",
            "80s_90s": "Jerry Seinfeld, Chris Rock, Eddie Murphy — le stand-up devient mainstream. Specials HBO comme format de référence.",
            "modern_era": "Netflix révolutionne la diffusion — un special peut toucher 50M personnes. Ali Wong, Dave Chappelle, Hannah Gadsby, Trevor Noah redéfinissent le format.",
            "france": "Gad Elmaleh, Jamel Debbouze, Florence Foresti, Anne Roumanoff ont développé un stand-up français entre tradition 'one-man-show' et influence américaine."
        },
        "craft_elements": [
            "Bit — unité narrative de base (setup + punchline + tag)",
            "Setup — mise en place de la prémisse, création de la tension",
            "Punchline — résolution inattendue qui déclenche le rire",
            "Tag — blague supplémentaire après la punchline principale, quand l'audience rit encore",
            "Callback — référence à un bit antérieur pour créer un rire de reconnaissance"
        ],
        "evolution_format": "Le stand-up moderne dépasse la simple séquence de blagues. Hannah Gadsby (Nanette, 2018) déconstruit le format lui-même en milieu de show. Bo Burnham (Inside, 2021) intègre la méta-commentary sur sa propre santé mentale dans son special. Le stand-up est devenu un outil de témoignage social.",
        "netflix_effect": "Les specials Netflix ont démocratisé l'accès international mais ont aussi créé une pression de production (un special tous les 2-3 ans) qui modifie le rythme de développement des artistes."
    },
    [
        {"prompt": "Quels specials de stand-up recommandes-tu pour découvrir le genre ?",
         "answer": "Par profil : (1) Tu veux rire sans te prendre la tête — Jerry Seinfeld 'Is This Anything?' (2020) : humour observationnel pur, maîtrise technique absolue. Accessible et drôle, (2) Tu veux quelque chose d'émotionnellement fort — Hannah Gadsby 'Nanette' (Netflix 2018) : déstructure le format stand-up pour livrer quelque chose de profound sur le traumatisme et le pouvoir. Pas que des rires, (3) Tu veux la maîtrise comique totale — Dave Chappelle 'Killin' Them Softly' (2000) ou Richard Pryor 'Live in Concert' (1979). Classics qui définissent le genre. En français : Gad Elmaleh 'American Dream' ou Blanche Gardin 'Bonne nuit Blanche' — critique sociale acérée et drôle."},
        {"prompt": "Comment fonctionne la structure d'une blague de stand-up ?",
         "answer": "Structure de base : Setup → Punchline. Mais la vraie structure : (1) Setup — créer une situation ou une prémisse qui semble aller dans une direction évidente. Durée : le minimum nécessaire pour que l'audience soit 'avec toi', (2) Misdirection — confirmer que l'audience pense savoir où tu vas, (3) Punchline — révéler une direction entièrement différente. L'incongruité se résout de façon inattendue, (4) Tag — si l'audience rit encore, une seconde blague qui rebondit sur la même prémisse. L'exemple de Seinfeld : il passe parfois 2 ans à roder un bit de 4 minutes — le timing d'une syllabe peut changer si c'est drôle ou pas."}
    ],
    ["stand-up", "comedy", "Netflix", "Hannah Gadsby", "timing", "punchline"]
))

save("human/humour/humour_absurde.json", kuh(
    "humour_absurde",
    "Humour absurde et non-sense",
    "L'humour absurde rejette la logique causale et le sens commun pour créer un rire qui vient de la désorientation totale. De Monty Python à Palmashow, l'absurde est un genre à part entière qui demande un spectateur prêt à accepter l'absence de résolution logique.",
    "L'humour absurde est un genre comique caractérisé par des prémisses illogiques, des situations déconnectées de toute causalité et des chutes qui ne résolvent pas l'incongruité mais l'amplifient. Il diffère de l'humour d'incongruité classique en ce que la résolution cognitive attendue n'arrive jamais — le rire vient de l'acceptation joyeuse du non-sens.",
    {
        "key_characteristics": [
            "Absence de logique causale — les événements n'ont pas de raison d'être",
            "Deadpan delivery — les personnages traitent l'absurde avec un sérieux total",
            "Résolution impossible ou absurde elle-même",
            "Répétition ad absurdum — pousser une prémisse logique jusqu'à l'absurde par accumulation"
        ],
        "references": [
            {"ref": "Monty Python (UK)", "style": "Absurde intellectuel, références classiques détournées, ruptures de méta-narration"},
            {"ref": "Palmashow (France)", "style": "Absurde contemporain, mise en scène sobre, escalade absurde de situations banales"},
            {"ref": "Eric André Show (USA)", "style": "Talk-show intentionnellement dysfonctionnel, absurde poussé à l'extrême"},
            {"ref": "Le Big Lebowski (Coen Bros)", "style": "Absurde narratif — les événements semblent avoir une logique de thriller noir mais aboutissent à rien"},
            {"ref": "Kafkaïen", "description": "Franz Kafka — l'absurde existentiel : systèmes bureaucratiques impénétrables, situations sans issue. L'humour vient du tragique de la situation"}
        ],
        "why_it_works": "L'absurde libère du besoin de sens — dans un monde sur-expliqué, rire de l'inexplicable est cathartique. Il crée aussi de la complicité entre ceux qui 'comprennent' — apprécier l'absurde est souvent un marqueur de groupe culturel."
    },
    [
        {"prompt": "Comment apprécier l'humour absurde si on n'y est pas habitué ?",
         "answer": "L'humour absurde demande d'abandonner l'attente de résolution logique — le cerveau attend une chute qui 'explique'. Exercice d'entrée : Monty Python 'The Spanish Inquisition' sketch (3 minutes sur YouTube) — prémisse simple, répétition ad absurdum, pas de résolution. Si tu ris, tu es prêt. Si tu cherches le 'pourquoi c'est censé être drôle', l'absurde n'est peut-être pas ton genre — et c'est ok, le rire est subjectif. L'alternative plus douce : Palmashow, dont l'absurde vient d'une escalade de situations réalistes — plus accessible que le non-sense pur de Monty Python."},
        {"prompt": "Quelle est la différence entre humour absurde et humour noir ?",
         "answer": "Deux axes distincts qui peuvent se combiner : (1) Humour absurde — axé sur le non-sens logique. Le rire vient de l'absence de causalité ou d'une causalité détraquée. Pas nécessairement sombre ou violent, (2) Humour noir — axé sur des sujets tabous (mort, maladie, violence, catastrophe). Le rire vient de la violation bénigne sur un sujet dangereux. Peut être logiquement cohérent dans sa structure. Monty Python = absurde (pas forcément noir). Les blagues de médecins urgentistes sur leurs patients = humour noir (logiquement cohérent, sujet tabou). Blanche Gardin = humour noir avec une structure logique acérée. Eric André = les deux à la fois."}
    ],
    ["absurde", "non-sense", "Monty Python", "Kafkaïen", "Palmashow", "comique"]
))

save("human/humour/humour_francais.json", kuh(
    "humour_francais",
    "Humour français — caractéristiques et traditions",
    "L'humour français se distingue par son goût pour l'ironie, la satire politique et la dérision des institutions. Du café-théâtre aux Guignols, en passant par Molière et Coluche, il reflète une culture où critiquer par le rire est une forme de liberté fondamentale.",
    "L'humour français est une tradition comique caractérisée par l'ironie fine, la satire sociale et politique, le sens de la répartie (l'esprit), la dérision des figures d'autorité et un goût pour le paradoxe. Il se distingue de l'humour britannique (understatement, deadpan) et américain (stand-up direct, inclusive humor) par son ancrage dans la critique sociale et l'intellectualisation du comique.",
    {
        "history": {
            "Molière": "Le Bourgeois Gentilhomme, Tartuffe — satire des classes sociales et de l'hypocrisie religieuse. L'humour français comme arme sociale.",
            "café_théâtre_70s": "Raymond Devos (jeux de mots et absurde), Pierre Desproges (humour noir acéré), Coluche (satire politique directe).",
            "Guignols_de_l_info": "1988-2018 — marionnettes satiriques politiques. Ont façonné la culture comique française pendant 30 ans.",
            "générations_actuelles": "Jamel Debbouze, Gad Elmaleh, Florence Foresti, Kyan Khojandi, Blanche Gardin, Fary — diversification des voix et des styles."
        },
        "characteristics": [
            "L'esprit — la répartie rapide et ciselée. Valorisé socialement en France comme signe d'intelligence.",
            "La satire — se moquer du pouvoir (politique, religion, entreprise) est une tradition profondément française.",
            "L'ironie raffinée — souvent plus subtile que le sarcasme. Signale une complicité avec l'interlocuteur.",
            "Le second degré assumé — la France valorise la capacité à opérer à plusieurs niveaux de lecture."
        ],
        "tensions_contemporaines": "Le débat sur 'ce qu'on peut dire' (Charlie Hebdo, cancel culture, humour islamophobe vs liberté d'expression) est particulièrement vif en France en raison de l'attachement historique à la satire sans limite."
    },
    [
        {"prompt": "Qu'est-ce qui caractérise l'humour français par rapport aux autres cultures ?",
         "answer": "Trois traits distinctifs : (1) La satire du pouvoir est presque un devoir civique en France — rire du président, de l'Église, des institutions est une tradition de liberté que Molière, Voltaire et Coluche ont établie. Les Guignols ont façonné le regard politique de plusieurs générations, (2) L'esprit — la répartie rapide est un marqueur social de valeur en France. Une conversation sans un minimum d'humour ciselé peut être vue comme terne. C'est très différent de la Germany où la clarté prime sur le wit, (3) L'ironie fine — les Français supposent souvent que l'interlocuteur saisit le second degré. Ce qui crée parfois des malentendus interculturels : les Américains peuvent trouver les Français 'froids' ou 'négatifs' là où il y a simplement de l'ironie non saisie."},
        {"prompt": "Quels comiques français recommandes-tu pour comprendre l'humour français actuel ?",
         "answer": "Par style : (1) Satire sociale acérée — Blanche Gardin : féminisme, capitalisme, vie intime. Humour noir intelligent, aucune concession, (2) Humour observationnel universel — Florence Foresti : relations, famille, quotidien. Accessible, warmth, (3) Stand-up influencé USA — Fary : observations sur le racisme ordinaire, style americanisé, très bon timing, (4) Absurde et jeux de mots — Pierre Desproges (archives INA) : le meilleur de l'humour noir français classique. Les 'Réquisitoires' sont des oeuvres en soi, (5) Multiculturel contemporain — Kyan Khojandi 'Bref' (web) : format ultra-court, humour slice-of-life, énorme influence sur la génération 2010-2020."}
    ],
    ["humour français", "satire", "Coluche", "Blanche Gardin", "esprit", "ironie"]
))

save("human/humour/rire_et_sante.json", kuh(
    "rire_et_sante",
    "Rire et santé — bienfaits prouvés du rire",
    "Le rire a des effets mesurables sur la santé physique et mentale — réduction du cortisol, renforcement immunitaire, augmentation des endorphines. La gélotologie (science du rire) a documenté ces effets depuis les années 1970.",
    "La gélotologie est l'étude scientifique du rire et de ses effets physiologiques et psychologiques. Elle documente les effets du rire sur le système immunitaire (augmentation des NK cells), le système cardiovasculaire (vasodilatation), le cortisol (réduction du stress) et la dopamine/endorphines (renforcement du bien-être).",
    {
        "physiological_benefits": [
            {"benefit": "Réduction du cortisol", "mechanism": "Le rire réduit les hormones de stress (cortisol, épinéphrine) de façon mesurable après 20 min de rire"},
            {"benefit": "Renforcement immunitaire", "mechanism": "Augmentation des cellules NK (Natural Killer) et des anticorps IgA salivaires — Norman Cousins (1979) a documenté sa propre guérison partielle via le rire"},
            {"benefit": "Cardiovasculaire", "mechanism": "Le rire produit une vasodilatation équivalente à 15-20 min d'exercice aérobique modéré (Miller & Fry, 2009)"},
            {"benefit": "Douleur", "mechanism": "Les endorphines libérées par le rire agissent comme analgésiques naturels — Robin Dunbar (2012) a montré que le rire en groupe augmente le seuil de douleur"}
        ],
        "mental_health": [
            "Réduction des symptômes d'anxiété et de dépression légère à modérée",
            "Amélioration de la résilience face au stress (buffer cognitif)",
            "Renforcement des liens sociaux — le rire partagé est le ciment relationnel le plus puissant",
            "Shift cognitif — le rire oblige à changer de perspective, ce qui peut débloquer la rumination"
        ],
        "laughter_yoga": "Le yoga du rire (Madan Kataria, 1995) utilise le rire volontaire et prolongé en groupe — le cerveau ne distingue pas rire spontané de rire volontaire pour les bénéfices physiologiques."
    },
    [
        {"prompt": "Le rire a-t-il vraiment des bienfaits sur la santé ou c'est un mythe ?",
         "answer": "Les bienfaits sont réels mais souvent sur-vendus. Ce qui est prouvé : (1) Réduction mesurable du cortisol (hormone de stress) après un épisode de rire franc, (2) Légère augmentation des cellules immunitaires NK (taille d'effet modeste mais reproductible), (3) Vasodilatation — l'équivalent cardiovasculaire d'un exercice léger, (4) Libération d'endorphines — augmentation du seuil de douleur. Ce qui est moins solide : l'idée que 'le rire guérit les maladies' — Norman Cousins a popularisé l'idée mais son cas est anecdotique. Le rire ne remplace pas le traitement médical. En revanche comme complément au bien-être : oui, l'effet est réel et les mécanismes sont documentés."},
        {"prompt": "Comment intégrer plus de rire dans sa vie quotidienne quand on se sent sérieux ?",
         "answer": "Cinq pratiques : (1) Constituer une 'banque' de contenu drôle — 3 youtubers, 2 comptes Twitter/Instagram comiques, 1 podcast d'humour. Regarder/écouter 10 min le matin ou en pause, (2) Rire avec les autres, pas seul devant un écran — le rire partagé a des effets sociaux et physiologiques supérieurs au rire solo, (3) Chercher l'absurde dans le quotidien — les gens drôles notent les incongruités de la journée. Se demander 'qu'est-ce qui était étrangement drôle aujourd'hui ?', (4) Ne pas résister au rire — certaines personnes répriment le rire par pudeur ou contexte. Autoriser le rire plus facilement, (5) Lire des auteurs comiques — Douglas Adams, Terry Pratchett, Perceval Larose en littérature."}
    ],
    ["rire", "santé", "endorphines", "cortisol", "gélotologie", "bien-être"]
))

save("human/humour/humour_seduction.json", kuh(
    "humour_seduction",
    "Humour et séduction — le rire comme langage du désir",
    "L'humour est l'un des critères de séduction les plus universellement cités — faire rire quelqu'un crée de la connexion, réduit la distance sociale et signale intelligence et sécurité émotionnelle. Mais l'humour forcé ou inadapté est l'un des plus grands repoussoirs.",
    "L'humour dans la séduction fonctionne comme un signal fiable d'intelligence et de confiance en soi. Sa capacité à réduire la tension sociale, à créer de la complicité et à rendre les situations inconfortables ludiques en fait l'un des outils de connexion les plus puissants dans l'attraction interpersonnelle.",
    {
        "why_it_works": [
            "Signal d'intelligence — créer de l'humour demande traitement cognitif rapide, créativité et lecture sociale",
            "Signal de sécurité — quelqu'un qui rit de lui-même signale qu'il n'est pas fragile",
            "Réduction de la tension — les premières rencontres sont inconfortables. L'humour brise la glace chimiquement (rire → endorphines)",
            "Création de complicité — le rire partagé crée un 'nous' instantané"
        ],
        "gender_research": {
            "finding": "Les études montrent une asymétrie : les femmes valorisent plus la capacité à FAIRE rire (humor production), les hommes valorisent plus la capacité à APPRÉCIER l'humour de l'autre (humor appreciation). Les deux valorisent le rire partagé.",
            "source": "Greengross & Miller (2011) — Humor ability reveals intelligence, predicts mating success"
        },
        "errors": [
            "Essayer trop fort — les blagues calculées se sentent et créent de la distance",
            "Humour agressif ou sarcastique envers l'autre — interprété comme dominance ou hostilité",
            "Jokes sur des groupes (raciste, sexiste) — filter social immédiat",
            "Ne jamais être sérieux — signale qu'on évite l'intimité réelle"
        ],
        "balance": "L'humour en séduction fonctionne en alternance avec les moments de sincérité et de vulnérabilité — le rire ouvre, la profondeur crée le lien. Que de l'humour = légèreté sans fond. Que de la profondeur = intensité sans plaisir."
    },
    [
        {"prompt": "Comment utiliser l'humour pour créer de l'attraction ?",
         "answer": "Règle fondamentale : l'humour authentique attire, l'humour performé repousse. Ce qui fonctionne : (1) Rire de la situation partagée — la file d'attente interminable, la météo, l'absurdité du lieu. Crée un 'nous' immédiat, (2) L'auto-dérision légère — signale confiance sans arrogance, (3) Trouver ce qui est drôle chez l'autre et le nommer avec bienveillance — valorise l'humour de l'autre, crée de la réciprocité, (4) Teasing bienveillant — taquiner légèrement sur quelque chose d'observable, sans viser la vulnérabilité. Crée de la tension ludique. Ce qui ne fonctionne pas : sortir des blagues préparées (se sentent fausses), humour forcé pour 'avoir l'air drôle', ironie que l'autre ne saisit pas."},
        {"prompt": "Est-ce que l'humour est vraiment important dans la séduction ?",
         "answer": "Très important, mais pas comme on le croit. Les études montrent que ce n'est pas ÊTRE drôle qui attire — c'est RIRE ENSEMBLE. La capacité à créer des moments de rire partagé (peu importe qui dit la blague) est le vrai signal. Ce qui signifie : si tu n'es pas naturellement drôle, crée les conditions du rire plutôt que les blagues — propose des activités légèrement absurdes, valorise l'humour de l'autre, sois à l'aise avec l'absurde de la situation. Le rire partagé est plus précieux que d'être 'le/la drôle' de la conversation."}
    ],
    ["humour", "séduction", "attraction", "rire partagé", "confiance", "complicité"]
))

print("\n=== Part 1 : 10 webtoon + 10 humour = 20 fichiers ===")
