"""
White-Box Testing: Statement Coverage
Technique: Ensure every line of code executes at least once
Function: handle(), _clean(), _lower() - Command Parsing Engine
Student: Saikiran (259053820)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import InfoSnippetAssistant


class TestCommandParsingStatementCoverage(unittest.TestCase):
    """
    White-Box Statement Coverage Tests
    
    Goal: Execute every statement in handle(), _clean(), and _lower() at least once
    This ensures all lines of code are covered.
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.assistant = InfoSnippetAssistant()
    
    def test_handle_empty_input_statement(self):
        """
        Statement Coverage: Line 33-34 - Empty input check
        Tests: if not raw: return "Type 'help'..."
        """
        result = self.assistant.handle("")
        self.assertIn("help", result.lower())
        print("✓ Covered: Empty input check (lines 33-34)")
    
    def test_handle_help_command_statement(self):
        """
        Statement Coverage: Line 36-45 - Help command branch
        Tests: if low in ("help", "h", "?"): return help menu
        """
        result = self.assistant.handle("help")
        self.assertIn("Commands:", result)
        print("✓ Covered: Help command branch (lines 36-45)")
    
    def test_handle_help_shortcut_h_statement(self):
        """
        Statement Coverage: Line 36 - Help shortcut 'h'
        Tests: 'h' in ("help", "h", "?")
        """
        result = self.assistant.handle("h")
        self.assertIn("Commands:", result)
        print("✓ Covered: Help shortcut 'h' (line 36)")
    
    def test_handle_help_shortcut_question_statement(self):
        """
        Statement Coverage: Line 36 - Help shortcut '?'
        Tests: '?' in ("help", "h", "?")
        """
        result = self.assistant.handle("?")
        self.assertIn("Commands:", result)
        print("✓ Covered: Help shortcut '?' (line 36)")
    
    def test_handle_topics_command_statement(self):
        """
        Statement Coverage: Line 47-48 - Topics command branch
        Tests: if low == "topics": return self._list_topics()
        """
        result = self.assistant.handle("topics")
        self.assertIn("Available topics:", result)
        print("✓ Covered: Topics command branch (lines 47-48)")
    
    def test_handle_info_command_statement(self):
        """
        Statement Coverage: Line 50-51 - Info command branch
        Tests: if low.startswith("info "): return self._get_info(raw[5:])
        """
        result = self.assistant.handle("info privacy")
        self.assertIn("privacy:", result)
        print("✓ Covered: Info command branch (lines 50-51)")
    
    def test_handle_unknown_command_statement(self):
        """
        Statement Coverage: Line 53-57 - Unknown command fallback
        Tests: return error message (default case)
        """
        result = self.assistant.handle("unknown")
        self.assertIn("not sure", result.lower())
        print("✓ Covered: Unknown command fallback (lines 53-57)")
    
    def test_clean_normal_text_statement(self):
        """
        Statement Coverage: Line 20-24 - _clean() method
        Tests: text.strip(), while loop for double spaces, return text
        """
        result = self.assistant._clean("  hello  world  ")
        self.assertEqual("hello world", result)
        print("✓ Covered: _clean() method (lines 20-24)")
    
    def test_clean_double_spaces_statement(self):
        """
        Statement Coverage: Line 22-23 - Double space replacement loop
        Tests: while "  " in text: text.replace("  ", " ")
        """
        result = self.assistant._clean("hello    world")
        self.assertEqual("hello world", result)
        print("✓ Covered: Double space replacement (lines 22-23)")
    
    def test_clean_none_input_statement(self):
        """
        Statement Coverage: Line 21 - None input handling
        Tests: text = (text or "").strip()
        """
        result = self.assistant._clean(None)
        self.assertEqual("", result)
        print("✓ Covered: _clean() with None input (line 21)")
    
    def test_lower_normal_text_statement(self):
        """
        Statement Coverage: Line 26-27 - _lower() method
        Tests: (text or "").strip().lower()
        """
        result = self.assistant._lower("  HELLO  ")
        self.assertEqual("hello", result)
        print("✓ Covered: _lower() method (lines 26-27)")
    
    def test_lower_none_input_statement(self):
        """
        Statement Coverage: Line 27 - None input handling in _lower()
        Tests: (text or "").strip().lower()
        """
        result = self.assistant._lower(None)
        self.assertEqual("", result)
        print("✓ Covered: _lower() with None input (line 27)")
    
    def test_list_topics_statement(self):
        """
        Statement Coverage: Line 59-65 - _list_topics() method
        Tests: keys = list(self._snippets.keys()), keys.sort(), loop, lines.append()
        """
        result = self.assistant._list_topics()
        self.assertIn("Available topics:", result)
        self.assertIn("about", result)
        print("✓ Covered: _list_topics() method (lines 59-65)")
    
    def test_get_info_valid_topic_statement(self):
        """
        Statement Coverage: Line 67-73 - _get_info() valid topic branch
        Tests: topic = self._lower(topic_text), if not topic, if topic in self._snippets
        """
        result = self.assistant._get_info("privacy")
        self.assertIn("privacy:", result)
        print("✓ Covered: _get_info() valid topic (lines 67-73)")
    
    def test_get_info_empty_topic_statement(self):
        """
        Statement Coverage: Line 69-70 - _get_info() empty topic branch
        Tests: if not topic: return "Usage: info <topic>"
        """
        result = self.assistant._get_info("")
        self.assertIn("Usage", result)
        print("✓ Covered: _get_info() empty topic (lines 69-70)")
    
    def test_get_info_suggestions_statement(self):
        """
        Statement Coverage: Line 75-84 - _get_info() suggestions branch
        Tests: suggestions loop, if suggestions: return suggestions
        """
        result = self.assistant._get_info("priv")  # Partial match
        self.assertIn("Did you mean", result)
        print("✓ Covered: _get_info() suggestions (lines 75-84)")
    
    def test_get_info_no_match_statement(self):
        """
        Statement Coverage: Line 86-89 - _get_info() no match branch
        Tests: return "No information found..."
        """
        result = self.assistant._get_info("nonexistent123")
        self.assertIn("No information found", result)
        print("✓ Covered: _get_info() no match (lines 86-89)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

