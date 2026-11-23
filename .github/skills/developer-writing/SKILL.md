# Developer Writing Guide

Use this guide for every issue, branch, commit, pull request, review comment, and engineering document in this repository.

## Commit messages

- Follow Conventional Commits: `type(scope): imperative summary`.
- Keep the subject specific to the change and preferably under 72 characters.
- Use an imperative verb: `feat(policy): add stale evidence denial`.
- Add a short body only when the reason, constraint, or tradeoff is not clear from the subject and diff.
- Keep one logical change per commit. Avoid unrelated formatting and filler such as `update code` or `done`.
- For squash merges, write a meaningful final subject and body based on the actual pull request.

## Issues

Describe the user or system problem, why it matters, and the smallest useful scope. Include:

- Requirement and decision references where applicable (`PRD-xxx`, `ADR-xxx`, and release gate).
- Acceptance criteria that can be checked without interpretation.
- Denial paths, retries, concurrency, privacy, and failure cases relevant to the change.
- Dependencies and the evidence needed for completion.

Do not turn legal or issuer decisions into engineering assumptions. Label unresolved decisions and keep gated behavior disabled.

## Pull requests

Use a concise title that names the change. Explain what changed and why, then identify tests actually run, pending checks, risks, and follow-ups. Link the intended issue with `Closes #N` when the pull request completes it.

Keep the description factual and brief. Do not claim checks passed, approvals were granted, or review occurred unless verified. A ready-for-review pull request is not evidence of approval or passing checks.

## Code and documentation

Use clear, direct language. Explain invariants and non-obvious decisions rather than narrating obvious code. Prefer precise names and examples tied to the actual behavior. Avoid promotional claims, boilerplate, repeated headings, and unsupported performance or compliance statements.

## Before publishing a change

1. Read this guide and inspect the current `main` branch, active pull requests, related issues, and existing implementation.
2. Confirm the work is not duplicated under another name or contract.
3. Review the complete diff for correctness, security, privacy, data migration, rollback, and gate impact.
4. Run only the checks applicable to the change and record their actual outcome.
5. Open a regular pull request against `main`, link the correct issue, and leave it open if a required check is missing or failing.

For compliance, money movement, ownership, and smart-contract changes, include the threat-model impact, relevant requirement/decision IDs, schema or API changes, migration and rollback plan, test evidence, and risk classification. Do not enable a release gate through code alone.
