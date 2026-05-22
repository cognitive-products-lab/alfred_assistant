# ALFRED — Politique d'Accessibilité

> **Bloc 22.01** — Politique d'accessibilité
> Document de référence : `src/accessibility/accessibility_manager.py`
> Statut : V1 — Document évolutif V1 → V3

---

## 1. Vision

ALFRED est conçu comme un assistant intelligent adaptatif, ayant pour objectif de réduire la charge mentale, favoriser l'autonomie et rendre les interactions numériques plus accessibles, compréhensibles et humaines.

---

## 2. Principes fondamentaux

| Principe | Description |
|---|---|
| **Inclusion by Design** | L'accessibilité est intégrée dès la conception. |
| **Cognitive Load Reduction** | Interfaces claires, informations hiérarchisées, simplification, aide contextuelle. |
| **Adaptive Experience** | ALFRED adapte la voix, le rythme, la complexité, l'affichage et les interactions. |
| **Human-Centered AI** | L'IA doit assister sans surcharger. |
| **Accessibility First** | Les fonctions essentielles doivent rester lisibles, compréhensibles et utilisables. |

---

## 3. Fonctionnalités cibles

### Assistance vocale *(Bloc 22.02)*
- lecture à voix haute d'un texte sélectionné ;
- lecture d'un document ou d'une page web ;
- voix officielle Alfred pour la restitution ;
- vitesse adaptable (ralentissement / accélération) ;
- tonalité adaptable (neutre, doux, motivant, professionnel) ;
- résumé vocal.

### Traduction *(Bloc 22.03)*
- traduction texte FR ↔ EN, puis autres langues ;
- traduction vocale ;
- reformulation simplifiée.

### Accessibilité visuelle *(Bloc 22.06)*
- typographie dyslexie (OpenDyslexic) ;
- contrastes élevés ;
- zoom et redimensionnement ;
- thèmes d'accessibilité ;
- réduction de la fatigue visuelle.

### Assistance cognitive *(Bloc 22.04 / 22.05 / 22.09 / 22.10)*
- résumés intelligents ;
- aide à la compréhension ;
- explication des acronymes et termes techniques ;
- reformulation simplifiée ;
- mode "langage facile à comprendre".

---

## 4. Publics concernés

ALFRED vise à aider notamment :
- personnes neuroatypiques ;
- utilisateurs dyslexiques ;
- utilisateurs fatigables ;
- personnes isolées ;
- personnes âgées ;
- utilisateurs en surcharge cognitive ;
- utilisateurs multitâches ;
- utilisateurs en situation de handicap.

---

## 5. Principes techniques

- local-first lorsque possible ;
- protection des données ;
- consentement utilisateur ;
- personnalisation contrôlée ;
- transparence des interactions IA ;
- possibilité de désactiver les aides.

---

## 6. Référentiels visés

- **WCAG** 2.1 / 2.2 (niveaux A et AA) ;
- **RGPD** ;
- **ISO 27001** ;
- inclusion numérique ;
- Privacy by Design ;
- Ethical AI.

---

## 7. Structure des modules (Bloc 22)

```
src/accessibility/
├── accessibility_manager.py      # 22.01 — Politique & orchestration
├── accessibility_settings.json   # Configuration globale
├── audio/
│   ├── text_reader.py            # 22.02 — Lecture vocale
│   └── voice_output_manager.py   # 22.02 — Gestion sortie vocale
├── translation/
│   └── translator.py             # 22.03 — Traduction multilingue
├── cognitive/
│   ├── summarizer.py             # 22.04 / 22.09 — Résumé & reformulation
│   └── explain_terms.py          # 22.05 / 22.10 — Explication termes
└── ui/
    └── (accessibilité visuelle — V2)
```

**Liens avec modules existants :**
- `src/conversation/output/` (TTS Piper — voix Alfred)
- `src/knowledge/` (base de connaissances pour explications)

---

## 8. Philosophie ALFRED

ALFRED ne doit pas uniquement être performant.
Il doit être **compréhensible, rassurant, adaptatif et accessible**.

---

*Document créé le 22/05/2026 — Source : ALFRED_Accessibility_Policy.pdf*
*À mettre à jour à chaque évolution majeure des fonctionnalités d'accessibilité.*
