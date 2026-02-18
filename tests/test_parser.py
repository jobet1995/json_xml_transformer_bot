import unittest
import tempfile
import os
import json
import xml.etree.ElementTree as ET
from src.parser import (
    load_json_file,
    load_multiple_json,
    load_xml_file,
    load_multiple_xml
)

class TestParser(unittest.TestCase):
    """Unit tests for parser.py"""

    def setUp(self):
        """Set up temporary JSON and XML files safely"""

        # -------------------------
        # JSON files
        # -------------------------
        self.sample_json = {"Name": "Alice", "Age": 25, "Email": "alice@test.com"}
        self.temp_json = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8')
        json.dump(self.sample_json, self.temp_json)
        self.temp_json.close()  # critical for Windows

        self.sample_json2 = {"Name": "Bob", "Age": 30, "Email": "bob@test.com"}
        self.temp_json2 = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8')
        json.dump(self.sample_json2, self.temp_json2)
        self.temp_json2.close()

        # -------------------------
        # XML files
        # -------------------------
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

        self.temp_xml2 = tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode='w', encoding='utf-8')
        self.temp_xml2.write(self.xml_content)
        self.temp_xml2.close()

    def tearDown(self):
        """Remove temporary files"""
        os.unlink(self.temp_json.name)
        os.unlink(self.temp_json2.name)
        os.unlink(self.temp_xml.name)
        os.unlink(self.temp_xml2.name)

    # -------------------------
    # JSON tests
    # -------------------------
    def test_load_json_file(self):
        data = load_json_file(self.temp_json.name, safe=True)
        self.assertIsInstance(data, dict)
        self.assertEqual(data["Name"], "Alice")

    def test_load_multiple_json(self):
        files = [self.temp_json.name, self.temp_json2.name]
        data_list = load_multiple_json(files)
        self.assertEqual(len(data_list), 2)
        self.assertEqual(data_list[1]["Name"], "Bob")

    def test_load_json_file_not_found(self):
        # Use safe=False to force exception
        with self.assertRaises(FileNotFoundError):
            load_json_file("nonexistent.json", safe=False)

    def test_load_invalid_json(self):
        temp_invalid = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8')
        temp_invalid.write("invalid json")  # malformed JSON
        temp_invalid.close()
        with self.assertRaises(json.JSONDecodeError):
            load_json_file(temp_invalid.name, safe=False)
        os.unlink(temp_invalid.name)

    # -------------------------
    # XML tests
    # -------------------------
    def test_load_xml_file(self):
        root = load_xml_file(self.temp_xml.name, safe=True)
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(root.tag, "People")
        persons = root.findall("Person")
        self.assertEqual(len(persons), 2)

    def test_load_multiple_xml(self):
        files = [self.temp_xml.name, self.temp_xml2.name]
        roots = load_multiple_xml(files)
        self.assertEqual(len(roots), 2)
        self.assertEqual(roots[0].tag, "People")
        self.assertEqual(len(roots[1].findall("Person")), 2)

    def test_load_xml_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            load_xml_file("nonexistent.xml", safe=False)

    def test_load_invalid_xml(self):
        temp_invalid = tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode='w', encoding='utf-8')
        temp_invalid.write("<root><unclosed></root>")  # malformed XML
        temp_invalid.close()
        with self.assertRaises(ET.ParseError):
            load_xml_file(temp_invalid.name, safe=False)
        os.unlink(temp_invalid.name)


if __name__ == "__main__":
    unittest.main()
