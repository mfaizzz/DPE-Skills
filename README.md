# DPE Skills

Faiz Ibrahim's combined skill library for engineering, data platforms, reviews, documentation and product work. One trigger selects relevant domain skills, applies scoped output-quality checks and validates the requested outcome with evidence.

```text
DPE Skills: review this Snowflake and ADF migration end to end.
DPE Skills: improve this design document without changing its structure.
DPE Skills: debug this pipeline and preserve the current file contract.
```

The superset retains all 422 skill directories from the prior library, refreshes the six Anti-Slop skills in place under DPE quality names, and adds a dedicated DPE E2E review skill: **423 library skills**, plus the `dpe-skills` entry point. It does not load all skills for every task.

## Install locally for Codex

Requires Python 3.11 or later. No package manager, API key, optional runtime or network call is needed for search, validation or entry installation.

```bash
git clone https://github.com/mfaizzz/DPE-Skills.git
cd DPE-Skills
python3 scripts/dpe.py validate
python3 scripts/dpe.py install
```

Installation copies the entry point and records the checkout's path in `~/.codex/skills/dpe-skills/references/library-root.txt`. It updates only that skill folder, backs up its previous entry files, and does not overwrite global/project AGENTS.md or enable hooks. Keep the checkout in place; rerun install if you move it. Start a new Codex session if its skill catalogue was already loaded. In a checkout-aware session, SKILL.md can also be read directly.

## Discover and validate

```bash
python3 scripts/dpe.py find "Snowflake SQL ADF outbound migration"
python3 scripts/dpe.py find "review this pull request"
python3 scripts/dpe.py validate
python3 -m unittest discover -s tests -v
```

Search returns a primary candidate, relevant matches and proposed quality/E2E complements; inspect their descriptions before loading. It is a local lexical router, not a guarantee of perfect classification. Exact skill IDs are accepted. Optional tools described by individual skills remain optional and are not installed or authenticated by this library.

## What is combined

- Complete prior domain-skill catalogue, with active legacy brand names and cross-references migrated to DPE.
- Current six-skill Anti-Slop suite: core UI filter, UI, copywriting, comments, human/accessibility and responsive layout. DPE removes the first-run/mode wizard and applies relevant quality checks automatically when invoked. UI rules do not govern SQL or documentation formatting.
- DPE working contract and E2E review: current-repository standards, source-to-target parity, environment/identity checks, failure/alert/replay behavior, deployment, rollback and scoped decommission.

The source snapshot is adapted reference material, not an assertion of an employer's official or latest DPE standards. The target repository and approved specifications remain authoritative. An agent must inspect code before running it and respect user permissions. Invoking the skill does not authorize push/deploy/send operations, persistent memory, hooks, tool installation or data transmission.

## Layout

- `SKILL.md`: single entry point and routing rules.
- `skills/`: 423 domain and quality skills with their sidecars.
- `references/dpe/`: shared working, E2E and output-quality contracts.
- `scripts/dpe.py`: dependency-free search, validation and installation.
- `docs/THIRD_PARTY_NOTICES.md`: sources, pinned revisions, licences and adaptation notes.
- `docs/VALIDATION.md`: validation results and known evidence limits.

Inherited source guides and agent contracts are reference material; the supported DPE setup is documented here. The prior distribution's CLI, host plugins, hooks, installers and benchmark logs are intentionally not installed or bundled as executable infrastructure. Skills that describe external CLIs require those tools to be supplied separately; they are never silently enabled.

## Attribution

Maintained and integrated by **Faiz Ibrahim**. Original additions use the root MIT licence. Third-party portions retain their original licences and authorship; see [source and adaptation notices](docs/THIRD_PARTY_NOTICES.md). Active DPE branding does not relabel third-party authorship.
