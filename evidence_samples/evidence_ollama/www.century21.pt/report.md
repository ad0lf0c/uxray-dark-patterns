# UX-Ray Dark Pattern Analysis Report

**Website:** https://www.century21.pt
**Final URL:** https://www.century21.pt/
**Page title:** CENTURY 21® Portugal | Encontre a sua casa.
**Risk score:** 4.0/10
**Risk level:** Medium - preliminary

## Consent Banner Interaction

- **Selector matched:** `#CybotCookiebotDialog`
- **Has Accept All:** True
- **Has Reject All:** False
- **Has Manage Options:** False
- **Dismissed via:** escape_key

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

### 1. Asymmetric Consent — Accept Easier Than Reject

**Category:** manipulative_consent  
**Status:** ⚠️ confirmed  
**Risk points:** 2.5

**Evidence:**
- A one-click 'Accept All' button was detected on the consent banner.
- No equivalent 'Reject All' button was found at the same level.

### 2. Pre-selected Option (Page-Level)

**Category:** preselection  
**Status:** 🔍 suspected  
**Risk points:** 1.5

**Evidence:**
- Pre-selected option: Necessários
- Pre-selected option: CybotCookiebotDialogBodyLevelButtonNecessaryInline

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
