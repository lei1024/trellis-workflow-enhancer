# Integration Catalog

Revalidate this catalog on every run. Names, paths, and invocation metadata
change more often than workflow responsibilities. The catalog is a routing aid,
not proof that a skill is installed or active.

## Ownership

| System | Owns | Must not replace |
| --- | --- | --- |
| Trellis | task lifecycle, package scope, task artifacts, spec selection, acceptance evidence | domain interview depth, independent review discipline, visual iteration |
| Matt Pocock skills | decision shaping, durable domain language, TDD, diagnosis, review, module design, and optional tracker workflows | Trellis task state, package selection, Trellis check, or release evidence |
| Waza skills | planning challenge, UI, diagnosis, review/release checks, research/reading/writing, and health inspection | Trellis task state, task artifacts, root-cause evidence ownership, or Trellis check |
| Enhancer contract | route/phase/hook/artifact evidence and smoke verification | executing a user-invoked skill or replacing any source skill |

## Upstream Verification

Use read-only sources only. Do not update or install globally unless the user
selects that separate action.

| Source | Canonical location | What to check |
| --- | --- | --- |
| Matt Pocock | `https://github.com/mattpocock/skills` and `https://www.aihero.dev/skills` | current README, current invocation classes, current skill names, relevant `SKILL.md` files, and checked revision |
| Waza | `https://github.com/tw93/Waza` | `VERSION`, current skill metadata, invocation behavior, and only the relevant upstream skills |
| Trellis | target repository `.trellis/` plus installed Trellis metadata | local config parser, workflow, package context, spec layers, and task behavior |

If upstream access is unavailable, say so. Use installed skills as local
evidence, label the version as unverified, and do not describe them as latest.

## Candidate Capability Map

Use only rows whose local and upstream capability is verified. Current names
are examples, not a permanent contract.

| Area | Typical Matt capability | Typical Waza capability | Trellis integration boundary |
| --- | --- | --- | --- |
| Unclear requirements | explicit `grill-with-docs` / `grill-me`; model-invoked `grilling` | `think` for a decision-complete plan | one deep Phase 1.1 route; decisions return to task artifacts |
| Domain and module design | model-invoked `domain-modeling`, `codebase-design`; explicit `wayfinder` for very large work | none by default | preserve Trellis planning/status; write decisions to `CONTEXT.md`, ADRs, `prd.md`, or `design.md` |
| Concrete state or UI question | model-invoked `prototype` | `ui` | prototype/UI verdict and acceptance states return to `design.md` |
| External facts | model-invoked `research` | `read`, `learn` | cited findings go under the active task `research/` directory |
| Behavior feedback | model-invoked `tdd` | none by default | implementation plan records a real seam and feedback command |
| Bugs and regressions | model-invoked `diagnosing-bugs` | `hunt` | reproduce and confirm root cause before repair; record evidence in task artifacts |
| Review | model-invoked `code-review` | `check` for release/merge/audit | independent review only after Trellis check and only for selected risk |
| Documentation | none by default | `write` | source and task ownership remain in Trellis |
| Workflow health | none by default | `health` | advisory audit, never automatic task or config mutation |
| Cross-session continuity | explicit `handoff` | none by default | handoff points to Trellis artifacts; resume through Trellis |

## Common Collision Rules

- Do not run Trellis brainstorming and a second full Matt interview in series.
  Use the verified Matt route as the deep form of that planning step.
- Do not allow a Waza visual decision to bypass Trellis `design.md`.
- Do not interpret the enhancer's hook as skill execution. It injects the
  current workflow route; explicit-only skills still require the user's slash
  command.
- Do not report `Installed` or `Routed` as `Integrated`. Use the proof levels in
  [the runtime integration contract](integration-contract.md).
- Do not call a successful lint, build, or health scan bug reproduction unless it
  can observe the reported failure.
- Do not add an independent review gate to every change. Restrict it to the
  risk classes observed in the target repository.
- Do not import full third-party skill text into a project-local customization.
  Record routing, source version, trigger, invocation mode, phase, artifact,
  gate, and ownership boundary instead.

## Invocation classes to verify

Matt's current catalog separates user-invoked orchestration from model-invoked
discipline. Confirm the target's actual frontmatter rather than assuming from
the brand:

| Class | Matt examples | Integration behavior |
| --- | --- | --- |
| User-invoked | `ask-matt`, `grill-with-docs`, `grill-me`, `triage`, `improve-codebase-architecture`, `setup-matt-pocock-skills`, `to-spec`, `to-tickets`, `implement`, `wayfinder`, `handoff`, `teach`, `writing-great-skills` | Route as explicit; hook surfaces the command and waits |
| Model-invoked | `prototype`, `diagnosing-bugs`, `research`, `tdd`, `domain-modeling`, `codebase-design`, `code-review`, `resolving-merge-conflicts`, `grilling` | Route as an automatic candidate only when the task intent matches |

Waza's current eight-skill set is `think`, `ui`, `check`, `hunt`, `write`,
`learn`, `read`, and `health`. Verify each local frontmatter and route its
output to a Trellis artifact; Waza's documented chaining is manual, so a
successful hook injection does not mean the next Waza skill already ran.
