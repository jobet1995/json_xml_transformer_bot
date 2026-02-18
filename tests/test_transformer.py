import unittest
import pandas as pd
import tempfile
import os
import json
from src.transformer import (
    flatten_json,
    json_to_dataframe,
    json_file_to_dataframe,
    xml_to_dataframe,
    rename_columns,
    transform_dataframe
)

class TestTransformer(unittest.TestCase):
    """Unit tests for transformer.py"""

    def setUp(self):
        """Set up temporary JSON and XML files"""

        # Nested JSON data
        self.json_data = [
            {"Name": "Alice", "Details": {"Age": "25", "Email": "alice@test.com"}},
            {"Name": "Bob", "Details": {"Age": "30", "Email": "bob@test.com"}}
        ]
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8')
        json.dump(self.json_data, self.temp_json)
        self.temp_json.close()

        # Sample XML
        self.xml_content = """<?xml version="1.0"?>
        <People>
            <Person>
                <Name>Alice</Name>
                <Age>25</Age>
                <Email>alice@test.com</Email>
            </Person>
            <Person>
                <Name>Bob</Name>
                <Age>30</Age>
                <Email>bob@test.com</Email>
            </Person>
        </People>
        """
        self.temp_xml = tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode='w', encoding='utf-8')
        self.temp_xml.write(self.xml_content)
        self.temp_xml.close()

    def tearDown(self):
        os.unlink(self.temp_json.name)
        os.unlink(self.temp_xml.name)

    # -------------------------
    # JSON tests
    # -------------------------
    def test_json_file_to_dataframe(self):
        df = json_file_to_dataframe(self.temp_json.name)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("Details.Age", df.columns)
        self.assertEqual(df.shape[0], 2)

    def test_flatten_json(self):
        nested_json = {"A": {"B": 1, "C": {"D": 2}}, "E": 3}
        flat = flatten_json(nested_json)
        expected = {"A.B": 1, "A.C.D": 2, "E": 3}
        self.assertEqual(flat, expected)

    def test_json_to_dataframe(self):
        df = json_to_dataframe(self.json_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("Details.Age", df.columns)
        self.assertEqual(df.shape[0], 2)

    # -------------------------
    # XML tests
    # -------------------------
    def test_xml_to_dataframe(self):
        df = xml_to_dataframe(self.temp_xml.name, record_tag="Person")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("Name", df.columns)
        self.assertEqual(df.shape[0], 2)

    # -------------------------
    # Column and transformation tests
    # -------------------------
    def test_rename_columns(self):
        df = json_to_dataframe(self.json_data)
        df_renamed = rename_columns(df, {"Details.Age": "Age"})
        self.assertIn("Age", df_renamed.columns)

    def test_transform_dataframe(self):
        df = json_to_dataframe(self.json_data)
        df_renamed = rename_columns(df, {"Details.Age": "Age"})
        df_transformed = transform_dataframe(df_renamed, {"Age": int})
        self.assertTrue(pd.api.types.is_integer_dtype(df_transformed["Age"]))
        self.assertEqual(df_transformed["Age"].iloc[0], 25)
        df_transformed = transform_dataframe(df_transformed, {"Age": lambda x: x + 1})
        self.assertEqual(df_transformed["Age"].iloc[0], 26)
        self.assertEqual(df_transformed["Age"].iloc[1], 31)


if __name__ == "__main__":
    unittest.main()
