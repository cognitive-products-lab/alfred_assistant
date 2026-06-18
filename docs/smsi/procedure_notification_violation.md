# Procédure de Notification de Violation de Données — 72h CNIL

> **Référence :** RGPD Art. 33-34 — Notification violations données personnelles  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras (DPO de fait)  
> **Statut :** Approuvé

---

## 1. Obligation légale

**Art. 33 RGPD :** En cas de violation de données à caractère personnel, le responsable de traitement (CPL) notifie la CNIL **dans les 72 heures** suivant la prise de connaissance.

**Art. 34 RGPD :** Si la violation est susceptible d'engendrer un risque élevé pour les droits et libertés, les personnes concernées sont notifiées **sans délai injustifié**.

---

## 2. Définition — Violation de données personnelles

Une violation est tout incident de sécurité entraînant, de manière accidentelle ou illicite :
- La **destruction** de données personnelles
- La **perte** ou l'**altération** de données personnelles
- La **divulgation** non autorisée ou l'**accès** non autorisé à des données personnelles

---

## 3. Procédure de décision — Arbre de décision

```
Incident détecté
      │
      ▼
Données personnelles concernées ?
  │ OUI                    │ NON
  ▼                        ▼
Risque pour droits    Documentation
et libertés ?         interne uniquement
  │                        
  ├─ RISQUE NÉGLIGEABLE → Documentation interne (registre incidents)
  │
  ├─ RISQUE FAIBLE → Notification CNIL (Art. 33) dans 72h
  │
  └─ RISQUE ÉLEVÉ  → Notification CNIL (Art. 33) + Notification personnes (Art. 34)
```

---

## 4. Formulaire de notification CNIL

**Canal :** https://notifications.cnil.fr (portail officiel CNIL)

**Informations à fournir (Art. 33.3) :**
1. Nature de la violation (destruction, perte, divulgation, accès non autorisé)
2. Catégories et nombre approximatif de personnes concernées
3. Catégories et nombre approximatif d'enregistrements affectés
4. Coordonnées du DPO ou point de contact
5. Conséquences probables de la violation
6. Mesures prises ou envisagées pour remédier et atténuer les effets

**DPO / Contact CPL :**
- Nom : Céline Darras
- Organisation : Cognitive Products Lab
- Email : darkmiroir@gmail.com
- Rôle : Fondatrice / Responsable Sécurité

---

## 5. Notification aux personnes concernées (Art. 34)

Si risque élevé pour les droits et libertés :
- Canal : message direct via ALFRED ou email
- Délai : sans délai injustifié après la prise de connaissance
- Contenu minimum :
  - Description claire de la violation en langage accessible
  - Coordonnées du DPO
  - Conséquences probables
  - Mesures prises pour remédier

**Exceptions (pas de notification individuelle requise si) :**
- Des mesures de protection techniques ont été appliquées (ex : chiffrement AES-256 actif) rendant les données inintelligibles
- Des mesures ont été prises rendant le risque élevé improbable
- La notification individuelle exigerait un effort disproportionné → communication publique à la place

---

## 6. Registre des violations (Art. 33.5)

Toutes les violations doivent être documentées dans `data/security/incident_register.json` y compris :
- Celles qui ne nécessitent pas de notification CNIL (risque négligeable)
- Les faits, effets et mesures prises

---

## 7. Délais récapitulatifs

| Étape | Délai |
|---|---|
| Prise de connaissance → Notification CNIL | **72 heures max** |
| Prise de connaissance → Notification personnes (risque élevé) | **Sans délai injustifié** |
| Documentation interne (tous incidents) | **Immédiate** |
| Rapport post-incident complet | **5 jours ouvrés (P1)** |

---

## 8. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité RGPD Art. 33-34 |

> **Cognitive Products Lab — Confidentiel interne**
