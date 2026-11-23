> **Mission** Make professional diligence, responsible onchain participation, and eligible private-market access understandable, auditable, and secure - without implying guaranteed returns.

# Credence Harbor — US Rule 506(c) Accredited-Investor Pilot
## Product Requirements, HLD, LLD and Engineering Delivery Blueprint | v2.0

**Decision baseline v2.0 | 23 November 2026 | US Rule 506(c) accredited-investor pilot | Internal engineering, issuer counsel and compliance review**


---

# Document governance and decision status

| Field | Proposed baseline / status |
| --- | --- |
| Product name | Credence Harbor - working name; trademark, domain, and company clearance outstanding |
| Document ownership | Product lead + principal architect; legal, compliance, security, engineering co-sign required |
| Scope | Public educational content; accredited-investor onboarding; one Reg D 506(c) private placement; issuer/partner-managed payment, legal register and investor servicing |
| Default launch | One US domestic issuer; US-resident accredited purchasers only for pilot; Rule 506(c) offering; single approved issuer + offering; hard-stop until signed go-live |
| Technology choice | Next.js/TypeScript, TypeScript NestJS modular monolith, PostgreSQL, Redis, Kafka/managed bus later, Solidity/Foundry, managed EVM L2 |
| Authority model | Partner transfer agent/issuer register is legal book of record when required; blockchain mirrors or participates as expressly approved |
| Architecture posture | Regulated workflows use fail-closed policy enforcement, PII off-chain, no guaranteed returns, phased chain rollout |
| Review gate | US securities counsel confirms 506(c), issuer/SPV, bad actor, solicitation, broker status, bank/escrow, transfer restrictions, Form D/state notices before live sale |

## How to use this document

This is an engineering build specification. Section 0 is the binding US Rule 506(c) pilot decision. Sections 1-9 define product, legal route and implementation; sections 10-18 cover security, QA, operational readiness and execution. Requirements are identified by PRD-xxx; interfaces and work packages can be converted directly into GitHub epics and tickets. Any requirement marked GATED must not be enabled by a feature flag without signed legal/compliance approval.

# Executive architecture recommendation

Start with an intentionally modular monolith for fast, auditable delivery, not dozens of microservices. Isolate the compliance decision engine, financial ledger, signing/chain execution and ownership reconciliation as separately permissioned boundaries from day one. Separate read-only community functions from the legally regulated investment lifecycle. Do not require blockchain for the R1 live sale; optionally use a single EVM L2 for independently approved and audited R2 token representations. Maintain immutable journal records, idempotent async jobs and an independent reconciliation service. Treat smart contracts as enforcement and transparency components, not substitutes for off-chain legal ownership, bank settlement, identity verification, or fiduciary accountability.

## Review lenses applied

| Lens | Primary checks |
| --- | --- |
| Product | Does each persona achieve a real job without disguised speculation or incentives? |
| Security / formal methods | What can be stolen, frozen, double-issued, replayed, forged, or manipulated? |
| Legal / compliance | What registrations, permissions, offering exemptions, marketing restrictions and recordkeeping apply? |
| Backend / data | Which system is authoritative? How do retries, reorgs, partial settlement and reconciliation work? |
| Smart contract | Are mint/transfer/distribution/pause/recovery gates explicit and testable? |
| Frontend / accessibility | Can a user understand risks, fees, custody, eligibility and states before approving? |
| SRE / FinOps | Can the platform monitor, halt, recover and explain transactions during outages? |
| Abuse / trust & safety | Are incentives resistant to sybil attacks, paid shills and conflicts of interest? |

---


# 0. Binding launch decision, document precedence and change log

**DECISION-506C-001 — selected for pilot:** A US-domestic issuer conducts one Rule 506(c) private offering. During the pilot, only US-resident verified accredited investors or US-organized eligible entities may purchase; non-US persons are refused for investment even where a different offering route might otherwise exist. General solicitation is permitted only for legal/compliance-approved offer material. All securities remain restricted. The application is a technology and servicing layer, not a self-declared broker-dealer, transfer agent, bank, investment adviser or exchange. Actual business activity, compensation and contracts—not a software disclaimer—determine regulatory status.

**Precedence:** The v2 Rule 506(c) launch requirements supersede any illustrative multi-jurisdiction, Reg A, Reg CF, free-trading, platform token, stablecoin or onchain-mint assumptions inherited from v1. The pilot legal route is firm as a *design choice*; legal sufficiency still requires issuer counsel review. V2 marks G0-G5 release gates, not a representation that any approvals have been received.

| Decision | Pilot binding constraint | Deferred alternative |
| --- | --- | --- |
| Offering route | Rule 506(c); all purchasers must be accredited and reasonably verified | Reg 506(b), Reg A, Reg CF, Reg S and foreign offerings need new designs |
| Entity | One US issuer or one US deal-specific SPV subject to entity/fund analysis | Multi-SPV marketplace or pooled evergreen fund |
| Investor | US residents and eligible domestic entities with KYB/UBO rules | Non-US investor onboarding |
| Capital | USD wire/ACH via approved bank/escrow/custody partners; platform does not directly hold investor funds | Stablecoins, FIBO, internal currency and direct wallet funding |
| Ownership | Issuer legal register / agent approved by counsel is authoritative | Token-native definitive shareholder register |
| Smart contracts | Testnet interface and security proof; mainnet issuance OFF at first-sale gate | Audited, permissioned token representation after legal approval |
| Distribution | Issuer-approved general solicitation and offering documents with immutable approval trail | Auto-generated AI investment promotions or referral commissions |
| Recommendations | No personalized recommendations; research is educational and conflict-disclosed | Licensed or otherwise legally supported advisory features |

## 0.1 Evidence-backed US regulatory baseline

- **Rule 506(c):** general solicitation is permitted, but every purchaser must be accredited, issuer must take reasonable verification steps, and Regulation D conditions including Rule 506(d) bad-actor disqualification apply. Restricted securities are not freely resellable. Sources: [SEC-01], [SEC-02], [SEC-03].
- **Verification is not a checkbox:** obtain a dated third-party letter or other defensible evidence with method, source, issuer reliance rationale, risk flags, and transaction-time approval. Nonexclusive methods include prescribed income, net worth and qualifying third-party confirmations; an existing previously verified purchaser may have a distinct representation path. A third-party vendor approval alone is not a transfer of the issuer's responsibility. Sources: [SEC-02], [SEC-04].
- **2025 high-minimum staff no-action:** a facts-specific SEC staff position discusses high investment minimums as a verification factor. It does not create a $100 retail exception or replace counsel's fact-specific analysis. Do not make it the default product verification method. Source: [SEC-05].
- **Form D:** issuer tracks first-sale date as the first irrevocable contractual commitment to invest and files within 15 calendar days; state-specific notice/fees may also apply. Store reminders and evidence, not an unsupported automatic regulator submission. Sources: [SEC-01], [SEC-06].
- **Intermediary status:** transaction-based compensation, investor solicitation, executing transactions, handling funds, or running a trading venue can create broker-dealer registration issues. A licensed placement agent/broker-dealer is a CONDITIONAL dependency determined by counsel and operating model, not an automatic Reg D rule. Source: [SEC-07].
- **Restrictions:** verify bad actors for required covered persons, prohibited transactions/sanctions as applicable, state notice obligations, fraud/marketing controls, and restrictions on resale. Pooled SPVs may separately require Investment Company Act/adviser analysis. Sources: [SEC-03], [SEC-08], [SEC-09], [SEC-10].

## 0.2 Functional launch boundary (R1 vs R2)

| Surface | R1 controlled accredited pilot | R2 or later |
| --- | --- | --- |
| Public | Issuer-approved education and 506(c) solicitation content, as counsel permits | Multi-issuer rankings / marketing personalization |
| Onboarding | US residency/business formation, identity, sanctions, KYB/UBO, verification provider | Non-US jurisdictions |
| Investor | One deal, full document acknowledgement, e-sign, funding via partner, register-confirmed ownership, statements | Multiple offers, secondary transfers, more currencies |
| Admin | Offering approval, covered-person screening checklist, consent/docs versions, manual cases, alerts, reconciliations, filing deadlines | Automatic multi-issuer deal operations |
| Chain | No required production token; only testnet smart-contract prototype and interface proofs | Permissioned security token, if approved and audited |
| Economics | Contractual investment terms only; portfolio values reported as issuer supplied estimates, clearly labeled | FIBO, stablecoin, redeemable fund receipt |

## 0.3 Pilot assumptions, not legal conclusions

One issuer; a single security class; no investment recommendations; no internal exchange; no proprietary custody; no transaction-based compensation paid to an unregistered platform; no platform-issued securities; pilot currency USD; no non-US investors; one designated escrow/payment partner; subscription may require issuer countersignature before becoming irrevocable. These parameters are conservative implementation choices and must be ratified by counsel. Branding remains provisional.


# 1. Product thesis and non-negotiable constraints

# 1.1 Opportunity

The whitepaper combines four distinct propositions: expert-verified professional social graph (Phi), access credential/reserve-asset concept (FIBO), internal payment unit (Equilibrium), and fractional participation in private ventures (Holdings). The v2 launch authorizes ONLY the US Rule 506(c) accredited-investor workflow; all others are explicitly out of the pilot transaction path. Credence Harbor keeps the user problems - credible due diligence, trustworthy professionals, simpler onboarding and more transparent access - while replacing ambiguous financial claims with enforceable economic and legal definitions.

## 1.2 Design principles

- No guaranteed capital appreciation: never present a schedule, oracle, or admin-set price as an economic price floor; disclosed redemption rights and realizable reserve assets determine what an asset can actually support.

- One wallet is not one person: verified identities, risk decisions and legal beneficial ownership are represented separately from wallet keys; do not put government IDs or sensitive documents on public chains.

- Compliance before marketing and settlement: user eligibility is evaluated per offering, jurisdiction, date, transaction amount, sanctions result and legal route; it is rechecked at settlement and transfers.

- One source of truth per business event: book-of-record investor data remains with the authorized issuer/transfer agent; internal ledger is authoritative for platform entries; onchain balances are independently reconciled.

- Clear separation of duty: issuer, escrow/custodian, broker-dealer/funding portal, transfer agent, compliance provider, auditor and application operator each have explicit contractual and technical roles.

- User safety wins against growth loops: no dark patterns, leaderboard manipulation, opaque expert scoring, yield guarantees, unrestricted referrals to regulated offerings, or algorithmic personalized investment advice by default.

- Progressive decentralization: moderation, personal data and regulatory approvals require controlled services; governance only acquires powers that are legal, understandable and reversible through documented emergency controls.

## 1.3 Explicit non-goals through first regulated release

- Open order-book DEX or peer-to-peer trading of private securities

- Launching a self-issued algorithmic stablecoin or price-appreciation promise

- Global access without per-country legal review

- Synthetic secondary liquidity or unrestricted token transfers

- Autonomous AI investment recommendations or autonomous custody decisions

- Native cross-chain bridging of security tokens

- Using engagement score as legal proof of investor sophistication or accredited status

## 1.4 Proposed brand and product language

| Brand module | User-facing value | Technical boundary |
| --- | --- | --- |
| Harbor Commons | Verified discussions, research, expert attestations | community, content, moderation, proof-of-role |
| Harbor Verify | Identity verification and investor access | identity, KYC/KYB, suitability, policy decision |
| Harbor Treasury | Balances, transaction history and custody visibility | payments, settlement orchestration, journal, reserve proof |
| Harbor Ventures | Eligible private-market offerings and investor servicing | offering, subscription, ownership, distributions |
| Harbor Council | Proposal discussions and scoped governance | off-chain governance and later timelock-led onchain proposals |
| Harbor Pass | Non-financial access/membership credential, optional | nontransferable credential; no redeemability or investment marketing |

> **Brand clearance** Credence Harbor is a working architectural name, not a verified available trademark or domain. Rename the software namespace before public launch if counsel identifies collision risk.

# 2. Personas, journeys, KPIs and product scope

# 2.1 Actors and permission model

| Actor | Goals | Restricted capabilities |
| --- | --- | --- |
| Reader / guest | Read public education, see eligible public disclosures | Cannot invest, claim expertise, or view controlled offering documents |
| Verified member | Connect profile, publish research, follow experts | Cannot inherit financial eligibility from professional reputation |
| Verified subject-matter expert | Publish attributable reports, display credential evidence | Cannot silently edit prior attestations; disclosures required |
| Issuer / venture operator | Post verified company data, manage assigned offering workflow | Cannot self-approve compliance or distributions |
| Verified accredited investor | Verified US identity, reasonable-step accreditation evidence, offering-specific approval, sign, fund, track | NO purchase without fresh SALE_ACCEPT eligibility decision |
| Compliance reviewer | Resolve cases, policies, holds with evidence | No unilateral fund movement or policy deployment |
| Finance / operations | Reconcile payments, create distribution batches | No unilateral mint or custody withdrawal |
| Moderator | Manage abuse, content, appeals | Cannot change KYC or ownership records |
| Auditor / regulator | Read scoped evidence and signed attestations | Least-privilege read access; redacted PII |
| Platform administrator | Configure products and incident control | No omnipotent super-admin; four-eyes approvals |

## 2.2 Golden-path user journeys

1. Discovery: visitor reads a protocol research card with evidence links, disclosures, methodology and freshness timestamp; community votes are not presented as verified facts.

1. Expert: professional submits credentials to vendor, receives expiring role attestation, publishes signed analysis, discloses compensation/conflicts; moderators can revoke displayed verification.

1. Member: creates passkey-enabled account, links optional wallet with SIWE-like signed challenge and consent, controls privacy; membership does not require buying any platform asset.

1. Investor: sees eligibility disclaimer, begins KYC/KYB, sanctions/PEP and jurisdiction review, verifies accreditation when required; offering tiles are conditionally hidden or restricted.

1. Subscription: reads risk memo and offering documents, passes amount/eligibility checks, executes subscription agreement, funds escrow through partner, receives authoritative confirmation and then tokenized representation if enabled.

1. Servicing: receives notices, documented NAV/distribution information, payment status, tax documentation through provider; available transfer options respect lockups and legal restrictions.

1. Governance: discusses proposal, votes on community scope; regulated contracts and customer funds are not subject to unconstrained community voting.

## 2.3 Success metrics and guardrails

| Measure | Initial target / instrumentation | Red-line guardrail |
| --- | --- | --- |
| Activation | >=60% of verified members complete 3 meaningful actions in 14 days; cohort metric | Never reward speculative trades or guaranteed profit expectations |
| Expert quality | >=80% of high-impact reports have citations + disclosures + reviewer metadata | Paid endorsements always marked; no paid verification decisions |
| KYC completion | >=70% of eligible applicants complete with provider, excluding intentional declines | No compliance bypass to improve conversion |
| Ledger accuracy | 100% daily bank/custody/platform/onchain reconciled or open explained exceptions | Unreconciled movement triggers hold and escalation |
| Security | 0 critical unremediated contract findings at production gate | No production issuance if audit exceptions remain |
| Reliability | 99.9% app read SLA, 99.95% settlement monitoring target (measured separately) | Safety may intentionally stop issuance and settlement |
| User comprehension | >=90% pass plain-language risk/fee comprehension prompt in usability testing | No inaccurate display of stable or guaranteed returns |

## 2.4 Phased feature requirements — Reg D 506(c) superseding matrix

| ID | P | Deliverable / BE-FE-SC | Acceptance and release gate |
| --- | --- | --- | --- |
| PRD-001 | P0 | Web account with passkeys/MFA; verified session and wallet link optional | Recovery and anti-replay, staff step-up; G1 |
| PRD-002 | P0 | Privacy & consent, per-investor entity profile | Data minimization, retention schedule and audit; G1 |
| PRD-003 | P0 | Expert badges and disclosures, educational Commons | No accreditation inferred from reputation; G2 |
| PRD-004 | P0 | Versioned public research and moderation | Paid conflict label, archival correction trail; G2 |
| PRD-005 | P0 | Human-approved issuer general-solicitation asset registry | No publication without active signed marketing approval; G2 |
| PRD-006 | P0 | KYC/KYB + sanctions + US residency evidence | Provider + human review, source hashes, deny/review paths; G3 |
| PRD-007 | P0 | Reasonable-step accreditation verification | Method-specific proof, issuer reliance, transaction-time checks; G3 |
| PRD-008 | P0 | Rule 506(d) covered-person screening workbench | Signed responsible-person roster and periodic refresh; G2 |
| PRD-009 | P0 | One 506(c) offering with issuer/SPV docs and immutable versioning | Legal counsel approved offer, minimum/cap, controlled amendments; G2 |
| PRD-010 | P0 | Eligibility Policy Decision Point (PDP) | Action-specific fail-closed decisions on intent/sign/accept/issue; G3 |
| PRD-011 | P0 | Version-bound e-sign/acknowledgment and countersign | Consent evidence with document hash and definitive sale timestamp; G4 |
| PRD-012 | P0 | Idempotent reservation + subscription acceptance saga | Prevent duplicate allotments and stale eligibility; G4 |
| PRD-013 | P0 | Partner-hosted USD funding and refund handling | No platform custody, provider webhook + statement reconciliation; G4 |
| PRD-014 | P0 | Immutable double-entry financial subledger and exception queue | Reconcile provider to internal, no negative entitlement; G4 |
| PRD-015 | P0 | Issuer/registrar legal holder and investor statement integration | Legal book of record ack drives portfolio completed status; G4 |
| PRD-016 | P0 | Form D, state notice, marketing and complaint evidence records | Filing tasks/owners/deadlines/receipts; G4 |
| PRD-017 | P0 | Admin separation of duties, immutable audit, case management | No creator self-approval, scoped roles; G3 |
| PRD-018 | P0 | Investor account/portfolio dashboard | Display illiquidity, restricted status, record provenance, no fictitious price; G4 |
| PRD-019 | P0 | Partner simulation + failure and incident runbooks | Duplicates/timeouts/holds/refunds tested; G4 |
| PRD-020 | P1 | Permissioned ERC-3643-based security representation | Counsel + agent design, audit, register ack before mint; G5 |
| PRD-021 | P1 | EIP-712 issuance auth, indexer/finality/reorg recovery | No replay, supply cap, pause and cross-system reconciliation; G5 |
| PRD-022 | P2 | Distribution management via partner | Issuer-approved payables, tax review and holder record date; NEW GATE |
| PRD-023 | P2 | AI research assistants | Citation fidelity/human approve, no personalized buy/sell; NEW GATE |
| PRD-024 | P2 | FIBO/Equilibrium/governance/DEX/cross-chain | Explicitly disabled; separate future product/legal review |

**Investor qualification invariant:** Self-attestation may be collected as a supporting input but is never sufficient alone for the pilot's initial Rule 506(c) verification. A durable, auditable decision must reference the actual proof method and issuer-approved reliance assessment. Identity verification ≠ accreditation verification ≠ subscription acceptance.

# 3. US Regulation D 506(c): legal, economic and compliance architecture

## 3.1 Offering route, boundaries and issuers

The pilot selects **Rule 506(c)** for one US issuer or one deal-specific SPV. All purchasers are accredited investors with reasonable steps to verify at/before the irrevocable purchase commitment. Marketing materials may be publicly accessible after issuer/counsel approval. A public offer webpage does not permit public checkout. Regardless of statutory exemption, federal and state antifraud rules apply. Rule 506(d) covered-person checks, resale restrictions and required regulatory notices are non-negotiable. The single issuer/deal does not imply that an SPV is automatically outside fund/adviser rules.

| Checkpoint | Owner / authority | Evidence and software requirement | Fail state |
| --- | --- | --- | --- |
| Issuer + SPV structure, asset type | Issuer counsel | Entity documents, board approvals, securities/opinion memo, route classification | unpublished |
| Intermediary / broker-dealer necessity | Securities counsel + operator | Written functional/compensation analysis; partner agreement if required | no solicitation/acceptance |
| Rule 506(d) screening | Issuer counsel/compliance | Covered-person roster, underlying decisions, remediation/waiver if any, review time | block offering |
| Solicitation content | Issuer+legal+compliance reviewers | Versioned approval, risk statements, audience/channels, withdrawal and complaints | not public |
| KYC/KYB + OFAC/sanctions | Compliance owner and relevant partners | Verified identity/UBO, restrictions/false-positive reviews, adverse-case record | review/deny |
| Accreditation | Issuer reliance decision + specialist vendor | Dated verification method/evidence reference, adverse indicators, recheck at sale | review/deny |
| Offering eligibility | Policy service | Issuer/security ID, residence, risk, allocation, amount, verification, docs | fail closed |
| Investment agreement | Issuer/registered partner if applicable | Final doc version and investor signature; first irrevocable contract date | cannot finalize |
| Money movement | Bank/escrow/partner | Source-of-funds policies, designated accounts, immutable settlement reference | no holdings |
| Beneficial/legal ownership | Issuer holder register / authorized transfer agent | Confirmed acceptance, securities units, legal entity/holder identity | portfolio pending |
| Filings | Issuer counsel | Form D deadline from first sale, state notices, receipts and updates | compliance escalation |

## 3.2 Accredited verification: policy model, method and evidence

**Initial R1 methods:** independent accredited verification provider and, subject to counsel's evidence policy, document-based or qualifying third-party written confirmation. SEC permits multiple nonexclusive methods and a specific previously-verified purchaser representation route; policies must represent the correct rule rather than inventing a universal 90-day legal expiration. Store method_code, jurisdiction, vendor, evidence_hash, issued_at, verification_completed_at, source_as_of, last_adverse_check_at, policy_recheck_due_at (internal), investor_category, issuer_reliance_signed_at, related_subscriptions and supersession status. Raw tax/bank documents should ordinarily remain with the specialist provider; platform stores only encrypted references and minimal decisions.

| Method | Evidence to capture | Preconditions | Policy |
| --- | --- | --- | --- |
| QUALIFIED_THIRD_PARTY | Dated written confirmation from qualified BD, SEC-registered IA, attorney or CPA with prescribed assertions | Check qualification, issuance date, relationship and identity binding | counsel-configured temporal check |
| INCOME_RECORDS | Specified IRS forms and expectation evidence | Secure vendor review, permitted-year coverage | counsel-approved |
| NET_WORTH_RECORDS | Financial records and credit report + investor representation | Applicable documentation dating and liability consideration | counsel-approved |
| PRIOR_VERIFIED_REPRESENTATION | Historical reasonable-step evidence + fresh purchaser rep | No known contrary information; 506(c) conditions satisfied | separate route, not a blanket extension |
| PRINCIPLES_BASED | Documentary/vendor dossier and rationale | Facts-and-circumstances objectively support reasonable steps | explicit reviewer+issuer approval |
| HIGH_MINIMUM_NAL | As described in 2025 staff letter | Not chosen for R1; counsel fact-specific written approval required | DISABLED default |

**No verification shortcut:** UI `selfAttested=true`, possession of a wallet, reputation badges, staking FIBO, subscription >= $100, and third-party KYC do not count as automatic Rule 506(c) accredited verification.

## 3.3 KYC/KYB, sanctions, legal identity and jurisdiction

US-resident natural persons and US-organized entities only (a restrictive pilot product choice). Capture residency and identity evidence, tax classification/W-9 workflow if required by partners, entity formation/authority/UBO data for KYB, sanctions matches and disposition, approved bank account owner, and investor-to-legal-holder mapping. Geolocation/IP cannot be sole proof of US eligibility. Screen on onboarding and immediately before sale, and continuously or event-driven as directed by the approved partner policy. PEP is risk-based review, not automatic legal disqualification. Required AML program ownership depends on each participating entity's actual activities and regulations. No raw SSN, tax returns or passports in smart contracts or product analytics.

## 3.4 Action-level policy as code

Evaluate `VIEW_RESTRICTED_DOCS` (policy choice), `CREATE_INTENT`, `SIGN`, `ACCEPT_SALE`, `ISSUE_SECURITY`, `TRANSFER_SECURITY`, and `DISTRIBUTE`. Public display of approved 506(c) solicitation is a separate `PUBLISH_MARKETING_ASSET` action, not gated by accreditation. Backend access control never relies on the frontend. The **ACCEPT_SALE** decision must verify accredited status, issuer reliance, identity, jurisdiction, sanctions, offering state, issuer allocation cap, securities class, material docs version, and lack of outstanding adverse flags; it records policy_version and evidence_set_hash.

```typescript
function evaluate506cSale(x: SaleContext): Decision {
  if (x.offering.exemption !== 'REG_D_506C' || x.offering.state !== 'OPEN') return deny('OFFERING_UNAVAILABLE');
  if (!x.issuer.badActorScreeningApproved || !x.issuer.marketingApproved) return deny('ISSUER_HOLD');
  if (!x.investor.usResidencyVerified || !x.investor.identityCleared || !x.investor.sanctionsCleared) return review('IDENTITY_OR_SANCTIONS');
  if (!x.accreditation.isVerified || !x.accreditation.issuerRelianceApproved || x.accreditation.hasAdverseInformation) return review('ACCREDITATION_EVIDENCE');
  if (x.docs.hash !== x.signedAgreement.docsHash || !x.signedAgreement.isValid) return deny('DOCUMENT_VERSION_CHANGED');
  if (!x.capacity.canAccept(x.amountMinor) || !x.bankAccount.ownerMatch) return review('ALLOCATION_OR_FUNDS');
  return allow({ policyVersion: x.policyVersion, evidenceHash: x.evidenceSetHash, maxAgeSeconds: 60 });
}
// Always execute with a DB lock/atomic capacity reservation and append-only decision log;
// final irrevocable acceptance is a distinct, authorized transition.
```

## 3.5 Marketing, issuer placement activities and Rule 506(d)

General solicitation may occur, but all public communications require issuer/legal approval of the exact asset, material risk disclosures, permissible claims, version hash, effective dates, campaign audience, and withdrawal/kill switch. Capture impressions/distribution channel evidence to reconstruct who saw which version if necessary. Avoid performance promises, fake expert endorsements, paid solicitation by unregistered persons, referral bounties tied to securities sales and AI-personalized advice. Legal counsel must decide whether a registered broker-dealer/placement agent is required for the actual platform activities and compensation; if involved, contract for KYC/AML division of responsibility and any applicable FINRA filing/reporting obligations. Do not assume all Rule 506(c) issuances legally require a broker-dealer; do not assume a technology-only label removes broker risk.

## 3.6 Filings and regulatory clock

Once the first investor is irrevocably contractually committed (which may differ from funding/issuer countersignature under agreements), create an `OfferingFirstSaleRecorded` event and a **Form D base due = first sale + 15 calendar days (move to next business day if the calculated date is a Saturday, Sunday or US holiday)** task, with human legal ownership and SEC/EDGAR proof-of-filing reference. State notice/fee obligations have separate state-specific deadlines and start triggers; do not hard-code them to 15 days. Support amended Form D tasks as counsel determines. Records have immutable audit and evidence export; the platform must not claim filings are submitted merely because a task is created.

## 3.7 Fund, ownership and securities restrictions

Use a partner-managed USD escrow/payment channel. Only verified provider settlement makes `FUNDED`, and only issuer/transfer-agent register confirmation makes `OWNERSHIP_RECORDED`. Model subscription rescission/refund, rejected wires, under/overfunding, chargeback/ACH returns and stale issuer acceptance. Restricted securities are not free-trading; do not launch peer-to-peer securities swaps, order books or secondary transfer endpoints. Rule 144 or another valid transfer exemption and any issuer/TA consent would need separate legal verification if secondary transfer is introduced. FIBO and Equilibrium are outside R1.

## 3.8 Audit retention and privacy decisions

Define a retention matrix jointly with issuer counsel, service providers and applicable federal/state law. Preserve issuer representations, verification method, timestamped evidence/rationale, Rule 506(d) screenings, content approvals, signatures, payment records, investor confirmations, complaints, filing receipts, sanctions dispositions and audit trail. Raw PII/tokenized vendor refs have distinct access/retention and deletion rules; statutory retention overrides a simple erase request. Evidence packages must be exportable with hash manifest and operator attribution.

## 3.9 Responsibility, authority and partner contracts

| Party | Owns | API integration / evidence |
| --- | --- | --- |
| Issuer and counsel | Offering exemption, 506(d), approved disclosures, acceptance, filings, holder legal rights | Dual approved issuer config, signoff and document hash |
| Credence platform | UI/UX, access controls, workflow ledger, technical audit and case queue | No direct investor fund custody or fee-for-sale compensation in R1 |
| Verification specialist | Collect/review accreditation documentation where delegated | Signed verification attestation, method, dated proof reference |
| Identity/sanctions specialist | Identity and matching signals | Signed case refs; manual decisions with evidence |
| Placement agent/BD if required | Regulated solicitation/execution duties within agreement | Partner transaction ack, compensation and FINRA obligations as applicable |
| Bank/escrow/fund movement partner | USD fund custody/receipt/refund | Hosted instructions, statement, authoritative transfer IDs |
| Issuer register/TA if appointed | Holder register, transfer restrictions, issuance records | Signed position ack and versioned statements |
| Auditor/legal operations | Ledger reconciliations, filing tasks, escalation | Export bundles, exception timeline, responsible approvals |

> **Stop-ship:** G0 legal signoff is required before the app may market an actual security; G4 completed partner sandbox and issuer signoff is required before any real irrevocable sale. The issuer and professional advisors—not this draft—make the legal determinations.

# 4. System context and bounded domains

![506(c) system context and external providers](credence_506c_assets/01_506c_context.png)

## 4.1 Domain ownership and anti-corruption boundaries

| Bounded context | Responsibilities | Not permitted to own |
| --- | --- | --- |
| Identity | Account, wallet links, consent, sessions | Raw passport files, legal ownership |
| Reputation | Professional credentials, reputation evidence, publication claims | Accredited status, ability to sell securities |
| Research & Community | Posts, reports, comments, moderation, discoverability | Regulatory recommendations disguised as personalized advice |
| Compliance | Case workflows, policies, eligibility, sanctions decision references | Customer money movement or final legal holder record |
| Offerings | Issuer due diligence, offering room, terms, risk docs, versioning | Custody of investor funds |
| Subscriptions | Intent, agreement, cap table sync, state machine | Mint before finalized payment and authorized confirmation |
| Treasury & Ledger | Journal, refunds, reconciliation, external balances | Unilateral reserve valuation or fabricated onchain settlement |
| Chain Gateway | RPC, signed transactions, events, finality, mint authorizations | Sensitive KYC document storage |
| Governance | Proposals, discussion, votes, bounded permissions | Ability to rewrite balances or override securities law |
| Observability / Audit | Immutable log, metrics, incidents, evidence export | Authorization to change prior business events |

## 4.2 HLD: service topology and trust boundaries

![506(c) high-level system architecture](credence_506c_assets/02_506c_hld.png)

## 4.3 Recommended initial deployable architecture

One TypeScript NestJS modular monolith hosts identity, community, research, offering metadata, case orchestration and public APIs with explicit module interfaces. Compliance decision service, financial journal/reconciliation workers and chain transaction signer run as distinct deployments and database credentials. The backend-for-frontend (BFF) exposes scoped screen aggregates. Asynchronous outbox events persist in the same database transaction as business state; dispatch to managed queue. Use Kafka only when sustained throughput or multi-consumer replay warrants it. A service split needs evidence of separate scaling, failure-domain or access-control needs, not fashion.

## 4.4 Deployment baseline

| Layer | Default | Requirements |
| --- | --- | --- |
| Frontend | Next.js + React + TypeScript + TanStack Query | SSR accessible public pages, CSP, consent controls, no secret handling |
| Identity | OIDC provider + passkeys/WebAuthn; SIWE wallet link | MFA for staff, short sessions, refresh rotation, step-up for financial acts |
| API | NestJS / OpenAPI + Zod/class-validator | Contract-first OpenAPI, versioning, rate limits, deterministic error envelope |
| State | PostgreSQL 16+ / PITR; managed Redis | Tenant and row-security strategy, append-only journal, encryption |
| Events | Transactional outbox -> SQS/managed broker | At-least-once, dedupe, DLQ, replay testing |
| Blockchain (R2 optional only) | Solidity + Foundry + reviewed OpenZeppelin/permissioned token components | OFF for R1; G5 legal/custody/audit authorization required |
| Infrastructure | AWS or equivalent, IaC Terraform, Kubernetes optional | Isolated accounts, KMS/HSM, secrets, GitHub Actions, SBOM |
| Observability | OpenTelemetry, Prometheus/Grafana, SIEM | PII redaction, tracing, runbooks, cardinality control |

---

# 5. Frontend specification and experience architecture

## 5.1 Navigation information architecture

![Figure: Frontend navigation surfaces and permissioned consoles](credence_assets/03_ia.png)

## 5.2 Rule 506(c) frontend screens and accessibility states

![Reg D frontend and actor surfaces](credence_506c_assets/03_506c_frontend.png)

| Route | Audience | State / UX obligations |
| --- | --- | --- |
| `/` and `/research` | Public | Educational claims, conflict disclosures and no implied yield or insurance |
| `/offerings/:slug` | Public if approved for 506(c) solicitation | Exact counsel-approved public facts, issuer identity, risk/illiquidity, not a promise of eligibility |
| `/onboarding/us` | Applicant | Verified country/residency and human-friendly unsupported country exit |
| `/verification/identity` | Applicant | Vendor-hosted KYC/KYB, user consent, retries and manual review state |
| `/verification/accreditation` | Applicant | Method disclosure, third-party flow, privacy notice, outcome pending / verified / further-review |
| `/investor/eligibility/:offeringId` | Applicant | Eligibility explanation, evidence recency warning and never a legal guarantee |
| `/offerings/:id/documents` | Eligible investor | Versioned PPM/risks/subscription docs; acknowledgement; download and re-accept |
| `/subscriptions/new` | Eligible investor | Amount, class, minimum/cap, beneficial owner, explicitly irrevocable commitment point |
| `/subscriptions/:id/sign` | Investor | Identity-bound provider e-sign; version hash and separate issuer countersign step |
| `/subscriptions/:id/funding` | Investor | Partner-hosted bank instructions; payable entity verification and fraud notice |
| `/subscriptions/:id/status` | Investor | `SIGNED`, `ACCEPTANCE_PENDING`, `FUNDS_PENDING`, `FUNDED`, `REGISTER_PENDING`, `OWNERSHIP_CONFIRMED` separated |
| `/portfolio` | Holder | Record-as-of, legal security units, restrictions, distributions and partner source; no faux market price |
| `/staff/issuer/offerings` | Issuer authorized | Publish/close workflow only after dual approval and counsel checks |
| `/staff/compliance` | Compliance team | Method-specific verification, holds, sanctions and dual approval evidence |
| `/staff/ops` | Finance/recon | Pending funds/register mismatch, returns, refund, document/export and incident control |
| `/staff/filings` | Issuer legal ops | Rule 506(d) coverage and Form D/state filing countdown + filing evidence |

**Critical FE test states:** self-attested but NOT verified; verified but adverse sanctions; legal docs superseded between viewing and signature; investment below offering minimum; funding-provider timeout; issuer rejection after signature; unexpected return of ACH funds; US resident fails documentary check; public landing not an investment right. WCAG 2.2 AA, non-color-only status, keyboard support, accessible progress timeline and screen-reader-readable risk tables.

## 5.3 User experience rules

- Every financial figure includes currency, decimals, valuation method, as-of timestamp and provenance; portfolio totals label estimated versus confirmed.

- No hidden investment commitment on social click; an explicit, separate regulated funnel starts only when legally permitted.

- Investor-facing status must distinguish application review, approved, reserved, awaiting payment, payment confirmed, ownership recorded, token representation pending, completed, failed and refund pending.

- Display irreversible/expiring actions before wallet signature; decode EIP-712 domain, value and recipient; require step-up on wallet change and large amounts.

- WCAG 2.2 AA target; keyboard navigation, reduced-motion support, contrast, accessible dialog alerts, screen-reader-readable financial tables and localization-ready labels.

- Administrative consoles require explicit actor attribution, batch previews, confirmation, four-eyes approvals and no destructive edits of accounting or investor ownership.

- Handle empty, stale, provider-down, chain-reorg, sanctions-hold, document-version-changed and maintenance states as first-class screen designs.

## 5.4 Frontend component contracts

| Component | Props / interfaces | Mandatory behavior |
| --- | --- | --- |
| EligibilityGate | offeringId, action, decision, expiresAt | Never trust cached allow for execution; recheck server-side |
| IdentityStatus | status, provider, lastReviewedAt, actions | Show user-safe reasons; shield sensitive review metadata |
| OfferingDisclosure | documentVersion, riskCategories, acknowledgment | Require re-acceptance on material revision |
| MoneyAmount | minorUnits, currencyCode, pricingAsOf | Integer precision; never JS floating math for settlement |
| TxTimeline | events[], externalRefs[], lastSyncAt | Differentiate unfinalized and reconciled |
| ExpertBadge | claimId, role, issuer, expiry, revoked | Clickable evidence context; expired badges automatically hidden |
| ResearchEvidence | claims, citations, conflictDisclosure | Version history and contest/flag actions |
| PortfolioHolding | legalUnits, onchainUnits, asOf, exceptions | Disclose mismatches, do not silently merge |

## 5.5 Checkout UX acceptance test

Given a Rule 506(c)-verified US investor on one counsel-approved offering with its configured legal minimum, when they choose an allowed amount, the UI shows legal entity, security type, actual rights, risks of loss and illiquidity, all fees, signed agreement and exact settlement destination. If an eligibility condition becomes invalid before the legally binding acceptance, the action blocks and records a re-review. Funding instructions also require current sanctions and source-of-funds checks under partner policy. If a payment provider returns a timeout, the UI shows pending rather than allowing another payment instruction with a different idempotency key. The UI only labels ownership complete after authoritative register confirmation; chain tokenization may follow separately.


---

# 6. Backend LLD: components, persistence and service contracts

## 6.1 Module dependency rules

Dependencies are directed: identity -> claims; reputation -> identity claims; offering -> issuer and compliance policy; subscription -> offering + compliance + payment + ledger; ownership -> authoritative transfer-agent adapter; chain gateway -> authorized work items. Community must never call ledger writes. Ledger and compliance must not trust community tokens. Modular boundaries use explicit interfaces and internal versioned DTOs. Reconcile webhooks by verified source IDs rather than UI order.

## 6.2 Suggested repository map

```
credence-harbor/
  apps/web              # Next.js public + member + investor app
  apps/admin            # separate staff console deployment
  apps/api              # NestJS modular API + BFF
  services/policy       # compliance PDP, typed policy registry
  services/ledger       # journal + reconciliation + projections
  services/chain        # RPC adapters, indexer, signing worker
  packages/contracts    # Solidity Foundry workspace
  packages/sdk          # generated OpenAPI / ABI client
  packages/domain       # schemas and value-object library
  packages/ui           # accessible design system
  infra/terraform       # IAM, DB, compute, networking, KMS
  docs/adr              # architecture decision records
  docs/specs            # diagrams, runbooks, threat models
  tests/e2e             # cross-boundary acceptance tests
```

## 6.3 Reg D pilot entity map, persistence and constraints

![506(c) data lineage and authority](credence_506c_assets/07_506c_data.png)

| Entity | Required fields | Authority and database constraint |
| --- | --- | --- |
| `issuers` | issuer_id, US entity, legal route approval, counsel_approval_ref | Approval immutable/versioned; issuer cannot self-publish |
| `covered_persons` | person_id, issuer_id, role, screen_status, screen_evidence_hash | Rule 506(d) screened roster with approval and effective period |
| `marketing_assets` | asset_id, offering_id, version_hash, channel, status, approvers | Public only if ACTIVE approval and no kill switch |
| `offerings` | issuer_id, security_class_id, route=`REG_D_506C`, min_usd, cap_usd, documents_version, status | DB CHECK route; issuer not accept own unchecked publication |
| `investors` | user_id, legal_holder_id, US residency result, investor_kind | Investor entity/beneficial holder distinct from wallet identity |
| `identity_cases` | provider_ref, clearance, source, evidence_hash, updated_at | Encrypted; raw PII outside product database |
| `accreditation_checks` | method, vendor_ref, completion_time, issuer_reliance_approved, evidence_hash, status | Attestation cannot be silently rewritten; superseded records preserved |
| `investor_entity_owners` | investor_entity_id, beneficial_owner_ref, controller_role, review_ref | KYB ownership/authority subject to partner policy |
| `policy_decisions` | action, investor, offering, policy_hash, evidence_set_hash, verdict, evaluated_at | Append-only; decision must be checked on `ACCEPT_SALE` |
| `subscriptions` | investor_id, offering_id, amount_minor, status, version, first_sale_at | Scoped idempotency, monotonic transition version |
| `agreements` | subscription, docs_hash, investor_signature_ref, issuer_acceptance_ref, committed_at | Immutable commitment evidence; sign != irrevocable sale automatically |
| `bank_instructions` | subscription, partner_ref, destination_identity, status | Only authorized provider flow; not platform-held bank credentials |
| `settlement_receipts` | partner_tx_ref unique, amount_minor, statement_hash, finality_status | Partner is authoritative for received funds |
| `holder_register_acks` | registrar_ref, holder_id, security_id, unit_count, as_of, signature_hash | Source for legally confirmed portfolio |
| `journal_transactions` | source_id unique, currency, debit_sum, credit_sum | Immutable balanced postings, reversal not mutation |
| `filing_tasks` | form_type, jurisdiction, first_sale_trigger, due_date, receipt_ref, accountable_owner | `COMPLETED` only after recorded external receipt |
| `audit_events` | actor, object, old/new hash, reason, trace, UTC timestamp | Append-only, WORM replicated |
| `chain_issuance_reqs` | optional register_ack, policy_hash, nonce, status | R1 production disabled, R2 audited only |

**Transaction model:** One subscription business transition, its reservation, matching journal operation and outbox event persist atomically in the relevant transactional boundary. No onchain/offchain distributed transaction is treated as atomic. Reconcile by immutable external identifiers. All relevant monetary quantities are integer minor units in USD. Add foreign keys, partial unique indexes and DB-owned no-update permissions; sample DDL is in `db/schema_506c.sql`.

## 6.3.1 Data ownership boundaries

Identity and verification evidence is encrypted and restricted to compliance staff. Financial journal does not receive passport, SSN or income document bytes. Event bus carries tokenized subject IDs and policy decision refs. Legal register is issuer/appointed agent authority; UI portfolio is derived read-model, never issuer-authored from chain alone. A blockchain wallet is optional for v1 pilot and cannot substitute for ownership registration.

## 6.3.2 State transition atomicity and outbox

`createSubscription` uses `(investor_id, offering_id, idempotency_key)` uniqueness and transactional capacity hold. `acceptSale` locks the subscription/approved offering allocation, re-runs PDP with required evidence, records issuer irrevocable acceptance and `first_sale_at` in same DB transaction, atomically emits `offering.first_sale_recorded.v1` iff earliest first sale. Funding and legal register are separate provider-driven transitions. Worker inbox dedupes vendor event IDs and never assumes exactly-once delivery.

## 6.4 Transactions and idempotency

API mutations accept Idempotency-Key and X-Request-ID. Store key hash scoped to authenticated principal, endpoint, offering and payload canonical hash with 24-72 hour TTL for transient requests and effectively permanent dedupe for provider payments, issuer confirmations and chain settlement. Duplicate identical request returns prior response; same key with different payload yields HTTP 409. Do not rely on exactly-once delivery. Use Postgres transaction + outbox row, worker inbox dedupe, bounded retries, DLQ and operator recovery. Reserve balances using explicit ledger postings and TTL, never a boolean in memory.

## 6.5 Financial journal rules

Use immutable double-entry postings per currency, no cross-currency balancing without an explicit FX trade and rate snapshot. Sum debit entries equals sum credit entries for every transaction and currency, all amounts stored in integer minor units or high-precision integer token base units. State changes create reversing entries rather than edits. Separate customer liabilities, escrow, fees, pending funding, revenue, partner receivables, unresolved exceptions and reserves. Service-owned accounts are provisioned from controlled chart-of-accounts with signoff. Financial reporting uses projections from the journal, not UI caches.

```
journal.post({ transactionId, currency: 'USD', entries: [
  { account: 'ESCROW_RECEIVABLE', side: 'DEBIT', amountMinor: 10000 },
  { account: 'INVESTOR_PENDING',  side: 'CREDIT',amountMinor: 10000 }
] })
// When bank/custodian sends definitive settled confirmation:
// post a separate, balanced reclassification transaction.
// A provider timeout never assumes the funds arrived.
```

## 6.6 Consistency and authority matrix

| Event | Source authority | Retry / error policy |
| --- | --- | --- |
| User registration | Identity provider + local user aggregate | Webhooks verify signature; idempotent upsert |
| Compliance approval | Case system with signed policy version | Expire and recheck; no stale allow |
| Bank settlement | Provider settlement ID / statement | Poll fallback, immutable event ingestion |
| Shareholder register | Transfer-agent signed snapshot or API receipt | Reconcile and quarantine conflicts |
| Chain mint | Canonical finalized chain event | Resubmit only with nonce-safe signer and state reconciliation |
| Content publication | Application DB + signed revision hash | Invalidate caches; preserve versions |
| Financial valuation | Issuer/custodian/auditor signed valuation | Age limit + stale badge; never infer from token price |

---

# 7. 506(c) critical sequences, sale semantics and state machines

## 7.1 Investor accreditation and offering eligibility

![Reasonable-step accredited verification and decision DAG](credence_506c_assets/04_506c_eligibility.png)

A verified member may view legally approved public 506(c) solicitation without being accredited; the actual purchase must be gated. Self-certification is a supporting representation, not the required verification standard. Store accreditation provider result + method + evidence reference + issuer reliance reviewer and adverse flag status. Compliance PDP is invoked at creation, signing, issuer acceptance and optional mint. Issuer acceptance is final only when the subscription agreement defines the investor as irrevocably committed.

## 7.2 Subscription -> partner funds -> legal holder

![Primary R1 investment sequence; optional token is separate](credence_506c_assets/05_506c_subscription.png)

1. Public user views approved offer material; version and distribution channel logged.
2. Investor links one legal identity, completes US residence/KYC, reasonable-step accreditation evidence and sanctions screening.
3. Policy authorizes document access and intent; investor reads version-locked PPM/agreement and applicable risks.
4. System reserves capacity and gathers signed investor subscription; no sale marked without defined issuer acceptance/irrevocable commitment.
5. Issuer/partner checks acceptance eligibility at exact irrevocable point and records immutable `first_sale_at` if first sold; filing tasks are triggered.
6. Partner receives USD into designated account and confirms settled receipt. Platform does not receive or possess investor funds.
7. Registrar/issuer records legal holder and security units; portfolio marks ownership confirmed only after definitive acknowledgment.
8. Optional, separately gated post-pilot token representation requires legal/TA consent and audited smart contract; token is never a shortcut for ownership.
9. If funds fail or agreement rejected, use partner-approved hold/release/refund path with immutable reversals and explicit customer communication.

## 7.3 Subscription state machine and authoritative timestamps

| State | Entry authority | Exit / critical invariant |
| --- | --- | --- |
| `DRAFT` | Investor | A browser draft has no investment effect |
| `VERIFYING` | Eligibility service | No move to `READY_TO_SIGN` without verified accredited evidence and US identity |
| `READY_TO_SIGN` | PDP + offering service | Bound to approved material docs version and minimum/capacity |
| `INVESTOR_SIGNED` | E-sign provider | Not necessarily first sale; depends on contract terms |
| `ISSUER_ACCEPTANCE_PENDING` | Subscription service | Revalidate eligibility, issuer authority and available allocation |
| `SALE_ACCEPTED` | Authorized issuer/countersign | `first_sale_at` recorded from irrevocable commitment semantics; immutable evidence |
| `FUNDS_PENDING` | Bank partner | A pending bank status cannot imply receipt; follow counsel/partner sequencing |
| `FUNDS_SETTLED` | Bank statement/provider final receipt | Reflected only after reconciliation |
| `REGISTER_PENDING` | Issuer / registrar adapter | Cannot complete before securityholder record ack |
| `OWNERSHIP_CONFIRMED` | Issuer register / agent | Only now legally confirmed portfolio line |
| `EXCEPTION_REVIEW` | Any workflow validator | Holds, mismatches or adverse information; operator remediation with audit |
| `REFUND_PENDING` | Issuer/finance authorized | Partner-mediated return and reconciled journal reversal |
| `REJECTED` / `CANCELLED` | Issuer or investor per terms | End state; never erase sale evidence if already irrevocable |
| `CLOSED` | Issuer ops | Investor servicing continues on recorded legal position |

**Important:** This is a reference state machine. Parties may require `FUNDS_SETTLED` before issuer acceptance instead; configure event timing according to the signed agreements and partner contract. FIRST SALE remains the first irrevocable contractual commitment, not a guessed payment date or a token mint.

## 7.4 Onchain event ingestion / optional later token

![Onchain issuance only after register acknowledgment](credence_506c_assets/06_506c_chain.png)

Optional chain execution has isolated signer credentials, policy review, signed EIP-712 authority, finalized indexed event and registrar-to-chain reconciliation. A deep reorg, mismatched register balance, disabled issuer or sanctions hold raises an issuance pause. A chain event cannot independently approve legal ownership. Multi-chain bridges and DEX trading remain prohibited in R1 and R2 without fresh legal review.

## 7.5 Failure handling for US pilot

| Injected failure | Expected result | Operator |
| --- | --- | --- |
| KYC passed but accredited self-check only | DENY `ACCEPT_SALE` | Compliance |
| Verification vendor down / adverse info | REVIEW, no manual allow without signed evidence | Compliance + issuer |
| Reg 506(d) screening missing / issuer bad actor | Unpublish offering; halt acceptance | Issuer counsel |
| Signed agreement altered before countersign | Block and re-sign proper version | Issuer / Legal |
| Two acceptSale API calls race last capacity | DB serializes acceptance; one succeeds | BE |
| Partner says funded and bank statement disagrees | Keep pending, exception and no ownership | Finance |
| First sale accepted but filing not yet submitted | Countdown + escalation, legal owner assigned | Issuer counsel |
| Agent rejects shareholder record | Open exception; no token mint, follow refund/repair terms | Registrar ops |
| ACH return after confirmed funding | Freeze servicing as allowed; ledger reversal and legal counsel workflow | Finance/issuer |
| Chain transaction mined but register changed | Hold token publication; refuse duplicate mint, reconcile | SC + registrar |

# 8. Smart contract specification — OPTIONAL post-pilot security representation

## 8.1 Contract release boundary

**R1 production contains zero required smart-contract settlement or token issuance operations.** The US 506(c) private sale, verified investor, partner USD settlement and legal holder register operate entirely without blockchain. In parallel, the SC team delivers testnet restricted series-token proof, fuzz tests, formal invariants and signing controls. The onchain feature flag remains OFF until G5 (issuer legal authority, registrar workflow, approved custody/chain, complete audit and customer disclosures). No FIBO, stablecoin, AMM, private DEX or cross-chain security bridge in the pilot.

## 8.2 Logical topology

![Restricted security token and permission boundary](credence_506c_assets/08_506c_contracts.png)

The permissioned token mirrors a defined beneficial/security position only where legal documents and register permit. `SeriesToken` should use an established ERC-3643 compatible implementation after compatibility review, not pretend that ERC-20 alone enforces securities restrictions. A verifier's result is not published to an open onchain PII registry: allowlist eligibility is expressed as an expiring hashed/attested predicate, with privacy and revocation semantics.

## 8.3 Contract inventory, roles and operations

| Component | Operations | Privilege / non-negotiable checks |
| --- | --- | --- |
| `SeriesToken` | mint/burn, restricted transfer, freeze, transfer events | Issuer/agent-approved operator only; cap, lockup, allowlist, pause |
| `IdentityClaimAdapter` | approved wallet claim, revoke, expiry | Trust only accredited/identity attestations, no raw personal details |
| `ComplianceModule` | canTransfer / canMint, paused policy | Fail closed on stale sanctions/lockup/claim data |
| `IssuanceController` | `mintWithAuthorization` and nonce consume | EIP-712: chainId, contract, series, holder, units, registerAckHash, policyHash, deadline |
| `GovernanceTimelock` / multisig | role changes, pause, upgrades if any | Independent approvers, no issuer-only unlimited admin |
| `RegisterReconciler` (offchain) | compare legal units vs finalized chain units | Hard pause issuance when mismatch; no legal power delegated to chain |
| `DistributionManager` | later record-date claims | OFF R1; separate tax and distribution legal assessment |

## 8.4 Suggested standards and explicit non-uses

ERC-3643 fits permissioned/restricted series *if* approved by counsel/TA. EIP-712 for replay-resistant role-authorized mint orders, EIP-1271 for contract wallets, ERC-4337 only optional UX and not proof of accreditation. OpenZeppelin reviewed access and role libraries with formal test coverage. ERC-4626/7540 vaults, CCIP bridges and public secondary trading are **not required and must not be deployed in the Reg D pilot**.

## 8.5 Illustrative mint authorization

```solidity
struct MintAuthorization {
  bytes32 subscriptionId;
  bytes32 securitySeriesId;
  address beneficiary;
  uint256 units;
  bytes32 legalRegisterAckHash;
  bytes32 policyHash;
  uint64 expiresAt;
  uint256 nonce;
}
// verify typed signature + issuer role + trusted registrar ack + policy + claim freshness
// consumed[digest] == false; supply + units <= cap; pause == false
// atomic consume and mint, emit commitment to subscriptionId
```

**Exception:** No unauthorized forced transfer or recovery; only lawful, case-linked, role-separated correction with event logs. Contract code must not assert that possession of an NFT/token constitutes a legally valid stake unless legal counsel and the issuer register explicitly establish that relationship.

## 8.6 Invariants and executable test strategy

| Proof ID | Safety property | Required verification |
| --- | --- | --- |
| SC-INV-01 | Mint implies valid registrar acknowledgment, live policy, role authorization and approved recipient | Foundry unit + fuzz, model state machine |
| SC-INV-02 | Each `(chain, contract, series, subscription, nonce)` issues at most once | Invariant with concurrent retry/reorg scenarios |
| SC-INV-03 | totalSupply <= authorizedLegalUnits <= seriesCap (within approved token model) | Cross-system reconciliation oracle + fuzz |
| SC-INV-04 | frozen, ineligible or sanctioned wallet cannot receive restricted token | Multi-role transfer fuzz matrix |
| SC-INV-05 | any role rotation/upgrade cannot silently bypass eligibility | Timelock/AccessManager proofs and upgrade regression |
| SC-INV-06 | pause prevents all issuance and transfer paths required by policy | Handler-based Foundry invariants |
| SC-INV-07 | no reserve/stable price promises exist in contracts or UI | Source and integration review |
| SC-INV-08 | reorg never independently triggers second legal issuance | Chain indexer chaos test + registrar comparison |

Delivery: Foundry, Slither, Echidna/Medusa optional, property-based random action sequences, multisig compromise tabletop, external contract audit, critical/high findings closed, signed deployment manifest, two RPC sources, deterministic replay. Formal methods model `eligible -> approved -> legallyRecorded -> signedMint -> consumed` and explicitly prove `minted => legallyRecorded` under trust assumptions; they cannot independently prove partner's real-world register truth.

# 9. API, events, contracts and developer integration

## 9.1 Reg D 506(c) HTTP API — `/v2` contracts

Use OpenAPI 3.1, OIDC+RBAC, RFC 9457 errors, `Idempotency-Key` on mutations, UTC timestamps, no PII leakage, string-encoded integer USD cents, typed `X-Request-ID`, and audit correlation. APIs are *examples*, not live provider-ready endpoints. Full schemas are in `specs/openapi_506c.yaml`. Issuer/staff writes require step-up and dual approval where specified.

| Method and path | Role | Behavior and authorization |
| --- | --- | --- |
| `GET /v2/public/offerings/:id` | Public | Only counsel-approved current 506(c) solicitation projection |
| `GET /v2/public/marketing/:id` | Public | Approved/expiry-checked campaign asset and disclosure evidence |
| `POST /v2/me/verification/identity` | Applicant | Vendor session, encrypted identity ref, consent |
| `POST /v2/me/verification/accreditation` | Applicant | Start approved verification method; never self-approve |
| `GET /v2/me/verification/status` | Applicant | Safe method outcome/state without private reviewer details |
| `GET /v2/me/offering-eligibility/:id` | Applicant | PREVIEW-only policy and obligations; not irrevocable approval |
| `GET /v2/offerings/:id/documents` | Eligible investor | Authoritative docs+hashes+version and read receipt |
| `POST /v2/subscriptions` | Eligible investor | Reserve amount; idempotent create; `202` without a sale claim |
| `POST /v2/subscriptions/:id/signing-session` | Investor | Version-bound e-sign provider session |
| `POST /v2/subscriptions/:id/issuer-acceptance` | Issuer authorized | Recompute policy; record irrevocable commitment and first-sale event |
| `POST /v2/subscriptions/:id/funding-instructions` | Investor | Approved bank partner checkout, no platform-held funds |
| `GET /v2/subscriptions/:id` | Investor/issuer-scoped | Status provenance, exceptions, timestamps |
| `GET /v2/me/portfolio` | Holder | Legal holder register data, no token-derived ownership assumptions |
| `GET /v2/staff/filings` | Legal ops | First sale + Form D/state deadlines and verified receipt |
| `POST /v2/staff/marketing/:id/approve` | Dual authorized | Publish only after two independent approvals |
| `POST /v2/staff/cases/:id/resolve` | Compliance | Reason-coded decision with evidence and separation |
| `POST /v2/webhooks/{provider}` | Partner only | HMAC/mTLS, envelope persist, replay dedupe, no direct mint |

**Example - `POST /v2/subscriptions`:**

```json
{
  "offeringId":"off_506c_001", "investorLegalEntityId":"inv_001",
  "amountMinor":"2500000", "currency":"USD", "termsVersion":7,
  "acknowledgedDocumentHashes":["sha256:a1..."]
}
```

`202` returns `{subscriptionId, status:"VERIFYING", nextAction, requestId}`, with no claim of security allocation or investor accredited status. `409` on idempotency payload mismatch or stale terms, `403` if unauthorized, `422` invalid money/terms, `423` restricted holding state. **No funds or securities move in synchronous public API handler.**

## 9.2 Reg D event catalog and outbox contracts

| Event type | Source and immutable keys | Consumer / control |
| --- | --- | --- |
| `issuer.506c.approved.v1` | issuerId, approvedPolicyHash, counselRef | offering publish gate |
| `issuer.bad_actor_screening.approved.v1` | issuerId, rosterVersion, approvalRefs | publish and sale gate |
| `marketing.asset.approved.v1` | assetId, contentHash, channels, effective/expiry | public delivery projection |
| `investor.identity.cleared.v1` | subjectRef, evidenceRef, caseVersion | PDP, no raw PII |
| `investor.accreditation.verified.v1` | method, completedAt, proofRef, issuerRelianceRef | PDP; separate from identity |
| `eligibility.decision.recorded.v1` | decisionId, action, policyVersion, evidenceHash | audit and subscription |
| `subscription.investor_signed.v1` | subId, docsHash, providerSignatureRef | issuer acceptance queue |
| `subscription.sale_accepted.v1` | subId, committedAt, issuerAcceptanceRef | legal register, Form D calculation |
| `offering.first_sale_recorded.v1` | issuerId, offeringId, firstIrrevocableCommitmentAt | filings task creation (once per offering) |
| `payment.funds_settled.v1` | partner, statementRef, paymentRef, amount | immutable journal posting |
| `register.ownership.confirmed.v1` | securityId, legalHolderId, units, registrarAckHash | portfolio & optional token issuer |
| `filing.form_d.confirmed.v1` | filingId, externalReceiptRef, approvedBy | legal compliance projection |
| `security.token.issued.v1` | chainId, blockHash, txHash, finality, registerAck | OPTIONAL G5, chain reconciliation |
| `reconciliation.exception.opened.v1` | severity, sourceRef, heldAction | ops halt and incident |

**Invariant:** accept-sale decision + signature and issuer legally binding timestamp cannot be constructed from an asynchronous event without the system's authoritative persisted state. Consumer operations are idempotent and replay-safe.

## 9.3 External webhook security

Providers get isolated endpoint credentials and keys, request signing with timestamp skew checks, event replay deduplication, IP allowlisting where feasible, secret rotation, schema validation and durable raw payload hashes. All callbacks first persist with source identity, event ID and signature verdict. They are never direct synchronous instructions to mint or move funds; workers reconcile vendor state by independent API when status ambiguity or high financial impact exists.

## 9.4 Example API payloads

```
POST /v1/subscriptions
Idempotency-Key: 8e31...  (scoped per investor)
{
  "offeringId": "off_001",
  "amountMinor": "10000",
  "currency": "USD",
  "termsVersion": 6,
  "consentDocumentHashes": ["sha256:..."]
}
202 Accepted
{
  "subscriptionId": "sub_001",
  "state": "ELIGIBILITY_PENDING",
  "nextAction": "VERIFY_IDENTITY",
  "requestId": "req_..."
}
// Every monetary field uses stringified integer minor units.
// Client prices are never authorization or valuation sources.
```

## 9.5 Repository acceptance and CI policy

Changes require OWNERS review for compliance, smart contracts and payments. A PR must include threat-model delta, relevant PRD/ADR IDs, OpenAPI/schema diff, migration plan, rollback instructions, unit/fuzz/integration evidence and risk classification. CI: type checks, unit tests, integration tests with provider simulators, deterministic Foundry tests, fuzz corpus, static analysis, secret scanning, license/SBOM, container vulnerability scan, DB migration dry run, preview deploy and signed artifacts. Never deploy new contract permissions from the application CI identity.


---

# 10. Reputation, research and AI intelligence design

## 10.1 Trust score specification

Do not build a single opaque popularity or authority score. Separate identity verification (verified/unverified), role attestations (with issuer and expiry), disclosure compliance, publication evidence quality, domain expertise evidence, correction/retraction record and community feedback. A research ranking model may combine these with explicit weights, but must publish a plain-language explanation and be A/B-tested for fairness and manipulation. No commercial payment changes factual expert badge or sanctions checks.

## 10.2 Reputation components

| Factor | Evidence | Anti-gaming constraint |
| --- | --- | --- |
| Professional claim | Attestation from recognized issuing authority; expiration | Vendor validation + reviewer + revocation |
| Research quality | Source validity, method clarity, citation completeness | Human editorial challenge; no citations laundering |
| Review consistency | Conflict-declared peer review linked to report versions | Reviewer independence and rate-limiting |
| Onchain performance | Chain data only with transparent event derivation | No implied future performance; anti-wash checks |
| Community response | Diverse unique verified contributor feedback | Sybil detection; no engagement-to-investment rewards |
| Corrections | Versioned retractions, reviewer findings | Retraction visible, no deletion of history |

## 10.3 AI agents are advisory, never dispositive

Introduce specialized internal assistant tasks only after reliable evidence pipelines exist: Research Summarizer (citation-grounded), Citation Validator (source and hash check), Risk Extractor (facts/uncertainty), Community Abuse Classifier (flag-only), Offering Document Classifier (extraction with human approval) and Reconciliation Copilot (operator-only proposed explanations). Every AI output includes model/version, source hashes, timestamp, confidence/uncertainty, human approver and trace ID. No model autonomously sets KYC status, accreditation, security classification, distributions, token minting or personal investment advice. Prompt injection defenses separate retrieved text from instructions; tools use read-only scoped credentials by default.

## 10.4 AI evaluation and launch gates

| Test | Measure | Required action on failure |
| --- | --- | --- |
| Citation fidelity | Report fact statements trace to source bytes and date | Hold publication / label unverified |
| Hallucination rate | Expert-labeled blinded review of summaries | Rollback model/rules |
| Bias / manipulation | Counterfactual user and sponsor groups | Audit weights and freeze ranking changes |
| Data leakage | Canary PII tests and secret scan | Block deployment; incident review |
| Tool abuse | Prompt injection and untrusted link evaluation | Restrict execution to allowlisted tools |
| Financial advice boundary | Red-team prompts testing personalized buy/sell tips | Refuse or route to licensed human where required |

## 10.5 Editorial evidence provenance

Each report stores human-readable claims, associated evidence URLs/doc hashes, as-of data time, primary/secondary source class, contributor signature, revision lineage and correction reason. Onchain anchoring is optional and should anchor report digest batches rather than user PII. Complaints and takedown must preserve audit evidence under retention policies while suppressing illegal or harmful public content.


---

# 11. Security, privacy and abuse threat model


## 11.0 Reg D pilot security and fraud-abuse controls

**Threat boundary:** Public investor marketing and private investor onboarding occupy separate trust domains; the existence of a publicly solicited offering never allows anonymous checkout. State-backed authorizations reject forged accreditation payloads, issuer approvals, or delayed OFAC events. Privileged actions require a reason, signed approval and review trace. Financial partner webhooks are evidence, not instructions. Abuse controls include referral/commission checks, influencer/conflict disclosures, source-of-funds anomaly review, account takeover defenses, malicious broker impersonation, forged Form D receipt, PPM version substitution, and fraudulent wire-instruction replacement. Implement change-of-bank-account step-up and a verified call-back policy for redirection attempts.

### 11.0.1 Release-specific attack tests

- Forged `isAccredited` claim; self-attestation only; altered third-party letter; revoked/accreditation adverse status; stale issuer-reliance approval.
- Issuer missing covered-person screening; public marketing asset edited after legal approval; partner referral paid by securities-sales volume.
- US address chosen but foreign residency/KYB conflict; multiple beneficial-holder identities sharing one wallet; sanctioned investor after signature before sale.
- Double capacity reservation under 1000 concurrent attempts; issuer acceptance race with offering close; replayed first-sale event generating duplicate filing deadline.
- Funding instructions replaced via phishing; partner callback valid but amount/currency/owner mismatch; ACH return after registration; attempted silent journal correction.
- Unapproved token mint / chain reorg; two signed issuance instructions for same subscription; user claims chain asset is legal transferable security.


## 11.1 Threat table

| Threat / target | Mitigation | Evidence for release |
| --- | --- | --- |
| Credential stuffing / account takeover | Passkeys, WebAuthn, device/session alerts, rate-limits, staff MFA | Auth pentest + recovery tabletop |
| Malicious wallet signature / phishing | Typed signing preview, domain binding, wallet anomaly signals | Cross-chain replay regression |
| Partner webhook spoofing | HMAC/JWS verification, nonce/timestamp and replay store | Negative integration tests |
| False accreditation / synthetic identity | Verified vendor and reviewer path; fraud signals | Case audit and manual review sampling |
| Offering document tampering | Document version hash, signature binding and WORM archive | Hash mismatch integration tests |
| Oracle / reserve manipulation | Multi-source attestation, independent accounting, age guard | Attestation incident exercise |
| Authorization key compromise | HSM/MPC signing, multisig, scoped roles, time delays, break glass | Key rotation rehearsal |
| Double mint / replay | Consumed digest mapping, legal ack, supply invariant, idempotency | Invariant fuzz + independent audit |
| Reorg or RPC inconsistency | Provider quorum, canonical chain index, finality policy, halt controls | Injected reorg chaos tests |
| Journal corruption / mismatch | Balanced immutable postings, PITR, WORM snapshots, external recon | Reconstruction test + signoff |
| Sybil reputation inflation | Identity-bound moderation, manipulation detection, no financial rewards | Adversarial bot simulation |
| PII exfiltration | Envelope encryption, PII minimization, access policies, DLP logs | Data access review + tabletop |

## 11.2 IAM and data privacy controls

Use least privilege with ABAC plus RBAC and explicit approval rules. Staff actions require WebAuthn step-up, reason and request context. Private data is encrypted in transit and at rest, secrets in KMS/Secrets Manager, production support access is time-boxed and logged. Separate KYC vendor evidence from application records. Assign data processor/controllership responsibilities, data inventory, retention schedules, DSAR export/deletion rules and breach response by geography. Never store government identifiers, biometric templates or sensitive sanctions explanations on public chain, in telemetry, in client analytics or LLM prompts.

## 11.3 Financial incident and stop authority

Define graduated stops: stop new account links, freeze investment intake, stop funding, stop issuance, stop token transfers where law and contract permit, disable cross-chain relay (future), and read-only mode. Halt rights should use distinct roles with independent event logs. Recovery requires incident commander, compliance, legal and engineering acceptance according to severity. Do not allow governance quorum to override emergency legal sanctions controls. Back up immutable storage and rehearsed keys; publish a responsible disclosure process and pre-agreed exploit disclosure timeline.

## 11.4 Non-functional and security targets

| Area | Acceptance objective | Verification |
| --- | --- | --- |
| SLO availability | Read APIs 99.9%, compliance decision service 99.95% target; deliberate safe-stop excluded transparently | SLO dashboards and error budgets |
| Latency | p95 read API <400ms sans partner; p95 eligibility cached safe response <300ms | Load tests at measured target |
| Reliability | Zero missing/duplicate journal postings in fault-injection tests | Model-based event replay |
| Recovery | RPO <=15 minutes, RTO <=2 hours for core app; journal restore with proof | Quarterly restore exercise |
| Privacy | No high-severity user PII leakage / broad staff access | Quarterly role review |
| Security standard | OWASP ASVS 5.0 Level 2 baseline; high-risk transactions additional controls | Requirements traceability spreadsheet |
| Backpressure | Graceful degraded public reads, investment intake fail-closed | Queue + downstream chaos tests |
| Auditability | Trace every investment from identity decision to legal position | Audit sample reproducible end to end |
| Key controls | No single employee can unilaterally issue or transfer customer-held securities | Key ceremony proof + permission matrix |

---

# 12. Infrastructure, environments, observability and DevSecOps

## 12.1 Reference deployment

![Figure: Reference deployment: service isolation, KMS and external counterparties](credence_assets/08_deployment.png)

## 12.2 Environment policy

| Environment | Purpose | Guardrails |
| --- | --- | --- |
| Local | Dev + docker compose + simulated partner APIs | Never use production KYC data or signing keys |
| Dev shared | Automated integration and contract deployments | Synthetic KYC and zero-value transfers |
| Staging | Production-like infra and DR rehearsals | Separate accounts, controlled synthetic personal data, no live customer funds |
| Preprod/canary | Readiness verification with approved restricted datasets | Contract addresses immutable per release; approvals required |
| Production | Audited and approved feature flags, limited jurisdictions | Break-glass procedures, multi-sig, isolation, immutable evidence |

## 12.3 Observability and incident runbooks

- Trace identifiers span UI click, request, policy decision, vendor attempt, journal posting, chain authorization, blockchain tx and ownership confirmation.

- Operational metrics: KYC vendor failure, decision age, pending escrow aging, bank/custody mismatch, orphaned blocks, finality lag, failed mints, idempotency conflicts, rejected document versions, proof-of-reserves age.

- Financial dashboards must expose unmatched settlement, double-entry imbalance (should be impossible), transfer-agent mismatches, chain holder mismatches, and unresolved exception SLA.

- Runbooks: auth outage, provider outage, RPC chain reorg, exposed key, incorrect whitelist rule, payment split-brain, compromised editorial claim, bad contract deployment, backup restoration and customer compensation route.

- SIEM alerts are routed to on-call and compliance according to severity. Mask addresses only when necessary: wallet/public onchain data may be linkable to identified users; access still governed.

## 12.4 Change and rollout controls

Use feature flags scoped by jurisdiction, partner, offering, user tier and read-only versus write actions. Gate all monetary feature launches on recorded test evidence, legal memo reference, vendor contract ID, data protection review, key ceremony, audit signoff and rollback runbook. Deploy migrations with expand-migrate-contract and down-migration analysis. No unreviewed automatic upgrade to issuer-linked token code or policy rules. All releases include changelog and operator briefing.


---

# 13. Engineering ownership, epics and definition of done

## 13.1 Team topology and interfaces

| Workstream | Accountable role | Deliverables / dependencies |
| --- | --- | --- |
| Product + Design | PM / Product designer | PRD stories, UX maps, Figma, accessibility, content + disclosure vocabulary |
| Frontend | FE lead + 2 engineers | Next.js portals, SDK integration, consistent pending/confirmed state |
| Backend Core | BE lead + 2 engineers | Identity/community/offering/subscription API, integration + OpenAPI |
| Financial Systems | BE payments + finance SME | Journal, provider adapters, recon, controlled correction |
| Smart Contracts | SC lead + 1 engineer | ERC-3643 adapter, issuance contracts, tests, deployment roles |
| Compliance / Legal | Compliance officer + counsel | Rulebook, approved jurisdictions/offer types, vendor agreements |
| Security / Formal | Security engineer + external auditor | Threat model, invariant campaign, audit, signer/key reviews |
| DevOps / SRE | Platform engineer | IaC, SLOs, pipeline, DR, monitoring, on-call |
| QA | Automation + domain QA | BDD acceptance suites, chaos, reorg, reconciliation evidence |
| AI / Research (later) | Research lead / ML engineer | Citation-grounded assistants, safety evals, human review tools |

## 13.2 Major epics with deliverables

| Epic | Lead | Deliverable | Release gate |
| --- | --- | --- | --- |
| E-01 Identity & Claims | BE + FE | Login, passkeys, wallet link, profiles, consent | Threat model and account takeover test |
| E-02 Commons & Research | BE + FE | Feed, source-backed reports, moderation, version history | Abuse and claims integrity review |
| E-03 Expert Reputation | BE + risk | Claim issuance/revocation, conflict declarations | Issuer validation and expiry controls |
| E-04 Policy & Case Mgmt | BE + compliance | Decision engine, KYC/KYB adapters, reviewer workflow | Legal rule signoff, evidence and audit export |
| E-05 Offering Room | BE + FE + legal | Issuer data room, document versions, eligibility UI | Content + distribution constraints approval |
| E-06 Subscription Saga | BE + FE | Agreement, reservation, funding, exception states | Cross-system replay tests |
| E-07 Financial Ledger | BE + finance | Balanced journal + reconciliation + partner adapter | Double-entry proofs and restore rehearsal |
| E-08 SC Restricted Issuance | SC | Token, registry, issuance controller, deploy scripts | Audit, invariants, multisig ceremony |
| E-09 Portfolio & Distributions | BE + FE + SC | Legal positions, payout statements, exceptions | Reconcile independent authoritative source |
| E-10 Security & SRE | SRE + security | Production controls, monitoring, runbooks, incident drills | SLO evidence, pen-test closure |
| E-11 Governance | BE + FE + SC | Proposals, community voting, bounded timelock | Governance legal and attack-model signoff |
| E-12 AI research assistant | AI + editorial | Cited summaries, risk extraction, review and audit | Safety eval/PII/prompt-injection gates |

## 13.3 Engineer-ready task template

```
Title: [E-06][BE] Idempotent subscription creation and reservation
Requirement: PRD-009 | Design: ADR-006 | Dependency: E-04 eligibility
Inputs: offeringId, amountMinor, termsVersion, consentDocHashes
Success: 202 with stable subscriptionId and unexpired reservation
Acceptance:
  - duplicate key + same payload returns same ID
  - duplicate key + changed payload returns 409
  - expired KYC denies; user never reaches fund instruction
  - emitted outbox event and DB reservation commit atomically
  - tests include 500 parallel duplicate requests and process crash
Evidence: OpenAPI diff, unit+integration report, trace exemplar,
          migration/backout, security reviewer approval
```

## 13.4 Definition of done across BE, FE and SC

A story is done only when its contract/schema is merged, access control specified, PII handling reviewed, negative cases tested, instrumentation added, docs updated, runbook adjusted if needed, staging evidence captured and owner signs the dependency checklist. Regulated-money or contract stories additionally need legal/compliance acceptance and independent reviewer acknowledgment. No task is done because happy-path local tests passed.


---

# 14. US accredited-investor pilot roadmap, critical path and release gates

**Planning horizon: 40 weeks to an initial controlled live pilot, with weeks 41-52 allocated to post-pilot assurance/optional tokenization.** This is a dependency-based staffing estimate, not a promise of regulatory clearance. Assume 2 FE, 3 BE, 1-2 SC (R2), 1 platform/SRE, QA, designer, PM, dedicated issuer legal/compliance ops, banking/placement-agent liaison, external reviewer. Do not accelerate by removing legal controls.

## 14.1 Workstreams and timeboxed milestones

![Pilot critical path with legally mandatory gates](credence_506c_assets/09_506c_roadmap.png)

| Milestone | Weeks | FE/BE/SC output | Acceptance evidence / gate |
| --- | --- | --- | --- |
| M0 Legal design and operating model | 1-4 | Issuer/SPV, offering model, BD/IA/TA/custody roles, comms policy; domain ADRs | G0 issuer counsel + sponsor approves 506(c), covered-person and business activity model |
| M1 Technical and security foundation | 5-8 | Monorepo, CI, OIDC/passkey, RBAC, audit trail, encryption, IaC, API standard | G1 pen-test baseline, privilege audit, data governance approved |
| M2 Issuer room and public solicitation | 9-12 | Document/CMS approval, disclosures, public offering route, campaign immutable hash, moderation | G2 issuer/legal approve one real offering and communication templates; Rule 506(d) roster |
| M3 Investor verification / policy | 11-18 | KYC/KYB/sanctions/accreditation provider, issuance reliance, manual cases, PDP/eligibility | G3 100% adverse test cases fail closed, evidence export approved |
| M4 Subscription and USD settlement | 17-26 | E-sign, issuer acceptance, capacity, bank escrow hosted funding, ledger, investor status | G4a external sandbox pass; matched partner statements and remediation |
| M5 Registrar and filing operations | 23-30 | Definitive legal ownership acknowledgment, statements, Form D/state clocks/filing evidence, partner SLA | G4b counsel + partner complete first-sale clock and ownership rehearsals |
| M6 Controlled live accredited pilot | 31-36 | 1 issuer / 1 security class, invite-only US purchasers, caps and manual monitoring | G4 live checklist signoff, on-call + rollback/tabletop; actual sale only after clearance |
| M7 Pilot stabilization | 37-40 | Reconciliation, refunds/returns, support, controls evidence, limited operations analytics | 30-day clean recon target, incident drill, no unresolved critical exceptions |
| M8 Optional onchain representation | 28-44 (parallel; launch >= 41) | SC restricted token, EIP-712, attestations, indexer, audit/fuzz/partner proof | G5 full legal+TA+audit approval, zero unapproved mint |
| M9 Broader platform | 45-52+ | Additional issuer and investor services, community AI and governance only via new scoping | New product/marketing/regulatory approval, separate roadmap |

## 14.2 Critical dependency graph

**Mandatory path:** (1) issuer/counsel legal route and operating model -> (2) bank/escrow and BD applicability/partner selection -> (3) security class and PPM/subscription terms -> (4) communications/covered-person approvals -> (5) investor verification and issuer reliance -> (6) e-sign and irrevocable contract definition -> (7) settlement+holder register simulator certifications -> (8) Form D/state notice execution playbook -> (9) controlled live pilot. The OPTIONAL chain lane begins after legal ownership model and does not gate first sale.

## 14.3 Feature flags, environment policy and owner

| Flag | Default | Required enablement |
| --- | --- | --- |
| `506c.public_marketing` | OFF | G2 signed approved content version+distribution channel |
| `506c.investor_kyc` | SANDBOX | G3 security and provider contracts |
| `506c.accreditation_verify` | SANDBOX | G3 verification evidence policy + issuer reliance signoff |
| `506c.create_subscription` | OFF | G4 offer/partner/e-sign sandbox approval |
| `506c.accept_sale` | OFF | G4 issuer, bank, legal, finance, compliance unanimous approval |
| `506c.bank_funding` | OFF | G4 partner production certification; dual approval |
| `506c.register_ownership` | OFF | G4 registrar authorization and reconciliation |
| `506c.form_d_tasks` | ON prelaunch | Counsel-approved first-sale rule and escalation contacts |
| `506c.token_mint` | OFF throughout R1 | G5 counsel+TA+audit+keys+policy review |
| `fibo`, `equilibrium`, `exchange`, `crosschain`, `retail_offerings` | HARD_DISABLED | New program/independent legal and financial review |

## 14.4 Release and compliance signoff gates

**G0 (before marketing):** issuer counsel memo about security, 506(c), integration with other offers, fund/adviser status if SPV, broker-dealer vs tech boundary, who is responsible for Form D/state filings, covered-person due diligence, risk disclosures, entity and security rights. **G1 (platform security):** auth controls, WORM audit, vendor DPA, encryption and breach response. **G2 (marketing):** issuer-approved public text/content hash, 506(d), eligible geographies and staff sponsorship rules. **G3 (investors):** KYC/KYB, method-specific verification, sanctions escalations, issuer reliance evidence, action-level policy tests. **G4 (money and ownership):** issuer agreement irrevocability, reservation/caps, provider sandbox, statement reconciliation, registrar authority, filing timers, refunds and incident drill; no unresolved critical findings. **G5 (chain):** documented legal/token rights, validated ERC-3643 implementation, signer separation, formal invariants, independent audit, deployment attestations, two-RPC indexer and recovery tabletop.

### 14.4.1 Go/No-Go ownership

Product sponsor + issuer executive + US securities counsel + compliance officer + finance owner + engineering/security lead sign the G4 launch sheet. Any one may veto activation. CTO alone cannot enable sale, mint or custody. Evidence is persisted with timestamp, policy hash and identity of approvers; the kill switch can revoke further sale acceptance while preserving customer servicing.

## 14.5 Operational SLOs and validation

- 100% of irrevocably accepted sales have a linked dated accreditation method, evidence, issuer reliance approval, verified identity, sanctions check and exact docs hash.
- 100% of first-sale events open Form D review tasks; actual filings measured against legally determined due date, with receipt attachment.
- 100% of `OWNERSHIP_CONFIRMED` investor positions map to registrar/issuer approved holder record.
- Zero platform-controlled keys permitted to unilaterally withdraw investor funds or mint securities.
- 99.9% read API availability pilot objective; financial acceptance always fail-closed even if uptime declines.
- Daily ledger-to-partner settlement and position-to-register reconciliation; unexplained differences block progression and page ops.
- 30-day observation period with no unresolved critical financial/regulatory breaks before broadening cohort (internal exit target).

# 15. Risks, assumptions, open decisions and exit criteria

## 15.1 Program risk register

| ID / priority | Risk | Treatment / explicit owner |
| --- | --- | --- |
| R-01 CRITICAL | Unregistered securities solicitation/custody or incorrect offering exemption | Legal approves route and intermediary; block transactions by policy |
| R-02 CRITICAL | Artificially guaranteed token floor creating unsupported financial liabilities | Do not implement; independent economics/legal design if revisited |
| R-03 CRITICAL | Onchain token ownership diverges from legal shareholder register | Authoritative TA sync, exception holds, controlled correction protocol |
| R-04 HIGH | Sanctions/KYC outage or provider spoofing | Fail-closed decisions, verified webhooks, vendor failover policies |
| R-05 HIGH | Key compromise permits unauthorized issuance | HSM/multisig, split approval, caps, timelock, monitoring |
| R-06 HIGH | Fractional investors face impossible liquidity expectations | Illiquidity disclosure; transfer restriction and redemption routes explicit |
| R-07 HIGH | Reputation bought/manipulated by issuers and bots | No paid verification, disclosures, evidence and sybil checks |
| R-08 HIGH | Cross-border users bypass geo through VPN | Residency, tax and identity evidence; geo only supplementary |
| R-09 HIGH | Provider accounting delays create payment disputes | Reconciliation aging, idempotency, support escalation |
| R-10 MEDIUM | Vendor lock-in in KYC, TA, escrow and custody | Anti-corruption adapters and contract tests |
| R-11 MEDIUM | Premature microservices overcomplicate audit | Modular monolith baseline; evidence-led split |
| R-12 MEDIUM | Unreliable AI summaries harm investors | Human approval, citations, explicit uncertainty and opt-out |

## 15.2 Architecture decision records (ADRs): v2 accepted additions below supersede v1 proposal statuses

| ADR | Decision | Status |
| --- | --- | --- |
| ADR-001 | Product brand = Credence Harbor; trademark/domain search and rename plan | PROPOSED |
| ADR-002 | US pilot, Reg D 506(c), one issuer/one offering, all buyers verified accredited | SELECTED DESIGN; counsel signoff G0 |
| ADR-003 | Social/reputation are independent of investment eligibility | ACCEPTED DESIGN PRINCIPLE |
| ADR-004 | No guaranteed-price or yield product in MVP | ACCEPTED DESIGN PRINCIPLE |
| ADR-005 | Legal register or transfer-agent record is authoritative | REQUIRES PARTNER CONFIRMATION |
| ADR-006 | Modular monolith core + isolated policy/ledger/signer boundaries | PROPOSED |
| ADR-007 | No onchain issuance required in R1; one EVM L2 optional G5 | GATED |
| ADR-008 | Partner-managed USD funding and custody; no platform investor-fund custody | SELECTED DESIGN; partner approval G4 |
| ADR-009 | Optional access pass does not gate necessary investment rights | PROPOSED |
| ADR-010 | Publishing research score is interpretable; no opaque financial advice | ACCEPTED DESIGN PRINCIPLE |
| ADR-011 | Provider reconciliation is mandatory before irreversible mint | ACCEPTED DESIGN PRINCIPLE |
| ADR-012 | Governance powers exclude financial ownership override | ACCEPTED DESIGN PRINCIPLE |

## 15.3 Remaining decisions and safe engineering defaults

| Open item | Engineering default | Decision authority / deadline |
| --- | --- | --- |
| Exact issuer entity + asset type? | US domestic issuer or single-deal US SPV | Issuer counsel at G0 |
| 506(c) first-sale legal point? | Configurable commitment state; not necessarily funding | Issuer + legal G0/G4 |
| Broker-dealer / placement agent needed? | Do not pay transaction-based commissions or solicit as agent until counsel opinion | US securities counsel G0 |
| Investor type and entity onboarding? | US natural persons only initially; US entity cohorts only after KYB checks | Compliance and partner G3 |
| Minimum offering ticket? | Per-offering; no $100 blanket promise | Issuer/BD/counsel G2 |
| Verification provider/method? | Specialist third-party + signed issuer reliance and alternate reviews | Compliance/issuer counsel G3 |
| KYC/AML responsibilities? | Provider + responsible issuer/intermediary, contract-defined | Counsel + partners G0/G3 |
| Bank/escrow partner? | Partner-issued hosted funding instructions, no direct platform custody | Finance + counsel G4 |
| Register/TA? | Issuer register or authorized TA confirmed by legal | Issuer counsel G0/G4 |
| Onchain network? | No R1 production chain required; one EVM L2 optional G5 | SC/issuer/legal later |
| Marketing channels and approvals? | Only signed materials, publish disabled by default | Issuer counsel G2 |
| State-specific offering/notice obligations? | Per-state compliance rulebook, manually approved due-date rules | Issuer counsel G4 |
| FIBO/Equilibrium/governance? | Excluded and disabled throughout pilot | New program/business case |

## 15.4 Definition of MVP success

The MVP is successful when a visitor can assess a credible expert-backed report, a professional can prove and revoke their credentials, an eligible investor can complete a legally approved end-to-end offering process with externally verified financial settlement and legal ownership, and operators can independently reconstruct the entire lifecycle. The MVP is not successful merely because a token was deployed or a fundraising counter increased.


---

# 16. Test matrices and sample acceptance cases

## 16.1 Integration contract matrix

| Scenario | BE expected | FE expected | SC expected |
| --- | --- | --- | --- |
| Sanctions hold after reservation | Deny funding, preserve evidence and reversible ledger states | Show hold without exposing restricted details | No mint, prevent transfer if relevant |
| Duplicate payment webhook | Dedupe + exactly one journal transaction | One timeline row, no duplicate receipts | No duplicate auth issuance |
| TA ack rejected | Exception + refund/review process | Show ownership not recorded | No mint |
| Expiry before token mint | Refresh policy, reject stale authorization | Show re-verification needed | Revert invalid signature/expiry |
| Unfinalized chain mint reorg | Rollback projection, reconcile external state | Pending -> rechecking | Supply consistency after canonical state |
| User changes linked wallet | Invalidate previous signed auth, step-up approval | Security alert and pending state | Mint bound to latest allowlisted wallet |
| Legal document revision | Invalidate signature and require new acceptance | Show changed terms and delta | Mint condition checks current terms hash |
| Key compromised | Revoke signer via multisig and pause intake | Notify affected users appropriately | Enforce pause and authority rotation |

## 16.2 QA pyramid and load profile

Unit: domain state and policy edge cases; integration: real DB + queue + vendor stubs; contract: ABI and OpenAPI compatibility; E2E: Playwright accessible workflows; SC: Forge unit/fuzz/invariants; nonfunctional: k6/Locust with modeled user distribution; chaos: provider late callbacks, out-of-order events, chain reorg, DB failover, failed secrets rotation. Use stable synthetic users and fixtures; never run capital-moving tests in production without approved kill switches. Load planning baseline, not commitment: 10k daily active users, 100k public report views per day, 1k concurrent sessions, <=100 approved financial subscriptions per day in restricted pilot. Validate cost and latency empirically and revise design when thresholds are exceeded.

## 16.3 Gherkin-style acceptance suite

```
Feature: no issuance before authoritative ownership
  Given a subscription is FUNDED
  And the transfer-agent record is not confirmed
  When a mint request is submitted
  Then the issuance controller does not mint
  And an audit record links the denied request to its legal gate

Feature: duplicate provider settlement
  Given settlement ID P-44 has already been journaled
  When the same signed callback is delivered 200 times
  Then exactly one balanced posting group exists
  And the subscription state is not advanced twice

Feature: expired accredited investor verification
  Given a Reg D 506(c) subscription is READY_TO_SIGN
  And the verified accreditation evidence has expired
  When the investor initiates funding
  Then the system blocks funding with a re-verify next action
  And no partner payment instruction is sent
```

## 16.4 Contract proof obligations / formal-method plan

| Proof obligation | Method | Failure injection |
| --- | --- | --- |
| Single-use issuance | Foundry invariant + symbolic path proof | Duplicate signature / nonce collision / reentrancy |
| Supply limit | Inductive state invariant | Rogue agent / transfer hook / forced transfer |
| Compliance closure | Model checking of transfer state machine | Revocation during transaction, expired claim |
| Distribution conservation | SMT property / fuzz with bounded value | Precision/dust/claim recursion |
| Role non-escalation | Permission reachability graph | Compromised minter and issuer admin |
| Upgrade safety | Storage layout diff / authorization tests | Unauthorized implementation / initializer replay |
| Ledger balance | Property-based state-machine tests | Out-of-order callbacks and double retry |
| External reconciliation | Deterministic replay tests + audit trails | Mismatched share units, missing register statement |

---


# 17. Pilot implementation contracts, QA and compliance traceability

## 17.1 Traceability matrix by responsible actor

| Regulatory objective | FE artifact | BE state/evidence | Partner / legal | SC |
| --- | --- | --- | --- | --- |
| Accredited investor only | Verification step, explicit pending/denied | `accreditation_checks`, PDP `ACCEPT_SALE` | Accredited specialist + issuer acceptance | No token mint |
| Reasonable steps verified | Explain method without exposing PII | Proof metadata, issuer reliance and supporting docs hash | Issuer counsel policy + auditor | Optional claim hash only |
| Approved solicitation | Public approved offer, disclaimers | Asset CMS review and version hash | Issuer/legal/BD when applicable | None |
| Bad actor disqualification | Staff checklist | covered-person roster, case and signing | Counsel screening signoff | None |
| First sale clock | Issuer acceptance and immutable timestamp | `first_sale_at` event, filings tasks and receipts | Counsel legal meaning of irrevocable commitment | None |
| Investor funds safety | Hosted provider checkout + pending UX | payment intents, bank statement recon, ledger | Bank/escrow partner | None |
| Restricted securities | Illiquidity and no transfer CTA | legal holder register + transfer holds | Issuer/registrar counsel | Optional ERC-3643 G5 |
| AML/OFAC | Review and hold state | sanctions provider record + disposition | Obligated partners, counsel risk policy | Fail-closed claim G5 |

## 17.2 Release test suite: adversarial Gherkin

```gherkin
Scenario: Self-attestation is insufficient to accept sale
 Given investor A has completed KYC and checked an accredited investor box
 And no issuer-approved reasonable-step verification exists
 When issuer attempts to accept the subscription
 Then the policy service returns REVIEW ACCREDITATION_EVIDENCE
 And no first-sale clock or legal ownership event is recorded

Scenario: Rule 506(d) hold blocks solicitation and sale
 Given approved public marketing material exists
 When a relevant issuer covered-person screening is placed on HOLD
 Then the public offering transitions to unavailable
 And accept-sale is disabled regardless of cached investor eligibility

Scenario: Irrevocable acceptance starts Form D tracking once
 Given issuer accepts the first subscription according to agreement terms
 When the acceptance webhook is delivered three times
 Then there is one first_sale_at timestamp and one Form D task
 And the due date is calculated 15 calendar days from that timestamp

Scenario: Legal holder record is authoritative
 Given partner reports a settled bank receipt
 And registrar has not acknowledged legal ownership
 Then the portfolio displays register pending, not owned
 And onchain issuance authorizations cannot be executed

Scenario: Marketing update invalidates publication approval
 Given asset hash X has two approvals
 When its actual bytes are changed to hash Y
 Then no content with hash Y can be served as an approved offer
 And marketing must be reviewed and signed again
```

## 17.3 Non-functional release acceptance

Verification evidence lookups must degrade to REVIEW not ALLOW; bank settlement must be recomputable from independently fetched statements; hold and refund workflows must survive process restart; personal data must not appear in application logs, Kafka payloads or public RPC; capacity reservations and investor legal ownership must maintain uniqueness under retry/concurrency; every state-changing request has unique actor/request IDs, hash-linked evidence and reconciled as-of timestamps.

## 17.4 Dated regulatory reference ledger

These sources were checked for design baseline on 23 November 2026. SEC staff letters and guides are not legal advice; laws and staff guidance can change, including 2026 proposals that are not assumed adopted. Counsel must review law, rule text, and the exact offering facts before production.

| Ref | Primary source | Link |
| --- | --- | --- |
| SEC-01 | SEC Rule 506(c) overview (reviewed March 2026) | https://www.sec.gov/resources-small-businesses/exempt-offerings/general-solicitation-rule-506c |
| SEC-02 | SEC Assessing Accredited Investors under Reg D | https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/assessing-accredited-investors-under-regulation-d |
| SEC-03 | SEC 506(d) Bad Actor Disqualification guide | https://www.sec.gov/resources-small-businesses/small-business-compliance-guides/disqualification-felons-other-bad-actors-rule-506-offerings-related-disclosure-requirements |
| SEC-04 | SEC Regulation D verification and methods | https://www.sec.gov/files/general-solicitation-small-entity-compliance-guide.htm |
| SEC-05 | SEC Division of Corporation Finance Latham & Watkins no-action (Mar 2025) | https://www.sec.gov/rules-regulations/no-action-interpretive-exemptive-letters/division-corporation-finance/no-action/latham-watkins-503c-031225 |
| SEC-06 | SEC Filing Form D notice | https://www.sec.gov/resources-small-businesses/exempt-offerings/filing-form-d-notice |
| SEC-07 | SEC Broker-Dealers capital raising overview | https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/broker-dealers |
| SEC-08 | SEC Rule 144 restricted securities | https://www.sec.gov/reports-and-publications/investor-publications/investorpubsrule144htm |
| SEC-09 | OFAC Guidance / FAQ 560 for virtual asset businesses | https://ofac.treasury.gov/faqs/560 |
| SEC-10 | SEC Private Funds / Investment Company Act | https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/private-funds |
| SEC-11 | SEC Transfer Agents, status is activity- and security-specific | https://www.sec.gov/about/divisions-offices/division-trading-markets/transfer-agents |
| SEC-12 | SEC Regulation D C&DIs (2026 guidance) | https://www.sec.gov/rules-regulations/staff-guidance/corporation-finance-interpretations/securities-act-rules |
| FINRA-01 | FINRA 5123 private placement filings; applicability/exemptions determined by member counsel | https://www.finra.org/rules-guidance/rulebooks/finra-rules/5123 |

## 17.5 Engineering deliverable index

`specs/openapi_506c.yaml`, `db/schema_506c.sql`, `contracts/interfaces/I506cIssuanceController.sol`, `planning/milestones_506c.csv`, `planning/backlog_506c.csv`, `docs/diagrams/graphviz/506c_*.dot`, `docs/adr/ADR-013-506c-pilot.md`, `docs/adr/ADR-014-sale-time.md`, and the full updated markdown are included in the starter pack. Scaffolds are design inputs, not deployable regulated services.


# 18. Prior cross-market references and caveats (historical v1 context)

References below support standards and legal design constraints as of 23 November 2026. Regulations vary by offering, country, intermediary and implementation; current legislation and SEC staff statements do not constitute platform-specific approvals. Engineering must obtain current professional advice before making legally operative decisions.

SEC - Regulation D Rule 506(c) - https://www.sec.gov/resources-small-businesses/exempt-offerings/general-solicitation-rule-506c

SEC - Regulation A - https://www.sec.gov/resources-small-businesses/exempt-offerings/regulation

SEC - Regulation Crowdfunding - https://www.sec.gov/resources-small-businesses/exempt-offerings/regulation-crowdfunding

SEC - Statement on Tokenized Securities (Jan 2026) - https://www.sec.gov/newsroom/speeches-statements/corp-fin-statement-tokenized-securities-012826-statement-tokenized-securities

SEC - Crypto asset and DLT Trading and Markets FAQ - https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/frequently-asked-questions-relating-crypto-asset-activities-distributed-ledger-technology

FinCEN - FIN-2019-G001 guidance - https://www.fincen.gov/resources/statutes-regulations/guidance/application-fincens-regulations-certain-business-models

ESMA - Markets in Crypto-Assets (MiCA) - https://www.esma.europa.eu/esmas-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica

FATF - Updated Recommendation 16 - https://www.fatf-gafi.org/content/fatf-gafi/en/publications/Fatfrecommendations/update-Recommendation-16-payment-transparency-june-2025.html

ERC-3643 - T-REX - https://eips.ethereum.org/EIPS/eip-3643

EIP-712 - Typed structured signatures - https://eips.ethereum.org/EIPS/eip-712

ERC-4337 - Account abstraction - https://eips.ethereum.org/EIPS/eip-4337

ERC-4626 - Tokenized vaults - https://eips.ethereum.org/EIPS/eip-4626

ERC-7540 - Asynchronous tokenized vaults - https://eips.ethereum.org/EIPS/eip-7540

OpenZeppelin - AccessManager and timelock - https://docs.openzeppelin.com/contracts/5.x/access-control

NIST - SP 800-63-4 Digital Identity - https://csrc.nist.gov/pubs/sp/800/63/4/final

OWASP - Application Security Verification Standard 5 - https://asvs.owasp.org/

Chainlink - CCIP documentation - https://docs.chain.link/ccip/overview

## Appendix A. Delivery artifacts index (superseded by v2 index in 17.5)

- PRD IDs PRD-001 to PRD-020 are the minimum epic-level traceability identifiers. Detailed tickets should extend as PRD-009-01 etc.

- Keep diagram sources in architecture_diagrams.md; image exports embedded in this document are illustrative build snapshots.

- Maintain ADR files /docs/adr/ADR-001.md ... ADR-012.md with explicit owner/date/impact and revisit triggers.

- API source-of-truth should live under packages/sdk/openapi.yaml; this document is explanatory, not a substitute for machine-enforced schema.

- Maintain financial chart-of-accounts, legal offering documents and eligibility policy files as access-controlled, separately approved artifacts.

- Release scorecard is a continuously updated evidence index, not a marketing launch checklist.

## Appendix B. Ownership and authority invariants

- Never let an onchain wallet address alone prove legal entitlement to an SPV or private company.

- Never let a social badge or community vote prove accredited investor status.

- Never let an admin-set reserve price substitute for a legal redemption obligation and realized backing.

- Never let a transaction hash without chain finality prove irreversible settlement.

- Never allow a single service credential or human to change investor eligibility, escrow settlement and issuance authorization unilaterally.

- Never show independent onchain balances as audited proof of complete reserves and liabilities.

> **End-of-document status (v2)** No live securities marketing, acceptance, payment or tokenization is authorized by this document. The US Rule 506(c) pilot requires signed gates G0-G4, actual provider agreements, specific issuer legal documentation and required filings; tokenization additionally requires G5. Only one 506(c) offering is in the approved engineering target.
