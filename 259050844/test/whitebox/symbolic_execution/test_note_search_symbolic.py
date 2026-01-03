"""
White-Box Testing: Symbolic Execution
Technique: Symbolic execution with path condition derivation
Function: Advanced Note Search (Keyword & Tag Based)
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


class TestNoteSearchSymbolicExecution(unittest.TestCase):
    """Symbolic Execution Derived Tests for Note Search"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.note_mgr = NoteManager(file_path=self.temp_file.name)
        # Setup test data
        self.note_mgr.create_note("Meeting Notes", "Discuss project", tags=["work"])
        self.note_mgr.create_note("Shopping List", "Buy groceries", tags=["personal"])
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    # Path 1: search_notes - keyword matches title
    def test_path1_search_keyword_title_match(self):
        """
        Path Condition: keyword != None AND keyword in note.title
        Symbolic Input: keyword = "Meeting"
        Concrete Input: "Meeting"
        Expected Output: Notes with "Meeting" in title
        """
        result = self.note_mgr.search_notes(keyword="Meeting")
        self.assertIn("Meeting Notes", result)
        print("✓ Path 1: Search keyword (title match) -> Results")
    
    # Path 2: search_notes - keyword matches content
    def test_path2_search_keyword_content_match(self):
        """
        Path Condition: keyword != None AND keyword in note.content AND keyword not in note.title
        Symbolic Input: keyword = "groceries"
        Concrete Input: "groceries"
        Expected Output: Notes with "groceries" in content
        """
        result = self.note_mgr.search_notes(keyword="groceries")
        self.assertIn("Shopping List", result)
        print("✓ Path 2: Search keyword (content match) -> Results")
    
    # Path 3: search_notes - keyword no match
    def test_path3_search_keyword_no_match(self):
        """
        Path Condition: keyword != None AND keyword not in note.title AND keyword not in note.content
        Symbolic Input: keyword = "nonexistent"
        Concrete Input: "nonexistent"
        Expected Output: "No notes found"
        """
        result = self.note_mgr.search_notes(keyword="nonexistent")
        self.assertIn("no notes found", result.lower())
        print("✓ Path 3: Search keyword (no match) -> No results")
    
    # Path 4: search_notes - tag matches
    def test_path4_search_tag_match(self):
        """
        Path Condition: tag != None AND tag in note.tags
        Symbolic Input: tag = "work"
        Concrete Input: "work"
        Expected Output: Notes with "work" tag
        """
        result = self.note_mgr.search_notes(tag="work")
        self.assertIn("Meeting Notes", result)
        print("✓ Path 4: Search tag (match) -> Results")
    
    # Path 5: search_notes - tag no match
    def test_path5_search_tag_no_match(self):
        """
        Path Condition: tag != None AND tag not in note.tags
        Symbolic Input: tag = "nonexistent"
        Concrete Input: "nonexistent"
        Expected Output: "No notes found"
        """
        result = self.note_mgr.search_notes(tag="nonexistent")
        self.assertIn("no notes found", result.lower())
        print("✓ Path 5: Search tag (no match) -> No results")
    
    # Path 6: search_notes - keyword and tag both match
    def test_path6_search_keyword_and_tag_match(self):
        """
        Path Condition: keyword != None AND keyword matches AND tag != None AND tag matches
        Symbolic Input: keyword = "project", tag = "work"
        Concrete Input: keyword="project", tag="work"
        Expected Output: Notes matching both
        """
        result = self.note_mgr.search_notes(keyword="project", tag="work")
        self.assertIn("Meeting Notes", result)
        print("✓ Path 6: Search keyword and tag (both match) -> Results")
    
    # Path 7: search_notes - keyword matches but tag doesn't
    def test_path7_search_keyword_match_tag_no_match(self):
        """
        Path Condition: keyword matches AND tag != None AND tag doesn't match
        Symbolic Input: keyword = "project", tag = "personal"
        Concrete Input: keyword="project", tag="personal"
        Expected Output: "No notes found"
        """
        result = self.note_mgr.search_notes(keyword="project", tag="personal")
        self.assertIn("no notes found", result.lower())
        print("✓ Path 7: Search keyword (match) tag (no match) -> No results")
    
    # Path 8: search_notes - no keyword, no tag
    def test_path8_search_no_params(self):
        """
        Path Condition: keyword == None AND tag == None
        Symbolic Input: keyword = None, tag = None
        Concrete Input: search_notes()
        Expected Output: "No notes found" or all notes
        """
        result = self.note_mgr.search_notes()
        self.assertIsInstance(result, str)
        print("✓ Path 8: Search no params -> Result")


if __name__ == '__main__':
    unittest.main(verbosity=2)

