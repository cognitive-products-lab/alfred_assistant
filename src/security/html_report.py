"""
html_report.py
Génère un rapport HTML de sécurité ALFRED — utilisé par la démo live.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.security.security_dashboard import get_dashboard
from src.security.security_governance import SecurityGovernance


def _badge(text: str, color: str) -> str:
    return f'<span class="badge" style="background:{color}">{text}</span>'


def _risk_color(level: str) -> str:
    if "CRITICAL" in level.upper() or "CRITIQUE" in level.upper():
        return "#e74c3c"
    if "HIGH" in level.upper() or "ÉLEVÉ" in level.upper() or "ELEVE" in level.upper():
        return "#e67e22"
    if "MEDIUM" in level.upper() or "MOYEN" in level.upper():
        return "#f1c40f"
    if "OK" in level or "✅" in level or "+" in level:
        return "#27ae60"
    return "#95a5a6"


def generate_html_report(output_path: Path | None = None) -> Path:
    """Génère le rapport HTML et retourne son chemin."""
    now = datetime.now(timezone.utc)
    dashboard = get_dashboard(lookback_hours=24)
    gov = SecurityGovernance()

    score_data   = dashboard.get_security_score()
    audit        = dashboard.get_audit_summary()
    threats      = dashboard.get_threat_summary()
    incidents    = dashboard.get_incident_summary()
    devices      = dashboard.get_device_summary()
    compliance   = dashboard.get_compliance_status()
    findings     = gov.run_hardening_checks()
    risks        = gov.get_risk_matrix()

    score  = score_data["score"]
    grade  = score_data["grade"]
    grade_color = {"A": "#27ae60", "B": "#2ecc71", "C": "#f39c12",
                   "D": "#e67e22", "F": "#e74c3c"}.get(grade, "#95a5a6")

    passed_gov = sum(1 for f in findings if f["passed"])

    # ── Rows gouvernance ──────────────────────────────────────────────────────
    gov_rows = ""
    for f in findings:
        icon  = "✓" if f["passed"] else "✗"
        color = "#27ae60" if f["passed"] else _risk_color(f["severity"])
        gov_rows += f"""
        <tr>
          <td style="text-align:center;font-size:1.1rem;color:{color}">{icon}</td>
          <td><strong>{f['category']}</strong></td>
          <td>{f['title']}</td>
          <td><span class="badge" style="background:{_risk_color(f['severity'])}">{f['severity']}</span></td>
          <td style="color:#888;font-size:.85rem">{f['recommendation'] if not f['passed'] else '—'}</td>
        </tr>"""

    # ── Rows compliance ───────────────────────────────────────────────────────
    comp_rows = ""
    for c in compliance["checks"]:
        color = "#27ae60" if c["status"] == "OK" else "#e74c3c"
        icon  = "✓" if c["status"] == "OK" else "✗"
        comp_rows += f"""
        <tr>
          <td style="text-align:center;color:{color};font-size:1.1rem">{icon}</td>
          <td><span class="badge" style="background:#2c3e50">{c['standard']}</span></td>
          <td>{c['name']}</td>
          <td style="color:#888;font-size:.85rem">{c['detail']}</td>
        </tr>"""

    # ── Rows matrice risques ──────────────────────────────────────────────────
    risk_rows = ""
    for r in risks[:8]:
        risk_rows += f"""
        <tr>
          <td style="text-align:center;font-weight:bold;font-size:1.1rem;
              color:{_risk_color(r['severity'])}">{r['risk_score']}</td>
          <td><span class="badge" style="background:{_risk_color(r['severity'])}">{r['severity']}</span></td>
          <td><strong>{r['category']}</strong></td>
          <td>{r['risk']}</td>
          <td style="color:#888;font-size:.85rem">{r['recommendation']}</td>
        </tr>"""
    if not risk_rows:
        risk_rows = '<tr><td colspan="5" style="text-align:center;color:#27ae60;padding:1.5rem">✓ Aucun risque résiduel — posture 100 %</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ALFRED — Rapport Sécurité</title>
<style>
  :root {{
    --bg: #0d1117; --card: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e; --accent: #58a6ff;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Segoe UI', system-ui, sans-serif;
          background: var(--bg); color: var(--text); padding: 2rem; }}
  h1 {{ font-size: 1.8rem; color: var(--accent); margin-bottom: .3rem; }}
  h2 {{ font-size: 1.1rem; color: var(--muted); margin: 2rem 0 1rem;
        text-transform: uppercase; letter-spacing: .08em; border-bottom: 1px solid var(--border); padding-bottom: .4rem; }}
  .header {{ display:flex; align-items:center; justify-content:space-between;
             border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }}
  .ts {{ color: var(--muted); font-size: .85rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .kpi {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px;
           padding: 1.2rem; text-align: center; }}
  .kpi-val {{ font-size: 2.2rem; font-weight: 700; }}
  .kpi-lbl {{ font-size: .8rem; color: var(--muted); margin-top: .3rem; text-transform: uppercase; letter-spacing: .05em; }}
  .score-circle {{ width: 110px; height: 110px; border-radius: 50%;
                   display:flex; flex-direction:column; align-items:center; justify-content:center;
                   border: 6px solid {grade_color}; margin: 0 auto .5rem; }}
  .score-num {{ font-size: 2rem; font-weight: 800; color: {grade_color}; }}
  .score-grade {{ font-size: 1rem; color: {grade_color}; font-weight: 700; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--card);
           border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-bottom: 2rem; }}
  th {{ background: #1c2128; color: var(--muted); font-size: .8rem;
        text-transform: uppercase; letter-spacing: .06em; padding: .7rem 1rem; text-align: left; }}
  td {{ padding: .7rem 1rem; border-top: 1px solid var(--border); font-size: .9rem; vertical-align: middle; }}
  tr:hover td {{ background: #1c2128; }}
  .badge {{ display:inline-block; padding: .2rem .6rem; border-radius: 4px;
            font-size: .75rem; font-weight: 700; color: #fff; }}
  .progress-bar {{ background: #21262d; border-radius: 6px; height: 12px; overflow: hidden; }}
  .progress-fill {{ height: 100%; border-radius: 6px;
                    background: linear-gradient(90deg, {grade_color}, {grade_color}88); }}
  footer {{ text-align: center; color: var(--muted); font-size: .8rem; margin-top: 3rem; padding-top: 1rem;
            border-top: 1px solid var(--border); }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>⚡ ALFRED — Rapport de Sécurité</h1>
    <p class="ts">Généré le {now.strftime('%d/%m/%Y à %H:%M UTC')} · Fenêtre d'analyse : 24h</p>
  </div>
  <div style="text-align:right">
    <div class="score-circle">
      <span class="score-num">{score}</span>
      <span class="score-grade">Grade {grade}</span>
    </div>
  </div>
</div>

<!-- KPIs -->
<div class="grid">
  <div class="kpi">
    <div class="kpi-val" style="color:{grade_color}">{score}<span style="font-size:1rem">/100</span></div>
    <div class="kpi-lbl">Score Sécurité</div>
    <div class="progress-bar" style="margin-top:.6rem">
      <div class="progress-fill" style="width:{score}%"></div>
    </div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#27ae60">{passed_gov}/{len(findings)}</div>
    <div class="kpi-lbl">Contrôles Gouvernance</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#58a6ff">{compliance['passed']}/{compliance['total']}</div>
    <div class="kpi-lbl">Conformité GDPR/OWASP</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#{'e74c3c' if threats['total_threats']>0 else '27ae60'}">{threats['total_threats']}</div>
    <div class="kpi-lbl">Menaces détectées (24h)</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#{'e74c3c' if incidents['open_critical']>0 else '27ae60'}">{incidents['open_critical']}</div>
    <div class="kpi-lbl">Incidents critiques ouverts</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#58a6ff">{devices['trusted']}</div>
    <div class="kpi-lbl">Appareils de confiance</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#58a6ff">{audit['total_events']}</div>
    <div class="kpi-lbl">Événements audit (24h)</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#{'e74c3c' if audit['denial_rate']>5 else '27ae60'}">{audit['denial_rate']}%</div>
    <div class="kpi-lbl">Taux de refus</div>
  </div>
</div>

<!-- Gouvernance -->
<h2>Contrôles de Durcissement ({passed_gov}/{len(findings)} — {round(passed_gov/len(findings)*100)}%)</h2>
<table>
  <thead><tr><th>État</th><th>Catégorie</th><th>Contrôle</th><th>Sévérité</th><th>Action requise</th></tr></thead>
  <tbody>{gov_rows}</tbody>
</table>

<!-- Matrice de risques -->
<h2>Matrice de Risques</h2>
<table>
  <thead><tr><th>Score</th><th>Sévérité</th><th>Catégorie</th><th>Risque</th><th>Recommandation</th></tr></thead>
  <tbody>{risk_rows}</tbody>
</table>

<!-- Conformité -->
<h2>Conformité GDPR / OWASP Top 10 ({compliance['passed']}/{compliance['total']} — {compliance['compliance_rate']}%)</h2>
<table>
  <thead><tr><th>État</th><th>Standard</th><th>Contrôle</th><th>Détail</th></tr></thead>
  <tbody>{comp_rows}</tbody>
</table>

<footer>
  ALFRED — Architecture Local-First Zero Trust · Security by Design · Privacy by Design<br>
  Bloc 20 Sécurité · {now.strftime('%Y')}
</footer>

</body>
</html>"""

    out = output_path or Path("demo/alfred_security_report.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    path = generate_html_report()
    print(f"Rapport HTML généré : {path}")
