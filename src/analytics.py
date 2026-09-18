# src/analytics.py
import pandas as pd
import os

def generate_summaries(df: pd.DataFrame, out_dir: str) -> pd.DataFrame:
    """Generates the required summary CSVs."""
    os.makedirs(out_dir, exist_ok=True)
    
    # grouped.csv
    grouped = df.groupby('countryorigin_iso3').agg(
        row_count=('dutiablevaluephp', 'size'),
        valid_measure_count=('dutiablevaluephp', 'count'),
        measure_sum=('dutiablevaluephp', 'sum'),
        measure_mean=('dutiablevaluephp', 'mean')
    ).reset_index()
    grouped.to_csv(f"{out_dir}/grouped.csv", index=False)
    
    # grouped_two.csv
    grouped_two = df.groupby(['countryorigin_iso3', 'tq']).agg(
        row_count=('dutiablevaluephp', 'size'),
        measure_sum=('dutiablevaluephp', 'sum')
    ).reset_index()
    grouped_two.to_csv(f"{out_dir}/grouped_two.csv", index=False)
    
    # pivot.csv
    pivot = pd.pivot_table(df, values='dutiablevaluephp', index='countryorigin_iso3', columns='tq', aggfunc='sum', margins=True)
    pivot.to_csv(f"{out_dir}/pivot.csv")
    
    # top10.csv
    top10 = grouped.nlargest(10, 'measure_sum')
    top10.to_csv(f"{out_dir}/top10.csv", index=False)
    
    return top10
