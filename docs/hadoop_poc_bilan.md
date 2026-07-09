# PROJECT : ALFRED
# BLOCK   : B29 — Démonstrateur Big Data Hadoop (PoC ciblé)
# FILE    : docs/hadoop_poc_bilan.md
# ROLE    : Bilan et regard critique du PoC Hadoop
# CREATED : 2026-07-09
# UPDATED : 2026-07-09
# STATUS  : VALIDATED — job MapReduce exécuté avec succès sur cluster réel le 09/07/2026

# PoC Hadoop — Bilan et regard critique

## Contexte

Demande du référent (thèse D52) : intégrer, dans la mesure du possible, un
démonstrateur Big Data (Hadoop) pour analyser des logs d'usage anonymisés,
dans le cadre de la préparation au déploiement public d'ALFRED. Positionné
dès le cadrage (08/07/2026) comme **PoC ciblé**, pas une infrastructure de
production — avec obligation de porter un regard critique honnête sur sa
pertinence réelle à l'échelle du projet (volet RSE/sobriété numérique
obligatoire de la thèse).

## Ce qui a été construit

1. **Anonymisation avant tout chargement** (`scripts/anonymize_logs_for_hadoop.py`)
   — champ par champ, à partir des vrais logs de sécurité ALFRED_PC
   (`logs/security/api_access.jsonl`, `audit_trail.jsonl`, `soc_alerts.jsonl`) :
   timestamp tronqué au jour, identifiants directs/quasi-directs supprimés
   (`api_key_hash`, `user_id`, `device_id`, `request_id`), texte libre
   supprimé (`message`). Bug réel trouvé et corrigé pendant l'implémentation :
   collision entre le champ de provenance ajouté et un champ `source`
   déjà présent dans les données brutes de `soc_alerts.jsonl`.

2. **Job MapReduce classique** (`hadoop_poc/mapper.py` + `hadoop_poc/reducer.py`,
   pattern word-count) — comptage d'événements par jour/catégorie
   (endpoint+résultat pour les accès API, action+décision pour l'audit,
   niveau pour les alertes SOC). **Logique validée en local avant toute
   infrastructure** (`cat *.jsonl | mapper.py | sort | reducer.py`),
   résultats vérifiés à la main.

3. **Cluster Hadoop pseudo-distribué** (`docker-compose.hadoop.yml`,
   `hadoop.env`) — 5 conteneurs (namenode, datanode, resourcemanager,
   nodemanager, historyserver), basé sur le référentiel communautaire
   `big-data-europe/docker-hadoop`, RAM/vCPU réduits par rapport aux
   valeurs par défaut du tutoriel (4 Go/2 vCPU vs 16 Go/8 vCPU — remonté
   de 2 à 4 Go après un deadlock de ressources, cf. incidents ci-dessous)
   — isolé du reste du projet (aucun `docker-compose.yml` de production
   n'existe côté ALFRED_PC).

## Volumétrie réelle traitée

| Source | Lignes | Taille |
|---|---:|---:|
| `api_access.jsonl` | 290 | 44 Ko |
| `audit_trail.jsonl` | 1 | 4 Ko |
| `soc_alerts.jsonl` | 1 108 | 252 Ko |
| **Total** | **1 399** | **~300 Ko** |

## Résultat de l'exécution

Job Hadoop Streaming exécuté avec succès le 09/07/2026 sur le cluster réel
(`scripts/run_hadoop_poc.py`) : chargement HDFS des 3 fichiers anonymisés,
job MapReduce (`mapper.py`/`reducer.py`) sur `/poc/input` → `/poc/output`,
rapatriement dans `data/hadoop_poc/output/result.tsv`.

```
$ hdfs dfs -ls /poc/output
Found 2 items
-rw-r--r--   3 root supergroup          0 2026-07-09 19:17 /poc/output/_SUCCESS
-rw-r--r--   3 root supergroup       1967 2026-07-09 19:17 /poc/output/part-00000
```

49 clés agrégées en sortie. Extrait (triées par volume décroissant) :

```
soc_alerts|2026-06-02|CRITICAL          281
soc_alerts|2026-06-01|CRITICAL          199
soc_alerts|2026-06-10|CRITICAL          114
soc_alerts|2026-05-31|CRITICAL           87
api_access|2026-06-02|/api/chat|ALLOW    44
api_access|2026-06-02|/api/admin|FORBIDDEN 44
api_access|2026-06-01|/api/chat|ALLOW    24
api_access|2026-06-01|/api/admin|FORBIDDEN 24
```

Résultat **identique** à la simulation locale préalable
(`cat *.jsonl | mapper.py | sort | reducer.py`, sans aucune infrastructure)
— validation croisée que le job distribué produit le même résultat que le
calcul local, sur ce volume.

### Deux incidents réels rencontrés et corrigés (transparence méthodologique)

1. **Deadlock de ressources YARN** — premier essai à 2048 Mo de RAM pour le
   nodemanager (réduction volontaire vs 16 Go par défaut du référentiel) :
   l'ApplicationMaster à lui seul a consommé toute la capacité du nœud
   (`Allocated Resources : <memory:2048, vCores:1>` sur une capacité
   configurée de `2048`), laissant 0 Mo pour les tâches map/reduce — le job
   est resté bloqué à `map 0% reduce 0%` pendant 15 minutes avant d'être
   tué manuellement. Corrigé en remontant à 4096 Mo (cf. `hadoop.env`).
   **Ce blocage est en soi une donnée du bilan critique** : même à
   l'échelle PoC, le dimensionnement de ressources Hadoop/YARN n'est pas
   trivial et peut échouer silencieusement (pas d'erreur explicite, juste
   un job qui ne progresse jamais).

2. **Python absent de l'image Hadoop** — `bde2020/hadoop-nodemanager`
   (Debian 9 "stretch", EOL) ne fournit pas Python. Installé manuellement
   (`apt-get install python3`, avec redirection des dépôts vers
   `archive.debian.org` car les miroirs stretch officiels sont hors ligne)
   → Python 3.5.3, qui ne supporte ni les f-strings ni
   `from __future__ import annotations` (PEP 563, 3.7+). `mapper.py` et
   `reducer.py` réécrits en syntaxe compatible 3.5 (`.format()`).
   **Illustre concrètement la dette technique/fragilité d'un empilement
   Hadoop générique** : image communautaire non maintenue, écart de version
   Python qui aurait pu passer inaperçu sans exécution réelle du job.

## Regard critique (sobriété numérique)

Hadoop (HDFS + YARN) est conçu pour distribuer le traitement de volumes de
données de plusieurs **gigaoctets à téraoctets** sur un cluster de
plusieurs machines. Le volume réel disponible dans ALFRED aujourd'hui
(~300 Ko, 1 399 lignes, un seul utilisateur) tient intégralement en
mémoire dans un script Python de dix lignes, ou dans une seule requête
SQL sur une table PostgreSQL avec `GROUP BY`.

Concrètement, pour obtenir le même résultat que ce PoC (comptage
d'événements par jour/catégorie), l'alternative de production réaliste
est :
```sql
SELECT log_type, date, category, COUNT(*)
FROM logs
GROUP BY log_type, date, category;
```
— exécutable en quelques millisecondes sur PostgreSQL (déjà en place pour
les comptes utilisateurs, Bloc 21.23) ou via `pandas`/`DuckDB` en local,
sans provisionner cinq conteneurs, sans cluster à maintenir, sans la
complexité opérationnelle (formatage HDFS, réplication, gestion YARN) que
requiert Hadoop même en mode pseudo-distribué single-node.

**Conclusion assumée pour la thèse** : la compétence Big Data/distribué
est démontrée par ce PoC isolé, documenté et **exécuté avec succès sur un
cluster réel** (cf. section précédente), mais la décision de production
responsable pour ALFRED à son échelle actuelle est de **ne pas** déployer
Hadoop — un choix cohérent avec le principe local-first et le volet RSE
(sobriété numérique) du projet. Les deux incidents rencontrés en cours de
route (deadlock de ressources, dépendance Python absente d'une image
communautaire non maintenue) ne sont pas des détails d'implémentation
anecdotiques : ils illustrent concrètement le coût opérationnel réel d'un
empilement Hadoop, même réduit à l'essentiel, pour un volume qui aurait
pu être traité en une requête SQL. Réévaluer uniquement si le volume de
logs change d'ordre de grandeur (multi-utilisateurs à grande échelle,
télémétrie produit à volume réel).

## Points de vigilance RGPD

- Anonymisation/agrégation faite **avant** tout chargement HDFS, jamais de
  log brut chargé dans le cluster.
- PoC jamais connecté à un pipeline de production ni à un flux de données
  en direct — exécution manuelle, ponctuelle, sur un export anonymisé.
- Durée de rétention TTL du PoC : sans objet (pas de rétention — les
  conteneurs et données HDFS sont détruits après le PoC, `docker compose
  down -v`).
- Ce traitement (même en PoC) est à documenter dans l'AIPD T001
  (backlog, non commencée) au même titre que les autres traitements de
  données liés au déploiement public.
