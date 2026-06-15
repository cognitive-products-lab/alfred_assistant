path = r"D:\PROJET_ALFRED\ALFRED_PC\assets\avatars\avatar_medium\base_medium\LAYERS_SPEC.md"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

start = 193
end = 342

new_section = '''## Calque BOUCHE (mouth)

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

'''

lines[start:end] = [new_section]

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("done")
