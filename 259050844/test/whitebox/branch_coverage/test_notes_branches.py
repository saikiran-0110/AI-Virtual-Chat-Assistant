"""
White-Box Testing: Branch Coverage
Technique: Ensure every decision (True/False) is tested
Functions: Note Creation, Retrieval, Deletion, Search, Update
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


class TestNotesBranchCoverage(unittest.TestCase):
    """White-Box Branch Coverage Tests for Notes System"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.note_mgr = NoteManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    # Branch: if not title.strip() in create_note
    def test_branch_create_note_empty_title_true(self):
        """Branch Coverage: if not title.strip() (TRUE branch)"""
        result = self.note_mgr.create_note("", "Content")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Branch: create_note empty title (TRUE)")
    
    def test_branch_create_note_empty_title_false(self):
        """Branch Coverage: if not title.strip() (FALSE branch)"""
        result = self.note_mgr.create_note("Title", "Content")
        self.assertIn("created", result.lower())
        print("✓ Branch: create_note empty title (FALSE)")
    
    # Branch: if not content.strip() in create_note
    def test_branch_create_note_empty_content_true(self):
        """Branch Coverage: if not content.strip() (TRUE branch)"""
        result = self.note_mgr.create_note("Title", "")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Branch: create_note empty content (TRUE)")
    
    def test_branch_create_note_empty_content_false(self):
        """Branch Coverage: if not content.strip() (FALSE branch)"""
        result = self.note_mgr.create_note("Title", "Content")
        self.assertIn("created", result.lower())
        print("✓ Branch: create_note empty content (FALSE)")
    
    # Branch: if not self._notes in list_all_notes
    def test_branch_list_notes_empty_true(self):
        """Branch Coverage: if not self._notes (TRUE branch)"""
        result = self.note_mgr.list_all_notes()
        self.assertIn("no notes", result.lower())
        print("✓ Branch: list_all_notes empty (TRUE)")
    
    def test_branch_list_notes_empty_false(self):
        """Branch Coverage: if not self._notes (FALSE branch)"""
        self.note_mgr.create_note("Note", "Content")
        result = self.note_mgr.list_all_notes()
        self.assertIn("Note", result)
        print("✓ Branch: list_all_notes empty (FALSE)")
    
    # Branch: Loop in retrieve_note - found/not found
    def test_branch_retrieve_note_found_true(self):
        """Branch Coverage: note found in loop (TRUE branch)"""
        self.note_mgr.create_note("Note", "Content")
        result = self.note_mgr.retrieve_note(1)
        self.assertIn("Note", result)
        print("✓ Branch: retrieve_note found (TRUE)")
    
    def test_branch_retrieve_note_found_false(self):
        """Branch Coverage: note not found in loop (FALSE branch)"""
        result = self.note_mgr.retrieve_note(999)
        self.assertIn("not found", result.lower())
        print("✓ Branch: retrieve_note found (FALSE)")
    
    # Branch: Loop in delete_note - found/not found
    def test_branch_delete_note_found_true(self):
        """Branch Coverage: note found in delete loop (TRUE branch)"""
        self.note_mgr.create_note("Note", "Content")
        result = self.note_mgr.delete_note(1)
        self.assertIn("deleted", result.lower())
        print("✓ Branch: delete_note found (TRUE)")
    
    def test_branch_delete_note_found_false(self):
        """Branch Coverage: note not found in delete loop (FALSE branch)"""
        result = self.note_mgr.delete_note(999)
        self.assertIn("not found", result.lower())
        print("✓ Branch: delete_note found (FALSE)")
    
    # Branch: if not matches in search_notes
    def test_branch_search_notes_no_matches_true(self):
        """Branch Coverage: if not matches (TRUE branch)"""
        result = self.note_mgr.search_notes(keyword="nonexistent")
        self.assertIn("no notes found", result.lower())
        print("✓ Branch: search_notes no matches (TRUE)")
    
    def test_branch_search_notes_no_matches_false(self):
        """Branch Coverage: if not matches (FALSE branch)"""
        self.note_mgr.create_note("Test Note", "Test content")
        result = self.note_mgr.search_notes(keyword="Test")
        self.assertIn("Test Note", result)
        print("✓ Branch: search_notes no matches (FALSE)")
    
    # Branch: if keyword in search_notes
    def test_branch_search_keyword_check_true(self):
        """Branch Coverage: keyword check in search (TRUE branch)"""
        self.note_mgr.create_note("Test Note", "Test content")
        result = self.note_mgr.search_notes(keyword="Test")
        self.assertIn("Test Note", result)
        print("✓ Branch: search keyword check (TRUE)")
    
    def test_branch_search_keyword_check_false(self):
        """Branch Coverage: keyword check in search (FALSE branch)"""
        self.note_mgr.create_note("Note", "Content")
        result = self.note_mgr.search_notes(keyword="nonexistent")
        self.assertIn("no notes found", result.lower())
        print("✓ Branch: search keyword check (FALSE)")
    
    # Branch: if tag in search_notes
    def test_branch_search_tag_check_true(self):
        """Branch Coverage: tag check in search (TRUE branch)"""
        self.note_mgr.create_note("Note", "Content", tags=["work"])
        result = self.note_mgr.search_notes(tag="work")
        self.assertIn("Note", result)
        print("✓ Branch: search tag check (TRUE)")
    
    def test_branch_search_tag_check_false(self):
        """Branch Coverage: tag check in search (FALSE branch)"""
        self.note_mgr.create_note("Note", "Content", tags=["work"])
        result = self.note_mgr.search_notes(tag="personal")
        self.assertIn("no notes found", result.lower())
        print("✓ Branch: search tag check (FALSE)")
    
    # Branch: if not title.strip() in update_note
    def test_branch_update_note_empty_title_true(self):
        """Branch Coverage: if not title.strip() in update (TRUE branch)"""
        self.note_mgr.create_note("Title", "Content")
        result = self.note_mgr.update_note(1, title="")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Branch: update_note empty title (TRUE)")
    
    def test_branch_update_note_empty_title_false(self):
        """Branch Coverage: if not title.strip() in update (FALSE branch)"""
        self.note_mgr.create_note("Title", "Content")
        result = self.note_mgr.update_note(1, title="New Title")
        self.assertIn("updated", result.lower())
        print("✓ Branch: update_note empty title (FALSE)")
    
    # Branch: Loop in update_note - found/not found
    def test_branch_update_note_found_true(self):
        """Branch Coverage: note found in update loop (TRUE branch)"""
        self.note_mgr.create_note("Title", "Content")
        result = self.note_mgr.update_note(1, title="New")
        self.assertIn("updated", result.lower())
        print("✓ Branch: update_note found (TRUE)")
    
    def test_branch_update_note_found_false(self):
        """Branch Coverage: note not found in update loop (FALSE branch)"""
        result = self.note_mgr.update_note(999, title="New")
        self.assertIn("not found", result.lower())
        print("✓ Branch: update_note found (FALSE)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

