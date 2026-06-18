# UX-Ray Dark Pattern Analysis Report

**Website:** https://www.ikea.com/pt
**Final URL:** https://www.ikea.com/pt/pt/
**Page title:** IKEA - Loja de móveis e decoração - A vida acontece em casa
**Risk score:** 8.0/10
**Risk level:** High - preliminary

## Consent Banner Interaction

- **Selector matched:** `#onetrust-banner-sdk`
- **Has Accept All:** True
- **Has Reject All:** True
- **Has Manage Options:** False
- **Accept / Reject area ratio:** 1.0×
- **Dismissed via:** reject_all

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
- Keyword detected: 'última oportunidade'

### 3. Obstruction Signals

**Category:** obstruction  
**Status:** 🔍 suspected  
**Risk points:** 2.0

**Evidence:**
- Keyword detected: 'cancel'
- Keyword detected: 'cancelar'

### 4. Pre-selected Option (Page-Level)

**Category:** preselection  
**Status:** 🔍 suspected  
**Risk points:** 1.5

**Evidence:**
- Pre-selected option: Opção: MICKE, Secretária, antracite/verm, 105x50 cm
- Pre-selected option: Opção: STRANDMON, Poltrona, Tommaboda bege forte
- Pre-selected option: Opção: JÄRNVÄG, Tapete pelo curto, motivo decorativo bege/bege escuro, 160x230 cm
- Pre-selected option: Opção: GULLABERG, Cómoda c/3 gavetas, branco, 99x48x100 cm

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
