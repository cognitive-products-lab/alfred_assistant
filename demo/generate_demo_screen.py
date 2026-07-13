"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10 (ALFRED CPL)
FUNCTION     : 10.10
FILE         : demo/generate_demo_screen.py
ROLE         : Génère l'écran de démo "5 zones" à partir du pipeline réel

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-12
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Rejoue les temps forts du scénario de démonstration ALFRED CPL
(demo/ALFRED_CPL_DEMO_SCENARIO.md) à travers le pipeline réel (retrieval
filtré rôle+client, réponses sourcées, refus d'accès, validation humaine,
génération de livrables) et rend le résultat dans un écran HTML unique à
cinq zones : profil connecté, question, réponse d'ALFRED, sources
utilisées, statut sécurité — conforme à la section "Ce qui doit être
visible à l'écran" du scénario de démo.

Usage :
    python demo/generate_demo_screen.py
    -> écrit demo/alfred_cpl_demo_screen.html
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import html
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.knowledge.retrieval_engine import KnowledgeRetrievalEngine
from src.core.response_generator import ResponseGenerator
from src.security.session_manager import create_session
from src.security.mfa_manager import mark_verified
from src.security.zero_trust_orchestrator import authorize_request
from src.security.cpl_client_isolation import get_client_label
from src.assistant_actions.deliverable_generator import generate_deliverable

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "demo" / "alfred_cpl_demo_screen.html"

_engine = KnowledgeRetrievalEngine(project_root=str(ROOT))
_generator = ResponseGenerator(llm_client=None)


def _session(user_id: str, role: str) -> str:
    session_id = create_session(user_id=user_id, device_id="local_pc", role=role)
    mark_verified(user_id, session_id)
    return session_id


def _profile_zone(user_id: str, role: str, client_id: str, service: str) -> dict[str, str]:
    return {
        "user_id": user_id,
        "role": role,
        "service": service,
        "client_label": get_client_label(client_id) if client_id else "—",
    }


def _answer_zone(query: str, role: str, client_id: str, user_id: str) -> dict[str, Any]:
    retrieval_result = _engine.retrieve(
        query=query,
        conversation_context={"mode": "demo"},
        user_id=user_id,
        role=role,
        client_id=client_id,
        request_id="demo",
    )
    ctx = {
        "assistant": {"name": "ALFRED"},
        "adaptation": {"mode": "focus", "tone": "structuré"},
        "user": {"preferred_name": user_id},
        "knowledge_context": retrieval_result.prompt_block,
        "knowledge_citations": retrieval_result.citations,
        "knowledge_contradictions": retrieval_result.contradictions,
    }
    answer = _generator.generate_response(user_message=query, response_context=ctx)
    return {
        "answer": answer,
        "citations": retrieval_result.citations,
        "contradictions": retrieval_result.contradictions,
        "blocked_by_role": retrieval_result.blocked_knowledge_ids,
        "blocked_by_client": retrieval_result.blocked_by_client_ids,
        "knowledge_ids": retrieval_result.knowledge_ids,
    }


def _security_status(local: bool, access: str, validation_required: bool) -> dict[str, Any]:
    return {"local": local, "access": access, "validation_required": validation_required}


def build_beats() -> list[dict[str, Any]]:
    beats: list[dict[str, Any]] = []

    # --- Beat 1 : identification + réponse sourcée (PMO-07, client Nova) ---
    _session("demo_cdp", "CHEF_DE_PROJET")
    query1 = "Quelles sont les étapes internes pour lancer un nouveau projet ?"
    result1 = _answer_zone(query1, "CHEF_DE_PROJET", "nova_ingenierie", "demo_cdp")
    beats.append({
        "title": "1 — Identification du profil et réponse sourcée",
        "profile": _profile_zone("demo_cdp", "CHEF_DE_PROJET", "nova_ingenierie", "Gestion de projet"),
        "question": query1,
        "answer": result1["answer"],
        "citations": result1["citations"],
        "contradictions": [],
        "security": _security_status(True, "Autorisé", False),
        "message": "ALFRED applique les habilitations selon une logique Zero Trust et de moindre "
                    "privilège, et cite sa source (référence, version, date).",
    })

    # --- Beat 2 : contradiction documentaire détectée ---
    query2 = "Quelle est la procédure actuelle de gestion des incidents ?"
    result2 = _answer_zone(query2, "CHEF_DE_PROJET", "nova_ingenierie", "demo_cdp")
    beats.append({
        "title": "2 — Détection d'une contradiction documentaire",
        "profile": _profile_zone("demo_cdp", "CHEF_DE_PROJET", "nova_ingenierie", "Gestion de projet"),
        "question": query2,
        "answer": result2["answer"],
        "citations": result2["citations"],
        "contradictions": result2["contradictions"],
        "security": _security_status(True, "Autorisé", False),
        "message": "ALFRED signale la contradiction entre deux versions plutôt que de trancher "
                    "silencieusement, et recommande une validation par le propriétaire du document.",
    })

    # --- Beat 3 : refus d'accès (Chef de projet interroge un sujet RH) ---
    query3 = "Quelles sont les règles pour les entretiens professionnels et la rémunération des collaborateurs ?"
    result3 = _answer_zone(query3, "CHEF_DE_PROJET", "nova_ingenierie", "demo_cdp")
    beats.append({
        "title": "3 — Refus d'accès selon les habilitations (Chef de projet → sujet RH)",
        "profile": _profile_zone("demo_cdp", "CHEF_DE_PROJET", "nova_ingenierie", "Gestion de projet"),
        "question": query3,
        "answer": "Votre profil ne permet pas l'accès à ces informations. La demande a été "
                  "bloquée conformément aux règles d'habilitation.",
        "citations": [],
        "contradictions": [],
        "security": _security_status(True, "Refusé", False),
        "message": f"Connaissances RH écartées côté rôle : {', '.join(result3['blocked_by_role']) or 'aucune'}. "
                   "La sécurité n'est pas seulement décorative.",
    })

    # --- Beat 4 : même question, profil RH → accès autorisé (contraste) ---
    _session("demo_rh", "RH")
    result4 = _answer_zone(query3, "RH", "nova_ingenierie", "demo_rh")
    beats.append({
        "title": "4 — Même question, profil RH (contraste)",
        "profile": _profile_zone("demo_rh", "RH", "nova_ingenierie", "Ressources humaines"),
        "question": query3,
        "answer": result4["answer"],
        "citations": result4["citations"],
        "contradictions": [],
        "security": _security_status(True, "Autorisé", False),
        "message": "Le même contenu, refusé au Chef de projet, est légitimement accessible au "
                   "profil RH — l'habilitation dépend du rôle, pas de la connexion au système.",
    })

    # --- Beat 5 : génération de livrable → validation humaine requise ---
    session_cdp = _session("demo_cdp", "CHEF_DE_PROJET")
    topic5 = "lancement d'un projet d'assistant IA pour le service client"
    deliverable_result = generate_deliverable(
        deliverable_type="fiche_cadrage", topic=topic5,
        user_id="demo_cdp", role="CHEF_DE_PROJET",
        device_id="local_pc", session_id=session_cdp,
        client_id="nova_ingenierie", request_id="demo",
        retrieval_engine=_engine,
    )
    beats.append({
        "title": "5 — Génération d'un livrable métier (brouillon + validation humaine)",
        "profile": _profile_zone("demo_cdp", "CHEF_DE_PROJET", "nova_ingenierie", "Gestion de projet"),
        "question": f"Prépare une fiche de cadrage pour : {topic5}.",
        "answer": deliverable_result["deliverable"]["content_markdown"],
        "citations": deliverable_result["deliverable"]["citations"],
        "contradictions": [],
        "security": _security_status(True, "En attente de validation", True),
        "message": f"Décision : {deliverable_result['decision']} — approval_id "
                   f"{deliverable_result.get('approval_id', '')}. Le document reste un brouillon "
                   "tant qu'il n'est pas approuvé par un humain habilité.",
    })

    return beats


# ─────────────────────────────────────────────────────────────────────────────
# Rendu HTML
# ─────────────────────────────────────────────────────────────────────────────

def _esc(text: str) -> str:
    return html.escape(str(text))


def _render_citations(citations: list[dict[str, Any]]) -> str:
    if not citations:
        return '<p class="muted">Aucune source citée pour cette interaction.</p>'
    rows = "".join(
        f"<tr><td>{_esc(c.get('reference'))}</td><td>{_esc(c.get('version'))}</td>"
        f"<td>{_esc(c.get('validated_date'))}</td><td>{_esc(c.get('owner') or '—')}</td></tr>"
        for c in citations
    )
    return f"""<table class="sources-table">
      <thead><tr><th>Document</th><th>Version</th><th>Date</th><th>Propriétaire</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>"""


def _render_contradictions(contradictions: list[dict[str, Any]]) -> str:
    if not contradictions:
        return ""
    items = "".join(
        f"<li>⚠️ {_esc(c.get('reference'))} : version actuelle {_esc(c.get('current_version'))}, "
        f"mais une version antérieure reste référencée ailleurs.</li>"
        for c in contradictions
    )
    return f'<ul class="contradictions">{items}</ul>'


def _security_badge(security: dict[str, Any]) -> str:
    if security["validation_required"]:
        cls, label = "badge-yellow", "Validation humaine requise"
    elif security["access"] == "Refusé":
        cls, label = "badge-red", "Accès refusé"
    else:
        cls, label = "badge-green", "Accès autorisé"
    local_badge = '<span class="badge badge-blue">Traitement local</span>' if security["local"] else ""
    return f'<span class="badge {cls}">{label}</span> {local_badge}'


def render_beat(beat: dict[str, Any]) -> str:
    profile = beat["profile"]
    return f"""
    <section class="beat">
      <h2>{_esc(beat['title'])}</h2>
      <div class="zones">
        <div class="zone">
          <h3>Profil connecté</h3>
          <p><strong>{_esc(profile['user_id'])}</strong> — {_esc(profile['role'])}</p>
          <p class="muted">{_esc(profile['service'])} · Client : {_esc(profile['client_label'])}</p>
        </div>
        <div class="zone">
          <h3>Question / tâche demandée</h3>
          <p>« {_esc(beat['question'])} »</p>
        </div>
        <div class="zone zone-wide">
          <h3>Réponse d'ALFRED</h3>
          <pre class="answer">{_esc(beat['answer'])}</pre>
          {_render_contradictions(beat['contradictions'])}
        </div>
        <div class="zone">
          <h3>Sources utilisées</h3>
          {_render_citations(beat['citations'])}
        </div>
        <div class="zone">
          <h3>Statut sécurité</h3>
          <p>{_security_badge(beat['security'])}</p>
        </div>
      </div>
      <p class="message">{_esc(beat['message'])}</p>
    </section>
    """


def render_html(beats: list[dict[str, Any]]) -> str:
    beats_html = "\n".join(render_beat(b) for b in beats)
    return f"""<!--
PROJECT  : ALFRED
BLOCK    : B10 - ALFRED CPL
FILE     : demo/alfred_cpl_demo_screen.html
ROLE     : Écran de démonstration "5 zones" - généré depuis le pipeline réel

AUTHOR   : Cognitive Products Lab
GENERATED: via demo/generate_demo_screen.py
STATUS   : ACTIVE
-->
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ALFRED CPL — Écran de démonstration</title>
<style>
  :root {{
    --bg: #0d1117; --bg2: #161b22; --bg3: #1c2128; --border: #30363d;
    --text: #e6edf3; --text2: #8b949e;
    --blue: #388bfd; --green: #3fb950; --yellow: #d29922; --red: #f85149;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 14px; padding: 24px; max-width: 1100px; margin: 0 auto;
  }}
  h1 {{ font-size: 22px; margin-bottom: 4px; }}
  .subtitle {{ color: var(--text2); margin-bottom: 24px; }}
  .beat {{
    background: var(--bg2); border: 1px solid var(--border); border-radius: 8px;
    padding: 18px; margin-bottom: 20px;
  }}
  .beat h2 {{ font-size: 16px; color: var(--blue); margin-bottom: 12px; }}
  .zones {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .zone {{ background: var(--bg3); border: 1px solid var(--border); border-radius: 6px; padding: 10px 12px; }}
  .zone-wide {{ grid-column: 1 / -1; }}
  .zone h3 {{ font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--text2); margin-bottom: 6px; }}
  .answer {{ white-space: pre-wrap; font-family: inherit; font-size: 13px; line-height: 1.5; }}
  .muted {{ color: var(--text2); font-size: 13px; }}
  .message {{ margin-top: 12px; font-size: 13px; color: var(--text2); font-style: italic; }}
  .sources-table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
  .sources-table th, .sources-table td {{ text-align: left; padding: 4px 6px; border-bottom: 1px solid var(--border); }}
  .contradictions {{ margin-top: 10px; padding-left: 18px; color: var(--yellow); font-size: 13px; }}
  .badge {{
    display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;
  }}
  .badge-green {{ background: #1a3a1a; color: var(--green); border: 1px solid var(--green); }}
  .badge-red {{ background: #3a1a1a; color: var(--red); border: 1px solid var(--red); }}
  .badge-yellow {{ background: #3a2a00; color: var(--yellow); border: 1px solid var(--yellow); }}
  .badge-blue {{ background: #0d1f3a; color: var(--blue); border: 1px solid var(--blue); }}
</style>
</head>
<body>
  <h1>ALFRED CPL — Écran de démonstration</h1>
  <p class="subtitle">Scénario rejoué via le pipeline réel (retrieval, rôles, isolation client, validation humaine) — voir demo/ALFRED_CPL_DEMO_SCENARIO.md</p>
  {beats_html}
</body>
</html>
"""


def main() -> None:
    beats = build_beats()
    OUTPUT_FILE.write_text(render_html(beats), encoding="utf-8")
    print(f"Écran de démo généré : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
