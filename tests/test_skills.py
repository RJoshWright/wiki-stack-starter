"""Structural checks for every skill in .claude/skills/*/SKILL.md.

Run from the repo root:  python -m unittest discover -s tests -v
"""
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.DOTALL)  # example syntax, not real links
MAX_DESCRIPTION = 1024


def split_frontmatter(text):
    """Return (frontmatter dict, body) or (None, text) if there is no frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            meta = {}
            for raw in lines[1:i]:
                if ":" in raw and not raw.startswith((" ", "\t")):
                    key, value = raw.split(":", 1)
                    meta[key.strip()] = value.strip().strip("\"'")
            return meta, "\n".join(lines[i + 1:])
    return None, text


def skill_files():
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


class SkillFileTests(unittest.TestCase):
    def test_skills_exist(self):
        self.assertTrue(skill_files(), f"no SKILL.md files found under {SKILLS_DIR}")

    def test_skill_structure(self):
        for path in skill_files():
            folder = path.parent.name
            with self.subTest(skill=folder):
                meta, body = split_frontmatter(path.read_text(encoding="utf-8-sig"))
                self.assertIsNotNone(meta, "missing or unclosed --- frontmatter")

                name = meta.get("name", "")
                description = meta.get("description", "")
                self.assertTrue(name, "frontmatter has no name")
                self.assertTrue(description, "frontmatter has no description")
                self.assertEqual(name, folder, "name must match the skill folder")
                self.assertRegex(name, SLUG_RE, "name must be lowercase kebab-case")
                self.assertLessEqual(len(description), MAX_DESCRIPTION, "description too long")

                self.assertTrue(body.strip(), "body is empty")
                self.assertRegex(body, r"(?m)^#{1,6} ", "body has no heading")

    def test_relative_links_resolve(self):
        for path in skill_files():
            body = split_frontmatter(path.read_text(encoding="utf-8-sig"))[1]
            for target in LINK_RE.findall(CODE_RE.sub("", body)):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                file_part = target.split("#", 1)[0]
                with self.subTest(skill=path.parent.name, link=target):
                    self.assertTrue((path.parent / file_part).exists(), f"broken link: {target}")


class SplitFrontmatterTests(unittest.TestCase):
    def test_parses_keys_and_body(self):
        meta, body = split_frontmatter("---\nname: demo\ndescription: \"A demo\"\n---\n# Demo\n")
        self.assertEqual(meta, {"name": "demo", "description": "A demo"})
        self.assertEqual(body.strip(), "# Demo")

    def test_rejects_missing_or_unclosed_frontmatter(self):
        self.assertIsNone(split_frontmatter("# No frontmatter\n")[0])
        self.assertIsNone(split_frontmatter("---\nname: demo\n# never closed\n")[0])


if __name__ == "__main__":
    unittest.main()
