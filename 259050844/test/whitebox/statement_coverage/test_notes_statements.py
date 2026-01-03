"""
White-Box Testing: Statement Coverage
Technique: Ensure every line of code executes at least once
Functions: Note Creation, Retrieval, Deletion, Search, Update, Storage
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


class TestNotesStatementCoverage(unittest.TestCase):
    """White-Box Statement Coverage Tests for Notes System"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.note_mgr = NoteManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_note_statement_coverage(self):
        """Statement Coverage: create_note() method - all lines"""
        result = self.note_mgr.create_note("Title", "Content")
        self.assertIn("created", result.lower())
        print("✓ Covered: create_note() method")
    
    def test_create_note_empty_title_statement(self):
        """Statement Coverage: create_note() - empty title check"""
        result = self.note_mgr.create_note("", "Content")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Covered: create_note() empty title check")
    
    def test_create_note_empty_content_statement(self):
        """Statement Coverage: create_note() - empty content check"""
        result = self.note_mgr.create_note("Title", "")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Covered: create_note() empty content check")
    
    def test_retrieve_note_statement_coverage(self):
        """Statement Coverage: retrieve_note() method - all lines"""
        self.note_mgr.create_note("Title", "Content")
        result = self.note_mgr.retrieve_note(1)
        self.assertIn("Title", result)
        print("✓ Covered: retrieve_note() method")
    
    def test_retrieve_note_not_found_statement(self):
        """Statement Coverage: retrieve_note() - not found branch"""
        result = self.note_mgr.retrieve_note(999)
        self.assertIn("not found", result.lower())
        print("✓ Covered: retrieve_note() not found")
    
    def test_list_all_notes_statement_coverage(self):
        """Statement Coverage: list_all_notes() method - all lines"""
        self.note_mgr.create_note("Note 1", "Content")
        result = self.note_mgr.list_all_notes()
        self.assertIn("Note 1", result)
        print("✓ Covered: list_all_notes() method")
    
    def test_list_all_notes_empty_statement(self):
        """Statement Coverage: list_all_notes() - empty list check"""
        result = self.note_mgr.list_all_notes()
        self.assertIn("no notes", result.lower())
        print("✓ Covered: list_all_notes() empty check")
    
    def test_delete_note_statement_coverage(self):
        """Statement Coverage: delete_note() method - all lines"""
        self.note_mgr.create_note("Note", "Content")
        result = self.note_mgr.delete_note(1)
        self.assertIn("deleted", result.lower())
        print("✓ Covered: delete_note() method")
    
    def test_delete_note_not_found_statement(self):
        """Statement Coverage: delete_note() - not found branch"""
        result = self.note_mgr.delete_note(999)
        self.assertIn("not found", result.lower())
        print("✓ Covered: delete_note() not found")
    
    def test_search_notes_statement_coverage(self):
        """Statement Coverage: search_notes() method - all lines"""
        self.note_mgr.create_note("Test Note", "Test content", tags=["test"])
        result = self.note_mgr.search_notes(keyword="Test")
        self.assertIn("Test Note", result)
        print("✓ Covered: search_notes() method")
    
    def test_search_notes_no_matches_statement(self):
        """Statement Coverage: search_notes() - no matches branch"""
        result = self.note_mgr.search_notes(keyword="nonexistent")
        self.assertIn("no notes found", result.lower())
        print("✓ Covered: search_notes() no matches")
    
    def test_update_note_statement_coverage(self):
        """Statement Coverage: update_note() method - all lines"""
        self.note_mgr.create_note("Title", "Content")
        result = self.note_mgr.update_note(1, title="New Title")
        self.assertIn("updated", result.lower())
        print("✓ Covered: update_note() method")
    
    def test_update_note_empty_title_statement(self):
        """Statement Coverage: update_note() - empty title check"""
        self.note_mgr.create_note("Title", "Content")
        result = self.note_mgr.update_note(1, title="")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Covered: update_note() empty title check")
    
    def test_save_notes_statement_coverage(self):
        """Statement Coverage: _save_notes() method"""
        self.note_mgr.create_note("Note", "Content")
        self.assertTrue(self.note_mgr._save_notes())
        print("✓ Covered: _save_notes() method")
    
    def test_load_notes_statement_coverage(self):
        """Statement Coverage: _load_notes() method"""
        self.note_mgr.create_note("Note", "Content")
        new_mgr = NoteManager(file_path=self.temp_file.name)
        self.assertTrue(new_mgr._load_notes())
        print("✓ Covered: _load_notes() method")


if __name__ == '__main__':
    unittest.main(verbosity=2)

