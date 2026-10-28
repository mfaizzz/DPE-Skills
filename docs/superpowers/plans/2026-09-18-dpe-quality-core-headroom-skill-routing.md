# Anti-slop, Headroom, and Skill Routing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install prompt-aware multi-skill routing, anti-slop and Headroom guidance, complete support files, and reliable Windows updates.

**Architecture:** Keep upstream packs immutable, place DPE-specific behavior in the canonical contract and routing index, and make the installer copy the shared files referenced by custom skills. Add tests at the public behavior boundaries before implementation.

**Tech Stack:** Python 3.11+, `unittest`, Markdown Agent Skills, JSON routing index.

**Spec:** `docs/superpowers/specs/2026-09-18-dpe-quality-core-headroom-skill-routing-design.md`

## Global Constraints

- Vendored anti-slop skills remain unchanged from the local upstream checkout.
- Skill selection uses one primary plus the smallest useful complementary stack, with no arbitrary cap for explicit workflow dependencies.
- Headroom provider routing is out of scope.
- User-owned files outside DPE-managed skill directories must not be deleted.
- Every completion claim requires fresh validation evidence.

---

### Task 1: Windows-safe installs and shared references

**Files:**
- Modify: `tests/test_dpe.py`
- Modify: `dpe/skills.py`
- Modify: `dpe/install.py`

**Interfaces:**
- Produces: repeatable `copy_skills_to(...)`, reference paths/counts in `install_user(...)`, and read-only-safe `uninstall_user(...)`.

- [x] Add tests that mark installed files read-only, reinstall/uninstall, and assert success.
- [x] Add tests that assert representative shared references exist under both `.agents/references` and `.claude/references`.
- [x] Run the focused tests and confirm they fail for the expected missing behavior.
- [x] Implement writable tree replacement and merged support-file copying.
- [x] Re-run focused tests and confirm they pass.

### Task 2: Anti-slop and Headroom skills

**Files:**
- Copy: `../anti-slop/skills/*` to `skills/`
- Create: `skills/dpe-headroom/SKILL.md`
- Modify: `skills/vendored.json`
- Modify: `docs/third-party.md`
- Modify: `dpe/index.py`
- Modify: `tests/test_routing.py`

**Interfaces:**
- Produces: six vendored `dpe-quality-core-*` skills, one portable Headroom skill, and prompt routing triggers.

- [x] Add routing and provenance tests for the new skills.
- [x] Run the focused tests and confirm they fail because the skills are absent.
- [x] Vendor the six anti-slop directories unchanged and register provenance.
- [x] Add the concise Headroom skill and curated triggers/roles.
- [x] Rebuild the skill index and re-run focused tests.

### Task 3: Multi-skill contract and quality audit

**Files:**
- Modify: `AGENTS.md`
- Modify: `.cursor/rules/dpe.mdc`
- Modify: `dpe/init_project.py`
- Modify: `dpe/cli.py`
- Modify: `dpe/skills.py`
- Modify: `skills/dpe-taste/SKILL.md`
- Modify: `tests/test_dpe.py`
- Modify: `tests/test_routing.py`

**Interfaces:**
- Produces: compact shared defaults, prompt-aware multi-skill guidance, and `dpe skills audit` JSON/human output.

- [x] Add tests for the managed project contract and the audit report shape.
- [x] Add multi-domain routing cases that require complementary skills in the shortlist.
- [x] Run the tests and confirm the new expectations fail.
- [x] Implement the compact contract, audit report, CLI command, and concise high-traffic metadata.
- [x] Rebuild the index and make the focused tests pass.

### Task 4: Deployment and end-to-end verification

**Files:**
- Modify: `skills/skill-index.json` through the generator only.
- Modify: `CHANGELOG.md`

**Interfaces:**
- Produces: validated repo and refreshed user-level installations.

- [x] Run anti-slop checks and smoke tests.
- [x] Run `python -m dpe skills index --root .`.
- [x] Run `python -m dpe validate --root .`.
- [x] Run the full unittest suite.
- [x] Install the editable DPE package if needed and run `dpe update --root .`.
- [x] Run `dpe init` for the Documents workspace to install the managed defaults.
- [x] Verify representative skills and shared references in both user roots.
- [x] Run `dpe doctor`, `dpe skills audit`, and representative multi-domain routing queries.
- [x] Review `git diff --check`, the complete diff, and the original request before reporting.
