# Case Study 2: "Build a Philippine Data Summary Program" - Group 2

## Project Google Drive Link: https://drive.google.com/drive/folders/1mL3LtozoE_Se__jcpsFeg2_lrlrKungJ?usp=sharing
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

## Member Roles & Task Allocation
| Member | Assigned Task / Requirements | Dedicated Branch Name \ GitHub Username |
|---|---|---|
| **Kate Robyn Alday** | • Configuration dictionary & environment setup<br>• Control structures for data pipeline execution<br>• Data structures (audit records, required columns)<br>• Type hinting lead across modules | `feature/data-structures` | `config.py`<br>`src/loader.py` 
| **Giana Elisha Tuplano** | • OOP implementation: Dataset Cleaner class & 3 methods<br>• Module initialization & package structure<br>• Pandas data filtering, `.loc` selection, & derived columns | `feature/oop-cleaner` | `src/cleaner.py`<br>`src/__init__.py` 
| **Hans Adrian Laudato** | • NumPy array conversions & vectorized operations<br>• Boolean masks & aggregation logic<br>• Performance benchmark (Loop vs. Vectorized over 5 runs with fixed seed) | `feature/numpy-benchmark` | `src/benchmark.py` 
| **Kaycelyn Tigas** | • Summary CSV generation (`grouped`, `grouped_two`, `pivot`, `top10`) <br>• Visualizations: Matplotlib bar chart & Seaborn heatmap | `feature/summary-outputs` | `src/analytics.py`<br>`src/visualizer.py` 
| **Gillian Maxine Estilloso** | • Automated validation framework (`validation.csv`) & tolerance checks<br>• Dynamic audit trail generation (`audit_log.csv`)<br>• Main execution driver (`main.py`) & exit status handling | `feature/validation-audit` | `src/validator.py`<br>`main.py` 
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
