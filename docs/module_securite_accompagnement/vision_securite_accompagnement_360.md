# Vision — Sécurité & accompagnement 360° dans la maison
## Cognitive Products Lab — ALFRED

> Version 1.0 — 2026-07-24
> Statut : CONCEPTION — aucun code écrit à ce stade
> Origine : conversation du 24/07/2026, suite à l'échec de l'intégration
> Google Home/Nest (enceintes non supportées par le SDM API — voir
> `docs/…` équivalent côté mémoire projet)

---

## 1. Vue d'ensemble

ALFRED doit pouvoir, à terme, assurer une présence de sécurité dans
l'ensemble du logement de Céline — détecter une situation anormale (chute,
immobilité prolongée), tenter de la confirmer directement avec elle (voix,
dans n'importe quelle pièce équipée), et si besoin alerter des personnes de
confiance. Ce document fixe la vision, les limites volontairement posées, et
les phases de construction — **sans engager de code avant que les
prérequis techniques (compte Tuya, modèle caméra, mécanisme SMS/appel)
soient confirmés.**

Ce n'est pas un chantier de vidéosurveillance classique : l'objectif est un
**compagnon de sécurité passif et respectueux**, pas un système de
surveillance permanent enregistré.

---

## 2. Périmètre matériel

Céline a plusieurs appareils connectés, tous visibles depuis l'app Google
Home mais chacun sur un écosystème/API distinct :

| Appareil | Marque | Statut pour ce chantier |
|---|---|---|
| Bouton d'alerte | Tuya | **Dans le périmètre** |
| Caméra de surveillance (flux RTSP, audio bidirectionnel) | Tuya | **Dans le périmètre** |
| Volets roulants | Somfy | Hors périmètre — écosystème séparé |
| Prise / interrupteur | Legrand | Hors périmètre — écosystème séparé |
| Aspirateur | iRobot Roomba | Hors périmètre — écosystème séparé |
| Aspirateur-laveur | Ecovacs | Hors périmètre — écosystème séparé |
| Radiateur / climatisation | Klarstein | Hors périmètre — écosystème séparé |

**Décision actée** : ne traiter que les appareils Tuya dans ce chantier.
Chaque autre marque nécessiterait sa propre intégration (API, identifiants,
cadrage) — à envisager séparément si un besoin réel se précise.

Un chantier antérieur (Google Home / Device Access) a été abandonné : les
appareils "Google Home" de Céline sont en réalité des enceintes Nest, hors
du périmètre du Smart Device Management API (qui ne couvre que
Thermostat/Camera/Doorbell/Nest Hub Max). Ce code reste dans le projet,
dormant, réutilisable si un appareil Nest compatible est acquis un jour.

---

## 3. Ligne rouge — ce qu'ALFRED ne fera jamais

**Aucun appel automatique et autonome d'ALFRED aux services d'urgence
(15/18/112), quel que soit le nombre de tentatives de confirmation
préalables infructueuses.**

Raison : les dispatchers des services d'urgence n'ont aucun protocole pour
traiter un appel émanant d'un système automatisé se présentant comme
"assistant virtuel autonome" — risque réel de classement sans suite au
moment précis où ça compterait, ce qui serait pire qu'une absence de
système. S'ajoute un risque légal d'appel abusif aux services de secours.

Les systèmes de référence dans ce domaine (Apple Watch détection de chute,
Life Alert, télé-assistance) n'appellent jamais les secours en direct — ils
passent systématiquement par un opérateur humain agréé qui vérifie la
situation avant de déclencher, lui, les secours via son propre protocole.

ALFRED suit le même principe : **toute escalade grave passe par un humain
de confiance**, jamais par un appel direct d'ALFRED aux secours.

---

## 4. Architecture envisagée (par couches)

```
┌─────────────────────────────────────────────────────────────────────┐
│                     COUCHE PRÉSENCE / VOIX                          │
│   ALFRED parle dans n'importe quelle pièce équipée d'une caméra     │
│   (flux audio bidirectionnel RTSP) — repli sur haut-parleur         │
│   téléphone si aucune caméra à portée.                              │
└───────────────────────────┬───────────────────────────────────────────┘
                            │ analyse temps réel (AUCUN enregistrement)
┌───────────────────────────▼───────────────────────────────────────────┐
│                     COUCHE DÉTECTION                                 │
│  • Analyse du flux vidéo (mouvement, posture) — modèle à définir      │
│  • Deux signaux distincts : "chute" (événement ponctuel) et           │
│    "immobilité prolongée" (absence de mouvement sur une durée)        │
└───────────────────────────┬───────────────────────────────────────────┘
                            │ déclenche
┌───────────────────────────▼───────────────────────────────────────────┐
│                     COUCHE CONFIRMATION                               │
│  • Chute détectée → ALFRED contacte Céline, demande confirmation      │
│    de l'état, demande l'accord avant tout transfert d'appel           │
│  • Immobilité prolongée → plusieurs tentatives de contact vocal       │
│    avant de considérer une non-réponse comme significative            │
└───────────────────────────┬───────────────────────────────────────────┘
                            │ si pas de réponse après plusieurs tentatives
┌───────────────────────────▼───────────────────────────────────────────┐
│                     COUCHE ESCALADE                                   │
│  • Contacts de confiance (Sébastien confirmé ; d'autres proches       │
│    ayant les clés du logement, prévus) — ALFRED les prévient          │
│    (message/appel), c'est EUX qui jugent s'il faut appeler les        │
│    secours.                                                           │
│  • Chaque contact doit donner son propre consentement explicite       │
│    avant que ses coordonnées soient enregistrées (formulaire dédié —  │
│    ce sont ses données personnelles, pas celles de Céline).           │
│  • Option : un vrai service de télé-assistance certifié (Présence     │
│    Verte, Filien ADMR, etc.) comme filet supplémentaire — leur         │
│    protocole professionnel gère alors l'appel aux secours si besoin.  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Cadre RGPD / AI Act (vérifié, pas deviné)

**RGPD** — l'arrêt CJUE Ryneš (C-212/13, 10 juillet 2014) précise que
l'exemption "activité purement personnelle/domestique" (art. 2§2.c RGPD) ne
saute que si la caméra capte un espace public ou partagé (rue, voisinage).
Des caméras strictement intérieures chez Céline relèvent donc de cette
exemption — pas d'obligation légale formelle de registre RGPD/AIPD pour son
usage personnel. Décision produit prise malgré tout, au-delà du minimum
légal :
- **Aucun enregistrement vidéo** — analyse en temps réel uniquement.
- **Consentement explicite par pièce** avant toute surveillance active
  dans cette pièce.

**AI Act** — l'exemption "usage personnel non professionnel" (art. 2) ne
s'applique **pas** si le système est classé "haut risque" — un système
d'inférence de données de santé (chute/immobilité) avec escalade de
sécurité touche des catégories sensibles. Pas de blocage pour l'usage
personnel de Céline aujourd'hui, mais si cette fonctionnalité devait un
jour intégrer le produit ALFRED vendu à d'autres personnes (via ALFRED
CPL), la classification "haut risque" redevient une question sérieuse côté
fournisseur, à retraiter à ce moment-là. Voir aussi le travail déjà fait sur
la reconnaissance d'occupant vs AI Act (même logique de prudence).

---

## 6. Phasage proposé

| Phase | Contenu | Statut |
|---|---|---|
| 0 | Connexion Tuya de base (compte développeur, lister bouton d'alerte + caméra) | À démarrer — bloqué sur 3 inconnues techniques (§7) |
| 1 | Accès au flux caméra (RTSP) + audio bidirectionnel, sans enregistrement, consentement par pièce | Pas commencé |
| 2 | Détection chute / immobilité prolongée (modèle d'analyse à choisir) | Pas commencé |
| 3 | Confirmation vocale multi-pièces via les caméras | Pas commencé |
| 4 | Escalade contacts de confiance (formulaire + consentement par contact) | Pas commencé |
| 5 (optionnel) | Intégration télé-assistance certifiée | Pas commencé, à confirmer si Céline souscrit |

**Décision de Céline (24/07/2026)** : démarrer uniquement par la Phase 0
cette session/les prochaines — "on verra toutes les applications possibles,
les limites qu'on pose proprement" une fois la connexion Tuya établie.

---

## 7. Inconnues techniques bloquant le début du code

1. Céline a-t-elle déjà un compte développeur sur la Tuya IoT Platform
   (iot.tuya.com), ou seulement l'application grand public Smart Life /
   Tuya Smart ?
2. Modèle exact de la caméra de surveillance.
3. La carte SIM dédiée à ALFRED (déjà créée, avec une adresse e-mail dédiée
   également) — destinée à être insérée dans un appareil/modem physique,
   ou à être utilisée via un service cloud (type Twilio) pour l'envoi de
   SMS/appels ?

Tant que ces trois points ne sont pas confirmés, aucun code d'intégration
Tuya ne doit être écrit — même logique de prudence que pour les chantiers
Google Agenda et Google Home (ne pas deviner les identifiants/contraintes
d'une API tierce).

---

## 8. Guide pas-à-pas — préparation de la prochaine session (Phase 0)

Contrairement à Google, Tuya Cloud API ne demande pas de flux OAuth avec
écran de consentement navigateur — juste une paire **Access ID / Access
Secret** générée une fois sur la Tuya IoT Platform. Plus simple à mettre en
place.

### A. À vérifier par Céline, avant la session (5 minutes)

1. **Région du compte app** : ouvrir l'app Tuya Smart ou Smart Life →
   **Moi (Me) → Réglages (Settings) → Compte et sécurité → Région**. Noter
   la région affichée (ex. "Europe de l'Ouest" / "Western Europe") — le
   Cloud Project créé à l'étape B devra utiliser le **même centre de
   données**, sinon les appareils n'apparaîtront jamais dans le projet.
2. **Modèle exact de la caméra de surveillance** (référence produit,
   visible dans l'app ou sur l'appareil).
3. ~~Carte SIM dédiée à ALFRED : appareil physique ou service cloud ?~~
   **Confirmé (24/07/2026)** : carte SIM insérée dans une **tablette
   Samsung A9 dédiée**, avec carte mémoire dédiée également, sur laquelle
   l'app ALFRED (compagnon Android, cf. `interface/companion_api.py` — PoC
   minimaliste actuel, 2 endpoints lecture seule) sera installée. L'envoi
   de SMS/appels lors d'une escalade passera donc par le **matériel de
   cette tablette**, pas par un service cloud type Twilio — l'app Android
   devra gagner une capacité d'émission SMS/appel qu'elle n'a pas
   aujourd'hui. Ce point rattache la Phase 4 de ce chantier à l'écart
   ALFRED_ANDROID vs desktop déjà documenté par ailleurs.

### B. Créer le compte développeur + Cloud Project (pendant la session)

1. Aller sur [iot.tuya.com](https://iot.tuya.com/) → se connecter (créer un
   compte développeur si besoin — gratuit).
2. Menu de gauche → **Cloud** → **Create Cloud Project** (Créer un projet
   Cloud).
3. Renseigner :
   - **Project Name** : ex. `ALFRED_TUYA`
   - **Description** : libre
   - **Development Method** : **Smart Home**
   - **Data Center** : celui correspondant à la région notée en A.1
4. Cliquer **Create**.
5. Dans la fenêtre d'autorisation des services API qui suit, sélectionner
   au minimum : **Industry Basic Service**, **Smart Home Basic Service**,
   **Device Status Notification** → **Authorize**.

### C. Lier le compte app (pour que les appareils apparaissent)

1. Dans le projet créé, onglet **Devices** → **Link Tuya App Account** →
   **Add App Account**.
2. Un QR code s'affiche → le scanner avec l'app Tuya Smart / Smart Life
   (généralement via le bouton "+" ou un scanner QR dans l'app).
3. Confirmer sur le téléphone (bouton **Confirm**).
4. Retour sur le site → cliquer **All Devices** → vérifier que le bouton
   d'alerte et la caméra apparaissent bien dans la liste.

### D. Récupérer les identifiants

1. Ouvrir la page **Overview** du projet (cliquer sur son nom).
2. Noter les deux valeurs affichées : **Access ID / Client ID** et
   **Access Secret / Client Secret** — équivalent du `client_id`/
   `client_secret` Google, mais sans navigateur ni consentement à rejouer.

### E. Ce que je ferai ensuite (pas à faire par Céline)

Une fois A–D confirmés, je créerai `src/integrations/tuya_client.py`
(probablement via la librairie `tuya-connector-python`, l'équivalent
officiel Tuya de `google-api-python-client`), stockerai l'Access ID/Secret
chiffrés selon le même principe que Google (`encryption_service.py`), et
listerai le bouton d'alerte + la caméra pour valider la connexion — sans
aller plus loin que la Phase 0 tant que ce n'est pas explicitement demandé.
