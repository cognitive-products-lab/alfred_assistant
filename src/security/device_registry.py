"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.08
FILE         : device_registry.py
ROLE         : Registre des appareils de confiance (local-first)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Gère la liste des device_id autorisés. Stockage JSON dans data/security/trusted_devices.json.
════════════════════════════════════════════════════════════
"""
"""
device_registry.py
Registre des appareils de confiance pour ALFRED.

Gère la liste des device_id autorisés à se connecter.
Local-first : stockage JSON dans data/security/trusted_devices.json.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from src.security.security_logger import log_event
from paths import PATHS

# ─────────────────────────────────────────────────────────
# Stockage
# ─────────────────────────────────────────────────────────

_REGISTRY_FILE = PATHS.data_security / "trusted_devices.json"


def _load_registry() -> dict:
    """Charge le registre depuis le disque."""
    if not _REGISTRY_FILE.exists():
        return {}
    try:
        return json.loads(_REGISTRY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        log_event("Registry appareils corrompu — réinitialisé", "ERROR")
        return {}


def _save_registry(registry: dict) -> None:
    """Sauvegarde le registre sur le disque."""
    _REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    _REGISTRY_FILE.write_text(
        json.dumps(registry, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )
def list_devices(include_revoked: bool = False) -> dict:
    """Retourne la liste des appareils pour le dashboard sécurité.

    Args:
        include_revoked: si True, retourne tous les appareils (y compris révoqués).
                         si False (défaut), retourne uniquement les appareils de confiance.
    """
    if include_revoked:
        return _load_registry()  # registre complet, révoqués inclus

    return {
        device_id: data
        for device_id, data in _load_registry().items()
        if data.get("trusted", False) is True
    }


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def register_device(
    device_id: str,
    label: str = "",
    owner: str = "OWNER"
) -> None:
    """
    Enregistre un appareil comme de confiance.

    Args:
        device_id : identifiant unique de l'appareil
        label     : nom lisible (ex : "PC Céline", "Téléphone principal")
        owner     : rôle propriétaire de l'appareil
    """
    registry = _load_registry()

    registry[device_id] = {
        "label": label or device_id,
        "owner": owner,
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "trusted": True,
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }

    _save_registry(registry)
    log_event(f"Appareil enregistré : {device_id} ({label})")


def is_trusted_device(device_id: str) -> bool:
    """
    Vérifie si un appareil est dans le registre de confiance.
    Met à jour la date de dernière connexion si trouvé.
    """
    registry = _load_registry()

    if device_id not in registry:
        log_event(f"Appareil non reconnu : {device_id}", "WARNING")
        return False

    device = registry[device_id]

    if not device.get("trusted", False):
        log_event(f"Appareil révoqué : {device_id}", "WARNING")
        return False

    # Mettre à jour last_seen
    registry[device_id]["last_seen"] = datetime.now(timezone.utc).isoformat()
    _save_registry(registry)

    return True


def revoke_device(device_id: str) -> None:
    """Révoque la confiance d'un appareil sans le supprimer."""
    registry = _load_registry()

    if device_id in registry:
        registry[device_id]["trusted"] = False
        _save_registry(registry)
        log_event(f"Appareil révoqué : {device_id}", "WARNING")
    else:
        log_event(f"Révocation : appareil inconnu {device_id}", "WARNING")


def remove_device(device_id: str) -> None:
    """Supprime définitivement un appareil du registre."""
    registry = _load_registry()

    if device_id in registry:
        del registry[device_id]
        _save_registry(registry)
        log_event(f"Appareil supprimé : {device_id}", "WARNING")


def list_trusted_devices() -> dict:
    """Retourne tous les appareils de confiance actifs."""
    registry = _load_registry()
    return {
        k: v for k, v in registry.items()
        if v.get("trusted", False)
    }


def get_device_info(device_id: str) -> dict:
    """Retourne les infos d'un appareil ou {} si inconnu."""
    registry = _load_registry()
    return registry.get(device_id, {})


# ─────────────────────────────────────────────────────────
# Initialisation : appareil local par défaut
# ─────────────────────────────────────────────────────────

def init_default_device(device_id: str = "local_pc") -> None:
    """
    Enregistre l'appareil local par défaut si absent.
    À appeler au démarrage d'ALFRED.
    """
    if not is_trusted_device(device_id):
        register_device(
            device_id=device_id,
            label="PC local ALFRED",
            owner="OWNER"
        )
        log_event(f"Appareil local par défaut enregistré : {device_id}")


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Test Device Registry ===")

    register_device("local_pc", "PC Céline", "OWNER")
    print(f"local_pc de confiance : {is_trusted_device('local_pc')}")
    print(f"inconnu de confiance  : {is_trusted_device('unknown_device')}")

    print(f"Appareils : {list_trusted_devices()}")

    revoke_device("local_pc")
    print(f"local_pc après révocation : {is_trusted_device('local_pc')}")


def record_failed_attempt(device_id: str) -> None:
    """Enregistre une tentative échouée pour un appareil."""
    registry = _load_registry()
    if device_id in registry:
        registry[device_id]["failed_attempts"] = registry[device_id].get("failed_attempts", 0) + 1
        _save_registry(registry)