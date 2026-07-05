<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Micro-segmentation Réseau — Configuration VLAN
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.8.22
VERSION  : V1.2
CREATED  : 2026-06-18
UPDATED  : 2026-07-05
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Micro-segmentation Réseau — Configuration VLAN

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.22  
> **Version :** 1.2 — 2026-07-05  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Horizon :** Implémentation Juillet 2026  
> **Statut :** En cours — VLAN switch+ER605 configurés et testés (section 6.6), ACL inter-VLAN restantes

---

## 1. Objectif

Isoler le PC Alfred des autres équipements du réseau local via micro-segmentation VLAN pour réduire la surface d'attaque et prévenir les mouvements latéraux.

---

## 2. Architecture VLAN cible

| VLAN | ID | Sous-réseau | Équipements | Description |
|---|---|---|---|---|
| **VLAN_PC_ALFRED** | 10 | 192.168.10.0/24 | PC Alfred (Minisforum) | Isolé — trafic sortant HTTPS uniquement |
| **VLAN_ADMIN** | 20 | 192.168.20.0/24 | PC de gestion | Administration réseau + accès VLAN10 |
| **VLAN_IOT** | 30 | 192.168.30.0/24 | Appareils IoT | Isolé — pas d'accès inter-VLAN |
| **VLAN_DEFAULT** | 1 | 192.168.1.0/24 | Appareils généraux | Réseau domestique standard |

---

## 3. Règles inter-VLAN

| Source | Destination | Action | Justification |
|---|---|---|---|
| VLAN_PC_ALFRED | Internet (HTTPS) | ALLOW | APIs externes (OpenAI) |
| VLAN_PC_ALFRED | VLAN_DEFAULT | DENY | Isolation PC Alfred |
| VLAN_PC_ALFRED | VLAN_IOT | DENY | Isolation IoT |
| VLAN_ADMIN | VLAN_PC_ALFRED | ALLOW (SSH/RDP) | Administration uniquement |
| VLAN_IOT | Tous | DENY sauf Internet | Isolation stricte IoT |

---

## 4. Plan d'implémentation Q3 2026

| Étape | Action | Responsable | Délai |
|---|---|---|---|
| 1 | Configuration VLANs sur SG108E | Céline Darras | Juillet 2026 |
| 2 | Paramétrage inter-VLAN routing ER605 | Céline Darras | Juillet 2026 |
| 3 | Déplacement PC Alfred sur port VLAN10 | Céline Darras | Juillet 2026 |
| 4 | Test connectivité + isolation | Céline Darras | Juillet 2026 |
| 5 | Documentation configuration finale | Céline Darras | Août 2026 |
| 6 | Audit et validation | Céline Darras | Août 2026 |

---

## 6. Procédure d'implémentation détaillée

> Équipement : Switch TP-Link TL-SG108E (Easy Smart, VLAN 802.1Q — géré via son
> interface web locale ou l'utilitaire "Easy Smart Configuration Utility", **pas**
> intégré au contrôleur SDN Omada) + Routeur TP-Link Omada ER605 (mode standalone,
> interface locale `192.168.0.1`).

### 6.1 Préparation — éviter tout auto-blocage (lockout)

1. Exporter/sauvegarder la configuration actuelle de l'ER605 (Réglages → Sauvegarde).
2. Garder un poste connecté en Ethernet direct au routeur pendant toute la manipulation
   (ne pas dépendre du Wi-Fi, qui peut être coupé pendant la reconfiguration).
3. Changer immédiatement les identifiants admin par défaut du routeur **et** du switch
   (config actuelle = "par défaut", donc probablement `admin/admin`).

### 6.2 Switch TL-SG108E — création des VLAN 802.1Q

1. Interface web du switch (IP par défaut `192.168.0.1`, ou assignation via l'utilitaire
   Easy Smart si aucune IP n'est encore configurée).
2. Onglet **VLAN → 802.1Q VLAN** → activer.
3. Créer les VLAN 10 (PC Alfred), 20 (Admin), 30 (IoT) — le VLAN 1 existe par défaut.
4. Affectation des ports :
   - Port relié au routeur (uplink) : **Tagged** sur VLAN 1/10/20/30 (trunk).
   - Port(s) du PC Alfred : **Untagged**, PVID 10.
   - Port(s) poste d'administration : **Untagged**, PVID 20.
   - Port(s) équipements IoT réseau : **Untagged**, PVID 30.
   - Ports restants : **Untagged** VLAN 1 (PVID 1, défaut).
5. Vérifier avant de sauvegarder que le port utilisé pour administrer le switch reste
   accessible après application (risque de se couper soi-même du switch sinon).

> **Note caméra eMeet PTZ Pixy** : si la caméra est connectée en USB au PC Alfred (cas
> le plus probable pour ce modèle), elle n'est pas un équipement réseau et n'a pas
> besoin d'être placée sur VLAN_IOT — elle hérite du VLAN10 du PC. VLAN_IOT reste
> réservé aux futurs équipements réseau (caméra IP, capteurs, etc.). À confirmer selon
> le mode de connexion réel avant migration.

### 6.3 Routeur ER605 — interfaces VLAN et DHCP

1. **Réseau → LAN → Interfaces** : créer une interface par VLAN (10, 20, 30) avec les
   sous-réseaux définis en section 2, DHCP activé sur chacune (plage dédiée).
2. Configurer le port LAN physique relié au switch en **trunk** (tagged 10/20/30 +
   natif VLAN 1).
3. Conserver VLAN 1 (192.168.1.0/24) comme réseau domestique par défaut.

### 6.4 Règles pare-feu inter-VLAN (ACL)

Traduire le tableau de la section 3 en règles ACL sur l'ER605
(**Transmission → Contrôle du réseau → Règles ACL**), dans cet ordre (règles
spécifiques avant règle générale) :

1. VLAN_PC_ALFRED → Internet (HTTPS/443) : ALLOW
2. VLAN_ADMIN → VLAN_PC_ALFRED (SSH/RDP) : ALLOW
3. VLAN_PC_ALFRED → VLAN_DEFAULT : DENY
4. VLAN_PC_ALFRED → VLAN_IOT : DENY
5. VLAN_IOT → tout sauf Internet : DENY
6. Règle finale implicite : DENY (vérifier qu'aucune règle "allow all" par défaut ne
   subsiste après création des ACL).

### 6.5 Migration et tests (ordre recommandé)

1. Basculer le PC Alfred sur le port VLAN10 → tester accès Internet + dashboard local.
2. Basculer les équipements admin sur VLAN20 → tester accès SSH/RDP vers PC Alfred.
3. Test d'isolation : depuis VLAN_DEFAULT (VLAN1), tenter un ping/accès vers le PC
   Alfred → doit échouer.
4. Basculer les éventuels équipements IoT réseau sur VLAN30 → vérifier qu'ils gardent
   l'accès Internet nécessaire mais aucun accès aux autres VLAN.
5. Documenter les résultats des tests dans l'historique de révision ci-dessous.

### 6.6 Réalisation — 2026-07-05

Switch TL-SG108E et ER605 configurés et testés :

- **Switch** : 802.1Q activé, VLAN 10 (`ALFRED_COR`, port 1 tagged/port 3 untagged),
  VLAN 20 (`ADMIN`, port 1 tagged/port 2 untagged), VLAN 30 (`IOT`, port 1 tagged
  seul, aucun port untagged pour l'instant). PVID : port 2 → 20, port 3 → 10.
- **ER605** : interfaces réseau créées en mode Normal (isolation désactivée,
  gérée via ACL section 6.4 à venir) — `PC_ALFRED` (VLAN10, `192.168.10.1/24`,
  DHCP `192.168.10.100-200`), `ADMIN` (VLAN20, `192.168.20.1/24`, DHCP
  `192.168.20.100-200`), `IOT` (VLAN30, `192.168.30.1/24`, DHCP
  `192.168.30.100-200`). Ports LAN 2-5 de l'ER605 auto-configurés en trunk
  (tagged 10/20/30, untagged natif VLAN1) — aucune configuration manuelle
  nécessaire côté trunk ER605.
- **Test de bascule** : reconfiguration temporaire nécessaire (port 3 remis en
  PVID 1 le temps de créer les interfaces VLAN sur l'ER605, car celui-ci ne
  comprenait pas encore les trames taguées — effet ciseau attendu lors d'une
  migration VLAN, cf. section 6.5). Une fois les interfaces ER605 créées, port 3
  repassé en PVID 10 sans problème.
- **Validation** : PC Alfred obtient bien `192.168.10.100/24`, passerelle
  `192.168.10.1`. Accès Internet (`ping 8.8.8.8` OK) et accès dashboard local
  (`localhost:8000/dashboard/...`) confirmés fonctionnels depuis VLAN10.
- **Découverte de sécurité pendant les tests** : l'adaptateur **Wi-Fi 6** de PC
  Alfred était actif et connecté directement au réseau de la Bbox
  (`192.168.1.119`, hors VLAN), malgré l'hypothèse initiale qu'aucun Wi-Fi
  n'était configuré sur cette machine. Cela créait un accès parallèle
  contournant entièrement l'isolation VLAN. **Corrigé** : adaptateur désactivé
  (`Disable-NetAdapter -Name "Wi-Fi 6"`, admin requis). Détail dans
  `acces_distant_durcissement_wan.md`.
- **Restant à faire** : règles ACL inter-VLAN (section 6.4, pas encore
  appliquées — actuellement tous les VLAN peuvent se joindre librement, la
  segmentation existe mais l'isolation n'est pas encore active), test
  d'isolation VLAN_DEFAULT (étape 3 ci-dessus), migration du poste admin
  (Dell, déjà sur VLAN20 côté switch) et test SSH/RDP vers PC Alfred.

---

## 7. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.22 |
| 1.1 | 2026-07-05 | Céline Darras | Ajout procédure d'implémentation détaillée (section 6) — préparation exécution Juillet 2026 |
| 1.2 | 2026-07-05 | Céline Darras | VLAN 10/20/30 configurés et testés sur switch+ER605 (section 6.6) — Internet et dashboard local validés depuis VLAN10, découverte et correction Wi-Fi non désactivé sur PC Alfred |

> **Cognitive Products Lab — Confidentiel interne**
