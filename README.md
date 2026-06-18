# UX-Ray: Portuguese Dark Pattern Detection Dataset

This repository contains structured datasets, reproducibility scripts, documentation, and selected evidence samples for a dark-pattern detection study on Portuguese-language websites.

The project uses **UX-Ray**, a Playwright-based evidence crawler and rule-based analyser designed to identify visible interface features associated with consent friction and dark-pattern risks. The repository is a reproducibility and transparency package for the report corpus, model-comparison runs, and selected exploratory local-model evidence.

## Repository structure

```text
uxray-dark-patterns/
├── README.md
├── LICENSE
├── dataset/
│   ├── dark_patterns_gemini_claude.csv
│   ├── dark_patterns_gpt.csv
│   ├── dark_patterns_ollama.csv
│   └── data_dictionary.md
├── docs/
│   ├── annotation_protocol.md
│   └── reproducibility.md
├── evidence_samples/
│   ├── evidence_gemini/
│   ├── evidence_gpt/
│   └── evidence_ollama/
└── scripts/
    ├── analyzer.py
    ├── crawler.py
    ├── export_dataset_gemini_claude.py
    ├── export_dataset_gpt.py
    ├── run_all_report_sites_gpt55.sh
    └── run_uxray.sh
```

## Datasets

The `dataset/` directory contains three CSV exports:

| File | Purpose |
|---|---|
| `dataset/dark_patterns_gpt.csv` | Main GPT-5.5 evidence export used for the final public report dataset. |
| `dataset/dark_patterns_gemini_claude.csv` | Comparative dataset for the earlier Gemini/Claude pipeline results. |
| `dataset/dark_patterns_ollama.csv` | Exploratory local-model/Ollama dataset associated with the extended self-hosted experiment. |
| `dataset/data_dictionary.md` | Field-level explanation of the dataset columns and reference labels. |

Each row represents one website evidence folder. The datasets include scan metadata, requested and final URLs, sector, capture status, researcher-assigned reference label, rule-based risk score, risk level, detected pattern categories, extracted interface metrics, and the list of public evidence artefacts available for that site.

## Evidence samples

Evidence samples are organised by pipeline:

```text
evidence_samples/
├── evidence_gemini/
├── evidence_gpt/
└── evidence_ollama/
```

### `evidence_gpt/`

This is the main public evidence sample set used to regenerate `dataset/dark_patterns_gpt.csv`.

### `evidence_gemini/`

This folder contains comparative Gemini evidence samples used for model-comparison and earlier pipeline validation.

### `evidence_ollama/`

This folder contains exploratory local-model/Ollama evidence samples. These runs document the extended self-hosted experiment and should be interpreted separately from the main GPT-5.5 report dataset.

## Public evidence files

Each public evidence folder may contain:

```text
screenshot.png
screenshot_with_banner.png
screenshot_consent_preferences.png
buttons.json
checkboxes.json
forms.json
summary.json
consent_banner.json
report.md
```

The public repository intentionally excludes raw or high-volume capture files such as:

```text
page.html
visible_text.txt
siamese_prediction.json
```

These files are excluded because they may contain copied third-party website content, large raw text extracts, or model-specific intermediate artefacts that are not required for public dataset reproducibility.

## Reference labels

The datasets use researcher-assigned reference labels.

| Label | Meaning |
|---|---|
| `confirmed` | Visible evidence strongly supports a dark-pattern concern. |
| `suspected` | Partial or borderline evidence suggests a dark-pattern risk. |
| `none` | Captured evidence appears balanced. |
| `inconclusive` | The site was reached, but the evidence was insufficient for reliable classification. |
| `blocked` | No reliable consent-interface analysis was possible. In the GPT export this corresponds to rows without a usable score and with little or no useful extracted evidence. |
| `unlabelled` | The site produced analysable evidence, but no confirmed/suspected/none reference label has been assigned. |

These labels are not external legal ground truth. They were assigned from the captured evidence package and are used as reference labels for evaluating and interpreting the rule-based pipeline output.

## Status rule

The GPT dataset export applies the following normalisation rule:

```text
usable score + useful extracted evidence  -> analysed
no usable score + almost no data          -> blocked
```

For true `blocked` rows, the row keeps only identification and capture metadata up to the `status` column. Fields after `status` are intentionally left empty so that blocked or non-evaluable captures are not presented as scored analyses.

Sites that were initially considered blocked during manual review but still produced a usable score and useful extracted evidence are marked as `analysed`; if no stronger manual label exists, their `reference_label` is set to `unlabelled`.

## Methodology

UX-Ray follows an evidence-first workflow:

1. `crawler.py` opens a target website using Playwright/Chromium.
2. The crawler captures browser evidence such as screenshots, buttons, links, forms, checkboxes/radio buttons, keyword hits, and scan metadata.
3. `analyzer.py` applies rule-based checks for dark-pattern indicators.
4. The generated `report.md` summarises the rule-based score, detected patterns, supporting evidence, and ethical redesign suggestions.
5. Dataset export scripts convert selected evidence folders into structured CSV datasets.
6. Researcher-assigned reference labels are used for interpretation and comparison.

## Reproducibility

Generate the main GPT-derived dataset from the included evidence samples:

```bash
python3 scripts/export_dataset_gpt.py \
  --evidence evidence_samples/evidence_gpt \
  --out dataset/dark_patterns_gpt.csv
```

Generate the Gemini/Claude comparison dataset:

```bash
python3 scripts/export_dataset_gemini_claude.py
```

Check the exported GPT status distribution:

```bash
cut -d',' -f8 dataset/dark_patterns_gpt.csv | sort | uniq -c
```

Check the first rows:

```bash
head -5 dataset/dark_patterns_gpt.csv
```

Run a single-site scan:

```bash
cd scripts
./run_uxray.sh https://www.worten.pt
```

Run the full GPT-5.5 report corpus:

```bash
cd scripts
./run_all_report_sites_gpt55.sh
```

Minimum environment:

- Python 3
- Playwright
- Chromium or a Chromium-compatible browser
- Network access to the target websites

Depending on the environment, Playwright browsers may need to be installed with:

```bash
python3 -m playwright install chromium
```

Results may vary because the analysed targets are live websites. Cookie banners, CMP configuration, wording, layout, bot-protection behaviour, and page state can change after capture.

## `report.md`

The `report.md` file is generated by `analyzer.py` for each evidence folder.

It records the Stage 2 rule-based analysis, including:

- risk score;
- risk level;
- detected pattern categories;
- supporting evidence;
- ethical redesign suggestions.

The included `report.md` files were generated from the original evidence captures. Since the public evidence samples exclude raw files such as `page.html` and `visible_text.txt`, regenerated reports from the reduced public samples may differ unless the full live capture is reproduced.

## Documentation

Additional documentation is available in:

```text
docs/
├── annotation_protocol.md
└── reproducibility.md
```

| File | Purpose |
|---|---|
| `docs/annotation_protocol.md` | Explains how researcher-assigned reference labels were created. |
| `docs/reproducibility.md` | Describes how to reproduce evidence collection and dataset export. |

## Scope

UX-Ray detects visible and extractable signals such as:

- button asymmetry;
- missing or hidden reject paths;
- pre-selected options;
- keyword indicators;
- friction or obstruction signals;
- crawler reachability problems.

UX-Ray does not fully detect:

- actual user behaviour;
- back-end consent storage;
- hidden tracking activity;
- full legal compliance;
- all multi-page flows;
- personalised A/B variants.

## Legal and ethical note

This repository identifies interface features consistent with consent-friction and dark-pattern concerns. It does not constitute a formal legal compliance determination.

Evidence screenshots may contain third-party website content and are included only as research evidence. This repository does not claim ownership over third-party website materials.

## License

The source code in this repository is released under the MIT License.

The datasets and documentation are provided for academic and reproducibility purposes. Evidence screenshots are included only as research evidence and are not relicensed as original creative works.
