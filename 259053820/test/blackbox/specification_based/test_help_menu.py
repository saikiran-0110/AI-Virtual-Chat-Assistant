"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning
Function: handle() - Help Menu Generator
Student: Saikiran (259053820)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import InfoSnippetAssistant


class TestHelpMenuSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Help Menu Generator
    
    Test Categories:
    1. Help command variations (help, h, ?)
    2. Help menu content verification
    3. Case sensitivity
    4. Whitespace handling
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.assistant = InfoSnippetAssistant()
    
    def test_help_command_returns_menu(self):
        """
        Test Case: Help command returns help menu
        Input: "help"
        Expected Output: Help menu with commands list
        Technique: Valid input partition
        """
        result = self.assistant.handle("help")
        # Function name: handle
        # Input: "help"
        # Expected: Contains "Commands:", "info <topic>", "topics", "Examples:"
        # Actual: result
        self.assertIn("Commands:", result, "Help menu should contain 'Commands:'")
        self.assertIn("info <topic>", result, "Help menu should contain 'info <topic>'")
        self.assertIn("topics", result, "Help menu should contain 'topics'")
        self.assertIn("Examples:", result, "Help menu should contain 'Examples:'")
        print(f"✓ PASS: Help menu - Input: 'help', Expected: Help menu, Actual: {result[:80]}...")
    
    def test_help_shortcut_h(self):
        """
        Test Case: Help shortcut 'h' returns menu
        Input: "h"
        Expected Output: Same help menu as "help"
        Technique: Valid input partition (alternative)
        """
        result_h = self.assistant.handle("h")
        result_help = self.assistant.handle("help")
        self.assertEqual(result_h, result_help, "Shortcut 'h' should return same as 'help'")
        print(f"✓ PASS: Help shortcut (h) - Input: 'h', Expected: Help menu, Actual: {result_h[:80]}...")
    
    def test_help_shortcut_question_mark(self):
        """
        Test Case: Help shortcut '?' returns menu
        Input: "?"
        Expected Output: Same help menu as "help"
        Technique: Valid input partition (alternative)
        """
        result_q = self.assistant.handle("?")
        result_help = self.assistant.handle("help")
        self.assertEqual(result_q, result_help, "Shortcut '?' should return same as 'help'")
        print(f"✓ PASS: Help shortcut (?) - Input: '?', Expected: Help menu, Actual: {result_q[:80]}...")
    
    def test_help_menu_contains_examples(self):
        """
        Test Case: Help menu contains example commands
        Input: "help"
        Expected Output: Help menu with examples section
        Technique: Content verification
        """
        result = self.assistant.handle("help")
        self.assertIn("Examples:", result)
        self.assertIn("info privacy", result)
        self.assertIn("info reminders", result)
        self.assertIn("topics", result)
        print(f"✓ PASS: Help menu examples - Input: 'help', Expected: Examples section, Actual: Contains examples")
    
    def test_help_case_insensitive(self):
        """
        Test Case: Help command is case insensitive
        Input: "HELP", "Help", "hElP"
        Expected Output: Same help menu for all
        Technique: Case variation partition
        """
        result_upper = self.assistant.handle("HELP")
        result_mixed = self.assistant.handle("Help")
        result_lower = self.assistant.handle("help")
        
        self.assertEqual(result_upper, result_lower, "Uppercase should work")
        self.assertEqual(result_mixed, result_lower, "Mixed case should work")
        print(f"✓ PASS: Help case insensitive - Input: 'HELP', Expected: Help menu, Actual: Help menu")
    
    def test_help_with_whitespace(self):
        """
        Test Case: Help command with whitespace
        Input: "  help  "
        Expected Output: Help menu (whitespace should be cleaned)
        Technique: Whitespace handling
        """
        result = self.assistant.handle("  help  ")
        self.assertIn("Commands:", result)
        print(f"✓ PASS: Help with whitespace - Input: '  help  ', Expected: Help menu, Actual: Help menu")


if __name__ == '__main__':
    unittest.main(verbosity=2)

