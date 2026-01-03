"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning
Function: Note File Storage Handler (Serialization)
Student: Abhinay Karnati (259050844)
"""

import unittest
import sys
import os
import json
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


class TestNoteStorageSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Note Storage
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
    
    def test_save_notes_to_file(self):
        """
        Test Case: Save notes to file
        Input: Create notes, save
        Expected Output: File should contain note data
        Technique: Serialization verification
        """
        self.note_mgr.create_note("Note 1", "Content 1")
        self.note_mgr.create_note("Note 2", "Content 2")
        self.assertTrue(os.path.exists(self.temp_file.name))
        with open(self.temp_file.name, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("notes", data)
            self.assertEqual(len(data["notes"]), 2)
        print("✓ PASS: Save notes to file - File contains note data")
    
    def test_load_notes_from_file(self):
        """
        Test Case: Load notes from file
        Input: Save notes, create new instance, load
        Expected Output: Notes should be loaded
        Technique: Serialization verification
        """
        self.note_mgr.create_note("Persistent Note", "This should persist")
        new_mgr = NoteManager(file_path=self.temp_file.name)
        result = new_mgr.list_all_notes()
        self.assertIn("Persistent Note", result)
        print("✓ PASS: Load notes from file - Notes loaded from file")
    
    def test_save_after_update(self):
        """
        Test Case: Save after updating note
        Input: Create note, update, save
        Expected Output: Updated note should be saved
        Technique: Serialization after modification
        """
        self.note_mgr.create_note("Original", "Content")
        self.note_mgr.update_note(1, title="Updated")
        new_mgr = NoteManager(file_path=self.temp_file.name)
        result = new_mgr.retrieve_note(1)
        self.assertIn("Updated", result)
        print("✓ PASS: Save after update - Updated note persisted")
    
    def test_save_after_delete(self):
        """
        Test Case: Save after deleting note
        Input: Create notes, delete one, save
        Expected Output: Deleted note should not be in file
        Technique: Serialization after deletion
        """
        self.note_mgr.create_note("Note 1", "Content 1")
        self.note_mgr.create_note("Note 2", "Content 2")
        self.note_mgr.delete_note(1)
        new_mgr = NoteManager(file_path=self.temp_file.name)
        result = new_mgr.list_all_notes()
        self.assertNotIn("Note 1", result)
        self.assertIn("Note 2", result)
        print("✓ PASS: Save after delete - Deleted note not in file")


if __name__ == '__main__':
    unittest.main(verbosity=2)

