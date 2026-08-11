# Vision — Design System CSS Cognitive Products Lab (adapté)

**Statut (2026-08-11) :** Étapes 0 à 3 **réalisées et vérifiées**. Étape 4 **partiellement traitée par choix** : 3 templates consolidés en toute confiance ; le reste du périmètre initial (style.css, cadrage.html, setup_bureau.html, dashboard_data.html, ~15 pages d'articles) **volontairement laissé tel quel**, avec justification — voir §7.
**Origine :** deux documents de travail déposés sur le Bureau (« framework CSS complet.docx » et « Design System CSS Officiel.docx »), servant de source d'inspiration mais **non repris tels quels** — ils décrivent un système bien plus large que ce dont les 4 produits ont réellement besoin aujourd'hui.

---

## 1. Constat de l'existant (audit du 11/08/2026)

| Repo | CSS externe | CSS inline (`<style>`) | Tokens (`:root`) | Thème sombre/clair | Notes |
|---|---|---|---|---|---|
| **ALFRED_WEB** | 1 fichier — `static/css/style.css` (2 784 lignes) | 39 templates, ~5 224 lignes | **≥ 6 jeux différents et incompatibles** (`--bg-main`/`--bg`/`--hw-bg`/`--qd-bg`...) | absent | site public + dashboards |
| **ALFRED_PC** | 0 fichier `.css` | 1 fichier — `interface/desktop_ui/index.html` (662 lignes de `<style>`) | **Le plus abouti** : échelle d'espacement `--sp-1`→`--sp-8`, easing nommé, accessibilité (`.hc`, `.dyslexia-font`, `.reduced-motion`) | ✅ complet (`data-theme`, `prefers-color-scheme`) | avatar/visèmes stylés ici |
| **ALFRED_CPL** | 0 fichier `.css` | 1 fichier démo, ~40 lignes | 1 jeu, quasi identique à celui des dashboards ALFRED_WEB (copié-collé) | absent | juste une démo |
| **ARTHUR** | — | — | — | — | dossier vide, pas encore de repo |

**Total : ~8 700 lignes de CSS, 1 seul fichier externe, 17+ blocs `:root` qui ne se parlent pas entre eux.** Aucun framework (Bootstrap/Tailwind) nulle part. Aucun mécanisme de partage entre les 4 repos — chacun est un dépôt git séparé.

Le point le plus mûr existant est `ALFRED_PC/interface/desktop_ui/index.html` : c'est lui qui a le vrai système de thème, l'accessibilité, l'échelle d'espacement. C'est la meilleure base de départ, pas les deux docs.

---

## 2. Ce que je retiens des deux documents, et ce que j'écarte

### À garder (bonnes idées, peu coûteuses)
- **La hiérarchie de tokens en 3 niveaux** (doc « Officiel » §03.6) : fondamentaux → sémantiques → composants. C'est ce qui manque le plus aujourd'hui (ALFRED_WEB confond les deux premiers niveaux en permanence).
- **Une couleur d'identité par produit** (`--product-alfred`, `--product-cpl`, `--product-arthur` + accent) : utile pour distinguer visuellement les 3 produits sans dupliquer toute la palette.
- **Convention de nommage `--catégorie-élément-variante`** (`--text-primary`, `--bg-page`, `--radius-large`) : plus lisible que l'existant (`--bg`, `--bg2`, `--bg3`, `--acc`...) qui oblige à deviner ce que chaque variable désigne.
- **Une seule source de vérité par famille de tokens**, avec interdiction de coder une couleur/un espacement en dur ailleurs.

### À écarter ou reporter (sur-ingénierie par rapport au besoin réel)
- L'arborescence complète proposée dépasse **90 fichiers CSS** (kanban, split-view, print/invoice/certificate/labels, workspace, documentation, presentation, kiosk, glass/oled/sepia...). Aucun de ces besoins n'existe dans le code actuel — c'est de la conception pour des cas hypothétiques.
- Le doc « framework CSS complet » n'est lui-même qu'à moitié écrit (s'arrête à `components/select.css`, aucun composant `alfred/` n'est rédigé) : ce n'est pas un livrable prêt à copier, plutôt un brouillon d'inspiration.
- `--font-ui: "OpenDyslexic","Montserrat",sans-serif` en police par défaut : OpenDyslexic doit rester une **option d'accessibilité activable**, pas la police par défaut de tout le monde (ALFRED_PC le fait déjà bien avec sa classe `.dyslexia-font`).
- Aucun des deux repos n'a de bundler (pas de Sass/PostCSS, pas de webpack/vite) : tout doit rester du CSS pur, chargeable directement via `<link>`, sans étape de build.

---

## 3. Architecture V1 proposée (réaliste, pas la version des 90 fichiers)

### Emplacement du code source
`D:\PROJET_ALFRED\SHARED_RESOURCES\design-system\` — dossier déjà présent mais vide, visiblement prévu pour ça. Il **n'est pas un dépôt git** (le dossier racine `PROJET_ALFRED` ne l'est pas), donc il ne peut pas être partagé par sous-module. Chaque produit garde une **copie vendorée** du CSS partagé dans son propre repo, synchronisée par un petit script (même logique que `sync_dashboards.py`, cf. mémoire projet — script séparé, jamais lancé automatiquement, toujours avec confirmation avant push).

```
SHARED_RESOURCES/design-system/
├── core/
│   ├── tokens.css        ← source unique des design tokens (fusion des 17 :root existants)
│   ├── reset.css
│   └── accessibility.css ← .hc / .dyslexia-font / .reduced-motion (repris tel quel de ALFRED_PC)
├── themes/
│   ├── dark.css
│   ├── light.css
│   └── high-contrast.css
└── components/            ← vide au départ, rempli seulement quand un composant existe ≥2 fois à l'identique
```

Pas de `layout/`, pas de `print/`, pas de `alfred/` complet en V1 — ces dossiers n'apparaissent que si un vrai besoin se présente (kanban, impression PDF...).

### Convention de nommage retenue
On adopte la convention `--catégorie-élément-variante` du doc « Officiel » **pour les nouveaux tokens**, mais on ne renomme pas en masse l'existant (`index.html` fait 2 900 lignes, un rename global casserait tout sans bénéfice immédiat). À la place, les anciens noms deviennent des alias :

```css
:root{
  /* --- niveau 1 : fondamentaux --- */
  --cpl-blue:#1F8FE5; --cpl-violet:#6E3FEA; --cpl-dark-blue:#16254C;

  /* --- identité produit --- */
  --product-alfred:#1F8FE5;       --product-alfred-accent:#6E3FEA;
  --product-cpl:#16254C;          --product-cpl-accent:#1F8FE5;
  --product-arthur:#6E3FEA;       --product-arthur-accent:#8A63F6;

  /* --- niveau 2 : sémantique (fusion des 6 jeux dashboard ALFRED_WEB) --- */
  --bg-page:#0d1117; --bg-surface:#161b22; --bg-surface-2:#1c2128;
  --text-primary:#e6edf3; --text-secondary:#8b949e;
  --color-success:#3fb950; --color-warning:#d29922; --color-error:#f85149; --color-info:#388bfd;

  /* --- espacement, repris tel quel de ALFRED_PC (le seul qui en a un) --- */
  --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px; --space-5:24px; --space-6:32px; --space-7:40px;

  /* --- alias de compatibilité, le temps de la migration --- */
  --bg: var(--bg-page); --surface-1: var(--bg-surface); --surface-2: var(--bg-surface-2);
  --sp-1: var(--space-1); --sp-2: var(--space-2); /* etc. */
}
```

Ceci n'est qu'une **esquisse d'orientation**, pas le fichier final — les vraies valeurs devront être vérifiées une par une contre les 17 jeux existants pour ne rien casser visuellement.

---

## 4. Plan de migration incrémental (rien de big-bang)

1. **Étape 0 — zéro risque.** Créer `SHARED_RESOURCES/design-system/core/tokens.css` en fusionnant les tokens réellement utilisés (pas les 90 imaginés). Ne touche à aucun fichier produit.
2. **Étape 1 — ALFRED_PC.** Extraire le `<style>` de `desktop_ui/index.html` vers un fichier CSS chargé en `<link>`, sans changer une seule valeur au départ. C'est le repo le plus mûr, donc le moins risqué pour valider la mécanique.
3. **Étape 2 — ALFRED_WEB, dashboards.** Les 6 templates `dashboard_conformite/gouvernance/risk_impact/vulnerabilites/security/tests` ont quasiment le même `:root` copié-collé : on les fait pointer vers un seul `static/css/dashboard-tokens.css`. Gain immédiat, risque faible (un seul template testé d'abord, comparaison visuelle avant/après, puis propagation).
4. **Étape 3 — ALFRED_CPL.** Aligner `demo/alfred_cpl_demo_screen.html` sur les mêmes tokens (déjà proches).
5. **Étape 4 — composants partagés, au cas par cas.** On n'extrait un composant (`button.css`, `card.css`...) que quand il existe réellement en double à l'identique dans au moins 2 produits — pas avant.

Chaque étape est vérifiable visuellement (capture d'écran avant/après) avant de passer à la suivante.

---

## 5. Points d'attention

- **Repos publics vs privés** (cf. mémoire projet) : le CSS n'est pas un secret, la copie vendorée dans chaque repo ne pose pas de problème de fuite.
- **Pas de bundler nulle part** : rester en CSS pur, plusieurs `<link rel="stylesheet">` plutôt que des chaînes `@import` (qui bloquent le rendu en cascade).
- **`ARTHUR` n'a pas encore de code** : le design system V1 se construit sans lui ; ses tokens produit (`--product-arthur`) sont déjà prévus pour quand il démarrera.
- Le fichier `interface/desktop_ui/index.html` fait 2 900 lignes et gère aussi l'avatar/visèmes — toute extraction doit être testée dans le Browser pane avant validation, pas seulement relue.

---

## 6. Prochaine étape si validé

Commencer par l'**Étape 0 + Étape 1** (fondation + ALFRED_PC), qui ne touchent qu'un seul repo et sont facilement vérifiables visuellement, avant de propager à ALFRED_WEB et ALFRED_CPL.

## 7. Journal de réalisation

### Étape 0 — fondation (`SHARED_RESOURCES/design-system/`)
`core/tokens.css` et `core/accessibility.css` créés à partir des tokens réels d'`ALFRED_PC/interface/desktop_ui/index.html` (le système le plus abouti, cf. §1) — pas des valeurs inventées dans les deux docx. Ajout, en pur alias, d'une couche « identité produit » (`--product-alfred`, `--product-cpl`, `--product-arthur` + accents) qui n'existait nulle part avant, prête pour quand ALFRED CPL / ARTHUR auront une vraie interface à themer.

### Étape 1 — ALFRED_PC (`interface/desktop_ui/`)
Extraction mécanique (script Python jetable, supprimé après usage) du `<style>` inline de `index.html` (676 lignes, dont 5 lignes de polices encodées en base64 impossibles à relire à la main) vers `css/fonts.css`, `css/tokens.css`, `css/accessibility.css`, `css/base.css`, `css/app.css`, chargés via `<link>`. Une assertion programmatique garantit qu'aucune ligne n'a été perdue ni dupliquée dans le découpage. Vérifié dans le Browser pane (`file://.../index.html`) : rendu identique, 0 erreur console, les 5 fichiers CSS chargés. `git diff --stat` : 676 lignes supprimées / 5 insérées dans `index.html`, comme attendu.

### Étape 2 — ALFRED_WEB (dashboards dupliqués)
7 templates (`dashboard_conformite/gouvernance/risk_impact/vulnerabilites/security/tests`, `smsi_dashboard`) partageaient un `:root` GitHub-dark quasi identique. Créé `static/css/dashboard-tokens.css` avec les 13 variables **réellement** identiques partout. Point important : `--teal` a **deux valeurs différentes et incompatibles** selon les dashboards (`#00a6a6` sur 4 d'entre eux, `#39d353` sur 2 autres, absente sur `smsi_dashboard`) — ce n'était pas une duplication mais un vrai désaccord de palette, donc `--teal` a été volontairement laissé **hors** du fichier partagé ; chaque template garde un `:root` local d'une seule ligne pour cette variable. Les 7 pages ont été vérifiées une par une via le serveur Flask réel (`python app.py`, port 5000) : `getComputedStyle` confirmant chaque token résolu (dont `--teal`), 0 erreur console sur les 7. `git diff --stat` : 13 insertions / 42 suppressions sur 7 fichiers.

### Étape 3 — ALFRED_CPL (démo)
`demo/alfred_cpl_demo_screen.html` est **généré** par `demo/generate_demo_screen.py` (pipeline réel) — donc édité côté générateur (source de vérité), pas seulement côté fichier généré, pour ne pas perdre la modification à la prochaine régénération. Ses valeurs (`--bg/--bg2/--bg3/--border/--text/--text2/--blue/--green/--yellow/--red`) étaient déjà strictement identiques à `dashboard-tokens.css` : rien à corriger, juste un commentaire ajouté expliquant l'alignement voulu. **Pas de `<link>` externe ajouté** : ce fichier doit rester autonome et fonctionner hors ligne pour la démo/forum du 14/10/2026 (cf. mémoire projet) — un lien vers un CSS d'un autre repo casserait cette portabilité. Vérifié en ouvrant le fichier directement dans le Browser pane : rendu et contenu intacts, 0 erreur console.

### Étape 4 — traitée en partie, avec un périmètre volontairement réduit

**Audit.** Un sondage des couleurs hex sur tout `templates/*.html` + `style.css` a montré que la palette GitHub-dark (`#0d1117`/`#161b22`/`#e6edf3`/`#8b949e`/`#388bfd`/`#3fb950`/`#d29922`/`#f85149`/`#8957e5`) revient des dizaines de fois (jusqu'à 140 occurrences pour une seule couleur) dans bien plus de fichiers que les 7 dashboards de l'Étape 2. Deux familles très différentes s'y cachaient :

1. **6 templates avec leur propre `:root`** (`doc_qualite_data.html`, `hardware.html`, `setup_bureau.html`, `security_report.html`, `dashboard_data.html`, `cadrage.html`) — mécanique, comparable à l'Étape 2.
2. **~15 pages d'articles** (`article_conformite_des_la_conception.html`, `article_gouvernance_360_ia.html`, `these_d52.html`, `pentest_demo.html`, `knowledge_map.html`...) où les mêmes couleurs sont codées en dur dans des **attributs `style="..."` inline**, dispersés dans le contenu (pas de `:root`, pas de bloc `<style>` à factoriser) — ex. `templates/article_conformite_des_la_conception.html:20` : `<nav style="font-size:12px;color:#8b949e;...">`.

**Fait traité (3 templates, faible risque, forte confiance) :**
- `security_report.html` : `--bg`/`--border`/`--text` étaient déjà identiques nom-pour-nom à `dashboard-tokens.css` → supprimés (viennent maintenant du fichier partagé) ; `--card`/`--muted` deviennent des alias (`var(--bg2)`, `var(--text2)`) ; `--accent:#58a6ff` reste local (valeur réellement différente de `--blue`, propre à cette page).
- `doc_qualite_data.html` et `hardware.html` : `--qd-surf/--qd-surf2/--qd-txt/--qd-dim` et `--hw-*` équivalents deviennent des alias vers `dashboard-tokens.css`. `--qd-bg/--hw-bg` (`#07090f`) et `--qd-bdr/--hw-bdr` (`#21262d`) restent en dur : valeur **réellement différente** de `--bg`/`--border` du fichier partagé (chrome de page plus sombre que les cartes dashboard — les deux fichiers partagent d'ailleurs cette même variante entre eux, cohérent). `--qd-teal` reste en dur (le fichier partagé n'a volontairement pas de `--teal`, cf. Étape 2). `--hw-done`/`--hw-accent` restent locaux (aucune correspondance ailleurs). Les 3 pages vérifiées via le serveur Flask réel (`getComputedStyle` + 0 erreur console).

**Volontairement laissé tel quel, avec justification :**
- **`style.css`** : a sa propre palette cohérente (`--blue:#4A90D9`, `--green:#4ADE80`, `--purple:#A78BFA`, `--teal:#2DD4BF`...), **différente et coexistante** avec la palette GitHub-dark des dashboards — ce n'est pas un oubli, ce sont deux langages visuels distincts (site public/marketing vs contenu technique). Rien à corriger.
- **`cadrage.html`, `setup_bureau.html`, `dashboard_data.html`** : palettes propres (violet/fuchsia pour cadrage ; cyan `#00d4ff`/orange pour les deux autres), avec des recoupements partiels mais pas de correspondance exacte et systématique qui justifierait une consolidation forcée (ex. `setup_bureau.html` et `dashboard_data.html` partagent `--acc:#00d4ff` et 2 autres couleurs, mais leurs `--bg`/`--surf`/`--border` diffèrent réellement). Forcer une fusion ici reviendrait à deviner l'intention du design plutôt qu'à corriger une duplication avérée.
- **Les ~15 pages d'articles à couleurs inline** : la duplication de *valeur* est réelle et massive, mais ce n'est pas une duplication de *structure* — il n'y a aucun bloc à pointer vers un fichier partagé, il faudrait remplacer individuellement des dizaines d'attributs `style="color:#8b949e"` par des classes CSS dans chaque fichier. Chantier qualitativement différent (refonte, pas consolidation), à haut risque de régression visuelle sur des articles déjà publiés et finis (cf. mémoire projet : plusieurs articles marqués comme publiés/clos), pour un bénéfice de maintenance faible (ce ne sont pas des pages activement dupliquées pour en créer de nouvelles). Décision : hors périmètre, sauf demande explicite dédiée.
