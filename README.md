# Credence Harbor

Credence Harbor is a planning-stage engineering design for a single US Rule 506(c) accredited-investor pilot. This repository records the proposed product boundaries, architecture, delivery plan, and engineering acceptance criteria.

**Planning material only. It is not an offer to sell securities, legal advice, evidence of regulatory approval, a production application, or authorization to market an offering.** The proposed pilot requires issuer counsel, compliance, partner, security, and operational approvals before any regulated workflow can be enabled.

## Pilot boundaries

- One US issuer or counsel-approved deal-specific entity and one Rule 506(c) offering.
- Accredited purchaser verification and issuer reliance evidence are required; self-attestation alone never enables a purchase.
- USD settlement is handled by approved bank or escrow partners. The platform does not hold investor funds.
- The issuer or appointed transfer agent's legal register remains authoritative for ownership.
- Live marketing, subscription acceptance, funding, ownership changes, and token issuance remain disabled until their required release gates are approved.
- Onchain representation is optional post-pilot work, separately gated by legal, transfer-agent, security, and audit approvals.

## Project plan

- [Product requirements and architecture](docs/PRD_HLD_LLD_506c.md)
- [Milestones M0–M9](planning/milestones_506c.csv)
- [Engineering backlog](planning/backlog_506c.csv)
- [ADR-013: 506(c) pilot](docs/adr/ADR-013-506c-pilot.md)
- [ADR-014: first-sale timestamp](docs/adr/ADR-014-sale-time.md)
- [ADR-015: optional onchain representation](docs/adr/ADR-015-onchain-optional.md)
- [Developer writing guide](.github/skills/developer-writing/SKILL.md)

Roadmap dates are planning estimates, not commitments or evidence of legal clearance. Resolve counsel and issuer decisions before implementing tasks whose acceptance depends on them. Keep all release gates fail-closed.

## Contribution workflow

Open a focused issue with acceptance criteria, dependencies, and relevant requirement or ADR references. Create a branch from the latest `main`, implement only that issue, and open a regular pull request against `main` that closes the issue. Merge by squash only after applicable validation and required CI pass. Keep blocked or unverified pull requests open.

Use Conventional Commits and follow the [developer writing guide](.github/skills/developer-writing/SKILL.md). For changes involving compliance, payments, ownership, or contracts, document the threat-model impact, migration and rollback plan, test evidence, and risk classification.
