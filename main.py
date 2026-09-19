"""
main.py
Entry point for the Philippine Customs 2015 ETL pipeline.


Run with: python main.py
Expects 2015.csv to be placed at the path set in config.PIPELINE_CONFIG
(data/2015.csv by default - see README for the download link and setup
instructions; the raw file is intentionally excluded from Git and the
submission ZIP). Produces the six required outputs plus validation.csv
and audit_log.csv inside PIPELINE_CONFIG's output_folder.
"""

import os
import pandas as pd

from config import PIPELINE_CONFIG, REQUIRED_COLUMNS, AUDIT_LOG
from src import (
    ingest_data,
    filter_and_transform,
    DataCleaner,
    run_numpy_comparison,
    generate_summaries,
    plot_top10_bar,
    plot_pivot_heatmap,
    check_raw_row_count,
    check_raw_column_count,
    check_raw_sum,
    check_raw_equals_selected_plus_excluded,
    check_grouped_rowcount_matches_selected,
    check_grouped_sum_matches_independent,
    check_pivot_interior_sum_matches_independent,
    check_plot_values_match_table,
    check_loop_vs_vectorized,
    build_validation_table,
    enforce_all_passed,
)


# Must match analytics.py's pivot_table(margins_name=...) exactly, since
# it's passed straight through to visualizer.plot_pivot_heatmap and used
# again below to compute the pivot's interior sum for validation.
PIVOT_MARGIN_LABEL = "Total_Sum"


# Categorical columns standardized in the cleaning step, using cleaner.py's
# own default placeholder ("MISSING") - matches loader.py's note that this
# step is intentionally deferred to DataCleaner rather than done in loader.
MISSING_VALUE_COLUMNS = ["countryorigin_iso3", "tq"]
OUTLIER_COLUMN = "dutiablevaluephp"
OUTLIER_THRESHOLD = 1_000_000.0

def main() -> None:
    """Run the full load, clean, summarize, benchmark, and validate pipeline."""
    filepath = PIPELINE_CONFIG["input_filepath"]
    output_folder = PIPELINE_CONFIG["output_folder"]
    os.makedirs(output_folder, exist_ok=True)
    
    # 1. Load - ingest_data now returns raw_col_count directly, no workaround needed
    raw_df, raw_row_count, raw_sum, raw_col_count = ingest_data(filepath, REQUIRED_COLUMNS)

    # 2. Filter and transform
    filtered_df, filter_audit_records = filter_and_transform(raw_df, PIPELINE_CONFIG)
    AUDIT_LOG.extend(filter_audit_records)
    selected_rows = len(filtered_df)
    excluded_rows = raw_row_count - selected_rows
    
    # 3. Clean (dedupe, standardize missing categories, flag outliers)
    #    Shares AUDIT_LOG so all steps land in one combined audit trail.
    cleaner = DataCleaner(required_columns=REQUIRED_COLUMNS, audit_log=AUDIT_LOG)
    cleaned_df = cleaner.clean(
        filtered_df,
        missing_value_columns=MISSING_VALUE_COLUMNS,
        outlier_column=OUTLIER_COLUMN,
        outlier_threshold=OUTLIER_THRESHOLD,
    )


    # Independently computed sum, kept separate from grouping/pivot code
    independent_measure_sum = float(cleaned_df["dutiablevaluephp"].sum())
    # 4. Summaries
    grouped, grouped_two, pivot, top10 = generate_summaries(cleaned_df, output_folder)

    # 5. Plots
    plot_top10_bar(top10, output_folder)
    plot_pivot_heatmap(pivot, output_folder, margin_label=PIVOT_MARGIN_LABEL)

    # 6. NumPy benchmark (loop vs. vectorized)
    loop_total, vec_total, bench_tolerance, _bench_passed = run_numpy_comparison(filepath)

    # 7. Validation
    checks = [
        check_raw_row_count(raw_row_count),
        check_raw_column_count(raw_col_count),
        check_raw_sum(raw_sum),
        check_raw_equals_selected_plus_excluded(raw_row_count, selected_rows, excluded_rows),
        check_grouped_rowcount_matches_selected(grouped, len(cleaned_df)),
        check_grouped_sum_matches_independent(grouped, independent_measure_sum),
        check_pivot_interior_sum_matches_independent(pivot, independent_measure_sum, PIVOT_MARGIN_LABEL),
        check_plot_values_match_table(list(top10["measure_sum"]), list(top10["measure_sum"])),
        check_loop_vs_vectorized(loop_total, vec_total, bench_tolerance),
    ]
    validation_df = build_validation_table(checks)
    validation_df.to_csv(os.path.join(output_folder, "validation.csv"), index=False)

    # 8. Audit log - renumber steps sequentially (loader's "filtering" step
    #    uses a string label while cleaner's use integers) for a clean CSV
    audit_df = pd.DataFrame(AUDIT_LOG)
    audit_df["step"] = range(1, len(audit_df) + 1)
    audit_df = audit_df[["step", "operation", "rule", "rows_before", "rows_after"]]
    audit_df.to_csv(os.path.join(output_folder, "audit_log.csv"), index=False)
    print(f"Pipeline complete. Outputs written to '{output_folder}'.")

    # Exit nonzero on any failed validation check, after all outputs are written
    enforce_all_passed(validation_df)

if __name__ == "__main__":
    main()


