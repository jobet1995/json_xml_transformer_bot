"""
parser.py
----------
Parses JSON and XML files into Python objects for transformation.

Features:
- Load single or multiple JSON files (dict or list)
- Load single or multiple XML files
- Handles empty files, BOM, whitespace, and malformed content
- Optional safe mode: return None instead of raising exceptions
- Integrated logging
Author: Jobet Casquejo
"""

import json
from pathlib import Path
import xml.etree.ElementTree as ET
from src.logger import get_logger

logger = get_logger(__name__)

# -------------------------
# JSON Parsing
# -------------------------
def load_json_file(file_path: str, safe: bool = True) -> dict | list | None:
    path = Path(file_path)
    if not path.is_file():
        msg = f"JSON file not found: {file_path}"
        logger.error(msg)
        if safe:
            return None
        else:
            raise FileNotFoundError(msg)

    try:
        content = path.read_text(encoding="utf-8-sig").strip()
        if not content:
            msg = f"JSON file is empty or contains only whitespace: {file_path}"
            logger.error(msg)
            if safe:
                return None
            else:
                raise json.JSONDecodeError(msg, content, 0)

        data = json.loads(content)
        return data

    except json.JSONDecodeError as e:
        logger.exception(f"Failed to parse JSON file: {file_path}")
        if safe:
            return None
        else:
            raise e


def load_multiple_json(files: list[str], safe: bool = True) -> list[dict | list]:
    all_data = []
    for file in files:
        data = load_json_file(file, safe=safe)
        if data is not None:
            all_data.append(data)
    return all_data


# -------------------------
# XML Parsing
# -------------------------
def load_xml_file(file_path: str, safe: bool = True) -> ET.Element | None:
    path = Path(file_path)
    if not path.is_file():
        msg = f"XML file not found: {file_path}"
        logger.error(msg)
        if safe:
            return None
        else:
            raise FileNotFoundError(msg)

    try:
        content = path.read_text(encoding="utf-8-sig").strip()
        if not content:
            msg = f"XML file is empty: {file_path}"
            logger.error(msg)
            if safe:
                return None
            else:
                raise ET.ParseError(msg)

        tree = ET.ElementTree(ET.fromstring(content))
        root = tree.getroot()
        return root

    except ET.ParseError as e:
        logger.exception(f"Failed to parse XML file: {file_path}")
        if safe:
            return None
        else:
            raise e


def load_multiple_xml(files: list[str], safe: bool = True) -> list[ET.Element]:
    all_roots = []
    for file in files:
        root = load_xml_file(file, safe=safe)
        if root is not None:
            all_roots.append(root)
    return all_roots
