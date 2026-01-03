"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
Functions: Knowledge Snippet Database, Snippet Retrieval Logic, Snippet File Serialization
Student: Sameer Shaik (259047772)
"""

import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import KeywordSnippetAssistant, PersistentSnippets


class TestSnippetSystemSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Snippet System
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.keyword_assistant = KeywordSnippetAssistant()
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.persistent = PersistentSnippets(file_path=self.temp_file.name)
    
    def tearDown(self):
        """Clean up"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_build_snippets_database(self):
        """
        Test Case: Build snippets database
        Input: Initialize KeywordSnippetAssistant
        Expected Output: Snippets database created
        Technique: Database initialization verification
        """
        self.assertIsNotNone(self.keyword_assistant._snippets)
        self.assertGreater(len(self.keyword_assistant._snippets), 0)
        print("✓ PASS: Build snippets database - Database initialized")
    
    def test_retrieve_snippet_by_keyword(self):
        """
        Test Case: Retrieve snippet using keywords
        Input: "ask privacy"
        Expected Output: Snippet about privacy
        Technique: Valid input partition
        """
        result = self.keyword_assistant.handle("ask privacy")
        self.assertIn("privacy", result.lower())
        print(f"✓ PASS: Retrieve snippet by keyword - Input: 'ask privacy', Output: {result[:50]}...")
    
    def test_retrieve_snippet_by_id(self):
        """
        Test Case: Retrieve snippet by ID
        Input: "show 1"
        Expected Output: Snippet with ID 1
        Technique: Valid input partition
        """
        result = self.keyword_assistant.handle("show 1")
        self.assertIn("ID: 1", result)
        print(f"✓ PASS: Retrieve snippet by ID - Input: 'show 1', Output: {result[:50]}...")
    
    def test_list_all_snippets(self):
        """
        Test Case: List all snippets
        Input: "all"
        Expected Output: List of all snippets
        Technique: Valid input partition
        """
        result = self.keyword_assistant.handle("all")
        self.assertIn("All snippets:", result)
        print(f"✓ PASS: List all snippets - Input: 'all', Output: {result[:50]}...")
    
    def test_snippet_serialization_save(self):
        """
        Test Case: Snippet serialization - save to file
        Input: Add snippet, save
        Expected Output: File should contain snippet data
        Technique: Serialization verification
        """
        self.persistent.handle("add Test Snippet | Test content")
        self.assertTrue(os.path.exists(self.temp_file.name))
        with open(self.temp_file.name, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("snippets", data)
        print("✓ PASS: Snippet serialization (save) - File contains snippet data")
    
    def test_snippet_serialization_load(self):
        """
        Test Case: Snippet serialization - load from file
        Input: Save snippet, create new instance, load
        Expected Output: Snippet should be loaded
        Technique: Serialization verification
        """
        self.persistent.handle("add Persistent Snippet | This should persist")
        new_persistent = PersistentSnippets(file_path=self.temp_file.name)
        result = new_persistent.handle("list")
        self.assertIn("Persistent Snippet", result)
        print("✓ PASS: Snippet serialization (load) - Snippet loaded from file")
    
    def test_search_snippets_by_keyword(self):
        """
        Test Case: Search snippets by keyword
        Input: "search privacy"
        Expected Output: Snippets containing "privacy"
        Technique: Valid input partition
        """
        result = self.persistent.handle("search privacy")
        self.assertIn("privacy", result.lower())
        print(f"✓ PASS: Search snippets by keyword - Input: 'search privacy', Output: {result[:50]}...")


if __name__ == '__main__':
    unittest.main(verbosity=2)

