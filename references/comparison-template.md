# Comparison Template

Use this as the user-facing decision surface. Keep it evidence-backed and
remove rows that are not supported by the target repository or verified skills.

| ID | Before | Optional after | Verified source capability | Benefit | Cost or risk | Prerequisite | Default |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I1 | Skill files or prose routes have no runtime proof | Project-local route manifest, phase breadcrumbs, prompt-hook evidence, artifact handoffs, and smoke verification | Trellis `workflow-state` hook contract plus selected Matt/Waza frontmatter | Detects false integration before it becomes a team convention | Requires a supported project hook and one explicit smoke run | Selected skill source and existing Trellis hook path | recommend for every applied bundle |
| S1 | Generic or ambiguous package/spec context | Explicit package and scoped specs | Trellis package parser | Less unrelated context | Requires current module map | Real package roots | recommend only for multi-root projects |
| D1 | Generic planning interview | One documented deep decision route | Verified Matt grilling/domain skill | Clear terms and decisions | User time, can be too heavy for small work | Uncertain domain/product decision | situational |
| F1 | Implementation without a named feedback loop | Test seam or documented manual feedback | Verified Matt TDD/diagnosis skill | Faster, more reliable correction | Test setup can be expensive | Real harness or reproducible fallback | recommend for behavior/bug work |
| R1 | Trellis check only | Independent risk review after check | Verified Matt review skill | Catches spec and standards drift | Extra latency | Named high-risk change class | situational |
| V1 | Visual work has no iteration protocol | Waza visual work with decision return | Verified Waza UI skill | Better rendered-state evidence | Requires screenshots or runnable surface | UI change | situational |
| H1 | Workflow drift is invisible | Read-only health audit | Verified Waza health skill | Reveals maintainability gaps | Audit noise if overused | Non-trivial repository | situational |
| N0 | Existing Trellis workflow | No change | Current Trellis evidence | Zero disruption | Known gaps remain | None | always available |

After the table, list:

1. Evidence: local paths, real commands, local versions, upstream source/date.
2. Scope: exact files/tasks each selected option would affect.
3. Non-overlap: what Trellis continues to own.
4. Runtime proof: manifest path, hook event/command, state tags, smoke command,
   and the fixed review order.
5. Choice: `Select I1 + IDs, all recommended, or N0 for no change.`

Do not include a row merely because it appears in this template. Replace the
example wording with repository-specific evidence before showing it to a user.
