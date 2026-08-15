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

### Les 5 fichiers à 1 occurrence — laissés tels quels, avec justification
`article_teletravail_flexible_sante_agefiph.html`, `article_ia_accessibilite_zero_trust.html`, `article_handicap_invisible_fatigue_competences_ambitions.html` (même valeur `#4ade80`), `article_canicule_populations_vulnerables.html` (`#fb923c`), `article_blessure_laboratoire_innovation.html` (`#8b5cf6`). Investigation : ce sont des badges de catégorie (`<span class="article-cat-badge" style="...">`), et leurs couleurs correspondent à la palette de `style.css` (le langage visuel du site public, `--green:#4ADE80`/`--orange:#FB923C` correspondent exactement ; le violet `#8b5cf6` est une valeur autonome, sans équivalent dans `style.css` ni dans la palette GitHub-dark). Pas la palette ciblée par ce chantier. Découverte supplémentaire : `.article-cat-badge` n'est définie dans **aucun** fichier CSS du dépôt — sur les 11 templates qui utilisent cette classe, 6 n'ont aucun style inline du tout (badge sans couleur/apparence). Corriger ces 5 fichiers proprement impliquerait de créer la classe de base manquante et de statuer sur les 6 autres templates : un chantier de complétude de fonctionnalité différent, pas une suppression de duplication. Décision : hors périmètre, même logique que `style.css`/`cadrage.html` à l'Étape 4.

### Bilan
9 fichiers modifiés (2 infra + 2 petits + 4 gros + 0 sur les 5 "1 occurrence", volontairement laissés tels quels), 7 commits, tous poussés sur `origin/main` d'`ALFRED_WEB`. Aucune régression détectée (0 erreur console sur l'ensemble des pages vérifiées, valeurs calculées identiques à l'original à chaque étape). Chantier clos.
