# Chantier — Articles à couleurs inline (ALFRED_WEB)

**Statut (2026-08-15) :** terminé. Voir §5 pour le journal complet (la tâche planifiée du 03:00 s'est bloquée sans rien exécuter ; le chantier a été repris et mené en direct en journée).
**Origine :** §7 de [`vision_design_system_cpl.md`](vision_design_system_cpl.md) laissait volontairement ce périmètre de côté à l'Étape 4 ("hors périmètre, sauf demande explicite dédiée"), avec ce risque noté : *« chantier qualitativement différent (refonte, pas consolidation), à haut risque de régression visuelle sur des articles déjà publiés et finis »*. Demande explicite reçue le 2026-08-14 pour lancer ce chantier séparément — la vision Étapes 0-4 reste un point d'arrêt propre et n'est pas rouverte.

---

## 1. Périmètre (audit du 2026-08-14)

Recherche `style="..."` contenant `color:#...` sur `ALFRED_WEB/templates/article_*.html`, `these_d52.html`, `knowledge_map.html`, `pentest_demo.html`.

**Gros volume (4 fichiers, ~470 occurrences) :**
| Fichier | Occurrences |
|---|---|
| `article_profil_personnalite_adaptatif.html` | 143 |
| `article_gouvernance_360_ia.html` | 124 |
| `article_evolution_interface_synchronisation_labiale.html` | 120 |
| `article_conformite_des_la_conception.html` | 83 |

**Volume modéré :**
| Fichier | Occurrences |
|---|---|
| `knowledge_map.html` | 13 |
| `these_d52.html` | 3 |

**1 occurrence isolée (à évaluer au cas par cas, peut-être laisser tel quel) :**
`article_teletravail_flexible_sante_agefiph.html`, `article_ia_accessibilite_zero_trust.html`, `article_handicap_invisible_fatigue_competences_ambitions.html`, `article_canicule_populations_vulnerables.html`, `article_blessure_laboratoire_innovation.html`

**Hors périmètre (0 occurrence) :** `article_perte_donnees.html`, `article_montee_en_competences_mastere_fede.html`, `article_formation_google_certifications_cefcys.html`, `article_carriere_grc_flexibilite_facteur_humain.html`, `article_accessibilite_fr_en_lecture_vocale.html`, `pentest_demo.html`.

## 2. Constat couleur

Échantillon sur `article_profil_personnalite_adaptatif.html` : les valeurs hex inline (`#e6edf3`, `#c9d1d9`, `#8b949e`, `#388bfd`, `#3fb950`, `#ec4899`, `#d29922`, `#8957e5`, `#f85149`, `#00a6a6`) correspondent **exactement** à la palette GitHub-dark déjà centralisée dans `static/css/dashboard-tokens.css` (Étape 2) :
```
--bg:#0d1117 --bg2:#161b22 --bg3:#1c2128 --border:#30363d
--text:#e6edf3 --text2:#8b949e --blue:#388bfd --green:#3fb950
--yellow:#d29922 --red:#f85149 --purple:#8957e5 --pink:#ec4899 --orange:#e07b39
```
Deux valeurs ne sont pas couvertes par `dashboard-tokens.css` : `#c9d1d9` (ton de texte intermédiaire, absent du fichier partagé) et `#00a6a6` (teal, **volontairement exclu** du fichier partagé depuis l'Étape 2 car sa valeur diverge selon les dashboards — même prudence à appliquer ici, ne pas supposer qu'un seul teal convient partout sans vérifier).

À reconfirmer par fichier avant de coder : cet échantillon ne couvre qu'un seul des 4 gros fichiers ; les 3 autres doivent être audités individuellement (mêmes valeurs très probables vu l'origine commune, mais à vérifier, pas à supposer).

## 3. Approche proposée

- Nouveau fichier `static/css/article-content.css` avec des classes utilitaires (`.at-text-primary`, `.at-text-secondary`, `.at-text-muted`, `.at-text-info`, `.at-text-success`, `.at-text-warn`, `.at-text-danger`, `.at-text-purple`, `.at-text-pink`, `.at-text-teal`...), valeurs alignées sur `dashboard-tokens.css` mais **fichier autonome** (les pages articles ne chargent pas `dashboard-tokens.css` aujourd'hui et n'ont pas de raison de dépendre du contexte "dashboard").
- **Un fichier à la fois**, jamais plusieurs en parallèle : ce sont des pages publiées et closes (cf. mémoire projet), le risque de régression visuelle est réel et chaque fichier doit être vérifié indépendamment avant de passer au suivant.
- Par fichier : remplacement mécanique des `style="color:#XXXXXX"` (et `background`/`border` si présents) par les classes utilitaires, avec assertion programmatique qu'aucune ligne n'est perdue/dupliquée (même méthode qu'Étape 1), puis vérification réelle : serveur Flask (`python app.py`, port 5000) + Browser pane, capture avant/après, `getComputedStyle` sur un échantillon, 0 erreur console.
- Ordre suggéré : commencer par les 2 fichiers "volume modéré" (`these_d52.html`, `knowledge_map.html`) pour valider la mécanique à faible risque, puis les 4 gros fichiers, puis statuer au cas par cas sur les 5 fichiers à 1 occurrence.
- **Un commit par fichier, jamais groupé** ; `git add` ciblé sur le(s) fichier(s) du point en cours, jamais `-A`. Test → commit → push avant de passer au fichier suivant (méthode déjà en vigueur sur ce chantier, cf. mémoire projet).
- Ne pas normaliser une couleur intentionnellement unique à un endroit précis (emphase narrative) juste parce que sa valeur hex ressemble à un token — relire le contexte, pas seulement la valeur.

## 4. Risques

- Articles déjà publiés/clos : haute exigence de fidélité visuelle, pas de « à peu près ».
- Contenu narratif où une couleur peut être un choix éditorial ponctuel plutôt qu'une répétition de palette — distinguer les deux avant de remplacer.
- Les 3 gros fichiers non encore échantillonnés peuvent révéler des valeurs hors palette GitHub-dark : dans ce cas, ne pas forcer une correspondance approximative, documenter et traiter comme un cas local (comme `--accent` sur `security_report.html` à l'Étape 4).

## 5. Journal de réalisation

**Statut (2026-08-15) : chantier terminé.** La session planifiée du 03:00 s'est bloquée dès le premier appel d'outil (probablement une invite de permission jamais validée, personne n'étant devant l'écran) — 0 travail effectué, voir la session `chantier-articles-couleurs-inline` (0 commit, 0 mise à jour de ce journal). Le chantier a été repris et exécuté en direct dans une conversation avec Céline le 15/08/2026 en journée, avec validation au fil de l'eau.

### Infrastructure (commits `784dce1`)
Ajout d'un bloc `{% block extra_css %}{% endblock %}` vide dans `base.html` (aucun effet sur les pages existantes, vérifié via l'accueil : 0 erreur console) et création de `static/css/article-content.css` avec les tokens de la palette GitHub-dark déjà utilisée en dur dans les 4 gros fichiers (mêmes valeurs que `dashboard-tokens.css`, plus `--text3:#c9d1d9`, `--teal:#00a6a6` et `--code:#79c0ff` spécifiques aux articles, absents du fichier dashboard).

### `these_d52.html` (commit `f771e1c`)
3 occurrences de `style="margin-top:0; font-size:1.05rem; color:#58a6ff;"` identiques (titres de section, répétés sur 10 sections générées par boucle) → extraites vers une classe locale `.thesis-section-title` dans le `<style>` déjà présent dans ce fichier. `#58a6ff` n'est pas dans la palette GitHub-dark partagée (déjà le cas pour `--accent` sur `security_report.html` à l'Étape 4) : gardé en valeur locale, pas de token partagé créé pour un cas isolé à ce fichier. Vérifié via serveur Flask réel : `getComputedStyle` confirme `rgb(88,166,255)` sur les 10 titres, 0 erreur console.

### `knowledge_map.html` (commit `cdd0706`)
Cas particulier découvert en cours d'audit : ce fichier a son propre `<style>` avec des tokens locaux déjà en place (`--km-purple/blue/green/gold/red`, définis mais pas tous utilisés). 4 boutons de filtre et 6 icônes de pipeline codaient encore la même palette en hex brut au lieu de `var(--km-*)`. Complété avec 2 tokens manquants (`--km-blue-light:#60a5fa`, `--km-muted:#8b949e`) pour couvrir les 2 valeurs non représentées, puis toutes les occurrences pointent vers les tokens existants. Aucun lien vers `article-content.css` ajouté ici (pas nécessaire, le fichier a déjà son propre système). Vérifié via serveur Flask réel : `getComputedStyle` sur les 4 filtres + 6 icônes confirme des valeurs identiques à l'original, 0 erreur console.

**Correctif (commit `0e66dc5`) :** la vérification finale de fin de chantier (grep sans filtre sur le mot "color") a trouvé 3 pastilles de légende (`.km-legend-dot`) oubliées lors du premier passage — leur `style="background:#hex"` ne contenait pas le mot "color", donc le filtre de recherche initial les avait manquées. Corrigées avec les mêmes tokens `--km-*`, revérifiées de la même façon (0 erreur, valeurs identiques).

### Les 4 gros fichiers (commits `ce70841`, `a6ddb79`, `271c4a2`, `1efb353`)
Traités un par un dans l'ordre : `article_conformite_des_la_conception.html` (83 occurrences), `article_evolution_interface_synchronisation_labiale.html` (120, dont 2 occurrences d'un bleu clair `#79c0ff` propre aux balises `<code>` → nouveau token `--code`), `article_gouvernance_360_ia.html` (124), `article_profil_personnalite_adaptatif.html` (143, le plus gros — inclut aussi `--red` et `--pink`, rares ailleurs). Pour chacun : ajout du `{% block extra_css %}` chargeant `article-content.css`, puis remplacement littéral de chaque `propriété:#hex` par `propriété:var(--token)` (aucune restructuration des attributs `style="..."`, seule la valeur couleur change). Audit préalable confirmant que les 4 fichiers partagent exactement la même palette (`--text/--text2/--text3/--blue/--green/--yellow/--red/--purple/--pink/--teal/--bg2/--bg3/--border`), sans surprise en dehors des cas déjà notés. Chaque fichier vérifié individuellement via serveur Flask réel avant commit : comptage des éléments migrés (90 à 152 selon le fichier), `getComputedStyle` sur un échantillon confirmant des valeurs identiques à l'original, 0 erreur console à chaque fois. Un commit par fichier, push après chaque test validé, comme prévu.

### Les 5 fichiers à 1 occurrence — couleur inline conservée (bon appel), mais correction d'une erreur d'analyse
`article_teletravail_flexible_sante_agefiph.html`, `article_ia_accessibilite_zero_trust.html`, `article_handicap_invisible_fatigue_competences_ambitions.html` (même valeur `#4ade80`), `article_canicule_populations_vulnerables.html` (`#fb923c`), `article_blessure_laboratoire_innovation.html` (`#8b5cf6`). Ce sont des badges de catégorie (`<span class="article-cat-badge" style="...">`), et leurs couleurs correspondent à la palette de `style.css` (le langage visuel du site public, `--green:#4ADE80`/`--orange:#FB923C` correspondent exactement ; le violet `#8b5cf6` est une valeur autonome). Pas la palette GitHub-dark ciblée par ce chantier — décision de ne pas toucher à la couleur inline elle-même, confirmée correcte.

**Correction (2026-08-15, plus tard le même jour) :** l'affirmation initiale « `.article-cat-badge` n'est définie dans aucun fichier CSS » était **fausse** — vérification insuffisante (seul `style.css` avait été regardé, pas le `<style>` local de chaque template). En réalité la classe avait sa propre règle CSS dupliquée (quasi à l'identique) dans **chacun** des 11 templates qui l'utilisent, exactement le même type de duplication que les dashboards à l'Étape 2 — pas une absence. Voir §"Consolidation `.article-cat-badge`" ci-dessous pour la correction.

### Consolidation `.article-cat-badge` (commit `360f9a8`)
Suite à la question de Céline sur la solidité de la protection de la palette dans la durée, ré-audit complet : les 11 templates utilisant `.article-cat-badge` (les 5 ci-dessus + `_template_article.html` le squelette de départ + 5 autres articles sans couleur dédiée) avaient chacun leur propre règle CSS locale, quasi-identique (majoritairement `background:rgba(74,144,217,.12);color:var(--blue-mid);border:1px solid rgba(74,144,217,.2)` — le bleu par défaut documenté dans le commentaire de `_template_article.html`). Regroupée en une seule règle dans `static/css/style.css`, valeur par défaut bleue (déjà utilisée par 5 des 6 fichiers sans couleur inline dédiée). Chaque fichier garde son éventuel `style="..."` inline sur le span pour sa couleur de catégorie : l'inline prévaut naturellement sur la règle partagée, donc aucun changement visuel pour ces cas. Petite normalisation assumée pour 3 fichiers qui utilisaient un padding/poids legèrement différent (`2px 10px`/600 → `.25rem .85rem`/700, la variante majoritaire). Vérifié via serveur Flask réel sur les 4 variantes de couleur (bleu, vert, orange, violet) : `getComputedStyle` confirme des valeurs identiques à l'original sur chacune, 0 erreur console.

### Vérification de la protection de la palette ailleurs sur le site (commit `b6749a8`)
Après la question « les templates sont-ils à jour pour assurer la conservation de la palette ? », audit de l'ensemble de `templates/*.html` (pas seulement le périmètre article) pour des hex de la palette GitHub-dark encore codés en dur dans des attributs `style="..."`. Trouvé et corrigé : `dashboard_security.html` (4 occurrences) et `dashboard_tests.html` (2 occurrences) — ces deux pages chargent déjà `dashboard-tokens.css` depuis l'Étape 2, donc simple remplacement par `var(--text2)`/`var(--bg2)`/`var(--border)`/`var(--bg)`, zéro nouvelle décision de token nécessaire. Vérifié via serveur Flask réel, 0 erreur console.

**Restent identifiés mais non corrigés (hors périmètre, décision explicite) :**
- `cadrage.html` (2 occurrences de `#8b949e`) : le fichier a déjà 3 valeurs de gris différentes et incohérentes entre elles (`--muted:#6B7280` utilisé 9 fois, `#8892a0` une fois, `#8b949e` deux fois) pour un usage visuellement similaire (texte de légende/métadonnée) — un vrai désordre local, mais qui dépasse le simple remplacement d'un hex dupliqué : nécessiterait de décider laquelle des 3 valeurs est la bonne référence, une décision de contenu/design que ce chantier ne tranche pas seul.
- `apprentissages.html` (1 occurrence de `#8b949e`, légende isolée) : valeur unique, faible enjeu, cohérent avec la logique déjà appliquée aux 5 fichiers à 1 occurrence du périmètre article.

### Dashboards statiques ALFRED_PC (commit local `ba0e1eeb`, non poussé)
Suite à la remarque de Céline de vérifier aussi côté `ALFRED_PC` : `ALFRED_PC/dashboard/` contient des dashboards HTML **statiques et autonomes** (servis via `python -m http.server` depuis la racine du repo, pas de Flask ici, pas de génération automatique — vérifié qu'aucun script Python ne réécrit ces fichiers avant d'y toucher), distincts des templates `ALFRED_WEB` bien qu'assez proches visuellement. Deux familles de palette y coexistent :
- **Famille GitHub-dark** (celle de ce chantier) : `dashboard_gouvernance/dashboard_gouvernance_dynamique.html`, `dashboard_quality_data/dashboard_quality_data_dynamique.html`, `dashboard_security/dashboard_security.html`, `dashboard_security/dashboard_security_dynamique.html`, `dashboard_tests/dashboard_tests.html`, `dashboard_tests/dashboard_tests_dynamique.html` — 6 fichiers, même bloc `:root` de 11 variables dupliqué à l'identique (exactement le même motif que l'Étape 2 sur `ALFRED_WEB`, jamais appliqué ici). Regroupé dans un nouveau `dashboard/dashboard-tokens.css`. `--teal` reste local (`#00a6a6` vs `#39d353`, même désaccord déjà documenté côté `ALFRED_WEB`), `--orange` reste local sur `quality_data` (`#f0883e`, valeur différente de celle d'`ALFRED_WEB`). Bonus : les 3 alias `--score-high/mid/low` de `dashboard_security.html` (valeurs identiques à `--green/--yellow/--red`) pointent maintenant vers ces variables plutôt que de dupliquer la valeur. Vérifié via serveur HTTP local réel (même méthode que `dashboard_test.py`) sur les 6 pages : `getComputedStyle` confirme des valeurs identiques à l'original, 0 erreur console.
- **Famille cyan/violet** (`--bg:#07090f`, `--acc:#00d4ff`, `--purple:#a78bfa`) : `ALFRED_DASHBOARD_DYNAMIC.html` (présent en double, à deux emplacements différents et **non identiques** — pas une simple copie), `dashboard_gouvernance/dashboard_gouvernance.html`, `dashboard_gouvernance/index.html`, `dashboard_gouvernance/norm.html` — 4-5 fichiers avec un `:root` très proche mais pas la palette ciblée par ce chantier. **Non traité** : nécessite d'abord de comprendre si certains de ces fichiers sont des versions historiques/obsolètes avant de les consolider (risque de fusionner un fichier actif avec un fichier abandonné). Signalé pour une décision explicite ultérieure, pas d'action prise.

Commit resté **local** dans `ALFRED_PC` (pas poussé), cohérent avec la divergence déjà connue sur ce dépôt — voir [[feedback_concurrent_session_data_risk]].

### Bilan
21 fichiers modifiés au total sur 2 dépôts (14 sur `ALFRED_WEB` : 2 infra + 2 petits + 4 gros + 11 consolidation badge avec chevauchement + 2 dashboards résiduels ; 7 sur `ALFRED_PC` : 1 nouveau fichier de tokens + 6 dashboards statiques), 11 commits au total (9 sur `ALFRED_WEB`, tous poussés sur `origin/main` ; 1 doc + 1 dashboards sur `ALFRED_PC`, restés locaux). Aucune régression détectée (0 erreur console sur l'ensemble des pages vérifiées, valeurs calculées identiques à l'original à chaque étape). La palette GitHub-dark est désormais protégée par des tokens partagés partout où elle est dupliquée de façon répétée et vérifiée, à l'exception de : `cadrage.html`/`apprentissages.html` sur `ALFRED_WEB` (désordre local pré-existant / cas isolé, signalés) et la famille cyan/violet sur `ALFRED_PC` (signalée, décision à prendre). Chantier clos.
