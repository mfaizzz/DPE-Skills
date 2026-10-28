# DPE E2E review

Apply to substantive systems/data changes, migrations and implementation reviews. Scale depth to the task. Mark non-applicable gates with a reason; do not impose a production migration checklist on a simple copy edit.

## Trace the path

Map source -> extraction -> intermediate storage -> orchestration -> delivery/target -> consumer. Record actual object names, repositories, environment bindings, service identities and dependencies. The user-nominated legacy package is the primary behavioral reference for a migration; document conflicts with newer specifications rather than guessing. Package filenames do not establish deployed SQL Agent job names, schedule overrides or runtime folders.

## Required checks when relevant

| Gate | Verify | Evidence |
|---|---|---|
| Contract | Procedure signature, fields/order, keys, types, filenames, paths, delimiter/quoting, encoding, nulls and line endings | Current source, generated output and approved specification |
| Correctness | Counts and values, duplicate multiplicity, missing/extra rows, empty/NULL cases, boundaries and regional identity keys | Meaningful executable checks; snapshots/windows stable enough to reconcile |
| Environment | Exact database/stage/endpoint, role, warehouse/runtime, permissions, grants and secrets reference | Approved binding checks before writes; service identity test |
| Orchestration | Success/failure dependencies, current-run file freshness, overlapping runs, retries and partial delivery | Pipeline definition plus positive and negative runtime tests |
| Operations | Logging/rethrow, failure propagation, notification delivery, monitoring, replay/backfill and retention | Run/query IDs, failed-run evidence, alert receipt and replay outcome |
| Deployment | Object ordering, schema/format/config creation, seed/state migration, CI checks, parameter rendering | Deployable assets and environment-specific validation |
| Cutover | Effective old scheduler/overrides, duplicate prevention, consumer acceptance, observation period | Approved plan and deployed evidence |
| Rollback | Stop new scheduler/transfers, reconcile partial outputs, restore old schedule and state safely | Concrete commands/configurations and rehearsed result where appropriate |
| Cleanup | Callers, shared helpers, legacy tasks, source/state consumers and obsolete files | Dependency review; scope deletion to assets proved unused |

## Data transfer safeguards

When preserving file bytes, use Binary transfer rather than parsing/serializing CSV. Fixed filenames require an all-required-files current-run gate before sending any file; concurrency 1 alone does not prove freshness or idempotency. Remote existence and nonzero size do not prove field/value or byte parity. Use checksums or compare bytes where supported. An SQL-only script cannot validate ADF/SFTP, consumer ingestion or notifications.

When comparing rows, account for duplicate counts and legitimate serialization/null normalization; hash equality alone has collision limitations. A later source read can differ because the source changed: use a stable window or snapshot. For feedback/queue flows, verify producers, state/watermarks, completion after actual successful unload, regional key uniqueness and retry behavior; creating empty target tables is not migration completion.

## Handover

Record revision/ref and date, scope, checked evidence, status by gate, severity/impact, remaining action and unresolved owner/decision. Label owner/date TBC when unknown. Keep completed evidence separate from pending work. Sign off only the boundary actually validated; local/static PASS never implies production readiness or permission to decommission shared legacy assets.
