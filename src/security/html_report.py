"""
html_report.py
Génère le rapport HTML de sécurité ALFRED — utilisé par la démo live.
"""

from __future__ import annotations

import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import json
from datetime import datetime, timezone

from src.security.security_dashboard import get_dashboard
from src.security.security_governance import SecurityGovernance


def _badge(text: str, color: str) -> str:
    return f'<span class="badge" style="background:{color}">{text}</span>'


def _risk_color(level: str) -> str:
    l = level.upper()
    if "CRITICAL" in l or "CRITIQUE" in l:
        return "#e74c3c"
    if "HIGH" in l or "ÉLEVÉ" in l or "ELEVE" in l:
        return "#e67e22"
    if "MEDIUM" in l or "MOYEN" in l:
        return "#f1c40f"
    if "LOW" in l or "FAIBLE" in l or "OK" in l or "✅" in l:
        return "#27ae60"
    return "#95a5a6"


def _gauge_color(rate: float) -> str:
    if rate >= 90:
        return "#27ae60"
    if rate >= 70:
        return "#f39c12"
    return "#e74c3c"


def _compliance_rows(checks: list[dict], key_ref: str) -> str:
    rows = ""
    for c in checks:
        ok    = c.get("status") == "OK"
        color = "#27ae60" if ok else "#e74c3c"
        icon  = "✓" if ok else "✗"
        ref   = c.get(key_ref, "")
        rows += f"""
        <tr>
          <td style="text-align:center;color:{color};font-size:1.1rem">{icon}</td>
          <td><span class="badge" style="background:#2c3e50">{ref}</span></td>
          <td>{c.get('name','')}</td>
          <td style="color:#888;font-size:.85rem">{c.get('detail','')}</td>
        </tr>"""
    return rows


def _gauge_block(label: str, rate: float, passed: int, total: int) -> str:
    color = _gauge_color(rate)
    return f"""
    <div class="gauge-block">
      <div class="gauge-header">
        <span class="gauge-label">{label}</span>
        <span class="gauge-pct" style="color:{color}">{rate}%</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" style="width:{rate}%;background:{color}"></div>
      </div>
      <div class="gauge-sub">{passed}/{total} contrôles validés</div>
    </div>"""


def generate_html_report(output_path: Path | None = None) -> Path:
    """Génère le rapport HTML complet et retourne son chemin."""
    now       = datetime.now(timezone.utc)
    dashboard = get_dashboard(lookback_hours=24)
    gov       = SecurityGovernance()

    score_data = dashboard.get_security_score()
    audit      = dashboard.get_audit_summary()
    threats    = dashboard.get_threat_summary()
    incidents  = dashboard.get_incident_summary()
    devices    = dashboard.get_device_summary()
    compliance = dashboard.get_compliance_status()
    iso27001   = dashboard.get_iso27001_status()
    rgpd       = dashboard.get_rgpd_status()
    findings   = gov.run_hardening_checks()
    risks      = gov.get_risk_matrix()

    score = score_data["score"]
    grade = score_data["grade"]
    grade_color = {"A": "#27ae60", "B": "#2ecc71", "C": "#f39c12",
                   "D": "#e67e22", "F": "#e74c3c"}.get(grade, "#95a5a6")

    passed_gov = sum(1 for f in findings if f.get("passed"))

    # ── Rows gouvernance ──────────────────────────────────────────────────────
    gov_rows = ""
    for f in findings:
        icon  = "✓" if f.get("passed") else "✗"
        color = "#27ae60" if f.get("passed") else _risk_color(f.get("severity", ""))
        gov_rows += f"""
        <tr>
          <td style="text-align:center;font-size:1.1rem;color:{color}">{icon}</td>
          <td><strong>{f.get('category','')}</strong></td>
          <td>{f.get('title','')}</td>
          <td><span class="badge" style="background:{_risk_color(f.get('severity',''))}">{f.get('severity','')}</span></td>
          <td style="color:#888;font-size:.85rem">{f.get('recommendation','') if not f.get('passed') else '—'}</td>
        </tr>"""

    # ── Rows conformité GDPR/OWASP ────────────────────────────────────────────
    comp_rows = _compliance_rows(compliance.get("checks", []), "standard")

    # ── Rows ISO 27001 ────────────────────────────────────────────────────────
    iso_rows = _compliance_rows(iso27001.get("checks", []), "control")

    # ── Rows RGPD ─────────────────────────────────────────────────────────────
    rgpd_rows = _compliance_rows(rgpd.get("checks", []), "article")

    # ── Rows matrice risques ──────────────────────────────────────────────────
    risk_rows = ""
    for r in risks[:8]:
        risk_rows += f"""
        <tr>
          <td style="text-align:center;font-weight:bold;font-size:1.1rem;
              color:{_risk_color(r.get('severity',''))}">{r.get('risk_score','')}</td>
          <td><span class="badge" style="background:{_risk_color(r.get('severity',''))}">{r.get('severity','')}</span></td>
          <td><strong>{r.get('category','')}</strong></td>
          <td>{r.get('risk','')}</td>
          <td style="color:#888;font-size:.85rem">{r.get('recommendation','')}</td>
        </tr>"""
    if not risk_rows:
        risk_rows = '<tr><td colspan="5" style="text-align:center;color:#27ae60;padding:1.5rem">✓ Aucun risque résiduel — posture 100 %</td></tr>'

    # ── Jauges conformité ────────────────────────────────────────────────────
    gauge_iso  = _gauge_block("ISO 27001", iso27001["compliance_rate"],
                               iso27001["passed"], iso27001["total"])
    gauge_rgpd = _gauge_block("RGPD / GDPR", rgpd["compliance_rate"],
                               rgpd["passed"], rgpd["total"])
    gauge_owasp = _gauge_block("OWASP / GDPR", compliance["compliance_rate"],
                                compliance["passed"], compliance["total"])

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
        text-transform: uppercase; letter-spacing: .08em;
        border-bottom: 1px solid var(--border); padding-bottom: .4rem; }}
  .header {{ display:flex; align-items:center; justify-content:space-between;
             border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }}
  .ts {{ color: var(--muted); font-size: .85rem; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .kpi {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px;
           padding: 1.2rem; text-align: center; }}
  .kpi-val {{ font-size: 2.2rem; font-weight: 700; }}
  .kpi-lbl {{ font-size: .8rem; color: var(--muted); margin-top: .3rem;
              text-transform: uppercase; letter-spacing: .05em; }}
  .score-circle {{ width: 110px; height: 110px; border-radius: 50%;
                   display:flex; flex-direction:column; align-items:center; justify-content:center;
                   border: 6px solid {grade_color}; margin: 0 auto .5rem; }}
  .score-num   {{ font-size: 2rem; font-weight: 800; color: {grade_color}; }}
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
  .progress-fill {{ height: 100%; border-radius: 6px; transition: width .3s; }}
  .gauges {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.2rem; margin-bottom: 2rem; }}
  .gauge-block {{ background: var(--card); border: 1px solid var(--border);
                  border-radius: 10px; padding: 1.2rem; }}
  .gauge-header {{ display:flex; justify-content:space-between; align-items:center; margin-bottom: .6rem; }}
  .gauge-label {{ font-weight: 700; font-size: 1rem; }}
  .gauge-pct   {{ font-size: 1.6rem; font-weight: 800; }}
  .gauge-sub   {{ color: var(--muted); font-size: .78rem; margin-top: .4rem; }}
  footer {{ text-align: center; color: var(--muted); font-size: .8rem; margin-top: 3rem; padding-top: 1rem;
            border-top: 1px solid var(--border); }}
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>⚡ ALFRED — Rapport de Sécurité</h1>
    <p class="ts">Généré le {now.strftime('%d/%m/%Y à %H:%M UTC')} · Fenêtre : 24h</p>
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
      <div class="progress-fill" style="width:{score}%;background:{grade_color}"></div>
    </div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#27ae60">{passed_gov}/{len(findings)}</div>
    <div class="kpi-lbl">Contrôles Gouvernance</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#{'e74c3c' if threats['total_threats']>0 else '27ae60'}">{threats['total_threats']}</div>
    <div class="kpi-lbl">Menaces (24h)</div>
  </div>
  <div class="kpi">
    <div class="kpi-val" style="color:#{'e74c3c' if incidents['open_critical']>0 else '27ae60'}">{incidents['open_critical']}</div>
    <div class="kpi-lbl">Incidents critiques</div>
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

<!-- Jauges conformité -->
<h2>Conformité Réglementaire</h2>
<div class="gauges">
  {gauge_iso}
  {gauge_rgpd}
  {gauge_owasp}
</div>

<!-- ISO 27001 -->
<h2>ISO 27001 — {iso27001['passed']}/{iso27001['total']} contrôles ({iso27001['compliance_rate']}%)</h2>
<table>
  <thead><tr><th>État</th><th>Contrôle</th><th>Domaine</th><th>Détail</th></tr></thead>
  <tbody>{iso_rows}</tbody>
</table>

<!-- RGPD -->
<h2>RGPD / GDPR — {rgpd['passed']}/{rgpd['total']} articles ({rgpd['compliance_rate']}%)</h2>
<table>
  <thead><tr><th>État</th><th>Article</th><th>Obligation</th><th>Détail</th></tr></thead>
  <tbody>{rgpd_rows}</tbody>
</table>

<!-- Gouvernance -->
<h2>Contrôles de Durcissement ({passed_gov}/{len(findings)} — {round(passed_gov/len(findings)*100) if findings else 0}%)</h2>
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

<!-- Conformité GDPR/OWASP -->
<h2>OWASP Top 10 / GDPR — {compliance['passed']}/{compliance['total']} ({compliance['compliance_rate']}%)</h2>
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
