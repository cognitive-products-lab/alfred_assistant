"""
Enrichissement Knowledge Base ALFRED - Batch 8 : iot (15 restants) + reasoning (10)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")

def save(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK  {path}")

def ku_iot(stem, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.professional.iot.{stem}",
      "title": title, "domain": "professional", "subdomain": "iot",
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": "technique, pragmatique, sensible à la confidentialité et à la sécurité",
        "structure": ["identifier le composant ou problème IoT", "expliquer le mécanisme", "pointer les risques", "proposer la solution"],
        "avoid": ["ignorer la sécurité", "négliger la contrainte de ressources", "trop générique"]
      },
      "tags": tags + ["IoT", "système ambiant"],
      "related_knowledge_units": ["knowledges.professional.engineering.systeme_design.local_first_architecture", "knowledges.cpl.ethics_governance.ethical_ai_framework"]
    }

def ku_reas(stem, title, summary, core_def, knowledge, examples, tags):
    return {
      "schema_version": "1.2", "type": "knowledge_unit",
      "id": f"knowledges.professional.engineering.reasoning.{stem}",
      "title": title, "domain": "professional", "subdomain": "engineering_reasoning",
      "status": "validated", "summary": summary, "core_definition": core_def,
      "knowledge": knowledge, "example_answers": examples,
      "response_guidance": {
        "tone": "rigoureux, ancré dans les mécanismes cognitifs et techniques du raisonnement LLM",
        "structure": ["identifier le type de raisonnement ou biais", "expliquer le mécanisme", "proposer une technique d'amélioration"],
        "avoid": ["confondre raisonnement humain et LLM", "ignorer les limites des LLMs", "trop abstrait"]
      },
      "tags": tags + ["raisonnement", "LLM", "inférence"],
      "related_knowledge_units": ["knowledges.professional.engineering.ai.reasoning_engine", "knowledges.human.cognition.critical_thinking"]
    }

# =============================================================================
# professional / iot (15 fichiers restants)
# =============================================================================

save("professional/iot/edge_ai_processing.json", ku_iot(
  "edge_ai_processing",
  "Traitement IA en edge (Edge AI)",
  "L'edge AI déplace l'inférence IA du cloud vers le dispositif local — réduisant la latence, préservant la confidentialité et réduisant les coûts de bande passante au prix d'une puissance de calcul plus limitée.",
  "L'Edge AI est l'exécution de modèles d'intelligence artificielle directement sur des dispositifs edge (PC, Raspberry Pi, smartphone, microcontrôleur) plutôt que dans le cloud, permettant l'inférence locale avec des avantages en termes de latence, confidentialité et résilience.",
  {
    "edge_ai_advantages": [
      "Latence : inférence en ms plutôt qu'en centaines de ms (pas de round-trip réseau)",
      "Confidentialité : les données ne quittent jamais le device",
      "Résilience : fonctionne sans connexion internet",
      "Coût : pas de coûts de bande passante ni d'API à la requête",
      "Compliance : données traitées localement — simplifie la conformité RGPD"
    ],
    "edge_ai_constraints": [
      "Puissance de calcul limitée — modèles plus petits ou quantisés",
      "Mémoire réduite — pas de grands modèles sans quantisation",
      "Gestion thermique — inférence intensive génère de la chaleur",
      "Mise à jour des modèles plus complexe que le cloud"
    ],
    "optimization_techniques": [
      {"technique": "Quantisation", "description": "Réduire la précision des poids (32-bit → 8-bit → 4-bit) — réduit la taille et accélère l'inférence", "trade_off": "Légère perte de qualité"},
      {"technique": "Pruning", "description": "Supprimer les poids les moins importants du réseau", "trade_off": "Nécessite un réentraînement"},
      {"technique": "Knowledge distillation", "description": "Entraîner un petit modèle (student) à imiter un grand modèle (teacher)", "trade_off": "Qualité réduite mais inférence beaucoup plus rapide"},
      {"technique": "ONNX Runtime", "description": "Format d'optimisation cross-platform pour l'inférence", "use": "Convertir et optimiser des modèles PyTorch/TensorFlow pour l'inférence edge"}
    ],
    "alfred_edge_ai": "ALFRED utilise Ollama en local pour les LLMs et llava:7b pour la vision — edge AI sur PC Windows. Les modèles 7B quantisés (Q4_K_M) offrent un bon compromis qualité/vitesse sur du matériel grand public."
  },
  [
    {"prompt": "Pourquoi utiliser un modèle local plutôt que l'API GPT-4 ?", "answer": "Trois raisons principales : confidentialité (les données ne sortent pas de ton PC), résilience (fonctionne sans internet), coût (pas de facturation par token). La contrepartie : qualité légèrement inférieure et inférence plus lente. Pour ALFRED, le choix est pragmatique : données personnelles sensibles → local first, avec fallback API optionnel si la qualité est insuffisante."},
    {"prompt": "Quels modèles peuvent tourner sur un PC standard pour l'IA locale ?", "answer": "Avec 16Go de RAM : Mistral 7B, Llama 3 8B, Gemma 2 9B — confortables en Q4/Q5. Avec 32Go : Mixtral 8x7B, Llama 3 70B en Q4. Pour la vision : llava 7B et 13B. Piper pour la TTS. Whisper pour la STT. La stack locale complète (STT + LLM + TTS) fonctionne très bien sur un bon PC, et le Minisforum MS-S1 Max (64Go) permettra les modèles 70B."}
  ],
  ["edge AI", "local", "quantisation", "Ollama", "inférence"]
))

save("professional/iot/home_automation_rules.json", ku_iot(
  "home_automation_rules",
  "Règles d'automatisation domotique",
  "Les règles d'automatisation domotique définissent les réponses automatiques aux événements capteurs — si-alors-sinon avec conditions temporelles, de contexte et de priorité. La bonne architecture évite les conflits de règles et les boucles.",
  "Les règles d'automatisation domotique sont des logiques conditionnelles (SI événement ET conditions ALORS action) qui permettent à un système de maison intelligente de répondre automatiquement aux changements d'état des capteurs et dispositifs, selon des critères de temps, de contexte et de priorité.",
  {
    "rule_structure": {
      "trigger": "L'événement qui déclenche l'évaluation (capteur, heure, état d'un autre dispositif)",
      "condition": "Critère supplémentaire pour que l'action soit exécutée (heure, mode, état utilisateur)",
      "action": "Ce qui se passe (allumer une lumière, envoyer une notification, activer un mode)"
    },
    "rule_types": [
      {"type": "Temporelle", "example": "À 22h30 → réduire luminosité à 20%"},
      {"type": "Événementielle", "example": "Mouvement détecté dans l'entrée → allumer lumière entrée"},
      {"type": "Conditionnelle", "example": "Si mouvement ET heure > 23h ET mode nuit actif → notification"},
      {"type": "Contextuelle", "example": "Si ALFRED en conversation → réduire volume TV"}
    ],
    "common_pitfalls": [
      "Conflits de règles : deux règles s'annulent mutuellement en boucle",
      "Règles trop sensibles : déclenchement intempestif (faux positifs capteur mouvement)",
      "Absence de priorité : règles de même niveau sans ordre d'exécution défini",
      "Règles temporelles sans exception : boulversées par des cas edge (vacances, invités)"
    ],
    "alfred_integration": "ALFRED peut être un déclencheur ou une condition dans les règles domotiques : 'Si ALFRED détecte que l'utilisateur travaille intensément → ne pas interrompre avec les notifications non critiques'."
  },
  [
    {"prompt": "Comment structurer les règles domotiques pour éviter les conflits ?", "answer": "Trois principes : hiérarchie (règles de sécurité > confort > énergie), mutex (deux règles sur le même dispositif avec une condition exclusive), et mode maître (un état global qui conditionne toutes les règles — 'mode absence' désactive les règles de confort). Et tester systématiquement les interactions entre règles avant activation."},
    {"prompt": "Comment intégrer ALFRED dans ma domotique ?", "answer": "ALFRED peut écouter les événements domotiques (via MQTT, Home Assistant API) et prendre des décisions contextuelles. Exemple : ALFRED détecte que tu travailles → envoie un événement à Home Assistant → baisse la musique, active 'Ne pas déranger'. Ou inversement : ALFRED reçoit des alertes domotiques et les synthétise pour toi. L'API webhook est le point d'intégration le plus simple."}
  ],
  ["domotique", "règles", "SI-ALORS", "automatisation", "Home Assistant"]
))

save("professional/iot/iot_security_fundamentals.json", ku_iot(
  "iot_security_fundamentals",
  "Sécurité IoT — fondamentaux",
  "Les dispositifs IoT sont parmi les vecteurs d'attaque les plus exploités : firmware non mis à jour, credentials par défaut, communications non chiffrées. La sécurité IoT doit être intégrée dès la conception, pas après.",
  "La sécurité IoT est l'ensemble des pratiques techniques et organisationnelles permettant de protéger les dispositifs connectés, leurs communications et les données qu'ils traitent contre les accès non autorisés, les manipulations et les compromissions.",
  {
    "iot_attack_vectors": [
      "Credentials par défaut non changés (admin/admin) — première cible des botnets",
      "Firmware non mis à jour — vulnérabilités connues non patchées",
      "Communications non chiffrées — interception de trafic en clair",
      "API ouvertes sans authentification",
      "Composants tiers non maintenus avec des dépendances vulnérables"
    ],
    "security_baseline": [
      "Changer les identifiants par défaut immédiatement",
      "Activer les mises à jour automatiques du firmware",
      "Isoler les dispositifs IoT sur un VLAN dédié",
      "Chiffrer toutes les communications (TLS 1.3 minimum)",
      "Désactiver les services inutilisés (UPnP, Telnet)",
      "Monitorer le trafic réseau des dispositifs IoT pour détecter les anomalies"
    ],
    "network_segmentation": "VLAN IoT séparé du réseau principal : si un dispositif est compromis, l'attaquant ne peut pas latéraliser vers le réseau personnel ou professionnel. Règle de base : les dispositifs IoT n'ont jamais besoin d'accéder aux PC ou NAS du réseau principal."
  },
  [
    {"prompt": "Comment sécuriser mes dispositifs IoT à la maison ?", "answer": "Quatre actions prioritaires : (1) VLAN IoT séparé sur le routeur (les IoT ne voient pas le réseau PC), (2) mots de passe uniques sur chaque dispositif, (3) mises à jour firmware activées automatiquement, (4) désactiver l'accès depuis internet si pas nécessaire (UPnP désactivé). Ça couvre 80% des vecteurs d'attaque courants."},
    {"prompt": "Est-ce que les dispositifs IoT autour d'ALFRED posent un risque de sécurité ?", "answer": "Potentiellement oui — particulièrement la caméra et le micro. Pour ALFRED : caméra activée uniquement sur demande, traitement local sans cloud, micro en mode push-to-talk plutôt que toujours-actif. Et le réseau : PC ALFRED sur un VLAN isolé est la configuration recommandée (cf. setup réseau ER605+SG108E). Un dispositif IoT compromis sur le même réseau pourrait écouter les échanges avec ALFRED."}
  ],
  ["sécurité IoT", "VLAN", "firmware", "credentials", "chiffrement"]
))

save("professional/iot/mqtt_protocol.json", ku_iot(
  "mqtt_protocol",
  "Protocole MQTT",
  "MQTT est le protocole de messagerie légère de référence pour l'IoT — publication/abonnement sur des topics, faible overhead, adapté aux connexions instables et aux dispositifs contraints.",
  "MQTT (Message Queuing Telemetry Transport) est un protocole de messagerie publish-subscribe léger conçu pour les communications M2M et IoT. Il utilise un broker central pour router les messages entre publishers et subscribers, avec un overhead minimal et une gestion adaptée aux connexions instables.",
  {
    "mqtt_concepts": [
      {"concept": "Broker", "description": "Serveur central qui reçoit, filtre et route les messages (Mosquitto, EMQX, HiveMQ)"},
      {"concept": "Topic", "description": "Chaîne hiérarchique qui classe les messages (ex: maison/salon/temperature)", "wildcards": "+ (un niveau), # (tous les niveaux)"},
      {"concept": "Publisher", "description": "Dispositif ou service qui publie des messages sur un topic"},
      {"concept": "Subscriber", "description": "Dispositif ou service qui s'abonne à un topic pour recevoir les messages"},
      {"concept": "QoS", "description": "Niveau de qualité de service — 0 (at most once), 1 (at least once), 2 (exactly once)"},
      {"concept": "Retain", "description": "Le broker conserve le dernier message d'un topic — utile pour l'état courant des capteurs"}
    ],
    "use_cases": [
      "Communication entre capteurs IoT et hub domotique (Home Assistant via MQTT)",
      "Télémétrie temps réel (température, humidité, état des dispositifs)",
      "Commandes de contrôle (allumer/éteindre, changer mode)",
      "Intégration ALFRED ↔ domotique (événements bidirectionnels)"
    ],
    "alfred_mqtt_integration": {
      "subscribe": "ALFRED peut s'abonner à des topics domotiques pour recevoir les événements (alerte, état capteur)",
      "publish": "ALFRED peut publier des commandes (mode_travail: actif) que la domotique écoute",
      "broker": "Mosquitto local sur le même réseau — pas de dépendance cloud"
    }
  },
  [
    {"prompt": "Comment intégrer ALFRED avec Home Assistant via MQTT ?", "answer": "Setup : Mosquitto broker local, ALFRED s'abonne aux topics HA (hass/state/#) et publie sur les topics de commande. Exemple : ALFRED publie 'hass/alfred/mode: focus' → HA l'écoute et ajuste la domotique (lumière, son). En Python : paho-mqtt est la bibliothèque de référence. Configuration MQTT dans HA : builtin depuis Home Assistant 2022."},
    {"prompt": "Quelle différence entre MQTT et REST pour l'IoT ?", "answer": "MQTT est event-driven et persistant : les dispositifs restent connectés et reçoivent les messages dès qu'ils arrivent. REST est request-response : le client doit poller pour savoir si l'état a changé. Pour l'IoT temps réel, MQTT est supérieur. Pour les intégrations API ponctuelles, REST est plus simple à implémenter. Les deux coexistent souvent : MQTT pour les événements temps réel, REST pour les configurations et les requêtes ponctuelles."}
  ],
  ["MQTT", "broker", "publish-subscribe", "Home Assistant", "Mosquitto"]
))

save("professional/iot/sensor_data_quality.json", ku_iot(
  "sensor_data_quality",
  "Qualité des données capteurs",
  "Les données capteurs sont intrinsèquement bruitées, incomplètes et parfois erronées. La qualité des données IoT s'évalue et s'améliore par le filtrage, la détection d'anomalies, la calibration et la fusion multi-capteurs.",
  "La qualité des données capteurs est l'évaluation et l'amélioration de la précision, de la complétude, de la cohérence et de la fraîcheur des données collectées par les dispositifs IoT, pour permettre une inférence fiable par les systèmes IA en aval.",
  {
    "quality_dimensions": [
      {"dimension": "Précision", "description": "La valeur mesurée correspond à la valeur réelle"},
      {"dimension": "Complétude", "description": "Pas de valeurs manquantes sur la période d'observation"},
      {"dimension": "Cohérence", "description": "Les valeurs sont dans les plages attendues et cohérentes entre capteurs"},
      {"dimension": "Fraîcheur", "description": "La mesure est suffisamment récente pour être utile"},
      {"dimension": "Résolution", "description": "La granularité temporelle correspond au besoin (1s, 1min, 1h)"}
    ],
    "noise_handling": [
      "Filtre moyenne mobile (rolling average) — lisse les pics sans éliminer les tendances",
      "Filtre de Kalman — optimal pour les signaux dynamiques bruités",
      "Seuillage par percentile — éliminer les valeurs en dehors du P2-P98",
      "Interpolation — remplir les valeurs manquantes par régression ou interpolation temporelle"
    ],
    "anomaly_detection": [
      "Seuils statiques : valeur hors plage → anomalie",
      "Seuils dynamiques : 3σ au-dessus de la moyenne mobile → anomalie",
      "Pattern matching : comportement attendu vs observé",
      "Cross-capteur : un capteur dévie alors que les autres sont stables → problème matériel"
    ]
  },
  [
    {"prompt": "Mon capteur de température donne parfois des valeurs aberrantes — comment filtrer ?", "answer": "Trois niveaux : (1) Filtre seuil absolu (temp hors [-10°C, 50°C] = invalide → ignorer), (2) Filtre zscore (3 déviations standard au-dessus de la moyenne des 10 dernières valeurs → spike → remplacer par la moyenne), (3) Filtre Kalman si tu veux le maximum de finesse. En pratique, le filtre seuil + zscore couvre 95% des cas."},
    {"prompt": "Comment savoir si un capteur IoT a besoin d'être recalibré ?", "answer": "Comparaison multi-capteurs (si tu as plusieurs capteurs du même type) : déviation systématique d'un capteur = dérive → recalibration. Sinon : comparaison avec une mesure de référence (thermomètre calibré, station météo externe). La plupart des capteurs grand public dérivent après 1-2 ans d'utilisation intensive."}
  ],
  ["qualité données", "bruit", "anomalie", "filtrage", "calibration"]
))

save("professional/iot/local_processing_architecture.json", ku_iot(
  "local_processing_architecture",
  "Architecture de traitement local (local-first IoT)",
  "L'architecture local-first pour l'IoT traite les données sur le réseau local avant (ou sans) envoi vers le cloud. Elle réduit la latence, améliore la confidentialité et crée des systèmes résilients aux pannes réseau.",
  "L'architecture local-first IoT est un paradigme de conception dans lequel le traitement des données et les décisions IA sont effectués sur des équipements locaux (PC, NAS, Raspberry Pi, hub domotique), en limitant ou éliminant la dépendance au cloud pour les fonctions core.",
  {
    "local_components": [
      {"component": "Broker local (MQTT)", "role": "Routage des messages entre dispositifs — Mosquitto sur le réseau local"},
      {"component": "Base de données locale", "role": "Stockage des timeseries et des états — InfluxDB, TimescaleDB, SQLite"},
      {"component": "Moteur de règles local", "role": "Exécution des automatisations — Node-RED, Home Assistant"},
      {"component": "Modèles IA locaux", "role": "Inférence sans cloud — Ollama, llava, Piper, Whisper"},
      {"component": "Dashboard local", "role": "Visualisation sans dépendance externe — Grafana, Home Assistant UI"}
    ],
    "cloud_optional_fallback": "Dans un design local-first, le cloud est optionnel (backup, accès distant, modèles de qualité supérieure) et non critique. Si le cloud est indisponible, toutes les fonctions core continuent.",
    "alfred_local_first": "ALFRED est conçu local-first : LLM via Ollama, TTS via Piper, STT via Whisper, mémoire via SQLite, données sur le PC Windows. L'API OpenAI/Anthropic est un fallback optionnel pour la qualité, pas une dépendance core."
  },
  [
    {"prompt": "Comment construire un hub domotique 100% local ?", "answer": "Stack recommandée : Home Assistant (hub central) + Mosquitto (broker MQTT) + Zigbee2MQTT ou Z-Wave pour les capteurs sans fil + InfluxDB/Grafana pour les historiques. Le tout sur un mini-PC ou Raspberry Pi 5. Home Assistant gère aussi les règles d'automatisation et les interfaces. Estimation : quelques heures de setup, puis très stable sur le long terme."},
    {"prompt": "Pourquoi local-first plutôt que de tout mettre dans le cloud ?", "answer": "Quatre raisons concrètes : (1) latence — une action domotique locale répond en <100ms vs 200-500ms via le cloud, (2) disponibilité — fonctionne si internet tombe, (3) confidentialité — les données de mouvement et de présence ne sortent pas de ta maison, (4) coût — pas de abonnement cloud à long terme. Limite : mise à jour et accès distant plus complexes."}
  ],
  ["local-first", "architecture", "Home Assistant", "Mosquitto", "offline"]
))

save("professional/iot/voice_wake_word.json", ku_iot(
  "voice_wake_word",
  "Détection du mot de réveil (wake word)",
  "Le wake word est le déclencheur vocal du mode écoute — 'Hey ALFRED', 'OK Google', 'Alexa'. Sa détection locale, en temps réel et hors ligne est une fonctionnalité sensible : faux positifs = intrusion non souhaitée dans la vie privée.",
  "La détection de wake word est la reconnaissance en temps réel d'un mot ou d'une phrase déclencheur qui active le mode d'écoute d'un assistant vocal. Elle doit fonctionner en local, avec une faible empreinte CPU, une haute précision et un taux de faux positifs minimal.",
  {
    "wake_word_solutions": [
      {"solution": "Porcupine (Picovoice)", "type": "Local, propriétaire freemium", "pros": ["Très précis", "Faible CPU", "Multi-plateforme"], "cons": ["Licence commerciale payante", "Mots de réveil limités en tier gratuit"]},
      {"solution": "OpenWakeWord", "type": "Local, open source", "pros": ["100% gratuit", "Personnalisable", "Python-friendly"], "cons": ["Moins précis que Porcupine", "Plus de CPU"]},
      {"solution": "Snowboy", "type": "Local, open source (déprécié)", "pros": ["Historiquement populaire"], "cons": ["N'est plus maintenu — ne pas utiliser pour nouveau projet"]},
      {"solution": "Whisper VAD", "type": "Transcription avec détection d'activité vocale", "pros": ["Déjà intégré si Whisper utilisé pour STT"], "cons": ["Plus lent pour le réveil que les solutions dédiées"]}
    ],
    "alfred_wake_word": {
      "current": "Mode push-to-talk (bouton ou raccourci) — privé et sans faux positifs",
      "planned": "OpenWakeWord pour 'Hey Alfred' en mode mains-libres optionnel",
      "recommendation": "Le push-to-talk est recommandé par défaut pour la confidentialité — le wake word toujours-actif = microphone toujours-actif"
    }
  },
  [
    {"prompt": "Comment ajouter 'Hey Alfred' à ALFRED ?", "answer": "Deux options : OpenWakeWord (open source, Python, fonctionne en local) ou Porcupine (plus précis, freemium). OpenWakeWord se configure avec un modèle pré-entraîné ou un modèle custom entraîné avec tes propres exemples. À intégrer dans main.py : boucle d'écoute continue en thread daemon qui déclenche le pipeline STT quand le wake word est détecté."},
    {"prompt": "Le mode wake word est-il sûr pour la vie privée ?", "answer": "Moins que le push-to-talk. Le wake word require un microphone actif en permanence — avec traitement local si bien implémenté. Les risques : faux positifs (activation non souhaitée), accès au micro par d'autres applications. Pour ALFRED : le mode ecoute (push-to-talk) est le défaut recommandé. Le mode wake word est opt-in pour les usages mains-libres."}
  ],
  ["wake word", "microphone", "activation vocale", "Porcupine", "OpenWakeWord"]
))

save("professional/iot/real_time_event_processing.json", ku_iot(
  "real_time_event_processing",
  "Traitement d'événements en temps réel",
  "Le traitement d'événements en temps réel permet de réagir aux données IoT avec une latence minimale — quelques millisecondes — en appliquant des règles, des agrégations et des alertes sans stocker d'abord dans une base de données.",
  "Le traitement d'événements en temps réel (Real-time Event Processing ou Stream Processing) est l'analyse et le traitement des données au fur et à mesure qu'elles sont générées, permettant des réponses immédiates sans attendre leur stockage et leur traitement différé.",
  {
    "stream_processing_concepts": [
      {"concept": "Event stream", "description": "Flux continu d'événements ordonnés dans le temps (ex: lectures capteur toutes les secondes)"},
      {"concept": "Windowing", "description": "Regrouper les événements en fenêtres temporelles pour calculer des agrégats (moyenne 5 min, max heure)"},
      {"concept": "Filtering", "description": "Sélectionner uniquement les événements qui remplissent certains critères"},
      {"concept": "Joining", "description": "Combiner deux streams en temps réel (ex: température + humidité)"},
      {"concept": "CEP (Complex Event Processing)", "description": "Détecter des patterns complexes dans un stream (3 alertes en 5 min → incident)"}
    ],
    "local_tools": [
      {"tool": "Node-RED", "description": "Visual flow editor pour le traitement d'événements IoT — très accessible, nombreux plugins"},
      {"tool": "Home Assistant automations", "description": "Règles d'automatisation intégrées — templates Jinja2 pour la logique complexe"},
      {"tool": "Python + asyncio", "description": "Pour le traitement custom en temps réel — paho-mqtt + asyncio"},
      {"tool": "SQLite avec triggers", "description": "Déclencheurs sur les insertions pour les traitements immédiats"}
    ]
  },
  [
    {"prompt": "Comment détecter en temps réel si quelqu'un entre dans la pièce ?", "answer": "Capteur PIR → MQTT → Node-RED (ou Home Assistant). Le flux : capteur publie 'mouvement: détecté' → Node-RED filtre sur ce topic → si contexte = correct (heure, mode) → déclenche l'action (notification, lumière, alerte ALFRED). La latence totale < 200ms avec une architecture locale."},
    {"prompt": "Comment agréger des données capteurs en temps réel pour un dashboard ?", "answer": "Stack recommandée : capteurs → MQTT → Telegraf (collecte) → InfluxDB (stockage timeseries) → Grafana (visualisation). Tout local. Telegraf s'abonne aux topics MQTT et insère dans InfluxDB automatiquement. Grafana rafraîchit en temps réel (5-30s selon le besoin). Cette stack est gratuite, performante et standard en domotique avancée."}
  ],
  ["temps réel", "stream processing", "Node-RED", "événements", "MQTT"]
))

save("professional/iot/iot_network_protocols.json", ku_iot(
  "iot_network_protocols",
  "Protocoles réseau IoT",
  "Le choix du protocole réseau IoT (Zigbee, Z-Wave, Matter, Wi-Fi, BLE) détermine la portée, la consommation énergétique, la latence, l'interopérabilité et la sécurité du système. Chaque protocole a ses cas d'usage optimaux.",
  "Les protocoles réseau IoT sont les standards de communication utilisés par les dispositifs connectés pour échanger des données. Ils se distinguent par leur portée, leur bande passante, leur consommation énergétique, leur topologie réseau et leur niveau d'interopérabilité.",
  {
    "protocols_comparison": [
      {"protocol": "Zigbee", "range": "10-100m", "power": "Très faible", "bandwidth": "250Kbps", "topology": "Mesh", "pros": ["Très faible consommation", "Mesh auto-réparant", "Large écosystème"], "cons": ["Interopérabilité variable entre marques", "Nécessite un hub"]},
      {"protocol": "Z-Wave", "range": "30-100m", "power": "Faible", "bandwidth": "100Kbps", "topology": "Mesh", "pros": ["Interopérabilité garantie (certification)", "Bande fréquence dédiée (moins d'interférences)"], "cons": ["Écosystème plus petit que Zigbee", "Plus cher"]},
      {"protocol": "Matter", "range": "Variable (IP-based)", "power": "Variable", "bandwidth": "Haut", "topology": "IP over Thread/Wi-Fi/Ethernet", "pros": ["Interopérabilité garantie cross-marques", "Sécurité moderne", "Support Apple/Google/Amazon/Amazon"], "cons": ["Standard récent (2022) — peu de dispositifs natifs"]},
      {"protocol": "Wi-Fi", "range": "30-100m", "power": "Élevé", "bandwidth": "Très haut", "topology": "Star", "pros": ["Pas de hub nécessaire", "Intégration directe"], "cons": ["Consommation élevée", "Sature le réseau Wi-Fi", "Sécurité variable"]},
      {"protocol": "BLE (Bluetooth Low Energy)", "range": "10-30m", "power": "Très faible", "bandwidth": "1Mbps", "topology": "Star/Mesh", "pros": ["Natif sur smartphones", "Très faible énergie"], "cons": ["Portée limitée", "Connectivité directe limitée sans hub"]}
    ],
    "recommendation_by_use_case": [
      "Capteurs batterie (température, humidité, détecteurs) : Zigbee ou Z-Wave",
      "Éclairage connecté : Zigbee (le plus large écosystème en 2024-2026)",
      "Nouveau projet cross-marque (2025+) : Matter",
      "Caméras et flux vidéo : Wi-Fi (bande passante nécessaire)",
      "Localisation intérieure : BLE"
    ]
  },
  [
    {"prompt": "Quel protocole choisir pour ma domotique : Zigbee ou Matter ?", "answer": "En 2025-2026 : Zigbee pour les capteurs batterie (large écosystème, fiable, faible consommation) et Matter pour les nouveaux dispositifs qui le supportent (interopérabilité future garantie). Les deux coexistent dans Home Assistant. Ne pas choisir uniquement du Wi-Fi pour la domotique — sature le réseau et consomme trop."},
    {"prompt": "Pourquoi mes dispositifs Zigbee perdent parfois la connexion ?", "answer": "Zigbee utilise un mesh — chaque dispositif alimenté (ampoule, prise connectée) est un routeur qui étend le réseau. Les problèmes courants : trop peu de routeurs dans le mesh (seulement des capteurs batterie), interférences Wi-Fi sur le canal 2.4GHz (aligner les canaux : Zigbee 11/15/20/25 pour éviter les canaux Wi-Fi 1/6/11), ou hub trop éloigné. Ajouter une prise connectée Zigbee entre le hub et les capteurs éloignés résout souvent le problème."}
  ],
  ["protocoles", "Zigbee", "Z-Wave", "Matter", "Wi-Fi", "BLE"]
))

save("professional/iot/iot_data_persistence.json", ku_iot(
  "iot_data_persistence",
  "Persistance des données IoT",
  "Les données IoT sont des timeseries — la structure optimale pour les stocker, les requêter et les analyser est une base de données dédiée aux séries temporelles (InfluxDB, TimescaleDB) plutôt qu'une base relationnelle classique.",
  "La persistance des données IoT est le stockage structuré et durable des mesures capteurs et événements IoT pour permettre leur analyse historique, leur visualisation et leur utilisation dans les modèles IA, avec une attention particulière aux performances sur les données temporelles.",
  {
    "timeseries_databases": [
      {"db": "InfluxDB", "type": "TSDB open source (v2 BSL, v1 MIT)", "pros": ["Performant", "Flux language pour l'analyse", "Grafana intégration native"], "cons": ["Licence BSL pour v2 (cloud commercial payant)"]},
      {"db": "TimescaleDB", "type": "Extension PostgreSQL", "pros": ["SQL standard", "Compatible avec l'écosystème PostgreSQL", "Excellent pour les jointures hybrides data relationnelle + timeseries"], "cons": ["Plus lourd qu'InfluxDB pour le pur timeseries"]},
      {"db": "SQLite avec tables temporelles", "type": "Léger, local", "pros": ["Zéro configuration", "Très léger", "Idéal pour les petits volumes"], "cons": ["Pas optimisé pour les timeseries — performances limitées à l'échelle"]}
    ],
    "retention_policies": [
      "Haute fréquence (1s) : garder 7 jours → downsampler à 1min → garder 1 an",
      "Downsampling automatique : agréger les données anciennes pour réduire le volume",
      "Données event (alertes, incidents) : conserver plus longtemps que les timeseries capteurs",
      "RGPD : les données de présence/comportement nécessitent une durée de conservation définie et un droit à l'effacement"
    ]
  },
  [
    {"prompt": "Comment stocker l'historique des données capteurs pour ALFRED ?", "answer": "Stack simple et efficace : InfluxDB v1 (licence MIT, très léger) avec Grafana pour la visualisation. Pour les données de conversation ALFRED : SQLite (déjà en place). Les données capteurs IoT (si intégrées) → MQTT → Telegraf → InfluxDB → Grafana. Tout local, tout gratuit, très performant."},
    {"prompt": "Pourquoi ne pas utiliser MySQL/PostgreSQL pour les données IoT ?", "answer": "MySQL/PostgreSQL sont conçus pour des lignes avec beaucoup de colonnes — les timeseries sont des millions de lignes avec peu de colonnes. Les TSDBs sont optimisées pour ce pattern : compression des timestamps (1-3x plus compact), index temporels natifs (requêtes range très rapides), et fonctions d'agrégation temporelle natives. Pour un petit système (< 100k points/jour), SQLite ou PostgreSQL suffisent. Au-delà : TSDB."}
  ],
  ["timeseries", "InfluxDB", "TimescaleDB", "persistence", "SQLite"]
))

save("professional/iot/environmental_signal_processing.json", ku_iot(
  "environmental_signal_processing",
  "Traitement des signaux environnementaux",
  "Les signaux environnementaux (lumière, son, température, humidité, CO2) sont des indicateurs du contexte qui permettent d'enrichir la compréhension de la situation d'un utilisateur et d'adapter les réponses en conséquence.",
  "Le traitement des signaux environnementaux est l'acquisition, le filtrage et l'interprétation des données physiques mesurées par des capteurs d'ambiance pour produire une compréhension du contexte utile aux systèmes d'intelligence ambiante.",
  {
    "environmental_signals": [
      {"signal": "Lumière (lux)", "interpretation": "Heure approximative, activité probable (travail intense vs repos), mode d'éclairage", "sensor": "BH1750, TSL2561"},
      {"signal": "Son (dB SPL)", "interpretation": "Niveau de bruit ambiant, présence de personnes, activité en cours", "sensor": "INMP441, MAX4466"},
      {"signal": "Température (°C)", "interpretation": "Confort thermique, activité physique, saison", "sensor": "DHT22, BME280, SHT40"},
      {"signal": "Humidité (%HR)", "interpretation": "Confort, risque de moisissures, impact sur la santé perçue", "sensor": "DHT22, BME280"},
      {"signal": "CO2 (ppm)", "interpretation": "Qualité de l'air, niveau d'occupation de la pièce, besoin de ventilation", "sensor": "SCD40, MH-Z19B"},
      {"signal": "COV (TVOC)", "interpretation": "Produits chimiques volatils, qualité de l'air global", "sensor": "SGP30, BME688"}
    ],
    "cognitive_impact_of_environment": [
      "CO2 > 1000 ppm : dégradation mesurable des fonctions cognitives (concentration, mémoire)",
      "Température > 26°C : réduction de la productivité cognitive de 8-12% (Harvard T.H. Chan School)",
      "Lumière > 500 lux à 5000K : améliore l'éveil et la concentration",
      "Bruit > 65dB : augmente le stress et réduit la qualité du travail cognitif"
    ],
    "alfred_context_enrichment": "ALFRED peut utiliser les données environnementales pour enrichir son contexte : si le CO2 est élevé, suggérer d'aérer ; si la luminosité est faible en après-midi, adapter le ton ; si la température est inconfortable, en tenir compte dans les recommandations de récupération."
  },
  [
    {"prompt": "Quels capteurs ajouter autour d'ALFRED pour enrichir son contexte ?", "answer": "Par ordre de valeur : (1) CO2 (SCD40 ~35€) — impacte directement la cognition, information utile pour ALFRED, (2) Température+humidité (BME280 ~5€) — confort et contexte général, (3) Lumière (BH1750 ~3€) — estimation de l'heure et de l'ambiance. Ces trois capteurs donnent un contexte environnemental riche. Tout s'intègre via I2C/GPIO sur un Raspberry Pi ou via Zigbee avec des capteurs commerciaux (Aqara, Sonoff)."},
    {"prompt": "Comment ALFRED peut utiliser la qualité de l'air pour m'aider ?", "answer": "Si le CO2 dépasse 1000 ppm, ALFRED peut signaler proactivement : 'L'air est un peu chargé — ouvrir une fenêtre 5 min aiderait à maintenir ta concentration.' Cette alerte proactive est un exemple d'intelligence ambiante appliquée : le capteur fournit le signal, ALFRED fournit le contexte et la suggestion actionnable."}
  ],
  ["capteurs", "environnement", "CO2", "lumière", "température", "cognition"]
))

save("professional/iot/energy_optimization_home.json", ku_iot(
  "energy_optimization_home",
  "Optimisation énergétique domestique",
  "L'optimisation énergétique domestique utilise les capteurs IoT et la domotique pour réduire la consommation sans dégrader le confort. Les gains moyens sont de 20-30% sur le chauffage et l'éclairage avec des dispositifs simples.",
  "L'optimisation énergétique domestique est l'utilisation de capteurs, d'actionneurs et d'algorithmes de contrôle pour maximiser l'efficacité énergétique d'un logement, en adaptant la consommation aux besoins réels des occupants et aux contraintes tarifaires.",
  {
    "optimization_levers": [
      {"lever": "Chauffage/climatisation", "savings": "15-30%", "methods": ["Programmation horaire", "Détection de présence", "Mode éco automatique en absence", "Apprentissage des préférences"]},
      {"lever": "Éclairage", "savings": "10-20%", "methods": ["Extinction automatique en absence", "Adaptation selon la lumière naturelle", "LED connectées avec scenes"]},
      {"lever": "Appareils en veille", "savings": "5-10%", "methods": ["Prises connectées avec coupure automatique", "Détection de veille prolongée"]},
      {"lever": "Optimisation tarifaire", "savings": "10-20%", "methods": ["Décalage des consommations aux heures creuses", "Intégration tarifs dynamiques (Tempo EDF)"]}
    ],
    "presence_detection": "La détection de présence fiable est la clé de l'optimisation : chauffer uniquement quand quelqu'un est là. Capteurs PIR classiques + règle 'absent depuis > 20 min → mode éco'. Amélioration avec BLE (trackers de téléphone) ou reconnaissance d'appareils sur le réseau Wi-Fi (nmap/Fing).",
    "alfred_energy_awareness": "ALFRED peut intégrer le contexte énergétique : suggérer de lancer le lave-vaisselle la nuit (heures creuses), rappeler d'éteindre les veilles avant une longue absence, ou anticiper la recharge des batteries selon les tarifs."
  },
  [
    {"prompt": "Comment démarrer l'optimisation énergétique avec la domotique ?", "answer": "Par ordre d'impact : (1) Prises connectées sur les gros consommateurs en veille (TV, box, PC de salon) avec coupure automatique, (2) Thermostat connecté avec programmation horaire et détection de présence, (3) Éclairage LED avec extinction automatique par capteur de présence. Ces trois investissements ont le meilleur ROI (< 2 ans d'amortissement pour le thermostat)."},
    {"prompt": "Comment ALFRED peut aider à réduire ma consommation électrique ?", "answer": "ALFRED peut agir comme coordinateur : rappeler les habitudes de consommation ('tu laisses souvent la box allumée la nuit'), suggérer des optimisations selon les tarifs heure creuse, et intégrer des alertes domotiques ('la clim est restée allumée pendant ton absence'). L'IA contextuelle transforme des données de consommation en recommandations actionnables."}
  ],
  ["énergie", "optimisation", "domotique", "chauffage", "présence"]
))

save("professional/iot/edge_device_authentication.json", ku_iot(
  "edge_device_authentication",
  "Authentification des dispositifs edge",
  "Authentifier les dispositifs IoT avant de leur permettre de publier sur le réseau est une étape de sécurité fondamentale. Les identités de dispositif (certificats, PSK, OAuth2 device flow) protègent l'intégrité du système.",
  "L'authentification des dispositifs edge est le processus par lequel un système vérifie l'identité d'un dispositif IoT avant de lui accorder l'accès aux ressources réseau, en utilisant des mécanismes cryptographiques (certificats, tokens) adaptés aux contraintes des systèmes embarqués.",
  {
    "auth_methods": [
      {"method": "Username/Password MQTT", "security": "Faible si non chiffré — acceptable avec TLS", "use": "Dispositifs simples sur réseau local TLS"},
      {"method": "Certificate-based TLS (mTLS)", "security": "Fort", "use": "Systèmes critiques, connexions cloud", "challenge": "Gestion des certificats (renouvellement, révocation)"},
      {"method": "Pre-shared keys (PSK)", "security": "Moyen", "use": "Dispositifs très contraints en ressources", "challenge": "Distribution sécurisée des clés"},
      {"method": "OAuth2 Device Flow", "security": "Fort", "use": "Dispositifs qui se connectent à des APIs cloud", "flow": "Dispositif → code → utilisateur autorise → token"}
    ],
    "local_auth_setup": [
      "Mosquitto avec ACL (Access Control List) : chaque dispositif a un username/password unique",
      "Certificats auto-signés pour le réseau local (Let's Encrypt si accès externe)",
      "Rotation régulière des credentials (au moins annuelle)",
      "Monitoring des connexions inattendues (nouveau device sur le broker → alerte)"
    ]
  },
  [
    {"prompt": "Comment sécuriser mon broker MQTT contre les accès non autorisés ?", "answer": "Trois niveaux : (1) Username/password unique par dispositif dans mosquitto.conf + password file, (2) TLS pour chiffrer le canal (même sur réseau local), (3) ACL (Access Control List) pour limiter quel dispositif peut publier/s'abonner sur quels topics. Résultat : un dispositif compromis ne peut pas publier sur les topics d'un autre dispositif."},
    {"prompt": "Un nouveau dispositif inconnu s'est connecté à mon broker MQTT — que faire ?", "answer": "Incident de sécurité potentiel. Vérifier les logs du broker (mosquitto log_type all) pour identifier le source IP et les topics tentés. Si l'IP n'est pas reconnue : bloquer via le firewall, changer les credentials de tous les dispositifs, vérifier si d'autres dispositifs ont été compromis. Dans le futur : implémenter des ACL strictes pour rejeter les connexions non authentifiées."}
  ],
  ["authentification", "sécurité", "MQTT", "certificats", "ACL"]
))

save("professional/iot/iot_monitoring_alerting.json", ku_iot(
  "iot_monitoring_alerting",
  "Monitoring et alerting IoT",
  "Un système IoT sans monitoring est un système aveugle — on ne sait pas qu'un capteur est mort, que les données dérivent ou qu'une intrusion a eu lieu jusqu'à ce que les conséquences arrivent. Le monitoring préventif évite les surprises.",
  "Le monitoring IoT est la surveillance continue des dispositifs, des flux de données et des métriques systèmes pour détecter les anomalies, les pannes et les dérives avant qu'elles n'impactent le service. L'alerting déclenche des notifications selon des seuils définis.",
  {
    "monitoring_dimensions": [
      {"dimension": "Disponibilité des dispositifs", "metrics": ["Last seen timestamp", "Heartbeat manqués", "Taux de perte de paquets"]},
      {"dimension": "Qualité des données", "metrics": ["Valeurs hors plage", "Taux de valeurs manquantes", "Drift de calibration"]},
      {"dimension": "Performance système", "metrics": ["Latence MQTT", "CPU/RAM du hub", "Espace disque"]},
      {"dimension": "Sécurité", "metrics": ["Connexions inattendues", "Tentatives d'authentification échouées", "Trafic réseau anormal"]}
    ],
    "alerting_tools": [
      {"tool": "Grafana Alerting", "description": "Alertes basées sur les métriques InfluxDB — email, Slack, PushOver"},
      {"tool": "Home Assistant notifications", "description": "Notifications mobiles sur des conditions domotiques"},
      {"tool": "Watchdog scripts", "description": "Scripts cron qui vérifient la fraîcheur des données et alertent si trop vieux"},
      {"tool": "MQTT watchdog", "description": "Monitorer les topics de heartbeat — si silence > X min → alerte"}
    ]
  },
  [
    {"prompt": "Comment savoir si un capteur IoT est mort ou hors ligne ?", "answer": "Heartbeat pattern : chaque capteur publie un message sur son topic toutes les N minutes. Un script de monitoring vérifie la fraîcheur (last_seen). Si > 2× la période → alerte. En domotique : Home Assistant a un mécanisme d'unavailability natif pour les dispositifs Zigbee/Z-Wave. Pour les capteurs MQTT custom, ajouter un timestamp à chaque publication et monitorer."},
    {"prompt": "Comment recevoir une alerte si ALFRED ne répond plus ?", "answer": "Watchdog process : un script externe (cron ou service systemd) vérifie régulièrement qu'ALFRED est actif (ping sur l'API locale, vérification du processus). Si silence → notification PushOver ou SMS. Et réciproquement : ALFRED peut lui-même envoyer un heartbeat régulier vers un service de monitoring (UptimeRobot en mode 'push') — si le heartbeat cesse, UptimeRobot alerte."}
  ],
  ["monitoring", "alerting", "heartbeat", "disponibilité", "Grafana"]
))

# =============================================================================
# professional / engineering / reasoning (10 premiers fichiers)
# =============================================================================

save("professional/engineering/reasoning/ambiguity_resolution.json", ku_reas(
  "ambiguity_resolution",
  "Résolution d'ambiguïté",
  "Les LLMs rencontrent régulièrement des requêtes ambiguës. Bien les résoudre, c'est identifier la source de l'ambiguïté (lexicale, syntaxique, pragmatique), choisir l'interprétation la plus probable, ou poser une question de clarification ciblée.",
  "La résolution d'ambiguïté dans les LLMs est le processus par lequel le modèle identifie et traite les situations où le sens ou l'intention d'un message n'est pas unique, en choisissant l'interprétation la plus probable selon le contexte, ou en demandant une clarification minimale.",
  {
    "ambiguity_types": [
      {"type": "Lexicale", "example": "'Je veux financer ma voiture' — financer = acheter avec crédit ou simplement payer ?", "resolution": "Contexte de la conversation ou inférence par défaut"},
      {"type": "Syntaxique", "example": "'J'ai vu l'homme avec les jumelles' — qui a les jumelles ?", "resolution": "Inférence pragmatique selon le contexte"},
      {"type": "Référentielle", "example": "'Il a dit qu'il viendrait' — qui est 'il' ?", "resolution": "Mémoire conversationnelle, antécédent le plus proche"},
      {"type": "Pragmatique", "example": "'Tu peux me donner l'heure ?' — demande réelle ou expression ?", "resolution": "Interprétation littérale vs pragmatique selon le contexte"}
    ],
    "resolution_strategies": [
      "Inférence par défaut : choisir l'interprétation la plus probable selon la base de connaissances et le contexte",
      "Clarification ciblée : une seule question sur le point ambigu critique, pas plusieurs questions",
      "Présupposition explicite : 'Je suppose que tu parles de X — si ce n'est pas le cas, précise'",
      "Réponse bifurquée : traiter les deux interprétations si elles sont également probables et que les réponses sont courtes"
    ],
    "alfred_application": "ALFRED évite les questions de clarification excessives — une par échange maximum. Si l'ambiguïté porte sur un détail non critique, il choisit l'interprétation la plus probable et le dit explicitement. Si l'ambiguïté rendrait la réponse entièrement inutile, il pose une question ciblée."
  },
  [
    {"prompt": "Je veux 'automatiser ma vie' — par où commencer ?", "answer": "Large question — j'interprète ça comme : identifier les tâches répétitives qui te coûtent du temps ou de l'énergie, et trouver des outils pour les déléguer. Dis-moi dans quel domaine tu veux commencer (travail, maison, finances, santé) et je cible les outils adaptés. Ou si tu as une tâche spécifique en tête, décris-la moi."},
    {"prompt": "Comment ALFRED gère les questions floues ?", "answer": "Deux approches selon le type de flou : (1) si je peux inférer une interprétation raisonnable, je réponds en la précisant explicitement au début ('Je comprends ta question comme...') — tu peux corriger si besoin. (2) Si le flou rendrait la réponse inutile, je pose une seule question ciblée sur le point essentiel. Je n'interroge pas sur tout à la fois."}
  ],
  ["ambiguïté", "clarification", "interprétation", "contexte", "pragmatique"]
))

save("professional/engineering/reasoning/chain_of_thought_basics.json", ku_reas(
  "chain_of_thought_basics",
  "Chain of Thought — raisonnement pas à pas",
  "Le Chain of Thought (CoT) est une technique de prompting qui encourage le LLM à décomposer son raisonnement en étapes explicites avant de donner une réponse. Il améliore significativement les performances sur les tâches complexes et réduit les erreurs.",
  "Le Chain of Thought (CoT) est une technique de prompting et une capacité de raisonnement des LLMs qui consiste à générer une séquence d'étapes de raisonnement intermédiaires avant de produire la réponse finale, améliorant les performances sur les tâches qui nécessitent plusieurs étapes logiques.",
  {
    "cot_techniques": [
      {"technique": "Few-shot CoT", "description": "Fournir des exemples de raisonnement pas à pas dans le prompt", "trigger": "Exemples avec solutions développées"},
      {"technique": "Zero-shot CoT", "description": "Ajouter 'Raisonnons étape par étape' dans le prompt", "trigger": "'Let's think step by step' / 'Raisonnons étape par étape'"},
      {"technique": "Self-consistency", "description": "Générer plusieurs chemins de raisonnement et prendre le résultat majoritaire", "use": "Problèmes ambigus ou incertains"},
      {"technique": "Tree of Thoughts", "description": "Explorer plusieurs branches de raisonnement en parallèle et évaluer leur qualité", "use": "Problèmes de planification complexe"}
    ],
    "when_cot_helps": [
      "Mathématiques et calculs multi-étapes",
      "Raisonnement logique (syllogismes, déduction)",
      "Problèmes de planification (séquences d'actions)",
      "Analyse de scénarios complexes",
      "Déduction à partir de règles et de faits"
    ],
    "cot_limitations": [
      "Peut générer des raisonnements convaincants mais incorrects (confident hallucinations)",
      "Augmente la longueur des réponses — pas adapté aux échanges rapides",
      "Les étapes intermédiaires ne sont pas nécessairement le vrai mécanisme interne du modèle",
      "Moins utile pour les connaissances factuelles directes"
    ]
  },
  [
    {"prompt": "Comment utiliser le CoT pour améliorer les réponses d'ALFRED sur des problèmes complexes ?", "answer": "Deux façons : dans le prompt système (inclure 'Pour les problèmes complexes, décompose le raisonnement avant de conclure') ou dans la requête ('Raisonne étape par étape avant de répondre'). ALFRED applique naturellement le CoT sur les problèmes qui le nécessitent — mais le forcer explicitement améliore la précision sur les questions d'analyse et de calcul."},
    {"prompt": "Peut-on faire confiance au raisonnement pas à pas d'un LLM ?", "answer": "Partiellement. Le CoT améliore la précision mais ne garantit pas l'exactitude. Les étapes intermédiaires peuvent être plausibles mais incorrectes. Pour les décisions importantes : valider la logique humainement, vérifier les chiffres indépendamment, et utiliser des sources de vérité externes quand c'est possible. Le CoT est un outil d'aide à la réflexion, pas une preuve."}
  ],
  ["chain of thought", "CoT", "raisonnement", "prompting", "étapes"]
))

save("professional/engineering/reasoning/confidence_estimation.json", ku_reas(
  "confidence_estimation",
  "Estimation de la confiance dans les réponses IA",
  "Un LLM ne sait pas naturellement 'ce qu'il ne sait pas'. L'estimation de la confiance consiste à évaluer la fiabilité d'une réponse et à le communiquer à l'utilisateur — via des phrases de hedge, des sources citées ou des scores explicites.",
  "L'estimation de la confiance dans les réponses IA est la capacité à évaluer et communiquer le niveau de certitude ou de fiabilité d'une réponse générée, permettant à l'utilisateur de calibrer son niveau de confiance et de prendre des décisions éclairées.",
  {
    "confidence_signals": [
      {"signal": "Cohérence interne", "description": "Le modèle produit la même réponse sur des formulations différentes de la même question — signe de forte représentation interne"},
      {"signal": "Couverture dans les données d'entraînement", "description": "Sujets rares ou très récents → confiance plus faible"},
      {"signal": "Consensus de self-consistency", "description": "Si plusieurs chemins de raisonnement convergent → plus fiable"},
      {"signal": "Présence de sources accessibles", "description": "RAG sur des sources vérifiées → confiance dans les faits plus haute"}
    ],
    "hedge_phrases": [
      "Haute confiance : réponse directe sans hedge",
      "Moyenne confiance : 'À ma connaissance...', 'Il me semble que...', 'Dans la plupart des cas...'",
      "Faible confiance : 'Je ne suis pas certain, mais...', 'Tu devrais vérifier, mais je pense que...'",
      "Hors compétence : 'C'est en dehors de ce que je maîtrise bien — consulte [source spécialisée]'"
    ],
    "alfred_confidence_system": {
      "description": "ALFRED utilise un ConfidenceScorer qui évalue la couverture mémorielle et la couverture knowledge avant de décider d'ajouter une phrase de hedge",
      "thresholds": {"high": 0.7, "medium": 0.4},
      "hedge_trigger": "Score < 0.4 → phrase de hedge automatique"
    }
  },
  [
    {"prompt": "Comment savoir si ALFRED est sûr de sa réponse ?", "answer": "Deux signaux : (1) ALFRED utilise des phrases de hedge explicites ('je pense que', 'à ma connaissance') quand sa confiance est plus faible, (2) quand ALFRED cite une source ou fait référence à sa base de connaissance, la réponse est plus fiable. Pour les informations critiques (santé, légal, financier) : toujours vérifier indépendamment, quelle que soit la confiance d'ALFRED."},
    {"prompt": "Pourquoi les LLMs sont-ils confiants même quand ils se trompent ?", "answer": "Les LLMs génèrent des réponses fluentes par construction — le modèle est entraîné à produire des réponses plausibles, pas à évaluer leur exactitude. L'hallucination confiante est une conséquence de cet entraînement. Solutions : RAG (ancrer les réponses sur des sources vérifiées), self-consistency (comparer plusieurs générations), et hedge explicite quand la confiance interne est faible."}
  ],
  ["confiance", "hedge", "hallucination", "certitude", "calibration"]
))

save("professional/engineering/reasoning/context_window_management.json", ku_reas(
  "context_window_management",
  "Gestion de la fenêtre de contexte",
  "La fenêtre de contexte d'un LLM est limitée — au-delà, le modèle oublie le début de la conversation. Gérer cette contrainte demande compression, sélection et structuration du contexte pertinent.",
  "La gestion de la fenêtre de contexte est l'ensemble des techniques permettant d'optimiser l'utilisation de la fenêtre de contexte limitée d'un LLM, en sélectionnant, compressant et structurant l'information pour maximiser la qualité des réponses sans dépasser les limites du modèle.",
  {
    "context_window_sizes": [
      {"model": "Llama 3 8B (Ollama)", "tokens": "8192 (8K)", "notes": "Court — conversations moyennes"},
      {"model": "Mistral 7B (Ollama)", "tokens": "32768 (32K)", "notes": "Confortable pour des sessions longues"},
      {"model": "GPT-4o", "tokens": "128000 (128K)", "notes": "Très long — long documents possibles"},
      {"model": "Claude 3.5 Sonnet", "tokens": "200000 (200K)", "notes": "Le plus long disponible à date"}
    ],
    "context_management_techniques": [
      {"technique": "Conversation summarization", "description": "Résumer périodiquement l'historique de conversation pour le compresser dans le contexte"},
      {"technique": "Selective retention", "description": "Garder uniquement les messages les plus pertinents pour la question courante"},
      {"technique": "Memory externalization", "description": "Stocker en mémoire externe (SQLite, vector DB) et récupérer les parties pertinentes via RAG"},
      {"technique": "Context compression", "description": "Compresser le contexte avec un modèle léger avant de l'envoyer au modèle principal"},
      {"technique": "Sliding window", "description": "Garder les N derniers messages et un résumé de l'historique plus ancien"}
    ],
    "alfred_context_strategy": "ALFRED utilise SQLite pour la mémoire épisodique (persistante entre sessions) et compresse le contexte de session en gardant les échanges récents + un résumé de la session. Pour les informations importantes, elles sont stockées en mémoire structurée et récupérées par RAG quand pertinent."
  },
  [
    {"prompt": "Pourquoi ALFRED oublie parfois des choses dites en début de conversation ?", "answer": "La fenêtre de contexte du LLM est limitée. Quand la conversation est longue, les éléments les plus anciens sortent du contexte actif du modèle. ALFRED utilise une mémoire épisodique (SQLite) pour persister les informations importantes entre sessions, mais dans une session très longue, le début peut être compressé. Si quelque chose est important, note-le ou dis-le moi en début de message — je le prendrai en compte."},
    {"prompt": "Comment optimiser les coûts d'API LLM liés au contexte ?", "answer": "Trois leviers : (1) Résumé automatique du contexte — compresser l'historique toutes les N turns, (2) RAG — ne pas mettre tout le contexte dans le prompt, injecter uniquement les parties pertinentes, (3) Modèle adapté à la tâche — ne pas utiliser GPT-4 pour les tâches qui marchent avec GPT-3.5. Le coût API LLM est quasi-linéaire avec le nombre de tokens — optimiser le contexte est le levier le plus direct."}
  ],
  ["contexte", "fenêtre", "tokens", "mémoire", "compression"]
))

save("professional/engineering/reasoning/contextual_weighting.json", ku_reas(
  "contextual_weighting",
  "Pondération contextuelle dans les réponses",
  "Face à plusieurs sources d'information (mémoire, knowledge, conversation, instructions système), un LLM doit pondérer leur importance relative. La pondération contextuelle est le mécanisme qui détermine quelle source prime.",
  "La pondération contextuelle est le processus par lequel un LLM détermine l'importance relative des différentes sources d'information disponibles (instructions système, historique conversationnel, knowledge RAG, données utilisateur) pour construire une réponse cohérente et pertinente.",
  {
    "context_sources_hierarchy": [
      {"source": "Instructions système", "weight": "Très élevé — override des autres sources dans la plupart des cas"},
      {"source": "Tour de conversation récent", "weight": "Élevé — contexte immédiat de la requête"},
      {"source": "Connaissances RAG récupérées", "weight": "Moyen-élevé — factuel et spécifique"},
      {"source": "Historique conversation lointain", "weight": "Moyen — contexte général de l'utilisateur"},
      {"source": "Connaissances d'entraînement", "weight": "Base — tout ce que le modèle sait par défaut"},
      {"source": "Inférences et extrapolations", "weight": "Faible — à hedger explicitement"}
    ],
    "weighting_challenges": [
      "Conflits entre sources (instructions système contredisent une information RAG)",
      "Sources obsolètes (connaissance d'entraînement vs information récente)",
      "Sources de qualité variable (document RAG peu fiable vs instruction explicite)",
      "Biais de récence vs importance (la dernière info n'est pas toujours la plus importante)"
    ],
    "alfred_weighting_model": "ALFRED applique une hiérarchie : règles système (non overridable) > mémoire utilisateur (contexte personnel) > knowledge RAG (factuel) > historique conversation > connaissance générale. En cas de conflit, ALFRED privilégie les sources plus spécifiques et plus récentes."
  },
  [
    {"prompt": "Si je te dis quelque chose qui contredit ta knowledge, laquelle tu choisis ?", "answer": "Ce que tu me dis prend priorité sur mes connaissances générales — tu connais ton contexte mieux que moi. Si tu me dis 'dans notre entreprise, le processus X fonctionne ainsi', je m'adapte même si c'est différent de la pratique standard. Exception : si tu me demandes quelque chose qui viole une règle de sécurité ou éthique fondamentale — là les règles système s'appliquent quoi qu'il arrive."},
    {"prompt": "Comment les LLMs choisissent ce qui prime dans leur contexte ?", "answer": "L'attention mechanism des transformers pondère les tokens selon leur pertinence pour générer le token suivant. Concrètement : les instructions système et le contexte récent ont tendance à peser plus. Les informations RAG bien ciblées peuvent primer sur les connaissances d'entraînement. Mais ce n'est pas déterministe — d'où l'importance d'instructions claires et de RAG précis pour guider la pondération vers ce qu'on veut."}
  ],
  ["pondération", "sources", "priorité", "RAG", "attention", "contexte"]
))

print("\nBatch 8 IoT (15) + Reasoning (10 premiers) : DONE")
