# src/visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_plots(top10_df: pd.DataFrame, df: pd.DataFrame, out_dir: str) -> None:
    """Generates and saves the required plots."""
    # bar.png
    plt.figure(figsize=(10, 6))
    plt.bar(top10_df['countryorigin_iso3'], top10_df['measure_sum'])
    plt.title("Top 10 Countries by Dutiable Value")
    plt.xlabel("Country ISO3")
    plt.ylabel("Total Dutiable Value (PHP)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/bar.png")
    plt.close()
    
    # heatmap.png
    pivot_no_margins = pd.pivot_table(df, values='dutiablevaluephp', index='countryorigin_iso3', columns='tq', aggfunc='sum')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_no_margins.fillna(0), cmap="viridis")
    plt.title("Heatmap of Dutiable Value by Country and TQ")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/heatmap.png")
    plt.close()
