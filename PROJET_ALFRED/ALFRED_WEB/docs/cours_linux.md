# Commandes Linux — ALFRED

> Semaine 1 : Decouvrir le terminal Linux

---

## Commandes de navigation

```bash
pwd               # Afficher le dossier courant (Print Working Directory)
ls                # Lister les fichiers du dossier
ls -la            # Lister avec details + fichiers caches
cd dossier        # Se deplacer dans un dossier
cd ..             # Remonter d'un niveau
cd ~              # Aller dans ton dossier personnel
```

## Commandes de creation

```bash
mkdir mon_dossier             # Creer un dossier
mkdir -p a/b/c                # Creer plusieurs niveaux d'un coup
touch fichier.txt             # Creer un fichier vide
cat fichier.txt               # Afficher le contenu d'un fichier
echo "texte" > fichier.txt    # Ecrire dans un fichier (efface l'existant)
echo "texte" >> fichier.txt   # Ajouter a la fin d'un fichier
```

## Commandes de gestion de fichiers

```bash
cp source destination    # Copier un fichier
mv source destination    # Deplacer / renommer
rm fichier.txt           # Supprimer un fichier (ATTENTION irreversible)
rm -r dossier            # Supprimer un dossier et son contenu
```

## Permissions (Cybersecurite)

```bash
chmod 755 fichier.sh    # Donner les droits d'execution
chmod 644 fichier.txt   # Lecture seule pour les autres
chown user fichier      # Changer le proprietaire
sudo commande           # Executer en mode administrateur
```

### Signification des chiffres chmod :
- **7** = lecture + ecriture + execution (rwx)
- **6** = lecture + ecriture (rw-)
- **5** = lecture + execution (r-x)
- **4** = lecture seule (r--)

## EXERCICES Semaine 1

```bash
# 1. Afficher ton dossier courant
pwd

# 2. Creer la structure ALFRED_WEB
mkdir -p ALFRED_WEB/{frontend,backend,database,scripts,docs,logs}

# 3. Creer un fichier test
touch ALFRED_WEB/test.txt

# 4. Verifier que tout est cree
ls -la ALFRED_WEB/

# 5. Ecrire dans le fichier de log
echo "[INFO] Premier test Linux" >> ALFRED_WEB/logs/activity.log
```

---

*Fiche creee le 21/05/2026 — Semaine 1 Plan ALFRED 2026*
