"""
cleaner.py
OOP-based data cleaning utilities for the Customs 2015 pipeline.

Defines the DataCleaner class, which performs cleaning operations on the
DataFrame produced by loader.py (deduplication, standardizing messy
category values, and flagging outliers) and records each action into a
shared audit log list, such as config.AUDIT_LOG, for later export by
validator.py.
"""

from typing import Dict, List, Optional, Set

import pandas as pd


class DataCleaner:
    """Performs OOP-based cleaning operations on the Customs dataset.

    Instance attributes:
        required_columns: Set of column names the cleaner expects to find
            and may operate on.
        audit_log: List of audit record dictionaries. When an existing list
            is passed in (e.g. config.AUDIT_LOG), that same list object is
            reused, so records appended here are visible wherever the
            caller holds a reference to it.
        step_count: Number of cleaning operations logged so far.
    """

    def __init__(
        self,
        required_columns: Set[str],
        audit_log: Optional[List[dict]] = None,
    ) -> None:
        """Initialize the cleaner.

        Args:
            required_columns: Set of column names the cleaner expects to
                operate on, e.g. config.REQUIRED_COLUMNS.
            audit_log: Optional existing list of audit records to append
                to, such as config.AUDIT_LOG. Defaults to a new empty list.
        """
        self.required_columns: Set[str] = required_columns
        self.audit_log: List[dict] = audit_log if audit_log is not None else []
        self.step_count: int = len(self.audit_log)

    def _log(self, operation: str, rule: str, rows_before: int, rows_after: int) -> None:
        """Append one audit record to the shared audit log.

        Args:
            operation: Short name of the cleaning operation performed.
            rule: Human-readable description of the rule that was applied.
            rows_before: Row count before this operation.
            rows_after: Row count after this operation.
        """
        self.step_count += 1
        self.audit_log.append(
            {
                "step": self.step_count,
                "operation": operation,
                "rule": rule,
                "rows_before": rows_before,
                "rows_after": rows_after,
            }
        )

    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """Drop duplicate rows and log the result.

        Args:
            df: The DataFrame to deduplicate.
            subset: Optional list of column names to consider when
                identifying duplicates. Defaults to using all columns.

        Returns:
            A new DataFrame with duplicate rows removed.
        """
        rows_before = len(df)
        cleaned = df.drop_duplicates(subset=subset).copy()
        rule = f"drop duplicates on {subset}" if subset else "drop fully duplicate rows"
        self._log("remove_duplicates", rule, rows_before, len(cleaned))
        return cleaned

    def standardize_missing(
        self,
        df: pd.DataFrame,
        columns: List[str],
        placeholder: str = "MISSING",
    ) -> pd.DataFrame:
        """Replace missing values in the given categorical columns with a placeholder.

        Args:
            df: The DataFrame to clean.
            columns: List of categorical column names to standardize.
            placeholder: Text used to fill missing values so they appear as
                an explicit group rather than being dropped. Defaults to
                "MISSING".

        Returns:
            A new DataFrame with missing values filled in the given columns.
            Row count is unchanged; only cell values are affected.
        """
        rows_before = len(df)
        cleaned = df.copy()
        for column in columns:
            if column in cleaned.columns:
                cleaned[column] = cleaned[column].fillna(placeholder)
        self._log(
            "standardize_missing",
            f"fill missing values in {columns} with '{placeholder}'",
            rows_before,
            len(cleaned),
        )
        return cleaned

    def flag_outliers(self, df: pd.DataFrame, column: str, threshold: float) -> pd.DataFrame:
        """Add a Boolean flag column marking values above a threshold.

        Args:
            df: The DataFrame to annotate.
            column: Name of the numerical column to check against the
                threshold, e.g. "dutiablevaluephp".
            threshold: Values strictly greater than this are flagged True.

        Returns:
            A new DataFrame with an added "<column>_outlier_flag" column.
            Row count is unchanged.

        Raises:
            ValueError: If column is not present in df.
        """
        if column not in df.columns:
            raise ValueError(
                f"flag_outliers: column '{column}' not found in DataFrame. "
                f"Available columns: {list(df.columns)}"
            )
        rows_before = len(df)
        flagged = df.copy()
        flag_column = f"{column}_outlier_flag"
        flagged[flag_column] = flagged[column] > threshold
        self._log(
            "flag_outliers",
            f"flag {column} > {threshold} as {flag_column}",
            rows_before,
            len(flagged),
        )
        return flagged

    def clean(
        self,
        df: pd.DataFrame,
        missing_value_columns: List[str],
        outlier_column: str,
        outlier_threshold: float,
        dedup_subset: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """Run the full cleaning sequence: dedupe, standardize, then flag.

        Args:
            df: The DataFrame to clean, typically the output of
                loader.filter_and_transform.
            missing_value_columns: Categorical columns to standardize
                missing values in.
            outlier_column: Numerical column to check for outliers.
            outlier_threshold: Threshold above which values are flagged.
            dedup_subset: Optional list of columns used to identify
                duplicate rows. Defaults to using all columns.

        Returns:
            The fully cleaned DataFrame, after deduplication, missing-value
            standardization, and outlier flagging.
        """
        deduped = self.remove_duplicates(df, subset=dedup_subset)
        standardized = self.standardize_missing(deduped, missing_value_columns)
        flagged = self.flag_outliers(standardized, outlier_column, outlier_threshold)
        return flagged
