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
]
