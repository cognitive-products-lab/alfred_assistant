"""
Nouveaux domaines : knowledges/cuisine/
cuisine/fondamentaux + cuisine/monde + cuisine/asiatique
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku(stem, domain, subdomain, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.{domain}.{subdomain}.{stem}",
      "title": title,
      "domain": domain,
      "subdomain": subdomain,
      "status": "validated",
      "summary": summary,
      "core_definition": core_def,
      "knowledge": knowledge,
      "example_answers": examples,
      "response_guidance": {
        "tone": "pratique, sensoriel, chaleureux — comme partager une recette avec un ami qui sait cuisiner",
        "structure": ["expliquer la technique ou le principe", "donner un exemple concret ou une recette", "donner un conseil pratique actionnable"],
        "avoid": ["jargon professionnel non explique", "recettes sans contexte", "etre trop vague"]
      },
      "tags": tags + ["cuisine"],
      "related_knowledge_units": []
    }

# ─── FONDAMENTAUX ─────────────────────────────────────────────────────────────

save("cuisine/fondamentaux/couteaux_et_decoupe.json", ku(
  "couteaux_et_decoupe", "cuisine", "fondamentaux",
  "Couteaux et techniques de decoupe",
  "La maitrise du couteau est la compétence de base la plus rentable en cuisine — une decoupe reguliere assure une cuisson homogene et une meilleure presentation. Le couteau de chef (20cm) couvre 90% des usages quotidiens.",
  "Les techniques de decoupe en cuisine comprennent la selection du couteau adapte a chaque usage, la tenue correcte de la lame et de l'aliment (griffe du chat), et les coupes classiques (julienne, brunoise, chiffonnade, mirepoix) qui permettent une cuisson homogene et une presentation soignee.",
  {
    "essential_knives": [
      {"knife": "Couteau de chef (8-10 pouces)", "use": "Couteau principal — legumes, viandes, herbes. 90% des usages"},
      {"knife": "Couteau d'office (3-4 pouces)", "use": "Travaux de precision — peler, eplucher, couper petit"},
      {"knife": "Couteau a pain (scie)", "use": "Pain, tomates, agrumes — ne jamais utiliser pour autre chose"},
      {"knife": "Couteau filet de sole", "use": "Poissons — lame flexible pour longer les aretes"}
    ],
    "blade_grip": "Pinch grip : tenir la lame entre pouce et index a la base, les 3 autres doigts sur le manche. Plus de controle, moins de fatigue que tenir par le manche seul.",
    "food_grip": "Griffe du chat : doigts replies, phalange en contact avec la lame, extremites protegees. Le couteau glisse sur la jointure, jamais sur les bouts des doigts.",
    "classic_cuts": [
      {"name": "Julienne", "size": "Batons 3mm x 3mm x 5cm", "use": "Wok, salades, garnitures"},
      {"name": "Brunoise", "size": "Des 2-3mm", "use": "Farces, sauces, garnitures fines"},
      {"name": "Mirepoix", "size": "Des 1-1.5cm", "use": "Bouillons, braises, fonds"},
      {"name": "Chiffonnade", "size": "Herbes ou feuilles en lanières fines", "use": "Garniture fraiche"},
      {"name": "Paysanne", "size": "Carres 1cm x 1cm x 3mm", "use": "Potages, legumes d'accompagnement"}
    ]
  },
  [
    {"prompt": "Pourquoi ma decoupe est-elle irreguliere et comment m'ameliorer ?", "answer": "Deux causes principales : (1) Couteau mal aiguise — un couteau tranchant est plus facile a controler et plus sur qu'un couteau emoussé qui glisse. Aiguiser ou faire aiguiser regulierement, (2) Technique de grip — essayer la 'griffe du chat' (doigts replies, jointures guident la lame) et le pinch grip sur la lame. Exercice pratique : couper lentement une carotte en rondelles en visant une epaisseur reguliere sur toute la longueur. La regularite vient de la pratique repetee, pas du talent. 10 minutes par jour pendant 2 semaines transforment le geste."},
    {"prompt": "Quel couteau choisir pour commencer si je n'ai qu'un budget limité ?", "answer": "Un seul couteau : couteau de chef 20cm, budget 30-60 euros. Marques honnnetes dans cette gamme : Victorinox Fibrox (tres populaire, excellent rapport qualite-prix), Opinel Intempora. Ne pas acheter un set de 6 couteaux bas de gamme — un bon couteau de chef vaut mieux que 6 mauvais. A ajouter si budget : couteau d'office 10cm (15-25 euros). Puis investir dans un aiguiseur a pierre ou un fusil d'affutage. Le couteau mal entretenu perd toute valeur — l'entretien est aussi important que l'achat initial."}
  ],
  ["couteau", "decoupe", "brunoise", "julienne", "technique", "fondamentaux"]
))

save("cuisine/fondamentaux/cuissons_fondamentales.json", ku(
  "cuissons_fondamentales", "cuisine", "fondamentaux",
  "Modes de cuisson fondamentaux",
  "Maitriser les 6 modes de cuisson fondamentaux (poeler, rotir, mijoter, steamer, frire, griller) permet d'adapter n'importe quel ingredient a l'effet souhaite — croustillant, fondant, juteux, caramelise. Chaque mode a sa logique physique et ses erreurs classiques.",
  "Les modes de cuisson en cuisine se divisent en cuissons seches (four, grill, poele sans liquide), cuissons humides (vapeur, pochage, mijotage) et cuissons grasses (friture, saute), chacune exploitant differents mecanismes de transfert de chaleur pour obtenir des textures et des saveurs specifiques.",
  {
    "cooking_methods": [
      {
        "method": "Sauter / Poeler",
        "technique": "Matiere grasse tres chaude, petites pieces, mouvement continu ou pas selon la viande",
        "key_point": "Secher les aliments avant — l'humidite empeche la caramelisation (reaction de Maillard)",
        "errors": "Poele trop froide (bouilli au lieu de saute), trop d'aliments en meme temps (temperature chute)"
      },
      {
        "method": "Rotir (four)",
        "technique": "Chaleur sèche enveloppante, arrosage regulier pour proteger la surface",
        "key_point": "Monter en temperature progressivement pour les grosses pieces, ou saisir d'abord sur le feu",
        "errors": "Ouvrir le four trop souvent, ne pas laisser reposer la viande avant de couper"
      },
      {
        "method": "Mijoter / Braiser",
        "technique": "Longue cuisson douce dans un liquide, a couvert, entre 80-95 degres",
        "key_point": "Les viandes dures (collagene) deviennent fondantes — jamais a ebullition vive",
        "errors": "Ebullition trop forte (viande filandreuse), pas assez de temps"
      },
      {
        "method": "Vapeur",
        "technique": "Vapeur d'eau a 100 degres, aliment au-dessus du liquide, jamais en contact",
        "key_point": "Preserve le plus de vitamines et l'humidite naturelle de l'aliment",
        "errors": "Cuit en avance et laisse se dessecher, eau qui bout a sec"
      },
      {
        "method": "Friture",
        "technique": "Immersion dans l'huile entre 160 et 180 degres",
        "key_point": "Temperature clef — trop froide: gras; trop chaude: brule dehors, cru dedans. Thermometre indispensable",
        "errors": "Trop d'aliments en meme temps (temperature chute), huile a mauvaise temperature"
      },
      {
        "method": "Grill / Plancha",
        "technique": "Surface tres chaude, contact direct, marquage",
        "key_point": "Ne pas bouger avant que la piece se detache naturellement — elle colle tant qu'elle n'est pas marquee",
        "errors": "Trop manipuler, piece mal sechee"
      }
    ],
    "maillard_reaction": "La reaction de Maillard (> 140°C) est la caramelisation des proteines qui cree les saveurs et la couleur brune. Elle necessite une surface SECHE — c'est pourquoi on seche la viande et on chauffe fort avant d'ajouter les aliments."
  },
  [
    {"prompt": "Pourquoi ma viande ne dore-t-elle pas en poele ?", "answer": "Trois causes possible : (1) Poele pas assez chaude — l'huile doit fremer et presque fumer avant d'ajouter la viande, (2) Viande trop humide — eponger avec du papier absorbant avant cuisson (l'humidite fait de la vapeur qui empeche la caramelisation), (3) Trop de pieces en meme temps — la temperature chute, les aliments rendent leur jus et bouillent. Solution : poele bien chaude, viande sechée, cuire en petites quantites si necessaire. La regle : si ca siffle fort a l'ajout, bonne temperature. Si ca crepite doucement, trop froid."},
    {"prompt": "Comment cuire un steak parfait ?", "answer": "Etapes : (1) Sortir 30 min du frigo (temperature ambiante), (2) Secher a fond avec papier absorbant, saler, (3) Poele en fonte ou acier tres chaude avec peu d'huile (ou ghee), (4) Deposer le steak — ne pas toucher pendant 2-3 min, laisser se detacher naturellement, (5) Retourner une seule fois, (6) Ajouter beurre + thym + ail les 30 dernieres secondes, arroser en inclinant la poele, (7) REPOSER sous papier alu 5 min avant de couper — le jus se redistribue. Cuissons : 2 min/face = saignant, 3 min = a point, 4 min = bien cuit. Thermometre : 52°C = saignant, 58°C = a point."}
  ],
  ["cuisson", "Maillard", "sauter", "rotir", "mijoter", "friture"]
))

save("cuisine/fondamentaux/sauces_bases.json", ku(
  "sauces_bases", "cuisine", "fondamentaux",
  "Sauces de base — les 5 sauces meres",
  "Auguste Escoffier a codifie 5 sauces meres dont decoulent la plupart des sauces de la cuisine classique europeenne. Les maitriser donne acces a une palette infinie de variations et comprendre leur logique permet d'improviser avec confiance.",
  "Les cinq sauces meres de la cuisine classique (Bechamel, Veloute, Espagnole, Sauce tomate, Hollandaise) sont les preparations de base dont derivent la quasi-totalite des sauces classiques europeennes, selon la codification d'Escoffier (1903). Elles reposent sur des techniques de liaison (roux, reduction, emulsion) applicables au-dela des recettes specifying.",
  {
    "mother_sauces": [
      {
        "name": "Bechamel",
        "base": "Roux blanc (beurre + farine) + lait chaud",
        "derivatives": ["Sauce Mornay (+fromage)", "Sauce creme (+creme)", "Sauce soubise (+oignons etouves)"],
        "key_point": "Verser le lait chaud sur le roux froid ou le roux chaud sur le lait froid — jamais les deux chauds en meme temps (grumeaux)"
      },
      {
        "name": "Veloute",
        "base": "Roux blanc + fond blanc (volaille, veau ou poisson)",
        "derivatives": ["Sauce Supreme (+creme, volaille)", "Sauce allemande (+jaunes d'oeufs)", "Sauce vin blanc (+vin et poisson)"],
        "key_point": "La qualite du fond definit la qualite de la sauce"
      },
      {
        "name": "Espagnole",
        "base": "Roux brun + fond brun (veau rotis)",
        "derivatives": ["Demi-glace", "Sauce bordelaise (+vin rouge, moelle)", "Sauce chasseur (+champignons, tomates)"],
        "key_point": "La plus longue a realiser — la demi-glace est une reduction intense de l'espagnole"
      },
      {
        "name": "Sauce tomate",
        "base": "Tomates + fond + aromates",
        "derivatives": ["Sauce provençale", "Sauce bolognaise", "Sauce napolitaine"],
        "key_point": "La cuisson longue et douce elimine l'acidite des tomates"
      },
      {
        "name": "Hollandaise",
        "base": "Emulsion de beurre clarifie + jaunes d'oeufs + vinaigre/citron",
        "derivatives": ["Sauce Bearnaise (+estragon, echalotes)", "Sauce Maltaise (+orange sanguine)", "Sauce mousseline (+creme montee)"],
        "key_point": "Emulsion fragile — temperature clef (60-70°C), le beurre doit etre ajoute lentement"
      }
    ],
    "modern_sauces": "Au-dela des sauces meres classiques : les jus (reduction de deglaçage), les vinaigrettes (emulsion huile/acide), les coulis (legumes ou fruits mixes et filtres), les beurres emulsionnes."
  },
  [
    {"prompt": "Comment reussir une bechamel sans grumeaux ?", "answer": "Deux methodes infaillibles : (1) Roux chaud + lait froid : faire le roux (beurre fondu + farine, remuer 1-2 min), retirer du feu. Ajouter le LAIT FROID d'un coup en fouettant energiquement. Les grumeaux se dissolvent car le roux chaud est plus fluide. Remettre sur feu, remuer jusqu'a epaississement, (2) Roux froid + lait chaud : preparer le roux et le refroidir. Verser le lait CHAUD dessus en fouettant — meme principe. L'erreur classique : lait chaud sur roux chaud — gelatinisation immediate et grumeaux garantis. Ratio basique : 20g beurre + 20g farine + 250ml lait = bechamel legere. 40g/40g/250ml = bechamel epaisse."},
    {"prompt": "Comment faire une sauce rapide avec ce que j'ai dans ma poele apres cuire de la viande ?", "answer": "Deglaçage — une des techniques les plus rentables en cuisine rapide : (1) Retirer la viande et la garder au chaud, (2) Jeter l'exces de gras si trop (garder 1-2 cuilleres), (3) Ajouter du liquide (vin, fond, eau, creme) dans la poele chaude et gratter les sucs attaches au fond — c'est l'essence du gout, (4) Reduire a feu vif jusqu'a consistance sauceuse, (5) Finir avec un peu de beurre froid hors du feu (monter au beurre) pour le brillant et la richesse. Ce principe marche avec n'importe quelle viande et n'importe quel liquide — les combinaisons sont infinies."}
  ],
  ["sauces", "bechamel", "hollandaise", "roux", "Escoffier", "cuisine classique"]
))

save("cuisine/fondamentaux/assaisonnement.json", ku(
  "assaisonnement", "cuisine", "fondamentaux",
  "Sel, poivre, acide — les trois piliers de l'assaisonnement",
  "Samy Fehout et Samin Nosrat (Salt Fat Acid Heat) ont codifie que 90% des plats ratEs souffrent d'un manque de sel, d'acide ou de gras. L'assaisonnement est la difference entre un plat correct et un plat memorable.",
  "L'assaisonnement en cuisine est l'art d'equilibrer les quatre elements fondamentaux (sel, gras, acide, chaleur selon Nosrat, ou sel, sucre, acide, umami) pour exhausser la saveur naturelle des ingredients plutot que la masquer. Un plat bien assaisonne n'a pas le gout du sel — il a le gout de lui-meme en mieux.",
  {
    "samin_nosrat_framework": {
      "source": "Samin Nosrat, Salt Fat Acid Heat (2017)",
      "salt": "Exhausse toutes les saveurs, reduit l'amertume, equilibre le sucre. Saler en plusieurs etapes (pas seulement a la fin)",
      "fat": "Vehicule les aromes liposolubles, apporte richesse et onctuosite. Huile d'olive pour le cru, beurre pour la finition, saindoux/ghee pour haute temperature",
      "acid": "Equilibre le gras, reveille les saveurs plates. Citron, vinaigre, vin, yaourt, tomate",
      "heat": "Transforme les textures et les saveurs — croustillant vs fondant, caramelisation vs bouilli"
    },
    "umami": "Cinquieme saveur — 'saveur de bouche' ou saveur de glutamate. Sources : parmesan, sauce soja, miso, tomate, champignons seches, viande maturee, anchois. Aprofond les saveurs sans les alourdir.",
    "practical_tips": [
      "Gouter tout le temps pendant la cuisson — pas seulement a la fin",
      "Le sel : saler l'eau de pates/legumes (elle doit etre 'aussi salee que la mer' selon la tradition italienne)",
      "L'acide en finition : un filet de citron sur presque n'importe quel plat chaud juste avant de servir le reveille",
      "Le sucre equilibre l'acidite et l'amertume (pas seulement dans les desserts)",
      "Rectifier l'assaisonnement a froid vs a chaud — les saveurs changent avec la temperature"
    ]
  },
  [
    {"prompt": "Mon plat est fade malgre que j'aie sale — pourquoi et comment remedier ?", "answer": "Causes courantes : (1) Pas assez de sel (la plupart des cuisiniers domicile sous-salent par peur), (2) Manque d'acide — un filet de citron ou d'un peu de vinaigre peut transformer un plat plat en quelque chose de vif, (3) Manque d'umami — une petite quantite de sauce soja, miso, parmesan ou anchois peut profondifier extraordinairement, (4) Gras insuffisant ou mauvais type. Test : ajouter du sel et gouter, puis essayer un peu de citron. Si ca reveille le plat — c'etait l'element manquant. Le gout 'neutre' d'un plat est rarement le sel seul — c'est souvent l'acidite ou l'umami qui manque."},
    {"prompt": "Comment utiliser le vinaigre et le citron en cuisine ?", "answer": "Acid brightens everything — regles d'utilisation : (1) En finition sur les plats chauds juste avant de servir — viande rotie, soupe, risotto, legumes roties. Ajouter en fin evite l'evaporation de l'acidite volatile, (2) Dans les vinaigrettes : ratio 3:1 (huile:acide) comme base, ajuster au gout, (3) Pour equilibrer une sauce trop grasse ou trop douce — quelques gouttes de citron, (4) Choisir le bon acide : citron = fraicheur vive, vinaigre balsamique = douceur et profondeur, vinaigre de cidre = note fruitee douce, vinaigre blanc = neutre. Eviter de cuisiner longtemps avec le citron (amer) — l'ajouter en finition."}
  ],
  ["sel", "acide", "umami", "assaisonnement", "Samin Nosrat", "saveur"]
))

save("cuisine/fondamentaux/equipement_base.json", ku(
  "equipement_base", "cuisine", "fondamentaux",
  "Equipement de cuisine essentiel",
  "Un equipement minimal de qualite vaut mieux qu'une multitude d'ustensiles bas de gamme. La regle : investir dans les pieces qui servent tous les jours, acheter bon une fois plutot que mauvais plusieurs fois.",
  "L'equipement de cuisine essentiel comprend les materiaux de cuisson (poeles, casseroles), les outils de preparation (couteaux, planche, mandoline) et les electromenagers structurants (four, mixeur), selectionnes selon les criteres de durabilite, d'efficacite thermique et de polyvalence.",
  {
    "priority_equipment": [
      {"item": "Poele en fonte ou en acier", "why": "Retention de chaleur superieure, surface antiadhesive naturelle si bien entretenue, va au four", "care": "Ne jamais savonner — secher et huiler. Se bonifie avec le temps"},
      {"item": "Casserole en inox a fond triple", "why": "Polyvalente, distribution de chaleur homogene, durable, compatible toutes plaques", "care": "Bicarbonate pour les traces"},
      {"item": "Couteau de chef 20cm", "why": "90% des taches de decoupe en un outil", "care": "Aiguiser regulierement, laver a la main"},
      {"item": "Planche a decouper en bois ou composite", "why": "Plus douce pour les lames que le plastique ou verre", "care": "Huile de mineral oil regulierement pour le bois"},
      {"item": "Balance de cuisine", "why": "Precision en patisserie, reproductibilite des recettes"},
      {"item": "Thermometre de cuisson", "why": "Indispensable pour les viandes, frites, caramels, temperage chocolat"}
    ],
    "optional_but_high_value": [
      "Mandoline (tranches ultra-regulieres)",
      "Robot culinaire (pesto, hummus, sauces)",
      "Mixeur plongeant (soupes veloutees, sauces directement dans la casserole)",
      "Wok en acier (cuisson vive et rapide, grands volumes)"
    ],
    "avoid": [
      "Sets de couteaux complets — la plupart des couteaux ne servent jamais",
      "Poeles antiadhesives bas de gamme — se rayent et se detériorent en mois",
      "Gadgets monofonctionnels (avocat slicer, etc.)"
    ]
  },
  [
    {"prompt": "Ma poele en teflon est rayee — est-elle dangereuse ?", "answer": "La question est debattue mais par prudence : oui, une poele en teflon fortement rayee est a remplacer. Les particules de revetement PTFE se detachent dans les aliments aux hautes temperatures — le PFAS (composes perfluores) est sous scrutin toxicologique. Alternative plus durable : poele en acier carbone (type de Buyer) ou en fonte emaillee (Le Creuset, Lodge). Ces poeles durent une vie entiere si entretenues, n'ont pas de revetement chimique et donnent une meilleure caramelisation. Investissement initial plus eleve, amortissement tres long."},
    {"prompt": "Quel est le matériau ideal pour la cuisine quotidienne — inox ou fonte ?", "answer": "Les deux ont des usages distincts : (1) Inox avec fond triple : ideal pour les sauces, deglaçages, cuissons avec liquide. Facile a nettoyer, polyvalent, repond rapidement aux changements de temperature, (2) Fonte / acier : ideal pour saisir la viande, rotir, cuire les oeufs. Retention de chaleur superieure, coloration parfaite, va au four. Mais : lourde, lente a monter en temperature, necessite entretien. Solution ideale : poele en acier pour les saisisons + casseroles en inox pour le reste. La fonte emaillee (Le Creuset) est le meilleur des deux mondes pour les plats mijotes mais a un prix eleve."}
  ],
  ["equipement", "poele", "couteau", "fonte", "inox", "cuisine"]
))

# ─── CUISINE FRANCAISE ─────────────────────────────────────────────────────────

save("cuisine/francaise/cuisine_francaise_bases.json", ku(
  "cuisine_francaise_bases", "cuisine", "francaise",
  "Cuisine française — fondements et philosophie",
  "La cuisine française est le systeme culinaire le plus codifie et le plus influent du monde occidental. Ses techniques (fonds, sauces, cuissons) ont forme la cuisine professionnelle mondiale. Sa philosophie : respecter le produit, maitriser la technique, valoriser la saisonnalite.",
  "La cuisine française est un systeme culinaire dont la codification par Escoffier (Le Guide Culinaire, 1903) a defini les standards de la cuisine professionnelle mondiale jusqu'a nos jours. Elle repose sur le respect des produits de saison, la maitrise des techniques de base (fonds, sauces, cuissons) et l'organisation en brigade de cuisine.",
  {
    "philosophy": [
      "Le produit d'abord — la technique est au service du produit, pas l'inverse",
      "La saisonnalite — chaque ingredient a une saison optimale",
      "La brigade et l'organisation — la cuisine professionnelle française a cree la structure brigade (Escoffier)",
      "La transmission — les techniques s'apprennent par compagnonnage (maitre → apprenti)"
    ],
    "plats_emblematiques": [
      {"plat": "Boeuf Bourguignon", "region": "Bourgogne", "technique": "Braise au vin rouge"},
      {"plat": "Bouillabaisse", "region": "Provence/Marseille", "technique": "Soupe de poissons avec rouille"},
      {"plat": "Cassoulet", "region": "Languedoc", "technique": "Confit de canard + haricots + charcuterie, longue cuisson"},
      {"plat": "Pot-au-Feu", "region": "National", "technique": "Bouillon de viandes et legumes — cuisson lente"},
      {"plat": "Blanquette de Veau", "region": "National", "technique": "Veau braise, sauce blanche creme"},
      {"plat": "Sole Meuniere", "region": "National (cuisine bourgeoise)", "technique": "Beurre noisette"}
    ],
    "regional_diversity": "La cuisine française n'est pas une — c'est la somme de cuisines régionales distinctes : alsacienne (choucroute, baeckeoffe), provençale (ratatouille, pissaladiere), basque (piperade, axoa), lyonnaise (quenelles, tablier de sapeur), bretonne (galettes, far)."
  },
  [
    {"prompt": "Comment realiser un boeuf bourguignon reussi ?", "answer": "Etapes cles : (1) Mariner la viande (boeuf a braiser en cubes) 12-24h dans le vin rouge avec carottes, oignons, thym, laurier, (2) Secher et saisir les morceaux en petites quantites a feu vif — la coloration est essentielle pour la saveur, (3) Faire un mirepoix avec la garniture, saupoudrer de farine (singer), mouiller avec la marinade filtree, (4) Cuisson douce 2-3h au four ou sur feu doux — le bouillon doit a peine frissonner, jamais bouillir, (5) Separement : lardons, champignons, petits oignons perles — ajouter en fin. Le secret : qualite du vin (vin qu'on boit) + longue cuisson douce + repos une nuit (encore meilleur le lendemain)."},
    {"prompt": "Quelles sont les differences entre la cuisine du Nord et celle du Sud de la France ?", "answer": "Clivage historique beurre/huile d'olive : (1) Nord et Centre : gastronomie au beurre, a la creme, aux fromages a pate molle (normandie, bourgogne). Viandes en sauce, choucroute alsacienne, carbonades flamandes pres de la Belgique, (2) Sud et Méditerranée : huile d'olive, tomates, herbes (thym, romarin, basilic), poissons, ail. Cuisine plus legere, plus coloree, plus parfumee. La ratatouille, la bouillabaisse, la soupe au pistou sont impossibles sans la luminosite du Sud. (3) Atlantique et Bretagne : produits de la mer, fruits de mer, beurre sale breton, galettes de ble noir. Ce clivage culinaire reflète la geographie, le climat et les influences culturelles de chaque region."}
  ],
  ["cuisine française", "bourguignon", "Escoffier", "brigade", "terroir"]
))

save("cuisine/francaise/patisserie_bases.json", ku(
  "patisserie_bases", "cuisine", "francaise",
  "Patisserie française — bases et logique",
  "La patisserie française est une science de la precision : les ratios sont critiques, la temperature est decisire, et la maitrise des cinq pates de base (brisee, sablee, feuilletee, chou, genoise) ouvre l'acces a la quasi-totalite du repertoire classique.",
  "La patisserie française est une discipline culinaire caracterisee par la precision des mesures, la comprehension des reactions chimiques (gluten, proteines, levures) et la maitrise de techniques comme le feuilletage, l'emulsion et le temperage. Elle se distingue de la cuisine par son aspect scientifique — les ratios ne sont pas indicatifs mais determinants.",
  {
    "five_base_doughs": [
      {"pate": "Pate brisee", "ratio": "2:1:0.5 (farine:beurre:eau environ)", "use": "Tartes salees, quiches", "key": "Sabler rapidement, ne pas trop travailler (developpe le gluten = dur)"},
      {"pate": "Pate sablee", "ratio": "Riche en beurre et sucre, peu d'eau", "use": "Tartes sucrees, sables", "key": "Plus fragile que brisee — craquante apres cuisson"},
      {"pate": "Pate feuilletee", "ratio": "Detrempe + beurre de tourage, 6 tours", "use": "Millefeuille, croissant (variante), vol-au-vent", "key": "Beurre et detrempe a la meme temperature — si trop froid ou trop mou, les couches ne se forment pas"},
      {"pate": "Pate a choux", "ratio": "Eau + beurre + farine + oeufs (dessication puis incorporation)", "use": "Eclairs, profiteroles, gougeres", "key": "Dessication correcte sur le feu avant les oeufs. Texture : ruban qui tombe de la cuillere"},
      {"pate": "Genoise / biscuit", "ratio": "Oeufs + sucre + farine, oeufs montes", "use": "Biscuit roulade, Charlotte, layer cake base", "key": "Fouetter oeufs + sucre jusqu'a ruban, incorporer la farine en soulevant pour ne pas casser la mousse"}
    ],
    "temperature_critical": [
      "Beurre a 20-25°C pour les pates sabrees/brisees — ni froid (dure) ni fondu (graisse)",
      "Chocolat tempere : montée 50°C, descente 27°C, remontee 31°C (noir) — cristallisation du beurre de cacao",
      "Creme patissiere : pasteurisee a 82-85°C (ne pas depasser — oeufs coagulent)",
      "Meringue italienne : sirop a 121°C verse sur blancs montes"
    ]
  },
  [
    {"prompt": "Pourquoi ma pate a choux ne gonfle-t-elle pas ?", "answer": "Causes courantes : (1) Dessication insuffisante — apres ajouter la farine, il faut remuer sur le feu jusqu'a ce que la pate se detache des parois et forme une boule seche. Si pas assez desseche, trop humide, ne gonfle pas bien, (2) Trop d'oeufs ou pas assez — ajouter les oeufs un a un et tester la consistance : la pate doit former un 'V' qui tombe lentement de la spatule, (3) Four pas assez chaud (minimum 190°C) ou ouvert trop tot — ne jamais ouvrir avant 25 min, (4) Depot trop plat — la pate a choux a besoin de volume avant cuisson pour avoir un espace interieur. Test : deposer une boulette dans un bol d'eau froide — elle doit flotter."},
    {"prompt": "Comment reussir une tarte au citron meringuee parfaite ?", "answer": "Trois composantes : (1) Pate sablee bien cuite 'a blanc' (fond de tarte pre-cuit avec poids) — texture croustillante qui resiste a l'humidite de la creme, (2) Creme citron (lemon curd) : zestes + jus citrons + sucre + oeufs + beurre, cuisson douce en remuant jusqu'a 82°C. Refroidir avant garnissage, (3) Meringue italienne (plus stable que francaise) : blancs montes + sirop a 121°C verse en filet. Bruler au chalumeau. La creme doit etre acidulee et pas trop sucree — l'equilibre acide/sucre est la cle gustative. Repos au frais 2h minimum avant service — la creme se tient mieux."}
  ],
  ["patisserie", "pate feuilletee", "pate a choux", "genoise", "temperature", "precision"]
))

# ─── CUISINE ASIATIQUE ────────────────────────────────────────────────────────

save("cuisine/asiatique/cuisine_japonaise.json", ku(
  "cuisine_japonaise", "cuisine", "asiatique",
  "Cuisine japonaise — umami et technique",
  "La cuisine japonaise est batie sur trois principes fondateurs : l'umami (dashi), la saisonnalite rigoureuse (shun) et la presentation (moritsuke). Elle englobe des styles aussi divers que la street food (takoyaki, ramen) et la haute cuisine omakase (kaiseki).",
  "La cuisine japonaise est un systeme culinaire qui valorise la fraicheur et la saisonnalite des produits (shun), l'expression de l'umami naturel des ingredients (via le dashi) et la beaute de la presentation comme partie integrante du repas. Classee au patrimoine immatériel de l'UNESCO en 2013 sous le nom de 'washoku'.",
  {
    "dashi": {
      "definition": "Bouillon de base japonais — la colonne vertebrale de la cuisine japonaise",
      "types": [
        {"name": "Ichiban dashi", "ingredients": "Kombu (algue sechee) + katsuobushi (bonite sechee)", "use": "Soupe miso, chawan mushi, hot pot — le plus delicat"},
        {"name": "Niban dashi", "ingredients": "Memes ingredients reinfuses", "use": "Braises, sauces — plus intense"},
        {"name": "Kombu dashi", "ingredients": "Kombu seulement (vegan)", "use": "Cuissons vegetariennes, dipping sauces"},
        {"name": "Iriko dashi", "ingredients": "Petites sardines sechees", "use": "Miso soupe rustique, ramen"}
      ]
    },
    "key_dishes": [
      {"dish": "Ramen", "description": "Soupe de nouilles avec bouillon (shio/shoyu/tonkotsu/miso) — regionalement tres varie", "complexity": "Le bouillon tonkotsu prend 12-24h"},
      {"dish": "Sushi/Sashimi", "description": "Riz vinaigre + poisson cru (nigiri, maki, temaki)", "key": "Qualite du riz aussi importante que le poisson"},
      {"dish": "Tempura", "description": "Friture legere en pate tres fine (eau glacee + farine peu travaillee)", "key": "Pate grumeleuse est voulue — ne pas trop melanger"},
      {"dish": "Okonomiyaki", "description": "Crepe/galette de chou + proteines + sauce okonomi + mayonnaise", "region": "Osaka vs Hiroshima (styles distincts)"},
      {"dish": "Yakitori", "description": "Brochettes de poulet (toutes parties) grillees au charbon binchotan, sauce tare ou sel"}
    ],
    "condiments": [
      "Shoyu (sauce soja) — base fermentee, umami profond",
      "Miso — pate de soja/riz fermentee, rouge/blanc/mixte selon region",
      "Mirin — vin de riz sucre, apporte brillant et complexite aux sauces",
      "Sake de cuisine — denature en alcool alimentaire, hydrate et attendrit",
      "Wasabi frais — racine de Wasabia japonica (rare, cher). Ce qu'on a souvent en Occident : raifort colore",
      "Ponzu — sauce soja + agrumes japonais (yuzu, sudachi)"
    ]
  },
  [
    {"prompt": "Comment faire un bon ramen chez soi sans passer 24h en cuisine ?", "answer": "Shortcut version : (1) Bouillon — faire dorer des os de porc ou de poulet au four 30 min, puis mijoter 3-4h avec ail, gingembre, shiitake seches, (2) Tare — concentrer la sauce : soja + mirin + sake + sucre, reduction. C'est la tare qui donne le 'type' de ramen (shoyu ici), (3) Nouilles ramen fraisches ou seches (rayon japonais), cuire separement, (4) Garnitures : oeuf marin (oeufs cuits 7 min, mariner 6h dans soja+mirin+eau), chashu (porc roti et braise), nori, ciboulette. La cle : separer bouillon + tare + garnitures = chacun peut personnaliser. Version 2h possible (bouillon chicken bones + cubes de fond) pour du quotidien."},
    {"prompt": "C'est quoi le dashi et est-ce que c'est difficile a faire ?", "answer": "Le dashi est le fond japonais — mais contrairement aux fonds francais (8h de cuisson), le dashi de base se fait en 20 minutes. Recette de l'ichiban dashi : (1) Kombu (algue sechee) dans eau froide, monter doucement jusqu'a frissement (pas bouillir — libere l'amarume), retirer le kombu. Temperature : 60°C max, (2) Ajouter les flocons de bonite (katsuobushi), laisser infuser 3-4 min OFF du feu, (3) Filtrer. C'est pret. Ce bouillon limpide est la base de la soupe miso, du chawan mushi, des braises japonaises. Gout d'umami pur, doux et profond. Le kombu et la bonite se trouvent en epicerie japonaise ou en ligne — commencer par les packs dashi en sachet (comme un sachet de the) si c'est la premiere fois."}
  ],
  ["cuisine japonaise", "dashi", "ramen", "sushi", "umami", "washoku"]
))

save("cuisine/asiatique/cuisine_chinoise.json", ku(
  "cuisine_chinoise", "cuisine", "asiatique",
  "Cuisine chinoise — diversite regionale et techniques wok",
  "La cuisine chinoise est l'une des plus anciennes et des plus diversifiees du monde — Cantonaise, Sichuanaise, Shanghainaise, du Shandong, Hunan et Fujian sont des systemes culinaires aussi distincts que la cuisine italienne et la cuisine espagnole. Le wok et la maitrise du 'wok hei' en sont les symboles techniques.",
  "La cuisine chinoise n'est pas une mais un ensemble de traditions culinaires regionales profondement differentes en techniques, ingredients et saveurs, unifiees par quelques techniques communes (wok, vapeur, friture, braise) et des ingredients de base partagEs (soja, gingembre, ail, vin de riz). Les Huit Grandes Traditions Culinaires (Ba Da Cai Xi) en codifient la diversite.",
  {
    "regional_styles": [
      {"region": "Canton (Guangdong)", "style": "Fraicheur, vapeur, produits de qualite mise en valeur sans masquage. Dim sum.", "dishes": ["Canard laque", "Crevettes vapeur", "Har gow", "Char siu"]},
      {"region": "Sichuan", "style": "Piment + poivre du Sichuan (effet anesthesiant) = ma-la (engourdi-pique). Audacieux, intense.", "dishes": ["Mapo tofu", "Dan Dan mian", "Kung Pao chicken", "Hot pot"]},
      {"region": "Shanghai", "style": "Sucre et sauce soja (hong shao — braise rouge). Poissons d'eau douce.", "dishes": ["Porc braise hong shao", "Xiao long bao (raviolis soupe)"]},
      {"region": "Pekin / Nord", "style": "Ble (nouilles, pains cuits a la vapeur), cuissons robustes.", "dishes": ["Peking duck", "Jiaozi (raviolis)"]},
      {"region": "Hunan", "style": "Piment frais (pas le poivre du Sichuan), aigre-piquant, umami fort.", "dishes": ["Porc Mao (dong po rou variante Hunan)"]}
    ],
    "wok_hei": {
      "definition": "Le 'souffle du wok' — saveur fumee et caramelisee que seul un wok tres chaud sur flamme vive peut creer",
      "home_challenge": "Difficile a reproduire a la maison avec les plaques standard — le gaz professionnel monte 3-5x plus chaud. Solution partielle : (1) Wok en acier bien culotte, (2) Plaque gaz la plus puissante, (3) Quantites TRES petites pour ne pas refroidir le wok"
    }
  },
  [
    {"prompt": "Comment faire un vrai riz frite chinois ?", "answer": "Quatre secrets : (1) Riz de la VEILLE, bien sec (riz chaud = vapeur qui fait coller). Riz jasmin ou long grain, (2) Wok tres chaud — fumer legerement avant d'ajouter l'huile, (3) Cuire par petites quantites — trop de riz = temperature chute = riz pate, (4) Ordre : huile chaude → aromatics (ail, gingembre, oignon) 30 secondes → proteines → pousser sur le cote → oeufs brouilles → riz — melanger → soja + sesame + ciboulette en finition. Recette de base : 200g riz cuit froid, 2 oeufs, 1 oignon vert, sauce soja, huile de sesame. 5 minutes de cuisson si tout est prepare."},
    {"prompt": "Qu'est-ce que le mapo tofu et comment le faire ?", "answer": "Mapo tofu est le plat emblematique du Sichuan : tofu soyeux dans une sauce de boeuf hache + pate de haricots fermenteE pimentee (doubanjang) + bouillon + poivre du Sichuan. L'effet 'ma-la' (engourdi-pique) est unique. Recette simple : (1) Sauter le boeuf hache avec le doubanjang (2 cuil. a soupe) dans l'huile, (2) Ajouter ail et gingembre, (3) Mouiller avec bouillon de poulet, (4) Ajouter le tofu soyeux en cubes delicatement, (5) Epaissir avec un peu de fecule, (6) Finir avec huile pimentee et poivre du Sichuan moudlu et ciboulette. Le doubanjang est l'ingredient cle — en epicerie asiatique."}
  ],
  ["cuisine chinoise", "wok", "Sichuan", "cantonais", "dim sum", "wok hei"]
))

save("cuisine/asiatique/cuisine_thaie.json", ku(
  "cuisine_thaie", "cuisine", "asiatique",
  "Cuisine thaïlandaise — equilibre des 5 saveurs",
  "La cuisine thaïlandaise est construite sur l'equilibre de cinq saveurs simultanees dans chaque plat : sucre, sale, acide, piquant et umami. Cette recherche d'equilibre dynamique la distingue de la plupart des autres cuisines asiatiques et la rend immediatement identifiable.",
  "La cuisine thaïlandaise est un systeme culinaire elabore autour de l'equilibre des cinq saveurs (sucre, sale, acide, piquant, umami) dans chaque preparation, utilisant des ingredients aromatics frais (citronnelle, galanga, feuilles de kaffir, piments frais) et des sauces fermentees (nuoc-mam thai, pate de crevettes) comme fondations de saveur.",
  {
    "flavor_balance": "La philosophie thaïe : chaque plat doit etre goute et ajuste jusqu'a ce qu'aucune saveur ne domine les autres. Le cuisinier ajoute en permanence jusqu'a l'equilibre.",
    "core_ingredients": [
      "Citronnelle (lemongrass) — aromatique frais, base des curries et des soupes",
      "Galanga (kha) — proche du gingembre mais plus floral et poivré — pas interchangeable",
      "Feuilles de Kaffir lime (bai makrut) — aromatique intense, soupes et curries",
      "Nam pla (nuoc-mam) — sauce de poisson fermentee — base salee et umami",
      "Pate de crevettes (kapi) — concentre fermente, base des pates de curry",
      "Piments (prik) — nombreuses varietes, de doux a extremement fort"
    ],
    "key_dishes": [
      {"dish": "Tom Kha Gai", "description": "Soupe de poulet au lait de coco + galanga + citronnelle + kaffir + champignons"},
      {"dish": "Pad Thai", "description": "Nouilles de riz sautees au wok, crevettes/tofu, oeufs, germes de soja, sauce tamarind + nuoc-mam + sucre"},
      {"dish": "Green Curry (Kaeng Khiao Wan)", "description": "Curry de lait de coco + pate de curry vert (piments verts + aromatics) + proteines + aubergines thaies"},
      {"dish": "Larb", "description": "Salade de viande hachee cuite + herbes fraisches + sauce + riz grille moudlu — caractere isaan du Nord-Est"},
      {"dish": "Som Tum", "description": "Salade de papaye verte au pilon — aigre/sale/piquant/sucre en meme temps"}
    ]
  },
  [
    {"prompt": "Comment faire un pad thai a la maison qui a vraiment le gout du restaurant ?", "answer": "Trois secrets : (1) La sauce pad thai : tamarind concentrate + sauce de poisson + sucre de palme (ratio 3:3:2 environ). C'est la cle — la sauce en bouteille 'pad thai' du supermarche est passable mais la maison est bien meilleure, (2) Wok tres chaud, petites quantites, (3) Ne pas trop remuer — laisser les nouilles colorer legerement avant de tout melanger. Recette : nouilles de riz plonges dans l'eau chaude 30 min (pas bouillies), puis wok chaud, huile, echalotes + crevettes, pousser sur cote, oeuf brouille, nouilles + sauce, germes de soja, ciboule. Service : cacahuetes concassees + citron vert + piment en poudre + sucre. Le citron vert presse est INDISPENSABLE a table."},
    {"prompt": "Quelle est la difference entre curry vert, rouge et jaune thai ?", "answer": "Les differences viennent principalement de la pate de curry : (1) Curry vert (kaeng khiao wan) : piments verts frais + citronelle + galanga + kaffir + coriandre. Le plus pique generalement. Lait de coco, aubergines thaies, basilic thai, (2) Curry rouge (kaeng phet) : piments rouges seches + meme aromatics. Plus chaleureux que le vert, (3) Curry jaune (kaeng kari) : influence indienne — curcuma + poudre de curry + piments moins piques. Le plus doux, le plus 'accessible'. En pratique : tous les trois sont au lait de coco, tous ont des proteines et des legumes. La difference est dans la couleur de la pate de curry — faite maison (longue) ou en bocal (pratique). Les pates en bocal de marques Mae Ploy ou Maesri sont de bonne qualite."}
  ],
  ["cuisine thaie", "curry", "pad thai", "lait de coco", "nuoc-mam", "galanga"]
))

save("cuisine/asiatique/cuisine_coreenne.json", ku(
  "cuisine_coreenne", "cuisine", "asiatique",
  "Cuisine coreenne — fermentation et banchan",
  "La cuisine coreenne est fondee sur la fermentation (kimchi, doenjang, gochujang) et le systeme des banchan — petits plats d'accompagnement partages autour du riz. Elle connait un essor international majeur, portee par la vague Hallyu (culture pop coreenne).",
  "La cuisine coreenne est un systeme culinaire centre sur le riz, les legumes fermentes (kimchi), les pates fermentees (gochujang, doenjang, ganjang) et les proteines grillees (KBBQ). Le systeme des banchan (multiples petits plats servis simultanement) reflete une philosophie du partage et de la variete.",
  {
    "fermentation_culture": {
      "kimchi": "Chou pe-tsai (ou radis, concombre) fermente avec gochujang, ail, gingembre, oignon vert. Varietes : baechu-kimchi (chou), kkakdugi (radis), oi-sobagi (concombre). Fermentation naturelle 1-5 jours a temperature ambiante, puis frigo.",
      "gochujang": "Pate de piment rouge + riz glutineux + soja — sucree, pimentee, umami. Ingredient de base des marinades, sauces et braixes.",
      "doenjang": "Pate de soja fermentee — analogue du miso japonais mais plus intense et terreux. Soupe de doenjang (doenjang jjigae) = soupe nationale"
    },
    "key_dishes": [
      {"dish": "Bibimbap", "description": "Riz + legumes varies assaisonnes + viande ou oeuf + gochujang, melanger. Souvent en bol en pierre (dolsot bibimbap) pour le riz croustillant"},
      {"dish": "KBBQ (Korean BBQ)", "description": "Viandes marinées (samgyeopsal = poitrine de porc, bulgogi = boeuf marine, galbi = cotes) grillees a table"},
      {"dish": "Tteokbokki", "description": "Gateau de riz en sauce gochujang epiceE — street food emblematique"},
      {"dish": "Japchae", "description": "Nouilles de patate douce sautees avec legumes et boeuf — plat de fete"},
      {"dish": "Sundubu jjigae", "description": "Soupe piquante au tofu soyeux, fruits de mer ou viande, oeuf cru ajouté a table"}
    ]
  },
  [
    {"prompt": "Comment faire du kimchi maison ?", "answer": "Recette de base (baechu-kimchi) : (1) Couper le chou pe-tsai en quartiers, saler generousement entre les feuilles (200g sel / 1kg chou), laisser 2h (le sel sort l'eau), rincer 3 fois, essorer, (2) Faire la pate : gochugaru (flocons de piment coreen) + ail rape + gingembre rape + nuoc-mam (ou sauce soja) + sucre + oignon vert en lamelles. Ratio approximatif : 4 cuil. gochugaru + 4 gousses ail + 1 cuil. gingembre + 2 cuil. nuoc-mam + 1 cuil. sucre pour 1kg chou, (3) Masser le chou avec la pate en portant des gants (le piment tache), (4) Mettre en bocal fermé. A temperature ambiante 1-2 jours jusqu'a deegrenouillage, puis frigo. Se conserve des mois — plus il fermente, plus il est aigre."},
    {"prompt": "Qu'est-ce que le gochujang et comment l'utiliser ?", "answer": "Le gochujang est une pate de piment coreen fermentee — une des bases de la cuisine coreenne. Gout : sucre, piquant, fermentee, umami profond. Texture : epaisse. Usages : (1) Marinade : gochujang + sauce soja + sesame + sucre + ail = marinade pour poulet, porc, boeuf (bulgogi gochujang), (2) Sauce : detendu avec vinaigre de riz + huile de sesame = sauce pour bibimbap, (3) Dans les ragoûts et jjigae pour la profondeur et la couleur, (4) Remplacant du harissa dans les recettes europeennes — moins floral mais umami en plus. Trouve en epicerie asiatique ou en ligne. Se conserve tres longtemps au frigo."}
  ],
  ["cuisine coreenne", "kimchi", "gochujang", "KBBQ", "bibimbap", "fermentation"]
))

save("cuisine/asiatique/cuisine_vietnamienne.json", ku(
  "cuisine_vietnamienne", "cuisine", "asiatique",
  "Cuisine vietnamienne — fraicheur et herbes",
  "La cuisine vietnamienne est une des plus herbacees et des plus fraisches au monde — les herbes fraiches (menthe, basilic thai, coriandre, perilla) ne sont pas des garnitures mais des ingredients a part entiere. Elle est aussi l'une des moins grasses de la cuisine asiatique.",
  "La cuisine vietnamienne est un systeme culinaire caracterise par l'utilisation abondante d'herbes fraiches, une sauce de poisson (nuoc-mam) comme base d'assaisonnement, une maitrise du bouillon long (pho) et un equilibre des saveurs entre frais, sale, acide et umami. Elle est consideree comme l'une des cuisines les plus saines au monde.",
  {
    "regional_differences": [
      {"region": "Nord (Hanoi)", "style": "Plus sobre, bouillons clairs, moins sucre, plus fermente", "dishes": ["Pho bo (vrai pho hanoi)", "Bun bo Nam Bo", "Cha ca La Vong"]},
      {"region": "Centre (Hue)", "style": "Royal, plus pique, plus complexe", "dishes": ["Bun bo Hue (soupe pimentée de boeuf)", "Banh khoai", "Mi Quang"]},
      {"region": "Sud (Ho Chi Minh)", "style": "Plus sucre, coconut, plus influence khmer", "dishes": ["Banh mi (le plus populaire ici)", "Hu tieu", "Com tam"]}
    ],
    "key_dishes": [
      {"dish": "Pho", "description": "Soupe de bouillon de boeuf (os + gingembre brule + epices) + nouilles de riz + tranches de boeuf. Bouillon se prépare 6-12h", "key": "Le bouillon est tout — epices (clou de girofle, badiane, cannelle, cardamome noire)"},
      {"dish": "Banh mi", "description": "Baguette vietnamienne (farine + riz) + garnitures : charcuterie, pate hepatique, piments, daikon + carottes marinees, concombre, coriandre", "key": "Heritage colonial francais (baguette) fusionne avec la cuisine vietnamienne"},
      {"dish": "Goi cuon (rouleaux de printemps frais)", "description": "Galette de riz humidifiee + crevettes + porc + vermicelles + laitue + herbes. Sauce cacahuetes ou nuoc cham", "key": "Pas frit — frais et sain"},
      {"dish": "Bun cha", "description": "Porc hache grille + vermicelles + herbes + bouillon dipping acide-sucre-sale"},
      {"dish": "Nuoc cham", "description": "Sauce dipping universelle : nuoc-mam + sucre + citron vert + eau + ail + piment"}
    ]
  },
  [
    {"prompt": "Comment faire un pho maison qui a le vrai gout ?", "answer": "La cle : le bouillon (pho broth). (1) Brûler l'oignon et le gingembre directement sur la flamme ou sous le grill jusqu'a noir — ca caramelise et parfume sans amertume, (2) Blanchir les os (boeuf) 5 min, jeter l'eau (elimine les impuretes), (3) Cuire les os 6-8h minimum dans l'eau froide avec gingembre/oignon brulee + sachet d'epices (badiane, clou de girofle, cannelle, cardamome noire, graines de coriandre), (4) Filtrer, saler et rectifier. Les slices de boeuf (filet ou paleron tres finement tranche) cuissent en 30 secondes dans le bouillon chaud verse dessus. Garnitures de table : pousses de soja, basilic thai, lime, piment, sauce hoisin et sriracha. Sans brûler l'oignon et le gingembre — pas le meme gout."},
    {"prompt": "Quelles herbes utiliser dans la cuisine vietnamienne et ou les trouver ?", "answer": "Les herbes essentielles vietnamiennes : (1) Basilic thai (rau que) — plus anise et moins sucre que le basilic europeen, (2) Menthe (rau hung) — plus petite feuille, plus parfumee, (3) Coriandre fraiche (rau mui) — meme plante que la coriandre europeenne, (4) Perilla / tia to — feuille verte et violette, gout entre la menthe et l'anis, unique, (5) Chrysanthemum vietnamien (rau tia to variante). Les herbes ne sont pas garnies a la fin — elles sont ajoutees en quantite sur les plats ou a table pour que chacun compose. Trouver dans les epiceries asiatiques (quartier chinois/vietnamien) — incontournables pour l'authenticite."}
  ],
  ["cuisine vietnamienne", "pho", "banh mi", "nuoc-mam", "herbes", "fraicheur"]
))

save("cuisine/asiatique/cuisine_indienne.json", ku(
  "cuisine_indienne", "cuisine", "asiatique",
  "Cuisine indienne — epices et diversite regionale",
  "La cuisine indienne est l'une des plus diverses au monde — elle varie enormement entre le Nord (creamy, riche, ghi) et le Sud (coco, tamarind, riz). Elle se caracterise par l'usage de melanges d'epices fraiches torrefies plutot que d'epices sèches en poudre.",
  "La cuisine indienne est un systeme culinaire d'une diversite interne extreme — differente au Kerala, au Punjab, au Rajasthan, au Bengal et au Tamil Nadu — caracterise par l'usage systematique d'epices (jusqu'a 25 dans un plat), des techniques de cuisson en ghee (beurre clarifie), d'un large systeme vegetarien et d'un art de la fermentation (idli, dosa).",
  {
    "regional_overview": [
      {"region": "Nord (Punjab, Mughal heritage)", "style": "Creamy, riche, ghi, tandoor, naan, fromages (paneer)", "dishes": ["Butter chicken", "Dal makhani", "Palak paneer", "Tandoori chicken"]},
      {"region": "Sud (Tamil Nadu, Kerala, Karnataka)", "style": "Riz, coco, tamarind, piments forts, vegetarien dominant", "dishes": ["Idli-sambar", "Dosa (crepe fermentee)", "Fish curry Kerala (lait de coco)", "Biryani Hyderabad"]},
      {"region": "Goa (heritage portugais)", "style": "Vindaloo (influences pork + vinaigre + piment)", "dishes": ["Vindaloo", "Fish recheado"]},
      {"region": "Gujarat/Rajasthan (vegetarien strict)", "style": "Sucre et acide en balance, pas d'ail-oignon certains secteurs", "dishes": ["Dal baati churma", "Dhokla (fermente)", "Thali guajrati"]}
    ],
    "spice_philosophy": {
      "fresh_grinding": "Les cuisiniers indiens traditionnels torrefient et broient les epices entieres au moment de la cuisson — une coriandre fraichement moulue n'a rien a voir avec la coriandre en poudre du supermarche",
      "tempering_tadka": "La technique du tadka : faire chauffer des epices entieres dans le ghee chaud (graines de moutarde, cumin, cardamome, clou de girofle) jusqu'a ce qu'elles eclatent — libere les huiles essentielles",
      "garam_masala": "Melange d'epices (non standardise — varie selon les regions et les familles) ajoute en fin de cuisson pour la chaleur aromatique"
    }
  },
  [
    {"prompt": "Comment faire un curry indien maison qui a l'air authentique ?", "answer": "Cinq etapes pour un curry de base authentique : (1) Tadka : ghee (ou huile) chaud → graines de cumin + moutarde → les laisser eclater, (2) Base aromatique : oignon jusqu'a dore profond (10-15 min, la cle de la richesse) + gingembre + ail, (3) Epices sechees : curcuma + coriandre moulee + cumin moulu + piment → cuire 1-2 min avec les aromates, (4) Tomato et proteines, cuire, (5) Finir avec garam masala + coriandre fraiche. Le secret numero 1 : les oignons. Ils doivent etre vraiment dores, pas juste translucides — ca prend 15 min et c'est la base de toute la richesse d'un curry."},
    {"prompt": "C'est quoi la difference entre un curry indien et un curry thai ?", "answer": "Differences fondamentales : (1) Base aromatique : curry indien = oignon/gingembre/ail frissonnes longuement + epices sechees. Curry thai = pate d'herbes fraiches (citronnelle, galanga, piments) qui ne cuit qu'une minute, (2) Liquide : curry indien = eau ou tomates ou creme/yaourt. Curry thai = quasi-exclusivement lait de coco, (3) Saveur : curry indien = chaud, complexe, terreux, epices longues. Curry thai = vif, frais, parfume, aromatique, (4) Piment : curry thai = piment plus directement piquant. Curry indien = chaleur distribuee par les epices melangees, (5) Herbes finales : curry thai = basilic thai, feuilles kaffir. Curry indien = coriandre fraiche, parfois fenugrec. Deux cuisines completement distinctes qui utilisent le meme mot 'curry' par commodite occidentale."}
  ],
  ["cuisine indienne", "curry", "epices", "tadka", "garam masala", "ghee"]
))

print("\n=== Domaine 'cuisine' + 'cuisine asiatique' : 12 fichiers crees ===")
