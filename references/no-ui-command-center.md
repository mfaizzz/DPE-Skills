# dpe No-UI Command Center

dpe does not need a web UI to behave like a command center. The backend layer now stores state, routes models, logs runs, extracts memory candidates, and syncs vector memory through CLI and JSON artifacts.

## Core Loop

1. `dpe run "<task>"`
2. Plan uses the frontier model.
3. Execute uses the lower-cost model unless risk escalation is detected.
4. Audit uses the frontier model.
5. Memory is saved, extracted, approved, and synced into vector DB.

## Commands

```bash
scripts/dpe status
scripts/dpe run "build Laravel subscription module" --tool claude
scripts/dpe runs list
scripts/dpe runs show run_YYYYMMDD_HHMMSS
scripts/dpe memory extract
scripts/dpe memory inbox
scripts/dpe memory approve 1
scripts/dpe memory reject 1
scripts/dpe memory search "postgresql saas decision"
scripts/dpe model route "update payment webhook validation"
scripts/dpe eval latest
```

## Files

- `ai-assistant/runtime/system_state.json` — current command-center state.
- `ai-assistant/runs/*.json` — Plan → Execute → Audit → Memory packets.
- `ai-assistant/memory/inbox.jsonl` — pending memory candidates.
- `ai-assistant/memory/durable-memory.md` — approved permanent memory.
- `ai-assistant/memory/semantic-memory.sqlite3` — local vector memory index.
- `ai-assistant/config/model-router.yaml` — model routing policy.

## Safety

The memory extractor is conservative. It rejects obvious secrets, API keys, `.env` content, bearer tokens, passwords, and private keys before creating memory candidates.

## Cron Example

```cron
0 * * * * cd /path/to/repo && scripts/dpe memory extract >/tmp/dpe-memory-extract.log 2>&1
5 * * * * cd /path/to/repo && python3 ai-assistant/scripts/auto_memory.py sync >/tmp/dpe-memory-sync.log 2>&1
0 3 * * * cd /path/to/repo && scripts/dpe eval latest >/tmp/dpe-eval.log 2>&1
```
