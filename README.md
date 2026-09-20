# Case Study 2: "Build a Philippine Data Summary Program" - Group 2

**Project Google Drive Link:** https://drive.google.com/drive/folders/1mL3LtozoE_Se__jcpsFeg2_lrlrKungJ?usp=sharing

## Project Description

This project delivers an automated, reproducible Python data processing pipeline designed to ingest, transform, analyze, and audit large-scale Philippine public datasets. Using the **2015 Philippine Customs dataset** (~493.5 MB), the system processes over 2.2 million import transactions to generate summary statistics, create decision-ready data visualizations, and execute rigorous mathematical integrity checks.

The program performs:
1. **Data Ingestion & Cleaning:** Filtered selection and unit processing using Object-Oriented Programming (OOP) design patterns.
2. **Performance Benchmarking:** Comparative analysis evaluating standard Python loop operations against optimized NumPy vectorized calculations on fixed-seed samples.
3. **Summary & Visualization:** Automated output generation for category breakdowns, including Matplotlib bar charts and Seaborn heatmaps.
4. **Data Reconciliation & Audit Logging:** Multi-step programmatic integrity checks (`validation.csv`) and execution tracking (`audit_log.csv`) to guarantee 100% data fidelity against baseline Customs reference totals.

---

## Dataset Information

- **Dataset Name:** Philippine Customs Import Records (2015)
- **Source:** BetterGov.PH (`2015.csv`)
- **File Size:** ~493.5 MB (2,236,612 rows, 30 columns)
- **Baseline Dutiable Value Total:** PHP 3,587,267,375,257.00
- **SHA-256 Checksum:** `b3b5a3a95340179a716a05611d51ad4906484d38363d1ac36494a404c04e4370`

> **Note:** The raw dataset is excluded from version control due to file size constraints. Download `2015.csv` and place it inside the `data/` directory prior to running the program.

---

## Setup Instructions

1. Clone the repository and navigate into it:
   ```bash
   git clone <your-repo-url>
   cd Case-Study-2_Group-2
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download `2015.csv` from the BetterGov.PH Philippine Customs dataset and place it at:
   ```
   data/2015.csv
   ```
   Verify the file's integrity by checking its SHA-256 hash matches:
   `b3b5a3a95340179a716a05611d51ad4906484d38363d1ac36494a404c04e4370`

---

## Filter and Transformation Rules

**Filter conditions** (applied via `.loc` with two conditions):
- `countryorigin_iso3 == "CHN"` — origin country is China
- `dutiablevaluephp > 1000.0` — dutiable value exceeds PHP 1,000
- *Assumption:* shipments with a dutiable value of PHP 1,000 or below are treated as negligible/noise for this analysis and excluded.

**Sorting:** filtered records are sorted by `dutiablevaluephp` in descending order.

**Derived columns:**
- `estimated_vat_php` (numerical) — `dutiablevaluephp * 0.12`, an estimated 12% VAT
- `is_high_value_flag` (category/flag) — `True` if `dutiablevaluephp > 1,000,000`, else `False`

**Missing categories:** rows with missing `countryorigin_iso3` or `tq` values are standardized to an explicit `"MISSING"` placeholder (via `DataCleaner.standardize_missing()`) rather than dropped, so they appear as their own group in all summaries.

**Missing numerical values:** `dutiablevaluephp` is never filled with zero or any placeholder; missing values are reported separately (`valid_measure_count` in `grouped.csv` distinguishes total row count from non-null measure count).

**Field metadata:**
| Field | Meaning |
|---|---|
| `countryorigin_iso3` | Origin country of the import (ISO-3 code) |
| `tq` | Reporting quarter the import was recorded in (e.g. `2015q1`–`2015q4`) |
| `dutiablevaluephp` | Dutiable value in Philippine Pesos (PHP) |

---

## Run Instructions

From the project root, with your virtual environment activated and `data/2015.csv` in place:

```bash
python main.py
```

This runs the full pipeline (load → filter → clean → summarize → plot → benchmark → validate) and writes all outputs to the `outputs/` folder:
`grouped.csv`, `grouped_two.csv`, `pivot.csv`, `top10.csv`, `bar.png`, `heatmap.png`, `validation.csv`, `audit_log.csv`.

If any validation check fails, the program prints the specific discrepancy and exits with a nonzero status.

---

## Plot Descriptions

- **`bar.png`** — Shows the top 10 origin countries ranked by total dutiable value (PHP), after filtering to China-origin shipments over PHP 1,000.
- **`heatmap.png`** — Shows total dutiable value (PHP) broken down by both origin country and reporting quarter, with the margin totals excluded so the color scale reflects only the individual category combinations.

---

## Member Roles & Task Allocation

| Member | Assigned Task / Requirements | Branch Name | Primary Files Owned |
|---|---|---|---|
| **Kate Robyn Alday** | Configuration dictionary & environment setup; control structures for pipeline execution; data structures (audit records, required columns); type hinting lead across modules | `feature/data-structures` | `config.py`, `src/loader.py` |
| **Giana Elisha Tuplano** | OOP implementation: DataCleaner class & 3 methods; module initialization & package structure; pandas `.loc` filtering & derived columns | `feature/oop-cleaner` | `src/cleaner.py`, `src/__init__.py` |
| **Hans Adrian Laudato** | NumPy array conversions & vectorized operations; Boolean masks & aggregation logic; performance benchmark (loop vs. vectorized, 5 runs, fixed seed) | `feature/numpy-benchmark` | `src/benchmark.py` |
| **Kaycelyn Tigas** | Summary CSV generation (`grouped`, `grouped_two`, `pivot`, `top10`); visualizations (Matplotlib bar chart & Seaborn heatmap) | `feature/summary-outputs` | `src/analytics.py`, `src/visualizer.py` |
| **Gillian Maxine Estilloso** | Automated validation framework (`validation.csv`) & tolerance checks; audit trail generation (`audit_log.csv`); main execution driver (`main.py`) & exit status handling | `feature/validation-audit` | `src/validator.py`, `main.py` |

---

## Repository Structure

```text
Case-Study-2_Group-2/
│
├── data/
│   └── 2015.csv               # Downloaded raw dataset (Ignored by Git)
│
├── src/
│   ├── __init__.py            # Package initializer
│   ├── loader.py              # File loading & column validation logic
│   ├── cleaner.py             # Data cleaning class & filtering methods
│   ├── benchmark.py           # NumPy vs. Python loop performance benchmarks
│   ├── analytics.py           # Aggregation logic & summary CSV export functions
│   ├── visualizer.py          # Matplotlib & Seaborn chart generation
│   └── validator.py           # Data audit logging & balance checks
│
├── config.py                  # Global configurations, file paths, & tolerances
├── main.py                    # Pipeline execution entry point
├── analysis.ipynb             # Jupyter Notebook demonstration
│
├── .gitignore                 # Standard Python & large file exclusions
├── requirements.txt           # Environment dependencies
├── contributions.md           # Member contribution log & review hashes
├── submission_manifest.txt    # Repo URL, release tag, & target commit hash
└── README.md                  # Project documentation
```
