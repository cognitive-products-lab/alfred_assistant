# Chantier — Système d'audit complet par norme
## Vers les certifications officielles CPL

> ✅ Phase 1 accomplie — 2026-06-18 (Sprint conformité 42% → 97% A+)
> Dashboard automatique opérationnel · 24 preuves SMSI · Audit horodaté à chaque commit
> Prochaine phase : docs/audits/ GAP analysis + pré-audit ISO 27001 externe (2027 Q1)

---

## Vision

Créer un **système d'audit interne structuré** pour chaque norme applicable à CPL.
Chaque audit couvre :
- La liste exhaustive des exigences de la norme
- Le statut de conformité par exigence (conforme / partiel / non-conforme / N/A)
- Les preuves documentaires associées (liens vers fichiers existants)
- Les écarts identifiés (GAP analysis)
- Le plan de remédiation avec responsable et date cible
- Le niveau de maturité (0-5 selon CMM)

Ce système permettra de :
1. Connaître l'état de conformité réel à tout moment
2. Prioriser les efforts de remédiation
3. Préparer les audits externes et certifications officielles
4. Démontrer la conformité aux clients B2B et partenaires institutionnels

---

## Normes et certifications cibles

### Niveau 1 — Certifications prioritaires

#### ISO 27001:2022
- **Organisme** : ISO / auditeur certifié COFRAC
- **Périmètre CPL** : Système de management de la sécurité de l'information (SMSI)
- **Livrables audit** : 93 contrôles de l'Annexe A, déclaration d'applicabilité (SoA)
- **Fichier audit** : `docs/audits/iso27001_audit.json` + `iso27001_soa.md`
- **Durée préparation estimée** : 12-18 mois

#### RGPD / CNIL — Conformité documentée
- **Organisme** : CNIL (contrôle) / DPO interne ou externe
- **Périmètre** : Tous traitements CPL (7 traitements documentés + futurs)
- **Livrables audit** : Registre art.30 ✅, AIPD par traitement sensible, procédures droits
- **Fichier audit** : `docs/audits/rgpd_audit_checklist.md`
- **Durée** : 3-6 mois pour atteindre conformité documentée complète

### Niveau 2 — Certifications structurantes

#### AI Act — Conformité systèmes haut risque
- **Organisme** : Autorité nationale compétente (ANSSI / futur AI Office France)
- **Périmètre** : ALFRED CPL (risque élevé potentiel) + ARTHUR (risque élevé)
- **Livrables audit** : Documentation technique (art.11), système de gestion des risques IA (art.9), logs (art.12), notice de transparence (art.13)
- **Fichier audit** : `docs/audits/aiact_conformite.md`
- **Échéance légale** : Août 2026 pour systèmes haut risque

#### NIS2 — Si CPL entre dans le périmètre
- **Organisme** : ANSSI
- **Périmètre** : Infrastructure SI CPL
- **Livrables audit** : Mesures art.21, procédures notification incidents
- **Fichier audit** : `docs/audits/nis2_audit.md`

### Niveau 3 — Certifications spécialisées

#### HDS — Hébergement Données de Santé (ARTHUR uniquement)
- **Organisme** : Organisme d'accréditation COFRAC
- **Périmètre** : Si ARTHUR collecte des données de santé d'enfants
- **Livrables** : 6 catégories d'hébergement, audit sur site
- **Fichier audit** : `docs/audits/hds_audit.md`
- **Prérequis** : ISO 27001 + ISO 20000-1

#### SecNumCloud — Hébergement cloud CPL futur
- **Organisme** : ANSSI
- **Périmètre** : Infrastructure cloud si CPL héberge des données sensibles
- **Fichier audit** : `docs/audits/secnumcloud_audit.md`

#### PASSI — Si CPL lance une activité de conseil SSI
- **Organisme** : ANSSI
- **Sous-domaines** : Audit organisationnel, architecture, configuration, code, pentest
- **Fichier audit** : `docs/audits/passi_audit.md`

---

## Structure d'un fichier d'audit (JSON)

```json
{
  "_meta": {
    "norme": "ISO 27001:2022",
    "version_norme": "2022",
    "date_audit": "2026-06-16",
    "auditeur": "Céline Rousselot (auto-audit interne)",
    "statut_global": "en_cours",
    "score_maturite_global": 1.8,
    "next_review": "2026-12-16"
  },
  "controls": [
    {
      "id": "A.5.1",
      "titre": "Politiques de sécurité de l'information",
      "chapitre": "5. Politiques organisationnelles",
      "statut": "partiel",
      "maturite": 2,
      "preuve": "docs/gouvernance/blueprint_gouvernance_complet.md",
      "gap": "PSSI formelle non rédigée — blueprint existant à formaliser",
      "action": "Rédiger PSSI formelle selon template ANSSI",
      "responsable": "Céline Rousselot",
      "date_cible": "2026-09-01",
      "date_realisation": null,
      "commentaire": ""
    }
  ],
  "soa": {
    "description": "Statement of Applicability — liste des 93 contrôles et justification d'inclusion/exclusion",
    "controls_applicables": 85,
    "controls_exclus": 8,
    "exclusions_justifiees": [
      "A.14.2.7 — Développement externalisé : non applicable (dev interne uniquement)"
    ]
  }
}
```

---

## Structure d'une checklist d'audit (Markdown)

```markdown
# Audit [NORME] — CPL [Date]

## Résumé exécutif
- Score global : X/100
- Niveau de maturité : X/5 (CMM)
- Contrôles conformes : XX / YY
- Écarts critiques : X
- Prochaine révision : [date]

## Section [N] — [Titre]

### [N.1] [Exigence]
| | |
|--|--|
| **Exigence** | Texte exact de l'exigence normative |
| **Statut** | ✅ Conforme / ⚠️ Partiel / ❌ Non conforme / N/A |
| **Maturité** | 0-5 |
| **Preuve** | Lien vers document de preuve |
| **Gap identifié** | Description de l'écart |
| **Action** | Action corrective requise |
| **Responsable** | Nom / rôle |
| **Date cible** | JJ/MM/AAAA |

```

---

## Niveaux de maturité (CMM adapté)

| Niveau | Label | Description |
|--------|-------|-------------|
| 0 | Inexistant | Aucune pratique en place |
| 1 | Initial | Pratiques ad hoc, non documentées |
| 2 | Reproductible | Pratiques documentées, application partielle |
| 3 | Défini | Processus formalisés, appliqués systématiquement |
| 4 | Maîtrisé | Mesures et indicateurs, amélioration continue |
| 5 | Optimisé | Innovation, benchmark, amélioration proactive |

---

## Roadmap de certification

```
✅ 2026 Q2 — Dashboard conformité (7 normes · 97% A+) + SMSI 24 preuves
✅ 2026 Q2 — RGPD 95.5% · ISO27001 98.4% · AI Act 91.7% · NIS2 100%
🔵 2026 Q3 — DPA OpenAI formalisée + VLAN isolation PC Alfred
🟡 2026 Q3 — Audit interne RGPD complet (checklist + GAP analysis) (checklist + GAP analysis)
2026 Q3 — AIPD pour T001 (profil psychologique) et T004 (enfant ARTHUR)
2026 Q4 — Audit interne ISO 27001 (93 contrôles, SoA)
2026 Q4 — PSSI formelle rédigée et approuvée
2027 Q1 — Audit externe ISO 27001 (pré-audit)
2027 Q2 — Certification ISO 27001 (si budget disponible)
2027 Q2 — Conformité AI Act complète (ARTHUR + ALFRED CPL)
2027 Q4 — Évaluation HDS si ARTHUR en production avec données santé
```

---

## Fichiers à créer (chantier)

```
docs/audits/
├── README_AUDITS.md              ← Guide du système d'audit
├── iso27001/
│   ├── iso27001_audit.json       ← 93 contrôles + statut + preuves
│   ├── iso27001_soa.md           ← Déclaration d'applicabilité
│   └── iso27001_gap_analysis.md  ← Écarts et plan de remédiation
├── rgpd/
│   ├── rgpd_checklist.md         ← Exigences RGPD par article
│   ├── rgpd_aipd_t001.md         ← AIPD Traitement #001
│   ├── rgpd_aipd_t004.md         ← AIPD Traitement #004 (ARTHUR)
│   └── rgpd_droits_procedure.md  ← Procédure exercice des droits
├── aiact/
│   ├── aiact_classification.md   ← Classification par produit
│   ├── aiact_haut_risque_arthur.md ← Dossier conformité ARTHUR
│   └── aiact_haut_risque_cpl.md  ← Dossier conformité ALFRED CPL
├── nis2/
│   └── nis2_perimetre_analyse.md ← CPL dans le périmètre ?
├── hds/
│   └── hds_readiness.md          ← Évaluation préalable
└── secnumcloud/
    └── secnumcloud_readiness.md  ← Évaluation préalable
```

---

*À démarrer après validation et merge de PR #10*  
*Créé le 2026-06-16 — Cognitive Products Lab*
