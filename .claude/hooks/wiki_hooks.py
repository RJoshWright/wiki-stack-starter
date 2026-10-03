"""Claude Code hooks that keep the wiki a reliable source of truth.

One script, one subcommand per hook event (wired up in .claude/settings.json):
  pre    PreToolUse  (Write|Edit|NotebookEdit)  block edits to files under raw/
  post   PostToolUse (Write|Edit)               check a wiki page against the CLAUDE.md conventions

Each reads the hook's JSON on stdin and answers with JSON on stdout.
Standard library only; if PyYAML is installed, frontmatter is also checked for valid YAML.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"

# Navigation and record files that don't follow the page schemas.
SKIP_CHECKS = {"log.md", "dashboard.md"}
# Folders holding content pages (placeholders are allowed in navigation files before setup).
CONTENT_DIRS = {"concepts", "entities", "sources", "comparisons", "syntheses"}
PLACEHOLDER = re.compile(r"\{\{?[A-Z][A-Z0-9_]+\}\}?")
TABLE_LINK_PIPE = re.compile(r"\[\[[^\]]*?(?<!\\)\|")


def read_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def emit(obj):
    print(json.dumps(obj))
    sys.exit(0)


def target_path(data):
    ti = data.get("tool_input") or {}
    p = ti.get("file_path") or ti.get("notebook_path") or ""
    if not p:
        return None
    path = Path(p)
    if not path.is_absolute():
        path = Path(data.get("cwd") or ROOT) / path
    return path.resolve()


def is_under(path, root):
    try:
        path.relative_to(root.resolve())
        return True
    except ValueError:
        return False


# ---------- pre: raw/ is read-only ----------
def pre(data):
    path = target_path(data)
    if path and is_under(path, RAW):
        emit({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"raw/ is immutable (CLAUDE.md Safety Rules): {path.relative_to(ROOT).as_posix()}. "
                    "Record facts in wiki/sources/ instead. If the user asked to file a new source "
                    "document into raw/, ask them to copy it there unchanged."
                ),
            }
        })
    emit({})


# ---------- post: wiki page conventions ----------
def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def check_page(path, content_page=True):
    """Return a list of convention problems on one wiki page (empty when it's clean)."""
    text = path.read_text(encoding="utf-8")
    if not content_page and PLACEHOLDER.search(text):
        return []  # a navigation template that setup-wiki hasn't filled yet
    fm, body = split_frontmatter(text)
    if fm is None:
        return ["No YAML frontmatter (every wiki page must have it)."]
    issues = []

    meta = None
    try:
        import yaml
        meta = yaml.safe_load(fm)
        if not isinstance(meta, dict):
            issues.append("Frontmatter is not a YAML mapping.")
            meta = None
    except ImportError:
        pass
    except Exception as e:
        issues.append(f"Frontmatter is not valid YAML: {str(e).splitlines()[0]}")

    for n, line in enumerate(fm.splitlines(), 2):
        if re.search(r'(?<!["\'])\[\[', line):
            issues.append(f"Frontmatter line {n}: wiki-link not quoted, use [\"[[slug|Name]]\", ...]: {line.strip()[:90]}")

    if meta:  # without PyYAML, the cluster checks are skipped
        ptype = meta.get("type")
        if ptype in ("concept", "entity") and not meta.get("cluster"):
            issues.append(f"`type: {ptype}` page has no `cluster:` field.")
        if meta.get("cluster_role") == "hub" and "## In this cluster" not in body:
            issues.append("`cluster_role: hub` page has no `## In this cluster` section.")

    unpiped = sorted(set(re.findall(r"\[\[([^\]|#\\]+)\]\]", text)))
    if unpiped:
        issues.append("Wiki-links without a proper display name (use [[slug|Proper Name]]): "
                      + ", ".join(unpiped[:8]))

    for n, line in enumerate(body.splitlines(), 1):
        if line.lstrip().startswith("|") and TABLE_LINK_PIPE.search(line):
            issues.append(f"Table row with an unescaped pipe in a wiki-link (use [[slug\\|Name]]): {line.strip()[:90]}")
            break

    if content_page:
        left = sorted(set(PLACEHOLDER.findall(text)))
        if left:
            issues.append("Placeholder left in the page: " + ", ".join(left[:5]))
    return issues


def post(data):
    path = target_path(data)
    if not path or path.suffix != ".md" or not is_under(path, WIKI) or path.name in SKIP_CHECKS:
        emit({})
    if not path.exists():
        emit({})
    content_page = path.relative_to(WIKI.resolve()).parts[0] in CONTENT_DIRS
    issues = check_page(path, content_page)
    if not issues:
        emit({})
    rel = path.relative_to(ROOT).as_posix()
    emit({
        "decision": "block",
        "reason": f"Wiki convention check on {rel}:\n- " + "\n- ".join(issues)
                  + "\nFix these (or say why they're intended) before moving on.",
    })


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    handlers = {"pre": pre, "post": post}
    if cmd not in handlers:
        sys.exit(0)
    try:
        handlers[cmd](read_input())
    except SystemExit:
        raise
    except Exception as e:  # never break the session over a hook bug
        print(json.dumps({"systemMessage": f"wiki hook '{cmd}' error: {e}"}))
        sys.exit(0)
