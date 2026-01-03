"""
White-Box Testing: Branch Coverage
Technique: Ensure every decision (True/False) is tested
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


class TestCalculatorBranchCoverage(unittest.TestCase):
    """White-Box Branch Coverage Tests for Calculator"""
    
    def setUp(self):
        self.calculator = Calculator()
    
    # Branch: if not expression.strip() in calculate
    def test_branch_calculate_empty_expression_true(self):
        """Branch Coverage: if not expression.strip() (TRUE branch)"""
        result = self.calculator.calculate("")
        self.assertIn("Invalid", result)
        print("✓ Branch: calculate empty expression (TRUE)")
    
    def test_branch_calculate_empty_expression_false(self):
        """Branch Coverage: if not expression.strip() (FALSE branch)"""
        result = self.calculator.calculate("2 + 3")
        self.assertIn("Result", result)
        print("✓ Branch: calculate empty expression (FALSE)")
    
    # Branch: if not all(c in allowed_chars) in calculate
    def test_branch_calculate_invalid_chars_true(self):
        """Branch Coverage: if not all(c in allowed_chars) (TRUE branch)"""
        result = self.calculator.calculate("2 + abc")
        self.assertIn("Invalid", result)
        print("✓ Branch: calculate invalid chars (TRUE)")
    
    def test_branch_calculate_invalid_chars_false(self):
        """Branch Coverage: if not all(c in allowed_chars) (FALSE branch)"""
        result = self.calculator.calculate("2 + 3")
        self.assertIn("Result", result)
        print("✓ Branch: calculate invalid chars (FALSE)")
    
    # Branch: ZeroDivisionError exception
    def test_branch_calculate_division_by_zero_true(self):
        """Branch Coverage: ZeroDivisionError (TRUE branch)"""
        result = self.calculator.calculate("10 / 0")
        self.assertIn("zero", result.lower())
        print("✓ Branch: calculate division by zero (TRUE)")
    
    def test_branch_calculate_division_by_zero_false(self):
        """Branch Coverage: ZeroDivisionError (FALSE branch)"""
        result = self.calculator.calculate("10 / 2")
        self.assertIn("Result: 5", result)
        print("✓ Branch: calculate division by zero (FALSE)")
    
    # Branch: General Exception
    def test_branch_calculate_exception_true(self):
        """Branch Coverage: General Exception (TRUE branch)"""
        result = self.calculator.calculate("(((")
        self.assertIn("Invalid", result)
        print("✓ Branch: calculate exception (TRUE)")
    
    def test_branch_calculate_exception_false(self):
        """Branch Coverage: General Exception (FALSE branch)"""
        result = self.calculator.calculate("2 + 3")
        self.assertIn("Result: 5", result)
        print("✓ Branch: calculate exception (FALSE)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

