"""Kuro project scaffolding and built-in templates."""
from __future__ import annotations

from pathlib import Path


def create_project(destination: str | Path) -> Path:
    root = Path(destination)
    if root.exists() and any(root.iterdir()):
        raise ValueError(f"project directory is not empty: {root}")
    root.mkdir(parents=True, exist_ok=True)
    (root / "src").mkdir(exist_ok=True)
    name = root.name.replace(" ", "-").lower()
    files = {
        "kuro.package": f'name = "{name}"\nversion = "0.1.0"\nentry = "src/main.kuro"\n',
        "src/main.kuro": 'Print "Hello from Kuro".\n',
        ".gitignore": "build/\nkuro.lock\n",
        "README.md": f"# {name}\n\nBuild with `kuro bundle src/main.kuro`.\n",
    }
    for relative, content in files.items():
        (root / relative).write_text(content, encoding="utf-8")
    return root
