> **STATUS : LOCKED v1.0** — base `avatar_medium_no_face.png` créée, bbox
> sourcils/yeux/bouche figées (voir `avatar_medium_no_face.yaml`). Toute
> nouvelle variante de calque doit respecter ces bbox exactement.

# Spec calques visage ALFRED — sourcils / yeux / bouche

Branche : `feature/avatar-medium-bust-regen`
Référence mesurée : `alfred_medium_neutral_o.png` (frame "o" du cycle speaking
-- visage de face, bouche ouverte en "o", déjà alignée sur le groupe
i/o/u/m : bbox personnage x 347-701 cx=524, y 86-1448)

## Principe général

- **Canvas de chaque calque : 1024 x 1536 px** (identique au canvas des avatars de base)
- **PNG RGBA, fond transparent** (alpha = 0 partout sauf sur l'élément du calque)
- Le calque est positionné en **(0,0)** et superposé directement sur l'image de
  base (pas de décalage/échelle au runtime) → l'élément doit être dessiné
  exactement aux coordonnées indiquées ci-dessous dans le canvas 1024x1536.
- **Recommandation clé** : si tous les avatars "bust" de base (idle, listening,
  thinking, speaking...) sont générés avec la **même position/échelle de tête**
  que `alfred_medium_neutral.png` (cf. spec cadrage buste précédente : tête en
  haut ≈ y 66-90px, centre horizontal ≈ x 521), alors **un seul jeu de calques
  sourcils/yeux/bouche** peut être réutilisé sur TOUTES les variantes de
  visage/corps, au lieu de produire un set de calques par état. Ça simplifie
  énormément la génération.

## Calque SOURCILS (eyebrows)

- **Bounding box dans le canvas** : x 415–615, y 172–196 (largeur 200 px,
  hauteur 24 px)
- **Centre approximatif** : x = 515, y = 184
- Contient les DEUX sourcils (gauche + droit) dans une seule image
- Variantes à produire (1 fichier par variante, même bbox) :
  - `eyebrows_neutral.png` — sourcils neutres (référence actuelle)
  - `eyebrows_raised.png` — sourcils levés (surprise/écoute)
  - `eyebrows_furrowed.png` — sourcils froncés (concentration/réflexion)
  - `eyebrows_one_raised.png` — un sourcil levé (scepticisme)

1. eyebrows_neutral.png
sur fond canal alpha : ## Calque SOURCILS (eyebrows) - **Bounding box dans le canvas** : x 415–615, y 172–196 (largeur 200 px, hauteur 24 px) - **Centre approximatif** : x = 515, y = 184 - Contient les DEUX sourcils (gauche + droit) dans une seule image

Generate a single standalone image. Plain solid white background, no
gradient, no shadow, no border, no text, no labels, no watermark.
Subject: a pair of anime-style eyebrows (left eyebrow + right eyebrow),
front-facing, perfectly symmetrical (mirrored), centered in the frame,
filling about 60% of the image width.
Do NOT draw anything else: no eyes, no face, no skin, no hair, no nose.
Only the two eyebrow shapes on the white background.
Style: thin, slightly curved/arched anime eyebrow shape, soft brush-stroke
texture with visible hair strokes, color dark brown (#3A2418).
Expression: neutral, relaxed natural arch, both eyebrows level and
identical in shape (mirrored), resting position — calm/neutral mood.

2. eyebrows_raised.png
sur fond canal alpha : ## Calque SOURCILS (eyebrows) - **Bounding box dans le canvas** : x 415–615, y 172–196 (largeur 200 px, hauteur 24 px) - **Centre approximatif** : x = 515, y = 184 - Contient les DEUX sourcils (gauche + droit) dans une seule image

Generate a single standalone image. Plain solid white background, no
gradient, no shadow, no border, no text, no labels, no watermark.
Subject: a pair of anime-style eyebrows (left eyebrow + right eyebrow),
front-facing, perfectly symmetrical (mirrored), centered in the frame,
filling about 60% of the image width.
Do NOT draw anything else: no eyes, no face, no skin, no hair, no nose.
Only the two eyebrow shapes on the white background.
Style: thin, slightly curved/arched anime eyebrow shape, soft brush-stroke
texture with visible hair strokes, color dark brown (#3A2418).
Expression: both eyebrows raised significantly higher than neutral
position, more strongly arched, surprised/attentive/listening look. Both
eyebrows identical in shape and height (mirrored).

3. eyebrows_furrowed.png
sur fond canal alpha : ## Calque SOURCILS (eyebrows) - **Bounding box dans le canvas** : x 415–615, y 172–196 (largeur 200 px, hauteur 24 px) - **Centre approximatif** : x = 515, y = 184 - Contient les DEUX sourcils (gauche + droit) dans une seule image

Generate a single standalone image. Plain solid white background, no
gradient, no shadow, no border, no text, no labels, no watermark.
Subject: a pair of anime-style eyebrows (left eyebrow + right eyebrow),
front-facing, perfectly symmetrical (mirrored), centered in the frame,
filling about 60% of the image width.
Do NOT draw anything else: no eyes, no face, no skin, no hair, no nose.
Only the two eyebrow shapes on the white background.
Style: thin, slightly curved anime eyebrow shape, soft brush-stroke
texture with visible hair strokes, color dark brown (#3A2418).
Expression: furrowed/concentrated look — both eyebrows angled downward
toward the center of the face, inner ends lowered and pulled closer
together than neutral, outer ends slightly raised, conveying focus or
mild frustration. Both eyebrows identical in shape (mirrored).

4. eyebrows_one_raised.png
sur fond canal alpha : ## Calque SOURCILS (eyebrows) - **Bounding box dans le canvas** : x 415–615, y 172–196 (largeur 200 px, hauteur 24 px) - **Centre approximatif** : x = 515, y = 184 - Contient les DEUX sourcils (gauche + droit) dans une seule image

Generate a single standalone image. Plain solid white background, no
gradient, no shadow, no border, no text, no labels, no watermark. 
Subject: a pair of anime-style eyebrows (left eyebrow + right eyebrow),
front-facing, asymmetrical, centered in the frame, filling about 60% of
the image width.
Do NOT draw anything else: no eyes, no face, no skin, no hair, no nose.
Only the two eyebrow shapes on the white background.
Style: thin, slightly curved anime eyebrow shape, soft brush-stroke
texture with visible hair strokes, color dark brown (#3A2418).
Expression: skeptical/questioning look — the RIGHT eyebrow (viewer's
right, on the right side of the image) is raised higher and more arched
than neutral. The LEFT eyebrow (viewer's left) stays in the neutral
relaxed position, level, normal arch. The two eyebrows must look clearly
different in height/shape from each other.

## Calque YEUX (eyes)

> **STATUS : LOCKED v1.0** — spec complète dans `eyes_spec.yaml`
> (bbox, géométrie, couleurs, écartement, taille par œil, gaze direction).

- **Bounding box dans le canvas** : x 415–615, y 193–222 (largeur 200 px,
  hauteur 29 px) — chevauche légèrement le bas des sourcils
- **Centre approximatif** : x = 515, y = 207
- **Taille d'un œil** : 60 x 26 px
- **Écartement** : centre œil gauche x=465, centre œil droit x=565
  (interocular distance = 100 px)
- Contient les DEUX yeux (gauche + droit), iris vert RGB(79,167,130)
- Variantes à produire :
  - `eyes_open.png` — yeux ouverts, regard neutre (référence actuelle)
  - `eyes_half.png` — mi-clos (fatigue/transition blink)
  - `eyes_closed.png` — fermés (blink)
  - `eyes_side.png` — regard de côté, gaze_direction = right
  - `eyes_happy.png` — yeux souriants (^^), iris_visible = false

### Prompt industriel commun (template)

```text
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.
Background fully transparent.

Draw ONLY a pair of anime-style male eyes.
No eyebrows. No nose. No mouth. No skin. No face. No hair.
No shadows. No glow.

Position the eyes inside:
x = 415-615
y = 193-222
Center: x = 515, y = 207

Left eye center_x = 465, right eye center_x = 565
(interocular distance = 100 px).
Each eye size ≈ 60 px wide x 26 px tall.
Left and right eyes perfectly symmetrical (mirrored).

Outline color: #2A1F1A (thin line weight).
Sclera: plain white, no shading, no texture.
Iris color: RGB(79,167,130), round shape, medium size,
one small highlight in the upper-left of each iris (when visible).
Eyelashes: subtle, low count, thin.

Everything outside the eye shapes must be fully transparent (alpha=0).

<VARIANT-SPECIFIC LINE — see below>
```

### Deltas par variante (à ajouter à la fin du prompt commun)

1. **`eyes_open.png`**
```text
Variant: eyelid_opening = 100%. Eyes fully open, neutral expression,
gaze direction = forward (looking straight at viewer).
```

2. **`eyes_half.png`**
```text
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.
Background fully transparent.

Draw ONLY a pair of anime-style male eyes.
STRICTLY NO eyebrows, no eyebrow lines, no eyebrow shapes anywhere in the
image. No nose. No mouth. No skin. No face outline. No hair.
No shadows. No glow.
Only the eye shapes themselves must have non-zero alpha — everything else
fully transparent (alpha=0).

Position the eyes inside:
x = 415-615
y = 193-222
Center: x = 515, y = 207

Left eye center_x = 465, right eye center_x = 565
(interocular distance = 100 px).
Each eye size ~= 60 px wide x 26 px tall.
Left and right eyes perfectly symmetrical (mirrored).

Outline color: #2A1F1A (thin line weight).
Sclera: plain white, no shading, no texture.
Iris color: RGB(79,167,130), round shape, medium size.

CRITICAL DIFFERENCE FROM "eyes_open": the upper eyelid must droop down and
cover EXACTLY THE TOP HALF of each iris (eyelid_opening = 50%). The visible
eye opening must be noticeably SHORTER/THINNER in height than a fully open
eye -- roughly half the vertical height. Only the lower half of each iris
and the lower sclera are visible. Gaze direction = forward. Relaxed, tired,
half-closed expression. Both eyes identical (mirrored). Do NOT draw fully
open eyes -- the eyelid coverage must be clearly visible and obvious.
```

3. **`eyes_closed.png`**
```text
Variant: eyelid_opening = 0%. Eyes fully closed — draw each eye as a
simple curved closed-eyelid line (#2A1F1A) with subtle short eyelashes,
no iris/sclera visible. Both eyes identical (mirrored).
```

4. **`eyes_side.png`**
```text
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.
Background fully transparent.

Draw ONLY a pair of anime-style male eyes.
STRICTLY NO eyebrows, no eyebrow lines, no eyebrow shapes anywhere in the
image. No nose. No mouth. No skin. No face outline. No hair.
No shadows. No glow.
Only the eye shapes themselves must have non-zero alpha — everything else
fully transparent (alpha=0).

Position the eyes inside:
x = 415-615
y = 193-222
Center: x = 515, y = 207

Left eye center_x = 465, right eye center_x = 565
(interocular distance = 100 px).
Each eye size ~= 60 px wide x 26 px tall.
Eyelid shape: fully open (eyelid_opening = 100%), identical outline shape
to a neutral open eye -- only the iris/pupil position changes.

Outline color: #2A1F1A (thin line weight).
Sclera: plain white, no shading, no texture.
Iris color: RGB(79,167,130), round shape, medium size, one small highlight.

CRITICAL DIFFERENCE FROM "eyes_open": both irises and pupils must be shifted
clearly toward the RIGHT side of the eye shape (viewer's right), leaving
visible white sclera on the LEFT side of each eye. The iris should touch or
nearly touch the right edge of the eye outline. Both eyes must look in the
EXACTLY THE SAME direction (consistent rightward gaze), mirrored eye shapes
but matching gaze direction (not mirrored gaze). Do NOT center the iris --
the offset must be clearly visible and obvious.
```

5. **`eyes_happy.png`**
```text
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.
Background fully transparent.

Draw ONLY a pair of anime-style male "happy eyes".
STRICTLY NO eyebrows, no eyebrow lines, no eyebrow shapes anywhere in the
image. No nose. No mouth. No skin. No face outline. No hair.
No shadows. No glow.
Only the eye shapes themselves must have non-zero alpha — everything else
fully transparent (alpha=0).

Position the eyes inside:
x = 415-615
y = 193-222
Center: x = 515, y = 207

Left eye center_x = 465, right eye center_x = 565
(interocular distance = 100 px).
Each eye shape ~= 60 px wide x 26 px tall.
Left and right eyes perfectly symmetrical (mirrored).

CRITICAL DIFFERENCE FROM "eyes_open": do NOT draw realistic eyes with iris
and sclera at all. Instead draw each eye as a SIMPLE UPWARD-CURVING ARC LINE
("^" caret shape), like a closed happy/smiling eye in anime style. Line
color #2A1F1A, thin line weight, smooth curve, no fill, no iris, no pupil,
no sclera, no eyelashes. Both arcs identical in shape and size (mirrored),
conveying a cheerful/happy expression. The shape must look completely
different from an open eye -- just two simple curved lines.
```



## Calque BOUCHE (mouth)

> **STATUS : LOCKED v1.0** -- spec complete dans `mouth_spec.yaml`
> (bbox, anchor, couleurs, phonemes, expressions). 11 calques au total
> (7 phonemes + 4 expressions), tous ancres sur le meme point
> `anchor = (525, 293)` pour eviter tout saut entre variantes.

- **Bounding box dans le canvas** : x 470-580, y 262-325 (largeur 110 px,
  hauteur 63 px)
- **Anchor (point d'ancrage commun a toutes les variantes)** : x = 525, y = 293
- **Couleurs verrouillees** : contour `#2A1F1A`, interieur bouche `#4A1C1C`,
  langue `#D97B87`, dents `#FFFFFF`
- **mouth_base (reference de largeur)** : 60 x 8 px (bouche fermee neutre)
- Variantes a produire (11 au total) :
  - Phonemes (7, lip-sync Piper/XTTS - A/E/I/O/U/M) :
    - `mouth_closed.png` - opening 0%, levres visibles
    - `mouth_m.png` - opening 0%, levres pincees (bilabiale "m")
    - `mouth_a.png` - ouverture verticale 100%, horizontale 60%, dents+langue visibles
    - `mouth_e.png` - ouverture verticale 60%, horizontale 90%, dents visibles
    - `mouth_i.png` - ouverture verticale 40%, horizontale 100%, forme etiree
    - `mouth_o.png` - ouverture verticale 100%, horizontale 45%, forme ronde
    - `mouth_u.png` - ouverture verticale 70%, horizontale 35%, forme arrondie
  - Expressions (4, separees des phonemes) :
    - `mouth_smile.png` - coins releves, dents non visibles
    - `mouth_big_smile.png` - coins releves, dents visibles
    - `mouth_concerned.png` - coins abaisses, ouverture legere
    - `mouth_surprised.png` - forme ronde, ouverture moyenne

### Prompt industriel commun (template)

```text
Create a PNG RGBA image, canvas exactly 1024x1536 pixels.
Background fully transparent.

Draw ONLY a single anime-style male mouth (lips, and interior/teeth/tongue
only if specified by the variant).
No eyes. No eyebrows. No nose. No skin. No face. No hair. No chin.
No shadows. No glow.

Position the mouth inside:
x = 470-580
y = 262-325
Anchor (center of the drawn mouth): x = 525, y = 293

Reference closed-mouth width ~60px, height ~8px - all variants must stay
centered on this same anchor point so switching between variants never
causes a visual jump.

Outline color: #2A1F1A (thin line weight), anime style.
Mouth interior color (when visible): #4A1C1C.
Tongue color (when visible): #D97B87.
Teeth color (when visible): #FFFFFF.

Everything outside the mouth shape must be fully transparent (alpha=0).

<VARIANT-SPECIFIC LINE - see below>
```

### Deltas par variante (a ajouter a la fin du prompt commun)

1. **`mouth_closed.png`**
```text
Variant: opening = 0%. Lips closed, neutral relaxed expression, no smile,
no frown, no teeth/tongue visible. Simple horizontal closed-mouth line
with subtle upper/lower lip volume, centered on the anchor.
```

2. **`mouth_m.png`**
```text
Variant: opening = 0%, lips_pressed = true. Lips pressed firmly together
(bilabial "m"), flatter/thinner than mouth_closed, no teeth/tongue
visible, centered on the anchor.
```

3. **`mouth_a.png`**
```text
Variant: opening_vertical = 100%, opening_horizontal = 60%,
teeth_visible = true, tongue_visible = true. Mouth wide open in a tall
oval shape (vowel "A" / "ah"), upper row of teeth visible, tongue
partially visible at the bottom, centered on the anchor.
```

4. **`mouth_e.png`**
```text
Variant: opening_vertical = 60%, opening_horizontal = 90%,
teeth_visible = true, tongue_visible = false. Mouth open in a wide
horizontal slit (vowel "E" / "eh"), lips stretched sideways, upper teeth
visible, centered on the anchor.
```

5. **`mouth_i.png`**
```text
Variant: opening_vertical = 40%, opening_horizontal = 100%,
shape = stretched, teeth_visible = true, tongue_visible = false. Mouth
stretched to its widest horizontal extent with a thin vertical opening
(vowel "I" / "ee"), slight hint of teeth, centered on the anchor.
```

6. **`mouth_o.png`**
```text
Variant: opening_vertical = 100%, opening_horizontal = 45%, shape = round,
teeth_visible = true, tongue_visible = false. Mouth open in a rounded,
roughly circular shape (vowel "O" / "oh"), lips pursed into an "O", hint
of upper teeth, centered on the anchor.
```

7. **`mouth_u.png`**
```text
Variant: opening_vertical = 70%, opening_horizontal = 35%,
shape = rounded, teeth_visible = false, tongue_visible = false. Lips
pushed forward and tightly rounded/pursed into a small circle (vowel "U"
/ "oo"), narrower than mouth_o, centered on the anchor.
```

8. **`mouth_smile.png`**
```text
Variant: corners = raised, teeth_visible = false. Closed-mouth smile -
corners of the mouth curve upward, lips remain closed, no teeth visible,
friendly/warm expression, centered on the anchor.
```

9. **`mouth_big_smile.png`**
```text
Variant: corners = raised, teeth_visible = true. Open smile - corners of
the mouth curve upward and the mouth opens slightly, upper row of teeth
visible, cheerful/happy expression, centered on the anchor.
```

10. **`mouth_concerned.png`**
```text
Variant: corners = lowered, opening = slight. Corners of the mouth turn
downward, mouth slightly open, worried/concerned expression, centered on
the anchor.
```

11. **`mouth_surprised.png`**
```text
Variant: shape = round, opening = medium. Mouth forms a medium-sized
round "o"-like opening, surprised/astonished expression, slight hint of
teeth optional, centered on the anchor.
```

## Validation à l'intégration

- Vérifier `bbox` (alpha>128) de chaque calque ⊆ bounding box ci-dessus
  (avec marge ±5px tolérée pour le débordement naturel des traits/cils)
- Vérifier alignement horizontal : centre x de chaque calque ≈ 505-515
  (cohérent entre sourcils/yeux/bouche et avec le visage de base)
- Composer (overlay alpha) chaque calque sur `alfred_medium_neutral.png`
  "visage vierge" (yeux/sourcils/bouche effacés) et comparer visuellement au
  rendu d'origine — l'écart doit être imperceptible pour les variantes
  "neutral"/"closed"/"open" (régression visuelle).
