"""
src package
Philippine Customs 2015 ETL pipeline package.

Exposes the pipeline's core building blocks so main.py can import
everything through `src` directly, e.g.:

    from src import ingest_data, filter_and_transform, DataCleaner
"""

from .loader import ingest_data, filter_and_transform
from .cleaner import DataCleaner
from .benchmark import run_numpy_comparison, filter_valid_records, calculate_average_value
from .analytics import generate_summaries
from .visualizer import plot_top10_bar, plot_pivot_heatmap
from .validator import (
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

__all__ = [
    "ingest_data",
    "filter_and_transform",
    "DataCleaner",
    "run_numpy_comparison",
    "filter_valid_records",
    "calculate_average_value",
    "generate_summaries",
    "plot_top10_bar",
    "plot_pivot_heatmap",
    "check_raw_row_count",
    "check_raw_column_count",
    "check_raw_sum",
    "check_raw_equals_selected_plus_excluded",
    "check_grouped_rowcount_matches_selected",
    "check_grouped_sum_matches_independent",
    "check_pivot_interior_sum_matches_independent",
    "check_plot_values_match_table",
    "check_loop_vs_vectorized",
    "build_validation_table",
    "enforce_all_passed",
]
