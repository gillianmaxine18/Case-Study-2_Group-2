import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_top10_bar(top10_df: pd.DataFrame, output_dir: str) -> None:
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

def plot_pivot_heatmap(pivot_df: pd.DataFrame, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(12, 8))
    
    # exclude margins: drop the 'Total' row and column before plotting
    heatmap_data = pivot_df.drop(index='Total', errors='ignore').drop(columns='Total', errors='ignore')
    
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
