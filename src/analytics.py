import pandas as pd
import os


def generate_summaries(df: pd.DataFrame, output_dir: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generate the four required summary tables from the cleaned dataset.

    Writes grouped.csv, grouped_two.csv, pivot.csv, and top10.csv to
    output_dir, and returns each as a DataFrame for downstream use
    (plotting and validation).

    Args:
        df: The cleaned, filtered DataFrame to summarize. Must contain
            'countryorigin_iso3', 'tq', and 'dutiablevaluephp'.
        output_dir: Folder to write the four CSV files into. Created if
            it doesn't already exist.

    Returns:
        A tuple of (grouped, grouped_two, pivot, top10) DataFrames.
    """
    #output folder maker if there's none
    os.makedirs(output_dir, exist_ok=True)

    # convert missing categories to explicit strings so they appear as groups
    df['countryorigin_iso3'] = df['countryorigin_iso3'].fillna('Missing')
    df['tq'] = df['tq'].fillna('Missing')

    # 1. grouped.csv: Group by 1st category
    grouped = df.groupby('countryorigin_iso3', dropna=False).agg(
        row_count=('dutiablevaluephp', 'size'),
        valid_measure_count=('dutiablevaluephp', 'count'),
        measure_sum=('dutiablevaluephp', 'sum'),
        measure_mean=('dutiablevaluephp', 'mean')
    ).reset_index()
    grouped.to_csv(os.path.join(output_dir, 'grouped.csv'), index=False)

    # 2. grouped_two.csv: Group by both categories
    grouped_two = df.groupby(['countryorigin_iso3', 'tq'], dropna=False).agg(
        row_count=('dutiablevaluephp', 'size'),
        measure_sum=('dutiablevaluephp', 'sum')
    ).reset_index()
    grouped_two.to_csv(os.path.join(output_dir, 'grouped_two.csv'), index=False)

    # 3. pivot.csv: showing measure sum in both categories with margins
    pivot = pd.pivot_table(
        df,
        values='dutiablevaluephp',
        index='countryorigin_iso3',
        columns='tq',
        aggfunc='sum',
        margins=True,
        margins_name='Total_Sum'
    )
    pivot.to_csv(os.path.join(output_dir, 'pivot.csv'))

    # 4. top10.csv: 10 largest groups by measure sum
    top10 = grouped.sort_values(by='measure_sum', ascending=False).head(10)
    top10.to_csv(os.path.join(output_dir, 'top10.csv'), index=False)

    return grouped, grouped_two, pivot, top10
