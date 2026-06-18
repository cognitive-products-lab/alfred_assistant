# Procédure de Signalement d'Incidents — NIS2 Art. 23

> **Référence :** Directive (UE) 2022/2555 — NIS2 Art. 23  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Contexte NIS2

La Directive NIS2 impose aux entités essentielles et importantes de signaler les incidents significatifs à l'autorité nationale compétente (en France : **ANSSI** et **CERT-FR**).

**Statut CPL :** En phase V1, CPL n'est pas encore formellement qualifiée entité NIS2. Cette procédure est établie en anticipation de la croissance et par principe de conformité proactive.

---

## 2. Critères d'incident significatif (Art. 23 NIS2)

Un incident est significatif si :
- Il a causé ou est susceptible de causer une **perturbation opérationnelle grave**
- Il a causé des **pertes financières importantes** pour l'entité
- Il a affecté ou est susceptible d'affecter **d'autres personnes physiques ou morales** de manière considérable

---

## 3. Délais de notification (Art. 23.4)

| Délai | Obligation |
|---|---|
| **24 heures** | Alerte précoce à l'ANSSI/CERT-FR (si suspicion d'acte illicite ou impact transfrontalier) |
| **72 heures** | Notification d'incident complète avec évaluation initiale (gravité, indicateurs) |
| **1 mois** | Rapport final complet avec cause racine, mesures prises, impact |

---

## 4. Canal de signalement

**CERT-FR :** https://www.cert.ssi.gouv.fr/contact/  
**ANSSI — portail signalement :** https://www.ssi.gouv.fr  
**Email urgence CERT-FR :** cert-fr.cossi@ssi.gouv.fr  
**Téléphone CERT-FR :** +33 1 71 75 84 68

---

## 5. Contenu de la notification initiale (72h)

1. Identité de l'entité notifiante (CPL — Cognitive Products Lab)
2. Date et heure de détection
3. Description de l'incident (nature, systèmes affectés)
4. Évaluation préliminaire de la gravité et de l'impact
5. Mesures de containment déjà prises
6. Existence d'une violation de données personnelles (lien RGPD)

---

## 6. Lien avec la procédure incidents ALFRED

Cette procédure s'articule avec :
- `procedure_incidents.md` — procédure générale de gestion des incidents
- `procedure_notification_violation.md` — notification CNIL si données personnelles
- `data/security/incident_register.json` — registre centralisé

---

## 7. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité NIS2 Art. 23 |

> **Cognitive Products Lab — Confidentiel interne**
