# Skills

The default response voice is [`malaysia-localisation`](../skills/malaysia-localisation/SKILL.md): short, simple and easy to understand, matching the user’s English, BM or rojak. It complements the primary task skill and is included in the lean, core, engineering and full profiles. Explicit language, tone, length and format requests take priority. `dpe install` / `dpe update` refresh the default voice in supported user instruction files; `dpe init` adds it to project instructions. Existing projects can rerun `dpe init` to refresh their managed block.


Canonical skills live in [`skills/`](../skills/). Each folder contains `SKILL.md` with YAML frontmatter. Write descriptions so agents can self-select: lead with **Use when…** and concrete user triggers (CI failure, release notes, cofounder mode, etc.).

## Writing a skill

A loaded skill stays in the conversation and is read again on every later turn, so keep `SKILL.md` short: a checklist of what to do, in the order to do it, with the checks that matter. Put the detail (long tables, examples, templates, per-stack variants) in `reference.md` next to it and end `SKILL.md` with one line naming it; the agent opens it only when it needs it. The 20 everyday first-party skills follow this shape (41 KB in total, from 143 KB). Vendored skills are never reworded in place.

## Routing

- Say `dpe` or use cofounder mode for cross-domain work.
- `dpe skills find "<task>"` chooses a primary skill and useful complements. `selection` explains selected and deferred skills, weak confidence, and missing named skills. Read descriptions and check host capabilities before loading. `matches` remains a ranked search list.
- Mixed asks are scored by concern as well as the whole prompt. Explicit skill ids and aliases take priority; negated requests, incompatible alternatives, user-only slash commands, and unavailable skills are deferred. Ordinary words such as “schema” do not count as named requests without invocation context.
- The CLI uses the installed profile by default. Use `--profile lean|core|engineering|full` to override it, or pass an actual host inventory to the Python `select_skill_stack(..., available=...)` API. A profile check cannot prove that a running host exposes every installed skill; inspect its live inventory. Optional runtimes remain capability checks in the selected skill.
- Selection is a lexical heuristic, not a probability or a runtime command. Re-route when the task changes. Tests and the [routing benchmark](benchmarks/README.md) cover a recorded regression corpus; they do not guarantee every future prompt or prove coding quality.
- The router scores a request against each skill's own words and curated trigger phrases, plus the vocabulary of real requests: [`benchmarks/routing-queries.json.gz`](../benchmarks/routing-queries.json.gz) holds 30 generated messages per skill, `dpe skills index` keeps each skill's 150 most distinctive words in `skill-index.json`, and a BM25 match against them is added (relative to the best-fitting skill). That is what lets "jest hanging after tests finish" find a debugging skill. Regenerate the messages when a skill's purpose changes; the prompt used is described in the [benchmark notes](benchmarks/README.md).
- `dpe skills audit` measures always-loaded description size, long skill bodies, provenance grouping, and broken relative references.
- Deprecated DPE names resolve via [`skills/aliases.json`](../skills/aliases.json).
- Vendored third-party skills are listed in [`skills/vendored.json`](../skills/vendored.json).

## Profiles

`dpe install --profile lean` (where a first install starts) lists about 25 everyday skills with short descriptions and installs the other ~210 whole in `~/.dpe/library`. The agent reaches them through [`dpe-skill-finder`](../skills/dpe-skill-finder/SKILL.md): `dpe skills find "<task>"` names the skills and `dpe skills show <id>` prints one. The list lives in [`skills/lean.json`](../skills/lean.json); `dpe validate` keeps it small and complete.

`dpe install --profile core` installs DPE co-founder essentials plus the **loop-engineering** pack (12 loop/triage/CI/PR skills) and `dpe-grounding`. Always-on loop discipline is in [`AGENTS.md`](../AGENTS.md#loop-engineering-always-on); always-on grounding is in [`AGENTS.md`](../AGENTS.md#grounding-always-on).

`dpe install --profile engineering` installs and lists every skill except the 47 of the marketingskills pack (about 195), for people who build software and do not need the marketing set.

`dpe install --profile full` installs and lists the entire library (~240 skills), including all other vendored packs.

## Vendored packs

| Pack | Skills | Optional pip tool |
|---|---|---|
| marketingskills | 47 marketing/CRO/SEO/copy skills | — |
| superpowers | 15 process skills (brainstorm, TDD, debug, plans, session diagnosis) | — |
| hallmark | Anti-AI design skill | — |
| browser-use | 5 browser agent skills | `browser-use` |
| graphify | Knowledge-graph skill | `graphifyy` |
| markitdown | Document conversion skill | `markitdown[all]` |
| opendataloader-pdf | Structured PDF extraction, OCR, tables, bounding boxes, and RAG citations | `opendataloader-pdf` |
| loop-engineering | 12 loop/triage/CI/PR skills | — |
| taste-skill | 10 anti-slop frontend / imagegen skills | — |
| scroll-world | Scroll-scrub Higgsfield cinematic world landing | Higgsfield CLI, ffmpeg |
| dcg | Destructive Command Guard (agent shell/git safety hooks) | `dcg` binary (upstream installer) |
| emil-skills | 12 motion craft / design engineering skills (web + Expo animation, Sonner, Swift) | — |
| i-have-adhd | Action-first, numbered, no-preamble output shape (explicit `/i-have-adhd`) | — |
| ecc | 10 curated engineering skills: MySQL/MariaDB, migrations, error handling, MCP servers, Playwright E2E, WCAG 2.2, ADRs, Vue 3, Python, pytest | — |
| graft | Codebase map and call-tracing skill (needs a `graft/` index) | `@nanonets/graft` CLI (npm) |
| moli | 2 browser-fetch and CDP skills (`moli-webfetch`, `moli-cdp-server`) | Moli browser (Rust binary, not bundled) |
| dpe-quality-core | 6 delivery gates for general output, UI, mobile layout, copy, people/accessibility, and code comments | — |

`dpe-headroom` routes context-compression work but does not install or configure the optional Headroom runtime. Use it only for bulky tool output; normal concise answers belong to `dpe-token-saver`.

Attribution: [`docs/third-party.md`](third-party.md). Optional deps: [`requirements-optional.txt`](../requirements-optional.txt).

## Overlaps (keep both)

| DPE skill | Vendored skill | When to prefer vendored |
|---|---|---|
| `dpe-taste` | `hallmark` | New UI pages that need a distinct non-template look |
| `dpe-taste` | `taste-skill` (default), `soft-skill`, `minimalist-skill`, `brutalist-skill`, `redesign-skill` | Full tasteskill.dev pack: dials, redesign audit, direction variants |
| `dpe-marketing-growth` | `product-marketing`, `copywriting`, `cro` | Deep marketing task with frameworks |
| `dpe-browser-automation` | `browser-use` | Full browser-use agent stack is installed |
| `dpe-diagnose-loop` | `systematic-debugging` | Superpowers debug workflow requested |
| `dpe-tdd-loop` | `test-driven-development` | Superpowers TDD workflow requested |
| `dpe-diagnose-loop`, `dpe-ratchet-loop` | `loop-triage`, `loop-verifier`, `minimal-fix` | Loop-engineering agent loops (CI/PR/issue sweeps) |
| `dpe-gsap-animation`, `dpe-lenis-smooth-scroll` | `scroll-world` | Higgsfield scroll-scrub fly-through world landing; use DPE GSAP/Lenis for code-only motion |
| `dpe-taste`, `taste-skill`, `hallmark` | `emil-design-eng`, `animate`, `apple-design` | Motion craft (easing, duration, interruption, gesture); keep taste/hallmark for layout, type, color, content |
| `dpe-throwaway-prototype`, `dpe-rapid-prototype` | `prototype` | `/prototype` is user-invoked; the model-run path for UI variants is `dpe-throwaway-prototype` (its UI.md builds switchable variants); `dpe-rapid-prototype` for MVP scaffolds |
| `dpe-expo-react-native` | `animate-expo` | Motion, gestures, sheets, haptics in Expo; keep the DPE skill for app structure, EAS, and release |
| `dpe-quality-copywriting`, `dpe-token-saver` | `i-have-adhd` | Reader asked for action-first output; it is an explicit mode that persists until "stop adhd mode" |
| `dpe-database-engineering` | `mysql-patterns`, `database-migrations` | MySQL/MariaDB specifics (InnoDB, replica lag) or a zero-downtime migration plan |
| `dpe-cypress` | `e2e-testing` | Cypress requests go to `dpe-cypress`; Playwright suites stay with `e2e-testing` |
| `dpe-browser-automation`, `dpe-qa-automation-strategy` | `e2e-testing` | Writing or de-flaking a Playwright suite (POM, config, CI artifacts) |
| `dpe-ui-ux-design-to-code` | `accessibility` | Formal WCAG 2.2 AA build or audit |
| `dpe-claude-code-setup` | `mcp-server-patterns` | Building an MCP server, not just configuring one |
| `dpe-coding-best-practices` | `error-handling` | Typed errors, retries, circuit breakers, user-facing failure messages |
| `dpe-tech-lead` | `architecture-decision-records` | Writing the ADR file itself |
| `dpe-nuxt-development` | `vue-patterns` | Vue 3 / Pinia work outside Nuxt |
| `dpe-taste`, `taste-skill`, `hallmark` | `dpe-quality-ui`, `dpe-quality-layoutmobile` | Use design skills to choose direction, then Anti-Slop specialists to audit the produced UI and responsive behavior |
| `dpe-grounding` | `dpe-deep-research`, `odl-pdf` | Always-on grounding discipline; add deep-research for multi-source synthesis, odl-pdf for citation-ready PDF extraction |
| `markitdown` | `odl-pdf` | OpenDataLoader-specific or structured PDF work: scanned OCR, tables, JSON, bounding boxes, or citation-ready RAG; keep `markitdown` for generic Office/PDF/HTML-to-Markdown conversion |
| — | `python-patterns`, `python-testing` | DPE has no Python skill of its own; these are the defaults |

## Aliases (merged DPE duplicates)

| Old ID | Canonical |
|---|---|
| `dpe-caveman` | `dpe-token-saver` |
| `dpe-bug-finding` | `dpe-diagnose-loop` |
| `dpe-root-cause-investigation` | `dpe-diagnose-loop` |
| `dpe-project-management` | `dpe-planning-execution` |
| `dpe-social-content-calendar` | `dpe-content-calendar` |
| `dpe-agent-security-hardening` | `dpe-prompt-injection-defense` |
| `dpe-grill-me` | `dpe-grill-with-docs` |
| `dpe-zoom-out` | `dpe-codebase-analysis` |
