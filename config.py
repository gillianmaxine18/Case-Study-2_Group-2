"""
config.py
Central configuration for the Philippine Customs 2015 ETL pipeline.
 
Defines PIPELINE_CONFIG (the input path, filter values, grouping
columns, and output folder used across the whole pipeline),
REQUIRED_COLUMNS (the set of columns loader.py validates the raw file
against), and AUDIT_LOG (the shared list that loader.py and
cleaner.DataCleaner append to, and that main.py writes out to
audit_log.csv at the end of the run).
"""

# required configuration dictionary
PIPELINE_CONFIG = {
    "input_filepath": "data/2015.csv",  # standardized to the data/ folder convention (see README)
    "output_folder": "outputs/",
    "filters": {
    "target_quarter": "2015q1", # Condition 1: reporting quarter is Q1 2015
    "min_value_php": 1000.0     # Condition 2: Dutiable value > 1000
                                 # Assumption: shipments under PHP 1,000 dutiable value are treated
                                 # as negligible/noise for this analysis.
    },
    # rubric strictly three columns for Customs 2015
    "grouping_columns": ["countryorigin_iso3", "tq"],
    "numerical_measure": "dutiablevaluephp",

    # required source documentation for selected fields
    "field_metadata": {
        "countryorigin_iso3": "Origin country of the import (ISO-3 code).",
        "tq": "Reporting quarter the import was recorded in (e.g. '2015q1', '2015q2').",
        "dutiablevaluephp": "Dutiable value in Philippine Pesos (PHP)."
    }
}

# required set data structure for column validation
REQUIRED_COLUMNS = {
    "countryorigin_iso3", 
    "tq", 
    "dutiablevaluephp"
}

# required list data structure for audit records
AUDIT_LOG = []
