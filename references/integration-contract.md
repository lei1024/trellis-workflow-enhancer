# Runtime Integration Contract

`skill-integration.json` is the proof record for an applied enhancement. It
prevents a project from calling a skill "integrated" because a directory or a
paragraph exists while the agent never receives the route at runtime.

## Required Shape

```json
{
  "schema": 1,
  "required_states": [
    "no_task",
    "planning",
    "planning-inline",
    "in_progress",
    "in_progress-inline"
  ],
  "routes": [
    {
      "skill": "grill-with-docs",
      "owner": "matt",
      "mode": "explicit",
      "phase": "planning",
      "trigger": "unresolved product or domain decisions",
      "artifacts": [
        ".trellis/tasks/<active>/prd.md",
        ".trellis/tasks/<active>/design.md"
      ],
      "gate": "before task.py start"
    }
  ],
  "review_order": ["trellis-check", "code-review"],
  "hook": {
    "event": "UserPromptSubmit",
    "command_contains": ["inject-workflow-state.py"],
    "output_markers": ["workflow-state", "skill-routing"]
  }
}
```

## Field Rules

- `schema` is `1`.
- `routes` contains one entry for each selected skill. `skill` is the local
  directory/frontmatter name, `mode` is `automatic`, `conditional`, or
  `explicit`, and `phase` is `planning`, `implementation`, `quality-check`,
  `review`, `finish`, or `cross-session`.
- `trigger` states the observed user intent. `artifacts` names concrete durable
  outputs such as `prd.md`, `design.md`, `implement.md`, `research/`,
  `CONTEXT.md`, an ADR, or a review record. `gate` states what must happen
  before the phase advances.
- A skill whose frontmatter has `disable-model-invocation: true` must use
  `mode: explicit`. The hook may display `/skill`; it does not execute it.
- The route must occur both in `### Skill Routing` and in the matching
  `[workflow-state:...]` block in `.trellis/workflow.md`.
- `hook.command_contains` must match the configured per-turn hook command.
  `output_markers` must be present in the actual smoke output when `--smoke` is
  used.
- When `code-review` is selected, `review_order` must start with
  `trellis-check`, and the in-progress breadcrumb must state that order.

## Proof Levels

Use these labels in reports:

| Label | Evidence | Claim allowed |
| --- | --- | --- |
| Installed | local skill source exists | Skill is available locally |
| Routed | workflow table names trigger and handoff | The workflow knows the candidate |
| Phase-bound | state block names the route | The current phase can surface it |
| Hook-configured | host config points to a state-injection hook | The host is wired to try injection |
| Runtime-observed | `verify_integration.py --smoke` passes | The hook emitted the route markers |
| Integrated | all layers plus artifact/gate contract pass | The selected integration is active |

Do not collapse these labels into a single green check.
