---
name: trellis-workflow-enhancer
description: Audit and apply real, project-local Trellis integrations for Matt Pocock and Waza skills, with phase routing, hook injection, durable artifact handoffs, and smoke-test evidence. Use when a user wants to strengthen, compare, modernize, integrate, or debug Trellis with Matt/Waza workflows, especially when skills are installed but do not actually trigger.
---

# Trellis Workflow Enhancer

Build an optional integration layer, not a replacement framework. Trellis owns
task state, package/spec scope, planning artifacts, acceptance evidence, check,
spec updates, and finish. Matt and Waza contribute focused engineering habits
only where the target repository has an observed gap.

## Two Modes

Start in **audit mode**. Read the target repository and present evidence-backed
options. Do not create tasks, edit Trellis files, install/update skills, change
hooks, or alter task status before the user selects concrete enhancement IDs.
`N0` means no change and is a valid result.

After a concrete selection, enter **apply mode**. Apply only the selected
bundles and the required `I1` runtime-binding prerequisite. Never claim an
integration is active until the bundled verifier passes; a route in Markdown or
an installed skill directory alone is not proof.

## What Counts As Integrated

Treat an enhancement as integrated only when all of these layers agree:

1. **Source**: the selected skill is available from a project-local
   `.agents/skills/<name>/SKILL.md` or platform-equivalent project-local path,
   and its frontmatter has been read.
2. **Route**: `.trellis/workflow.md` has a `### Skill Routing` row naming the
   skill, trigger, and Trellis handoff.
3. **Phase**: the route is repeated in the relevant
   `[workflow-state:...]` breadcrumb block, including inline variants when the
   target supports them.
4. **Invocation**: the route mode matches the skill frontmatter. A skill with
   `disable-model-invocation: true` is explicit-only; a hook may surface its
   slash command but must never claim to execute it silently.
5. **Runtime**: a configured `UserPromptSubmit`/equivalent hook reads the
   workflow state and emits context. Run the hook smoke test when applying.
6. **Handoff**: the skill result names a durable Trellis artifact and a gate
   that must be satisfied before the phase advances.

The machine-readable contract is
`.trellis/skill-integration.json`. Use the schema and examples in
[references/integration-contract.md](references/integration-contract.md). It
is an audit record and a cross-check, not a second task tracker.

## 1. Collect Current Evidence

Read the target repository before recommending anything:

1. Read `AGENTS.md`/`CLAUDE.md`, `.trellis/config.yaml`,
   `.trellis/workflow.md`, `.trellis/spec/`, active task artifacts, and the
   configured platform hook files.
2. Run the installed Trellis context command when available. Read the config
   parser or local documentation before assuming package or scope semantics.
3. Discover selected skills from the target project's local skill directories,
   shared skill roots, and the active agent's skill list. Read each selected
   `SKILL.md` fully before naming its behavior. Record whether the skill is
   automatic, conditional, or explicit-only from its frontmatter.
4. Check official Matt and Waza sources in read-only mode. Record the checked
   revision or version, date, local version, and unavailable sources. Never call
   an installed skill current without an upstream check. Read
   [the integration catalog](references/integration-catalog.md) before routing.
5. Inspect real validation commands and test infrastructure. Do not infer a
   test runner from a framework or invent a command.

Redact secrets, tokens, private URLs, user data, and internal hostnames from
reports and durable artifacts.

## 2. Diagnose Boundaries, Not Brands

Use the current Trellis workflow as the baseline. Assess only surfaces where
repository evidence justifies a change:

- package ownership and spec scope;
- requirement, domain, and API decision clarity;
- tests, bug reproduction, and feedback loops;
- independent review and module/interface design;
- UI/visual iteration and documentation work;
- WIP, durable knowledge, and workflow maintainability.

For every candidate, state the observed Trellis gap, the verified source
capability, the phase it belongs to, the durable artifact it produces, and what
Trellis responsibility it must not replace. Never recommend a skill because it
is popular.

## 3. Present Options Before Editing

Read [the comparison template](references/comparison-template.md). Produce one
compact table in the user's language with:

`ID | Before | Optional after | Verified source capability | Benefit | Cost or risk | Prerequisite | Default`

Include `I1` (runtime binding and evidence), every evidence-backed optional
bundle, and `N0` (no change). Mark defaults as `recommend`, `situational`, or
`do not add`. State that any applied bundle includes `I1`.

After the table, show:

1. evidence and source revisions used;
2. invocation mode and overlap guards;
3. exact files and task state affected by each option;
4. verification commands, including the hook smoke test;
5. one explicit selection prompt: `Select I1 + IDs, all recommended, or N0.`

Do not treat silence, agreement with the analysis, or a request to "optimize"
as selection. Wait for a concrete choice.

## 4. Apply Only Selected Options

After selection, preserve dirty work and make only selected, project-local
changes:

1. Verify each selected skill source and frontmatter. Do not silently install,
   update, or replace a third-party skill. If the source is missing, report the
   prerequisite instead of fabricating a route.
2. Add or update `### Skill Routing` rows in `.trellis/workflow.md`. Each row
   must name the trigger, mode, phase handoff, and artifact. Keep
   `disable-model-invocation: true` skills explicit-only.
3. Add or update matching `[workflow-state:...]` blocks. A hook can only inject
   text that exists in these blocks; a route table outside them is not runtime
   activation. Include both normal and Codex inline blocks when present.
4. Keep the execution order explicit: Trellis check first, then the selected
   independent Matt/Waza review, then spec update and commit. Do not let
   `/check` or `/code-review` replace `trellis-check`.
5. Write `.trellis/skill-integration.json` for the selected routes. Include
   `mode`, `phase`, `trigger`, `artifacts`, `gate`, hook markers, and
   `review_order`. Do not use an empty artifact, a placeholder such as `none`,
   or a vague claim such as `handled by the workflow`.
6. Record stable project-specific routing and verified source revisions in the
   project's local `trellis-local` skill. Do not copy third-party skill text.
7. Run the bundled verifier from this skill:

   ```bash
   python3 <path-to-trellis-workflow-enhancer>/scripts/verify_integration.py \
     <target-repository> --smoke
   ```

   The verifier must pass before reporting "integrated". If it fails, report
   the exact layer that is missing: source, route, phase, invocation, runtime,
   or handoff.

Do not change global agent settings, global hook approval, `.gitignore`, task
history, commit state, or issue-tracker configuration unless the user selected
that separate action. A project hook prerequisite that still needs host
approval is **pending**, not active.

## 5. Verify and Hand Off

For audit mode, report "installed", "routed", "hook configured", and "runtime
observed" separately. For apply mode, report "integrated" only when all six
proof layers and the verifier pass.

At minimum, validate:

- `.trellis/skill-integration.json` schema and route entries;
- local skill frontmatter and invocation modes;
- workflow state tags and route-table handoffs;
- hook configuration, hook source markers, and `--smoke` output;
- Trellis config/package context, task context JSONL, Markdown links, and the
  fixed `trellis-check -> independent review` order.

Run source checks only when selected work changed source. Never invent a test
command; report missing automation and manual evidence plainly.

Finish with the same before/after table, marking selected options as applied and
unselected options as deferred. State local skills and upstream versions used,
remaining tradeoffs, intentionally untouched surfaces, and any host approval
still required.
