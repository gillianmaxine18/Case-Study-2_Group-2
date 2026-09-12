"""
config.py
Configuration data structures for the Philippine Customs 2015 ETL pipeline.
"""

# required configuration dictionary
PIPELINE_CONFIG = {
    "input_filepath": "2015.csv",
    "output_folder": "outputs/",
    "filters": {
        "target_country": "CHN",  # Condition 1: Origin country is China
        "min_value_php": 0.0      # Condition 2: Dutiable value > 0
    },
    # rubric strictly three columns for Customs 2015
    "grouping_columns": ["countryorigin_iso3", "tq"],
    "numerical_measure": "dutiablevaluephp",

    # required source documentation for selected fields
    "field_metadata": {
        "countryorigin_iso3": "Origin country of the import (ISO-3 code).",
        "tq": "Tariff Quota or category classification for the goods.",
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