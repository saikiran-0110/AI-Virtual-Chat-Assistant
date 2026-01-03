"""
White-Box Testing: Symbolic Execution
Technique: Symbolic execution with path condition derivation
Function: handle() - Command Parsing Engine
Student: Saikiran (259053820)

This test file implements test cases derived from symbolic execution analysis.
See symbolic_execution_report.md for the symbolic execution tree and path conditions.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import InfoSnippetAssistant


class TestCommandParsingSymbolicExecution(unittest.TestCase):
    """
    Symbolic Execution Derived Tests
    
    These tests are derived from symbolic execution analysis where:
    - Input is represented as symbol 'x'
    - Path conditions are identified for each execution path
    - Concrete test inputs are selected to satisfy each path condition
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.assistant = InfoSnippetAssistant()
    
    # Path 1: x is empty -> return help message
    def test_path1_empty_input(self):
        """
        Path Condition: x == "" OR x.strip() == ""
        Symbolic Input: x = ""
        Concrete Input: ""
        Expected Output: "Type 'help' to see available commands."
        """
        result = self.assistant.handle("")
        self.assertIn("help", result.lower())
        print("✓ Path 1: Empty input -> Help message")
    
    # Path 2: x.lower() in ("help", "h", "?") -> return help menu
    def test_path2_help_command(self):
        """
        Path Condition: x.lower() in ("help", "h", "?")
        Symbolic Input: x = "help" OR "h" OR "?"
        Concrete Input: "help"
        Expected Output: Help menu text
        """
        result = self.assistant.handle("help")
        self.assertIn("Commands:", result)
        print("✓ Path 2: Help command -> Help menu")
    
    def test_path2_help_shortcut_h(self):
        """
        Path Condition: x.lower() == "h"
        Symbolic Input: x = "h"
        Concrete Input: "h"
        Expected Output: Help menu text
        """
        result = self.assistant.handle("h")
        self.assertIn("Commands:", result)
        print("✓ Path 2b: Help shortcut 'h' -> Help menu")
    
    def test_path2_help_shortcut_question(self):
        """
        Path Condition: x.lower() == "?"
        Symbolic Input: x = "?"
        Concrete Input: "?"
        Expected Output: Help menu text
        """
        result = self.assistant.handle("?")
        self.assertIn("Commands:", result)
        print("✓ Path 2c: Help shortcut '?' -> Help menu")
    
    # Path 3: x.lower() == "topics" -> return topics list
    def test_path3_topics_command(self):
        """
        Path Condition: x.lower() == "topics" AND x.lower() not in ("help", "h", "?")
        Symbolic Input: x = "topics"
        Concrete Input: "topics"
        Expected Output: Topics list
        """
        result = self.assistant.handle("topics")
        self.assertIn("Available topics:", result)
        print("✓ Path 3: Topics command -> Topics list")
    
    # Path 4: x.lower().startswith("info ") -> return info result
    def test_path4_info_command_valid(self):
        """
        Path Condition: x.lower().startswith("info ") AND x[5:].strip() != "" 
                        AND x[5:].strip().lower() in snippets
        Symbolic Input: x = "info " + y, where y in snippets
        Concrete Input: "info privacy"
        Expected Output: Topic information
        """
        result = self.assistant.handle("info privacy")
        self.assertIn("privacy:", result)
        print("✓ Path 4: Info command (valid topic) -> Topic info")
    
    def test_path4_info_command_empty_topic(self):
        """
        Path Condition: x.lower().startswith("info ") AND x[5:].strip() == ""
        Note: After _clean(), "info " becomes "info" which doesn't startswith("info "), so goes to error path
        Symbolic Input: x = "info " OR "info   "
        Concrete Input: "info "
        Expected Output: Error message (because cleaning removes trailing space)
        """
        result = self.assistant.handle("info ")
        # After _clean(), "info " becomes "info", which doesn't match "info " pattern
        self.assertIn("not sure", result.lower())
        print("✓ Path 4b: Info command (empty topic) -> Error message (after cleaning)")
    
    def test_path4_info_command_invalid_topic(self):
        """
        Path Condition: x.lower().startswith("info ") AND x[5:].strip() != ""
                        AND x[5:].strip().lower() not in snippets
                        AND (no suggestions found)
        Symbolic Input: x = "info " + y, where y not in snippets and no partial match
        Concrete Input: "info nonexistent123"
        Expected Output: "No information found..."
        """
        result = self.assistant.handle("info nonexistent123")
        self.assertIn("No information found", result)
        print("✓ Path 4c: Info command (invalid topic, no suggestions) -> No info message")
    
    def test_path4_info_command_with_suggestions(self):
        """
        Path Condition: x.lower().startswith("info ") AND x[5:].strip() != ""
                        AND x[5:].strip().lower() not in snippets
                        AND (suggestions found)
        Symbolic Input: x = "info " + y, where y partially matches snippet
        Concrete Input: "info priv"
        Expected Output: Suggestions message
        """
        result = self.assistant.handle("info priv")
        self.assertIn("Did you mean", result)
        print("✓ Path 4d: Info command (invalid topic, with suggestions) -> Suggestions")
    
    # Path 5: Default case -> return error message
    def test_path5_unknown_command(self):
        """
        Path Condition: x != "" AND x.lower() not in ("help", "h", "?")
                        AND x.lower() != "topics" AND not x.lower().startswith("info ")
        Symbolic Input: x = any string not matching above conditions
        Concrete Input: "unknowncommand"
        Expected Output: Error message with help suggestion
        """
        result = self.assistant.handle("unknowncommand")
        self.assertIn("not sure", result.lower())
        self.assertIn("help", result.lower())
        print("✓ Path 5: Unknown command -> Error message")
    
    # Path 6: Testing _clean() with symbolic input
    def test_path6_clean_normal_text(self):
        """
        Path Condition: text != None AND text.strip() != "" AND "  " not in text
        Symbolic Input: x = normal text without double spaces
        Concrete Input: "hello world"
        Expected Output: "hello world"
        """
        result = self.assistant._clean("hello world")
        self.assertEqual("hello world", result)
        print("✓ Path 6: _clean() normal text -> Cleaned text")
    
    def test_path6_clean_with_double_spaces(self):
        """
        Path Condition: text != None AND "  " in text (loop condition)
        Symbolic Input: x = text with double spaces
        Concrete Input: "hello    world"
        Expected Output: "hello world" (spaces normalized)
        """
        result = self.assistant._clean("hello    world")
        self.assertEqual("hello world", result)
        print("✓ Path 6b: _clean() with double spaces -> Normalized text")
    
    def test_path6_clean_none_input(self):
        """
        Path Condition: text == None OR text.strip() == ""
        Symbolic Input: x = None
        Concrete Input: None
        Expected Output: ""
        """
        result = self.assistant._clean(None)
        self.assertEqual("", result)
        print("✓ Path 6c: _clean() None input -> Empty string")


if __name__ == '__main__':
    unittest.main(verbosity=2)

