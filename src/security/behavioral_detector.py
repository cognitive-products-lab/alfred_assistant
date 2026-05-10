def detect_behavior_anomaly(current_value: float, baseline_value: float, threshold: float = 20.0) -> bool:
    """Détecte un écart comportemental simple."""
    return abs(current_value - baseline_value) > threshold

def calculate_behavior_score(anomalies: list[bool]) -> int:
    """Calcule un score à partir d'une liste d'anomalies."""
    return sum(1 for anomaly in anomalies if anomaly)
