---
name: trellis-workflow-enhancer
description: Analyze a repository's Trellis workflow against the currently installed and upstream Matt Pocock and Waza skills, then present evidence-backed optional enhancements before changing anything. Use when a user wants to strengthen, compare, modernize, integrate, or audit Trellis with Matt/Waza workflows, or asks for an opt-in agent-development workflow improvement.
---

# Trellis Workflow Enhancer

Build a recommendation, not a replacement framework. Trellis remains the task,
specification, and acceptance system. Matt and Waza supply only verified,
non-overlapping discipline where the user elects to use it.

## Non-Negotiable Gate

Start in analysis-only mode. Do not create tasks, edit Trellis files, install or
update skills, change version control, or alter task status until the user
selects specific enhancement IDs from the comparison report.

The user may choose no enhancements. Treat that as a successful outcome and
leave the repository unchanged.

## 1. Collect Current Evidence

Read the target repository before recommending anything:

1. Read `AGENTS.md`/`CLAUDE.md`, `.trellis/config.yaml`,
   `.trellis/workflow.md`, `.trellis/spec/`, and active task artifacts.
2. Run the installed Trellis context command when available. Read the config
   parser or local documentation before assuming package or scope semantics.
3. Discover installed skills from the target project's `.agents/skills/`, the
   user's shared skill roots, and the active agent's skill list. Read each
   selected `SKILL.md` fully before naming its behavior.
4. Check the current upstream source without modifying it. Use the official
   Matt and Waza repositories described in
   [the integration catalog](references/integration-catalog.md). Record the
   checked revision or version, date, local version, and any unavailable source.
   Never claim a skill is current merely because it is installed locally.
5. Inspect real validation commands and test infrastructure. Do not infer a test
   runner from a framework or invent a command.

Redact secrets, tokens, private URLs, user data, and internal hostnames from
the report and any durable artifact.

## 2. Diagnose Boundaries, Not Brands

Use the current Trellis workflow as the baseline. Assess only the following
surfaces when evidence justifies them:

- package ownership and spec scope;
- requirement and domain decision clarity;
- feedback loops, tests, and bug reproduction;
- independent review and module/interface design;
- UI/visual iteration and documentation work;
- WIP, durable knowledge, and workflow maintainability.

Do not recommend a skill because it is popular. For every candidate, state
which observed Trellis gap it addresses and what existing Trellis responsibility
it must not replace. Read the integration catalog before routing Matt or Waza.

## 3. Present Options Before Editing

Read [the comparison template](references/comparison-template.md). Produce one
compact table in the user's language with these columns:

| ID | Before | Optional after | Verified source capability | Benefit | Cost or risk | Prerequisite | Default |
| --- | --- | --- | --- | --- | --- | --- | --- |

Include a row for every credible option and a `no change` choice. Separate
recommendations into small independently selectable bundles, normally scope,
discovery, feedback, review, UI, and health. Mark each default as one of:
`recommend`, `situational`, or `do not add`.

After the table, show:

1. the evidence and source versions used;
2. overlap guards explaining why Trellis, Matt, and Waza are not run twice for
   the same responsibility;
3. the exact files and task state that a selected option would affect;
4. a single explicit selection prompt, for example: `Select S1, D1, F1, R1,
   V1, H1, all recommended, or no change.`

Do not treat silence, agreement with the analysis, or a request to "optimize"
as selection. Wait for a concrete choice.

## 4. Apply Only Selected Options

Create or activate a Trellis task only after the user selects an option set and
the target workflow requires one. Preserve existing task history and dirty
work. Keep each edit tied to a selected ID.

- Put project-specific routing and source versions in a project-local
  `trellis-local` skill. Do not modify upstream Trellis or third-party skills.
- Keep task-specific decisions in `prd.md` and `design.md`; promote stable
  terminology to `CONTEXT.md` and irreversible cross-module choices to ADRs.
- Reference Matt or Waza by its verified current name. Do not copy their skill
  content into the project or force a global installation/update.
- Do not change `.gitignore`, commit, push, archive tasks, add lifecycle hooks,
  or change global agent settings unless the user explicitly selected that
  separate action.
- For behavior changes, describe a real feedback loop. Use TDD only when a
  suitable test seam and harness exist. For bugs, reproduce before repair;
  document a manual fallback only when automation is not practical.

## 5. Verify and Hand Off

Verify the selected behavior using the repository's real tools. At minimum,
validate Trellis config/package context, task context JSONL, edited Markdown
links, and absence of removed placeholders. Run source checks only when the
selected work changed source, and report any unrun command plainly.

Finish with the same before/after table, marking selected options as applied and
unselected options as deferred. State the local skills and upstream versions
actually used, remaining tradeoffs, and every intentionally untouched surface.
