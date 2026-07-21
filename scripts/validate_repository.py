
"""Run static, privacy, and structural validation of the public repository."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
EXPECTED_NOTEBOOKS = [
    "01_download_and_merge.ipynb",
    "02_sample_and_labels.ipynb",
    "03_descriptive_analysis.ipynb",
    "04_logistic_regression.ipynb",
    "05_ebm_analysis.ipynb",
    "06_performance_and_thresholds.ipynb",
    "07_fairness_and_subgroup_analysis.ipynb",
    "08_sensitivity_analysis.ipynb",
    "09_final_outputs.ipynb",
]

PRIVATE_PATH_PATTERNS = [
    re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
    re.compile(r"/Users/"),
    re.compile(r"/home/[^/]+/"),
]
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|access[_-]?token|secret|password)\s*[:=]"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
]


def validate_notebook(path: Path) -> list[str]:
    errors: list[str] = []
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    for cell_index, cell in enumerate(notebook.cells):
        if cell.cell_type != "code":
            continue
        if cell.get("outputs"):
            errors.append(f"{path.name}: code cell {cell_index} contains saved outputs")
        if cell.get("execution_count") is not None:
            errors.append(f"{path.name}: code cell {cell_index} has an execution count")
        try:
            ast.parse(cell.source)
        except SyntaxError as exc:
            errors.append(f"{path.name}: code cell {cell_index} syntax error: {exc}")
    text = path.read_text(encoding="utf-8")
    for pattern in PRIVATE_PATH_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.name}: possible user-specific absolute path")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            errors.append(f"{path.name}: possible embedded secret")
    return errors


def main() -> int:
    errors: list[str] = []
    for notebook_name in EXPECTED_NOTEBOOKS:
        path = NOTEBOOK_DIR / notebook_name
        if not path.exists():
            errors.append(f"Missing notebook: {path}")
            continue
        errors.extend(validate_notebook(path))

    required_root_files = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "CITATION.cff",
    ]
    for filename in required_root_files:
        if not (ROOT / filename).exists():
            errors.append(f"Missing repository file: {filename}")

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository static validation passed.")
    print(f"Validated {len(EXPECTED_NOTEBOOKS)} output-free notebooks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
