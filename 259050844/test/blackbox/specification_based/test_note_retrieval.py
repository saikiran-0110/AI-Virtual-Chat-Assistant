"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
Function: Note Retrieval & Viewing
Student: Abhinay Karnati (259050844)
"""

import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

try:
    from main import NoteManager
except ImportError:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    spec_path = os.path.join(project_root, '259050844', 'test', 'blackbox', 'specification_based')
    if spec_path not in sys.path:
        sys.path.insert(0, spec_path)
    from test_note_creation import NoteManager


class TestNoteRetrievalSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Note Retrieval
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.note_mgr = NoteManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        """Clean up"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_retrieve_note_valid_id(self):
        """
        Test Case: Retrieve note with valid ID
        Input: id=1
        Expected Output: Note details
        Technique: Valid input partition
        """
        self.note_mgr.create_note("Test Note", "Test content")
        result = self.note_mgr.retrieve_note(1)
        self.assertIn("Test Note", result)
        self.assertIn("Test content", result)
        print(f"✓ PASS: Retrieve note (valid ID) - Input: id=1, Output: {result[:50]}...")
    
    def test_retrieve_note_invalid_id(self):
        """
        Test Case: Retrieve note with invalid ID
        Input: id=999
        Expected Output: Error message
        Technique: Invalid input partition
        """
        result = self.note_mgr.retrieve_note(999)
        self.assertIn("not found", result.lower())
        print(f"✓ PASS: Retrieve note (invalid ID) - Input: id=999, Output: {result}")
    
    def test_retrieve_note_negative_id(self):
        """
        Test Case: Retrieve note with negative ID
        Input: id=-1
        Expected Output: Error message
        Technique: Boundary value - negative number
        """
        result = self.note_mgr.retrieve_note(-1)
        self.assertIn("not found", result.lower())
        print(f"✓ PASS: Retrieve note (negative ID) - Input: id=-1, Output: {result}")
    
    def test_list_all_notes_empty(self):
        """
        Test Case: List all notes when none exist
        Input: No notes
        Expected Output: "No notes found"
        Technique: Empty state partition
        """
        result = self.note_mgr.list_all_notes()
        self.assertIn("no notes", result.lower())
        print(f"✓ PASS: List notes (empty) - Output: {result}")
    
    def test_list_all_notes_with_data(self):
        """
        Test Case: List all notes with data
        Input: Create notes, then list
        Expected Output: List of all notes
        Technique: Valid state partition
        """
        self.note_mgr.create_note("Note 1", "Content 1")
        self.note_mgr.create_note("Note 2", "Content 2")
        result = self.note_mgr.list_all_notes()
        self.assertIn("Note 1", result)
        self.assertIn("Note 2", result)
        print("✓ PASS: List notes (with data) - Output contains all notes")


if __name__ == '__main__':
    unittest.main(verbosity=2)

