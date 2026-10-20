"""
CLI Entrypoint for archify
"""

import os
import sys
import json
import argparse
import subprocess
from .scanner import scan_architecture
from .renderers import generate_html, generate_svg

def main():
    parser = argparse.ArgumentParser(
        prog="archify",
        description="Zero-dependency Interactive SVG and HTML Architecture Visualizer"
    )
    parser.add_argument("path", nargs="?", default=".", help="Target project directory to analyze")
    parser.add_argument("-o", "--output", help="Output path for HTML report")
    parser.add_argument("--svg", help="Generate SVG architecture diagram at path")
    parser.add_argument("--json", action="store_true", help="Output architecture metadata as JSON")
    parser.add_argument("--open", action="store_true", help="Open generated HTML immediately in default browser")

    args = parser.parse_args()

    if args.json:
        data = scan_architecture(args.path)
        print(json.dumps(data, indent=2))
        return

    html_path = generate_html(args.path, args.output)
    print(f"✅ Interactive HTML Architecture Map: {html_path}")

    if args.svg:
        svg_path = generate_svg(args.path, args.svg)
        print(f"✅ SVG Architecture Diagram: {svg_path}")

    if args.open:
        if sys.platform == "darwin":
            subprocess.Popen(["open", html_path])
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", html_path])
        elif sys.platform == "win32":
            os.startfile(html_path)

if __name__ == "__main__":
    main()
