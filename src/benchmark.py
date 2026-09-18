import time
import numpy as np
import pandas as pd

def run_numpy_comparison(data_path: str, sample_size: int = 100000) -> tuple[float, float, float, bool]:
    """
    Compares the execution time of a loop-based calculation versus a vectorised 
    NumPy equivalent using a fixed-seed sample from the 'dutiablevaluephp' column.
    """
    df = pd.read_csv(data_path)
    data_array = df["dutiablevaluephp"].sample(n=sample_size, random_state=42).to_numpy()
    
    threshold = 15000.0
    multiplier = 1.10
    tolerance = 1e-8
    
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
    # Ensure you provide the correct file path to your dataset
    run_numpy_comparison("path_to_your_dataset.csv")
