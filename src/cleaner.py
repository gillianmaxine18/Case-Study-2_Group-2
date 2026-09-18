# src/cleaner.py
import pandas as pd
from typing import List, Dict, Any

class DataCleaner:
    """Cleans and transforms the dataset."""
    def __init__(self, df: pd.DataFrame, config: dict):
        self.df = df.copy()
        self.config = config
        self.excluded_rows = 0

    def filter_data(self, audit_log: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Applies filters using .loc and updates audit log."""
        initial_rows = len(self.df)
        
        # Filter: Drop NaNs and ensure value > 0
        valid_mask = self.df['countryorigin_iso3'].notna() & self.df['tq'].notna() & self.df['dutiablevaluephp'].notna()
        val_mask = self.df['dutiablevaluephp'] > self.config.get('min_value_php', 0.0)
        
        self.df = self.df.loc[valid_mask & val_mask].copy()
        
        final_rows = len(self.df)
        self.excluded_rows = initial_rows - final_rows
        
        if final_rows == 0:
            raise ValueError("Filter returned no rows.")
            
        audit_log.append({'step': 'Clean', 'operation': 'Filter out NaNs and <=0', 'rule': 'Must be valid', 'rows_before': initial_rows, 'rows_after': final_rows})
        return audit_log

    def add_derived_columns(self) -> None:
        """Adds a numerical column and a category/flag column."""
        self.df['tax_per_tq'] = self.df['dutiablevaluephp'] / pd.to_numeric(self.df['tq'], errors='coerce')
        self.df['is_high_value'] = (self.df['dutiablevaluephp'] > 1000000).astype(str)

    def sort_data(self) -> pd.DataFrame:
        """Sorts the dataframe by the primary measure."""
        self.df = self.df.sort_values(by='dutiablevaluephp', ascending=False)
        return self.df
