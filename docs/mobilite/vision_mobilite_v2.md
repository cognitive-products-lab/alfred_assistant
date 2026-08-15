# ALFRED — Vision Mobilité V2 (client mobile & contexte externe)

> Bloc officiel 07 — Mobilité & Contexte externe. Document de vision : décrit
> une cible produit, pas un état livré. Statut réel de chaque brique précisé
> explicitement ci-dessous (fait / en cours / prévu) pour ne jamais présenter
> un écart connu comme un fait accompli.

## 1. Objectif

Permettre à ALFRED d'être utilisable depuis un appareil mobile léger
(ALFRED_ANDROID, dépôt Kotlin/Compose séparé) en restant connecté au cœur
ALFRED_PC, sans dupliquer la logique conversationnelle, la mémoire ou la base
de connaissances sur l'appareil mobile. Le mobile est un **client**, pas un
second cœur.

## 2. Architecture cible

```
[ALFRED_ANDROID]  --REST/WebSocket-->  [tunnel WireGuard]  -->  [ALFRED_PC / core]
   client léger        JWT + TLS mutuel      (ER605)              LLM + mémoire + knowledge
```

- **Transport** : API REST/WebSocket exposée par ALFRED_PC.
- **Tunnel** : WireGuard, routé via le routeur ER605 déjà en place (segmentation
  VLAN 10/20/30 opérationnelle depuis le 05/07/2026, cf. `docs/architecture/README.md`).
- **Authentification** : JWT (jeton à courte durée de vie, renouvelable), plus
  TLS mutuel (certificat client + serveur) pour l'accès distant hors réseau
  local.
- **Contexte partagé** : `data/context/user_context.json` (ce bloc) sert de
  point d'échange pour l'état déclaré (localisation, activité, appareil actif)
  entre les sessions PC et mobile — schéma défini, pas encore branché au
  pipeline (cf. section 5).

## 3. État réel au 12/08/2026 — écart assumé entre vision et code

| Brique | Cible (vision) | État réel aujourd'hui |
|---|---|---|
| Transport | API REST/WebSocket | `interface/companion_api.py` : API REST minimale (FastAPI), 2 endpoints (`GET /api/status`, `GET /api/notifications`). Pas de WebSocket. |
| Réseau | Tunnel WireGuard, accès distant sécurisé | **Réseau local uniquement**, écoute sur `0.0.0.0:8420` pour être joignable depuis l'émulateur/téléphone sur le même Wi-Fi. Aucun tunnel WireGuard branché à ce jour — hors scope de cette session. |
| Authentification | JWT + TLS mutuel | **Jeton statique** (`COMPANION_API_TOKEN` en `.env`), comparé en temps constant (`hmac.compare_digest`). TLS (simple, pas mutuel) ajouté le 14/08/2026 : certificat auto-signé local (`tools/security/generate_local_tls_cert.py`), ancré côté Android (`network_security_config.xml`), cleartext HTTP désormais refusé — preuve : `tests/dashboard_tests/test_companion_api_tls.py`. JWT et TLS mutuel restent hors scope. |
| Client mobile | App Android complète | PoC "Compagnon" validé de bout en bout le 02/07/2026 (build + connexion API réelle) — Bloc 24, pas le produit complet. HTTPS traité le 14/08 ; notifications (sync locale périodique WorkManager, pas FCM — décision produit assumée local-first) et mode hors-ligne (cache Room) traités le 14/08 également. Reste hors scope : JWT, tests instrumentés device réel (Robolectric non ajouté). Détail : `ALFRED_ANDROID/docs/BLOC24_STATUS_SESSION.md`. |
| Contexte partagé | Synchronisation PC ↔ mobile | `user_context.json` existe avec un exemple réel et cohérent (complété le 12/08/2026) mais n'est lu par aucun module du pipeline à ce jour — vérifié dans `src/`. |

## 3bis. Premier test sur appareil réel — 15/08/2026

Premier essai réel (tablette Galaxy Tab A9+, WiFi domicile) — confirme concrètement
l'écart réseau ci-dessus, plus deux écarts supplémentaires découverts en usage réel :

- **Réseau local uniquement, vraiment** : le WiFi domicile de la tablette
  (`192.168.1.0/24`, distribué par la Bbox Must) n'est pas une interface de
  l'ER605 — aucune des VLAN (LAN/ALFRED_COR/ADMIN/IOT) ne le couvre. Une ACL
  inter-VLAN ne peut donc rien pour ce cas (elle ne joue qu'entre réseaux
  internes de l'ER605) ; une redirection de port WAN→LAN a été tentée mais
  n'aboutit pas non plus sans cibler l'IP WAN de l'ER605 (que l'app ne connaît
  pas) et sans que le certificat TLS local la couvre (SAN limité à
  `192.168.10.100`/`localhost`/`10.0.2.2`). Validation de l'app faite via un
  contournement `adb reverse` (tunnel de développement, pas une solution
  utilisateur). **Un accès WiFi domicile → PC réel nécessite soit un SSID
  dédié raccordé à une interface de l'ER605, soit le tunnel WireGuard déjà
  prévu en feuille de route (section 4, point 2)** — les deux restent à faire.
  Accès 5G/donnée mobile confirmé non fonctionnel comme attendu (testé
  involontairement via le "WiFi sécurisé" Samsung, un VPN intégré).
- **Audio TTS jamais streamé au client distant** (nouvel écart, pas dans le
  tableau ci-dessus car découvert seulement lors de ce test) : PiperTTS joue
  la voix sur la sortie audio locale du PC, jamais envoyée au client Android
  — seuls les évènements de synchronisation (visèmes, début/fin de parole)
  passent par SSE. Résultat : en mode vocal distant, c'est le PC qui parle,
  pas l'appareil mobile. Amélioration demandée par Céline en priorité pour la
  prochaine session (streaming audio vers le client).
- **Bugs pipeline confirmés en conditions réelles, non spécifiques à Android** :
  (1) routage de connaissance incorrect + hallucination du modèle local en
  anglais sur une question profil/météo (fiche `governance.gouvernance_...`
  chargée hors-sujet, réponse générée en anglais incohérent) ; (2) fiabilité
  des appels d'outils du modèle local toujours limitée (garde-fou de secours
  déclenché sur "résume mes tâches"), confirmant le taux d'échec ~35-40% déjà
  documenté le 24/07/2026. Les deux à traiter dans une session dédiée au
  pipeline, indépendante de la mobilité.

Détail complet du déroulé de session : `ALFRED_ANDROID/docs/BLOC24_STATUS_SESSION.md`.

**Lecture honnête de cet écart** : ce n'est pas un retard caché, c'est l'état
attendu d'un PoC réseau local qui n'a pas encore été durci pour un accès
distant réel. La feuille de route ci-dessous (section 4) formalise ce qui
reste à faire, dans l'ordre où cela devient nécessaire.

## 4. Feuille de route (par priorité, pas de date engagée)

1. **Durcir l'API compagnon existante** avant tout accès hors réseau local :
   TLS fait le 14/08/2026 (certificat local auto-signé, cf. tableau ci-dessus) ;
   reste à faire — remplacer le jeton statique par JWT (courte durée + refresh).
2. **Tunnel WireGuard** entre le mobile et le réseau domestique (VLAN dédié,
   cohérent avec la micro-segmentation déjà en place), pour permettre l'usage
   hors du Wi-Fi local sans exposer directement le port 8420 sur Internet.
3. **Brancher `user_context.json`** (ou son successeur) dans le pipeline
   réel : décider à ce moment-là s'il doit être alimenté par le client Android
   (déclaration manuelle) ou par une détection automatique — question ouverte,
   pas tranchée par ce document.
4. **WebSocket** pour les échanges conversationnels temps réel depuis le
   mobile (le REST actuel suffit pour status/notifications, pas pour une
   conversation fluide).
5. **Produit complet côté Android** : HTTPS, notifications push (FCM ou
   équivalent), mode hors-ligne (cache local) — cf. écarts déjà identifiés au
   Bloc 24.

## 5. Relation avec le Bloc 24 (ALFRED_ANDROID)

Le PoC ALFRED_ANDROID (Bloc 24) est la **première brique concrète** de cette
vision : il prouve que la connexion client léger ↔ API locale ALFRED_PC
fonctionne de bout en bout (build + émulateur/téléphone + appel API réel,
02/07/2026). Ce document (Bloc 07) porte la vision réseau/sécurité qui
encadre l'extension de ce PoC vers un produit mobile complet ; le Bloc 24
porte l'implémentation Kotlin/Compose elle-même. Les deux blocs restent
volontairement distincts dans le dashboard (`b07` = contexte/mobilité
transverse, `b24` = compagnon Android) mais avancent de pair.

## 6. Ce que ce document n'est pas

Ni une spécification d'API formelle (OpenAPI/Swagger), ni un engagement de
date. Il sert de référence de cadrage pour prioriser les futurs sprints
mobilité, à mettre à jour à chaque évolution réelle de `companion_api.py` ou
du tunnel réseau.
