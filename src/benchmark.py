"""
benchmark.py
NumPy loop-vs-vectorized performance comparison for the Customs 2015 pipeline.

Defines run_numpy_comparison(), which samples the real dutiablevaluephp
column with a fixed seed, times a plain Python loop against an
equivalent Boolean-mask NumPy calculation over five runs, and returns
the two totals plus a tolerance and pass flag for validator.py's
loop-vs-vectorized check; also defines filter_valid_records() and
calculate_average_value() as the two standalone functions required by
the assignment's "Functions and parameters" rubric line.
"""

import time
import numpy as np
import pandas as pd

def run_numpy_comparison(data_path: str, sample_size: int = 100000) -> tuple[float, float, float, bool]:
    """
    Compares the execution time of a loop-based calculation versus a vectorised 
    NumPy equivalent using a fixed-seed sample from the 'dutiablevaluephp' column.
    """
    # matches loader.py's encoding='latin1' - the raw file has bytes that
    # aren't valid UTF-8, so the default encoding crashes with UnicodeDecodeError
    df = pd.read_csv(data_path, encoding='latin1')
    data_array = df["dutiablevaluephp"].sample(n=sample_size, random_state=42).to_numpy()
    
    threshold = 15000.0
    multiplier = 1.10
    # 0.01 (one centavo) matches validator.py's own DEFAULT_TOLERANCE
    # convention - 1e-8 is unrealistically tight for sums in the hundreds
    # of billions of PHP, where ordinary floating-point summation drift of
    # a fraction of a peso is normal and not a real discrepancy.
    tolerance = 0.01
    
    loop_times = []
    vectorised_times = []
    
    loop_total = 0.0
    vec_total = 0.0
    
    for _ in range(5):
        start_loop = time.perf_counter()
        loop_total = 0.0
        for value in data_array:
            if value > threshold:
                loop_total += value * multiplier
        loop_times.append(time.perf_counter() - start_loop)
        
        start_vec = time.perf_counter()
        mask = data_array > threshold
        vec_total = float(np.sum(data_array[mask] * multiplier))
        vectorised_times.append(time.perf_counter() - start_vec)

    median_loop = float(np.median(loop_times))
    median_vec = float(np.median(vectorised_times))
    
    print("--- Performance Results ---")
    print(f"Median loop time: {median_loop:.5f} seconds")
    print(f"Median vectorised time: {median_vec:.5f} seconds")
    print(f"Performance gain: {median_loop / median_vec:.2f}x faster")
    
    is_pass = bool(np.isclose(loop_total, vec_total, atol=tolerance))
    
    return loop_total, vec_total, tolerance, is_pass

def filter_valid_records(records: list[dict], min_value: float = 0.0) -> list[dict]:
    """
    Filters a list of dataset records, keeping only those above a minimum value.
    """
    valid_records = []
    for record in records:
        if record.get("value", 0.0) > min_value:
            valid_records.append(record)
    return valid_records

def calculate_average_value(records: list[dict], default_avg: float = 0.0) -> float:
    """
    Calculates the average value from a list of records. 
    Returns the default average if the list is empty.
    """
    if not records:
        return default_avg
    
    total = sum(record.get("value", 0.0) for record in records)
    return float(total / len(records))

if __name__ == "__main__":
    # Standalone test entry point only. main.py always passes the real
    # dataset path directly to run_numpy_comparison(), so this block only
    # matters if someone runs `python src/benchmark.py` on its own.
    try:
        from config import PIPELINE_CONFIG
        dataset_path = PIPELINE_CONFIG["input_filepath"]
    except ImportError:
        dataset_path = "data/2015.csv"
        print("Note: could not import config.py (run this from the project root). "
              f"Falling back to default path: {dataset_path}")

    run_numpy_comparison(dataset_path)
