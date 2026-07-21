
"""Execute the numbered notebook pipeline into outputs/executed_notebooks."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
OUTPUT_DIR = ROOT / "outputs" / "executed_notebooks"
NOTEBOOKS = [
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


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for notebook_name in NOTEBOOKS:
        source = NOTEBOOK_DIR / notebook_name
        output_name = notebook_name.replace(".ipynb", "_executed.ipynb")
        print(f"Executing {notebook_name} ...", flush=True)
        command = [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            str(source),
            "--output",
            output_name,
            "--output-dir",
            str(OUTPUT_DIR),
            "--ExecutePreprocessor.timeout=-1",
        ]
        subprocess.run(command, cwd=ROOT, check=True)
    print(f"Executed notebooks written to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
