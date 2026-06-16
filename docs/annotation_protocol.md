# Annotation Protocol

This document describes how the researcher-assigned reference labels were created for the UX-Ray dark-pattern dataset.

## Purpose

The reference labels are used to evaluate the rule-based pipeline output. They are not external ground truth labels and were not assigned by multiple independent annotators. For this reason, the dataset uses the term **researcher-assigned reference labels**.

## Evidence used for labelling

Each site was labelled using the captured evidence package, including:

- `screenshot.png`
- `buttons.json`
- `checkboxes.json`
- `forms.json`
- `summary.json`
- `report.md`

Where available, visual evidence from screenshots was compared with structured evidence such as button text, button size, visibility, checkbox state, and rule-based findings.

## Labelling criteria

The classification considered whether:

- an accept path and reject path were both available;
- accept and reject actions appeared at the same interaction level;
- accept and reject buttons had comparable visual salience;
- non-essential options were pre-selected;
- refusal required extra steps compared with acceptance;
- the interface contained obstruction, urgency, scarcity, or consent-friction indicators;
- the captured evidence was sufficient to support a reliable classification.

## Label definitions

| Label | Meaning |
|---|---|
| `confirmed` | Visible evidence strongly supports the presence of a dark-pattern concern. |
| `suspected` | Partial or borderline evidence suggests a dark-pattern risk, but the evidence is not strong enough for a confirmed classification. |
| `none` | Captured evidence appears balanced, with no clear dark-pattern concern identified. |
| `inconclusive` | The site was reached, but the captured evidence was insufficient for a reliable classification. |
| `blocked` | CAPTCHA, bot wall, timeout, or another access barrier prevented normal assessment. |
| `unlabelled` | No manual reference label has been assigned yet. |

## Exclusion from metrics

Blocked and inconclusive sites should be reported in corpus statistics, but excluded from precision, recall, F1, and accuracy calculations unless a specific evaluation design states otherwise.
