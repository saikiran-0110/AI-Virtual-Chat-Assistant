"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
Function: Note Deletion Function
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


class TestNoteDeletionSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Note Deletion
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
    
    def test_delete_note_valid_id(self):
        """
        Test Case: Delete note with valid ID
        Input: id=1
        Expected Output: "Note deleted. ID=1"
        Technique: Valid input partition
        """
        self.note_mgr.create_note("Note to delete", "Content")
        result = self.note_mgr.delete_note(1)
        self.assertIn("deleted", result.lower())
        self.assertIn("ID=1", result)
        print(f"✓ PASS: Delete note (valid ID) - Input: id=1, Output: {result}")
    
    def test_delete_note_invalid_id(self):
        """
        Test Case: Delete note with invalid ID
        Input: id=999
        Expected Output: Error message
        Technique: Invalid input partition
        """
        result = self.note_mgr.delete_note(999)
        self.assertIn("not found", result.lower())
        print(f"✓ PASS: Delete note (invalid ID) - Input: id=999, Output: {result}")
    
    def test_delete_note_negative_id(self):
        """
        Test Case: Delete note with negative ID
        Input: id=-1
        Expected Output: Error message
        Technique: Boundary value - negative number
        """
        result = self.note_mgr.delete_note(-1)
        self.assertIn("not found", result.lower())
        print(f"✓ PASS: Delete note (negative ID) - Input: id=-1, Output: {result}")
    
    def test_delete_note_zero_id(self):
        """
        Test Case: Delete note with zero ID
        Input: id=0
        Expected Output: Error message
        Technique: Boundary value - zero
        """
        result = self.note_mgr.delete_note(0)
        self.assertIn("not found", result.lower())
        print(f"✓ PASS: Delete note (zero ID) - Input: id=0, Output: {result}")
    
    def test_delete_multiple_notes(self):
        """
        Test Case: Delete multiple notes
        Input: Create 3 notes, delete 2
        Expected Output: Remaining note should exist
        Technique: Valid state partition
        """
        self.note_mgr.create_note("Note 1", "Content 1")
        self.note_mgr.create_note("Note 2", "Content 2")
        self.note_mgr.create_note("Note 3", "Content 3")
        self.note_mgr.delete_note(1)
        self.note_mgr.delete_note(2)
        result = self.note_mgr.list_all_notes()
        self.assertIn("Note 3", result)
        self.assertNotIn("Note 1", result)
        print("✓ PASS: Delete multiple notes - Remaining notes correct")


if __name__ == '__main__':
    unittest.main(verbosity=2)

