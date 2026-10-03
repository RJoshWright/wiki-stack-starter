"""Checks for .claude/hooks/wiki_hooks.py and its wiring in .claude/settings.json.

Run from the repo root:  python -m unittest discover -s tests -v
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS = REPO_ROOT / ".claude" / "hooks" / "wiki_hooks.py"
SETTINGS = REPO_ROOT / ".claude" / "settings.json"

spec = importlib.util.spec_from_file_location("wiki_hooks", HOOKS)
wiki_hooks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wiki_hooks)

CLEAN_PAGE = """---
type: concept
title: "Pricing Strategy"
sources: ["[[summary-setup-interview|Setup Interview]]"]
related: ["[[acme-widgets|Acme Widgets]]"]
cluster: market
cluster_role: member
---

# Pricing Strategy

[[acme-widgets|Acme Widgets]] sets list prices yearly.

| Company | Note |
|---|---|
| [[summit-group\\|Summit Group]] | Discounts often |
"""


def run_hook(cmd, payload):
    out = subprocess.run([sys.executable, str(HOOKS), cmd], input=json.dumps(payload),
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


class CheckPageTests(unittest.TestCase):
    def check(self, text, content_page=True):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.md"
            path.write_text(text, encoding="utf-8")
            return wiki_hooks.check_page(path, content_page)

    def assertFlags(self, text, fragment, content_page=True):
        issues = self.check(text, content_page)
        self.assertTrue(any(fragment in i for i in issues), f"expected '{fragment}' in {issues}")

    def test_clean_page_passes(self):
        self.assertEqual(self.check(CLEAN_PAGE), [])

    def test_missing_frontmatter(self):
        self.assertFlags("# No frontmatter\n", "No YAML frontmatter")

    def test_unquoted_frontmatter_link(self):
        self.assertFlags(CLEAN_PAGE.replace('related: ["[[acme-widgets|Acme Widgets]]"]',
                                            "related: [[acme-widgets|Acme Widgets]]"), "not quoted")

    def test_link_without_display_name(self):
        self.assertFlags(CLEAN_PAGE + "\nSee [[acme-widgets]].\n", "without a proper display name")

    def test_unescaped_pipe_in_table(self):
        self.assertFlags(CLEAN_PAGE.replace("summit-group\\|", "summit-group|"), "unescaped pipe")

    def test_placeholder_only_flagged_on_content_pages(self):
        page = CLEAN_PAGE + "\nOwner: {{OWNER_NAME}}\n"
        self.assertFlags(page, "Placeholder")
        self.assertEqual(self.check(page, content_page=False), [])

    def test_filled_navigation_file_is_checked(self):
        self.assertFlags(CLEAN_PAGE + "\nSee [[acme-widgets]].\n", "display name", content_page=False)

    def test_cluster_rules(self):
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML not installed; cluster checks are skipped without it")
        self.assertFlags(CLEAN_PAGE.replace("cluster: market\n", ""), "no `cluster:`")
        self.assertFlags(CLEAN_PAGE.replace("cluster_role: member", "cluster_role: hub"), "In this cluster")


class HookCommandTests(unittest.TestCase):
    def test_pre_blocks_raw(self):
        result = run_hook("pre", {"tool_input": {"file_path": str(REPO_ROOT / "raw" / "papers" / "x.pdf")}})
        self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_pre_allows_wiki(self):
        self.assertEqual(run_hook("pre", {"tool_input": {"file_path": str(REPO_ROOT / "wiki" / "hot.md")}}), {})

    def test_post_ignores_files_outside_wiki(self):
        self.assertEqual(run_hook("post", {"tool_input": {"file_path": str(REPO_ROOT / "README.md")}}), {})

    def test_post_passes_navigation_templates(self):
        # Before setup the navigation files hold {{PLACEHOLDERS}}; they must not be blocked.
        for name in ("index.md", "overview.md", "hot.md"):
            with self.subTest(file=name):
                self.assertEqual(run_hook("post", {"tool_input": {"file_path": str(REPO_ROOT / "wiki" / name)}}), {})

    def test_settings_wire_both_hooks(self):
        hooks = json.loads(SETTINGS.read_text(encoding="utf-8"))["hooks"]
        self.assertIn("wiki_hooks.py\" pre", hooks["PreToolUse"][0]["hooks"][0]["command"])
        self.assertIn("wiki_hooks.py\" post", hooks["PostToolUse"][0]["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
