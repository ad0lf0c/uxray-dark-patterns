import json
import argparse
from pathlib import Path


RISK_WEIGHTS = {
    "manipulative_consent": 2.5,
    "interface_interference": 2.0,
    "urgency_scarcity": 2.0,
    "confirm_shaming": 1.5,
    "preselection": 1.5,
    "obstruction": 2.0,
}


KEYWORDS = {
    "manipulative_consent": [
        "accept all", "aceitar tudo", "manage options", "gerir opções",
        "cookies", "consent", "consentimento", "privacy", "privacidade"
    ],
    "urgency_scarcity": [
        "only today", "limited time", "last chance", "hurry", "only",
        "left", "tempo limitado", "última oportunidade", "restam", "apenas hoje"
    ],
    "confirm_shaming": [
        "no thanks", "i don't want", "não quero", "continuar sem",
        "no, i prefer", "não, prefiro"
    ],
    "obstruction": [
        "cancel", "unsubscribe", "cancelar", "anular subscrição",
        "manage subscription", "gerir subscrição"
    ],
}


def load_json(path, default=None):
    if default is None:
        default = []
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def detect_patterns(folder: Path):
    summary = load_json(folder / "summary.json", {})
    if not isinstance(summary, dict):
        summary = {}

    buttons = load_json(folder / "buttons.json", [])
    if not isinstance(buttons, list):
        buttons = []

    checkboxes = load_json(folder / "checkboxes.json", [])
    if not isinstance(checkboxes, list):
        checkboxes = []

    visible_text_path = folder / "visible_text.txt"
    visible_text = visible_text_path.read_text(encoding="utf-8") if visible_text_path.exists() else ""
    text_lower = visible_text.lower()

    findings = []

    # Keyword-based detection
    for category, words in KEYWORDS.items():
        hits = [word for word in words if word in text_lower]
        if hits:
            findings.append({
                "category": category,
                "technique": category.replace("_", " ").title(),
                "evidence": [f"Keyword detected: '{hit}'" for hit in hits],
                "risk_points": RISK_WEIGHTS.get(category, 1.0)
            })

    # Consent asymmetry detection
    button_texts = [
        (b.get("text") or "").strip().lower()
        for b in buttons
        if b.get("visible") and (b.get("text") or "").strip()
    ]

    accept_terms = ["accept all", "aceitar tudo", "allow all", "permitir tudo"]
    reject_terms = ["reject all", "rejeitar tudo", "decline all", "recusar tudo"]

    has_accept = any(any(term in text for term in accept_terms) for text in button_texts)
    has_reject = any(any(term in text for term in reject_terms) for text in button_texts)

    if has_accept and not has_reject:
        findings.append({
            "category": "manipulative_consent",
            "technique": "Asymmetric Consent Choice",
            "evidence": [
                "An 'accept all' option was detected.",
                "No equally visible 'reject all' option was detected among visible buttons/links."
            ],
            "risk_points": 2.5
        })

    # Visual hierarchy approximation
    accept_buttons = []
    reject_buttons = []

    for b in buttons:
        text = (b.get("text") or "").strip().lower()
        if not b.get("visible"):
            continue

        area = int(b.get("width") or 0) * int(b.get("height") or 0)

        if any(term in text for term in accept_terms):
            accept_buttons.append((text, area, b))
        if any(term in text for term in reject_terms):
            reject_buttons.append((text, area, b))

    if accept_buttons and reject_buttons:
        max_accept_area = max(x[1] for x in accept_buttons)
        max_reject_area = max(x[1] for x in reject_buttons)

        if max_accept_area > max_reject_area * 1.5:
            findings.append({
                "category": "interface_interference",
                "technique": "Visual Hierarchy Manipulation",
                "evidence": [
                    f"Accept option area: {max_accept_area}",
                    f"Reject option area: {max_reject_area}",
                    "The accept option appears significantly more visually prominent."
                ],
                "risk_points": 2.0
            })

    # Preselection detection
    preselected = [
        cb for cb in checkboxes
        if cb.get("checked") is True
    ]

    if preselected:
        evidence = []
        for cb in preselected[:5]:
            label = cb.get("label") or cb.get("name") or cb.get("id") or "Unnamed option"
            evidence.append(f"Pre-selected option detected: {label}")

        findings.append({
            "category": "preselection",
            "technique": "Pre-selected Consent or Option",
            "evidence": evidence,
            "risk_points": 1.5
        })

    raw_score = sum(f["risk_points"] for f in findings)
    score = min(10, round(raw_score, 1))

    if score >= 7:
        risk_level = "High"
    elif score >= 4:
        risk_level = "Medium"
    elif score > 0:
        risk_level = "Low"
    else:
        risk_level = "None detected"

    return summary, findings, score, risk_level


def generate_report(folder: Path, output: Path):
    summary, findings, score, risk_level = detect_patterns(folder)

    lines = []
    lines.append("# UX-Ray Dark Pattern Analysis Report")
    lines.append("")
    lines.append(f"**Website:** {summary.get('url_requested', 'Unknown')}")
    lines.append(f"**Final URL:** {summary.get('url_final', 'Unknown')}")
    lines.append(f"**Page title:** {summary.get('title', 'Unknown')}")
    lines.append(f"**Risk score:** {score}/10")
    lines.append(f"**Risk level:** {risk_level}")
    lines.append("")

    lines.append("## Evidence Files")
    lines.append("")
    lines.append("- `screenshot.png`")
    lines.append("- `page.html`")
    lines.append("- `visible_text.txt`")
    lines.append("- `buttons.json`")
    lines.append("- `forms.json`")
    lines.append("- `checkboxes.json`")
    lines.append("")

    lines.append("## Detected Patterns")
    lines.append("")

    if not findings:
        lines.append("No obvious dark patterns were detected by the rule-based analyzer.")
        lines.append("")
    else:
        for i, finding in enumerate(findings, 1):
            lines.append(f"### {i}. {finding['technique']}")
            lines.append("")
            lines.append(f"**Category:** {finding['category']}")
            lines.append(f"**Risk points:** {finding['risk_points']}")
            lines.append("")
            lines.append("**Evidence:**")
            for ev in finding["evidence"]:
                lines.append(f"- {ev}")
            lines.append("")

    lines.append("## Suggested Ethical Redesign")
    lines.append("")
    lines.append("- Make privacy-preserving options as visible as privacy-invasive options.")
    lines.append("- Avoid pre-selected consent options.")
    lines.append("- Use neutral wording instead of guilt, urgency, or emotional pressure.")
    lines.append("- Ensure cancellation/refusal paths require no more steps than acceptance/subscription paths.")
    lines.append("- Present important costs, renewals, and data-sharing purposes before the user commits.")
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("This is a first rule-based analysis. The next version should use an AI model to inspect the screenshot, DOM, visible text, and interaction flow to provide richer explanations.")
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"[+] Report generated: {output}")


def main():
    parser = argparse.ArgumentParser(description="UX-Ray dark pattern analyzer")
    parser.add_argument("folder", help="Evidence folder to analyze")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.exists():
        raise SystemExit(f"Folder not found: {folder}")

    output = folder / "report.md"
    generate_report(folder, output)


if __name__ == "__main__":
    main()
