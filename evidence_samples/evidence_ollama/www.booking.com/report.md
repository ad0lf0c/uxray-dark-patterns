# UX-Ray Dark Pattern Analysis Report

**Website:** https://www.booking.com
**Final URL:** https://www.booking.com/index.pt-pt.html?aid=304142&label=gen173nr-10CAEoggI46AdIM1gEaLsBiAEBmAEzuAEHyAEM2AED6AEB-AEBiAIBqAIBuALN9sHRBsACAdICJDE2ZWJiNGQzLWIzNDQtNDk0Mi05MTc1LTE4YmJmMTMyYTY4N9gCAeACAQ&chal_t=1781562188797&force_referer=
**Page title:** Booking.com | Website oficial | Os melhores hotéis, voos, alugueres de carros e alojamentos
**Risk score:** 6.5/10
**Risk level:** Medium - preliminary

## Consent Banner Interaction

- **Selector matched:** `[role='dialog'][aria-modal='true']`
- **Has Accept All:** False
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

### 1. Manipulative Consent Signals

**Category:** manipulative_consent  
**Status:** 🔍 suspected  
**Risk points:** 2.5

**Evidence:**
- Keyword detected: 'cookies'
- Keyword detected: 'privacidade'

### 2. Urgency Scarcity Signals

**Category:** urgency_scarcity  
**Status:** 🔍 suspected  
**Risk points:** 2.0

**Evidence:**
- Keyword detected: 'tempo limitado'

### 3. Obstruction Signals

**Category:** obstruction  
**Status:** 🔍 suspected  
**Risk points:** 2.0

**Evidence:**
- Keyword detected: 'cancel'

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
