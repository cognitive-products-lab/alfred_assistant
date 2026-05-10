# ALFRED — Assistant Cognitif Adaptatif

## Principes fondamentaux
- **Local-first** : toutes les données restent en local
- **Security by Design** : sécurité intégrée dès la conception
- **Zero Trust** : aucune confiance implicite

## Démarrage rapide
\\\powershell
# 1. Créer et activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configurer les secrets
Copy-Item .env.example .env
# Éditer .env avec tes vraies valeurs

# 4. Lancer ALFRED
python -m src.main
\\\

## Architecture
V1 -> Pipeline minimal fonctionnel
V2 -> Intelligence décisionnelle
V2++ -> Valeur métier
V3 -> Compagnon cognitif adaptatif
V4 -> Action sur l'environnement
