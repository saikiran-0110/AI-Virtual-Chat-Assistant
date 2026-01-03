"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
Function: Note Update & Edit Logic
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


class TestNoteUpdateSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Note Update
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
    
    def test_update_note_title(self):
        """
        Test Case: Update note title
        Input: id=1, title="Updated Title"
        Expected Output: "Note updated."
        Technique: Valid input partition
        """
        self.note_mgr.create_note("Original Title", "Content")
        result = self.note_mgr.update_note(1, title="Updated Title")
        self.assertIn("updated", result.lower())
        retrieved = self.note_mgr.retrieve_note(1)
        self.assertIn("Updated Title", retrieved)
        print(f"✓ PASS: Update note title - Input: id=1, title='Updated Title', Output: {result}")
    
    def test_update_note_content(self):
        """
        Test Case: Update note content
        Input: id=1, content="Updated content"
        Expected Output: "Note updated."
        Technique: Valid input partition
        """
        self.note_mgr.create_note("Title", "Original content")
        result = self.note_mgr.update_note(1, content="Updated content")
        self.assertIn("updated", result.lower())
        retrieved = self.note_mgr.retrieve_note(1)
        self.assertIn("Updated content", retrieved)
        print(f"✓ PASS: Update note content - Input: id=1, content='Updated content', Output: {result}")
    
    def test_update_note_tags(self):
        """
        Test Case: Update note tags
        Input: id=1, tags=["new", "tags"]
        Expected Output: "Note updated."
        Technique: Valid input partition
        """
        self.note_mgr.create_note("Title", "Content", tags=["old"])
        result = self.note_mgr.update_note(1, tags=["new", "tags"])
        self.assertIn("updated", result.lower())
        print(f"✓ PASS: Update note tags - Input: id=1, tags=['new', 'tags'], Output: {result}")
    
    def test_update_note_invalid_id(self):
        """
        Test Case: Update note with invalid ID
        Input: id=999, title="New Title"
        Expected Output: Error message
        Technique: Invalid input partition
        """
        result = self.note_mgr.update_note(999, title="New Title")
        self.assertIn("not found", result.lower())
        print(f"✓ PASS: Update note (invalid ID) - Input: id=999, Output: {result}")
    
    def test_update_note_empty_title(self):
        """
        Test Case: Update note with empty title
        Input: id=1, title=""
        Expected Output: Error message
        Technique: Invalid input partition
        """
        self.note_mgr.create_note("Title", "Content")
        result = self.note_mgr.update_note(1, title="")
        self.assertIn("cannot be empty", result.lower())
        print(f"✓ PASS: Update note (empty title) - Input: title='', Output: {result}")
    
    def test_update_note_all_fields(self):
        """
        Test Case: Update all note fields
        Input: id=1, title="New Title", content="New content", tags=["new"]
        Expected Output: "Note updated."
        Technique: Valid input partition - multiple fields
        """
        self.note_mgr.create_note("Old Title", "Old content", tags=["old"])
        result = self.note_mgr.update_note(1, title="New Title", content="New content", tags=["new"])
        self.assertIn("updated", result.lower())
        retrieved = self.note_mgr.retrieve_note(1)
        self.assertIn("New Title", retrieved)
        self.assertIn("New content", retrieved)
        print("✓ PASS: Update note (all fields) - All fields updated")


if __name__ == '__main__':
    unittest.main(verbosity=2)

