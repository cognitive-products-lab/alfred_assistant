"""
ALFRED — src/knowledge/french_stopwords.py
Mots-outils français de 4+ lettres, partagés entre knowledge_ranker.py et
taxonomy_router.py (le seul plancher appliqué aux mots de requête dans ces
deux modules est len(word) >= 4). Sans ce filtre, des mots ultra-fréquents
comme "pour" ou "faire" matchent la quasi-totalité des fiches knowledge —
observé en usage réel le 20/08/2026 : "Combien de session maximum par jour
puis-je faire pour maximiser mon apprentissage ?" chargeait des fiches
cpl/product_platform sans rapport, faisant "délirer" la réponse sur une
procédure d'installation ALFRED CPL.
"""

FRENCH_STOPWORDS = frozenset({
    "pour", "dans", "avec", "sans", "vers", "chez", "leur", "leurs",
    "votre", "vos", "notre", "nos", "cette", "quand", "comme",
    "alors", "aussi", "donc", "mais", "peut", "peux", "veux", "veut",
    "dois", "doit", "vais", "vas", "suis", "sommes", "êtes", "sont",
    "était", "étais", "avait", "avais", "avoir", "être", "cela", "ceci",
    "voici", "voila", "voilà", "bien", "très", "trop", "beaucoup",
    "jour", "jours", "fois", "chose", "choses", "rien", "quelque",
    "quelques", "puis", "puisse", "certain", "certains", "certaine",
    "certaines", "encore", "toujours", "jamais", "souvent", "parfois",
    "maintenant", "après", "avant", "pendant", "depuis", "jusqu",
    "entre", "chaque", "autre", "autres", "même", "mêmes", "ainsi",
    "cependant", "pourtant", "puisque", "lorsque", "tant", "autant",
    "fait", "faire", "faites", "font", "vous", "nous",
    "elle", "elles", "leur", "tout", "toute", "toutes", "tous",
    "sujet", "manière", "façon", "cadre", "type", "types",
})
