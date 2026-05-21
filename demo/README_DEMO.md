# ALFRED — Kit de Démonstration Cybersécurité
## Bloc 20 · Security by Design · Zero Trust · Local-First

---

## Démarrage rapide

### Windows — Démonstration complète (recommandé)
```powershell
# Clic droit → Exécuter avec PowerShell
.\demo\demo_cybersecurity.ps1
```

### Windows — Dashboard seul (double-clic)
```
demo\dashboard_security.bat
```

### Multiplateforme — Attaques en direct
```bash
python demo/demo_attack.py
```

### Rapport HTML seul
```bash
python src/security/html_report.py
# Ouvre ensuite : demo/alfred_security_report.html
```

---

## Ce que montre chaque script

### `demo_cybersecurity.ps1` — Démonstration complète en 4 étapes

| Étape | Module | Ce qui se passe |
|-------|--------|----------------|
| 1 | `security_dashboard.py` | Rapport texte : score 100/100, métriques audit, menaces, appareils |
| 2 | `html_report.py` | Génération rapport HTML + ouverture automatique navigateur |
| 3 | `security_governance.py` | 13 contrôles durcissement CRITICAL→LOW, matrice de risques |
| 4 | `pytest tests/security/` | 136 tests d'intrusion en direct (SQL/XSS/prompt/ZT...) |
| Bonus | `demo_attack.py` | Simulation d'attaques réelles bloquées en temps réel |

---

### `demo_attack.py` — 4 blocs de démonstration live

#### Bloc 1 — Validation des entrées
Simule les vecteurs d'attaque les plus courants, montre le blocage en temps réel :

| Catégorie | Exemples de payloads |
|-----------|---------------------|
| SQL Injection | `'; DROP TABLE users; --` · `1' OR '1'='1` · `UNION SELECT *` |
| XSS | `<script>alert(1)</script>` · `onerror=alert(1)` · `javascript:` |
| Path Traversal | `../../etc/passwd` · `..\windows\system32` |
| Command Injection | `; rm -rf /` · `$(whoami)` · `powershell -enc ...` |
| Prompt Injection | `Ignore previous instructions` · `DAN mode` · `Bypass safety` |
| SSRF / LDAP | `ldap://internal` · `http://127.0.0.1:8080` · `gopher://` |

#### Bloc 2 — Score de menace
Affiche le score calculé par `threat_detector.py` sur chaque type d'input — légitime vs malveillant.

#### Bloc 3 — Filtre de sortie
Montre le masquage automatique de clés API, JWT, tokens GitHub et mots de passe dans les réponses.

#### Bloc 4 — Pipeline Zero Trust complet
Simule 5 scénarios de contrôle d'accès de bout en bout :

| Scénario | Résultat attendu |
|----------|----------------|
| Input SQL injection | REFUSÉ — étape 1 (input_validator) |
| Appareil inconnu | REFUSÉ — étape 3 (device_registry) |
| GUEST tente DELETE_DATA | REFUSÉ — étape 4 (access_control) |
| USER accède ressource CRITICAL | REFUSÉ — étape 5 (policy_engine) |
| OWNER requête normale | AUTORISÉ — pipeline complet validé |

---

### `dashboard_security.bat` — Dashboard instantané

Double-clic depuis l'explorateur Windows :
1. Affiche le rapport texte dans le terminal
2. Génère `demo/alfred_security_report.html`
3. Ouvre automatiquement dans le navigateur par défaut

---

## Rapport HTML — `alfred_security_report.html`

Interface sombre avec :
- **Score global** 0–100 avec grade A→F (cercle coloré)
- **8 KPIs** en temps réel : score, gouvernance, conformité, menaces, incidents, appareils, audit, taux de refus
- **Tableau gouvernance** : 13 contrôles avec état, sévérité, action requise
- **Matrice de risques** : triée likelihood × impact
- **Tableau conformité** : GDPR + OWASP A01→A10

---

## Prérequis

```
Python 3.11+
pip install pytest python-dotenv bcrypt cryptography openpyxl
```

Fichier `.env` à la racine (copier `.env.example` et remplir les valeurs).

---

## Structure du dossier demo/

```
demo/
├── demo_cybersecurity.ps1       Script principal démo — Windows PowerShell
├── dashboard_security.bat       Lanceur dashboard rapide — double-clic Windows
├── demo_attack.py               Simulation d'attaques live — multiplateforme
├── alfred_security_report.html  Rapport HTML généré (créé à l'exécution)
└── README_DEMO.md               Ce fichier
```

---

## Chiffres clés à mettre en avant

| Indicateur | Valeur |
|------------|--------|
| Score de sécurité | **100/100 — Grade A** |
| Tests d'intrusion | **136/136 passés (100%)** |
| Contrôles gouvernance | **13/13 (100%)** |
| Conformité OWASP/GDPR | **10/10** |
| Vecteurs d'attaque bloqués | **SQL · XSS · Path traversal · Command · Prompt injection · SSRF** |
| Architecture | **Zero Trust · Local-First · Fail-secure** |

---

*ALFRED — Security by Design | Privacy by Design | Local-First Zero Trust*
