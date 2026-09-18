# src/loader.py
import os
import pandas as pd
from typing import Tuple, List, Dict, Any

def load_data(filepath: str, required_columns: set) -> Tuple[pd.DataFrame, List[Dict[str, Any]], int, float]:
    """Loads data, checks columns, and initializes audit log."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing file: {filepath}")
    
    df = pd.read_csv(filepath, low_memory=False, encoding='latin1')
    
    missing_cols = required_columns - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    raw_rows = len(df)
    raw_sum = df['dutiablevaluephp'].sum()
    
    audit_log = [{'step': 'Load', 'operation': 'Read CSV', 'rule': 'None', 'rows_before': 0, 'rows_after': raw_rows}]
    return df, audit_log, raw_rows, raw_sum
