"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
Function: handle() - Command Parsing Engine
Student: Saikiran (259053820)
"""

import unittest
import sys
import os

# Add parent directory to path to import main module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import InfoSnippetAssistant


class TestCommandParsingSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Command Parsing Engine
    
    Test Categories:
    1. Valid commands (help, topics, info)
    2. Invalid/unknown commands
    3. Empty input
    4. Whitespace-only input
    5. Case variations
    6. Command with extra spaces
    """
    
    def setUp(self):
        """Set up test fixture - create InfoSnippetAssistant instance"""
        self.assistant = InfoSnippetAssistant()
    
    def test_help_command_exact(self):
        """
        Test Case: Help command - exact match
        Input: "help"
        Expected Output: Help menu text
        Technique: Valid input partition
        """
        result = self.assistant.handle("help")
        self.assertIn("Commands:", result)
        self.assertIn("info <topic>", result)
        self.assertIn("topics", result)
        print(f"✓ PASS: help command - Input: 'help', Output: {result[:50]}...")
    
    def test_help_command_shortcut_h(self):
        """
        Test Case: Help command - shortcut 'h'
        Input: "h"
        Expected Output: Help menu text
        Technique: Valid input partition (alternative form)
        """
        result = self.assistant.handle("h")
        self.assertIn("Commands:", result)
        print(f"✓ PASS: help command (h) - Input: 'h', Output: {result[:50]}...")
    
    def test_help_command_question_mark(self):
        """
        Test Case: Help command - question mark
        Input: "?"
        Expected Output: Help menu text
        Technique: Valid input partition (alternative form)
        """
        result = self.assistant.handle("?")
        self.assertIn("Commands:", result)
        print(f"✓ PASS: help command (?) - Input: '?', Output: {result[:50]}...")
    
    def test_topics_command(self):
        """
        Test Case: Topics command
        Input: "topics"
        Expected Output: List of available topics
        Technique: Valid input partition
        """
        result = self.assistant.handle("topics")
        self.assertIn("Available topics:", result)
        self.assertIn("about", result)
        print(f"✓ PASS: topics command - Input: 'topics', Output: {result[:50]}...")
    
    def test_info_command_valid_topic(self):
        """
        Test Case: Info command with valid topic
        Input: "info privacy"
        Expected Output: Topic information
        Technique: Valid input partition
        """
        result = self.assistant.handle("info privacy")
        self.assertIn("privacy:", result)
        print(f"✓ PASS: info command (valid) - Input: 'info privacy', Output: {result[:50]}...")
    
    def test_info_command_invalid_topic(self):
        """
        Test Case: Info command with invalid topic
        Input: "info nonexistent"
        Expected Output: Error message with "No information found" or suggestions
        Technique: Invalid input partition
        """
        result = self.assistant.handle("info nonexistent")
        # Check for "no information found" (lowercase) in the result
        self.assertIn("no information found", result.lower())
        print(f"✓ PASS: info command (invalid) - Input: 'info nonexistent', Output: {result[:50]}...")
    
    def test_unknown_command(self):
        """
        Test Case: Unknown command
        Input: "unknowncommand"
        Expected Output: Error message suggesting help
        Technique: Invalid input partition - Error handling
        """
        result = self.assistant.handle("unknowncommand")
        self.assertIn("not sure", result.lower())
        self.assertIn("help", result.lower())
        print(f"✓ PASS: unknown command - Input: 'unknowncommand', Output: {result[:50]}...")
    
    def test_empty_input(self):
        """
        Test Case: Empty input string
        Input: ""
        Expected Output: Message suggesting help
        Technique: Boundary value - empty input
        """
        result = self.assistant.handle("")
        self.assertIn("help", result.lower())
        print(f"✓ PASS: empty input - Input: '', Output: {result[:50]}...")
    
    def test_whitespace_only_input(self):
        """
        Test Case: Whitespace-only input
        Input: "   "
        Expected Output: Message suggesting help
        Technique: Boundary value - whitespace input
        """
        result = self.assistant.handle("   ")
        self.assertIn("help", result.lower())
        print(f"✓ PASS: whitespace input - Input: '   ', Output: {result[:50]}...")
    
    def test_command_with_extra_spaces(self):
        """
        Test Case: Command with extra spaces
        Input: "  help  "
        Expected Output: Help menu (should handle whitespace)
        Technique: Boundary value - extra whitespace
        """
        result = self.assistant.handle("  help  ")
        self.assertIn("Commands:", result)
        print(f"✓ PASS: command with spaces - Input: '  help  ', Output: {result[:50]}...")
    
    def test_case_insensitive_help(self):
        """
        Test Case: Case insensitive help command
        Input: "HELP"
        Expected Output: Help menu
        Technique: Valid input partition - case variation
        """
        result = self.assistant.handle("HELP")
        self.assertIn("Commands:", result)
        print(f"✓ PASS: uppercase help - Input: 'HELP', Output: {result[:50]}...")
    
    def test_case_insensitive_topics(self):
        """
        Test Case: Case insensitive topics command
        Input: "TOPICS"
        Expected Output: Topics list
        Technique: Valid input partition - case variation
        """
        result = self.assistant.handle("TOPICS")
        self.assertIn("Available topics:", result)
        print(f"✓ PASS: uppercase topics - Input: 'TOPICS', Output: {result[:50]}...")
    
    def test_info_command_empty_topic(self):
        """
        Test Case: Info command with empty topic
        Input: "info "
        Expected Output: Error message (after cleaning, "info " becomes "info" which doesn't match "info ")
        Technique: Boundary value - empty parameter
        """
        result = self.assistant.handle("info ")
        # After _clean(), "info " becomes "info", which doesn't startswith("info "), so returns error
        self.assertIn("not sure", result.lower())
        print(f"✓ PASS: info with empty topic - Input: 'info ', Output: {result[:50]}...")
    
    def test_info_command_with_multiple_spaces(self):
        """
        Test Case: Info command with multiple spaces
        Input: "info   privacy"
        Expected Output: Topic information (should normalize spaces)
        Technique: Boundary value - multiple spaces
        """
        result = self.assistant.handle("info   privacy")
        self.assertIn("privacy:", result)
        print(f"✓ PASS: info with multiple spaces - Input: 'info   privacy', Output: {result[:50]}...")


if __name__ == '__main__':
    unittest.main(verbosity=2)

