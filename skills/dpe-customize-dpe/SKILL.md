---
name: dpe-customize-dpe
description: Use when changing the DPE Skills entry point, catalogue, aliases, quality rules or local installation. Verify real supported paths and avoid assuming an inherited host plugin or CLI exists.
---
# Customize DPE Skills

Read the root SKILL.md, README.md and AGENTS.md before changing the distribution. The supported runtime is [scripts/dpe.py](../../scripts/dpe.py), a dependency-free local search/validate/install helper. Host plugins, inherited automatic-memory CLIs and hooks are not installed by this package.

- Each library skill lives at `skills/<id>/SKILL.md`; its frontmatter name must match the folder and its description must identify actual task triggers.
- Keep aliases in `skills/aliases.json` pointing to existing IDs. Use real descriptions and optional task tags in `scripts/dpe.py` for routing. Do not create duplicate specialists for the same concern.
- Rebuild the discoverable catalogue with `python3 scripts/dpe.py catalog > skills/catalog.json` after skill metadata changes.
- Shared quality, working and E2E contracts live in `references/dpe/`. Keep UI-specific guidance scoped to interfaces; do not make a style preference a universal SQL standard.
- Keep source provenance, original licences and modification records in `docs/THIRD_PARTY_NOTICES.md`. Do not erase third-party authorship during branding changes.
- Run `python3 scripts/dpe.py validate` and `python3 -m unittest discover -s tests -v`. For router changes, test representative domain requests, exact IDs, aliases, missing capabilities and installation boundaries.
- Refresh the selected Codex entry with `python3 scripts/dpe.py install` only when installation is requested. It backs up the previous entry, preserves unrelated files and does not enable hooks or overwrite global/project rules.
- Keep a publication review separate from local validation. Inspect the outgoing diff for private artifacts and credentials, and respect the user's current push/publish authorization.

This workflow adapts the previous library-configuration skill to the current DPE package rather than documenting an unbundled legacy runtime.
