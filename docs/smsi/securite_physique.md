<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Sécurité Physique — Zones Sécurisées
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.7.1
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Sécurité Physique — Zones Sécurisées

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.7.1  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Zones physiques définies

### Zone 1 — Bureau Principal (Zone Sécurisée)
- **Localisation :** Domicile Céline Darras — bureau personnel dédié
- **Équipements :** PC Alfred (Minisforum MS-S1 Max), Disque LaCie, Switch SG108E
- **Accès :** Accès restreint — pièce fermée à clé hors présence
- **Menaces mitigées :** Accès physique non autorisé, vol d'équipement

### Zone 2 — Réseau Local (Zone Contrôlée)
- **Équipements :** Routeur-Firewall TP-Link ER605, Switch manageable SG108E
- **Accès réseau :** WiFi sécurisé WPA3, réseau câblé dédié PC Alfred
- **Segmentation :** VLAN isolation PC Alfred planifié Q3 2026

### Zone 3 — Stockage Hors-ligne (Zone Haute Sécurité)
- **Équipements :** Disque LaCie chiffré (sauvegardes)
- **Stockage :** Rangement physique sécurisé, déconnecté du réseau sauf sauvegarde

---

## 2. Mesures de protection physique

| Mesure | Statut | Détail |
|---|---|---|
| Verrouillage bureau | ✅ En place | Porte fermée à clé hors présence |
| Chiffrement disque dur principal | ✅ En place | Disque D: chiffré (VeraCrypt) |
| Chiffrement sauvegarde LaCie | ✅ En place | Chiffrement intégral |
| Écran verrouillé automatiquement | ✅ En place | Timeout 5 min + MFA à déverrouillage |
| Cable antivol PC | ⚠️ Recommandé | À mettre en place |
| Alimentation ondulée (UPS) | 🟡 Planifié | Protection coupure courant |

---

## 3. Procédure en cas de compromission physique

1. **Vol ou perte d'équipement :** Déclarer incident P1, révoquer tous les accès, changer les clés cryptographiques, notifier CNIL si données personnelles concernées
2. **Accès physique non autorisé détecté :** Incident P2, inspection des équipements, vérification intégrité des données
3. **Incendie / sinistre :** Activer PCA, restaurer depuis sauvegarde LaCie (si préservée) ou backup secondaire

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.7.1 |

> **Cognitive Products Lab — Confidentiel interne**
