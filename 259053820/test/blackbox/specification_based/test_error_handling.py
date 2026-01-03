"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Error Input Testing
Function: handle() - Error & Invalid Command Handling
Student: Saikiran (259053820)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import InfoSnippetAssistant


class TestErrorHandlingSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Error & Invalid Command Handling
    
    Test Categories:
    1. Unknown commands
    2. Invalid command formats
    3. Empty/null inputs
    4. Special characters
    5. Very long inputs
    6. Error message content verification
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.assistant = InfoSnippetAssistant()
    
    def test_unknown_command_returns_error(self):
        """
        Test Case: Unknown command returns error message
        Input: "unknowncommand"
        Expected Output: Error message with "not sure" and "help" suggestion
        Technique: Invalid input partition
        """
        result = self.assistant.handle("unknowncommand")
        # Function name: handle
        # Input: "unknowncommand"
        # Expected: Error message suggesting help
        # Actual: result
        self.assertIn("not sure", result.lower(), "Should contain 'not sure'")
        self.assertIn("help", result.lower(), "Should suggest help")
        print(f"✓ PASS: Unknown command - Input: 'unknowncommand', Expected: Error message, Actual: {result[:80]}...")
    
    def test_invalid_command_format(self):
        """
        Test Case: Invalid command format
        Input: "xyz123"
        Expected Output: Error message
        Technique: Invalid input partition
        """
        result = self.assistant.handle("xyz123")
        self.assertIn("not sure", result.lower())
        print(f"✓ PASS: Invalid format - Input: 'xyz123', Expected: Error message, Actual: {result[:80]}...")
    
    def test_empty_string_error(self):
        """
        Test Case: Empty string input
        Input: ""
        Expected Output: Message suggesting help (not error, but guidance)
        Technique: Boundary value - empty input
        """
        result = self.assistant.handle("")
        self.assertIn("help", result.lower())
        print(f"✓ PASS: Empty string - Input: '', Expected: Help suggestion, Actual: {result[:80]}...")
    
    def test_whitespace_only_error(self):
        """
        Test Case: Whitespace-only input
        Input: "   "
        Expected Output: Message suggesting help
        Technique: Boundary value - whitespace
        """
        result = self.assistant.handle("   ")
        self.assertIn("help", result.lower())
        print(f"✓ PASS: Whitespace only - Input: '   ', Expected: Help suggestion, Actual: {result[:80]}...")
    
    def test_special_characters(self):
        """
        Test Case: Special characters in command
        Input: "@#$%"
        Expected Output: Error message
        Technique: Invalid input partition - special characters
        """
        result = self.assistant.handle("@#$%")
        self.assertIn("not sure", result.lower())
        print(f"✓ PASS: Special chars - Input: '@#$%', Expected: Error message, Actual: {result[:80]}...")
    
    def test_very_long_input(self):
        """
        Test Case: Very long invalid input
        Input: "a" * 1000
        Expected Output: Error message
        Technique: Boundary value - very long input
        """
        long_input = "a" * 1000
        result = self.assistant.handle(long_input)
        self.assertIn("not sure", result.lower())
        print(f"✓ PASS: Very long input - Input: 'a'*1000, Expected: Error message, Actual: Error message")
    
    def test_partial_command(self):
        """
        Test Case: Partial command (incomplete)
        Input: "inf"
        Expected Output: Error message
        Technique: Invalid input partition - incomplete command
        """
        result = self.assistant.handle("inf")
        self.assertIn("not sure", result.lower())
        print(f"✓ PASS: Partial command - Input: 'inf', Expected: Error message, Actual: {result[:80]}...")
    
    def test_error_message_contains_help_suggestion(self):
        """
        Test Case: Error message contains helpful suggestions
        Input: "invalid"
        Expected Output: Error message with "help" and "topics" suggestions
        Technique: Error message content verification
        """
        result = self.assistant.handle("invalid")
        self.assertIn("help", result.lower())
        self.assertIn("topics", result.lower())
        print(f"✓ PASS: Error message content - Input: 'invalid', Expected: Helpful error, Actual: {result[:80]}...")
    
    def test_numeric_command(self):
        """
        Test Case: Numeric-only command
        Input: "12345"
        Expected Output: Error message
        Technique: Invalid input partition - numeric
        """
        result = self.assistant.handle("12345")
        self.assertIn("not sure", result.lower())
        print(f"✓ PASS: Numeric command - Input: '12345', Expected: Error message, Actual: {result[:80]}...")
    
    def test_mixed_case_unknown_command(self):
        """
        Test Case: Mixed case unknown command
        Input: "UnKnOwN"
        Expected Output: Error message
        Technique: Case variation - invalid command
        """
        result = self.assistant.handle("UnKnOwN")
        self.assertIn("not sure", result.lower())
        print(f"✓ PASS: Mixed case unknown - Input: 'UnKnOwN', Expected: Error message, Actual: {result[:80]}...")


if __name__ == '__main__':
    unittest.main(verbosity=2)

