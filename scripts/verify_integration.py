#!/usr/bin/env python3
"""Verify that a Trellis skill integration is wired into the runtime path.

This deliberately checks more than whether a skill directory exists.  A route
must have a local skill source, a Trellis phase breadcrumb, an artifact handoff,
and a prompt hook that can inject the workflow context.  ``--smoke`` executes
the configured prompt hook once with a synthetic payload.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


STATE_RE = re.compile(
    r"\[workflow-state:([A-Za-z0-9_-]+)\]\s*\n(.*?)\n\s*\[/workflow-state:\1\]",
    re.DOTALL,
)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)

DEFAULT_MANIFEST = Path(".trellis/skill-integration.json")
DEFAULT_STATES = ("no_task", "planning", "in_progress")
INLINE_STATES = ("planning-inline", "in_progress-inline")
PHASE_STATES = {
    "planning": ("planning",),
    "implementation": ("in_progress",),
    "quality-check": ("in_progress",),
    "review": ("in_progress",),
    "finish": ("in_progress", "completed"),
    "cross-session": ("planning", "in_progress"),
}
HOOK_CONFIGS = (
    Path(".codex/hooks.json"),
    Path(".claude/settings.json"),
    Path(".cursor/hooks.json"),
    Path(".gemini/settings.json"),
    Path(".qoder/settings.json"),
    Path(".codebuddy/settings.json"),
    Path(".factory/settings.json"),
    Path(".trae/hooks.json"),
)
SKILL_ROOTS = (
    Path(".agents/skills"),
    Path(".agent/skills"),
    Path(".claude/skills"),
    Path(".cursor/skills"),
    Path(".gemini/skills"),
    Path(".qoder/skills"),
    Path(".codebuddy/skills"),
    Path(".factory/skills"),
    Path(".trae/skills"),
    Path(".kiro/skills"),
    Path(".zcode/skills"),
    Path(".snow/skills"),
    Path(".reasonix/skills"),
    Path(".kimi-code/skills"),
    Path(".grok/skills"),
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> Dict[str, str]:
    content = read_text(path)
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}
    values: Dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip("'\"")
    return values


def parse_state_blocks(content: str) -> Dict[str, str]:
    return {match.group(1): match.group(2).strip() for match in STATE_RE.finditer(content)}


def section_after_heading(content: str, heading: str) -> str:
    lines = content.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if re.match(r"^#{1,3}\s+", lines[index]):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def parse_route_rows(section: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or set(cells) <= {"-", "---", ""}:
            continue
        if cells[0].lower() in {"user intent", "用户意图"}:
            continue
        rows.append({"intent": cells[0], "action": cells[1], "handoff": cells[2]})
    return rows


def route_row(rows: Sequence[Dict[str, str]], skill: str) -> Optional[Dict[str, str]]:
    needle = "/" + skill
    for row in rows:
        if needle in row["action"] or re.search(
            r"(?<![A-Za-z0-9_-])" + re.escape(skill) + r"(?![A-Za-z0-9_-])",
            row["action"],
        ):
            return row
    return None


def iter_commands(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        command = value.get("command")
        if isinstance(command, str):
            yield command
        for child in value.values():
            yield from iter_commands(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_commands(child)


def load_hook_commands(repo: Path, event: str) -> List[Tuple[Path, str]]:
    result: List[Tuple[Path, str]] = []
    for relative in HOOK_CONFIGS:
        path = repo / relative
        if not path.is_file():
            continue
        try:
            data = json.loads(read_text(path))
        except (OSError, json.JSONDecodeError):
            continue
        hooks = data.get("hooks") if isinstance(data, dict) else None
        if not isinstance(hooks, dict):
            continue
        event_value = hooks.get(event)
        if event_value is None:
            continue
        result.extend((path, command) for command in iter_commands(event_value))
    return result


def command_source_paths(repo: Path, command: str) -> List[Path]:
    paths: List[Path] = []
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()
    for token in tokens:
        token = token.strip("'\"")
        if token.startswith("-") or token.startswith("$"):
            continue
        if not (token.endswith((".py", ".js", ".sh")) or "hook" in token or "workflow" in token):
            continue
        candidate = Path(token)
        if not candidate.is_absolute():
            candidate = repo / candidate
        if candidate.is_file() and candidate not in paths:
            paths.append(candidate)
    return paths


class Verification:
    def __init__(self, repo: Path, manifest_path: Path, smoke: bool) -> None:
        self.repo = repo
        self.manifest_path = manifest_path
        self.smoke = smoke
        self.passes: List[str] = []
        self.failures: List[str] = []
        self.manifest: Dict[str, Any] = {}
        self.workflow = ""
        self.states: Dict[str, str] = {}
        self.routes: List[Dict[str, Any]] = []
        self.hook_commands: List[Tuple[Path, str]] = []

    def ok(self, message: str) -> None:
        self.passes.append(message)

    def fail(self, message: str) -> None:
        self.failures.append(message)

    def load(self) -> bool:
        workflow_path = self.repo / ".trellis" / "workflow.md"
        if not workflow_path.is_file():
            self.fail("missing .trellis/workflow.md")
        else:
            try:
                self.workflow = read_text(workflow_path)
                self.states = parse_state_blocks(self.workflow)
                self.ok("Trellis workflow exists and state blocks are parseable")
            except OSError as exc:
                self.fail("cannot read .trellis/workflow.md: %s" % exc)

        if not self.manifest_path.is_file():
            self.fail("missing %s; installation or prose routing is not integration proof" % self.manifest_path)
            return False
        try:
            data = json.loads(read_text(self.manifest_path))
        except (OSError, json.JSONDecodeError) as exc:
            self.fail("invalid integration manifest %s: %s" % (self.manifest_path, exc))
            return False
        if not isinstance(data, dict):
            self.fail("integration manifest must be a JSON object")
            return False
        self.manifest = data
        if data.get("schema") != 1:
            self.fail("integration manifest schema must be 1")
        else:
            self.ok("integration manifest schema is 1")
        routes = data.get("routes")
        if not isinstance(routes, list) or not routes:
            self.fail("integration manifest must declare at least one route")
            return False
        self.routes = [route for route in routes if isinstance(route, dict)]
        if len(self.routes) != len(routes):
            self.fail("integration manifest routes must contain only objects")
        return True

    def check_states(self) -> None:
        required = list(DEFAULT_STATES)
        if (self.repo / ".codex/hooks.json").is_file():
            required.extend(INLINE_STATES)
        declared = self.manifest.get("required_states")
        if isinstance(declared, list) and declared:
            required = [str(state) for state in declared]
        for state in dict.fromkeys(required):
            body = self.states.get(state)
            if not body:
                self.fail("workflow is missing non-empty [workflow-state:%s]" % state)
            else:
                self.ok("workflow-state:%s is present" % state)

    def skill_path(self, skill: str) -> Optional[Path]:
        candidates = tuple(self.repo / root / skill / "SKILL.md" for root in SKILL_ROOTS)
        return next((path for path in candidates if path.is_file()), None)

    def check_route(self, route: Dict[str, Any], rows: Sequence[Dict[str, str]]) -> None:
        skill = route.get("skill")
        if not isinstance(skill, str) or not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", skill):
            self.fail("route has invalid skill name: %r" % (skill,))
            return
        mode = route.get("mode")
        phase = route.get("phase")
        trigger = route.get("trigger")
        artifacts = route.get("artifacts")
        gate = route.get("gate")
        if mode not in ("automatic", "explicit", "conditional"):
            self.fail("%s: mode must be automatic, explicit, or conditional" % skill)
        if phase not in PHASE_STATES:
            self.fail("%s: unknown phase %r" % (skill, phase))
        if not isinstance(trigger, str) or not trigger.strip():
            self.fail("%s: trigger is required" % skill)
        if not isinstance(artifacts, list) or not artifacts or not all(
            isinstance(item, str) and item.strip() for item in artifacts
        ):
            self.fail("%s: at least one durable artifact is required" % skill)
        if not isinstance(gate, str) or not gate.strip():
            self.fail("%s: gate is required" % skill)

        skill_path = self.skill_path(skill)
        if skill_path is None:
            self.fail("%s: no supported project-local skill source" % skill)
            return
        frontmatter = parse_frontmatter(skill_path)
        if frontmatter.get("name") != skill:
            self.fail("%s: SKILL.md frontmatter name does not match" % skill)
        disabled = frontmatter.get("disable-model-invocation", "").lower() == "true"
        if disabled and mode != "explicit":
            self.fail("%s: disable-model-invocation=true requires mode=explicit" % skill)
        elif disabled:
            self.ok("%s: explicit-only invocation matches frontmatter" % skill)
        else:
            self.ok("%s: model-invocation mode is compatible with frontmatter" % skill)

        row = route_row(rows, skill)
        if row is None:
            self.fail("%s: no route-table row" % skill)
            return
        row_text = " ".join(row.values())
        if mode == "explicit" and not re.search(r"explicit|user[- ]invok", row_text, re.IGNORECASE):
            self.fail("%s: explicit route is not declared explicit in workflow" % skill)
        if mode == "automatic" and re.search(r"explicit|user[- ]invok", row_text, re.IGNORECASE):
            self.fail("%s: automatic route is described as explicit in workflow" % skill)

        states = PHASE_STATES.get(phase, ())
        matching_states = []
        for state in states:
            if state in self.states:
                matching_states.append(state)
            inline = state + "-inline"
            if inline in self.states:
                matching_states.append(inline)
        state_text = "\n".join(self.states.get(state, "") for state in matching_states)
        if not state_text or ("/" + skill not in state_text and skill not in state_text):
            self.fail("%s: route is not bound to the %s workflow-state block" % (skill, phase))
        else:
            self.ok("%s: route is bound to %s" % (skill, phase))

        artifact_names = [Path(item).name for item in artifacts if isinstance(item, str)]
        if not any(name and name in row_text for name in artifact_names):
            self.fail("%s: route handoff does not name one of its artifacts" % skill)
        else:
            self.ok("%s: route names a durable Trellis handoff" % skill)

    def check_routes(self) -> None:
        section = section_after_heading(self.workflow, "### Skill Routing")
        if not section:
            self.fail("workflow is missing ### Skill Routing")
            return
        rows = parse_route_rows(section)
        if not rows:
            self.fail("### Skill Routing contains no route rows")
            return
        self.ok("skill routing table contains %d route(s)" % len(rows))
        for route in self.routes:
            self.check_route(route, rows)

    def check_review_order(self) -> None:
        review_order = self.manifest.get("review_order")
        if not isinstance(review_order, list) or not review_order:
            self.fail("review_order is required; it prevents third-party review from replacing Trellis check")
            return
        if "code-review" not in [route.get("skill") for route in self.routes]:
            self.ok("review_order declared")
            return
        if not review_order or review_order[0] != "trellis-check":
            self.fail("review_order must start with trellis-check")
            return
        body = "\n".join(
            self.states.get(state, "") for state in ("in_progress", "in_progress-inline")
        ).lower()
        trellis_index = body.find("trellis-check")
        review_index = body.find("code-review")
        if trellis_index < 0 or review_index < 0 or trellis_index > review_index:
            self.fail("workflow must place trellis-check before code-review")
        else:
            self.ok("Trellis check precedes independent code review")

    def check_hooks(self) -> None:
        hook = self.manifest.get("hook")
        if not isinstance(hook, dict):
            self.fail("integration manifest must declare hook.event, command_contains, and output_markers")
            return
        event = hook.get("event")
        contains = hook.get("command_contains")
        markers = hook.get("output_markers")
        if not isinstance(event, str) or not event:
            self.fail("hook.event is required")
            return
        if isinstance(contains, str):
            contains = [contains]
        if not isinstance(contains, list) or not contains or not all(isinstance(item, str) for item in contains):
            self.fail("hook.command_contains must be a non-empty string list")
            return
        if not isinstance(markers, list) or not markers or not all(isinstance(item, str) for item in markers):
            self.fail("hook.output_markers must be a non-empty string list")
            return
        self.hook_commands = load_hook_commands(self.repo, event)
        if not self.hook_commands:
            self.fail("no %s hook command found in supported project config" % event)
            return
        matching = [
            item for item in self.hook_commands if all(expected in item[1] for expected in contains)
        ]
        if not matching:
            self.fail("configured %s hook does not contain %s" % (event, ", ".join(contains)))
            return
        self.ok("%s hook is configured" % event)
        source_paths: List[Path] = []
        for _, command in matching:
            for path in command_source_paths(self.repo, command):
                if path not in source_paths:
                    source_paths.append(path)
        if not source_paths:
            self.fail("hook command does not resolve to a readable source file")
            return
        source_text = "\n".join(read_text(path) for path in source_paths)
        for marker in ("workflow.md", "workflow-state"):
            if marker not in source_text:
                self.fail("hook source does not read/inject %s" % marker)
        if not any(marker in source_text for marker in ("additionalContext", "hookSpecificOutput", "print(")):
            self.fail("hook source has no recognizable context output")
        else:
            self.ok("hook source reads workflow state and emits context")

    def smoke_hook(self) -> None:
        if not self.smoke or not self.hook_commands:
            return
        hook = self.manifest.get("hook")
        if not isinstance(hook, dict):
            return
        contains = hook.get("command_contains")
        if isinstance(contains, str):
            contains = [contains]
        matching = [
            command for _, command in self.hook_commands
            if isinstance(contains, list) and all(expected in command for expected in contains)
        ]
        if not matching:
            return
        payload = {
            "cwd": str(self.repo),
            "prompt": "trellis workflow enhancer integration smoke test",
            "session_id": "trellis-workflow-enhancer-smoke",
        }
        try:
            result = subprocess.run(
                matching[0],
                shell=True,
                cwd=str(self.repo),
                input=json.dumps(payload),
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15,
                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            self.fail("hook smoke test could not run: %s" % exc)
            return
        if result.returncode != 0:
            self.fail("hook smoke test exited %d: %s" % (result.returncode, result.stderr.strip()))
            return
        output = result.stdout
        markers = hook.get("output_markers", [])
        missing = [marker for marker in markers if marker not in output]
        if missing:
            self.fail("hook smoke output is missing %s" % ", ".join(missing))
        else:
            self.ok("hook smoke output contains the declared runtime markers")

    def run(self) -> int:
        if not self.load():
            return self.report()
        self.check_states()
        self.check_routes()
        self.check_review_order()
        self.check_hooks()
        self.smoke_hook()
        return self.report()

    def report(self) -> int:
        for message in self.passes:
            print("PASS: " + message)
        for message in self.failures:
            print("FAIL: " + message)
        print("\nIntegration proof: %d passed, %d failed" % (len(self.passes), len(self.failures)))
        return 1 if self.failures else 0


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify real Trellis/Matt/Waza runtime integration, not just installed files."
    )
    parser.add_argument("repo", type=Path, help="target Trellis repository")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="integration manifest relative to repo (default: %(default)s)",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="execute the configured UserPromptSubmit hook once with a synthetic payload",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo = args.repo.resolve()
    manifest = args.manifest if args.manifest.is_absolute() else repo / args.manifest
    if not repo.is_dir():
        print("FAIL: target repository does not exist: %s" % repo)
        return 1
    return Verification(repo, manifest, args.smoke).run()


if __name__ == "__main__":
    sys.exit(main())
