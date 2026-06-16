# UX-Ray: Portuguese Dark Pattern Detection Dataset

This repository contains a structured dataset, reproducibility scripts, and selected evidence samples for a dark-pattern detection study on Portuguese-language websites.

The project uses **UX-Ray**, a Playwright-based evidence crawler and rule-based analyser designed to identify visible interface features associated with consent friction and dark-pattern risks.

## Repository structure

```text
uxray-dark-patterns/
├── dataset/
│   ├── dark_patterns.csv
│   ├── dark_patterns.jsonl
│   └── data_dictionary.md
├── scripts/
│   ├── crawler.py
│   ├── analyzer.py
│   ├── run_uxray.sh
│   ├── run_all_report_sites_gpt55.sh
│   └── export_dataset.py
├── evidence_samples/
│   └── selected website evidence folders
└── docs/
    ├── annotation_protocol.md
    ├── reproducibility.md
    ├── limitations.md
    └── scope.md
```

## Dataset

The main dataset is available at:

```text
dataset/dark_patterns.csv
```

An equivalent line-delimited JSON version is available at:

```text
dataset/dark_patterns.jsonl
```

Each row represents one website capture. The dataset includes scan metadata, extracted interface signals, rule-based risk scores, detected pattern categories, and researcher-assigned reference labels.

The reference labels are:

| Label          | Meaning                                                                           |
| -------------- | --------------------------------------------------------------------------------- |
| `confirmed`    | Visible evidence strongly supports a dark-pattern concern                         |
| `suspected`    | Partial or borderline evidence suggests risk                                      |
| `none`         | Captured evidence appears balanced                                                |
| `inconclusive` | Site was reached, but the evidence was insufficient for reliable classification   |
| `blocked`      | CAPTCHA, bot wall, timeout, or another access barrier prevented normal assessment |
| `unlabelled`   | No manual reference label has been assigned yet                                   |

## Methodology

UX-Ray follows an evidence-first workflow:

1. `crawler.py` opens a target website using Playwright/Chromium.
2. The crawler captures browser evidence such as screenshots, buttons, links, forms, checkboxes/radio buttons, keyword hits, and scan metadata.
3. `analyzer.py` applies rule-based checks for dark-pattern indicators.
4. The generated `report.md` summarises the rule-based score, detected patterns, and ethical redesign suggestions.
5. `export_dataset.py` converts evidence folders into `dark_patterns.csv` and `dark_patterns.jsonl`.
6. Researcher-assigned reference labels are used for evaluation and comparison.

## Evidence samples

Selected evidence samples are included under:

```text
evidence_samples/
```

Each sample may contain:

```text
screenshot.png
buttons.json
checkboxes.json
forms.json
summary.json
report.md
```

Screenshots provide visual confirmation of the captured interface state. Structured files such as `buttons.json`, `checkboxes.json`, `summary.json`, and `report.md` provide the evidence used for scoring and comparison.

Full raw captures such as `page.html` and `visible_text.txt` are not included in the public evidence samples by default because they may contain copied third-party website content.

## Reproducibility

Generate the dataset from the included evidence samples:

```bash
python scripts/export_dataset.py --evidence evidence_samples --out dataset/dark_patterns.csv
```

Run a single-site scan:

```bash
cd scripts
./run_uxray.sh https://www.worten.pt
```

Run the full report corpus:

```bash
cd scripts
./run_all_report_sites_gpt55.sh
```

Minimum environment:

* Python 3
* Playwright
* Chromium or a Chromium-compatible browser
* Network access to the target websites

Results may vary because the analysed targets are live websites. Cookie banners, CMP configuration, wording, layout, bot-protection behaviour, and page state can change after capture.

## Scope

UX-Ray detects visible and extractable signals such as:

* button asymmetry;
* missing or hidden reject paths;
* pre-selected options;
* keyword indicators;
* friction or obstruction signals;
* crawler reachability problems.

UX-Ray does not fully detect:

* actual user behaviour;
* back-end consent storage;
* hidden tracking activity;
* full legal compliance;
* all multi-page flows;
* personalised A/B variants.

## Legal and ethical note

This repository identifies interface features consistent with consent-friction and dark-pattern concerns. It does not constitute a formal legal compliance determination.

Evidence screenshots may contain third-party website content and are included only as research evidence. This repository does not claim ownership over third-party website materials.

## License

The source code in this repository is released under the MIT License.

The dataset and documentation are provided for academic and reproducibility purposes. Evidence screenshots are included only as research evidence and are not relicensed as original creative works.
