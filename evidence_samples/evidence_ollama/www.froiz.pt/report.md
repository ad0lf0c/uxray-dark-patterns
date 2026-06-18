# UX-Ray Dark Pattern Analysis Report

**Website:** https://www.froiz.pt
**Final URL:** https://www.froiz.pt/
**Page title:** Supermercados Froiz
**Risk score:** 4.0/10
**Risk level:** Medium - preliminary

## Consent Banner Interaction

- **Selector matched:** `#CybotCookiebotDialog`
- **Has Accept All:** True
- **Has Reject All:** False
- **Has Manage Options:** True
- **Dismissed via:** close_button
- **Preference panel:** 6 of 12 checkboxes pre-selected

## Evidence Files

- `screenshot.png`
- `screenshot_with_banner.png`
- `screenshot_consent_preferences.png`
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
- Rejection requires navigating into 'Manage Options' — an extra step not required for acceptance.

### 2. Pre-selected Non-Essential Consent Categories

**Category:** preselection  
**Status:** ⚠️ confirmed  
**Risk points:** 1.5

**Evidence:**
- 6 of 12 consent checkboxes are pre-selected in the preference panel.
- Pre-selected: 'Preferências'
- Pre-selected: 'Estatísticas'
- Pre-selected: 'Marketing'
- Pre-selected: 'CybotCookiebotDialogBodyLevelButtonPreferencesInline'
- Pre-selected: 'CybotCookiebotDialogBodyLevelButtonStatisticsInline'
- Pre-selected: 'CybotCookiebotDialogBodyLevelButtonMarketingInline'

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
