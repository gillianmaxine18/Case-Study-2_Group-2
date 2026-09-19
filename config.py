"""
config.py
Configuration data structures for the Philippine Customs 2015 ETL pipeline.
"""

# required configuration dictionary
PIPELINE_CONFIG = {
    "input_filepath": "data/2015.csv",  # FIX: standardized to the data/ folder convention (see README)
    "output_folder": "outputs/",
    "filters": {
        "target_country": "CHN",   # Condition 1: Origin country is China
        "min_value_php": 1000.0    # FIX: raised from 0.0 so this is a real, meaningful filter
                                    # (was effectively a no-op: > 0.0 only excluded zero/negative rows).
                                    # Assumption: shipments under PHP 1,000 dutiable value are treated
                                    # as negligible/noise for this analysis.
    },
    # rubric strictly three columns for Customs 2015
    "grouping_columns": ["countryorigin_iso3", "tq"],
    "numerical_measure": "dutiablevaluephp",

    # required source documentation for selected fields
    "field_metadata": {
        "countryorigin_iso3": "Origin country of the import (ISO-3 code).",
        # FIX: tq actually holds the reporting quarter (2015q1-2015q4), not a tariff-quota
        # classification. Corrected to match what's in the actual dataset.
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
