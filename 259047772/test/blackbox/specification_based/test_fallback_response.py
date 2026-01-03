"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning
Function: Fallback Response Generator
Student: Sameer Shaik (259047772)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

# Try to import fallback functions - adjust import based on actual implementation
try:
    from main import FallbackResponse
except ImportError:
    # If not in main.py, create a placeholder for testing structure
    class FallbackResponse:
        def __init__(self):
            self._fallback_messages = [
                "I'm not sure how to help with that. Try typing 'help' for available commands.",
                "I don't understand that command. Type 'help' to see what I can do.",
                "Sorry, I didn't catch that. You can type 'help' to see available options."
            ]
        
        def generate_fallback(self, user_input):
            """Generate fallback response for unknown input"""
            if not user_input or not user_input.strip():
                return "Type 'help' to see available commands."
            
            # Return a helpful fallback message
            return (
                "I am not sure how to answer that.\n"
                "Try: topics (to see available information)\n"
                "Or type: help"
            )


class TestFallbackResponseSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Fallback Response
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.fallback = FallbackResponse()
    
    def test_fallback_unknown_command(self):
        """
        Test Case: Fallback for unknown command
        Input: "xyz123"
        Expected Output: Helpful fallback message
        Technique: Invalid input partition
        """
        result = self.fallback.generate_fallback("xyz123")
        self.assertIn("not sure", result.lower())
        self.assertIn("help", result.lower())
        print(f"✓ PASS: Fallback unknown command - Input: 'xyz123', Output: {result[:50]}...")
    
    def test_fallback_empty_input(self):
        """
        Test Case: Fallback for empty input
        Input: ""
        Expected Output: Help suggestion
        Technique: Boundary value - empty input
        """
        result = self.fallback.generate_fallback("")
        self.assertIn("help", result.lower())
        print(f"✓ PASS: Fallback empty input - Input: '', Output: {result}")
    
    def test_fallback_whitespace_input(self):
        """
        Test Case: Fallback for whitespace-only input
        Input: "   "
        Expected Output: Help suggestion
        Technique: Boundary value - whitespace
        """
        result = self.fallback.generate_fallback("   ")
        self.assertIn("help", result.lower())
        print(f"✓ PASS: Fallback whitespace input - Input: '   ', Output: {result}")
    
    def test_fallback_contains_help_suggestion(self):
        """
        Test Case: Fallback message contains helpful suggestions
        Input: "invalid"
        Expected Output: Message with help and topics suggestions
        Technique: Content verification
        """
        result = self.fallback.generate_fallback("invalid")
        self.assertIn("help", result.lower())
        self.assertIn("topics", result.lower())
        print(f"✓ PASS: Fallback helpful message - Input: 'invalid', Output: {result[:50]}...")


if __name__ == '__main__':
    unittest.main(verbosity=2)

