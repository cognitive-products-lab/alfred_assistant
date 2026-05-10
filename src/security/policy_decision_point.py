from src.security.policy_engine import evaluate_policy

def decide_access(role: str, resource_sensitivity: str, action: str) -> str:
    """PDP : prend une décision d'accès."""
    return evaluate_policy(role, resource_sensitivity, action)
