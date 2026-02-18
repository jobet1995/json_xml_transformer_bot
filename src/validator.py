"""
validator.py
-------------
Validates JSON/XML data before transformation and export.

Features:
- Checks for required fields.
- Checks for empty values.
- Logs warnings and errors using professional logging.
- Returns a cleaned/validated DataFrame.

Author: Jobet Casquejo
"""

import pandas as pd
from src.logger import get_logger

logger = get_logger(__name__)


def validate_required_fields(df: pd.DataFrame, required_fields: list) -> pd.DataFrame:
    """
    Validate that all required fields exist and are not entirely empty.

    Args:
        df (pd.DataFrame): DataFrame to validate.
        required_fields (list): List of column names that must exist and not be empty.

    Returns:
        pd.DataFrame: DataFrame containing only valid rows.

    Raises:
        ValueError: If required fields are missing from DataFrame.
    """
    # Check if required columns exist
    missing_columns = [col for col in required_fields if col not in df.columns]
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        raise ValueError(f"Missing required columns: {missing_columns}")

    # Check for rows where all required fields are empty
    valid_rows = df.dropna(subset=required_fields, how='all')
    num_invalid = len(df) - len(valid_rows)
    if num_invalid > 0:
        logger.warning(f"{num_invalid} rows dropped because required fields were empty")

    logger.info(f"Validation completed: {len(valid_rows)} valid rows out of {len(df)}")
    return valid_rows


def validate_field_types(df: pd.DataFrame, field_types: dict) -> pd.DataFrame:
    """
    Validate that fields have the expected data types and attempt conversion if possible.

    Args:
        df (pd.DataFrame): DataFrame to validate.
        field_types (dict): Dictionary mapping column names to expected types (e.g., {"Age": int})

    Returns:
        pd.DataFrame: DataFrame with converted types where possible.

    Raises:
        ValueError: If conversion fails for non-null values.
    """
    for field, expected_type in field_types.items():
        if field in df.columns:
            try:
                df[field] = df[field].astype(expected_type)
                logger.info(f"Field '{field}' converted to {expected_type.__name__}")
            except Exception as e:
                logger.error(f"Failed to convert field '{field}' to {expected_type.__name__}")
                raise ValueError(f"Failed to convert field '{field}' to {expected_type}") from e
        else:
            logger.warning(f"Field '{field}' not found in DataFrame")
    return df


def validate_dataframe(df: pd.DataFrame, required_fields: list = None, field_types: dict = None) -> pd.DataFrame:
    """
    Full validation pipeline for a DataFrame:
    - Checks required fields
    - Checks field types

    Args:
        df (pd.DataFrame): DataFrame to validate.
        required_fields (list, optional): List of required columns.
        field_types (dict, optional): Dictionary of column:type mappings.

    Returns:
        pd.DataFrame: Validated DataFrame.
    """
    if required_fields:
        df = validate_required_fields(df, required_fields)
    if field_types:
        df = validate_field_types(df, field_types)
    return df
