---
name: dpe-skill-finder
description: Use when no obvious DPE domain skill fits or a cross-domain task needs a small, justified specialist set.
---
# DPE Skill Finder

Locate the library using the installed entry's `references/library-root.txt`, or use the current checkout. Run `python3 scripts/dpe.py find "<the current user task>" --root "<library-root>"` from the checkout, or call the script by absolute path.

Read the returned `primary`, `matches` descriptions and `complements`. These are search candidates, not a directive to load them all. Choose the smallest relevant set and read their returned local paths. Exact IDs and aliases are supported. If the query has no useful match, proceed with ordinary reasoning and name the limitation; do not fabricate a skill or silently download one.

Search once per task and reroute when its scope changes. Apply the shared DPE quality gate, with E2E and visual specialists only where relevant. Skill availability does not imply an optional CLI/provider is installed, a credential is available or an external operation is authorized.
