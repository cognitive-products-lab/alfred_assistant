# Micro-segmentation Réseau — Configuration VLAN

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.8.22  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Horizon :** Implémentation Q3 2026  
> **Statut :** Planifié / Documentation préalable

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

## 5. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.8.22 |

> **Cognitive Products Lab — Confidentiel interne**
