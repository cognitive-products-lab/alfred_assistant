# CAHIER DES CHARGES — Sprites Avatar Medium V2
# Vue 3/4 droite — Canal alpha réel — Calques séparés

**Projet** : ALFRED — Avatar Medium  
**Version** : V2.0  
**Date** : 2026-06-22  
**Auteur** : Cognitive Products Lab  
**Statut** : RÉFÉRENCE DE GÉNÉRATION — ne pas modifier sans validation  

---

## 1. CONTEXTE ET OBJECTIF

L'avatar ALFRED (personnage masculin anime, cheveux sombres avec frange)
est affiché dans une fenêtre Kivy 1024x1536 px. Le système de rendu
utilise des calques PNG transparents superposés :

```
Calque 1 : avatar_medium_no_face_[sourcils].png   (base : personnage sans yeux ni bouche, avec sourcils)
Calque 2 : eyes_[variante].png                    (yeux seuls, transparent autour)
Calque 3 : mouth_[variante].png                   (bouche seule, transparent autour)
```

Les calques 2 et 3 sont superposés sur le calque 1 via alpha_composite
avec un offset vertical OFFSET_Y=127 pour compenser le décalage entre
les coordonnées de génération et la position réelle du visage.

**Contrainte absolue de perspective** : le personnage est en **vue 3/4 droite**
(il regarde vers SA droite = vers la GAUCHE du viewer). Tous les calques
yeux et bouche DOIVENT respecter cette perspective.

---

## 2. SPÉCIFICATIONS TECHNIQUES GLOBALES

| Paramètre | Valeur |
|-----------|--------|
| Format | PNG RGBA (4 canaux) |
| Dimensions canvas | 1024 x 1536 pixels |
| Fond | Entièrement transparent (alpha=0) sauf les éléments dessinés |
| Style | Anime masculin, trait net, couleurs plates |
| Perspective | Vue 3/4 droite (personnage face à SA droite = gauche viewer) |
| Résolution | 72 dpi (affichage écran uniquement) |

### Couleurs verrouillées (identiques sur tous les calques)

| Élément | Couleur HEX | Usage |
|---------|-------------|-------|
| Contour général | `#2A1F1A` | Contour yeux, sourcils, bouche |
| Intérieur bouche | `#4A1C1C` | Fond de bouche ouverte |
| Langue | `#D97B87` | Langue visible |
| Dents | `#FFFFFF` | Dents visibles |
| Iris (yeux) | `#3D2B1F` ou brun foncé anime | Iris des yeux |
| Pupille | `#1A0F0A` | Pupille au centre de l'iris |
| Blanc de l'oeil | `#F5F0EB` | Sclérotique |
| Reflet | `#FFFFFF` semi-transparent | Point de brillance sur iris |

### Bounding boxes LOCKED v1.0 (coordonnées dans le canvas 1024x1536)

Ces coordonnées sont celles des calques générés AVANT application de
l'OFFSET_Y=127. Les éléments doivent être dessinés dans ces zones.

| Calque | x0 | y0 | x1 | y1 | Largeur | Hauteur | Centre |
|--------|----|----|----|-----|---------|---------|--------|
| Yeux | 415 | 193 | 615 | 222 | 200 px | 29 px | 515 / 207.5 |
| Bouche | 470 | 262 | 580 | 325 | 110 px | 63 px | anchor 525 / 293 |

### Règles de transparence

- **Alpha = 0** partout sauf sur les pixels dessinés
- Pas de fond blanc, pas de fond gris, pas de quadrillage
- Le canal alpha doit être un VRAI canal alpha PNG (pas peint)
- Vérification : ouvrir dans Photoshop/GIMP — le fond doit apparaître
  comme quadrillage transparent, pas comme couleur unie
- Tolérance de transparence : pixels de bordure avec alpha partiel (AA)
  acceptés, mais fond = 0 strict

---

## 3. PERSPECTIVE 3/4 DROITE — RÈGLES DE DESSIN

Le personnage regarde vers **sa droite** (notre gauche). Cela implique :

### Pour les YEUX

```
Côté viewer GAUCHE  = oeil DROIT du personnage (dominant, plus visible)
Côté viewer DROITE  = oeil GAUCHE du personnage (foreshortened, plus petit)

Oeil dominant (viewer gauche)   : taille normale, iris centré ou légèrement visible
Oeil foreshortened (viewer droit) : 10-20% plus petit en largeur, même hauteur
Écart entre les deux yeux       : légèrement asymétrique
Axe horizontal                  : légèrement incliné (~2-3°, côté viewer gauche plus haut)
```

### Pour la BOUCHE

```
La bouche est légèrement décalée vers la gauche du viewer (la joue droite
du personnage est plus visible).
Coin gauche (viewer) = plus avancé, plus visible
Coin droit (viewer)  = légèrement en retrait, perspective 3/4
La largeur totale dessinée dans la bbox reste centrée sur l'anchor x=525
mais les coins ne sont pas symétriques.
```

### Asymétrie attendue (à respecter impérativement)

- Oeil gauche viewer (dominant) : environ 55-60% de la largeur de la bbox
- Oeil droit viewer (foreshortened) : environ 40-45% de la largeur de la bbox
- Bouche : coin gauche viewer ~5px plus bas que coin droit (perspective)

---

## 4. BASES NO_FACE AVEC SOURCILS (4 images à générer)

Ces 4 images sont la **fondation** de tout le système. Elles représentent
le personnage complet (tête, cheveux, épaules, buste) EN VUE 3/4 DROITE,
avec les sourcils intégrés dans l'image (pas en overlay), mais SANS yeux
ni bouche (zones lisses).

### Prompt commun (template base no_face)

```
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.

Anime-style young male character, 3/4 view facing THEIR RIGHT
(viewer's left). Dark brown/black hair with textured fringe/bangs
that falls over the forehead. The fringe covers part of the eyebrow
area but the EYEBROWS MUST BE CLEARLY VISIBLE beneath/through the fringe.

The character wears a dark suit with white shirt and tie (business/formal style).
The bust is visible from head to mid-chest level.

FACE CONSTRAINTS (CRITICAL):
- NO EYES: the eye areas must be blank, smooth skin — no iris, no pupil,
  no eyelid lines, no lashes. Just flat skin tone in the eye region.
- NO MOUTH: the mouth area must be blank, smooth skin — no lips, no line,
  just flat skin.
- NO NOSE TIP detail (subtle nose bridge is acceptable).
- Skin tone: warm light anime tone, approximately RGB(255, 228, 184).

HAIR: dark (near black or very dark brown), anime style with distinct
fringe/bangs covering the forehead. The fringe falls naturally.

BACKGROUND: fully transparent (alpha=0). The character silhouette has
proper alpha transparency — no white or colored background.

CANVAS POSITION: the face center should be approximately at x=515,
y=350-380 in the 1024x1536 canvas. Head occupies roughly y=80 to y=500.
The body (shoulders, suit) continues below.

[EYEBROW VARIANT — see below]
```

---

### 4.1 `avatar_medium_no_face_neutral.png`

**Sourcils : NEUTRES**

```
EYEBROWS (NEUTRAL variant):
Draw the eyebrows in a NEUTRAL/RELAXED position.
- Character's right eyebrow (viewer's LEFT, dominant side):
  Flat, horizontal, slightly arched. Natural resting position.
  Width approximately 45-50px. Color: dark brown #2A1F1A.
  Positioned clearly visible beneath the fringe.
- Character's left eyebrow (viewer's RIGHT, foreshortened):
  Same style but 10-15% shorter due to 3/4 perspective.
  Slightly less visible, natural foreshortening.
Expression conveyed: CALM, NEUTRAL, RESTING. No emotion visible.
```

**Fichier cible** : `base_medium/avatar_medium_no_face_neutral.png`  
**Usage dans le renderer** : base pour états idle, focus, offline, thinking

---

### 4.2 `avatar_medium_no_face_raised.png`

**Sourcils : LEVÉS**

```
EYEBROWS (RAISED variant):
Draw the eyebrows in a RAISED/ELEVATED position.
- Character's right eyebrow (viewer's LEFT):
  Arched upward, significantly higher than neutral position.
  The arch is pronounced, creating a surprised/attentive look.
  Slight wrinkle lines on forehead above the brow (optional, subtle).
- Character's left eyebrow (viewer's RIGHT):
  Same raised position, 10-15% shorter due to 3/4 perspective.
Expression conveyed: SURPRISE, ATTENTIVENESS, CURIOSITY, OPENNESS.
Both brows raised equally (symmetrically lifted despite 3/4 perspective).
```

**Fichier cible** : `base_medium/avatar_medium_no_face_raised.png`  
**Usage dans le renderer** : base pour états listening, challenge

---

### 4.3 `avatar_medium_no_face_furrowed.png`

**Sourcils : FRONCÉS**

```
EYEBROWS (FURROWED variant):
Draw the eyebrows in a FURROWED/CONTRACTED position.
- Character's right eyebrow (viewer's LEFT):
  Pulled downward and inward toward the nose bridge.
  Inner corner angled down steeply. Creates a V-shape toward center.
  Tension visible in the brow line.
- Character's left eyebrow (viewer's RIGHT):
  Same furrowed direction, foreshortened. Inner corner points toward
  the nose bridge (same side as the right brow in 3/4 view).
  
  The two inner corners of both brows converge toward the nose bridge,
  creating the classic anime "concentration/anger" frown shape.
  
Expression conveyed: CONCENTRATION, CONCERN, DETERMINATION, SLIGHT ANGER.
```

**Fichier cible** : `base_medium/avatar_medium_no_face_furrowed.png`  
**Usage dans le renderer** : base pour états error, cybersecurity

---

### 4.4 `avatar_medium_no_face_one_raised.png`

**Sourcils : UN LEVÉ (sourcil dominant)**

```
EYEBROWS (ONE RAISED variant):
Draw the eyebrows with ONLY ONE RAISED.
- Character's right eyebrow (viewer's LEFT = dominant side):
  RAISED — arched upward, skeptical position. This is the dominant
  eyebrow because it's on the more visible side in 3/4 view.
- Character's left eyebrow (viewer's RIGHT = foreshortened side):
  NEUTRAL — flat, resting position, not raised.
  
The contrast between raised right and flat left creates the skeptical/
questioning expression. Because of the 3/4 view, the raised brow
(viewer's left) is clearly visible and dominant.

Expression conveyed: SKEPTICISM, QUESTIONING, IRONY, "REALLY?".
```

**Fichier cible** : `base_medium/avatar_medium_no_face_one_raised.png`  
**Usage dans le renderer** : base pour état complicite, support

---

## 5. CALQUES YEUX (6 variantes à générer)

**Rappel technique** :
- Canvas 1024x1536, fond transparent
- Bbox cible : x=415-615, y=193-222 (200x29px)
- Centre visé : x=515, y=207.5
- Vue 3/4 droite (oeil viewer gauche = dominant)
- AUCUN autre élément que les yeux (pas de sourcils, pas de peau, pas de nez)

### Prompt commun yeux

```
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.
Background fully transparent (alpha=0) everywhere.

Draw ONLY two anime-style male eyes in 3/4 perspective.
The character faces THEIR RIGHT (viewer's left).

PERSPECTIVE RULES (MANDATORY):
- Left eye in image (viewer's left) = character's RIGHT eye = DOMINANT.
  This eye is larger, more frontal, fully detailed.
- Right eye in image (viewer's right) = character's LEFT eye = FORESHORTENED.
  This eye is 10-20% narrower in width, same height, same style.

POSITIONING (MANDATORY):
Place both eyes inside the bounding box: x=415 to x=615, y=193 to y=222.
Total width available: 200px. Total height available: 29px.
Dominant eye (left): approximately x=415 to x=520.
Foreshortened eye (right): approximately x=520 to x=615.
Inter-eye gap: approximately 5-8px.

STYLE:
Anime style, clean line art. Outline color: #2A1F1A (thin, 1-2px).
Iris: dark brown #3D2B1F. Pupil: #1A0F0A. White of eye: #F5F0EB.
Highlight dot: small white #FFFFFF point in upper-left of each iris.
No eyebrows. No eyelashes extending outside the bbox significantly.
No skin. No face. No nose. No hair.

Everything outside the drawn eyes must be alpha=0 (fully transparent).

[VARIANT-SPECIFIC — see below]
```

---

### 5.1 `eyes/01_open.png` → génère `eyes_open.png`

```
VARIANT: OPEN EYES
Both eyes fully open, maximum iris/pupil visible.
- Dominant eye (viewer left): upper eyelid at top of bbox, lower eyelid
  near bottom. Full circle/oval iris visible. Bright highlight dot.
- Foreshortened eye (viewer right): same openness, slightly compressed width.
Expression: ALERT, ATTENTIVE, NEUTRAL OPEN.
```

---

### 5.2 `eyes/02_half.png` → génère `eyes_half.png`

```
VARIANT: HALF-CLOSED EYES (relaxed/calm)
Both eyes half-closed — upper eyelid descends to cover top 35-45% of iris.
The iris is partially hidden behind the drooping upper eyelid.
- Dominant eye (viewer left): eyelid clearly covers upper portion of iris.
- Foreshortened eye (viewer right): same proportion, narrower.
Expression: CALM, RELAXED, RESTING, SLIGHTLY SLEEPY.
IMPORTANT: this is NOT a closed eye. Iris/pupil must be partially visible.
```

---

### 5.3 `eyes/03_closed.png` → génère `eyes_closed.png`

```
VARIANT: CLOSED EYES
Both eyes fully closed — no iris visible.
- Dominant eye (viewer left): a curved horizontal line representing the
  closed eyelid crease. Longer line (~60-70px). May have subtle lower
  lash line below.
- Foreshortened eye (viewer right): shorter curved line (~40-50px),
  same closed style, foreshortened.
Expression: EYES CLOSED — sleeping, blinking, peaceful.
IMPORTANT: shape must be a horizontal line/crease going FLAT or slightly
downward at corners — NOT an upward arch. The upward arch (∩) is for
happy eyes only.
```

---

### 5.4 `eyes/04_side.png` → génère `eyes_side.png`

```
VARIANT: SIDEWAYS GAZE (looking to viewer's right)
Both eyes open but iris/pupil shifted toward the RIGHT side of each eye.
- Dominant eye (viewer left): open eye, iris visible but shifted RIGHT
  (toward the nose side in 3/4 view). White of eye visible on left.
- Foreshortened eye (viewer right): same gaze direction, iris shifted
  right, narrower due to foreshortening.
Expression: GLANCING SIDEWAYS, LOOKING RIGHT, SUSPICIOUS or THOUGHTFUL.
The gaze direction shift should be clearly visible (iris not centered).
```

---

### 5.5 `eyes/05_happy.png` → génère `eyes_happy.png`

```
VARIANT: HAPPY EYES (smiling eyes, upward arc)
Both eyes are curved UPWARD in a ∩ shape (arc opening downward).
This represents eyes narrowed by smiling cheeks.
- Dominant eye (viewer left): pronounced upward arc ∩, wider.
- Foreshortened eye (viewer right): same upward arc ∩, narrower.

CRITICAL GEOMETRY — READ CAREFULLY:
- CORRECT shape: ∩ (arch/dome opening DOWNWARD) — like the top of a circle
- FORBIDDEN shape: ∪ (bowl opening UPWARD) — that is a closed/sad eye
- FORBIDDEN shape: — (flat horizontal line) — that is a closed eye
- The arc must curve UPWARD at its peak, NOT downward

Expression: HAPPY, JOYFUL, SMILING. The eyes should convey warmth.
```

---

### 5.6 `eyes/06_shining.png` → génère `eyes_shining.png`

```
VARIANT: SHINING/SPARKLING EYES
Both eyes fully open with exaggerated anime sparkle effect inside the iris.
- Dominant eye (viewer left): large open eye, iris filled with anime
  sparkle pattern — large highlight, secondary star-shaped reflection,
  gradient depth inside iris.
- Foreshortened eye (viewer right): same sparkling style, narrower.
Expression: WONDER, EXCITEMENT, STARRY-EYED, ADMIRATION.
The sparkle/shining effect inside the iris is the key visual element.
Multiple highlight dots or star shapes inside each iris are expected.
```

---

## 6. CALQUES BOUCHE (11 variantes à générer)

**Rappel technique** :
- Canvas 1024x1536, fond transparent
- Bbox cible : x=470-580, y=262-325 (110x63px)
- Anchor : x=525, y=293
- Vue 3/4 droite (coin gauche viewer plus avancé)
- Couleurs verrouillées : contour `#2A1F1A`, intérieur `#4A1C1C`, langue `#D97B87`, dents `#FFFFFF`

### Prompt commun bouche

```
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.
Background fully transparent (alpha=0) everywhere.

Draw ONLY a single anime-style male mouth in 3/4 perspective.
The character faces THEIR RIGHT (viewer's left).

PERSPECTIVE RULES (MANDATORY):
- The left side of the mouth (viewer's left) is slightly more forward/visible.
- The right side of the mouth (viewer's right) is slightly in perspective/retreat.
- Lips are NOT symmetric — left corner (viewer) is slightly more prominent.
- The overall mouth shape is centered on anchor x=525, y=293 but with
  subtle 3/4 asymmetry.

POSITIONING (MANDATORY):
Draw the mouth inside: x=470 to x=580, y=262 to y=325.
Anchor point (center of mouth): x=525, y=293.
Reference closed-mouth width: ~60px, height ~8px.
All variants must be centered on this same anchor so switching variants
never causes the mouth to jump position.

STYLE:
Anime style, clean line art. Outline: #2A1F1A (thin, 1-2px).
Mouth interior (when visible): #4A1C1C.
Tongue (when visible): #D97B87.
Teeth (when visible): #FFFFFF.
No eyes. No nose. No skin. No face. No hair. Only the mouth shape.
Everything outside the mouth must be fully transparent (alpha=0).

[VARIANT-SPECIFIC — see below]
```

---

### 6.1 `mouths/mouth_closed.png`

```
VARIANT: CLOSED MOUTH — opening 0%
Lips closed, neutral relaxed expression.
A simple horizontal line with subtle upper and lower lip volume.
Upper lip has a subtle Cupid's bow shape (slightly more pronounced on
the viewer's left due to 3/4 perspective).
Lower lip is slightly fuller.
No teeth, no tongue visible.
Width approximately 55-65px, height approximately 8-12px.
Centered on anchor (525, 293).
```

---

### 6.2 `mouths/mouth_m.png`

```
VARIANT: PRESSED LIPS — bilabial "M" sound
Lips pressed firmly together (more tension than mouth_closed).
Thinner and flatter than mouth_closed — the pressing creates a straighter
horizontal line with the upper and lower lip compressed.
Corners of mouth may be very slightly tensed/pulled.
No teeth, no tongue visible.
Width approximately 50-60px, height approximately 5-7px.
Centered on anchor (525, 293).
```

---

### 6.3 `mouths/mouth_a.png`

```
VARIANT: OPEN MOUTH — vowel "A" / "AH"
Maximum vertical opening. Tall oval shape.
opening_vertical = 100%, opening_horizontal = 60%.
Upper lip: curved, Cupid's bow visible at top.
Lower lip: rounded at bottom.
Interior: fully open, dark interior #4A1C1C visible.
Upper row of teeth visible at top (#FFFFFF, 4-5 teeth).
Tongue partially visible at the bottom (#D97B87).
3/4 perspective: left corner (viewer) slightly lower than right corner.
Width approximately 55-65px, height approximately 45-55px.
Centered on anchor (525, 293).
```

---

### 6.4 `mouths/mouth_e.png`

```
VARIANT: WIDE MOUTH — vowel "E" / "EH"
Wide horizontal opening, moderate vertical opening.
opening_vertical = 60%, opening_horizontal = 90%.
Lips stretched sideways, horizontal emphasis.
Upper row of teeth clearly visible (#FFFFFF).
No tongue visible.
Interior #4A1C1C.
3/4 perspective: left side (viewer) slightly more open than right.
Width approximately 80-95px (widest variant), height approximately 25-35px.
Centered on anchor (525, 293).
```

---

### 6.5 `mouths/mouth_i.png`

```
VARIANT: STRETCHED MOUTH — vowel "I" / "EE"
Widest horizontal stretch with thin vertical opening.
opening_vertical = 40%, opening_horizontal = 100%.
Lips stretched to maximum width, thin horizontal slit opening.
Slight hint of upper teeth at top (#FFFFFF).
No tongue visible. Interior very thin #4A1C1C line.
The corners are pulled maximally sideways — a wide, thin smile-like opening.
3/4 perspective: left corner (viewer) slightly more visible.
Width approximately 90-100px (maximum stretch), height approximately 10-20px.
Centered on anchor (525, 293).
IMPORTANT: this is the WIDEST and FLATTEST of all open mouth variants.
Must be clearly wider than mouth_e and much wider than mouth_o/mouth_u.
```

---

### 6.6 `mouths/mouth_o.png`

```
VARIANT: ROUND MOUTH — vowel "O" / "OH"
Rounded, roughly circular opening.
opening_vertical = 100%, opening_horizontal = 45%.
Lips pursed into an "O" shape. The opening is taller than it is wide.
Lips form a rounded oval/circle, pulled forward slightly (pursed).
Hint of upper teeth at top (optional, very subtle) #FFFFFF.
Interior #4A1C1C visible inside the round opening.
3/4 perspective: subtle — the left side (viewer) is marginally more visible.
Width approximately 40-50px, height approximately 45-55px.
Centered on anchor (525, 293).
IMPORTANT: must be clearly ROUNDER and NARROWER than mouth_e.
The height-to-width ratio should be approximately 1.0-1.2 (taller than wide or equal).
```

---

### 6.7 `mouths/mouth_u.png`

```
VARIANT: PURSED MOUTH — vowel "U" / "OO"
Lips pushed forward and tightly pursed into a small, narrow circle.
opening_vertical = 70%, opening_horizontal = 35%.
Narrower than mouth_o. Lips are more projected/forward (pout-like).
No teeth visible. No tongue visible.
Interior #4A1C1C visible through the small round opening.
3/4 perspective: the pursed lips still show subtle asymmetry.
Width approximately 28-38px (narrowest round variant), height approximately 35-45px.
Centered on anchor (525, 293).
IMPORTANT: this is a MOUTH not an eye. Do NOT draw an almond/leaf shape
with a pupil. Draw lips (upper and lower) forming a small round hole.
The opening must look like pursed lips/pout, not like an iris.
Height-to-width ratio approximately 1.2-1.5 (clearly taller than wide).
```

---

### 6.8 `mouths/mouth_smile.png`

```
VARIANT: CLOSED SMILE
Corners of mouth curve upward, lips remain closed (no teeth visible).
A warm, friendly smile with no opening.
Upper and lower lip both present, corners clearly raised.
3/4 perspective: left corner (viewer) raises slightly more than right.
Width approximately 60-75px, height approximately 10-16px.
Centered on anchor (525, 293).
Expression: WARM, FRIENDLY, CONTENT.
```

---

### 6.9 `mouths/mouth_big_smile.png`

```
VARIANT: OPEN SMILE / BIG SMILE
Corners raised, mouth open with teeth visible.
A cheerful, happy smile showing upper row of teeth.
Corners clearly elevated. Lips form a wide U-curve (open at top).
Upper teeth row visible: 4-5 white teeth #FFFFFF.
Interior #4A1C1C at back.
3/4 perspective: left side of smile (viewer) slightly more elevated.
Width approximately 70-85px, height approximately 20-30px.
Centered on anchor (525, 293).
Expression: CHEERFUL, HAPPY, JOYFUL.
```

---

### 6.10 `mouths/mouth_concerned.png`

```
VARIANT: CONCERNED / WORRIED MOUTH
Corners of mouth pulled DOWNWARD (opposite of smile).
Slight downward curve, mouth slightly open.
Lower lip pushed down, upper lip relatively flat.
The corners are clearly lower than the center.
Subtle interior visible #4A1C1C (slight opening, no teeth visible).
3/4 perspective: left corner (viewer) more visible in its downward pull.
Width approximately 50-65px, height approximately 15-25px.
Centered on anchor (525, 293).
Expression: WORRIED, CONCERNED, UNCERTAIN, UNHAPPY.
```

---

### 6.11 `mouths/mouth_surprised.png`

```
VARIANT: SURPRISED MOUTH
Round/oval opening, medium size. "O" of surprise.
Slightly larger than mouth_o but less tightly pursed — more open/slack.
Lips form a rounded oval, corners neutral (not raised, not lowered).
Medium interior visible #4A1C1C.
Optional: very subtle hint of teeth at top #FFFFFF.
3/4 perspective: slight asymmetry, left side (viewer) marginally more open.
Width approximately 45-60px, height approximately 40-50px.
Centered on anchor (525, 293).
Expression: SURPRISED, ASTONISHED. More relaxed/open than mouth_o.
DIFFERENCE from mouth_o: mouth_o is tighter/more pursed. mouth_surprised
is more open/slack, the lips are less tensed.
```

---

## 7. ORDRE DE GÉNÉRATION RECOMMANDÉ

```
Étape 1 — Bases no_face (4 images) :
  Priority 1 : avatar_medium_no_face_neutral.png   (le plus utilisé)
  Priority 2 : avatar_medium_no_face_raised.png
  Priority 3 : avatar_medium_no_face_furrowed.png
  Priority 4 : avatar_medium_no_face_one_raised.png

Étape 2 — Calques yeux (6 images) :
  Priority 1 : 01_open.png, 02_half.png, 03_closed.png  (les plus utilisés)
  Priority 2 : 05_happy.png, 06_shining.png
  Priority 3 : 04_side.png

Étape 3 — Calques bouche (11 images) :
  Priority 1 : mouth_closed.png, mouth_a.png, mouth_m.png  (lip-sync core)
  Priority 2 : mouth_e.png, mouth_i.png, mouth_o.png, mouth_u.png
  Priority 3 : mouth_smile.png, mouth_big_smile.png, mouth_concerned.png, mouth_surprised.png
```

---

## 8. VALIDATION DE CHAQUE IMAGE GÉNÉRÉE

Avant d'accepter une image, vérifier :

**Canal alpha :**
- [ ] Le fond est transparent (quadrillage dans Photoshop/GIMP)
- [ ] Pas de rectangle blanc ou gris en fond

**Positionnement :**
- [ ] L'élément est dans la bbox cible (voir section 2)
- [ ] L'anchor bouche est respecté (x=525, y=293 ± 5px)
- [ ] Le centre yeux est respecté (x=515, y=207.5 ± 5px)

**Perspective :**
- [ ] Vue 3/4 droite respectée (oeil/côté gauche viewer = dominant)
- [ ] Asymétrie visible et naturelle (pas un dessin symétrique de face)

**Style :**
- [ ] Style anime cohérent avec les autres calques
- [ ] Couleurs dans les valeurs verrouillées (section 2)
- [ ] Fond 100% transparent (pas de pixels parasites)

**Cohérence inter-variantes :**
- [ ] La taille de base est cohérente avec les autres variantes du même calque
- [ ] L'anchor/centre est au même endroit sur toutes les variantes
  (pour éviter le "saut" lors du changement de variante)

---

## 9. PIPELINE DE TRAITEMENT POST-GÉNÉRATION

Une fois les images générées et validées :

```
1. Ranger les yeux dans     : assets/avatars/avatar_medium/base_medium/eyes/
2. Ranger les bouches dans  : assets/avatars/avatar_medium/base_medium/mouths/
3. Ranger les no_face dans  : assets/avatars/avatar_medium/base_medium/

4. Lancer process_eyes.py   → génère eyes_open.png, eyes_half.png, etc.
5. Lancer process_mouths.py → génère mouth_a.png, mouth_closed.png, etc.

6. Mettre à jour compose_avatar.py :
   - Ajouter le paramètre "eyebrows" pour choisir la base no_face
   - EYEBROWS_ENABLED = True (les sourcils sont dans la base, plus de masquage)

7. Lancer build_speaking_frames.py pour générer les 14 sprites renderer

8. Tester visuellement avec alfred_with_ui.py
```

---

## 10. MAPPING ÉTATS → BASES + CALQUES

| État renderer | Base no_face | Yeux | Bouche |
|---------------|-------------|------|--------|
| idle | neutral | half | closed |
| listening | raised | open | closed |
| thinking | furrowed | half | closed |
| speaking (base) | neutral | open | closed |
| support | one_raised | happy | smile |
| focus | neutral | half | closed |
| challenge | raised | open | big_smile |
| complicite | one_raised | happy | big_smile |
| error | furrowed | open | concerned |
| offline | neutral | closed | closed |
| **speaking_a** | neutral | open | a |
| **speaking_e** | neutral | open | e |
| **speaking_i** | neutral | open | i |
| **speaking_o** | neutral | open | o |
| **speaking_u** | neutral | open | u |
| **speaking_m** | neutral | half | m |

---

*Fin du cahier des charges — Version 2.0 — 2026-06-22*
*Référence : LAYERS_SPEC.md (V1.0) pour les specs de génération originales*
