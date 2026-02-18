import pandas as pd
import json
import xml.etree.ElementTree as ET
from src.logger import get_logger

logger = get_logger(__name__)


# -------------------------
# JSON flattening
# -------------------------
def flatten_json(json_obj: dict, prefix: str = '') -> dict:
    """
    Flatten a nested JSON object into a single-level dictionary.
    """
    flat_dict = {}
    for key, value in json_obj.items():
        new_key = f"{prefix}{key}" if prefix == '' else f"{prefix}.{key}"
        if isinstance(value, dict):
            flat_dict.update(flatten_json(value, new_key))
        else:
            flat_dict[new_key] = value
    return flat_dict


def json_to_dataframe(json_data: list) -> pd.DataFrame:
    """
    Convert a list of JSON objects (already loaded) to a flattened DataFrame.
    """
    try:
        flattened_data = [flatten_json(item) for item in json_data]
        df = pd.DataFrame(flattened_data)
        logger.info(f"Converted JSON data to DataFrame with shape {df.shape}")
        return df
    except Exception as e:
        logger.exception("Failed to convert JSON data to DataFrame")
        raise e


def json_file_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Load a JSON file from disk and convert it to a flattened DataFrame.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        logger.info(f"Loaded JSON file: {file_path}")
        return json_to_dataframe(json_data)
    except FileNotFoundError:
        logger.error(f"JSON file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.exception(f"Failed to parse JSON file: {file_path}")
        raise e


# -------------------------
# XML to DataFrame
# -------------------------
def xml_to_dataframe(xml_file_path: str, record_tag: str) -> pd.DataFrame:
    """
    Convert XML file to pandas DataFrame.
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        records = []

        for record in root.findall(record_tag):
            record_dict = {child.tag: child.text for child in record}
            records.append(record_dict)

        df = pd.DataFrame(records)
        logger.info(f"Converted XML file '{xml_file_path}' to DataFrame with shape {df.shape}")
        return df
    except Exception as e:
        logger.exception(f"Failed to convert XML file '{xml_file_path}' to DataFrame")
        raise e


# -------------------------
# Column renaming
# -------------------------
def rename_columns(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """
    Rename columns in a DataFrame according to a mapping dictionary.
    """
    try:
        df = df.rename(columns=column_mapping)
        logger.info(f"Renamed columns: {list(column_mapping.keys())} -> {list(column_mapping.values())}")
        return df
    except Exception as e:
        logger.exception("Failed to rename columns in DataFrame")
        raise e


# -------------------------
# Data transformations
# -------------------------
def transform_dataframe(df: pd.DataFrame, transformations: dict = None) -> pd.DataFrame:
    """
    Apply optional transformations to DataFrame columns.
    """
    if not transformations:
        return df

    for column, func in transformations.items():
        if column in df.columns:
            try:
                df[column] = df[column].apply(func)
                logger.info(f"Applied transformation to column '{column}'")
            except Exception as e:
                logger.warning(f"Failed to transform column '{column}': {e}")
        else:
            logger.warning(f"Column '{column}' not found for transformation")
    return df
