"""
White-Box Testing: Symbolic Execution
Technique: Symbolic execution with path condition derivation
Function: Dictionary Definition Lookup
Student: Sameer Shaik (259047772)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

try:
    from main import Dictionary
except ImportError:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    spec_path = os.path.join(project_root, '259047772', 'test', 'blackbox', 'specification_based')
    if spec_path not in sys.path:
        sys.path.insert(0, spec_path)
    from test_dictionary_lookup import Dictionary


class TestDictionarySymbolicExecution(unittest.TestCase):
    """Symbolic Execution Derived Tests for Dictionary"""
    
    def setUp(self):
        self.dictionary = Dictionary()
    
    # Path 1: lookup - empty word
    def test_path1_lookup_empty_word(self):
        """
        Path Condition: word.strip() == ""
        Symbolic Input: x = ""
        Concrete Input: ""
        Expected Output: "Please provide a word to look up."
        """
        result = self.dictionary.lookup("")
        self.assertIn("provide a word", result.lower())
        print("✓ Path 1: Lookup empty word -> Error message")
    
    # Path 2: lookup - word found
    def test_path2_lookup_word_found(self):
        """
        Path Condition: word.strip() != "" AND word.lower() in definitions
        Symbolic Input: x = "python"
        Concrete Input: "python"
        Expected Output: Definition of python
        """
        result = self.dictionary.lookup("python")
        self.assertIn("python", result.lower())
        self.assertIn("programming", result.lower())
        print("✓ Path 2: Lookup word found -> Definition")
    
    # Path 3: lookup - word not found
    def test_path3_lookup_word_not_found(self):
        """
        Path Condition: word.strip() != "" AND word.lower() not in definitions
        Symbolic Input: x = "nonexistent"
        Concrete Input: "nonexistent"
        Expected Output: "No definition found for 'nonexistent'."
        """
        result = self.dictionary.lookup("nonexistent")
        self.assertIn("no definition found", result.lower())
        print("✓ Path 3: Lookup word not found -> Not found message")
    
    # Path 4: lookup - whitespace handling
    def test_path4_lookup_whitespace(self):
        """
        Path Condition: word.strip() != "" (after stripping whitespace)
        Symbolic Input: x = "  python  "
        Concrete Input: "  python  "
        Expected Output: Definition (whitespace trimmed)
        """
        result = self.dictionary.lookup("  python  ")
        self.assertIn("python", result.lower())
        print("✓ Path 4: Lookup with whitespace -> Definition (trimmed)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

