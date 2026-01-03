"""
White-Box Testing: Branch Coverage
Technique: Ensure every decision (True/False) is tested
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


class TestDictionaryBranchCoverage(unittest.TestCase):
    """White-Box Branch Coverage Tests for Dictionary"""
    
    def setUp(self):
        self.dictionary = Dictionary()
    
    # Branch: if not word.strip() in lookup
    def test_branch_lookup_empty_word_true(self):
        """Branch Coverage: if not word.strip() (TRUE branch)"""
        result = self.dictionary.lookup("")
        self.assertIn("provide a word", result.lower())
        print("✓ Branch: lookup empty word (TRUE)")
    
    def test_branch_lookup_empty_word_false(self):
        """Branch Coverage: if not word.strip() (FALSE branch)"""
        result = self.dictionary.lookup("python")
        self.assertIn("python", result.lower())
        print("✓ Branch: lookup empty word (FALSE)")
    
    # Branch: if word_lower in self._definitions in lookup
    def test_branch_lookup_word_found_true(self):
        """Branch Coverage: if word_lower in self._definitions (TRUE branch)"""
        result = self.dictionary.lookup("python")
        self.assertIn("python", result.lower())
        self.assertIn("programming", result.lower())
        print("✓ Branch: lookup word found (TRUE)")
    
    def test_branch_lookup_word_found_false(self):
        """Branch Coverage: if word_lower in self._definitions (FALSE branch)"""
        result = self.dictionary.lookup("nonexistent")
        self.assertIn("no definition found", result.lower())
        print("✓ Branch: lookup word found (FALSE)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

