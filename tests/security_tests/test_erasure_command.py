"""
PROJECT      : ALFRED
BLOCK        : B01 / RGPD
FILE         : test_erasure_command.py
ROLE         : Tests du droit à l'effacement Art. 17 RGPD (src/conversation/commands/erasure_command.py)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
UPDATED      : 2026-07-11
VERSION      : V1.0
STATUS       : VALIDATED
"""

from src.conversation.commands import erasure_command
from src.conversation.commands.erasure_command import erase_user_data


def test_erase_user_data_requires_confirmation():
    result = erase_user_data(confirm=False)

    assert result["confirmed"] is False
    assert result["files"]["deleted"] == []
    assert result["memory_purged"] is False


def test_erase_user_data_calls_file_and_memory_deletion(monkeypatch):
    calls = {}

    def fake_delete_user_data(confirm=False):
        calls["files_confirm"] = confirm
        return {"confirmed": True, "deleted": ["data/user_memory.json"], "missing": [], "errors": []}

    def fake_delete_all_memories(confirm=False):
        calls["memory_confirm"] = confirm
        return True

    monkeypatch.setattr(erasure_command, "delete_user_data", fake_delete_user_data)
    monkeypatch.setattr(erasure_command, "delete_all_memories", fake_delete_all_memories)

    result = erase_user_data(confirm=True)

    assert calls["files_confirm"] is True
    assert calls["memory_confirm"] is True
    assert result["confirmed"] is True
    assert result["right"] == "Art. 17"
    assert result["files"]["deleted"] == ["data/user_memory.json"]
    assert result["memory_purged"] is True
    assert "erased_at" in result


def test_erase_user_data_reports_memory_purge_failure(monkeypatch):
    monkeypatch.setattr(
        erasure_command,
        "delete_user_data",
        lambda confirm=False: {"confirmed": True, "deleted": [], "missing": [], "errors": []},
    )
    monkeypatch.setattr(erasure_command, "delete_all_memories", lambda confirm=False: False)

    result = erase_user_data(confirm=True)

    assert result["memory_purged"] is False


def test_cli_refuses_without_confirm_flag(monkeypatch, capsys):
    monkeypatch.setattr(erasure_command.sys, "argv", ["erasure_command.py"])

    exit_code = erasure_command._run_cli()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "--confirm" in captured.out


def test_cli_refuses_on_wrong_typed_phrase(monkeypatch, capsys):
    monkeypatch.setattr(erasure_command.sys, "argv", ["erasure_command.py", "--confirm"])
    monkeypatch.setattr("builtins.input", lambda _: "oui")

    exit_code = erasure_command._run_cli()

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "annulée" in captured.out


def test_cli_erases_on_correct_typed_phrase(monkeypatch, capsys):
    monkeypatch.setattr(erasure_command.sys, "argv", ["erasure_command.py", "--confirm"])
    monkeypatch.setattr("builtins.input", lambda _: erasure_command._CLI_CONFIRM_PHRASE)
    monkeypatch.setattr(
        erasure_command,
        "delete_user_data",
        lambda confirm=False: {"confirmed": True, "deleted": ["data/user_memory.json"], "missing": [], "errors": []},
    )
    monkeypatch.setattr(erasure_command, "delete_all_memories", lambda confirm=False: True)

    exit_code = erasure_command._run_cli()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Suppression effectuée" in captured.out
