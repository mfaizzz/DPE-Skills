---
name: dpe-e2e-review
description: Review end-to-end data/system migrations across source contracts, orchestration, delivery, service identities, monitoring, deployment, rollback and decommission evidence. Use for implementation sign-off or migration readiness.
---
# DPE E2E Review

Read ../../references/dpe/e2e-review.md and apply only relevant gates. Select the actual implementation/domain skill alongside this review. Follow current repository standards and approved specifications rather than treating this personal framework as an official organization standard.

Preserve completed findings and the latest checkpoint. Inspect changed files, affected callers and missing runtime evidence. Separate static checks, user-supplied results, live component tests and live E2E. Report only supported findings with evidence, impact, severity and the smallest remaining action. Do not grant production or legacy-decommission sign-off from isolated component tests.
