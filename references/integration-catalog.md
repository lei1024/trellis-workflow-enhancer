# Integration Catalog

Revalidate this catalog on every run. Names and paths change more often than
workflow responsibilities.

## Ownership

| System | Owns | Must not replace |
| --- | --- | --- |
| Trellis | task lifecycle, package scope, task artifacts, spec selection, acceptance evidence | domain interview depth, independent review discipline, visual iteration |
| Matt Pocock skills | decision grilling, durable domain language, TDD, diagnosis, review, and module design | Trellis task state, package selection, or release evidence |
| Waza skills | visual implementation, reading/writing assistance, and optional health inspection | task planning, bug evidence, or engineering review gates |

## Upstream Verification

Use read-only sources only. Do not update or install globally unless the user
selects that separate action.

| Source | Canonical location | What to check |
| --- | --- | --- |
| Matt Pocock | `https://github.com/mattpocock/skills` | current README, current skill names, and relevant `SKILL.md` files on the default branch |
| Waza | `https://github.com/tw93/Waza` | `VERSION`, installed skill metadata, and only the relevant upstream skills |
| Trellis | target repository `.trellis/` plus installed Trellis metadata | local config parser, workflow, package context, spec layers, and task behavior |

If upstream access is unavailable, say so. Use installed skills as local
evidence, label the version as unverified, and do not describe them as latest.

## Candidate Capability Map

Use only rows whose local and upstream capability is verified. Current names
are examples, not a permanent contract.

| Area | Typical Matt capability | Typical Waza capability | Trellis integration boundary |
| --- | --- | --- | --- |
| Unclear requirements | `grill-with-docs`, or stateless `grill-me` | none by default | a deep Phase 1.1 route; decisions return to task artifacts |
| Behavior feedback | `tdd` | none by default | implementation plan records real test seam or manual fallback |
| Bugs | `diagnose` or locally named equivalent | visual evidence may assist UI bugs | reproduction belongs in task evidence before repair |
| Review | `code-review` | none by default | independent check after Trellis verification for selected risk classes |
| Module design | `codebase-design` | none by default | use only when an observed ownership or seam problem exists |
| Visual work | none by default | `ui` | UX decisions and visual acceptance criteria return to `design.md` |
| Documentation | none by default | `read`, `write` | source and task ownership remain in Trellis |
| Workflow health | none by default | `health` | advisory audit, never automatic task or config mutation |

## Common Collision Rules

- Do not run Trellis brainstorming and a second full Matt interview in series.
  Use the verified Matt route as the deep form of that planning step.
- Do not allow a Waza visual decision to bypass Trellis `design.md`.
- Do not call a successful lint, build, or health scan bug reproduction unless it
  can observe the reported failure.
- Do not add an independent review gate to every change. Restrict it to the
  risk classes observed in the target repository.
- Do not import full third-party skill text into a project-local customization.
  Record routing, source version, trigger, and ownership boundary instead.
