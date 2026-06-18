# UX-Ray Dark Pattern Analysis Report

**Website:** https://www.supercasa.pt
**Final URL:** https://supercasa.pt/
**Page title:** SUPERCASA - Moradias e apartamentos, arrendamento e venda, anúncios gratuitos - SUPERCASA
**Risk score:** 2.5/10
**Risk level:** Low - preliminary

## Consent Banner Interaction

- **Selector matched:** `[role='dialog'][aria-modal='true']`
- **Has Accept All:** False
- **Has Reject All:** False
- **Has Manage Options:** False
- **Dismissed via:** close_button

## Evidence Files

- `screenshot.png`
- `screenshot_with_banner.png`
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
