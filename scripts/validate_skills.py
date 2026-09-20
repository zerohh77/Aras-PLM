#!/usr/bin/env python3
"""Read-only structural and public-hygiene checks for the Skill bundle."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required: python3 -m pip install PyYAML", file=sys.stderr)
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "aras-release30-core",
    "aras-release30-server-csharp",
    "aras-release30-webapi-csharp",
    "aras-release30-client-js",
)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def tracked_files() -> list[Path]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"], cwd=ROOT
    ).decode("utf-8")
    return [ROOT / item for item in output.split("\0") if item]


def read_yaml(path: Path, errors: list[str]) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        fail(errors, f"{path.relative_to(ROOT)}: invalid YAML: {exc}")
        return None


def validate_skill(skill_name: str, errors: list[str]) -> None:
    skill_dir = ROOT / "skills" / skill_name
    skill_file = skill_dir / "SKILL.md"
    metadata_file = skill_dir / "agents" / "openai.yaml"

    for path in (skill_file, metadata_file):
        if not path.is_file():
            fail(errors, f"missing required file: {path.relative_to(ROOT)}")
            return

    text = skill_file.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if not match:
        fail(errors, f"{skill_file.relative_to(ROOT)}: missing YAML frontmatter")
        return

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(errors, f"{skill_file.relative_to(ROOT)}: invalid frontmatter: {exc}")
        return

    if not isinstance(frontmatter, dict):
        fail(errors, f"{skill_file.relative_to(ROOT)}: frontmatter must be a mapping")
        return
    if frontmatter.get("name") != skill_name:
        fail(errors, f"{skill_file.relative_to(ROOT)}: name must match directory")
    if not SKILL_NAME_RE.fullmatch(str(frontmatter.get("name", ""))):
        fail(errors, f"{skill_file.relative_to(ROOT)}: invalid Skill name")
    if not isinstance(frontmatter.get("description"), str) or not frontmatter["description"].strip():
        fail(errors, f"{skill_file.relative_to(ROOT)}: description is required")

    metadata = read_yaml(metadata_file, errors)
    if not isinstance(metadata, dict):
        return
    interface = metadata.get("interface")
    policy = metadata.get("policy")
    if not isinstance(interface, dict):
        fail(errors, f"{metadata_file.relative_to(ROOT)}: interface mapping is required")
        return
    for field in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            fail(errors, f"{metadata_file.relative_to(ROOT)}: interface.{field} is required")
    short_description = interface.get("short_description", "")
    if isinstance(short_description, str) and not 25 <= len(short_description) <= 64:
        fail(errors, f"{metadata_file.relative_to(ROOT)}: short_description must be 25-64 characters")
    default_prompt = interface.get("default_prompt", "")
    if isinstance(default_prompt, str) and f"${skill_name}" not in default_prompt:
        fail(errors, f"{metadata_file.relative_to(ROOT)}: default_prompt must mention ${skill_name}")
    if policy != {"allow_implicit_invocation": True}:
        fail(errors, f"{metadata_file.relative_to(ROOT)}: implicit invocation must remain enabled")


def validate_links(paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            fail(errors, f"{path.relative_to(ROOT)}: unreadable Markdown: {exc}")
            continue
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                continue
            target = unquote(target.split(maxsplit=1)[0])
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                fail(errors, f"{path.relative_to(ROOT)}: broken link: {raw_target}")


def validate_hygiene(paths: list[Path], errors: list[str]) -> None:
    stale_name = "backend" + "-project"
    private_name = "HsAras" + "CommonApi"
    license_name = "M" + "IT"
    user_directory = "Us" + "ers"
    forbidden_patterns = (
        (re.compile(re.escape(stale_name), re.IGNORECASE), "stale Skill name"),
        (re.compile(re.escape(private_name), re.IGNORECASE), "private implementation identifier"),
        (re.compile(r"(?:/|[A-Za-z]:[/\\])" + user_directory + r"[/\\]"), "private filesystem path"),
        (re.compile(re.escape(license_name + " License"), re.IGNORECASE), "accidental license declaration"),
        (re.compile(r"SPDX-License-Identifier:\s*" + re.escape(license_name), re.IGNORECASE), "accidental SPDX declaration"),
        (re.compile(r"\blicense\s*:\s*[\"']?" + re.escape(license_name) + r"\b", re.IGNORECASE), "accidental license metadata"),
        (re.compile(r"-----BEGIN " + r"(?:RSA |EC |OPENSSH )?" + "PRIVATE KEY-----"), "private key"),
        (re.compile(r"\bghp_[A-Za-z0-9]{30,}\b|\bgithub_pat_[A-Za-z0-9_]{30,}\b"), "GitHub token"),
        (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    )

    for path in paths:
        if not path.is_file() or path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".toml", ".py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for pattern, label in forbidden_patterns:
            if pattern.search(text):
                fail(errors, f"{path.relative_to(ROOT)}: contains {label}")

    for path in paths:
        if path.name.casefold() in {"license", "license.txt", "license.md"}:
            fail(errors, f"{path.relative_to(ROOT)}: unexpected repository license file")


def validate_readme(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.is_file():
        fail(errors, "missing README.md")
        return
    text = readme.read_text(encoding="utf-8")
    required = (
        "Release 30",
        "14.0.22.40048",
        "```mermaid",
        "## 安装与使用",
        "## Skill 路由示例",
        "## 证据模型与覆盖边界",
        "## 校验",
        "## 仓库结构",
    )
    for marker in required:
        if marker not in text:
            fail(errors, f"README.md: missing expected marker: {marker}")
    if text.count("```mermaid") != 1 or text.count("```") % 2:
        fail(errors, "README.md: malformed fenced code blocks")


def main() -> int:
    errors: list[str] = []
    paths = tracked_files()

    for shared_file in ("skills/references/COVERAGE.md", "skills/references/SOURCES.md"):
        if not (ROOT / shared_file).is_file():
            fail(errors, f"missing required file: {shared_file}")

    for skill_name in SKILLS:
        validate_skill(skill_name, errors)
    validate_links(paths, errors)
    validate_hygiene(paths, errors)
    validate_readme(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validated {len(SKILLS)} Skills: structure, metadata, links, and repository hygiene are clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
