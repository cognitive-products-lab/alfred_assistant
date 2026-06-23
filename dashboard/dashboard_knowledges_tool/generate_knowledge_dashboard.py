"""
PROJECT  : ALFRED
FILE     : dashboard/dashboard_knowledges_tool/generate_knowledge_dashboard.py
ROLE     : Génère knowledge_dashboard_data.json à partir du registry, de la taxonomie
           et d'un scan réel du dossier knowledges/.
           Exécuté quotidiennement par sync_dashboards.py avant la copie vers ALFRED_WEB.
USAGE    : python dashboard/dashboard_knowledges_tool/generate_knowledge_dashboard.py
OUTPUT   : dashboard/dashboard_knowledges_tool/knowledge_dashboard_data.json
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

# ── Chemins ──────────────────────────────────────────────────────────────────
ROOT         = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = ROOT / "knowledges"
REGISTRY_PATH = KNOWLEDGE_DIR / "knowledge_registry.json"
TAXONOMY_PATH = KNOWLEDGE_DIR / "taxonomy.json"
LINKS_PATH    = KNOWLEDGE_DIR / "domain_links.json"
RULES_PATH    = KNOWLEDGE_DIR / "retrieval_rules.json"
OUT_DIR       = Path(__file__).resolve().parent
OUT_PATH      = OUT_DIR / "knowledge_dashboard_data.json"

# ── Métadonnées éditoriales par domaine (FR / EN) ────────────────────────────
DOMAIN_META: dict[str, dict] = {
    "core": {
        "label_fr": "Core",        "label_en": "Core",
        "emoji": "⚙️",             "color": "#8957e5",
        "usage_fr": "Identité fondamentale d'ALFRED, ses règles de comportement, son moteur "
                    "de personnalisation et d'adaptation à l'utilisateur. Toujours chargé en "
                    "priorité absolue.",
        "usage_en": "ALFRED's fundamental identity, behavioural rules, personalisation engine "
                    "and user adaptation layer. Always loaded with top priority.",
        "retrieval_hint_fr": "Activé sur toute requête liée à l'identité, aux préférences ou "
                             "au comportement d'ALFRED.",
        "retrieval_hint_en": "Triggered on any query relating to ALFRED's identity, preferences "
                             "or behaviour.",
    },
    "human": {
        "label_fr": "Humain",      "label_en": "Human",
        "emoji": "🧠",             "color": "#3fb950",
        "usage_fr": "Compréhension de l'utilisateur : gestion du stress, bien-être, "
                    "communication, intelligence émotionnelle. Domaine le plus riche en fichiers.",
        "usage_en": "User understanding: stress management, well-being, communication, "
                    "emotional intelligence. The richest domain in file count.",
        "retrieval_hint_fr": "Activé sur les requêtes émotionnelles, relationnelles ou de bien-être.",
        "retrieval_hint_en": "Triggered on emotional, relational or well-being queries.",
    },
    "professional": {
        "label_fr": "Professionnel", "label_en": "Professional",
        "emoji": "💼",               "color": "#388bfd",
        "usage_fr": "Cybersécurité, architecture IA, GRC, normes ISO, pilotage de projet et "
                    "leadership. Le domaine le plus volumineux.",
        "usage_en": "Cybersecurity, AI architecture, GRC, ISO standards, project management and "
                    "leadership. The largest domain by volume.",
        "retrieval_hint_fr": "Activé sur les requêtes techniques, sécurité, GRC, architecture ou management.",
        "retrieval_hint_en": "Triggered on technical, security, GRC, architecture or management queries.",
    },
    "cpl": {
        "label_fr": "CPL",         "label_en": "CPL",
        "emoji": "🏢",             "color": "#e07b39",
        "usage_fr": "Knowledges spécifiques à Cognitive Products Lab : stratégie produit, "
                    "pilotage business, éthique IA. Priorité critique — contexte propriétaire.",
        "usage_en": "Knowledges specific to Cognitive Products Lab: product strategy, business "
                    "management, AI ethics. Critical priority — proprietary context.",
        "retrieval_hint_fr": "Activé sur les requêtes liées au projet ALFRED, à CPL ou à la "
                             "stratégie d'entreprise.",
        "retrieval_hint_en": "Triggered on queries relating to the ALFRED project, CPL or "
                             "business strategy.",
    },
    "culture": {
        "label_fr": "Culture",     "label_en": "Culture",
        "emoji": "🎭",             "color": "#f0883e",
        "usage_fr": "Culture générale et univers fictifs (DC, Marvel). Crée de la proximité "
                    "conversationnelle. Une pénalité évite la sélection sur requêtes techniques.",
        "usage_en": "General culture and fictional universes (DC, Marvel). Creates conversational "
                    "rapport. A penalty prevents selection on technical queries.",
        "retrieval_hint_fr": "Activé uniquement sur les requêtes culturelles ou de divertissement.",
        "retrieval_hint_en": "Triggered only on cultural or entertainment queries.",
    },
    "system": {
        "label_fr": "Système",     "label_en": "System",
        "emoji": "🔒",             "color": "#d29922",
        "usage_fr": "Règles système fondamentales : mémoire, éthique IA, accessibilité. "
                    "Déclenche des safety_notes injectées en priorité dans le prompt LLM.",
        "usage_en": "Core system rules: memory, AI ethics, accessibility. Triggers safety_notes "
                    "injected with top priority into the LLM prompt.",
        "retrieval_hint_fr": "Activé sur toute requête liée à la vie privée, à la mémoire ou "
                             "à des sujets éthiques. Bonus automatique +5.0.",
        "retrieval_hint_en": "Triggered on any query relating to privacy, memory or ethical "
                             "topics. Automatic +5.0 bonus.",
    },
    "lifestyle": {
        "label_fr": "Lifestyle",   "label_en": "Lifestyle",
        "emoji": "🌿",             "color": "#56d364",
        "usage_fr": "Vie quotidienne, santé, productivité et trajectoire de vie. Complémentaire "
                    "au domaine human pour les requêtes pratiques.",
        "usage_en": "Daily life, health, productivity and life path. Complements the human "
                    "domain for practical day-to-day queries.",
        "retrieval_hint_fr": "Activé sur les requêtes quotidiennes : organisation, santé, "
                             "habitudes, objectifs personnels.",
        "retrieval_hint_en": "Triggered on daily queries: organisation, health, habits, "
                             "personal goals.",
    },
    "cognition": {
        "label_fr": "Cognition",   "label_en": "Cognition",
        "emoji": "🧩",             "color": "#a371f7",
        "usage_fr": "Processus mentaux et systèmes de pensée : attention, focus, biais cognitifs, "
                    "pensée critique, modèles mentaux. Complémentaire au domaine human pour "
                    "les requêtes liées à la clarté d'esprit et à la prise de décision.",
        "usage_en": "Mental processes and thinking systems: attention, focus, cognitive biases, "
                    "critical thinking, mental models. Complements the human domain for "
                    "queries about mental clarity and decision-making.",
        "retrieval_hint_fr": "Activé sur les requêtes liées à la concentration, aux biais, à la "
                             "pensée critique ou aux systèmes de réflexion (deep work, modèles mentaux).",
        "retrieval_hint_en": "Triggered on queries about focus, biases, critical thinking or "
                             "thinking systems (deep work, mental models).",
    },
    "communication": {
        "label_fr": "Communication", "label_en": "Communication",
        "emoji": "💬",               "color": "#39d353",
        "usage_fr": "Toutes les formes de communication : verbale, non-verbale, écrite, digitale, "
                    "interculturelle, influence et personal branding. 20 fichiers couvrant "
                    "les soft skills communicationnels essentiels.",
        "usage_en": "All forms of communication: verbal, non-verbal, written, digital, "
                    "cross-cultural, influence and personal branding. 20 files covering "
                    "essential communication soft skills.",
        "retrieval_hint_fr": "Activé sur les requêtes liées à la prise de parole, à l'écriture, "
                             "au leadership communicationnel, aux réseaux sociaux ou à l'influence.",
        "retrieval_hint_en": "Triggered on queries about public speaking, writing, communication "
                             "leadership, social media or influence.",
    },
    "index": {
        "label_fr": "Index",       "label_en": "Index",
        "emoji": "📑",             "color": "#8b949e",
        "usage_fr": "Répertoire d'index (vide actuellement).",
        "usage_en": "Index directory (currently empty).",
        "retrieval_hint_fr": "Non utilisé dans le pipeline actuel.",
        "retrieval_hint_en": "Not used in the current pipeline.",
    },
}

ENGINE_MODULES = [
    {
        "file": "knowledge_loader.py",
        "role_fr": "Chargeur & index en mémoire",
        "role_en": "Loader & in-memory index",
        "desc_fr": "Charge registry, taxonomie, domain_links et retrieval_rules. Construit "
                   "l'index mémoire. Fournit get_knowledge(), get_by_domain(), search().",
        "desc_en": "Loads registry, taxonomy, domain_links and retrieval_rules. Builds the "
                   "in-memory index. Provides get_knowledge(), get_by_domain(), search().",
    },
    {
        "file": "domain_matcher.py",
        "role_fr": "Correspondance requête → domaines",
        "role_en": "Query → domain matching",
        "desc_fr": "Fait correspondre la requête aux routes de domain_links.json par scoring "
                   "pondéré (mots-clés, synonymes, longueur). Retourne DomainMatch[].",
        "desc_en": "Matches the query to domain_links.json routes via weighted scoring "
                   "(keywords, synonyms, length). Returns DomainMatch[].",
    },
    {
        "file": "taxonomy_router.py",
        "role_fr": "Résolution intent → knowledge IDs",
        "role_en": "Intent → knowledge ID resolution",
        "desc_fr": "Parcourt taxonomy.json pour matcher les intents aux linked_knowledge. "
                   "Applique bonus priorité (critical +3.0, high +2.0, medium +1.0).",
        "desc_en": "Traverses taxonomy.json to match intents to linked_knowledge. "
                   "Applies priority bonus (critical +3.0, high +2.0, medium +1.0).",
    },
    {
        "file": "knowledge_ranker.py",
        "role_fr": "Fusion scores & classement",
        "role_en": "Score fusion & ranking",
        "desc_fr": "Fusionne DomainMatcher (×1.0) + TaxonomyRouter (×1.0) + bonus contenu "
                   "(×1.5). Filtre ≥ 6.0. Retourne top-3 knowledges.",
        "desc_en": "Fuses DomainMatcher (×1.0) + TaxonomyRouter (×1.0) + content bonus "
                   "(×1.5). Filters ≥ 6.0. Returns top-3 knowledges.",
    },
    {
        "file": "context_merger.py",
        "role_fr": "Construction du bloc LLM",
        "role_en": "LLM context block assembly",
        "desc_fr": "Assemble les knowledges retenus en prompt structuré. Tronque à 900 chars/"
                   "knowledge. Extrait et injecte les safety_notes.",
        "desc_en": "Assembles selected knowledges into a structured prompt. Truncates to "
                   "900 chars/knowledge. Extracts and injects safety_notes.",
    },
    {
        "file": "retrieval_engine.py",
        "role_fr": "Point d'entrée public",
        "role_en": "Public entry point",
        "desc_fr": "Orchestre loader → matcher → router → ranker → merger. "
                   "API publique : engine.retrieve(query) → RetrievalResult.",
        "desc_en": "Orchestrates loader → matcher → router → ranker → merger. "
                   "Public API: engine.retrieve(query) → RetrievalResult.",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
def _load_json(path: Path) -> dict | list:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


# Domaines exclus du dashboard public (version privée d'ALFRED uniquement)
PRIVATE_DOMAINS: set[str] = {"seduction"}


def _scan_domain_files() -> dict[str, dict[str, list[str]]]:
    """
    Scans knowledges/ pour compter les fichiers réels par domaine/sous-domaine.
    Retourne : { "core": { "core": ["alfred_core_identity", ...] }, ... }
    Les domaines listés dans PRIVATE_DOMAINS sont silencieusement ignorés.
    """
    result: dict[str, dict[str, list[str]]] = {}
    excluded = {
        "domain_links.json", "governance_rules.json", "knowledge_registry.json",
        "knowledge_template.json", "manifest.json", "retrieval_rules.json", "taxonomy.json",
    }
    for domain_dir in KNOWLEDGE_DIR.iterdir():
        if not domain_dir.is_dir():
            continue
        domain = domain_dir.name
        if domain in PRIVATE_DOMAINS:
            continue
        result[domain] = {}
        for item in domain_dir.iterdir():
            if item.is_dir():
                sub = item.name
                files = [
                    f.stem for f in item.iterdir()
                    if f.is_file() and f.suffix == ".json" and f.name not in excluded
                ]
                if files:
                    result[domain][sub] = sorted(files)
            elif item.is_file() and item.suffix == ".json" and item.name not in excluded:
                result[domain].setdefault("_root", []).append(item.stem)
    return result


def _get_recent_updates(domain: str, limit: int = 5) -> list[dict]:
    """Retourne les N fichiers les plus récemment modifiés pour un domaine."""
    entries: list[tuple[float, str, str]] = []
    domain_dir = KNOWLEDGE_DIR / domain
    if not domain_dir.exists():
        return []
    for f in domain_dir.rglob("*.json"):
        if f.name in {"domain_links.json", "knowledge_registry.json", "taxonomy.json",
                      "retrieval_rules.json", "knowledge_template.json",
                      "manifest.json", "governance_rules.json"}:
            continue
        try:
            mtime = f.stat().st_mtime
            rel = f.relative_to(KNOWLEDGE_DIR).as_posix()
            entries.append((mtime, rel, f.stem))
        except OSError:
            pass
    entries.sort(reverse=True)
    return [
        {
            "file": stem,
            "path": rel,
            "modified": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d"),
        }
        for mtime, rel, stem in entries[:limit]
    ]


def _get_taxonomy_priority(taxonomy: dict, domain_id: str) -> str:
    domains = taxonomy.get("domains", taxonomy.get("taxonomy", {}).get("domains", {}))
    dom = domains.get(domain_id, {})
    return dom.get("priority", "medium")


def _get_cross_links(links_data: dict) -> list[dict]:
    result = []
    for link in links_data.get("links", []):
        src_parts = link.get("source", "").split(".")
        if not src_parts:
            continue
        source_domain = src_parts[0]
        relationship = link.get("relationship", "")
        for t in link.get("targets", [])[:1]:
            target_domain = t.split(".")[0]
            if target_domain and target_domain != source_domain:
                result.append({
                    "from": source_domain,
                    "to": target_domain,
                    "label": relationship.replace("_", " "),
                })
    seen = set()
    deduped = []
    for l in result:
        key = (l["from"], l["to"])
        if key not in seen:
            seen.add(key)
            deduped.append(l)
    return deduped[:15]


def generate() -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    print(f"[knowledge_dashboard] Génération — {ts}")

    registry_data = _load_json(REGISTRY_PATH)
    taxonomy_data  = _load_json(TAXONOMY_PATH)
    links_data     = _load_json(LINKS_PATH)
    rules_data     = _load_json(RULES_PATH)
    scanned        = _scan_domain_files()

    # ── Stats globales depuis le registry ──────────────────────────────────
    knowledges_list = registry_data.get("knowledges", [])
    total     = len(knowledges_list)
    active    = sum(1 for k in knowledges_list if k.get("status") == "active")
    deprecated = sum(1 for k in knowledges_list if k.get("status") == "deprecated")

    # Compter par domaine depuis le scan réel
    domain_counts: dict[str, int] = {}
    for domain, subs in scanned.items():
        domain_counts[domain] = sum(len(files) for files in subs.values())

    # ── Retrieval config ───────────────────────────────────────────────────
    score_cfg = rules_data.get("scoring", {})
    retrieval_cfg = {
        "max_knowledge_per_query": rules_data.get("max_knowledge_per_query", 3),
        "minimum_score":           rules_data.get("minimum_score", 6.0),
        "max_domains_per_query":   rules_data.get("max_domains_per_query", 3),
        "domain_weights":          score_cfg.get("domain_weights", {}),
        "intent_match_bonus":      score_cfg.get("intent_match_bonus", 3.0),
        "title_match_bonus":       score_cfg.get("title_match_bonus", 2.5),
    }

    # ── Exemple IDs par domaine depuis le registry ─────────────────────────
    examples_by_domain: dict[str, list[str]] = {}
    for k in knowledges_list:
        d = k.get("domain", "")
        if d not in examples_by_domain:
            examples_by_domain[d] = []
        if len(examples_by_domain[d]) < 3:
            examples_by_domain[d].append(k["id"])

    # ── Construction des domaines ──────────────────────────────────────────
    domain_order = ["core", "human", "professional", "cpl", "culture", "system", "lifestyle", "cognition", "communication"]
    other_domains = [d for d in scanned if d not in domain_order]
    all_domains = domain_order + other_domains

    domains_out = []
    for domain_id in all_domains:
        subs = scanned.get(domain_id, {})
        count = domain_counts.get(domain_id, 0)
        if count == 0:
            continue

        meta  = DOMAIN_META.get(domain_id, {
            "label_fr": domain_id.title(), "label_en": domain_id.title(),
            "emoji": "📂", "color": "#8b949e",
            "usage_fr": "", "usage_en": "",
            "retrieval_hint_fr": "", "retrieval_hint_en": "",
        })
        priority = _get_taxonomy_priority(taxonomy_data, domain_id)

        subdomains_out = {}
        for sub, files in subs.items():
            subdomains_out[sub] = {"count": len(files), "files": files}

        # Sous-domaine plat (liste de noms de sous-dossiers + _root)
        sub_names = [s for s in subdomains_out if s != "_root"]

        domains_out.append({
            "id":       domain_id,
            "label_fr": meta["label_fr"],
            "label_en": meta["label_en"],
            "emoji":    meta["emoji"],
            "priority": priority,
            "color":    meta["color"],
            "count":    count,
            "active_count": sum(
                1 for k in knowledges_list
                if k.get("domain") == domain_id and k.get("status") == "active"
            ),
            "subdomains":       subdomains_out,
            "subdomain_names":  sub_names,
            "examples":         examples_by_domain.get(domain_id, []),
            "usage_fr":         meta["usage_fr"],
            "usage_en":         meta["usage_en"],
            "retrieval_hint_fr": meta["retrieval_hint_fr"],
            "retrieval_hint_en": meta["retrieval_hint_en"],
            "recent_updates":   _get_recent_updates(domain_id),
        })
        print(f"  {domain_id:18s}  {count:4d} fichiers  "
              f"{len(sub_names):2d} sous-domaines  priorité:{priority}")

    # ── Cross-links ────────────────────────────────────────────────────────
    cross_links = _get_cross_links(links_data)

    # ── Sortie ────────────────────────────────────────────────────────────
    output = {
        "generated_at":    ts,
        "version":         "1.0",
        "registry_version": registry_data.get("version", "unknown"),
        "stats": {
            "total_knowledges": total,
            "active":           active,
            "deprecated":       deprecated,
            "domains_count":    len(domains_out),
            "engine_modules":   len(ENGINE_MODULES),
            "max_per_query":    retrieval_cfg["max_knowledge_per_query"],
            "score_threshold":  retrieval_cfg["minimum_score"],
        },
        "domains":          domains_out,
        "cross_links":      cross_links,
        "retrieval_config": retrieval_cfg,
        "engine_modules":   ENGINE_MODULES,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"\n  [OK] {OUT_PATH}  ({size_kb:.1f} Ko)")
    print(f"     {total} knowledges · {len(domains_out)} domaines · "
          f"{len(cross_links)} liens inter-domaines")


if __name__ == "__main__":
    generate()
