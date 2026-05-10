def evaluate_policy(role: str, resource_sensitivity: str, action: str) -> str:
    """Évalue une politique d'accès simple."""
    if resource_sensitivity == "CRITICAL" and role not in ["OWNER", "ADMIN"]:
        return "DENY"

    if action in ["DELETE_DATA", "EXPORT_DATA"] and role != "OWNER":
        return "DENY"

    return "ALLOW"
