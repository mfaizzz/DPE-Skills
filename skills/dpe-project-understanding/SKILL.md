---
name: dpe-project-understanding
description: "Use when learning what a repo is, who it serves, what defines its behavior and which skills to load next: oriented reading plus selective sampling over full-tree dumps."
---

# Project understanding

DPE integration boundary: inherited CLI examples in this skill describe optional source-library tooling, not commands provided by this distribution. Use the root README and `scripts/dpe.py` for supported local search/validation/install, and current host capabilities for other operations. Do not install missing tools, enable hooks or write persistent memory automatically.


Use when the first task is learning what a repo is before touching it. For tracing how code runs, hand off to `dpe-codebase-analysis`.

1. **Resolve memory first.** Run `dpe memory-path --project <project-root>`; read `handoff.md` and `project.md` there if present before reading anything else.
2. **Read orientation artifacts**: nearest README, AGENTS.md/CLAUDE.md, docs, manifests, env examples, CI/runtime config.
3. **Verify every doc claim against real source.** README and docs are aspirational until the code backs them up.
4. **Sample with a budget, not exhaustively**: entry points and framework config, one representative domain slice, the data/model layer, integration boundaries, a few high-signal tests. Expand only to close a real uncertainty.
5. **Synthesize** purpose, likely users, stack, architecture style, and the source-of-truth files. Label every claim confirmed, inferred, or unknown.
6. **If a business detail can't be confirmed and nobody is available to ask**, mark it `Inferred:` with the best-supported reading — do not guess silently and do not block on it.
7. **Save the verified understanding** with `dpe remember --project <project-root> --kind project`; never write inferred or unknown claims to memory.
8. **Recommend the next 1-3 skills** for the concerns that remain, and say what each one will resolve.

Check before you finish: every claim in the summary cites a file, sampled vs unread areas are stated, and any existing memory or map was re-checked against current source rather than trusted as-is.

Full workflow, output template, and checklist: `reference.md`.
