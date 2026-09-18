"""
validator.py
Validation and reconciliation checks for the Customs 2015 pipeline.

Builds the validation.csv table required by the assignment: for every
required reconciliation rule, records the check name, expected value,
actual value, tolerance, and whether it passed. One function per check
so main.py can assemble them in whatever order the pipeline runs, plus
a helper to combine them into a DataFrame and enforce a nonzero exit
code if any check fails.
"""

from typing import Dict, List

import pandas as pd

# Reference values supplied in the assignment — Customs 2015 only.
REFERENCE_ROW_COUNT: int = 2_236_612
REFERENCE_COLUMN_COUNT: int = 30
REFERENCE_SUM_PHP: float = 3_587_267_375_257.0
REFERENCE_SUM_TOLERANCE: float = 1.00

# Default tolerance for float comparisons elsewhere (grouped sums, pivot, etc.)
DEFAULT_TOLERANCE: float = 0.01


def _make_check(check: str, expected: float, actual: float, tolerance: float) -> Dict[str, object]:
    """Build one validation.csv row, deciding pass/fail from the tolerance.

    Args:
        check: Short human-readable name of the check.
        expected: The independently computed or reference value.
        actual: The value produced by the pipeline being validated.
        tolerance: Maximum allowed absolute difference for a pass.

    Returns:
        A dict with keys check, expected, actual, tolerance, pass.
    """
    passed = bool(abs(float(expected) - float(actual)) <= tolerance)
    return {
        "check": check,
        "expected": expected,
        "actual": actual,
        "tolerance": tolerance,
        "pass": passed,
    }


def check_raw_row_count(raw_row_count: int) -> Dict[str, object]:
    """Check the loaded raw row count against the Customs 2015 reference."""
    return _make_check("raw_row_count_matches_reference", REFERENCE_ROW_COUNT, raw_row_count, 0)


def check_raw_column_count(raw_col_count: int) -> Dict[str, object]:
    """Check the raw file's column count against the Customs 2015 reference."""
    return _make_check("raw_column_count_matches_reference", REFERENCE_COLUMN_COUNT, raw_col_count, 0)


def check_raw_sum(raw_sum: float) -> Dict[str, object]:
    """Check the raw dutiablevaluephp sum against the Customs 2015 reference."""
    return _make_check("raw_sum_matches_reference", REFERENCE_SUM_PHP, raw_sum, REFERENCE_SUM_TOLERANCE)


def check_raw_equals_selected_plus_excluded(
    raw_rows: int, selected_rows: int, excluded_rows: int
) -> Dict[str, object]:
    """Check raw rows == selected rows + excluded rows.

    Missing-filter-value rows are counted in excluded_rows, per the
    assignment's rule that they belong in the excluded group.
    """
    return _make_check(
        "raw_rows_equal_selected_plus_excluded",
        raw_rows,
        selected_rows + excluded_rows,
        0,
    )


def check_grouped_rowcount_matches_selected(grouped_df: pd.DataFrame, selected_rows: int) -> Dict[str, object]:
    """Check that grouped.csv's row_count column sums to the selected row count."""
    total = int(grouped_df["row_count"].sum())
    return _make_check("grouped_rowcount_sums_to_selected", selected_rows, total, 0)


def check_grouped_sum_matches_independent(
    grouped_df: pd.DataFrame, independent_sum: float, tolerance: float = DEFAULT_TOLERANCE
) -> Dict[str, object]:
    """Check grouped.csv's measure_sum total against an independently computed sum."""
    total = float(grouped_df["measure_sum"].sum())
    return _make_check("grouped_sum_matches_independent_sum", independent_sum, total, tolerance)


def check_pivot_interior_sum_matches_independent(
    pivot_df: pd.DataFrame,
    independent_sum: float,
    margin_label: str,
    tolerance: float = DEFAULT_TOLERANCE,
) -> Dict[str, object]:
    """Check the pivot table's interior sum (margins excluded) against an independent sum.

    Args:
        pivot_df: The pivot table returned by analytics.generate_summaries.
        independent_sum: A sum computed separately from the pivot logic.
        margin_label: The label used for the margins row/column, e.g.
            analytics.py's margins_name value. Must match exactly or the
            margin row/column will be counted twice.
        tolerance: Allowed absolute difference for a pass.
    """
    interior = pivot_df.drop(index=margin_label, errors="ignore").drop(columns=margin_label, errors="ignore")
    total = float(interior.to_numpy().sum())
    return _make_check("pivot_interior_sum_matches_independent_sum", independent_sum, total, tolerance)


def check_plot_values_match_table(
    plotted_values: List[float], table_values: List[float], tolerance: float = DEFAULT_TOLERANCE
) -> Dict[str, object]:
    """Check that the values fed to a plot match its source summary table."""
    expected_sum = float(sum(table_values))
    actual_sum = float(sum(plotted_values))
    return _make_check("plot_values_match_summary_table", expected_sum, actual_sum, tolerance)


def check_loop_vs_vectorized(loop_total: float, vec_total: float, tolerance: float) -> Dict[str, object]:
    """Check that the loop and vectorized NumPy calculations agree.

    Consumes benchmark.run_numpy_comparison's returned (loop_total,
    vec_total, tolerance, is_pass) tuple directly.
    """
    return _make_check("loop_vs_vectorized_agree", loop_total, vec_total, tolerance)


def build_validation_table(checks: List[Dict[str, object]]) -> pd.DataFrame:
    """Assemble a list of check dicts into the validation.csv DataFrame."""
    return pd.DataFrame(checks, columns=["check", "expected", "actual", "tolerance", "pass"])


def enforce_all_passed(validation_df: pd.DataFrame) -> None:
    """Exit with a nonzero status if any validation check failed.

    Prints every failing row's discrepancy before exiting, per the
    assignment's requirement to display the discrepancy on failure.

    Args:
        validation_df: The DataFrame returned by build_validation_table.

    Raises:
        SystemExit: If any row's "pass" column is False.
    """
    failures = validation_df[~validation_df["pass"]]
    if not failures.empty:
        print("VALIDATION FAILED - the following checks did not pass:")
        for _, row in failures.iterrows():
            diff = abs(float(row["expected"]) - float(row["actual"]))
            print(
                f"  [{row['check']}] expected={row['expected']} actual={row['actual']} "
                f"tolerance={row['tolerance']} discrepancy={diff}"
            )
        raise SystemExit(1)
