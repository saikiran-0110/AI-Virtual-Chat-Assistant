"""
White-Box Testing: Statement Coverage
Technique: Ensure every line of code executes at least once
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


class TestDictionaryStatementCoverage(unittest.TestCase):
    """White-Box Statement Coverage Tests for Dictionary"""
    
    def setUp(self):
        self.dictionary = Dictionary()
    
    def test_lookup_statement_coverage(self):
        """Statement Coverage: lookup() method - all lines"""
        result = self.dictionary.lookup("python")
        self.assertIn("python", result.lower())
        print("✓ Covered: lookup() method")
    
    def test_lookup_empty_word_statement(self):
        """Statement Coverage: lookup() - empty word check"""
        result = self.dictionary.lookup("")
        self.assertIn("provide a word", result.lower())
        print("✓ Covered: lookup() empty word check")
    
    def test_lookup_word_found_statement(self):
        """Statement Coverage: lookup() - word found branch"""
        result = self.dictionary.lookup("python")
        self.assertIn("python", result.lower())
        self.assertIn("programming", result.lower())
        print("✓ Covered: lookup() word found")
    
    def test_lookup_word_not_found_statement(self):
        """Statement Coverage: lookup() - word not found branch"""
        result = self.dictionary.lookup("nonexistent")
        self.assertIn("no definition found", result.lower())
        print("✓ Covered: lookup() word not found")


if __name__ == '__main__':
    unittest.main(verbosity=2)

