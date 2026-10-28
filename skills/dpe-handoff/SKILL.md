---
name: dpe-handoff
description: "Use when the user asks to hand off, wrap up for another agent or session, or write a continuation document — compacts the conversation into <memory-dir>/handoff.md so a fresh agent in any tool can continue. Context-pressure handoffs belong to dpe-context-limit-continuation."
argument-hint: "What will the next session be used for?"
---

# Handoff

DPE integration boundary: inherited CLI examples in this skill describe optional source-library tooling, not commands provided by this distribution. Use the root README and `scripts/dpe.py` for supported local search/validation/install, and current host capabilities for other operations. Do not install missing tools, enable hooks or write persistent memory automatically.


For compacting the current conversation into a document a fresh agent, in any tool or model, can continue from. A handoff forced by context or token pressure instead uses `dpe-context-limit-continuation`.

1. **Resolve where it goes first.** Run `dpe memory-path --project <project-root>` for `<memory-dir>` — a vault path when `memory_storage` is obsidian, or `.dpe/` in the repo under legacy mode. Follow whichever it returns; never assume `.dpe/`. If no memory location is configured and the user does not want one set up, write to the OS temp directory and print the path instead.
2. **Write to `<memory-dir>/handoff.md`**, creating the directory if missing. Under legacy repo mode, add `.dpe/` to `.gitignore` if it is not already ignored.
3. **Overwrite the whole file; never append.** It holds only the current unfinished work, not a history. Tell the user to clear it once the work is done.
4. **Fill every section from `references/session-handoff-template.md`**: goal and status (done / not done / blocked); key decisions already made, with the reason, so the next agent does not reopen them; files and artifacts touched, linked by path or URL rather than pasted in full; verification performed *and* verification not performed; open risks and follow-ups; suggested next skills by id; a `FOR_NEXT_MODEL` paste block of ordered next steps with concrete paths or commands.
5. **Redact by hand before saving**: API keys, passwords, tokens, personal data. The handoff file is ephemeral and does not go through `dpe remember`.
6. **Route durable lessons elsewhere.** Anything worth keeping beyond this one task goes through `dpe-continuous-learning`, not into `handoff.md`.
7. **Don't duplicate** content that already lives in a PRD, plan, ADR, issue, or commit — link it instead of copying it in.

When the user wants a background agent to start at once, only launch it on request: save the summary to a temp file, give the session a descriptive name, and pass the file to the command (for example `claude --bg --name "<name>" -- "$(cat <file>)"`) so the shell cannot expand backticks or `$` in the summary. Check the installed CLI supports the flag first. The summary becomes the new agent's prompt, so redact secrets and personal data in it.

If the user passed arguments, treat them as the next session's focus and write the document around that.

The full template and the memory-first handoff protocol: `reference.md`.

Background-agent launch note adapted in part from in-progress/claude-handoff (skills pack by Matt Pocock, MIT).
