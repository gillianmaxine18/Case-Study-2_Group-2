# src/benchmark.py
import time
import numpy as np
import pandas as pd
from typing import Tuple

def extract_numerical_array(df: pd.DataFrame, column_name: str = 'dutiablevaluephp') -> np.ndarray:
    """
    Extracts a pandas Series into a NumPy array, filtering out nulls using a Boolean mask.
    
    Args:
        df (pd.DataFrame): The loaded Customs dataset.
        column_name (str): The target column to extract. Defaults to 'dutiablevaluephp'.
        
    Returns:
        np.ndarray: A 1D NumPy array containing valid numerical data.
    """
    valid_mask = df[column_name].notna().to_numpy()
    return df[column_name].to_numpy(dtype=np.float64)[valid_mask]

def compare_performance(data_array: np.ndarray, threshold: float = 1000.0) -> Tuple[str, float, float, float, bool]:
    """
    Compares loop vs vectorized calculation on an array using a fixed-seed sample.
    
    Args:
        data_array (np.ndarray): NumPy array of real numerical values.
        threshold (float): Value to mask and sum above. Defaults to 1000.0.
        
    Returns:
        Tuple[str, float, float, float, bool]: Formatted for validation.csv as 
        (check, expected, actual, tolerance, pass).
    """
    np.random.seed(42)
    sample_size = min(100000, len(data_array))
    sample = np.random.choice(data_array, size=sample_size, replace=False)

    loop_times = []
    expected_sum = 0.0
    for _ in range(5):
        start = time.perf_counter()
        total = 0.0
        for val in sample:
            if val > threshold:
                total += val
        end = time.perf_counter()
        loop_times.append(end - start)
        expected_sum = total

    vec_times = []
    actual_sum = 0.0
    for _ in range(5):
        start = time.perf_counter()
        mask = sample > threshold  
        actual_sum = float(np.sum(sample[mask]))
        end = time.perf_counter()
        vec_times.append(end - start)

    print(f"NumPy Benchmark -> Median Loop Time: {np.median(loop_times):.6f}s | Median Vectorized Time: {np.median(vec_times):.6f}s")

    tolerance = 1.00 
    is_pass = abs(expected_sum - actual_sum) <= tolerance
    
    return ("NumPy Loop vs Vectorized", expected_sum, actual_sum, tolerance, bool(is_pass))
