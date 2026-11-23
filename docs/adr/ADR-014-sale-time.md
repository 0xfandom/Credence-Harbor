# ADR-014 — Irrevocable subscription commitment defines first sale

**Status:** requires signed subscription agreement and US securities counsel approval by G4.
**Decision:** Store `legal_commitment_at` separately from investor signature, provider bank receipt and legal holder register. Trigger Form D task once per offering based on earliest irrevocable commitment, whose precise contractual trigger is defined in the final agreement. Use unique index, row locking and transactional outbox. Every correction is appended and counsel-approved; deadlines recomputed with verified evidence, never overwritten silently.

**Verification:** three duplicate issuer callbacks produce one clock; bank receipt without acceptance must not start the clock unless actual contract terms make it irrevocable.
