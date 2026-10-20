import os
import tempfile
import unittest
from archify.scanner import scan_architecture
from archify.renderers import generate_html, generate_svg

class TestArchify(unittest.TestCase):
    def test_scan_architecture(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            src_dir = os.path.join(tmpdir, "src")
            os.makedirs(src_dir)
            with open(os.path.join(src_dir, "main.py"), "w") as f:
                f.write("print('hello')\n")

            with open(os.path.join(tmpdir, "README.md"), "w") as f:
                f.write("# Sample Project\n")

            data = scan_architecture(tmpdir)
            self.assertEqual(data["total_nodes"], 2)
            self.assertEqual(data["total_files"], 2)
            node_names = [n["name"] for n in data["nodes"]]
            self.assertIn("src", node_names)
            self.assertIn("README.md", node_names)

    def test_generate_html(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "app.py"), "w") as f:
                f.write("import sys\n")

            out_html = os.path.join(tmpdir, "arch.html")
            path = generate_html(tmpdir, out_html)
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("Architecture Map", content)
                self.assertIn("app.py", content)

    def test_generate_svg(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "main.go"), "w") as f:
                f.write("package main\n")

            out_svg = os.path.join(tmpdir, "arch.svg")
            path = generate_svg(tmpdir, out_svg)
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("<svg", content)
                self.assertIn("main.go", content)

if __name__ == "__main__":
    unittest.main()
