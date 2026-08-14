# Chantier — Articles à couleurs inline (ALFRED_WEB)

**Statut (2026-08-14) :** planifié, pas encore exécuté. Lancement prévu le 2026-08-15 à 03:00 via tâche planifiée locale.
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

*(à compléter par la session du 2026-08-15 03:00, au fur et à mesure, même format que le §7 de `vision_design_system_cpl.md`)*
