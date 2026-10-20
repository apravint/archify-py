"""
Architecture Scanner
Discovers project modules, languages, package types, entrypoints, and metrics.
"""

import os
from typing import List, Dict, Any

IGNORED_DIRS = {
    ".git", "node_modules", "target", "dist", "build", "__pycache__",
    ".venv", "venv", ".tox", ".idea", ".vscode", ".eggs", "*.egg-info"
}

EXTENSION_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "React / TSX",
    ".jsx": "React / JSX",
    ".rs": "Rust",
    ".go": "Go",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C Header",
    ".sh": "Shell Script",
    ".bash": "Bash Script",
    ".md": "Documentation",
    ".json": "JSON Config",
    ".yaml": "YAML Config",
    ".yml": "YAML Config",
    ".toml": "TOML Config",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
    ".service": "Systemd Service"
}

def scan_architecture(target_path: str = ".") -> Dict[str, Any]:
    abs_path = os.path.abspath(os.path.expanduser(target_path))
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Target path does not exist: {abs_path}")

    target_name = os.path.basename(abs_path) or "Project"
    nodes: List[Dict[str, Any]] = []
    total_files = 0
    lang_counts: Dict[str, int] = {}

    if os.path.isdir(abs_path):
        for item in sorted(os.listdir(abs_path)):
            if item in IGNORED_DIRS or item.startswith("."):
                continue

            item_path = os.path.join(abs_path, item)

            if os.path.isdir(item_path):
                # Count files & detect dominant languages
                sub_files = 0
                dir_langs: Dict[str, int] = {}

                for root, dirs, files in os.walk(item_path):
                    dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]
                    for f in files:
                        sub_files += 1
                        ext = os.path.splitext(f)[1].lower()
                        lang = EXTENSION_MAP.get(ext)
                        if lang:
                            dir_langs[lang] = dir_langs.get(lang, 0) + 1
                            lang_counts[lang] = lang_counts.get(lang, 0) + 1

                total_files += sub_files

                # Classify node type
                kind = "Module"
                if os.path.exists(os.path.join(item_path, ".git")):
                    kind = "Sub-Repository"
                elif item in {"bin", "scripts", "cmd"}:
                    kind = "CLI Binaries"
                elif item in {"tests", "test"}:
                    kind = "Test Suite"
                elif item in {"docs", "doc"}:
                    kind = "Documentation"
                elif item in {"config", "configs", "systemd"}:
                    kind = "Configuration & Daemons"
                elif item in {"src", "lib", "pkg"}:
                    kind = "Core Source Package"

                top_lang = max(dir_langs, key=dir_langs.get) if dir_langs else "General"

                nodes.append({
                    "name": item,
                    "kind": kind,
                    "is_dir": True,
                    "language": top_lang,
                    "files": sub_files,
                    "path": item_path
                })

            elif os.path.isfile(item_path):
                total_files += 1
                ext = os.path.splitext(item)[1].lower()
                lang = EXTENSION_MAP.get(ext, "File")
                lang_counts[lang] = lang_counts.get(lang, 0) + 1

                nodes.append({
                    "name": item,
                    "kind": f"{lang} Entrypoint" if ext in {".py", ".sh", ".js", ".ts", ".rs", ".go"} else "File",
                    "is_dir": False,
                    "language": lang,
                    "files": 1,
                    "path": item_path
                })

    return {
        "target_name": target_name,
        "target_path": abs_path,
        "total_nodes": len(nodes),
        "total_files": total_files,
        "language_summary": lang_counts,
        "nodes": nodes
    }
