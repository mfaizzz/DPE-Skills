---
name: dpe-continuous-learning
description: "Use when tasks, reviews, incidents, or repeated observations produced a lesson: decide the smallest durable artifact that should capture it so future sessions do not relearn it."
---

# dpe Continuous Learning

DPE integration boundary: inherited CLI examples in this skill describe optional source-library tooling, not commands provided by this distribution. Use the root README and `scripts/dpe.py` for supported local search/validation/install, and current host capabilities for other operations. Do not install missing tools, enable hooks or write persistent memory automatically.


## Configured memory location

Persistent memory is opt-in: write only when the user explicitly requests it, using the current host-supported memory mechanism and its approved path. The legacy memory CLI described in inherited reference material is not bundled; do not run an unavailable command or enable hooks. When memory_storage is obsidian, all memory including handoffs lives directly in the vault; never create .dpe/memory in a code repo. The configured storage overrides legacy export wording below.

Use this skill when recent work produced a lesson worth keeping beyond the current chat.

## How this differs from nearby skills

- **`dpe-permanent-memory-orchestration`**: the mechanics of `<memory-dir>/`, `dpe remember`, and the Obsidian export; this skill decides what deserves to go there.
- **`dpe-rules-distill`**: promotes principles seen in 3+ places into rules; this skill handles a single fresh lesson.
- **`dpe-skill-creator`**: builds or revises a skill once this skill decides a skill is the right artifact.

## Meaningfulness gate

- Meaningful if any of these are true: files changed, a decision was made, a bug/risk was found, a pattern repeated, or a workflow improvement emerged.
- Trivial if all are false. In that case, stop after noting there was no durable delta.

## Routing ladder (smallest artifact that changes future behavior)

| Lesson looks like | Artifact |
|---|---|
| a plan another session may continue | `dpe remember --kind plan` → `<memory-dir>/plans.md` |
| a verified outcome, recurring bug, or verification result | `dpe remember --kind learning` → `<memory-dir>/learnings.md` |
| a choice worth defending later | `dpe remember --kind decision` → `<memory-dir>/decisions.md` |
| a durable fact about the repo, stack, or users | `dpe remember --kind project` → `<memory-dir>/project.md` |
| a small repeatable behavior (trigger -> action) | `dpe remember --project . --kind learning "When <trigger>: <action>. Evidence: <date, what happened>"` |
| a repeatable verification step, recurring trap, or reusable procedure | checklist, pitfall, or playbook under dpe `references/` |
| a change to how the assistant works across many tasks | skill (`dpe-skill-creator`) or rule (`dpe-rules-distill`) |

`dpe remember` redacts secrets and exports the four kind files to the Obsidian vault when one is configured, so a memory write is also the Obsidian sync.

## Workflow

1. Gather evidence from the finished task, diff, tests, review findings, and memory state.
2. Write each candidate learning in one sentence.
3. Choose the smallest artifact from the ladder that will reliably change future behavior.
4. Write it: `dpe remember --project . --kind <kind> "<one to three lines>"` for memory kinds; edit the file directly for references.
5. Fix stale or contradictory memory if discovered (append a dated correction).
6. Record whether the learning was applied, deferred, or rejected, and what evidence would justify promotion later.

## Guardrails

- Do not promote vague advice.
- Do not store secrets, sensitive customer data, or transient debug chatter in memory.
- Do not create a new skill when a checklist, pitfall, or short memory note is enough.
- Do not turn one-off observations into universal rules.
- Do not write the same lesson into two artifacts; the weaker one should point at the stronger.

## Output

Return:

- signals reviewed
- candidate learnings
- chosen artifact for each learning
- smallest safe update (and the `dpe remember` result, including export status)
- freshness issues found
- next promotion actions

## References

- `../../references/memory-first-handoff-protocol.md`
- `../../references/checklists/learning-promotion-checklist.md`
- `../../references/checklists/continuous-learning-checklist.md`
- `../../references/playbooks/continuous-learning-playbook.md`
- `../../docs/memory.md`
