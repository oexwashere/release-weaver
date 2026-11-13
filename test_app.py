import unittest
import app


class Tests(unittest.TestCase):
    def test_scopes_breaking_and_deduplication(self):
        r = app.parse(
            [
                "abcdef1 feat(api)!: replace endpoint",
                "fix: repair",
                "fix: repair",
                "Merge branch",
            ]
        )
        self.assertEqual(len(r["entries"]), 2)
        self.assertTrue(r["entries"][0]["breaking"])
        self.assertEqual(r["unparsed"], ["Merge branch"])

    def test_markdown_groups_and_links(self):
        r = app.parse(["abcdef1 feat(ui): add preview", "fix: close dialog"])
        text = app.markdown(r, "v1.0", "2026-01-01", "https://github.com/a/b")
        self.assertIn("## Features", text)
        self.assertIn("/commit/abcdef1", text)
        self.assertIn("## Fixes", text)

    def test_escaped_subjects(self):
        text = app.markdown(app.parse(["docs: <script> & [link]"]), "v1", "2026-01-01")
        self.assertIn("\\<script\\>", text)
        self.assertIn("\\[link\\]", text)

    def test_invalid_metadata(self):
        with self.assertRaises(ValueError):
            app.markdown(app.parse([]), "v1", "bad")
        with self.assertRaises(ValueError):
            app.markdown(app.parse([]), "v1", "2026-01-01", "javascript:x")


if __name__ == "__main__":
    unittest.main()
