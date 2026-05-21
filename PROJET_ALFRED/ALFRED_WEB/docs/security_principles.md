# Principes de Cybersécurité — ALFRED

> Semaine 1 — Fondamentaux cybersécurité (Plan Cybersécurité ALFRED 2026)

---

## La Triade CIA

| Principe | Definition | Exemple ALFRED |
|---|---|---|
| **Confidentialite** | Seules les personnes autorisees peuvent acceder aux donnees | Seul l'admin voit les mots de passe |
| **Integrite** | Les donnees ne sont pas modifiees sans autorisation | Les logs ne peuvent pas etre modifies |
| **Disponibilite** | Le systeme est accessible quand on en a besoin | Le dashboard ALFRED doit rester en ligne |

---

## Vocabulaire essentiel

### Menace
Une **menace** est une action potentielle qui pourrait causer un dommage.
- Exemple : Un hacker tente de se connecter au serveur ALFRED.

### Vulnerabilite
Une **vulnerabilite** est une faille dans le systeme.
- Exemple : Un mot de passe trop simple ("admin123").

### Risque
Le **risque** = Probabilite d'une menace x Impact sur le systeme.
- Exemple : Si ALFRED utilise HTTP (pas HTTPS), risque d'intercepter les donnees.

---

## Security by Design

Integrer la securite DES le debut du projet, pas a la fin.

Regles appliquees dans ALFRED :
- [ ] Validation de toutes les entrees utilisateur
- [ ] Jamais de mots de passe en clair dans le code
- [ ] Logs de toutes les actions sensibles
- [ ] Acces minimum necessaire pour chaque utilisateur

---

## Ports reseau a connaitre

| Port | Protocole | Usage |
|---|---|---|
| 80 | HTTP | Web non securise |
| 443 | HTTPS | Web securise |
| 22 | SSH | Acces serveur Linux |
| 3306 | MySQL | Base de donnees |
| 27017 | MongoDB | Base NoSQL |

---

## Bonnes pratiques Semaine 1

1. Ne jamais mettre un mot de passe dans le code source
2. Toujours valider les entrees utilisateur
3. Utiliser HTTPS plutot que HTTP
4. Journaliser les evenements importants dans les logs

---

*Document cree le 21/05/2026 — Semaine 1 Plan ALFRED 2026*
