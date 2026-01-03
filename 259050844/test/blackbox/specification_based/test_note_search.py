"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
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


class TestNoteSearchSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Note Search
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.note_mgr = NoteManager(file_path=self.temp_file.name)
        # Setup test data
        self.note_mgr.create_note("Meeting Notes", "Discuss project timeline", tags=["work", "meeting"])
        self.note_mgr.create_note("Shopping List", "Buy groceries", tags=["personal"])
        self.note_mgr.create_note("Project Ideas", "New features to implement", tags=["work", "ideas"])
    
    def tearDown(self):
        """Clean up"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_search_by_keyword_title_match(self):
        """
        Test Case: Search by keyword matching title
        Input: keyword="Meeting"
        Expected Output: Notes with "Meeting" in title
        Technique: Valid input partition - keyword in title
        """
        result = self.note_mgr.search_notes(keyword="Meeting")
        self.assertIn("Meeting Notes", result)
        print(f"✓ PASS: Search by keyword (title match) - Input: keyword='Meeting', Output: {result[:50]}...")
    
    def test_search_by_keyword_content_match(self):
        """
        Test Case: Search by keyword matching content
        Input: keyword="groceries"
        Expected Output: Notes with "groceries" in content
        Technique: Valid input partition - keyword in content
        """
        result = self.note_mgr.search_notes(keyword="groceries")
        self.assertIn("Shopping List", result)
        print(f"✓ PASS: Search by keyword (content match) - Input: keyword='groceries', Output: {result[:50]}...")
    
    def test_search_by_tag(self):
        """
        Test Case: Search by tag
        Input: tag="work"
        Expected Output: Notes with "work" tag
        Technique: Valid input partition - tag search
        """
        result = self.note_mgr.search_notes(tag="work")
        self.assertIn("Meeting Notes", result)
        self.assertIn("Project Ideas", result)
        print(f"✓ PASS: Search by tag - Input: tag='work', Output: {result[:50]}...")
    
    def test_search_no_matches(self):
        """
        Test Case: Search with no matches
        Input: keyword="nonexistent"
        Expected Output: "No notes found"
        Technique: Invalid input partition
        """
        result = self.note_mgr.search_notes(keyword="nonexistent")
        self.assertIn("no notes found", result.lower())
        print(f"✓ PASS: Search (no matches) - Input: keyword='nonexistent', Output: {result}")
    
    def test_search_empty_keyword(self):
        """
        Test Case: Search with empty keyword
        Input: keyword=""
        Expected Output: Usage message or all notes
        Technique: Boundary value - empty input
        """
        result = self.note_mgr.search_notes(keyword="")
        # Could return usage message or all notes
        self.assertIsInstance(result, str)
        print(f"✓ PASS: Search (empty keyword) - Input: keyword='', Output: {result[:50]}...")
    
    def test_search_keyword_and_tag(self):
        """
        Test Case: Search by both keyword and tag
        Input: keyword="project", tag="work"
        Expected Output: Notes matching both criteria
        Technique: Valid input partition - combined search
        """
        result = self.note_mgr.search_notes(keyword="project", tag="work")
        self.assertIn("Meeting Notes", result)
        print(f"✓ PASS: Search (keyword + tag) - Input: keyword='project', tag='work', Output: {result[:50]}...")


if __name__ == '__main__':
    unittest.main(verbosity=2)

