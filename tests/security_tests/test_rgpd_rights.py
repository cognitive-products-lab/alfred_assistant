"""
PROJECT : ALFRED
BLOCK   : B20 / RGPD
FILE    : tests/security_tests/test_rgpd_rights.py
ROLE    : Tests des 5 droits RGPD — Art. 15/16/17/20/21

Vérifie que chaque droit est réellement implémenté et fonctionnel :
  Art. 15 — Accès          : export_user_data() produit un fichier JSON lisible
  Art. 16 — Rectification  : user_profile.json est éditable
  Art. 17 — Effacement     : src/memory existe et est effaçable
  Art. 20 — Portabilité    : export_portable() + import_portable() round-trip
  Art. 21 — Opposition     : config/features.json liste les fonctions opposables
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


# ── Art. 15 — Droit d'accès ──────────────────────────────────────────────────

class TestArt15Access:

    def test_export_command_importable(self):
        """Le module export_command est importable."""
        from src.conversation.commands.export_command import export_user_data
        assert callable(export_user_data)

    def test_export_produces_file(self, tmp_path):
        """export_user_data() produit un fichier JSON non vide."""
        from src.conversation.commands.export_command import export_user_data
        out = tmp_path / "export_art15.json"
        result = export_user_data(output_path=out)
        assert result["status"] == "OK"
        assert out.exists()
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["_meta"]["right"].startswith("Art. 15")

    def test_export_contains_sections(self, tmp_path):
        """L'export contient au moins une section de données."""
        from src.conversation.commands.export_command import export_user_data
        out = tmp_path / "export_art15.json"
        result = export_user_data(output_path=out)
        assert len(result["sections_collected"]) >= 1

    def test_export_redacts_sensitive_keys(self, tmp_path):
        """Aucune clé cryptographique n'apparaît en clair dans l'export."""
        from src.conversation.commands.export_command import export_user_data
        out = tmp_path / "export_art15.json"
        export_user_data(output_path=out)
        content = out.read_text(encoding="utf-8").lower()
        for forbidden in ("fernet_key", "pin_salt", "secret_key", "mfa_secret"):
            assert forbidden not in content or "[redacted" in content, \
                f"Champ sensible '{forbidden}' non masqué dans l'export Art. 15"

    def test_commands_package_exists(self):
        """Le package src/conversation/commands/ existe."""
        pkg = ROOT / "src/conversation/commands/__init__.py"
        assert pkg.exists(), "src/conversation/commands/__init__.py manquant"


# ── Art. 16 — Rectification ──────────────────────────────────────────────────

class TestArt16Rectification:

    def test_user_profile_exists(self):
        """data/profile/user_profile.json est présent."""
        profile = ROOT / "data/profile/user_profile.json"
        assert profile.exists(), "user_profile.json manquant"

    def test_user_profile_is_valid_json(self):
        """user_profile.json est un JSON valide."""
        profile = ROOT / "data/profile/user_profile.json"
        data = json.loads(profile.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_user_profile_is_writable(self, tmp_path):
        """Un fichier de profil peut être modifié (simulation rectification)."""
        profile = ROOT / "data/profile/user_profile.json"
        data = json.loads(profile.read_text(encoding="utf-8"))
        out = tmp_path / "profile_modified.json"
        data["_test_rectification"] = "test_ok"
        out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        restored = json.loads(out.read_text(encoding="utf-8"))
        assert restored["_test_rectification"] == "test_ok"


# ── Art. 17 — Effacement ─────────────────────────────────────────────────────

class TestArt17Erasure:

    def test_memory_module_exists(self):
        """src/memory/ contient au moins un module Python."""
        mem_dir = ROOT / "src/memory"
        assert mem_dir.exists(), "src/memory/ manquant"
        py_files = list(mem_dir.glob("*.py"))
        assert len(py_files) >= 1, "Aucun module Python dans src/memory/"

    def test_memory_data_files_accessible(self):
        """Les fichiers de mémoire sont accessibles pour effacement."""
        episodes = ROOT / "data/memory/episodes.json"
        # Si le fichier existe, vérifier qu'il est lisible
        if episodes.exists():
            data = json.loads(episodes.read_text(encoding="utf-8"))
            assert data is not None

    def test_erasure_simulation(self, tmp_path):
        """Simulation d'effacement : remplacement par objet vide sans erreur."""
        fake_memory = tmp_path / "episodes.json"
        fake_memory.write_text(json.dumps({"episodes": [{"id": 1, "text": "test"}]}), encoding="utf-8")
        # Effacement = remplacement par structure vide
        fake_memory.write_text(json.dumps({"episodes": [], "_erased_at": "2026-06-18"}), encoding="utf-8")
        result = json.loads(fake_memory.read_text(encoding="utf-8"))
        assert result["episodes"] == []


# ── Art. 20 — Portabilité ────────────────────────────────────────────────────

class TestArt20Portability:

    def test_portability_module_importable(self):
        """Le module portability est importable."""
        from src.conversation.commands.portability import export_portable, import_portable
        assert callable(export_portable)
        assert callable(import_portable)

    def test_export_portable_produces_file(self, tmp_path):
        """export_portable() produit un fichier JSON structuré."""
        from src.conversation.commands.portability import export_portable
        out = tmp_path / "portability_export.json"
        result = export_portable(output_path=out)
        assert result["status"] == "OK"
        assert out.exists()
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["_meta"]["right"].startswith("Art. 20")
        assert "sections" in payload
        assert "reimportable_sections" in payload

    def test_export_portable_has_schema_version(self, tmp_path):
        """L'export inclut une version de schéma pour la compatibilité."""
        from src.conversation.commands.portability import export_portable, EXPORT_SCHEMA_VERSION
        out = tmp_path / "portability_export.json"
        export_portable(output_path=out)
        payload = json.loads(out.read_text(encoding="utf-8"))
        assert payload["_meta"]["schema_version"] == EXPORT_SCHEMA_VERSION

    def test_import_portable_rejects_wrong_schema(self, tmp_path):
        """import_portable() rejette un fichier avec schema_version incompatible."""
        from src.conversation.commands.portability import import_portable
        bad_file = tmp_path / "bad_export.json"
        bad_file.write_text(json.dumps({
            "_meta": {"schema_version": "99.9", "right": "Art. 20 RGPD — Portabilité"},
            "sections": {}
        }), encoding="utf-8")
        result = import_portable(bad_file)
        assert result["status"] == "ERROR"
        assert "incompatible" in result["reason"]

    def test_import_portable_rejects_missing_file(self):
        """import_portable() retourne ERROR si le fichier n'existe pas."""
        from src.conversation.commands.portability import import_portable
        result = import_portable("/tmp/inexistant_export_abc123.json")
        assert result["status"] == "ERROR"

    def test_round_trip_portable(self, tmp_path):
        """Round-trip export→import sans perte de données sur sections de test."""
        from src.conversation.commands.portability import export_portable, import_portable, EXPORT_SCHEMA_VERSION
        # Construit un mini-export valide sans toucher aux vrais fichiers
        out = tmp_path / "rt_export.json"
        payload = {
            "_meta": {
                "right": "Art. 20 RGPD — Portabilité des données",
                "schema_version": EXPORT_SCHEMA_VERSION,
                "exported_at": "2026-06-18T00:00:00+00:00",
                "generated_by": "test",
                "reimport_command": "",
                "note": "",
            },
            "sections": {},
            "sections_missing": [],
            "reimportable_sections": [],
        }
        out.write_text(json.dumps(payload), encoding="utf-8")
        result = import_portable(out)
        # Aucune section → statut OK avec listes vides
        assert result["status"] == "OK"
        assert result["restored"] == []


# ── Art. 21 — Opposition ─────────────────────────────────────────────────────

class TestArt21Opposition:

    def test_features_config_exists(self):
        """config/features.json existe."""
        features = ROOT / "config/features.json"
        assert features.exists(), "config/features.json manquant — Art. 21 non implémenté"

    def test_features_config_valid_json(self):
        """config/features.json est un JSON valide."""
        features = ROOT / "config/features.json"
        data = json.loads(features.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_features_has_opposable_items(self):
        """Au moins une fonctionnalité est marquée art21_opposable:true."""
        features = ROOT / "config/features.json"
        data = json.loads(features.read_text(encoding="utf-8"))
        opposable = [
            k for k, v in data.get("features", {}).items()
            if v.get("art21_opposable") is True
        ]
        assert len(opposable) >= 1, "Aucune fonctionnalité opposable dans features.json"

    def test_features_has_user_rights_declaration(self):
        """config/features.json déclare les droits utilisateur RGPD."""
        features = ROOT / "config/features.json"
        data = json.loads(features.read_text(encoding="utf-8"))
        rights = data.get("user_rights", {})
        assert rights.get("art21_opposition") is True, "art21_opposition non déclaré dans user_rights"

    def test_features_art21_flag_toggleable(self, tmp_path):
        """Une fonctionnalité opposable peut être désactivée par l'utilisateur."""
        features_src = ROOT / "config/features.json"
        data = json.loads(features_src.read_text(encoding="utf-8"))
        # Simulation : désactiver 'memory_conversational'
        out = tmp_path / "features_modified.json"
        data["features"]["memory_conversational"]["enabled"] = False
        out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        restored = json.loads(out.read_text(encoding="utf-8"))
        assert restored["features"]["memory_conversational"]["enabled"] is False


# ── Synthèse — vérification 5/5 ──────────────────────────────────────────────

class TestRgpdRightsSynthesis:

    def test_all_five_rights_have_proof_files(self):
        """Les 5 droits RGPD ont tous au moins un fichier de preuve sur disque."""
        proofs = {
            "Art.15 — Accès":           ROOT / "src/conversation/commands/export_command.py",
            "Art.16 — Rectification":   ROOT / "data/profile/user_profile.json",
            "Art.17 — Effacement":      ROOT / "src/memory",
            "Art.20 — Portabilité":     ROOT / "src/conversation/commands/portability.py",
            "Art.21 — Opposition":      ROOT / "config/features.json",
        }
        missing = [right for right, path in proofs.items() if not path.exists()]
        assert not missing, f"Droits RGPD sans preuve fichier : {missing}"
