import unittest
import pandas as pd
from src.validator import validate_required_fields, validate_field_types, validate_dataframe

class TestValidator(unittest.TestCase):
    """Unit tests for validator.py"""

    def setUp(self):
        """Set up a sample DataFrame for testing"""
        self.df = pd.DataFrame({
            "Name": ["Alice", "Bob", None],
            "Age": ["25", "30", None],
            "Email": ["alice@test.com", None, None]
        })

    # -------------------------
    # Test required fields
    # -------------------------
    def test_validate_required_fields_success(self):
        """Should return valid rows when required fields exist"""
        required_fields = ["Name", "Age"]
        df_valid = validate_required_fields(self.df, required_fields)
        self.assertEqual(len(df_valid), 2)  # Drops the row with None in Name & Age

    def test_validate_required_fields_missing_column(self):
        """Should raise ValueError if required column is missing"""
        required_fields = ["Name", "Age", "Address"]
        with self.assertRaises(ValueError):
            validate_required_fields(self.df, required_fields)

    # -------------------------
    # Test field type conversion
    # -------------------------
    def test_validate_field_types_success(self):
        """Should convert Age to int"""
        field_types = {"Age": int}
        df_converted = validate_field_types(self.df.dropna(subset=["Age"]), field_types)
        self.assertTrue(pd.api.types.is_integer_dtype(df_converted["Age"]))

    def test_validate_field_types_missing_column(self):
        """Should warn if column not present but not fail"""
        field_types = {"Salary": float}  # Column doesn't exist
        df_result = validate_field_types(self.df, field_types)
        self.assertIn("Age", df_result.columns)

    def test_validate_field_types_fail_conversion(self):
        """Should raise ValueError if conversion fails for non-null values"""
        df_invalid = pd.DataFrame({"Age": ["25", "thirty"]})  # 'thirty' cannot convert to int
        field_types = {"Age": int}
        with self.assertRaises(ValueError):
            validate_field_types(df_invalid, field_types)

    # -------------------------
    # Test full validation pipeline
    # -------------------------
    def test_validate_dataframe_full_pipeline(self):
        """Should perform both required field and type validation"""
        required_fields = ["Name", "Age"]
        field_types = {"Age": int}
        df_valid = validate_dataframe(self.df, required_fields, field_types)
        self.assertEqual(len(df_valid), 2)
        self.assertTrue(pd.api.types.is_integer_dtype(df_valid["Age"]))


if __name__ == "__main__":
    unittest.main()
