"""
loader.py
Loading, validation, filtering, and transformation for the Customs 2015 pipeline.

Defines ingest_data(), which reads the raw CSV in chunks, checks it
against config.REQUIRED_COLUMNS, and returns the raw row/column counts
and measure sum needed for validator.py's Step 4 reference checks; and
filter_and_transform(), which applies the two-condition .loc filter
from config.PIPELINE_CONFIG, sorts the result, and adds the two
required derived columns before handing off to cleaner.py.
"""

import os
import sys
import pandas as pd
from typing import Dict, List, Set, Tuple

def ingest_data(filepath: str, required_cols: Set[str], chunk_size: int = 100000) -> Tuple[pd.DataFrame, int, float, int]:
    """loads the dataset in chunks, checks for required columns, and gets raw totals

    Returns:
        A tuple of (df, raw_row_count, raw_sum, raw_col_count), where
        raw_col_count is the number of columns in the *original* file
        (before usecols narrows it down), needed for the Customs 2015
        reference check against 30 columns.
    """
    
    # control structure 1: missing file
    if not os.path.exists(filepath):
        print(f"CRITICAL ERROR: file '{filepath}' not found.")
        sys.exit(1)
        
    raw_row_count = 0
    raw_sum = 0.0
    chunks = []
    
    try:
        # check columns on first 5 rows to save ram
        first_chunk = pd.read_csv(filepath, nrows=5, encoding='latin1') # encoding to account for special characters
        
        # capture the raw column count (from the full file, before usecols
        # narrows things down) for the Step 4 reference check
        raw_col_count = len(first_chunk.columns)
        
        # control structure 2: missing columns
        missing_cols = required_cols - set(first_chunk.columns)
        if missing_cols:
            print(f"CRITICAL ERROR: missing required columns: {missing_cols}")
            sys.exit(1)
            
        print(f"loading '{filepath}' in chunks of {chunk_size}...")
        
        # control structure loop: read records in chunks
        for chunk in pd.read_csv(filepath, chunksize=chunk_size, usecols=list(required_cols), encoding='latin1'):
            raw_row_count += len(chunk)
            # get raw sum for step 4 validation audit
            raw_sum += chunk['dutiablevaluephp'].sum()
            chunks.append(chunk)
            
        df = pd.concat(chunks, ignore_index=True)
        return df, raw_row_count, raw_sum, raw_col_count
        
    except Exception as e:
        print(f"CRITICAL ERROR during file reading: {e}")
        sys.exit(1)


def filter_and_transform(df: pd.DataFrame, config: Dict) -> Tuple[pd.DataFrame, List[dict]]:
    """applies filters, sorts the data, and adds derived columns."""
    
    country = config["filters"]["target_country"]
    min_value = config["filters"]["min_value_php"]
    
    # 1. filter with .loc using two conditions
    mask = (df['countryorigin_iso3'] == country) & (df['dutiablevaluephp'] > min_value)
    filtered_df = df.loc[mask].copy()
    
    # control structure 3: filter returns empty
    if len(filtered_df) == 0:
        print(f"WARNING: filter for country '{country}' and value > {min_value} returned 0 rows.")
        sys.exit(1)
        
    # 2. sort by measure descending
    filtered_df = filtered_df.sort_values(by=config["numerical_measure"], ascending=False)
    
    # 3. add two derived columns (one numerical, one flag)
    filtered_df['estimated_vat_php'] = filtered_df['dutiablevaluephp'] * 0.12
    filtered_df['is_high_value_flag'] = filtered_df['dutiablevaluephp'] > 1000000
    
    # NOTE: missing-category standardization (explicit "MISSING" group) is
    # handled downstream by cleaner.DataCleaner.standardize_missing(), per
    # the group's integration contract (pipeline order: loader -> cleaner
    # -> analytics). The countryorigin_iso3 fill is dead code anyway: the
    # mask above requires an exact match against target_country, so a NaN
    # in that column can never survive the filter. Leave numerical NaNs
    # alone per rubric rules; that never happens here or in cleaner.py.
    
    # generate audit record
    audit_record = {
        "step": "filtering",
        "operation": "apply_loc_conditions",
        "rule": f"country == '{country}' AND value > {min_value}",
        "rows_before": len(df),
        "rows_after": len(filtered_df)
    }
    
    return filtered_df, [audit_record]
