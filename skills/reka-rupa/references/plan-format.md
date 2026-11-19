# Plan format for split design work

Each part of a Step 2b split is saved as a plan file in the same format as the `smart-plan` skill, so either skill can read it and `smart-implement` can run it. It stands alone; `smart-plan` is not required.

## Where and what to name it

`.agents/plans/design/YYYY/MM/DD/YYYY-MM-DD-<TICKET>-<kebab-name>-part<n>.md`, dated the day it is first written. No ticket: leave it out of the name. Take the ticket from the user, `--ticket=` or the branch name; never invent one; none found: ask once. Plans are English; replies use the user's language. A revised part keeps its file: bump `Revision`, add `Revision n: <what and why>`.

## Template (one part, short)

```markdown
# Plan: <part title>
Status: DRAFT · Revision: 1 · Ticket: <ABC-123 | none>
Part: <n> of <m> · Series: <kebab-name>

## Context      — why, the outcome of this part, and `Not in this part:` what later parts take
## Tasks        — `- [ ] T<n> <what> — <frame/layer/file> · Verify: <read-back or command the agent can run>`
## Execution log — empty; one dated line per event
```

Add `Owner-verify: <visual check only the user can do>` or `BLOCKED_BY: <id>` to a task only when needed.

Rules:
- Status stays `DRAFT` until the user's go; never pre-tick a task. With a ticket, ids are `<TICKET>-T<n>`.
- Task ids are unique across all parts and continue (part 2 starts after part 1's last). `BLOCKED_BY` points to the same or an earlier part.
- One part leaves the product usable on its own. Shared decisions and rules are written once, in the earliest part that needs them; later parts cite them.
- A visual judgement is an `Owner-verify`, never a `Verify`. A task's `Verify` proves what the agent can: nodes read back, a build, a screenshot taken.
- Tick a task only with evidence in the Execution log: node id plus the value read back, or a screenshot path and what it shows. "Looks right" is no `Verify`: name node and value. A claim the screenshot contradicts fails the task.
- If `smart-plan`'s `scripts/check-plan.py` is installed, run it on each part and fix every FAIL.
