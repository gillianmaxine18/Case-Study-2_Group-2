# main.py
import config
from src.loader import load_data
from src.cleaner import DataCleaner
from src.analytics import generate_summaries
from src.visualizer import create_plots
from src.benchmark import extract_numerical_array, compare_performance
from src.validator import check_and_export
import sys

def main():
    required_cols = set(config.GROUPING_COLS + [config.MEASURE_COL])
    validations = []
    
    try:
        print("Loading data...")
        df, audit_log, raw_rows, raw_sum = load_data(config.INPUT_PATH, required_cols)
        
        # 2015 Reference Checks
        validations.append(("Raw Rows Check", 2236612, raw_rows, 0, raw_rows == 2236612))
        validations.append(("Raw Sum Check", 3587267375257.0, raw_sum, 1.0, abs(3587267375257.0 - raw_sum) <= 1.0))
        
        print("Cleaning data...")
        cleaner = DataCleaner(df, config.FILTER_VALUES)
        audit_log = cleaner.filter_data(audit_log)
        cleaner.add_derived_columns()
        cleaned_df = cleaner.sort_data()
        
        # Reconciliation Check
        expected_rows = raw_rows - cleaner.excluded_rows
        validations.append(("Row Reconciliation", expected_rows, len(cleaned_df), 0, expected_rows == len(cleaned_df)))
        
        print("Generating summaries...")
        top10_df = generate_summaries(cleaned_df, config.OUTPUT_DIR)
        
        print("Generating plots...")
        create_plots(top10_df, cleaned_df, config.OUTPUT_DIR)
        
        print("Running NumPy Benchmark (Hans's Module)...")
        num_array = extract_numerical_array(cleaned_df, config.MEASURE_COL)
        validations.append(compare_performance(num_array))
        
        print("Running validation and exporting logs...")
        check_and_export(validations, audit_log, config.OUTPUT_DIR)
        
        print("SUCCESS: Program complete. Zip the outputs folder and submit!")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
