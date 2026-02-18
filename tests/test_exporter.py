import unittest
import os
import pandas as pd
from src.exporter import export_to_csv, export_to_excel

class TestExporter(unittest.TestCase):
    """Unit tests for exporter.py"""

    def setUp(self):
        """Set up test DataFrame and output paths"""
        self.df = pd.DataFrame({
            "Name": ["Alice", "Bob"],
            "Age": [25, 30]
        })
        self.csv_path = "tests/test_output.csv"
        self.xlsx_path = "tests/test_output.xlsx"

        # Ensure tests folder exists
        os.makedirs("tests", exist_ok=True)

    def tearDown(self):
        """Remove test files after tests"""
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        if os.path.exists(self.xlsx_path):
            os.remove(self.xlsx_path)

    def test_export_to_csv(self):
        """Test exporting DataFrame to CSV"""
        export_to_csv(self.df, self.csv_path)
        self.assertTrue(os.path.exists(self.csv_path))
        # Read back CSV and check contents
        df_loaded = pd.read_csv(self.csv_path)
        self.assertEqual(df_loaded.shape, self.df.shape)

    def test_export_to_excel(self):
        """Test exporting DataFrame to Excel"""
        export_to_excel(self.df, self.xlsx_path)
        self.assertTrue(os.path.exists(self.xlsx_path))
        # Read back Excel and check contents
        df_loaded = pd.read_excel(self.xlsx_path)
        self.assertEqual(df_loaded.shape, self.df.shape)

    def test_export_empty_dataframe_csv(self):
        """Test exporting empty DataFrame raises ValueError (CSV)"""
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            export_to_csv(empty_df, self.csv_path)

    def test_export_empty_dataframe_excel(self):
        """Test exporting empty DataFrame raises ValueError (Excel)"""
        empty_df = pd.DataFrame()
        with self.assertRaises(ValueError):
            export_to_excel(empty_df, self.xlsx_path)


if __name__ == "__main__":
    unittest.main()
