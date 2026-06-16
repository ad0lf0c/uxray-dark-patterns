#!/usr/bin/env python3
import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


# Edit these labels if your latest report changed any site classification.
# These are researcher-assigned reference labels, not external ground truth.
MANUAL_REFERENCE_LABELS = {
    "www.worten.pt": "confirmed",
    "www.auchan.pt": "confirmed",
    "www.booking.com": "none",
    "www.continente.pt": "confirmed",
    "www.flytap.com": "confirmed",
    "www.meo.pt": "inconclusive",
    "www.radiopopular.pt": "inconclusive",
    "www.nos.pt": "blocked",
    "www.publico.pt": "blocked",
    "expresso.pt": "blocked",
    "www.fnac.pt": "blocked",

    "www.cgd.pt": "confirmed",
    "www.millenniumbcp.pt": "suspected",
    "www.fidelidade.pt": "confirmed",
    "www.rtp.pt": "suspected",
    "www.sapo.pt": "inconclusive",
    "www.pingodoce.pt": "suspected",
    "www.lidl.pt": "suspected",
    "www.ageas.pt": "blocked",
    "www.vodafone.pt": "blocked",
    "www.edp.pt": "blocked",
}


SECTORS = {
    "www.worten.pt": "Electronics retail",
    "www.auchan.pt": "Supermarket",
    "www.booking.com": "Travel",
    "www.continente.pt": "Supermarket",
    "www.flytap.com": "Airline",
    "www.meo.pt": "Telecom",
    "www.radiopopular.pt": "Electronics retail",
    "www.nos.pt": "Telecom",
    "www.publico.pt": "News",
    "expresso.pt": "News",
    "www.fnac.pt": "Electronics retail",

    "www.cgd.pt": "Banking",
    "www.millenniumbcp.pt": "Banking",
    "www.fidelidade.pt": "Insurance",
    "www.rtp.pt": "Media",
    "www.sapo.pt": "Media",
    "www.pingodoce.pt": "Supermarket",
    "www.lidl.pt": "Supermarket",
    "www.ageas.pt": "Insurance",
    "www.vodafone.pt": "Telecom",
    "www.edp.pt": "Utilities",
}


ACCEPT_TERMS = [
    "accept", "aceitar", "aceitar todos", "aceitar tudo", "aceitar cookies",
    "aceitar todos os cookies", "permitir", "permitir todos", "allow", "allow all"
]

REJECT_TERMS = [
    "reject", "reject all", "recusar", "recusar tudo", "rejeitar",
    "rejeitar todos", "rejeitar tudo", "rejeitar cookies", "decline"
]

MANAGE_TERMS = [
    "configurar", "configuração", "definições", "preferências",
    "personalizar", "gerir", "saiba mais", "settings", "manage", "preferences"
]

BOT_TERMS = [
    "captcha", "robot", "verify you are human", "access denied",
    "forbidden", "blocked", "cloudflare", "anti-bot", "unusual traffic"
]


def read_json(path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        pass
    return default


def read_text(path):
    try:
        if path.exists():
            return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        pass
    return ""


def domain_from_folder(folder_name):
    return re.sub(r"_\d{8}_\d{6}$", "", folder_name)


def scan_date_from_folder(folder_name):
    match = re.search(r"_(\d{8})_(\d{6})$", folder_name)
    if not match:
        return ""
    raw = match.group(1) + match.group(2)
    try:
        return datetime.strptime(raw, "%Y%m%d%H%M%S").isoformat(sep=" ")
    except ValueError:
        return ""


def parse_report(report_text):
    score = ""
    risk_level = ""

    score_match = re.search(r"\*\*Risk score:\*\*\s*([0-9]+(?:\.[0-9]+)?)", report_text)
    if score_match:
        score = score_match.group(1)

    risk_match = re.search(r"\*\*Risk level:\*\*\s*([A-Za-z]+)", report_text)
    if risk_match:
        risk_level = risk_match.group(1)

    categories = re.findall(r"\*\*Category:\*\*\s*([^\n\r]+)", report_text)
    headings = re.findall(r"^###\s+\d+\.\s+(.+?)\s*$", report_text, flags=re.MULTILINE)

    detected_patterns = categories if categories else headings

    return score, risk_level, detected_patterns


def text_matches(text, terms):
    t = (text or "").lower()
    return any(term in t for term in terms)


def button_area(button):
    try:
        return float(button.get("width") or 0) * float(button.get("height") or 0)
    except Exception:
        return 0.0


def infer_status(reference_label, title, visible_text, has_report):
    if reference_label in {"blocked", "inconclusive"}:
        return reference_label

    combined = f"{title}\n{visible_text[:3000]}".lower()
    if any(term in combined for term in BOT_TERMS):
        return "blocked"

    if has_report:
        return "analysed"

    return "captured"


def main():
    parser = argparse.ArgumentParser(description="Export UX-Ray evidence folders to CSV/JSONL dataset.")
    parser.add_argument("--evidence", default="evidence", help="Evidence directory, default: evidence")
    parser.add_argument("--out", default="dataset/dark_patterns.csv", help="Output CSV path")
    args = parser.parse_args()

    evidence_dir = Path(args.evidence)
    out_csv = Path(args.out)
    out_jsonl = out_csv.with_suffix(".jsonl")

    if not evidence_dir.exists():
        raise SystemExit(f"Evidence directory not found: {evidence_dir}")

    out_csv.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for folder in sorted(evidence_dir.iterdir()):
        if not folder.is_dir():
            continue

        summary = read_json(folder / "summary.json", {})
        buttons = read_json(folder / "buttons.json", [])
        forms = read_json(folder / "forms.json", [])
        checkboxes = read_json(folder / "checkboxes.json", [])
        report_text = read_text(folder / "report.md")
        visible_text = read_text(folder / "visible_text.txt")

        folder_domain = domain_from_folder(folder.name)

        url_requested = summary.get("url_requested", "")
        url_final = summary.get("url_final", "")
        parsed_domain = urlparse(url_final or url_requested).netloc
        domain = parsed_domain or folder_domain

        title = summary.get("title", "")
        stats = summary.get("stats", {})
        keyword_hits = summary.get("keyword_hits", [])

        score, risk_level, detected_patterns = parse_report(report_text)

        visible_buttons = [
            b for b in buttons
            if b.get("visible") is True and button_area(b) > 0 and (b.get("text") or "").strip()
        ]

        accept_buttons = [
            b for b in visible_buttons
            if text_matches(b.get("text", ""), ACCEPT_TERMS)
        ]

        reject_buttons = [
            b for b in visible_buttons
            if text_matches(b.get("text", ""), REJECT_TERMS)
        ]

        manage_buttons = [
            b for b in visible_buttons
            if text_matches(b.get("text", ""), MANAGE_TERMS)
        ]

        max_accept_area = max([button_area(b) for b in accept_buttons], default=0.0)
        max_reject_area = max([button_area(b) for b in reject_buttons], default=0.0)

        if max_accept_area > 0 and max_reject_area > 0:
            accept_reject_ratio = round(max_accept_area / max_reject_area, 3)
        else:
            accept_reject_ratio = ""

        checked_inputs_count = sum(1 for c in checkboxes if c.get("checked") is True)

        reference_label = MANUAL_REFERENCE_LABELS.get(domain, "unlabelled")
        sector = SECTORS.get(domain, "Unknown")
        status = infer_status(reference_label, title, visible_text, bool(report_text))

        evidence_files = [
            f.name for f in folder.iterdir()
            if f.is_file() and f.name in {
                "screenshot.png",
                "page.html",
                "visible_text.txt",
                "buttons.json",
                "forms.json",
                "checkboxes.json",
                "summary.json",
                "report.md",
            }
        ]

        row = {
            "site_folder": folder.name,
            "domain": domain,
            "sector": sector,
            "url_requested": url_requested,
            "url_final": url_final,
            "title": title,
            "scan_date": scan_date_from_folder(folder.name),
            "status": status,
            "reference_label": reference_label,
            "rule_score": score,
            "risk_level": risk_level,
            "detected_patterns": "; ".join(detected_patterns),
            "keyword_hits_count": len(keyword_hits),
            "keyword_hits": "; ".join(str(k) for k in keyword_hits),
            "visible_text_chars": stats.get("visible_text_chars", ""),
            "buttons_links_count": stats.get("buttons_links_count", len(buttons)),
            "forms_count": stats.get("forms_count", len(forms)),
            "checkboxes_radios_count": stats.get("checkboxes_radios_count", len(checkboxes)),
            "visible_buttons_count": len(visible_buttons),
            "accept_buttons_count": len(accept_buttons),
            "reject_buttons_count": len(reject_buttons),
            "manage_buttons_count": len(manage_buttons),
            "max_accept_area": round(max_accept_area, 2),
            "max_reject_area": round(max_reject_area, 2),
            "accept_reject_area_ratio": accept_reject_ratio,
            "checked_inputs_count": checked_inputs_count,
            "evidence_files": "; ".join(sorted(evidence_files)),
        }

        rows.append(row)

    fieldnames = [
        "site_folder",
        "domain",
        "sector",
        "url_requested",
        "url_final",
        "title",
        "scan_date",
        "status",
        "reference_label",
        "rule_score",
        "risk_level",
        "detected_patterns",
        "keyword_hits_count",
        "keyword_hits",
        "visible_text_chars",
        "buttons_links_count",
        "forms_count",
        "checkboxes_radios_count",
        "visible_buttons_count",
        "accept_buttons_count",
        "reject_buttons_count",
        "manage_buttons_count",
        "max_accept_area",
        "max_reject_area",
        "accept_reject_area_ratio",
        "checked_inputs_count",
        "evidence_files",
    ]

    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with out_jsonl.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Exported {len(rows)} rows")
    print(f"CSV:   {out_csv}")
    print(f"JSONL: {out_jsonl}")


if __name__ == "__main__":
    main()