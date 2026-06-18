# UX-Ray Dark Pattern Analysis Report

**Website:** https://www.bankinter.pt
**Final URL:** https://www.bankinter.pt/
**Page title:** Conta Online, Crédito e Investimentos - Bankinter
**Risk score:** 4.0/10
**Risk level:** Medium - preliminary

## Evidence Files

- `screenshot.png`
- `page.html`
- `visible_text.txt`
- `buttons.json`
- `forms.json`
- `checkboxes.json`
- `consent_banner.json`
- `summary.json`

## Detected or Suspected Patterns

### 1. Manipulative Consent Signals

**Category:** manipulative_consent  
**Status:** 🔍 suspected  
**Risk points:** 2.5

**Evidence:**
- Keyword detected: 'cookies'
- Keyword detected: 'privacidade'

### 2. Pre-selected Option (Page-Level)

**Category:** preselection  
**Status:** 🔍 suspected  
**Risk points:** 1.5

**Evidence:**
- Pre-selected option: Particular
- Pre-selected option: SIM

## Suggested Ethical Redesign

- Make privacy-preserving options as visible and easy as privacy-invasive options.
- Provide a one-click 'Reject All' at the same level as 'Accept All'.
- Use equal visual weight (size, colour, contrast) for accept and reject controls.
- Default all non-essential consent categories to **off**.
- Avoid pre-selected consent options.
- Use neutral wording instead of guilt, urgency, or emotional pressure.
- Ensure cancellation/refusal paths require no more effort than acceptance paths.
- Present costs, renewals, and data-sharing purposes before the user commits.

## Limitations

- Rule-based screening — not definitive legal or UX proof of manipulation.
- Keyword matches on the main page may produce false positives.
- Multi-step patterns (cancellation obstruction, drip pricing) require deeper flow analysis.
- An AI-assisted stage should examine the screenshots for visual context.
