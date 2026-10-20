# 🏛️ archify-py

[![CI](https://github.com/apravint/archify-py/actions/workflows/ci.yml/badge.svg)](https://github.com/apravint/archify-py/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)

> **Zero-dependency, instantaneous interactive SVG and HTML architecture visualizer for software projects.**  
> Scans codebases, classifies modules and entrypoints, detects languages, and renders interactive glassmorphic HTML maps or embeddable SVG diagrams.

---

## ⚡ Key Highlights

- 🪶 **Zero Dependencies:** Pure Python standard library (`os`, `json`, `datetime`, `argparse`). No heavy AST parsers or Node.js toolchains needed.
- 🎨 **Modern Glassmorphic HTML:** Renders a clean dark-themed dashboard with live client-side search filtering.
- 📐 **GitHub-Ready SVG:** Generates crisp, scalable vector graphics suitable for embedding directly in repository `README.md` files.
- ⚡ **Instantaneous:** Analyzes massive repositories and builds full visual maps in milliseconds.

---

## 🚀 Quick Start

### Installation

```bash
pip install archify-py
```

Or install from source:

```bash
git clone https://github.com/apravint/archify-py.git
cd archify-py
pip install -e .
```

### Usage

```bash
# Generate interactive HTML architecture map in current directory
archify .

# Generate both HTML and embeddable SVG diagram
archify . --svg architecture.svg

# Open directly in your browser
archify /path/to/repo --open

# Output architecture tree and language metrics as JSON
archify . --json
```

---

## 🐍 Python API

```python
from archify import scan_architecture, generate_html, generate_svg

# Scan repo structure and metrics
data = scan_architecture("/path/to/project")
print(f"Total modules: {data['total_nodes']}, Total files: {data['total_files']}")

# Generate HTML map
html_file = generate_html("/path/to/project", output_path="map.html")

# Generate SVG diagram
svg_file = generate_svg("/path/to/project", output_path="arch.svg")
```

---

## 🧪 Testing

```bash
python3 -m unittest discover tests
```

---

## 📄 License

MIT License. Crafted with ❤️ by [apravint](https://github.com/apravint).
