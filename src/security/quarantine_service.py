from src.security.security_logger import log_event

QUARANTINED_MODULES: set[str] = set()

def quarantine_module(module_name: str, reason: str) -> None:
    """Met un module en quarantaine."""
    QUARANTINED_MODULES.add(module_name)
    log_event(f"Module mis en quarantaine : {module_name} | raison={reason}", "CRITICAL")

def is_quarantined(module_name: str) -> bool:
    """Vérifie si un module est en quarantaine."""
    return module_name in QUARANTINED_MODULES

def release_module(module_name: str) -> None:
    """Sort un module de quarantaine."""
    QUARANTINED_MODULES.discard(module_name)
    log_event(f"Module sorti de quarantaine : {module_name}")
