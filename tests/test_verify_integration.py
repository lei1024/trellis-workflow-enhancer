#!/usr/bin/env python3
"""Regression tests for the anti-false-integration verifier."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_integration.py"


WORKFLOW = """### Phase Index

[workflow-state:no_task]
No active task.
[/workflow-state:no_task]

[workflow-state:planning]
Use /grill-with-docs when decisions are unclear and write results to prd.md.
[/workflow-state:planning]

[workflow-state:planning-inline]
Use /grill-with-docs when decisions are unclear and write results to prd.md.
[/workflow-state:planning-inline]

[workflow-state:in_progress]
Run trellis-check before /code-review; write review findings to implement.md.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Run trellis-check before /code-review; write review findings to implement.md.
[/workflow-state:in_progress-inline]

### Skill Routing

| User intent | Skill/action | Trellis handoff |
| --- | --- | --- |
| Decisions are unclear | Explicit Matt `/grill-with-docs` | Stay in Phase 1.1; copy decisions into `prd.md` |
| Shared API risk after check | Automatic Matt `/code-review` | Run after `trellis-check`; record findings in `implement.md` |
"""


HOOK = """#!/usr/bin/env python3
import json
from pathlib import Path
# Emit the workflow-state blocks that the hook reads from the workflow file.
workflow = Path('.trellis/workflow.md').read_text(encoding='utf-8')
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": workflow + "\\n<skill-routing>"}}))
"""


MANIFEST = {
    "schema": 1,
    "required_states": ["no_task", "planning", "planning-inline", "in_progress", "in_progress-inline"],
    "routes": [
        {
            "skill": "grill-with-docs",
            "owner": "matt",
            "mode": "explicit",
            "phase": "planning",
            "trigger": "unresolved product or domain decisions",
            "artifacts": [".trellis/tasks/<active>/prd.md", ".trellis/tasks/<active>/design.md"],
            "gate": "before task.py start",
        },
        {
            "skill": "code-review",
            "owner": "matt",
            "mode": "automatic",
            "phase": "review",
            "trigger": "shared API risk after Trellis check",
            "artifacts": [".trellis/tasks/<active>/implement.md"],
            "gate": "after trellis-check and before commit",
        },
    ],
    "review_order": ["trellis-check", "code-review"],
    "hook": {
        "event": "UserPromptSubmit",
        "command_contains": ["inject-workflow-state.py"],
        "output_markers": ["workflow-state", "skill-routing"],
    },
}


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_repo(root: Path, manifest: object = MANIFEST) -> None:
    write_file(root / ".trellis" / "workflow.md", WORKFLOW)
    write_file(
        root / ".agents" / "skills" / "grill-with-docs" / "SKILL.md",
        "---\nname: grill-with-docs\ndescription: Ask questions.\ndisable-model-invocation: true\n---\n",
    )
    write_file(
        root / ".agents" / "skills" / "code-review" / "SKILL.md",
        "---\nname: code-review\ndescription: Review changes.\n---\n",
    )
    write_file(root / ".codex" / "hooks.json", json.dumps({
        "hooks": {"UserPromptSubmit": [{"hooks": [{
            "type": "command",
            "command": "python3 .codex/hooks/inject-workflow-state.py",
        }]}]}
    }))
    write_file(root / ".codex" / "hooks" / "inject-workflow-state.py", HOOK)
    write_file(root / ".trellis" / "skill-integration.json", json.dumps(manifest))


class VerifyIntegrationTests(unittest.TestCase):
    def run_verify(self, repo: Path, smoke: bool = False) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(VERIFY), str(repo)]
        if smoke:
            command.append("--smoke")
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_valid_contract_runs_hook_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            create_repo(repo)
            result = self.run_verify(repo, smoke=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("hook smoke output", result.stdout)

    def test_missing_manifest_is_not_called_integrated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            create_repo(repo)
            (repo / ".trellis" / "skill-integration.json").unlink()
            result = self.run_verify(repo)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("not integration proof", result.stdout)

    def test_disabled_skill_cannot_be_routed_as_automatic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            invalid = json.loads(json.dumps(MANIFEST))
            invalid["routes"][0]["mode"] = "automatic"
            create_repo(repo, invalid)
            result = self.run_verify(repo)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires mode=explicit", result.stdout)


if __name__ == "__main__":
    unittest.main()
