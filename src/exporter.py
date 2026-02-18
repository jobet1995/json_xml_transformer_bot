"""
exporter.py
-------------
Handles exporting pandas DataFrames to CSV, Excel, or SQL databases.
Integrated with professional logging.

Author: Jobet Casquejo
"""

import pandas as pd
import os
from src.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


def export_to_csv(df: pd.DataFrame, output_path: str, index: bool = False) -> None:
    """
    Export DataFrame to CSV file.

    Args:
        df (pd.DataFrame): DataFrame to export.
        output_path (str): Full file path to save CSV.
        index (bool): Whether to write row indices. Default is False.

    Raises:
        ValueError: If DataFrame is empty.
        Exception: For any unexpected file I/O errors.
    """
    if df.empty:
        logger.error("Attempted to export an empty DataFrame to CSV.")
        raise ValueError("Cannot export an empty DataFrame.")

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=index, encoding='utf-8-sig')
        logger.info(f"DataFrame successfully exported to CSV: {output_path}")
    except Exception as e:
        logger.exception(f"Failed to export DataFrame to CSV: {output_path}")
        raise e


def export_to_excel(df: pd.DataFrame, output_path: str, index: bool = False) -> None:
    """
    Export DataFrame to Excel file (.xlsx).

    Args:
        df (pd.DataFrame): DataFrame to export.
        output_path (str): Full file path to save Excel.
        index (bool): Whether to write row indices. Default is False.

    Raises:
        ValueError: If DataFrame is empty.
        Exception: For any unexpected file I/O errors.
    """
    if df.empty:
        logger.error("Attempted to export an empty DataFrame to Excel.")
        raise ValueError("Cannot export an empty DataFrame.")

    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=index, engine='openpyxl')
        logger.info(f"DataFrame successfully exported to Excel: {output_path}")
    except Exception as e:
        logger.exception(f"Failed to export DataFrame to Excel: {output_path}")
        raise e


def export_to_sql(df: pd.DataFrame, db_connection, table_name: str, if_exists: str = "replace") -> None:
    """
    Export DataFrame to SQL database table.

    Args:
        df (pd.DataFrame): DataFrame to export.
        db_connection: SQLAlchemy or sqlite3 connection object.
        table_name (str): Table name to export to.
        if_exists (str): Behavior if table exists: 'fail', 'replace', or 'append'. Default is 'replace'.

    Raises:
        ValueError: If DataFrame is empty.
        Exception: For any unexpected SQL errors.
    """
    if df.empty:
        logger.error("Attempted to export an empty DataFrame to SQL.")
        raise ValueError("Cannot export an empty DataFrame.")

    try:
        df.to_sql(name=table_name, con=db_connection, if_exists=if_exists, index=False)
        logger.info(f"DataFrame successfully exported to SQL table: {table_name}")
    except Exception as e:
        logger.exception(f"Failed to export DataFrame to SQL table: {table_name}")
        raise e
