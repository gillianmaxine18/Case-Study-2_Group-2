"""
visualizer.py
Plotting utilities for the Customs 2015 pipeline.
 
Defines plot_top10_bar() and plot_pivot_heatmap(), which take the
DataFrames returned by analytics.generate_summaries() and save the two
required charts (bar.png, heatmap.png) to output_folder, with titles,
axis labels, and units as required by the assignment.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_top10_bar(top10_df: pd.DataFrame, output_dir: str) -> None:
    """Draw and save a bar chart of the top 10 groups by measure sum.

    Args:
        top10_df: The top10.csv DataFrame from analytics.generate_summaries,
            with 'countryorigin_iso3' and 'measure_sum' columns.
        output_dir: Folder to save bar.png into. Created if missing.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # the bar chart maker
    plt.bar(top10_df['countryorigin_iso3'], top10_df['measure_sum'], color='steelblue')
    
    # titles, labels, and units (PHP)
    plt.title('Top 10 Countries of Origin by Total Dutiable Value')
    plt.xlabel('Country of Origin (ISO3)')
    plt.ylabel('Total Dutiable Value (PHP)')
    
    # rotate country codes so they don't overlap
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # save the plot
    plt.savefig(os.path.join(output_dir, 'bar.png'))
    plt.close()

def plot_pivot_heatmap(pivot_df: pd.DataFrame, output_dir: str, margin_label: str = 'Total_Sum') -> None:
    """Draw and save a heatmap of the pivot table, excluding margins.

    Args:
        pivot_df: The pivot.csv DataFrame from analytics.generate_summaries,
            built with margins=True.
        output_dir: Folder to save heatmap.png into. Created if missing.
        margin_label: The label used for the margins row/column. Must
            match analytics.py's margins_name exactly (default 'Total_Sum')
            or the margin row/column won't actually be excluded.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(12, 8))
    
    # exclude margins: drop the margin row and column before plotting
    heatmap_data = pivot_df.drop(index=margin_label, errors='ignore').drop(columns=margin_label, errors='ignore')
    
    # create the heatmap
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False, cbar_kws={'label': 'Dutiable Value (PHP)'})
    
    # add titles and labels
    plt.title('Heatmap of Total Dutiable Value (PHP) by Country and TQ')
    plt.xlabel('Treatment Qualifier (TQ)')
    plt.ylabel('Country of Origin (ISO3)')
    
    plt.tight_layout()
    
    # save the plot
    plt.savefig(os.path.join(output_dir, 'heatmap.png'))
    plt.close()
