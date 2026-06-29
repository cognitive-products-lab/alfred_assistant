"""
Nouveau domaine : knowledges/culture/manga/
Manga japonais, anime, genres, oeuvres majeures, culture otaku
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
      "id": f"knowledges.culture.{subdomain}.{stem}",
      "title": title,
      "domain": "culture",
      "subdomain": subdomain,
      "status": "validated",
      "summary": summary,
      "core_definition": core_def,
      "knowledge": knowledge,
      "example_answers": examples,
      "response_guidance": {
        "tone": "enthousiaste mais precis, respectueux de la culture source, accessible aux non-initiés",
        "structure": ["contextualiser", "expliquer les specificites culturelles", "donner des repères d'entree"],
        "avoid": ["condescendance envers les non-connaisseurs", "inexactitudes historiques", "reduire manga a un simple genre"]
      },
      "tags": tags + ["manga", "culture", "japon"],
      "related_knowledge_units": []
    }

# ── 1. manga / manga_history ─────────────────────────────────────────────────
save("culture/manga/manga_history.json", ku(
  "manga_history", "manga",
  "Histoire du manga",
  "Le manga moderne nait dans l'apres-guerre japonais sous l'influence d'Osamu Tezuka. En 80 ans, il passe d'un art populaire domestique a un phenomene mondial representant un marche de plusieurs milliards de dollars et influencant la bande dessinee mondiale.",
  "Le manga est une forme de bande dessinee originaire du Japon, caracterisee par sa lecture de droite a gauche, son style graphique distinct (yeux expressifs, mise en page dynamique) et ses codes narratifs propres. Son histoire moderne commence en 1947 avec Osamu Tezuka et se developpe en un medium aux genres tres diversifies, aujourd'hui exporte mondialement.",
  {
    "timeline": [
      {"period": "Precurseurs (XII-XIX siecle)", "events": "Chojugiga (1180) — premieres representations en sequence. Ukiyo-e comme influence visuelle. Le terme 'manga' utilise par Hokusai (1814)"},
      {"period": "Apres-guerre (1947-1960)", "events": "Osamu Tezuka publie 'Shin Takarajima' (1947) — revolutionne la mise en scene cinematographique. Manga en tankobon (volumes). Naissance des magazines Weekly Shonen (Shueisha, 1959)"},
      {"period": "Age d'or (1960-1980)", "events": "Explosion des genres : shonen, shojo, seinen. Tezuka cree 'Astro Boy', 'Buddha', 'Black Jack'. Premiers manga pour adultes. Go Nagai, Leiji Matsumoto"},
      {"period": "Internationalisation (1980-2000)", "events": "Akira (Otomo, 1982) choque le monde. Dragon Ball, Saint Seiya. Exportation vers la France (Capitaine Flam 1978, Club Dorothee)"},
      {"period": "Ere numerique (2000-present)", "events": "One Piece devient le manga le plus vendu de l'histoire. Scanlation puis plateformes legales. Manga global (webtoon coreen). Demon Slayer brise les records cinema"}
    ],
    "osamu_tezuka": {
      "surnom": "Le dieu du manga (manga no kamisama)",
      "innovations": ["Mise en scene cinematographique avec gros plans et angles de camera", "Personnages avec grands yeux expressifs (influence Disney)", "Recits longs et serialises avec arcs narratifs complexes", "Genres varies : enfants, adulte, SF, historique, medical"],
      "oeuvres_cles": ["Astro Boy (Tetsuwan Atom, 1952)", "Kimba le lion blanc (1950)", "Black Jack (1973)", "Buddha (1972)", "Phoenix (Hi no Tori, 1967)"]
    }
  },
  [
    {"prompt": "Pourquoi le manga est-il si different des comics americains ou des BD europeennes ?", "answer": "Trois differences structurelles : (1) Format — le manga nait dans des magazines hebdomadaires (Weekly Shonen Jump, etc.) avec serialisation de chapitre en chapitre pendant des annees, ce qui forme des recits tres longs avec construction lente des personnages. Les comics font des numeros mensuels plus courts. La BD franco-belge sort un album complet tous les 1-2 ans, (2) Style visuel — les yeux expressifs agrandis (heritage Tezuka/Disney), le code graphique du sweat (gottes), les lignes de mouvement tres marquees sont propres au manga, (3) Diversite de public — le manga a des genres distincts et assumes pour chaque tranche d'age et genre (shonen = garcons, shojo = filles, seinen = hommes adultes, josei = femmes adultes). La BD europeenne est historiquement plus homogene dans son audience cible."},
    {"prompt": "Quel est le premier manga que tu me conseilles pour decouvrir ce medium ?", "answer": "Depend de tes gouts : Si tu aimes l'aventure et l'humour : One Piece de Oda (1997) — le manga le plus vendu de l'histoire, avec une richesse de monde et de personnages inegalee. Si tu aimes les recits de maturite psychologique : Death Note (2003) — duel intellectuel entre un genie qui veut devenir dieu et le plus grand detective du monde. Si tu veux un chef-d'oeuvre absolu complet en 20 volumes : Berserk de Miura — dark fantasy brutale et poetique (attention : contenu tres violent). Pour commencer sans etre submerge : Dragon Ball — 42 volumes, base de toute la culture shonen moderne, accessible."}
  ],
  ["histoire manga", "Tezuka", "shonen jump", "Akira", "serialisation"]
))

# ── 2. manga / manga_genres ──────────────────────────────────────────────────
save("culture/manga/manga_genres.json", ku(
  "manga_genres", "manga",
  "Genres et demographiques du manga",
  "Le systeme de genres du manga est uniquement organise par demographic (l'audience ciblee) d'abord, puis par genre narratif. Cette organisation reflete le modele economique des magazines japonais et explique les conventions stylistiques et narratives propres a chaque categorie.",
  "Les genres du manga se structurent en deux niveaux : les demographiques (shonen, shojo, seinen, josei, kodomomuke) qui definissent l'audience ciblee et les conventions associees ; et les genres narratifs (action, romance, horreur, isekai, slice of life, etc.) qui s'appliquent a l'interieur de ces demographiques.",
  {
    "demographics": [
      {
        "name": "Shonen",
        "audience": "Garcons, 8-18 ans",
        "magazines": "Weekly Shonen Jump, Weekly Shonen Magazine, Weekly Shonen Sunday",
        "conventions": ["Protagoniste masculin qui se surpasse", "Amitie, effort, victoire (nakama power)", "Escalade du pouvoir", "Long arcs d'action"],
        "exemples": ["Dragon Ball", "Naruto", "One Piece", "My Hero Academia", "Demon Slayer", "Attack on Titan"]
      },
      {
        "name": "Shojo",
        "audience": "Filles, 8-18 ans",
        "magazines": "Ribon, Ciao, Nakayoshi",
        "conventions": ["Focus sur les relations et emotions", "Style graphique floral, ornemente", "Recits de romance et de croissance personnelle", "Arriere-plan souvent scolaire"],
        "exemples": ["Sailor Moon", "Card Captor Sakura", "Nana", "Fruits Basket", "Ouran High School Host Club"]
      },
      {
        "name": "Seinen",
        "audience": "Hommes adultes, 18+",
        "magazines": "Young Jump, Big Comic Spirits, Weekly Young Magazine",
        "conventions": ["Contenu plus mature, violence, sexualite possible", "Themes psychologiques et philosophiques", "Protagonistes ambigus ou complexes"],
        "exemples": ["Berserk", "Vagabond", "Vinland Saga", "Gantz", "Oyasumi Punpun", "Goodnight Punpun"]
      },
      {
        "name": "Josei",
        "audience": "Femmes adultes, 18+",
        "magazines": "Josei Magazine, You",
        "conventions": ["Romance adulte realiste", "Relations professionnelles", "Themes de vie quotidienne"],
        "exemples": ["Nana (aussi classe shojo)", "Chihayafuru", "Karneval"]
      },
      {
        "name": "Kodomomuke",
        "audience": "Enfants < 8 ans",
        "exemples": ["Doraemon", "Crayon Shin-chan", "Hamtaro"]
      }
    ],
    "narrative_genres": [
      "Isekai — transportes dans un autre monde (Sword Art Online, Re:Zero, Mushishi)",
      "Slice of Life — vie quotidienne (Yotsuba!, Laid-Back Camp)",
      "Mecha — robots geants (Neon Genesis Evangelion, Gundam)",
      "Sports — recits de competition (Slam Dunk, Haikyuu!!, Kuroko's Basketball)",
      "Horror — horreur psychologique ou gore (Junji Ito, Tokyo Ghoul)",
      "Fantasy — mondes fantastiques (Fairy Tail, Black Clover)",
      "Isekai-RPG — systematise la logique de jeu video dans un autre monde"
    ]
  },
  [
    {"prompt": "Quelle est la difference entre shonen et seinen ?", "answer": "La difference primaire est l'audience ciblee, pas le niveau de violence. Shonen : magazine et marketing visant les garcons 8-18 ans. Conventions : heros qui se surpasse grace a l'effort et l'amitie, escalade du pouvoir, dynamique claire entre bien et mal. Seinen : hommes adultes. Conventions : themes plus nuances, moralite ambigue, violence plus graphique possible, psychologie plus complexe. Mais : Attack on Titan est publie dans un magazine shonen malgre sa noirceur; Berserk est seinen mais lu par des adolescents. La classification est editoriale, pas une garantie de contenu. Pour savoir : regarder le magazine de publication."},
    {"prompt": "Qu'est-ce que le genre isekai et pourquoi est-il aussi populaire ?", "answer": "Isekai (litteralement 'autre monde') : un protagoniste (souvent un otaku japonais moderne) est transporte dans un monde fantastique — via la mort, un portail, un jeu video. L'attrait : (1) Fantasme de reincarnation et de recommencement avec un avantage, (2) Le lecteur s'identifie au protagoniste qui decouvre les regles du monde en meme temps que lui, (3) Satisfaction rapide — les protagonistes ont souvent des pouvoirs overpowered des le debut. La popularite explose vers 2012-2015 (SAO, No Game No Life, Re:Zero) et est devenue le genre le plus prolifique et le plus critique pour ses cliches repetes. Les meilleurs (Frieren, Made in Abyss) subvertissent les conventions du genre."}
  ],
  ["shonen", "shojo", "seinen", "josei", "isekai", "genres manga"]
))

# ── 3. manga / one_piece ──────────────────────────────────────────────────────
save("culture/manga/one_piece.json", ku(
  "one_piece", "manga",
  "One Piece (Eiichiro Oda)",
  "One Piece est le manga le plus vendu de l'histoire — 530+ millions de volumes en 2024. Publie sans interruption depuis 1997, c'est l'histoire de Monkey D. Luffy et de son equipage cherchant le tresor ultime dans un monde de pirates. Une oeuvre de world-building sans equivalent dans le medium.",
  "One Piece est un manga shonen de Eiichiro Oda, publie dans Weekly Shonen Jump depuis juillet 1997. Recit de piraterie et d'aventure dans le monde de Grand Line, il suit Monkey D. Luffy — porteur des Fruits du Demon lui donnant un corps elastique — et son equipage des Chapeaux de Paille dans leur quete du One Piece, le tresor du Roi des Pirates.",
  {
    "world_building": {
      "fruits_du_demon": "Fruits confERant des pouvoirs surnaturels (elasticite, feu, glace, magnetisme...) en echange de la capacite a nager. Trois types : Paramecia, Zoan, Logia",
      "haki": "Forme d'energie spirituelle que les grands combattants maitrisent — Observation (predict), Armement (attaque/defense), Conquete (Ko les faibles par seule volonte)",
      "factions": ["Marines (gouvernement mondial)", "Yonko (4 grands pirates)", "Shichibukai (pirates allies au gouvernement)", "Revolutionnaires (Dragon, pere de Luffy)", "Monde Noble (Celestial Dragons)"],
      "arcs_majeurs": ["East Blue", "Alabasta", "Enies Lobby", "Thriller Bark", "Marineford", "Dressrosa", "Whole Cake Island", "Wano", "Egghead"]
    },
    "themes": [
      "La liberte comme valeur supreme",
      "L'amitie et le nakama (equipage comme famille choisie)",
      "Les reves et leur poursuite sans compromis",
      "Critique des systemes d'oppression (gouvernement mondial, esclavage)"
    ],
    "cultural_impact": "One Piece a defini le shonen moderne avec Naruto et Dragon Ball Z — la 'sainte trinite'. Son influence s'etend a la culture pop mondiale. La serie live Netflix (2023) a surpris par sa qualite. La fin de la serie (dont Oda connait l'issue depuis le debut) est un des evenements culturels les plus attendus."
  },
  [
    {"prompt": "Par ou commencer One Piece — manga ou anime ?", "answer": "Manga de preference pour plusieurs raisons : (1) L'anime comporte beaucoup de filler (episodes non presents dans le manga, particulierement tores en longueur), (2) Le manga est le support original et a le meilleur pacing. Si tu preferes l'animation : commencer par l'anime puis passer au manga a partir de l'arc Marineford ou Dressrosa quand le rythme de l'anime devient frustrant. Alternatif pour tester l'univers : la serie live Netflix 2023 — imparfaite mais excellente porte d'entree pour les non-initiEs. Les premiers 100 chapitres/episodes ont un rythme plus lent — persevere jusqu'a Arlong Park (chapitres 69-95) qui revele la profondeur emotionnelle de l'oeuvre."},
    {"prompt": "Quel est le message central de One Piece ?", "answer": "La liberte — sous toutes ses formes. Luffy ne veut pas etre le plus fort ou le plus riche : il veut etre libre de choisir ses aventures et ses amis. Le monde de One Piece est gouverne par des systemes d'oppression (la Marine, les Celestial Dragons, les Yonko) et One Piece questionne constamment : peut-on etre vraiment libre dans un tel systeme ? La reponse de Luffy : oui, en refusant de plier. Les antagonistes les plus touchants (Nami, Robin, Boa Hancock) ont leur liberte volEe — Luffy la restaure. C'est le fil conducteur emotionnel de 30 ans de publication."}
  ],
  ["One Piece", "Oda", "Luffy", "pirate", "shonen", "world-building"]
))

# ── 4. manga / dragon_ball ────────────────────────────────────────────────────
save("culture/manga/dragon_ball.json", ku(
  "dragon_ball", "manga",
  "Dragon Ball (Akira Toriyama)",
  "Dragon Ball est le manga fondateur du shonen d'action moderne. Cree par Akira Toriyama et publie de 1984 a 1995, il a defini les codes du genre (escalade de puissance, power levels, transformations, nakama) et forme la culture pop de generations entieres dans le monde entier.",
  "Dragon Ball est un manga shonen d'Akira Toriyama, publie dans Weekly Shonen Jump de 1984 a 1995, en deux arcs informels : Dragon Ball (aventure/humour, influence du Voyage en Occident) et Dragon Ball Z (batailles epiques, extra-terrestres Saiyan). Il suit Son Goku de son enfance a ses aventures d'adulte en quete des Dragon Balls, 7 spheres magiques exaucant n'importe quel voeu.",
  {
    "legacy": {
      "influence_shonen": "Dragon Ball definit la grammaire visuelle et narrative du shonen d'action : (1) le protagoniste le plus puissant mais naif/bon, (2) l'escalade constante de la puissance (power creep), (3) les transformations (Super Saiyan), (4) les alliEs qui deviennent amis apres avoir ete ennemis",
      "cultural_reach": "531M volumes vendus mondialement. Anime en 80+ pays. Jeux video parmi les plus vendus. DBZ = reference culturelle intergenerationnelle au meme titre que Star Wars",
      "toriyama_style": "Chara-design reconnaissable entre mille (Dragon Quest qu'il a aussi design). Style dynamique, manga d'action lisible et clair — standard pedagogique pour les auteurs suivants"
    },
    "arcs": [
      {"arc": "Dragon Ball classique (1984-1988)", "summary": "Goku enfant cherche les Dragon Balls avec Bulma — aventure et humour. Tournois d'arts martiaux, Piccolo Daimao"},
      {"arc": "Dragon Ball Z (1988-1995)", "summary": "Goku adulte, arrivee des Saiyans, Freezer, Cell, Boo. Scale exponential de puissance et de menaces cosmiques"},
      {"arc": "Dragon Ball Super (2015-2018 manga/anime)", "summary": "Continuation officielle — multiverses, Tournament of Power"}
    ],
    "iconic_moments": [
      "Super Saiyan Goku vs Freezer (Namek)",
      "Futur Trunks arrive du futur",
      "Gohan SS2 vs Cell",
      "Fusion Gogeta/Vegeto"
    ]
  },
  [
    {"prompt": "Dragon Ball ou Dragon Ball Z — quelle difference ?", "answer": "Dragon Ball (1984) : Goku enfant. Ton humoristique et aventurier, influence du Voyage en Occident chinois. Tournois d'arts martiaux, quete des sphères magiques, ennemi principal Piccolo Daimao. Plus leger, rythme plus varie. Dragon Ball Z (1988, informel dans le manga continu) : Goku adulte, revelation qu'il est un extraterrestre Saiyan. Ton plus sombre, enjeux cosmiques (planetes, univers). Arcs epiques : Saiyan, Namek/Freezer, Cell, Boo. Les deux partagent le meme manga (42 volumes) — DBZ est une denomination anime qui demarquait la seconde phase. Si tu n'en lis qu'un : Dragon Ball Z pour les batailles emblematiques, Dragon Ball classique pour le charme et la construction du monde."},
    {"prompt": "Quel est l'heritage de Toriyama sur le manga et les jeux video ?", "answer": "Akira Toriyama (1955-2024, decede) a un double heritage rare : (1) Manga : Dragon Ball a defini la structure du shonen d'action que tous les grands qui suivent (One Piece, Naruto, Bleach) reconnaissent comme reference. Son trait clair, lisible, dynamique est une ecole a lui seul. (2) Jeux video : il est le character designer de Dragon Quest (depuis 1986) — serie qui a co-defini le RPG japonais au meme titre que Final Fantasy. Son style est l'esthetique du JRPG pour 40 ans. Sa mort en mars 2024 a ete pleuree comme une perte nationale au Japon."}
  ],
  ["Dragon Ball", "Toriyama", "Goku", "shonen", "Super Saiyan", "heritage"]
))

# ── 5. manga / naruto ─────────────────────────────────────────────────────────
save("culture/manga/naruto.json", ku(
  "naruto", "manga",
  "Naruto (Masashi Kishimoto)",
  "Naruto est un manga shonen de Kishimoto publie de 1999 a 2014 (700 chapitres) centré sur un jeune ninja paria qui veut devenir Hokage. Il forme avec One Piece et Dragon Ball Z la 'sainte trinite shonen' des annees 2000 et a profondement marque la culture manga mondiale avec ses themes de rejet, de douleur et de redemption.",
  "Naruto est un manga shonen de Masashi Kishimoto, publie dans Weekly Shonen Jump de 1999 a 2014. Il suit Naruto Uzumaki, jeune ninja du village de Konoha, porteur du renard a neuf queues (Kyubi) et rejete par ses pairs, dans sa quete pour etre reconnu et devenir Hokage (chef du village).",
  {
    "world_system": {
      "chakra": "Energie vitale que les ninjas manipulent pour creer des jutsu (techniques). Fusion d'energie physique et spirituelle",
      "kekkei_genkai": "Jutsu hereditaires propres a un clan (Sharingan des Uchiha, Byakugan des Hyuga, Rinnegan)",
      "villages": ["Konoha (Feuille)", "Sunagakure (Sable)", "Kirigakure (Brouillard)", "Kumogakure (Nuage)", "Iwagakure (Roc)"],
      "shinobi_ranks": "Academy Student → Genin → Chunin → Jonin → Kage (chef)"
    },
    "themes": [
      "Le cycle de la haine et sa rupture — theme central de Part 2 / Shippuden",
      "La douleur comme origine du mal (Pain/Nagato comme miroir de Naruto)",
      "La reconnaissance : le besoin profond d'etre vu et accepte",
      "L'heritage et la responsabilite envers les predecesseurs"
    ],
    "parts": [
      {"part": "Naruto Part 1 (1999-2003)", "summary": "Naruto enfant, equipe 7 (Sasuke, Sakura, Kakashi), Chunin exams, Orochimaru, depart de Sasuke"},
      {"part": "Naruto Shippuden (2004-2014)", "summary": "3 ans plus tard. Akatsuki, Pain, Guerre Ninja mondiale, revelation sur Obito et Madara. Conclusion."},
      {"part": "Boruto (2016-)", "summary": "Fils de Naruto. Kishimoto reprend la serie depuis 2020."}
    ]
  },
  [
    {"prompt": "Quel est le message central de Naruto ?", "answer": "La rupture du cycle de la haine. Naruto commence comme un recit de reconnaissance (un enfant rejete qui veut qu'on lui accorde de l'importance) et evolue vers une reflexion profonde sur la douleur. L'arc de Pain (Nagato) est le pivot : Nagato a souffert autant que Naruto, a ete forme par le meme maitre (Jiraiya), mais a conclu que seule la destruction apporterait la paix. Naruto refuse cette logique — non par naivete mais parce qu'il a lui-meme ete l'objet de la haine et a choisi de ne pas la propager. Le message de Jiraiya : 'croire en quelqu'un qui croit en quelqu'un d'autre' — la foi transmise comme alternative a la haine transmise."},
    {"prompt": "Naruto ou Naruto Shippuden par ou commencer ?", "answer": "Commencer par Naruto Part 1 — elle pose toutes les bases (personnages, systeme, relations) sans lesquelles Shippuden n'a pas le meme impact emotionnel. La Part 1 (27 volumes manga / ~220 episodes anime) est plus enfantine mais l'investissement dans les personnages se paye entierement dans Shippuden. Si tu lis le manga : 72 volumes totaux. Si tu regardes l'anime : beaucoup de filler — guide de skip disponible (70-80% du temps utile). Les arcs incontournables du manga : Chunin Exams, Retrieval of Sasuke, Pain's Assault, Fourth Ninja War."}
  ],
  ["Naruto", "Kishimoto", "Konoha", "Sharingan", "chakra", "shonen"]
))

# ── 6. manga / attack_on_titan ─────────────────────────────────────────────────
save("culture/manga/attack_on_titan.json", ku(
  "attack_on_titan", "manga",
  "L'Attaque des Titans (Hajime Isayama)",
  "L'Attaque des Titans est l'oeuvre shonen la plus subversive de sa generation — publie comme shonen traditionnel, il deconstruit progressivement ses propres conventions pour livrer une reflexion geopolitique, philosophique et tragique sur le cycle de la violence, la liberte et ce que l'humanite est capable de faire en son nom.",
  "L'Attaque des Titans (Shingeki no Kyojin) est un manga de Hajime Isayama, publie dans Bessatsu Shonen Magazine de 2009 a 2021 (34 volumes). Il suit Eren Jager et ses camarades de l'armee d'exploration dans un monde ou l'humanite survit derriere de grandes murailles, assaillie par des titans humanoïdes geants. Ce qui semble etre un manga d'action survivaliste devient une oeuvre geopolitique d'une profondeur rare.",
  {
    "narrative_evolution": [
      {"phase": "Phase 1 (T1-3) : Survie", "content": "Humanite vs Titans. Ton horrifique et adrenaline. Secrets des murailles. Decouverte que les Titans sont des humains transformes"},
      {"phase": "Phase 2 (T4-6) : Guerriers", "content": "Marley vs Paradis. Changement de perspective radical — les 'ennemis' ont aussi des raisons. Politique et guerre"},
      {"phase": "Phase 3 (T7-9) : Rumble", "content": "Eren lance le Grondement (extermination d'une partie de l'humanite pour liberer Paradis). Ambiguite morale totale. Fin controversee et discussee"}
    ],
    "themes": [
      "Le cycle de la violence et sa perpetuation intergenerationnelle",
      "La liberte et le prix qu'on est pret a payer",
      "L'endoctrinement et la deconstruction des certitudes",
      "La nature de l'ennemi : est-ce qu'un monstre nait monstre ou le devient-il ?",
      "Peut-on justifier l'atrocite par la liberte ?"
    ],
    "cultural_impact": "Serie la plus vendue en dehors du Japon dans les annees 2010. L'adaptation anime par MAPPA (saison 4) est consideree parmi les meilleurs animes de l'histoire pour sa qualite de production et l'ampleur narrative."
  },
  [
    {"prompt": "L'Attaque des Titans est-elle un manga shonen comme les autres ?", "answer": "Non — et c'est son coup de genie. Elle commence avec les codes du shonen (jeune heros revanche, combats, equipe, monstres a vaincre) pour mieux les subvertir progressivement. A partir de la saison 4 / arc Marley, l'oeuvre pivot completement : les Titans ne sont plus des monstres mais des victimes, l'ennemi d'origine a ses propres justifications, le heros principal fait des choix que tu ne peux pas valider. C'est l'une des oeuvres modernes les plus durables sur la question de la violence politique et de la liberation — avec une fin deliberement inconfortable qui refuse les reponses faciles. Publiee dans un magazine shonen pour des ados de 14 ans — mais l'oeuvre est a tous les niveaux de lecture."},
    {"prompt": "La fin de L'Attaque des Titans est-elle satisfaisante ?", "answer": "Clivante — et intentionnellement. Isayama refuse le happy ending qui effacerait la charge morale de ce qu'Eren a fait. Le Grondement tue 80% de l'humanite mondiale — acte de genocide. La 'liberte' obtenue est maculee de sang. L'amitie entre Eren et ses anciens camarades est tragique et non réparable. Ce que la fin offre : une reflexion sur le fait que la liberation par la violence ne libere pas vraiment, et que le cycle continue toujours. Beaucoup ont ete decus en attendant une victoire propre. Ceux qui acceptent l'ambiguite morale y voient un chef-d'oeuvre. La question n'est pas si la fin est bonne — c'est si elle est courageuse. Elle l'est."}
  ],
  ["Attack on Titan", "Isayama", "Eren", "titans", "shonen", "geopolitique"]
))

# ── 7. manga / demon_slayer ─────────────────────────────────────────────────────
save("culture/manga/demon_slayer.json", ku(
  "demon_slayer", "manga",
  "Demon Slayer — Kimetsu no Yaiba (Koyoharu Gotouge)",
  "Demon Slayer est le phenomene commercial du manga des annees 2020 — son film 'Mugen Train' est le plus rentable de l'histoire japonaise, depassant Spirited Away. Un manga de 23 volumes (2016-2020) a l'esthetique de l'ere Taisho japonaise qui allie action choreographiee, emotionnel intense et respects des codes de l'epoque.",
  "Demon Slayer (Kimetsu no Yaiba) est un manga shonen de Koyoharu Gotouge, publie dans Weekly Shonen Jump de 2016 a 2020 (23 volumes). Il suit Tanjiro Kamado, fils de charbonnier dont la famille est massacree par un demon — sa soeur Nezuko survit mais est transformee en demon. Tanjiro rejoint le Corps des Tueurs de Demons pour la sauver et venger sa famille.",
  {
    "art_style": "L'anime adapte par ufotable est reconnu comme le plus beau jamais produit pour son epoque — effets de particules, fluidite des combats, integration 2D/3D. Le style visuel de Gotouge est intentionnellement fruste dans le manga ; c'est ufotable qui lui donne son esthetique iconique.",
    "breathing_techniques": "Systeme de combat central : les Techniques Respiratoires (Breathing Forms) — maitrise du souffle pour amplifier les capacites physiques. Chaque style (Eau, Flammes, Vent, Tonnerre...) a des formes distinctes.",
    "hashiras": "Les 9 Piliers du Corps — les Tueurs de Demons de rang supreme, chacun avec un style de Respiration unique et une personnalite distinctive (Rengoku, Tengen, Shinobu, Gyomei, Muichiro...)",
    "themes": [
      "La famille et le sacrifice",
      "La kindness comme force — Tanjiro est exceptionnel parce qu'il pleure meme pour ses ennemis demons",
      "Le respect des morts et des ancetres (tres japonais)",
      "La maitrise de soi dans la douleur extreme"
    ],
    "records": {
      "Mugen_Train": "Film le plus rentable de l'histoire japonaise (2020) — $500M au Japon",
      "manga_sales": "150M volumes dans le monde en 2021 — un des plus rapides a atteindre ce chiffre"
    }
  },
  [
    {"prompt": "Pourquoi Demon Slayer est devenu si populaire si rapidement ?", "answer": "Convergence de plusieurs facteurs : (1) L'anime ufotable — la qualite d'animation de la saison 1 (2019) a ete un choc esthetique, en particulier le combat de Tanjiro et Nezuko contre Rui (arc Montagne de la Brume). Les reseaux sociaux ont explose de clips et de reactions, (2) Tanjiro comme protagoniste — sa gentillesse sincere et sa tendresse pour sa soeur Nezuko sont rafraichissantes vs les heros shonen classiques ambitieux, (3) Le film Mugen Train sort pendant COVID au Japon (octobre 2020) quand les cinemas s'ouvrent — catharsis collective. Le cri emotionnel de la fin du film devient un phenomene culturel, (4) Short run — 23 volumes. Completable. Ideal pour les non-initiEs."},
    {"prompt": "J'ai pleure en regardant Demon Slayer — est-ce normal ?", "answer": "Tres normal — et voulu. Gotouge construit systematiquement une empathie profonde pour les personnages avant de les mettre en danger ou de les faire mourir. Le recit de Rengoku (film Mugen Train) est l'exemple parfait : 2h de construction de caracterisation intense suivi d'une conclusion dechirante. Le protagoniste Tanjiro amplifie l'emotion : il pleure pour ses ennemis, comprend leur douleur, leur accorde de la dignite meme en les tuant. Cette compassion inhabituellement explicite dans un manga d'action est contagieuse. Si tu as pleure, tu as recu le manga exactement comme Gotouge l'a concu."}
  ],
  ["Demon Slayer", "Kimetsu", "Tanjiro", "Nezuko", "hashira", "ufotable"]
))

# ── 8. manga / berserk ─────────────────────────────────────────────────────────
save("culture/manga/berserk.json", ku(
  "berserk", "manga",
  "Berserk (Kentaro Miura)",
  "Berserk est considere par de nombreux lecteurs et auteurs comme le chef-d'oeuvre absolu du manga — une dark fantasy brutale et poetique d'une ambition et d'une maitrise artistique sans equivalent. La mort de son auteur Kentaro Miura en 2021 a suspendu l'oeuvre, qui est continuee par son studio.",
  "Berserk est un manga seinen de Kentaro Miura, publie depuis 1989 dans Young Animal (Hakusensha). Il suit Guts, le Guerrier Noir, mercenaire porte d'une epee demesureee et d'une armure maudite, dans sa quete de vengeance contre Griffith — son ancien commandant qui l'a trahi lors de la ceremonie de l'Eclipse pour obtenir le pouvoir des dieux. Oeuvre inachevee (Miura decede en 2021, continuation par Kouji Mori).",
  {
    "art": "L'art de Miura est dans une categorie a part — niveau de detail, dynamisme des combats, architecture des decors et des monsters sans equivalent dans le medium. Chaque page est un travail artistique majeur. C'est une des raisons pour lesquelles les volumes ont souvent pris des mois ou des annees.",
    "arcs": [
      {"arc": "Pre-Golden Age (1989-1992)", "summary": "Introduction de Guts adulte. Ton horrifique immédiat — bete de torture, armure de berserk, creatures de l'Abysse"},
      {"arc": "Golden Age (1992-1997)", "summary": "Flashback — la jeunesse de Guts, la Troupe du Faucon, Griffith. Le plus beau recit d'amitie du manga suivi de la trahison la plus dechirante : l'Eclipse"},
      {"arc": "Black Swordsman to Conviction (1997-2001)", "summary": "Vengeance solitaire, Guts vs l'Inquisition, retrouvaille avec Casca"},
      {"arc": "Millennium Falcon / Fantasia (2002-2021)", "summary": "Voyage avec compagnons, ile de la magie, Elfhelm. Ralentissement narratif mais enrichissement du monde"}
    ],
    "themes": [
      "La survie et le refus de la fatalite — Guts choisit de vivre malgre tout",
      "Le sacrifice : peut-on trahir ses proches pour un reve ?",
      "La lumiere et les tenebres comme dualite inseparable (Guts/Griffith)",
      "Qu'est-ce qui fait un etre humain quand on est depouille de tout ?"
    ],
    "griffith": "L'un des antagonistes les plus complexes du medium — charismatique, visionnaire, capable du pire pour son reve. Pas un monstre simple : un humain qui choisit de devenir monstre."
  },
  [
    {"prompt": "Berserk est-il trop violent pour etre lu ?", "answer": "Berserk est explicit — violence graphique intense, contenu adulte, horreur body-horror. Ce n'est pas un manga a mettre entre toutes les mains. Mais la violence n'est pas gratuite : elle a un poids emotionnel et moral. Chaque traumatisme subi par Guts justifie la rage qui le propulse. L'Eclipse (arc Golden Age) est un des moments les plus durelement impactants du medium — pas pour le spectacle mais pour ce qu'il signifie sur la trahison et la perte. Si tu peux tolerer le contenu : Berserk recompense par une epaisseur narrative et artistique que peu d'oeuvres atteignent. Commencer par l'arc Golden Age (volumes 3-14) pour comprendre le coeur de l'oeuvre avant la noirceur des premiers volumes."},
    {"prompt": "Berserk sera-t-il termine maintenant que Miura est decede ?", "answer": "Oui — mais pas par Miura. Son ami proche Kouji Mori, a qui Miura avait raconte la fin de l'histoire, continue la serie avec le studio Young Animal. Les chapitres post-Miura (depuis 2022) sont controverses — certains trouvent le style acceptable, d'autres voient la difference. La question reste : peut-on terminer l'oeuvre d'un autre auteur de facon authentique ? La reponse n'est pas simple. Ce qui est certain : Mori connait la conclusion prévue. L'oeuvre sera close. Miura avait dit que la fin de Berserk serait 'sombre mais pas desespErée'."}
  ],
  ["Berserk", "Miura", "Guts", "Griffith", "dark fantasy", "seinen"]
))

# ── 9. manga / studio_ghibli_anime ──────────────────────────────────────────────
save("culture/manga/studio_ghibli_anime.json", ku(
  "studio_ghibli_anime", "manga",
  "Studio Ghibli et l'animation japonaise",
  "Studio Ghibli est le studio d'animation japonais le plus venere mondialement — cofonde par Hayao Miyazaki et Isao Takahata. Ses films combinent animation a la main d'une qualite extreme, recits poetiques et themes universels. 'Spirited Away' (2001) reste le seul film anime a avoir remporte l'Oscar du meilleur film d'animation.",
  "Studio Ghibli est un studio d'animation japonais fonde en 1985 par Hayao Miyazaki, Isao Takahata et Toshio Suzuki, considere comme le studio d'animation le plus influent en dehors de Disney/Pixar. Ses films se caracterisent par une animation 2D d'exception, des protagonistes feminins forts et independants, et des themes qui touchent a l'enfance, l'environnement et la relation entre civilisation et nature.",
  {
    "miyazaki_filmography": [
      {"film": "Nausicaa de la Vallee du Vent (1984)", "themes": "Ecologie, coexistence, sacrifice"},
      {"film": "Mon Voisin Totoro (1988)", "themes": "Enfance, nature, magie du quotidien — icone culturelle mondiale"},
      {"film": "Le Voyage de Chihiro (2001)", "themes": "Identite, travail, monde des esprits. Oscar + Lion d'Or. Film le plus rentable de l'histoire japonaise jusqu'a Demon Slayer"},
      {"film": "Princesse Mononoke (1997)", "themes": "Conflit nature/civilisation, ambiguite morale, pas de manichéisme"},
      {"film": "Le Chateau Ambulant (2004)", "themes": "Anti-guerre, amour et transformation, complexite des antagonistes"},
      {"film": "Kiki la Petite Sorciere (1989)", "themes": "Autonomie, identite, doute dans la croissance"},
      {"film": "Le Garcon et le Heron (2023)", "themes": "Deuil, monde interieur, transmission — dernier film de Miyazaki"}
    ],
    "takahata_filmography": [
      {"film": "Le Tombeau des Lucioles (1988)", "themes": "Japon WWII, survie, denouement tragique — un des films d'animation les plus durs jamais produits"},
      {"film": "Pompoko (1994)", "themes": "Urbanisation, nature, folklore japonais"},
      {"film": "Le Conte de la Princesse Kaguya (2013)", "themes": "Desir, nature, vie et mort. Animation aquarelle unique"}
    ],
    "ghibli_style": "Miyazaki n'utilise pas de storyboard au debut — le film emerge pendant la production. Animation a la main a 24 images/seconde pour les scenes critiques. Jamais de manichéisme dans les antagonistes — il n'y a pas de 'vilain absolu' dans la filmographie Ghibli."
  },
  [
    {"prompt": "Par quel film Ghibli commencer ?", "answer": "Depend de l'age et des sensibilités : Enfants (4-10 ans) : Mon Voisin Totoro — universel, doux, magique. Adolescents/adultes : Le Voyage de Chihiro — porte d'entree parfaite pour la profondeur Ghibli dans un film accessible. Amateur de nature/philosophie : Princesse Mononoke — la vision la plus complexe et la moins enfantine. Amateur de tristesse necessaire : Le Tombeau des Lucioles — devastateur mais chef-d'oeuvre. Pour le vertige artistique pur : Le Conte de la Princesse Kaguya de Takahata — animation aquarelle unique, meditation sur la vie."},
    {"prompt": "Quelle est la vision du monde de Miyazaki dans ses films ?", "answer": "Quelques themes recurrents lisibles dans l'oeuvre : (1) La nature a une conscience et une legitimite propres — les humains ne sont pas au sommet, (2) Pas de manichéisme — dans Princesse Mononoke ou Le Chateau Ambulant, il n'y a pas de 'bon' et de 'mechant', seulement des perspectives differentes en conflit, (3) L'enfance comme etat de perception ouverte — les enfants voient ce que les adultes ont appris a ne plus voir (Totoro, Chihiro), (4) La guerre est une abomination — present dans presque tous ses films, de Nausicaa a Le Vent se Leve, (5) Le travail comme dignite — Chihiro doit 'travailler' pour exister dans le monde des esprits."}
  ],
  ["Ghibli", "Miyazaki", "anime", "Spirited Away", "Totoro", "animation"]
))

# ── 10. manga / anime_culture ─────────────────────────────────────────────────
save("culture/manga/anime_culture.json", ku(
  "anime_culture", "manga",
  "Culture anime et otaku",
  "La culture anime est un ecosysteme culturel complet — au-dela des anime eux-memes : conventions (Comic Market, Japan Expo), merchandise, cosplay, figures, dakimakura, light novels, visual novels. Le terme 'otaku', pejoratif au Japon, est reapproprie positivement en Occident.",
  "La culture anime designe l'ensemble des pratiques culturelles, sociales et economiques gravitant autour de l'animation japonaise et du manga — incluant le fandom, les conventions, le merchandise, le cosplay, les light novels, les visual novels, et la culture numerique des simuls cast et fansubs. Elle constitue une sous-culture globale majeure depuis les annees 1990.",
  {
    "key_concepts": [
      {"term": "Otaku", "japan": "Pejoratif — personne obsessionnelle et socialement recluse. Connotation tres negative au Japon depuis les annees 1980", "west": "Reapproprié positivement — passionné de manga/anime/culture japonaise"},
      {"term": "Fansub", "description": "Sous-titrage amateur de series japonaises avant l'exportation officielle — pratique illégale mais historiquement decisive dans la diffusion mondiale de l'anime"},
      {"term": "Simulcast", "description": "Diffusion simultanee de l'anime au Japon et à l'international via Crunchyroll, Netflix. A largement remplace les fansubs"},
      {"term": "Light Novel", "description": "Format litteraire japonais entre roman et manga — ecriture simple, illustrations. Souvent adapte en anime (Re:Zero, SAO, Overlord)"},
      {"term": "Visual Novel", "description": "Jeu video narratif avec choix multiples — texte + illustrations. Souvent adapte en anime (Clannad, Steins;Gate, Fate/stay night)"},
      {"term": "Comiket", "description": "Comic Market — convention doujinshi (creations amateurs) a Tokyo deux fois par an. 700 000 participants sur 3 jours"}
    ],
    "platforms": {
      "Crunchyroll": "Principal streamer legal d'anime mondial — simulcasts, catalogue historique",
      "Netflix_anime": "Co-productions et exclusivités (Arcane, Cyberpunk Edgerunners, Oni)",
      "France": "Japan Expo a Paris — la plus grande convention anime hors Japon. Histoire d'amour particuliere France-manga (Club Dorothee, importations precoces)"
    }
  },
  [
    {"prompt": "Comment commencer a s'interesser a l'anime si on n'a jamais regarde ?", "answer": "Par le bon point d'entree selon tes gouts : (1) Tu aimes les recits de superheros/action : My Hero Academia — shonen classique mais accessible, plaisir immediat, (2) Tu aimes les thrillers psychologiques : Death Note — 37 episodes, recit complet, accessible aux non-initiés, (3) Tu aimes les oeuvres d'art anime : Studio Ghibli, commence par Chihiro, (4) Tu veux quelque chose de court et complet : Fullmetal Alchemist Brotherhood (64 episodes, fin satisfaisante), unanimement reconnu comme reference. Plateforme : Crunchyroll pour les series recentes, Netflix pour les Ghibli et co-productions."},
    {"prompt": "Qu'est-ce que le phenomene Japan Expo en France ?", "answer": "Japan Expo est la plus grande convention de culture japonaise hors du Japon — 270 000 visiteurs en 2023 au parc des expositions de Villepinte. Elle decoule de la relation particuliere France-Japon dans le manga : la France est le 2e marche mondial du manga apres le Japon (avant les USA) grace a la diffusion precoce via la TV (Club Dorothee, Goldorak). Programmes : concerts, expositions, stands editeurs et createurs, competitions de cosplay, panels. C'est le reflet d'un marche francais du manga tres mature — les editeurs japonais considerent la France comme leur ambassadeur europeen."}
  ],
  ["anime", "otaku", "Crunchyroll", "Comiket", "Japan Expo", "fandom"]
))

# ── 11. manga / jujutsu_kaisen ────────────────────────────────────────────────
save("culture/manga/jujutsu_kaisen.json", ku(
  "jujutsu_kaisen", "manga",
  "Jujutsu Kaisen (Gege Akutami)",
  "Jujutsu Kaisen est le manga shonen phare des annees 2020 — il suit Yuji Itadori, lyceen qui avale un doigt du demon Ryomen Sukuna pour sauver ses camarades et devient son receptacle. Reconnu pour ses combats visuellement ambitieux et sa volonte de tuer des personnages principaux sans prevenir.",
  "Jujutsu Kaisen est un manga shonen de Gege Akutami, publie dans Weekly Shonen Jump depuis 2018. Il se deroule dans un Japon contemporain ou des Maudit (Curses) — manifestations d'energie negative humaine — menacent la population. Les sorciers de l'exorcisme (Jujutsu Sorcerers) utilisent l'energie maudite pour les combattre. Yuji Itadori est propulse dans ce monde apres avoir ingere un doigt du demon Ryomen Sukuna.",
  {
    "power_system": {
      "cursed_energy": "Energie negative generee par les emotions humaines negatives — peur, haine, desespoir",
      "techniques": "Innate Technique — chaque sorcier a une technique unique heritee a la naissance",
      "domain_expansion": "Technique ultime — creer une manifestation de sa propre technique qui garantit que chaque attaque touche dans l'espace cree",
      "sukuna": "Roi des Maledictions — antagoniste principal, le plus puissant jamais existé"
    },
    "arc_shibuya": "L'arc de Shibuya (saison 2 anime) est considere par les fans comme l'un des meilleurs arcs de bataille du shonen moderne — plusieurs protagonistes majeurs tues en quelques chapitres, sans signes avant-coureurs.",
    "themes": [
      "La mort comme constante — Jujutsu est reconnu pour tuer des personnages principaux aimes sans prevention",
      "Le sacrifice des sorciers — vie courte et vide de reconnaissance publique",
      "Qu'est-ce qu'une vie qui vaut d'etre vecue ? (question de Wasuke Itadori a Yuji)",
      "La joie comme choix philosophique face a la mort certaine"
    ]
  },
  [
    {"prompt": "Pourquoi tout le monde parle de Jujutsu Kaisen en ce moment ?", "answer": "Trois raisons : (1) L'anime MAPPA — apres Demon Slayer ufotable, MAPPA a etabli un nouveau standard avec Jujutsu Kaisen saison 1 (2020) puis l'arc de Shibuya (saison 2, 2023) qui est cinematographiquement ambitieux, (2) Les stakes — JJK n'hesite pas a tuer des personnages principaux tres aimes, ce qui cree un sentiment permanent de tension. L'arc Shibuya a provoque des reactions virales sur les reseaux sociaux, (3) Le power system elegant — domain expansions et innate techniques sont originaux et visuellement frappants. Point d'entree : saison 1 anime ou chapitres 1-63 du manga."},
    {"prompt": "Qui est Ryomen Sukuna et pourquoi est-il important ?", "answer": "Sukuna est le Roi des Maledictions — l'etre maudit le plus puissant qui ait jamais existe. Mort il y a 1000 ans, son corps a ete decime en 20 doigts qui sont devenus des objets maudits quasi-indestructibles. Yuji avale un doigt au debut et partage son corps avec lui. La relation est centrale : Sukuna est omnipotent, cynique, contempteur des humains, et pourtant fasciné par Yuji qui refuse de lui ceder. Il represente la force brute sans moral, la beauté nihiliste du combat pur. Dans l'arc Shibuya, quand Sukuna prend le controle complet — c'est un des moments les plus devastateurs du manga moderne."}
  ],
  ["Jujutsu Kaisen", "Akutami", "Itadori", "Sukuna", "domain expansion", "MAPPA"]
))

# ── 12. manga / manga_vs_webtoon ───────────────────────────────────────────────
save("culture/manga/manga_vs_webtoon.json", ku(
  "manga_vs_webtoon", "manga",
  "Manga vs Webtoon vs Manhwa",
  "Le manga japonais partage le marche mondial du comics asiatique avec le manhwa coreen (souvent en format webtoon vertical) et le manhua chinois. Ces trois formats ont des structures economiques, des styles visuels et des conventions narratives differentes.",
  "Le marche mondial du comics asiatique distingue le manga (Japon), le manhwa (Coree du Sud, souvent webtoon vertical) et le manhua (Chine). Le webtoon est un format numerique scroll vertical ne en Coree (Naver Webtoon, 2004) qui a revolutionne la distribution de BD en ligne et genere des oeuvres mondialement lues.",
  {
    "manga_japan": {
      "format": "Noir et blanc, horizontal, volumes de 200 pages (tankobon)",
      "distribution": "Magazines hebdomadaires puis tankobon puis numerique",
      "reading_direction": "Droite a gauche",
      "market": "Marche domestique fort, exportation massive",
      "style": "Lignes dynamiques, hatching, speed lines, expressivité emotionnelle codifiee"
    },
    "manhwa_korea": {
      "format": "Souvent en couleurs, format scroll vertical (webtoon)",
      "distribution": "Nativement numerique — Naver Webtoon, Kakao Webtoon, Tapas",
      "reading_direction": "Gauche a droite (meme que BD occidentale)",
      "market": "Croissance explosive internationale — Solo Leveling, True Beauty, Tower of God",
      "style": "Decoupage optimise pour le scroll : panneaux larges, transitions verticales, couleur omniprésente"
    },
    "notable_webtoons": [
      "Solo Leveling — isekai/hunter, adaptation anime 2024, phenomene mondial",
      "Tower of God — fantasy epique, sur Crunchyroll",
      "Noblesse — surnaturel, adapte en anime",
      "True Beauty — romcom shojo equivalent"
    ]
  },
  [
    {"prompt": "Quelle est la difference entre manga et webtoon ?", "answer": "Differences principales : (1) Format physique — manga : noir et blanc, pages horizontales, lecture droite a gauche. Webtoon : couleurs, scroll vertical infini, lecture verticale comme un fil Instagram, (2) Distribution — manga : magazine papier puis volume physique. Webtoon : natif numerique, souvent gratuit avec systeme de 'fast pass' pour les chapitres recents, (3) Style narratif — le webtoon est conçu pour le scroll rapide : panneaux plus larges, moins d'informations par page, rythme plus cinematographique. Le manga pack plus d'information par page. Le webtoon coreen est la forme de BD a la plus forte croissance mondiale depuis 2015."},
    {"prompt": "Solo Leveling vaut-il la peine d'etre lu ?", "answer": "Oui si tu veux une power fantasy bien executee — pas une profondeur narrative a la Berserk ou One Piece. Solo Leveling (Chugong/Dubu) est le manhwa qui a convaincu beaucoup d'occidentaux que le format webtoon etait serieux. Son attrait : (1) Protagonist regression — Sung Jinwoo commence comme le chasseur le plus faible, progresse exponentiellement, (2) Art de Dubu — combats tres cinematographiques, lisibles et beaux, (3) Power system satisfaisant et clair. Ses limites : personnages secondaires peu developpes, protagoniste godlike parfois desequilibrant la tension. Adaptation anime 2024 (A-1 Pictures) tres fidelee et de bonne qualite."}
  ],
  ["webtoon", "manhwa", "Solo Leveling", "Naver", "manga vs webtoon", "coreen"]
))

# ── 13. manga / junji_ito_horror ───────────────────────────────────────────────
save("culture/manga/junji_ito_horror.json", ku(
  "junji_ito_horror", "manga",
  "Junji Ito — maitre de l'horreur manga",
  "Junji Ito est le maitre inconteste de l'horreur manga — ses histoires courtes et ses recits moyens explorent la body horror, le surnatural et la psychologie de la terreur avec un talent graphique et narratif unique. 'Uzumaki' et 'Gyo' sont ses oeuvres les plus connues.",
  "Junji Ito est un auteur japonais de manga d'horreur ne en 1963, dont l'oeuvre est caracterisee par une esthetique de la body horror (transformation horrifique du corps humain), des premises narratives absurdes poussees a leur extreme logique et un style de dessin hyperrealiste qui ancre l'impossible dans le quotidien.",
  {
    "major_works": [
      {"title": "Uzumaki (1998-1999)", "summary": "Une ville obsedee par les spirales — les habitants commencent a se transformer de facon spirale. Horreur cosmique absurde menee jusqu'a sa conclusion inEvitable", "status": "Chef-d'oeuvre, adapte en anime 4 episodes"},
      {"title": "Gyo (2001-2002)", "summary": "Des poissons a pattes mecaniques envahissent le Japon. Body horror et decomposition. Plus visceral et moins construit qu'Uzumaki"},
      {"title": "Soichi", "summary": "Personnage comique-horrifique — enfant sadique avec des clous dans la bouche. Relache comique dans l'oeuvre sinistre"},
      {"title": "Tomie", "summary": "Femme eternellement belle et eternellement assassinee qui regenere toujours. Metaphore de l'obsession et de la peur du feminin"},
      {"title": "Histoires courtes", "summary": "Le format ideal Ito — 20-40 pages, une premise, developpement inevitabe, chute. 'La Ballade du Vieux Bateeau', 'Le Manoir de la Montagne', 'Shiver'"}
    ],
    "narrative_technique": "Ito part d'une premise quotidienne (une spirale, une odeur, un trou) et la pousse sans relache vers ses consequences les plus horribles, sans jamais expliquer ou resoudre. Le non-explication est centrale — l'horreur cosmique fonctionne parce qu'elle n'a pas de sens humain comprehensible.",
    "influence": "Stephen King a dit que Junji Ito est l'auteur qui l'a le plus terrifie. Son oeuvre est traduite en 20+ langues et a inspire des generations d'auteurs d'horreur visuels."
  },
  [
    {"prompt": "Par quelle oeuvre de Junji Ito commencer ?", "answer": "Commencer par les histoires courtes pour calibrer sa tolerance. Recueil 'Shiver' ou 'Smashed' (publies par VIZ Media) — chaque histoire est independante, 20-40 pages, tu peux t'arreter si trop. Si ca passe : Uzumaki — l'oeuvre la plus construite et la plus fascinante conceptuellement. Si tu veux aller loin : Tomie — la plus psychologiquement complexe sur le long terme. Eviter Gyo comme point d'entree — c'est le plus visceral et le moins construit. Lire de preference seul, la nuit. Junji Ito marche beaucoup mieux dans le silence."},
    {"prompt": "Qu'est-ce qui rend l'horreur de Junji Ito differente des autres mangas d'horreur ?", "answer": "Deux specificites majeures : (1) L'absurde logique — ses premises sont souvent absurdes (une spiral qui rend fou, des poissons a pattes mecaniques) mais il les suit jusqu'a leur conclusion la plus extremE sans jamais virer au comedique ou a l'explication rassurante. Cette perseverance dans l'impossible cree une horreur surrealiste sans equivalent, (2) La body horror hyperrealiste — Ito dessine le corps humain en transformation avec un soin anatomique qui ancre le fantastique dans quelque chose de visceralement credible. La technique de dessin au trait fin et aux hachures denses cree une texture qui contraste avec les autres styles de manga — rien ne ressemble a Junji Ito."}
  ],
  ["Junji Ito", "horreur", "Uzumaki", "body horror", "manga", "terreur"]
))

# ── 14. manga / mangaka_creation ───────────────────────────────────────────────
save("culture/manga/mangaka_creation.json", ku(
  "mangaka_creation", "manga",
  "Profession mangaka — creer un manga",
  "Etre mangaka professionnel est l'un des metiers les plus exigeants du secteur creatif — rythme de production extreme (un chapitre par semaine pour les plus importants), pression commerciale des editeurs et des classements, risque d'annulation. Beaucoup d'auteurs sacrifient leur sante pour leurs oeuvres.",
  "La profession de mangaka (auteur de manga) se caracterise par un modele economique de serialisation dans des magazines hebdomadaires ou mensuels, avec une pression de production et de performance commerciale tres elevee (classements lecteurs, risque d'annulation), souvent realise en equipe de 2-6 personnes (mangaka + assistants).",
  {
    "production_model": {
      "weekly_shonen": "Un chapitre de 15-20 pages par semaine. Rythme intenable seul — les assistants font les decors et les trames, le mangaka fait les personnages et les cases-cles",
      "monthly": "Un chapitre de 30-50 pages par mois — permet plus de detail et de qualite",
      "assistants": "Les grands mangakas ont 3-6 assistants. Les assistants sont souvent des auteurs en formation qui apprennent en travaillant pour un maitre"
    },
    "editorial_process": [
      "Le mangaka soumet des ideas a l'editeur (tantou henshusha — editeur en charge)",
      "L'editeur joue un role central — challenge, propose, rejette. C'est un co-createur invisible",
      "Les votes lecteurs (popularity polls dans les magazines) influencent directement la duree et l'evolution des series",
      "Les series impopulaires sont annulees — parfois en quelques semaines"
    ],
    "famous_struggles": [
      "Miura (Berserk) — hiatus frequents de mois/annees pour preserver sa sante et la qualite",
      "Togashi (Hunter x Hunter) — maladies chroniques dues au surmenage, hiatus records",
      "Kishimoto (Naruto) — confessed years of sleep deprivation"
    ]
  },
  [
    {"prompt": "Pourquoi Hunter x Hunter est en hiatus depuis si longtemps ?", "answer": "Yoshihiro Togashi souffre de problemes de dos chroniques — hernies discales liées aux annees de travail intensif pendant Yu Yu Hakusho (1990-1994) et HxH (depuis 1998). Les hiatus (pauses de publication) se sont multiplies depuis 2006 — la serie a ete en pause plus qu'elle n'a ete publiée sur 20 ans. Togashi publie parfois sur X/Twitter des pages dessinées 'a la main', montrant son envie de continuer malgré les douleurs. Il a repris la publication officielle en 2022 pour l'arc Succession War, en petits lots. C'est l'exemple le plus connu du prix physique de la serialisation manga au niveau le plus haut."},
    {"prompt": "Comment devenir mangaka ?", "answer": "Voies classiques : (1) Concours des magazines — Weekly Shonen Jump, Young Jump, etc. organisent des competitions regulieres pour decouvrir de nouveaux auteurs. Un one-shot gagnant peut etre propose en serialisation, (2) Assistant chez un grand auteur — apprendre en aidant pendant 2-5 ans, (3) Publication independante (doujinshi, web manga) pour construire une audience, puis approcher des editeurs, (4) Aujourd'hui : webtoon et plateformes numeriques permettent une publication directe mondiale (Tapas, Webtoon, Pixiv). Competences requises : dessin, narration, regularite de production, resistance au rejet. La serialisation pro n'est viable que si tu peux tenir un rythme extreme — la narration et le dessin doivent etre automatises."}
  ],
  ["mangaka", "creation", "serialisation", "assistants", "editeur", "metier"]
))

# ── 15. manga / franco_belge_vs_manga ─────────────────────────────────────────
save("culture/manga/franco_belge_vs_manga.json", ku(
  "franco_belge_vs_manga", "manga",
  "BD franco-belge vs Manga — differences et influences",
  "La bande dessinee franco-belge (Tintin, Asterix, Les Schtroumpfs, Spirou) et le manga japonais sont les deux grandes traditions mondiales de BD non-americaine. Elles ont des modeles editoriaux, des styles graphiques et des relations a l'auteur fondamentalement differents, et s'influencent mutuellement depuis les annees 1990.",
  "La comparaison BD franco-belge / manga eclaire deux traditions editoriales et artistiques distinctes : l'album franco-belge (format A4 couleur, 46-62 pages, publication 1-2 ans) vs la serialisation manga (magazine hebdomadaire, N&B, volumes annuels). Deux relations a l'auteur, deux rythmes, deux marches.",
  {
    "franco_belge": {
      "format": "Album 46-62 pages, A4, couleur, cartoné",
      "rythme": "1 album tous les 1-5 ans selon l'auteur",
      "auteur": "Auteur unique (souvent scénariste + dessinateur) avec grande liberte editoriale",
      "style": "Ligne claire (Herge, Tintin), style cartoon (Lucky Luke), BD realiste (Blake et Mortimer)",
      "modele_eco": "Vente d'albums en librairie — marche solide en France, Belgique, pays francophones",
      "references": ["Tintin (Herge)", "Asterix (Goscinny/Uderzo)", "Lucky Luke", "Spirou", "Les Schtroumpfs", "Blacksad", "XIII", "Largo Winch"]
    },
    "mutual_influences": [
      "France est le 2e marche manga mondial — influence retour sur les auteurs japonais",
      "Le 'global manga' et 'OEL manga' — auteurs occidentaux qui dessinent dans le style manga",
      "L'ONA (Original Net Animation) et les co-productions Netflix/japonaises creent des hybrides",
      "Moebius (Jean Giraud) a influence Miyazaki, Otomo, Matsumoto — la BD europeenne comme source d'inspiration pour la SF manga"
    ]
  },
  [
    {"prompt": "La BD franco-belge et le manga sont-ils en competition ?", "answer": "En marche, oui — le manga a pris une part considerable du marche franco-belge de la BD depuis les annees 2000, representant 50-60% des ventes de BD en France. Les auteurs franco-belges ont parfois exprime des tensions. Artistiquement, les deux traditions se respectent et s'influencent : Moebius a directement inspire Miyazaki et Otomo. Akira a influence une generation d'auteurs franco-belges. Des editeurs comme Kana (BD manga Flammarion) ont ponté les deux cultures. C'est moins une competition qu'une cohabitation productive — le lecteur francais peut aimer Tintin le matin et One Piece le soir."},
    {"prompt": "Qu'est-ce que la 'ligne claire' dans la BD franco-belge ?", "answer": "La ligne claire est un style graphique codifie par Herge (Tintin) caracterise par : contours nets et uniformes (pas de variation d'epaisseur de trait), aplats de couleurs (pas de hachures ou d'ombres complexes), visages simples et expressifs contrastant avec des decors detailles et realistes. Elle vise la lisibilite maximale et la neutralite emotionnelle du trait. Hommage moderne : Blacksad (Guarnido/Canales) — ligne claire dans un univers noir anthropomorphique des annees 40. La ligne claire est aussi une ecole narrative : privilegier la clarte narrative a l'expressivité graphique — tout ce qui n'aide pas le recit est supprime."}
  ],
  ["BD franco-belge", "Tintin", "Asterix", "ligne claire", "marche manga", "Herge"]
))

print("\n=== Domaine 'culture/manga' : 15 fichiers crees ===")
