"""
White-Box Testing: Branch Coverage
Technique: Ensure every decision (True/False) is tested
Function: handle(), _clean(), _lower(), _get_info() - Command Parsing Engine
Student: Saikiran (259053820)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import InfoSnippetAssistant


class TestCommandParsingBranchCoverage(unittest.TestCase):
    """
    White-Box Branch Coverage Tests
    
    Goal: Test both True and False outcomes of every decision point
    This ensures all branches are covered.
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.assistant = InfoSnippetAssistant()
    
    # Branch: if not raw (line 33)
    def test_branch_empty_input_true(self):
        """
        Branch Coverage: if not raw: (TRUE branch)
        Decision: Empty input -> True
        """
        result = self.assistant.handle("")
        self.assertIn("help", result.lower())
        print("✓ Branch: if not raw (TRUE)")
    
    def test_branch_empty_input_false(self):
        """
        Branch Coverage: if not raw: (FALSE branch)
        Decision: Non-empty input -> False
        """
        result = self.assistant.handle("help")
        self.assertIn("Commands:", result)
        print("✓ Branch: if not raw (FALSE)")
    
    # Branch: if low in ("help", "h", "?") (line 36)
    def test_branch_help_command_true(self):
        """
        Branch Coverage: if low in ("help", "h", "?"): (TRUE branch)
        Decision: Help command -> True
        """
        result = self.assistant.handle("help")
        self.assertIn("Commands:", result)
        print("✓ Branch: if help command (TRUE)")
    
    def test_branch_help_command_false(self):
        """
        Branch Coverage: if low in ("help", "h", "?"): (FALSE branch)
        Decision: Non-help command -> False
        """
        result = self.assistant.handle("topics")
        self.assertNotIn("Commands:\n- info", result)  # Not help menu
        print("✓ Branch: if help command (FALSE)")
    
    # Branch: if low == "topics" (line 47)
    def test_branch_topics_command_true(self):
        """
        Branch Coverage: if low == "topics": (TRUE branch)
        Decision: Topics command -> True
        """
        result = self.assistant.handle("topics")
        self.assertIn("Available topics:", result)
        print("✓ Branch: if topics command (TRUE)")
    
    def test_branch_topics_command_false(self):
        """
        Branch Coverage: if low == "topics": (FALSE branch)
        Decision: Non-topics command -> False
        """
        result = self.assistant.handle("help")
        self.assertNotIn("Available topics:", result)
        print("✓ Branch: if topics command (FALSE)")
    
    # Branch: if low.startswith("info ") (line 50)
    def test_branch_info_command_true(self):
        """
        Branch Coverage: if low.startswith("info "): (TRUE branch)
        Decision: Info command -> True
        """
        result = self.assistant.handle("info privacy")
        self.assertIn("privacy:", result)
        print("✓ Branch: if info command (TRUE)")
    
    def test_branch_info_command_false(self):
        """
        Branch Coverage: if low.startswith("info "): (FALSE branch)
        Decision: Non-info command -> False
        """
        result = self.assistant.handle("topics")
        self.assertNotIn("Usage: info", result)
        print("✓ Branch: if info command (FALSE)")
    
    # Branch: while "  " in text (line 22) in _clean()
    def test_branch_double_spaces_true(self):
        """
        Branch Coverage: while "  " in text: (TRUE branch - loop entry)
        Decision: Double spaces exist -> True (loop executes)
        """
        result = self.assistant._clean("hello    world")
        self.assertEqual("hello world", result)
        print("✓ Branch: while double spaces (TRUE - loop)")
    
    def test_branch_double_spaces_false(self):
        """
        Branch Coverage: while "  " in text: (FALSE branch - loop exit)
        Decision: No double spaces -> False (loop doesn't execute)
        """
        result = self.assistant._clean("hello world")
        self.assertEqual("hello world", result)
        print("✓ Branch: while double spaces (FALSE - no loop)")
    
    # Branch: if not topic (line 69) in _get_info()
    def test_branch_get_info_empty_topic_true(self):
        """
        Branch Coverage: if not topic: (TRUE branch)
        Decision: Empty topic -> True
        """
        result = self.assistant._get_info("")
        self.assertIn("Usage", result)
        print("✓ Branch: if not topic (TRUE)")
    
    def test_branch_get_info_empty_topic_false(self):
        """
        Branch Coverage: if not topic: (FALSE branch)
        Decision: Non-empty topic -> False
        """
        result = self.assistant._get_info("privacy")
        self.assertNotIn("Usage: info", result)
        print("✓ Branch: if not topic (FALSE)")
    
    # Branch: if topic in self._snippets (line 72)
    def test_branch_topic_in_snippets_true(self):
        """
        Branch Coverage: if topic in self._snippets: (TRUE branch)
        Decision: Valid topic -> True
        """
        result = self.assistant._get_info("privacy")
        self.assertIn("privacy:", result)
        print("✓ Branch: if topic in snippets (TRUE)")
    
    def test_branch_topic_in_snippets_false(self):
        """
        Branch Coverage: if topic in self._snippets: (FALSE branch)
        Decision: Invalid topic -> False
        """
        result = self.assistant._get_info("nonexistent")
        self.assertNotIn("nonexistent:", result)
        print("✓ Branch: if topic in snippets (FALSE)")
    
    # Branch: if suggestions (line 80) in _get_info()
    def test_branch_suggestions_true(self):
        """
        Branch Coverage: if suggestions: (TRUE branch)
        Decision: Suggestions found -> True
        """
        result = self.assistant._get_info("priv")  # Partial match
        self.assertIn("Did you mean", result)
        print("✓ Branch: if suggestions (TRUE)")
    
    def test_branch_suggestions_false(self):
        """
        Branch Coverage: if suggestions: (FALSE branch)
        Decision: No suggestions -> False
        """
        result = self.assistant._get_info("xyz123nonexistent")
        self.assertIn("No information found", result)
        print("✓ Branch: if suggestions (FALSE)")
    
    # Branch: for k in self._snippets (line 76) - loop entry/exit
    def test_branch_suggestions_loop_entry(self):
        """
        Branch Coverage: for k in self._snippets: (Loop entry)
        Decision: Loop executes when snippets exist
        """
        result = self.assistant._get_info("priv")
        # Loop should execute and find suggestions
        self.assertIn("Did you mean", result)
        print("✓ Branch: suggestions loop (ENTRY)")
    
    def test_branch_suggestions_loop_exit(self):
        """
        Branch Coverage: for k in self._snippets: (Loop exit)
        Decision: Loop completes after checking all snippets
        """
        result = self.assistant._get_info("nonexistent")
        # Loop should execute but find no matches
        self.assertIn("No information found", result)
        print("✓ Branch: suggestions loop (EXIT)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

