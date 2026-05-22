# ============================================================
# ALFRED — src/security/behavioral_detector.py
# Bloc 20.08 — Détection d'intrusion
#
# 📚 NOTION EXAM :
#   D42-1 — Capsule 5 : Analyse comportementale et détection d'anomalies (UEBA)
#
# 🎯 UTILITÉ ALFRED :
#   Détecte les dérives comportementales en comparant les valeurs
#   courantes à un baseline ; calcule un score d'anomalies cumulées.
#
# 🔐 BLOC SÉCURITÉ :
#   UEBA (User & Entity Behavior Analytics) — alertes sur écarts statistiques
# ============================================================

def detect_behavior_anomaly(current_value: float, baseline_value: float, threshold: float = 20.0) -> bool:
    """Détecte un écart comportemental simple."""
    return abs(current_value - baseline_value) > threshold

def calculate_behavior_score(anomalies: list[bool]) -> int:
    """Calcule un score à partir d'une liste d'anomalies."""
    return sum(1 for anomaly in anomalies if anomaly)
