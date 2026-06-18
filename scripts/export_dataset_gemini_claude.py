#!/usr/bin/env python3
"""Export all pipeline evidence into a structured CSV dataset.

Reads every evidence folder under evidence/ and evidence_gemini/,
extracts structured fields from JSON artefacts and report.md, and
writes dataset/dark_patterns.csv.

Usage:
    python3 export_dataset.py [--out dataset/dark_patterns.csv]
"""

import argparse
import csv
import json
import re
from pathlib import Path

# ── Sector mapping ────────────────────────────────────────────────────────────
SECTOR = {
    # Original corpus
    "www.worten.pt":        "Electronics retail",
    "www.auchan.pt":        "Supermarket",
    "www.booking.com":      "Travel",
    "www.continente.pt":    "Supermarket",
    "www.flytap.com":       "Airline",
    "www.meo.pt":           "Telecom",
    "www.radiopopular.pt":  "Electronics retail",
    "www.nos.pt":           "Telecom",
    "www.publico.pt":       "News",
    "expresso.pt":          "News",
    "www.expresso.pt":      "News",
    "www.fnac.pt":          "Electronics retail",
    # Expanded corpus
    "www.cgd.pt":           "Banking",
    "www.millenniumbcp.pt": "Banking",
    "www.fidelidade.pt":    "Insurance",
    "www.ageas.pt":         "Insurance",
    "www.rtp.pt":           "Media / Streaming",
    "www.sapo.pt":          "Media / Portal",
    "www.pingodoce.pt":     "Supermarket",
    "www.lidl.pt":          "Supermarket",
    "www.vodafone.pt":      "Telecom",
    "www.edp.pt":           "Utilities",
}

# ── Ground-truth labels (manually assigned by researcher) ─────────────────────
# Values: "confirmed" | "suspected" | "none" | "inconclusive" | "blocked"
GROUND_TRUTH = {
    # Original corpus
    "www.worten.pt":       "confirmed",      # visual hierarchy + ghost button
    "www.auchan.pt":       "confirmed",      # colour-based asymmetric consent
    "www.booking.com":     "none",           # banner is relatively fair
    "www.continente.pt":   "confirmed",      # complexity overload + buried reject
    "www.flytap.com":      "confirmed",      # pre-selected round trip + consent asymmetry
    "www.meo.pt":          "inconclusive",   # no banner captured
    "www.radiopopular.pt": "inconclusive",   # banner found, buttons unmeasured
    "www.nos.pt":          "blocked",
    "www.publico.pt":      "blocked",
    "expresso.pt":         "blocked",
    "www.expresso.pt":     "blocked",
    "www.fnac.pt":         "blocked",
    # Expanded corpus
    "www.cgd.pt":          "confirmed",      # no reject-all, accept-only blue button
    "www.millenniumbcp.pt":"suspected",      # accept 1.52x reject; reject exists but smaller
    "www.fidelidade.pt":   "confirmed",      # red accept button, no reject path
    "www.ageas.pt":        "blocked",
    "www.rtp.pt":          "suspected",      # no reject-all; 1017 partners = complexity overload
    "www.sapo.pt":         "inconclusive",   # banner not captured
    "www.pingodoce.pt":    "suspected",       # all 3 options present BUT filled green accept vs white-outline reject — ghost/fill visual asymmetry
    "www.lidl.pt":         "suspected",      # reject exists but path is obstructed
    "www.vodafone.pt":     "blocked",
    "www.edp.pt":          "blocked",
}

GT_PATTERNS = {
    # Original corpus
    "www.worten.pt":       "interface_interference,manipulative_consent",
    "www.auchan.pt":       "interface_interference,manipulative_consent",
    "www.booking.com":     "",
    "www.continente.pt":   "obstruction,manipulative_consent",
    "www.flytap.com":      "preselection,manipulative_consent",
    "www.meo.pt":          "",
    "www.radiopopular.pt": "",
    # Expanded corpus
    "www.cgd.pt":          "manipulative_consent",
    "www.millenniumbcp.pt":"interface_interference",
    "www.fidelidade.pt":   "interface_interference,manipulative_consent",
    "www.rtp.pt":          "manipulative_consent,obstruction",
    "www.sapo.pt":         "",
    "www.pingodoce.pt":    "",
    "www.lidl.pt":         "obstruction",
}


def load_json(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def parse_report(report_path: Path) -> dict:
    """Extract score, risk level, finding counts and categories from report.md."""
    result = {
        "score": None,
        "risk_level": "",
        "findings_count": 0,
        "confirmed_count": 0,
        "suspected_count": 0,
        "finding_categories": "",
    }
    if not report_path.exists():
        return result

    text = report_path.read_text(encoding="utf-8")

    m = re.search(r"\*\*Risk score:\*\*\s*([\d.]+)/10", text)
    if m:
        result["score"] = float(m.group(1))

    m = re.search(r"\*\*Risk level:\*\*\s*(.+)", text)
    if m:
        raw = m.group(1).strip()
        result["risk_level"] = raw.split(" - ")[0].strip()

    result["findings_count"] = len(re.findall(r"^### \d+\.", text, re.MULTILINE))
    result["confirmed_count"] = text.count("⚠️ confirmed")
    result["suspected_count"] = text.count("🔍 suspected")

    cats = re.findall(r"\*\*Category:\*\*\s*(\S+)", text)
    result["finding_categories"] = ",".join(sorted(set(cats)))

    return result


def extract_row(folder: Path, pipeline: str) -> dict:
    domain = folder.name.rsplit("_", 2)[0]  # strip _YYYYMMDD_HHMMSS

    summary  = load_json(folder / "summary.json")
    banner   = load_json(folder / "consent_banner.json")
    buttons  = load_json(folder / "buttons.json") if (folder / "buttons.json").exists() else []
    checks   = load_json(folder / "checkboxes.json") if (folder / "checkboxes.json").exists() else []
    report   = parse_report(folder / "report.md")

    status = summary.get("status", "unknown")
    pref   = banner.get("preference_panel") or {}

    if not isinstance(buttons, list):
        buttons = []
    if not isinstance(checks, list):
        checks = []

    pre_selected_page = sum(1 for c in checks if c.get("checked") is True)

    return {
        # ── Identification ─────────────────────────────────────────────────
        "pipeline":              pipeline,
        "domain":                domain,
        "sector":                SECTOR.get(domain, "Unknown"),
        "url_requested":         summary.get("url_requested", ""),
        "captured_at":           summary.get("captured_at", ""),
        "evidence_folder":       str(folder),

        # ── Scan outcome ───────────────────────────────────────────────────
        "status":                status,

        # ── Rule-based score ───────────────────────────────────────────────
        "score":                 report["score"],
        "risk_level":            report["risk_level"],
        "findings_count":        report["findings_count"],
        "confirmed_count":       report["confirmed_count"],
        "suspected_count":       report["suspected_count"],
        "finding_categories":    report["finding_categories"],

        # ── Consent banner ─────────────────────────────────────────────────
        "banner_detected":       banner.get("detected", False),
        "banner_selector":       banner.get("selector_matched", ""),
        "has_accept_all":        banner.get("has_accept_all", False),
        "has_reject_all":        banner.get("has_reject_all", False),
        "has_manage_options":    banner.get("has_manage_options", False),
        "accept_reject_ratio":   banner.get("accept_reject_area_ratio"),
        "banner_buttons_count":  len(banner.get("buttons", [])),
        "dismiss_method":        banner.get("dismiss_method", ""),

        # ── Preference panel ───────────────────────────────────────────────
        "pref_panel_opened":     bool(pref),
        "pref_total_checkboxes": pref.get("total_count", 0),
        "pref_pre_checked":      pref.get("pre_checked_non_essential_count", 0),

        # ── Page-level stats ───────────────────────────────────────────────
        "total_buttons_on_page": summary.get("stats", {}).get("buttons_links_count", len(buttons)),
        "pre_selected_on_page":  pre_selected_page,
        "forms_count":           summary.get("stats", {}).get("forms_count", 0),
        "visible_text_chars":    summary.get("stats", {}).get("visible_text_chars", 0),

        # ── Ground truth (researcher labels) ──────────────────────────────
        "ground_truth":          GROUND_TRUTH.get(domain, ""),
        "ground_truth_patterns": GT_PATTERNS.get(domain, ""),
    }


FIELDNAMES = [
    "pipeline", "domain", "sector", "url_requested", "captured_at",
    "status", "score", "risk_level", "findings_count", "confirmed_count",
    "suspected_count", "finding_categories",
    "banner_detected", "banner_selector", "has_accept_all", "has_reject_all",
    "has_manage_options", "accept_reject_ratio", "banner_buttons_count", "dismiss_method",
    "pref_panel_opened", "pref_total_checkboxes", "pref_pre_checked",
    "total_buttons_on_page", "pre_selected_on_page", "forms_count", "visible_text_chars",
    "ground_truth", "ground_truth_patterns",
    "evidence_folder",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export UX-Ray evidence to CSV dataset")
    parser.add_argument("--out", default="dataset/dark_patterns.csv")
    args = parser.parse_args()

    base = Path(__file__).parent
    out_path = base / args.out
    out_path.parent.mkdir(exist_ok=True)

    rows = []

    for pipeline, root in [
        ("claude", base / "evidence"),
        ("gemini", base / "evidence_gemini"),
        ("crawler_v2", base / "evidence_v2"),
    ]:
        if not root.exists():
            continue
        for folder in sorted(root.iterdir()):
            if not folder.is_dir():
                continue
            if not (folder / "summary.json").exists():
                continue
            rows.append(extract_row(folder, pipeline))

    # Keep the best scan per (pipeline, domain):
    # prefer completed over blocked, then most recent within same status.
    STATUS_RANK = {"completed": 0, "unknown": 1, "blocked": 2}
    seen: dict[tuple, dict] = {}
    for row in rows:
        key = (row["pipeline"], row["domain"])
        if key not in seen:
            seen[key] = row
        else:
            prev = seen[key]
            prev_rank = STATUS_RANK.get(prev["status"], 1)
            curr_rank = STATUS_RANK.get(row["status"], 1)
            if curr_rank < prev_rank or (curr_rank == prev_rank and row["captured_at"] > prev["captured_at"]):
                seen[key] = row
    rows = sorted(seen.values(), key=lambda r: (r["pipeline"], r["domain"]))

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[+] Dataset written: {out_path}  ({len(rows)} rows)")

    # ── Summary stats ──────────────────────────────────────────────────────
    analysed = [r for r in rows if r["status"] == "completed"]
    blocked  = [r for r in rows if r["status"] == "blocked"]
    print(f"    Rows total   : {len(rows)}")
    print(f"    Analysed     : {len(analysed)}")
    print(f"    Blocked      : {len(blocked)}")
    scores = [r["score"] for r in analysed if r["score"] is not None]
    if scores:
        print(f"    Score range  : {min(scores):.1f} – {max(scores):.1f}")
        print(f"    Score mean   : {sum(scores)/len(scores):.2f}")
    confirmed = sum(r["confirmed_count"] for r in analysed)
    print(f"    Confirmed findings: {confirmed}")


if __name__ == "__main__":
    main()
