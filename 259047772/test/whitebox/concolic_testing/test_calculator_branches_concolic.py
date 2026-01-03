"""
White-Box Testing: Concolic Testing
Technique: Concrete execution + Symbolic constraint collection + Constraint flipping
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


class TestCalculatorConcolicTesting(unittest.TestCase):
    """Concolic Testing - Iterative Constraint Flipping for Calculator"""
    
    def setUp(self):
        self.calculator = Calculator()
    
    def test_concolic_iteration1_valid_expression(self):
        """
        Concolic Iteration 1: Initial Concrete Input
        Initial Input: expression="2 + 3"
        Execution Path: expression.strip() != "" (True), all chars valid (True), eval succeeds (True)
        Constraints Collected: [expression.strip() != "", all chars valid, eval succeeds]
        Result: "Result: 5"
        """
        input_val = "2 + 3"
        result = self.calculator.calculate(input_val)
        self.assertIn("Result: 5", result)
        print(f"✓ Iteration 1: Input='{input_val}', Constraints=[expression != '', valid chars, eval succeeds], Result=5")
    
    def test_concolic_iteration2_flip_empty_constraint(self):
        """
        Concolic Iteration 2: Flip Empty Expression Constraint
        Previous Constraints: [expression.strip() != ""]
        Flipped Constraint: expression.strip() == ""
        New Input: "" (satisfies: expression.strip() == "")
        Execution Path: expression.strip() == "" (True)
        Constraints Collected: [expression.strip() == ""]
        Result: "Invalid expression."
        """
        input_val = ""
        result = self.calculator.calculate(input_val)
        self.assertIn("Invalid", result)
        print(f"✓ Iteration 2: Input='{input_val}', Flipped: empty constraint, Result=Invalid")
    
    def test_concolic_iteration3_flip_valid_chars_constraint(self):
        """
        Concolic Iteration 3: Flip Valid Characters Constraint
        Previous Constraints: [expression.strip() != "", all chars valid]
        Flipped Constraint: not all chars valid
        New Input: "2 + abc" (satisfies: expression.strip() != "", invalid chars)
        Execution Path: expression.strip() != "" (True), all chars valid (False)
        Constraints Collected: [expression.strip() != "", not all chars valid]
        Result: "Invalid characters in expression."
        """
        input_val = "2 + abc"
        result = self.calculator.calculate(input_val)
        self.assertIn("Invalid", result)
        print(f"✓ Iteration 3: Input='{input_val}', Flipped: valid chars constraint, Result=Invalid")
    
    def test_concolic_iteration4_flip_division_by_zero(self):
        """
        Concolic Iteration 4: Flip Division by Zero Constraint
        Previous Constraints: [eval succeeds]
        Flipped Constraint: ZeroDivisionError
        New Input: "10 / 0" (satisfies: valid chars, division by zero)
        Execution Path: expression.strip() != "" (True), all chars valid (True), ZeroDivisionError (True)
        Constraints Collected: [expression.strip() != "", all chars valid, ZeroDivisionError]
        Result: "Error: Division by zero."
        """
        input_val = "10 / 0"
        result = self.calculator.calculate(input_val)
        self.assertIn("zero", result.lower())
        print(f"✓ Iteration 4: Input='{input_val}', Flipped: division by zero constraint, Result=Division by zero error")
    
    def test_concolic_iteration5_flip_eval_exception(self):
        """
        Concolic Iteration 5: Flip Eval Exception Constraint
        Previous Constraints: [eval succeeds]
        Flipped Constraint: General Exception (invalid expression)
        New Input: "(((" (satisfies: valid chars, invalid expression)
        Execution Path: expression.strip() != "" (True), all chars valid (True), Exception (True)
        Constraints Collected: [expression.strip() != "", all chars valid, Exception]
        Result: "Error: Invalid expression."
        """
        input_val = "((("
        result = self.calculator.calculate(input_val)
        self.assertIn("Invalid", result)
        print(f"✓ Iteration 5: Input='{input_val}', Flipped: eval exception constraint, Result=Invalid expression")
    
    def test_concolic_iteration6_negative_numbers(self):
        """
        Concolic Iteration 6: Negative Numbers
        Previous Constraints: [expression.strip() != "", all chars valid, eval succeeds]
        New Input: "-5 + 3" (satisfies: all constraints, negative number)
        Execution Path: All checks pass, eval succeeds
        Constraints Collected: [expression.strip() != "", all chars valid, eval succeeds, negative number]
        Result: "Result: -2"
        """
        input_val = "-5 + 3"
        result = self.calculator.calculate(input_val)
        self.assertIn("Result: -2", result)
        print(f"✓ Iteration 6: Input='{input_val}', Constraints=[negative number], Result=-2")
    
    def test_concolic_iteration7_parentheses(self):
        """
        Concolic Iteration 7: Expression with Parentheses
        Previous Constraints: [expression.strip() != "", all chars valid, eval succeeds]
        New Input: "(2 + 3) * 4" (satisfies: all constraints, parentheses)
        Execution Path: All checks pass, eval succeeds
        Constraints Collected: [expression.strip() != "", all chars valid, eval succeeds, parentheses]
        Result: "Result: 20"
        """
        input_val = "(2 + 3) * 4"
        result = self.calculator.calculate(input_val)
        self.assertIn("Result: 20", result)
        print(f"✓ Iteration 7: Input='{input_val}', Constraints=[parentheses], Result=20")


if __name__ == '__main__':
    unittest.main(verbosity=2)

