"""
White-Box Testing: Statement Coverage
Technique: Ensure every line of code executes at least once
Function: Calculator Command Processor
Student: Sameer Shaik (259047772)
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

try:
    from main import Calculator
except ImportError:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    spec_path = os.path.join(project_root, '259047772', 'test', 'blackbox', 'specification_based')
    if spec_path not in sys.path:
        sys.path.insert(0, spec_path)
    from test_calculator import Calculator


class TestCalculatorStatementCoverage(unittest.TestCase):
    """White-Box Statement Coverage Tests for Calculator"""
    
    def setUp(self):
        self.calculator = Calculator()
    
    def test_calculate_statement_coverage(self):
        """Statement Coverage: calculate() method - all lines"""
        result = self.calculator.calculate("2 + 3")
        self.assertIn("Result: 5", result)
        print("✓ Covered: calculate() method")
    
    def test_calculate_empty_expression_statement(self):
        """Statement Coverage: calculate() - empty expression check"""
        result = self.calculator.calculate("")
        self.assertIn("Invalid", result)
        print("✓ Covered: calculate() empty expression check")
    
    def test_calculate_invalid_characters_statement(self):
        """Statement Coverage: calculate() - invalid characters check"""
        result = self.calculator.calculate("2 + abc")
        self.assertIn("Invalid", result)
        print("✓ Covered: calculate() invalid characters check")
    
    def test_calculate_division_by_zero_statement(self):
        """Statement Coverage: calculate() - division by zero"""
        result = self.calculator.calculate("10 / 0")
        self.assertIn("zero", result.lower())
        print("✓ Covered: calculate() division by zero")
    
    def test_calculate_valid_expression_statement(self):
        """Statement Coverage: calculate() - valid expression path"""
        result = self.calculator.calculate("5 * 6")
        self.assertIn("Result: 30", result)
        print("✓ Covered: calculate() valid expression")


if __name__ == '__main__':
    unittest.main(verbosity=2)

