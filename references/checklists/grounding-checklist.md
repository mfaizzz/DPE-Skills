# dpe Grounding Checklist

Use this checklist when the answer depends on documents, data, or facts the agent did not verify.

- Say "I don't have enough information to confidently answer this" when evidence is missing; do not fill gaps with plausible text.
- For long documents (roughly >20k tokens, or any contract, policy, report, or spec review): extract numbered verbatim quotes first and analyse only from those quotes.
- Every factual claim traces to `file:line`, a URL, a quote number, or command output. After drafting, retract or mark `unverified` any claim with no support.
- When the user supplies documents, answer only from them unless they ask for general knowledge. Label anything drawn from outside as `outside the provided sources`.
- High-stakes conclusions (security, money, legal, architecture) get a second independent pass; disagreement means re-verify.
- `dpe remember` only stores claims verified in-session.

## Release Gate

- Confirm what was verified.
- State what remains unverified.
- Add regression test, metric, SOP, or rollback trigger where applicable.
- Save durable memory only for stable decisions, preferences, constraints, or reusable lessons.
