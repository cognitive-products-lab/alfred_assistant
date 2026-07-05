<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Accès distant sécurisé (VPN) et durcissement WAN
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.8.20, A.6.7
VERSION  : V1.3
CREATED  : 2026-07-05
UPDATED  : 2026-07-05
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : En cours — double NAT résolu, pare-feu WAN vérifié, faille Wi-Fi PC Alfred corrigée, VPN restant
============================================================
-->
# Accès distant sécurisé (VPN) et durcissement WAN

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.20 (Sécurité réseau), A.6.7 (Travail à distance)
> **Version :** 1.2 — 2026-07-05
> **Propriétaire :** Cognitive Products Lab — Céline Darras
> **Horizon :** Implémentation Juillet 2026 (avec [vlan_config.md](vlan_config.md))
> **Statut :** En cours — double NAT résolu (section 1bis), pare-feu WAN ER605 vérifié (section 3), VPN/Wi-Fi/VLAN restants

---

## 1. Objectif

Compléter la micro-segmentation VLAN ([vlan_config.md](vlan_config.md)) par :
- un accès distant à ALFRED sans exposer directement de port (SSH/RDP/HTTP) sur Internet ;
- un durcissement de la face WAN du routeur Omada ER605 pour réduire la surface
  d'attaque exposée à Internet.

Principe directeur : aucun accès distant direct au VLAN_PC_ALFRED — tout accès
distant transite par le VPN, atterrit sur VLAN_ADMIN, puis est soumis à la règle
inter-VLAN existante (`VLAN_ADMIN → VLAN_PC_ALFRED (SSH/RDP) : ALLOW`). Cohérent
avec le principe Zero Trust de la [PSSI](../security/PSSI.md).

---

## 1bis. Résolution du double NAT (Bbox Must → ER605) — Réalisé 2026-07-05

> Prérequis à l'accès distant : sans cette étape, tout accès entrant (SSH, VPN)
> aurait nécessité une redirection de port des deux côtés (Bbox + ER605).

Constat : la Bbox Must (gamme Bouygues actuelle) ne propose **pas de vrai mode
bridge total** (contrairement aux anciens modèles Bbox 4K/Miami) — seul un mode
DMZ est disponible côté Bbox.

Procédure appliquée :

1. Réservation DHCP statique de l'ER605 sur la Bbox (`192.168.1.254` → DHCP →
   règles d'IP statique) : IP WAN fixe **192.168.1.120**, MAC `20:e1:5d:90:22:6b`.
   (L'ER605 conserve par ailleurs son IP LAN par défaut `192.168.0.1` côté
   interne, invisible depuis la Bbox — à ne pas confondre.)
2. Activation du **Mode DMZ** (Bbox → Réglages avancés → Redirection de port →
   DMZ) ciblant `192.168.1.120`, avec l'option "Ne pas rediriger les flux
   port 53/UDP" conservée (protection DNS activée) — recommandée par défaut,
   sans impact sur l'accès SSH/VPN.
3. Test de validation : connexion SSH depuis un réseau externe vers le PC
   Alfred → **OK**, confirmant la levée du blocage double NAT.

Conséquence de sécurité : l'ER605 reçoit désormais tout le trafic entrant sans
filtrage préalable par la Bbox — son propre pare-feu (section 3 ci-dessous)
devient la seule protection WAN et doit être vérifié/appliqué avant toute
exposition supplémentaire (VPN notamment).

Restant à faire : désactiver le Wi-Fi de la Bbox et le remplacer par un point
d'accès Omada (EAP) derrière l'ER605/switch (cf. section 4 et `vlan_config.md`).

### Découverte de sécurité — 2026-07-05

Pendant les tests de bascule VLAN (`vlan_config.md` section 6.6), l'adaptateur
**Wi-Fi 6** de PC Alfred a été trouvé actif et connecté directement au réseau
de la Bbox (`192.168.1.119`), malgré l'hypothèse initiale (confirmée par
Céline en amont de la config VLAN) qu'aucun Wi-Fi n'était configuré sur cette
machine — seul l'Ethernet devait donner accès à Internet.

Impact : cette interface créait un accès parallèle à PC Alfred entièrement
en dehors du VLAN10 et de toutes les règles ACL prévues, contournant de fait
toute la segmentation réseau mise en place.

Correction appliquée : `Disable-NetAdapter -Name "Wi-Fi 6" -Confirm:$false`
(PowerShell en tant qu'administrateur). Confirmé désactivé via `Get-NetAdapter`
(statut `Disabled`).

Action de suivi recommandée : vérifier périodiquement (`Get-NetAdapter`) que
cette interface reste désactivée, notamment après mises à jour Windows qui
peuvent parfois réactiver des adaptateurs.

---

## 2. Accès distant — Serveur VPN sur l'ER605

### 2.1 Choix du protocole

| Protocole | Disponibilité ER605 | Recommandation |
|---|---|---|
| OpenVPN | Supporté (firmware standard) | **Retenu** — large compatibilité clients, chiffrement AES éprouvé |
| WireGuard | Selon version firmware — à vérifier sur l'interface avant de s'y engager | Alternative si disponible (plus léger, plus rapide) |
| IPsec/L2TP/PPTP | Supportés mais PPTP obsolète (à ne pas utiliser) | Non retenu (IPsec plus adapté à un site-à-site qu'à un accès nomade) |

> Vérifier la version de firmware de l'ER605 et les protocoles VPN réellement
> proposés dans l'interface avant de figer le choix ci-dessus.

### 2.2 Procédure de mise en œuvre

1. Mettre à jour le firmware de l'ER605 à la dernière version stable avant toute
   config VPN (correctifs de sécurité).
2. Activer le serveur OpenVPN (**VPN → OpenVPN**) :
   - Créer un compte VPN dédié, distinct du compte admin du routeur.
   - Restreindre la portée du serveur VPN au sous-réseau **VLAN_ADMIN
     (192.168.20.0/24)** uniquement — pas d'accès direct VLAN_PC_ALFRED ni VLAN_IOT.
   - Générer le fichier `.ovpn` (certificat + clé) et le transférer par un canal
     sécurisé (jamais par email en clair).
3. Sur le poste distant : client OpenVPN Connect officiel, mot de passe fort dédié.
4. Ne jamais activer de redirection de port (port forwarding) WAN→LAN vers le PC
   Alfred pour SSH/RDP/HTTP — le VPN est l'unique point d'entrée distant.
5. Journaliser les connexions VPN (logs ER605) et les croiser mensuellement avec la
   revue du dashboard sécurité ALFRED (`security_dashboard.py`).

---

## 3. Durcissement WAN de l'ER605

Checklist à appliquer avant mise en production du VPN :

| # | Action | Raison | Statut |
|---|---|---|---|
| 1 | Changer le mot de passe admin par défaut (routeur + switch) | Config par défaut = `admin/admin` probable | ✅ Vérifié 2026-07-05 — compte custom déjà en place sur l'ER605 |
| 2 | Désactiver UPnP côté WAN | Empêche l'ouverture automatique de ports par des applications | ✅ Vérifié 2026-07-05 — UPnP désactivé, portmap list vide |
| 3 | Désactiver la gestion à distance (remote management) depuis le WAN | L'administration ne doit être possible que depuis le LAN ou via VPN | ✅ Vérifié 2026-07-05 — table "Remote Management" vide, aucune règle |
| 4 | Désactiver la réponse au ping (ICMP) côté WAN | Réduit la visibilité aux scans externes automatisés | ⏳ À vérifier (Firewall → Attack Defense) |
| 5 | Vérifier qu'aucune règle de redirection de port (port forwarding) n'est active, sauf strictement nécessaire | Chaque port ouvert est une surface d'attaque | ✅ Vérifié 2026-07-05 — Virtual Servers, One-to-One NAT et NAT-DMZ tous vides sur l'ER605 (seule la DMZ côté Bbox, section 1bis, est active) |
| 6 | Activer le firewall SPI (Stateful Packet Inspection) si disponible | Filtrage des connexions non sollicitées | ⏳ À vérifier (Firewall → Attack Defense) |
| 7 | Désactiver WPS sur le Wi-Fi si géré par ce routeur | Le WPS est un vecteur d'attaque connu (brute-force PIN) | ⏳ À faire lors de la mise en place du point d'accès Omada (section 4) |
| 8 | Activer les logs de sécurité et les alertes du routeur | Détection d'anomalies (cf. `behavioral_detector.py` côté logiciel) | ⏳ À vérifier |

---

## 4. Articulation avec l'existant

- `config/security/network_policy.json` + `src/security/network_security.py`
  (filtrage IP, anti-SSRF, rate-limit) couvrent la sécurité réseau **applicative**
  (déjà actif — DdA A.8.20).
- Ce document couvre la sécurité réseau **physique/infrastructure** (VPN + WAN) —
  complémentaire, pas redondant.
- Une fois implémenté, mettre à jour `docs/smsi/declaration_applicabilite.md`
  (ligne A.8.20) pour référencer ce document, et ajouter une ligne A.6.7 (Travail à
  distance) si absente.

---

## 5. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-07-05 | Céline Darras | Création — VPN + durcissement WAN, complément à vlan_config.md |
| 1.1 | 2026-07-05 | Céline Darras | Ajout section 1bis — résolution du double NAT Bbox Must via DMZ (réalisé et testé, SSH OK) |
| 1.2 | 2026-07-05 | Céline Darras | Vérification pare-feu WAN ER605 (section 3, points 1/2/3/5) — mdp admin, UPnP, remote management, redirections de port : tous conformes |
| 1.3 | 2026-07-05 | Céline Darras | Découverte et correction : adaptateur Wi-Fi 6 de PC Alfred actif hors VLAN (contournait la segmentation), désactivé via Disable-NetAdapter |

> **Cognitive Products Lab — Confidentiel interne**
