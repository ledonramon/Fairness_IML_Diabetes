# When Explanations Explain Labels

## Target Definition, Interpretability, and Fairness in Diabetes Prediction

This repository contains the complete computational pipeline for a research paper comparing two operational diabetes targets in NHANES August 2021--August 2023:

1. prior reported clinician diagnosis;
2. current HbA1c of at least 6.5%.

The analysis holds participants, predictors, preprocessing, and fixed folds constant while comparing logistic regression with a strictly additive Explainable Boosting Machine. It evaluates target concordance, out-of-fold predictive performance, model interpretation, subgroup false-negative-rate gaps, operating-threshold sensitivity, and sensitivity to removing race/ethnicity as a predictor.

The repository does not treat either operational target as universal clinical ground truth, and the analyses are associational rather than causal.

## Repository structure

```text
.
├── notebooks/                  # Numbered analytical pipeline
├── scripts/                    # Pipeline execution and static validation
├── data/
│   ├── raw/                    # Official NHANES XPT files; not versioned
│   └── processed/              # Derived participant-level data; not versioned
├── outputs/
│   ├── tables/                 # Intermediate tables; not versioned
│   ├── figures/                # Intermediate figures; not versioned
│   ├── models/                 # Fitted models; not versioned
│   └── final/                  # Paper-ready artifacts may be versioned
├── requirements.txt
├── requirements-lock.txt
├── CITATION.cff
├── .gitignore
└── README.md
```

## Data

Notebook 01 downloads five public-use NHANES files from the official NCHS August 2021--August 2023 release:

- `DEMO_L.xpt` — demographics, socioeconomic variables, examination weights, and survey-design variables;
- `DIQ_L.xpt` — diabetes questionnaire and treatment variables;
- `GHB_L.xpt` — glycohemoglobin;
- `BMX_L.xpt` — body measurements;
- `HIQ_L.xpt` — health-insurance variables.

Raw NHANES files and derived participant-level data are not redistributed in this repository. Notebook 01 downloads the official source files when they are absent and reconstructs the analytical datasets. Use of NHANES data remains subject to the NCHS Data User Agreement.

## Environment setup

The executed notebook metadata recorded Python 3.11.0, pandas 3.0.3, Matplotlib 3.11.0, and InterpretML 0.7.8. `requirements.txt` lists the direct project dependencies and compatible version ranges. `requirements-lock.txt` records the exact packages from the successful final pipeline execution under Windows and Python 3.11.

For the exact tested Windows environment:

```powershell
pip install -r requirements-lock.txt
```

For a smaller and more portable environment:

```powershell
pip install -r requirements.txt
```

### macOS or Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Notebook execution order

1. [`01_download_and_merge.ipynb`](notebooks/01_download_and_merge.ipynb) — Download the required public NHANES August 2021--August 2023 files, validate and merge them by participant identifier, construct project variables and the two operational targets, and create the adult analysis base and complete-case sample.
2. [`02_sample_and_labels.ipynb`](notebooks/02_sample_and_labels.ipynb) — Validate Notebook 01 outputs, document participant flow and missingness, quantify target prevalence and concordance, construct the four joint target groups, and save the labelled complete-case dataset used downstream.
3. [`03_descriptive_analysis.ipynb`](notebooks/03_descriptive_analysis.ipynb) — Describe the analytic sample, compare included and excluded adults, examine target concordance and discordant groups, inspect subgroup cell sizes, and generate descriptive tables and diagnostic figures.
4. [`04_logistic_regression.ipynb`](notebooks/04_logistic_regression.ipynb) — Fit the primary logistic-regression models using one fixed five-fold assignment, generate out-of-fold probabilities, fit full-sample models for interpretation, and estimate coefficient and probability-scale contrasts with paired bootstrap uncertainty.
5. [`05_ebm_analysis.ipynb`](notebooks/05_ebm_analysis.ipynb) — Fit strictly additive Explainable Boosting Machines using the exact folds from Notebook 04, generate out-of-fold probabilities, extract full-sample shape functions, and compare nonlinear predictor relationships across targets and with logistic regression.
6. [`06_performance_and_thresholds.ipynb`](notebooks/06_performance_and_thresholds.ipynb) — Evaluate logistic-regression and EBM out-of-fold probabilities under both targets, estimate paired bootstrap uncertainty, assess calibration, and select fold-specific classification thresholds within training data for 70%, 80%, and 90% sensitivity targets.
7. [`07_fairness_and_subgroup_analysis.ipynb`](notebooks/07_fairness_and_subgroup_analysis.ipynb) — Estimate target- and threshold-specific subgroup performance, reference-group gaps, cross-target gap differences, and paired bootstrap uncertainty for sex, race/ethnicity, income, and insurance history.
8. [`08_sensitivity_analysis.ipynb`](notebooks/08_sensitivity_analysis.ipynb) — Evaluate threshold sensitivity, complete-case selection, descriptive weighting, model-class consistency, and the consequences of removing race/ethnicity from the predictor set while retaining it for subgroup auditing.
9. [`09_final_outputs.ipynb`](notebooks/09_final_outputs.ipynb) — Assemble the final manuscript tables and figures directly from the completed analytical outputs, apply consistent publication formatting, package main and appendix artifacts, and write reproducibility manifests and metadata.

Notebook 09 depends on outputs from Notebook 08 and the completed primary pipeline. Restart the kernel before each notebook and execute cells from top to bottom; no hidden notebook state is intended.

## Reproducing the analysis

From the repository root, either run the notebooks interactively in the documented order or execute the pipeline with:

```bash
python scripts/run_pipeline.py
```

Executed notebook copies are written to `outputs/executed_notebooks/`; the clean source notebooks remain output-free. Full analysis can be computationally intensive because the default pipeline uses 1,000 bootstrap replicates and repeatedly fits logistic-regression and EBM models.

For temporary development runs only, the code recognizes the following environment variables:

- `LOGISTIC_N_BOOTSTRAP`
- `PERFORMANCE_N_BOOTSTRAP`
- `FAIRNESS_N_BOOTSTRAP`
- `NOTEBOOK08_BOOTSTRAP_REPLICATES`
- `NOTEBOOK09_BOOTSTRAP_REPLICATES`

Do not lower these values when reproducing manuscript results.

Run the static repository checks with:

```bash
python scripts/validate_repository.py
```

## Reproducing manuscript outputs

Notebook 09 creates the final main-paper and appendix tables and figures from upstream analytical outputs. Final artifacts are copied to `outputs/final/main/paper_ready`, and machine-readable manifests identify their producing notebook and manuscript location.

All publication-table LaTeX exports use escaped percentages and mathematical inequalities (`\%`, `$<$`, and `$\geq$`). Figures are exported as PDF and PNG, with 300 dpi used for unavoidable rasterized elements.

## Reproducibility design

The analytical pipeline preserves:

- a fixed random seed of 26;
- one five-fold assignment stratified by the four joint target groups;
- identical participants, predictors, folds, and preprocessing across targets;
- EBM interactions disabled in the primary analysis;
- threshold selection confined to outer-training data;
- participant-level paired bootstrap procedures;
- target-specific and threshold-specific subgroup analyses;
- direct generation of manuscript tables and figures from analysis outputs.

The MEC examination weights are used for descriptive complete-case point estimates and are not presented as fully survey-design-adjusted inference.

## Notebook output policy

Public source notebooks contain no saved outputs or execution counts. This removes stale results, local filesystem paths, warning traces, and large embedded figures from version control. Reproducible execution creates separate executed copies and regenerates all analytical artifacts.

## Availability

Analysis code is contained in this repository. Public NHANES source data are obtained from NCHS and are not redistributed.

## Citation

Repository citation metadata are provided in `CITATION.cff`.

## Contact

Ramon Leuenberger — rleuenberger@student.ethz.ch
