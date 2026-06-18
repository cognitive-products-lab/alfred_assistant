# Analyse d'Impact sur la Protection des Données (AIPD)
## Traitement : Données de santé et de bien-être — ALFRED

---

**Référence :** AIPD-ALFRED-001  
**Version :** 1.0  
**Date :** 2026-06-18  
**Responsable du traitement :** Cognitive Products Lab — Céline (fondatrice)  
**Délégué à la protection des données (DPD) :** Fondatrice (auto-DPD, entité de moins de 250 personnes)  
**Base légale :** Art. 9 §2.a RGPD — Consentement explicite  
**Référentiel CNIL :** Lignes directrices AIPD CNIL (2018) + Guide RGPD santé

---

## 1. Contexte et finalité du traitement

### 1.1 Description du traitement

ALFRED est un assistant personnel IA fonctionnant en local (Local-First) sur le PC de l'utilisateur. Il traite des données de santé et de bien-être dans le cadre des fonctionnalités suivantes :

| Fonctionnalité | Données traitées | Fichier |
|---|---|---|
| Journalisation bien-être | Énergie, humeur, émotions | `data/memory/wellbeing_log.json` |
| Profil utilisateur | Mots-clés santé, indicateurs bien-être | `data/profile/user_profile.json` |
| Mémoire épisodique | Conversations incluant contexte santé | `data/memory/episodes.json` |
| Coaching santé | Recommandations basées sur l'état | Traitement en mémoire volatile |

### 1.2 Finalités

- **Principale :** Adaptation des réponses de l'IA au contexte de bien-être de l'utilisateur
- **Secondaire :** Traçabilité longitudinale pour coaching personnalisé
- **Exclue explicitement :** Aucune transmission à des tiers, aucune profilage commercial, aucun partage

### 1.3 Catégories de personnes concernées

- Utilisateur principal (unique) : Céline
- Version future ARTHUR (enfants) — fera l'objet d'une AIPD distincte

---

## 2. Nécessité et proportionnalité

### 2.1 Minimisation des données

| Critère | Évaluation | Mesure |
|---|---|---|
| Données collectées | Minimales — seulement ce que l'utilisateur saisit | ✅ Conforme |
| Durée de conservation | 2 ans (wellbeing_log) — configurable | ✅ Conforme |
| Accès | Local uniquement, chiffrement Fernet AES-256 | ✅ Conforme |
| Transferts hors UE | Aucun (Local-First) | ✅ Conforme |

### 2.2 Mesures de minimisation implémentées

- Les données de santé ne transitent pas via API externe sauf consentement explicite supplémentaire
- Le chiffrement au repos couvre les champs `health_keywords` dans `user_profile.json`
- L'utilisateur peut supprimer toute donnée via commande `/forget` (Art. 17)

---

## 3. Identification et évaluation des risques

### 3.1 Risque 1 — Accès non autorisé aux données de santé

| | |
|---|---|
| **Menace** | Accès physique ou logique non autorisé au PC |
| **Probabilité** | Faible (PC personnel, usage unique) |
| **Impact** | Élevé (données de santé sensibles) |
| **Risque résiduel** | Moyen |
| **Mesures** | Chiffrement disque D: (BitLocker) · Fernet AES-256 champs sensibles · MFA obligatoire · Verrouillage session |

### 3.2 Risque 2 — Fuite via modèle LLM externe

| | |
|---|---|
| **Menace** | Transmission de données de santé à une API LLM tierce (OpenAI, Anthropic…) |
| **Probabilité** | Moyenne (usage API dans les prompts) |
| **Impact** | Élevé |
| **Risque résiduel** | Moyen → Faible après mesures |
| **Mesures** | `output_filter.py` filtre les PII avant envoi API · Pas d'injection automatique du wellbeing_log dans les prompts · DPA avec sous-traitants (voir RGPD-09) |

### 3.3 Risque 3 — Perte ou corruption des données

| | |
|---|---|
| **Menace** | Défaillance disque ou ransomware |
| **Probabilité** | Faible |
| **Impact** | Moyen |
| **Risque résiduel** | Faible |
| **Mesures** | Sauvegarde LaCie chiffrée · Export Art. 20 disponible · Chiffrement empêche la corruption silencieuse |

### 3.4 Risque 4 — Violation de la confidentialité (ARTHUR — futur)

| | |
|---|---|
| **Menace** | Accès des parents aux données de santé d'un enfant |
| **Probabilité** | N/A (ARTHUR V3 2027) |
| **Mesures prévues** | Séparation des profils · Rapports agrégés uniquement pour les parents · AIPD ARTHUR distincte |

---

## 4. Mesures de protection

### 4.1 Mesures techniques

| Mesure | Implémentation | Fichier de preuve |
|---|---|---|
| Chiffrement au repos | Fernet AES-256 | `src/security/encryption_service.py` |
| Contrôle d'accès | MFA obligatoire OWNER/ADMIN | `src/security/mfa_manager.py` |
| Journalisation accès | Audit trail horodaté | `src/security/audit_trail.py` |
| Filtre PII sortants | output_filter.py | `src/security/output_filter.py` |
| Consentement Art. 9 | Registre formel | `src/security/consent_art9.py` |

### 4.2 Mesures organisationnelles

- Données hébergées exclusivement en local (Local-First by design)
- Aucun employé tiers n'a accès aux données
- DPA formelle établie avec sous-traitants API (voir RGPD-09)
- Procédure de notification violation 72h documentée (voir RGPD-10)

---

## 5. Droits des personnes

| Droit | Implémentation |
|---|---|
| Accès Art. 15 | `src/conversation/commands/export_command.py` |
| Rectification Art. 16 | `data/profile/user_profile.json` éditable |
| Effacement Art. 17 | Commande `/forget` · `src/memory/` |
| Portabilité Art. 20 | `src/conversation/commands/portability.py` |
| Opposition Art. 21 | `config/features.json` — désactivation wellbeing_tracking |
| Retrait consentement | `src/security/consent_art9.py` → `revoke_consent()` |

---

## 6. Consultation de la CNIL

### 6.1 Nécessité de consultation préalable

La CNIL doit être consultée si le risque résiduel demeure élevé après mesures (Art. 36 RGPD).

**Conclusion :** Les risques résiduels sont **moyens à faibles** après application des mesures. La consultation préalable de la CNIL n'est **pas obligatoire** à ce stade pour un usage personnel mono-utilisateur.

**Seuil de réexamen :** Consultation requise si ALFRED est commercialisé ou étendu à plus de 50 utilisateurs traitant des données de santé.

---

## 7. Validation et revue

| | |
|---|---|
| **Validée par** | Céline — Responsable du traitement |
| **Date de validation** | 2026-06-18 |
| **Prochaine revue** | 2027-06-18 (annuelle) ou en cas de changement substantiel |
| **Déclencheurs de révision** | Nouvelle catégorie de données · Nouveau sous-traitant · Incident de sécurité · Extension ARTHUR |

---

*Document confidentiel interne — Cognitive Products Lab*  
*Généré conformément aux lignes directrices AIPD de la CNIL et au Règlement (UE) 2016/679*
