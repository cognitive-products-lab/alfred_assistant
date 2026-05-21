#!/usr/bin/env python3
# ============================================================
# ALFRED_WEB - Premier script Python
# Semaine 1 : Variables, input, print, conditions
# ============================================================

# LECON 1 : Variables et print
nom_projet = "ALFRED"
version    = "1.0"
annee      = 2026

print("=" * 40)
print(f"  Bienvenue dans le projet {nom_projet}")
print(f"  Version : {version} | Annee : {annee}")
print("=" * 40)

# LECON 2 : Demander une saisie utilisateur (input)
prenom = input("\nQuel est ton prenom ? ")

# LECON 3 : Conditions (if / elif / else)
if prenom == "":
    print("Tu n'as pas saisi de prenom.")
elif len(prenom) < 2:
    print("Prenom trop court !")
else:
    print(f"\nBonjour {prenom} ! ALFRED est pret a t'aider.")

# LECON 4 : Boucle for
print("\n--- ALFRED repete 5 fois ---")
for i in range(1, 6):
    print(f"  [{i}] ALFRED est en ligne.")

# LECON 5 : Liste (structure de donnees)
langages = ["Python", "SQL", "Java", "PHP", "HTML"]
print(f"\nLangages a apprendre : {', '.join(langages)}")

# LECON 6 : Fonction simple
def bienvenue(nom):
    return f"Bonjour {nom}, bienvenue dans ALFRED !"

message = bienvenue(prenom if prenom else "utilisateur")
print(f"\n{message}")

print("\n[ALFRED] Script termine avec succes.")

# ============================================================
# EXERCICES A FAIRE (Semaine 1)
# ============================================================
# 1. Ajoute une variable "ville" et affiche-la
# 2. Crée une condition : si age > 18, afficher "majeur"
# 3. Crée une boucle qui affiche les chiffres de 10 à 1
# 4. Crée une fonction qui calcule l'age depuis l'annee de naissance
