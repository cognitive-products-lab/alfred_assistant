# Accès ConnectBot → ALFRED PC

## Problème courant

Depuis ConnectBot, vous atterrissez dans `C:\Users\<nom>` (shell Windows CMD).  
Les commandes Linux (`ls`, `cd /mnt/d/...`) ne fonctionnent pas en CMD.

---

## Solution rapide (sans configuration)

```cmd
cd /d D:\PROJET_ALFRED\ALFRED_PC
```

> En CMD Windows, `cd D:\...` **ne change pas de lecteur**.  
> Il faut obligatoirement le flag `/d` pour changer de lecteur ET de dossier en même temps.

---

## Solution permanente (arriver automatiquement dans le bon dossier)

Lancez ce script **une seule fois** en PowerShell Administrateur sur le PC :

```powershell
cd D:\PROJET_ALFRED\ALFRED_PC
.\tools\connectbot\setup_ssh_windows.ps1
```

Après ça, chaque connexion ConnectBot ouvre directement `D:\PROJET_ALFRED\ALFRED_PC`.

---

## Commandes utiles en CMD Windows (≠ Linux)

| Linux       | CMD Windows              |
|-------------|--------------------------|
| `ls`        | `dir`                    |
| `pwd`       | `cd`                     |
| `cat`       | `type`                   |
| `cp`        | `copy`                   |
| `mv`        | `move`                   |
| `rm`        | `del`                    |
| `mkdir`     | `md`                     |

---

## Option alternative : WSL (Linux dans Windows)

Si WSL est installé, tapez `wsl` dans ConnectBot pour passer en shell Linux :

```cmd
wsl
cd /mnt/d/PROJET_ALFRED/ALFRED_PC
ls -la
python3 src/main.py
```

---

## Trouver l'IP du PC pour ConnectBot

Sur le PC Windows :

```cmd
ipconfig
```

Chercher `Adresse IPv4` sous votre carte réseau (ex: `192.168.1.XX`).

Dans ConnectBot : **Hôte** = cette IP, **Port** = 22.
