"""
White-Box Testing: Concolic Testing
Technique: Concrete execution + Symbolic constraint collection + Constraint flipping
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


class TestNoteSearchConcolicTesting(unittest.TestCase):
    """Concolic Testing - Iterative Constraint Flipping for Note Search"""
    
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
    
    def test_concolic_iteration1_keyword_match(self):
        """
        Concolic Iteration 1: Initial Concrete Input
        Initial Input: keyword="Meeting"
        Execution Path: keyword != None (True), keyword in title (True)
        Constraints Collected: [keyword != None, keyword in note.title]
        Result: Matches found
        """
        input_val = "Meeting"
        result = self.note_mgr.search_notes(keyword=input_val)
        self.assertIn("Meeting Notes", result)
        print(f"✓ Iteration 1: Input='{input_val}', Constraints=[keyword != None, keyword in title], Result=Matches")
    
    def test_concolic_iteration2_flip_keyword_match_constraint(self):
        """
        Concolic Iteration 2: Flip Keyword Match Constraint
        Previous Constraints: [keyword != None, keyword in title]
        Flipped Constraint: keyword not in title AND keyword not in content
        New Input: "nonexistent" (satisfies: keyword != None, no match)
        Execution Path: keyword != None (True), keyword in title (False), keyword in content (False)
        Constraints Collected: [keyword != None, keyword not in title, keyword not in content]
        Result: No matches
        """
        input_val = "nonexistent"
        result = self.note_mgr.search_notes(keyword=input_val)
        self.assertIn("no notes found", result.lower())
        print(f"✓ Iteration 2: Input='{input_val}', Flipped: keyword match constraint, Result=No matches")
    
    def test_concolic_iteration3_keyword_content_match(self):
        """
        Concolic Iteration 3: Keyword Matches Content
        Previous Constraints: [keyword not in title, keyword not in content]
        Flipped Constraint: keyword in content
        New Input: "groceries" (satisfies: keyword != None, keyword in content)
        Execution Path: keyword != None (True), keyword in title (False), keyword in content (True)
        Constraints Collected: [keyword != None, keyword not in title, keyword in content]
        Result: Matches found
        """
        input_val = "groceries"
        result = self.note_mgr.search_notes(keyword=input_val)
        self.assertIn("Shopping List", result)
        print(f"✓ Iteration 3: Input='{input_val}', Flipped: content match constraint, Result=Matches")
    
    def test_concolic_iteration4_tag_search(self):
        """
        Concolic Iteration 4: Tag Search
        Previous Constraints: [keyword != None]
        Flipped Constraint: keyword == None AND tag != None
        New Input: tag="work" (satisfies: keyword == None, tag != None, tag in note.tags)
        Execution Path: keyword == None (True), tag != None (True), tag in note.tags (True)
        Constraints Collected: [keyword == None, tag != None, tag in note.tags]
        Result: Matches found
        """
        input_val = "work"
        result = self.note_mgr.search_notes(tag=input_val)
        self.assertIn("Meeting Notes", result)
        print(f"✓ Iteration 4: Input=tag='{input_val}', Flipped: tag constraint, Result=Matches")
    
    def test_concolic_iteration5_tag_no_match(self):
        """
        Concolic Iteration 5: Tag No Match
        Previous Constraints: [tag != None, tag in note.tags]
        Flipped Constraint: tag not in note.tags
        New Input: tag="nonexistent" (satisfies: tag != None, tag not in note.tags)
        Execution Path: tag != None (True), tag in note.tags (False)
        Constraints Collected: [tag != None, tag not in note.tags]
        Result: No matches
        """
        input_val = "nonexistent"
        result = self.note_mgr.search_notes(tag=input_val)
        self.assertIn("no notes found", result.lower())
        print(f"✓ Iteration 5: Input=tag='{input_val}', Flipped: tag match constraint, Result=No matches")
    
    def test_concolic_iteration6_keyword_and_tag_both_match(self):
        """
        Concolic Iteration 6: Keyword and Tag Both Match
        Previous Constraints: [keyword == None OR tag == None]
        Flipped Constraint: keyword != None AND tag != None AND both match
        New Input: keyword="project", tag="work" (satisfies: both != None, both match)
        Execution Path: keyword != None (True), keyword matches (True), tag != None (True), tag matches (True)
        Constraints Collected: [keyword != None, keyword matches, tag != None, tag matches]
        Result: Matches found
        """
        result = self.note_mgr.search_notes(keyword="project", tag="work")
        self.assertIn("Meeting Notes", result)
        print("✓ Iteration 6: Input=keyword='project', tag='work', Flipped: both params constraint, Result=Matches")
    
    def test_concolic_iteration7_keyword_match_tag_no_match(self):
        """
        Concolic Iteration 7: Keyword Matches but Tag Doesn't
        Previous Constraints: [keyword matches, tag matches]
        Flipped Constraint: keyword matches AND tag doesn't match
        New Input: keyword="project", tag="personal" (satisfies: keyword matches, tag doesn't match)
        Execution Path: keyword matches (True), tag doesn't match (True)
        Constraints Collected: [keyword matches, tag doesn't match]
        Result: No matches
        """
        result = self.note_mgr.search_notes(keyword="project", tag="personal")
        self.assertIn("no notes found", result.lower())
        print("✓ Iteration 7: Input=keyword='project', tag='personal', Flipped: tag match constraint, Result=No matches")


if __name__ == '__main__':
    unittest.main(verbosity=2)

