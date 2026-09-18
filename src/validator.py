# src/validator.py
import pandas as pd
from typing import List, Tuple, Dict, Any
import sys
import os

def check_and_export(validations: List[Tuple[str, float, float, float, bool]], audit_log: List[Dict[str, Any]], out_dir: str) -> None:
    """Exports validation and audit logs, exits if check fails."""
    os.makedirs(out_dir, exist_ok=True)
    
    val_df = pd.DataFrame(validations, columns=['check', 'expected', 'actual', 'tolerance', 'pass'])
    val_df.to_csv(f"{out_dir}/validation.csv", index=False)
    
    audit_df = pd.DataFrame(audit_log)
    audit_df.to_csv(f"{out_dir}/audit_log.csv", index=False)
    
    if not val_df['pass'].all():
        print("Validation failed! Discrepancy found. Check validation.csv.")
        sys.exit(1)
    else:
        print("All validation checks passed!")
