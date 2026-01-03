"""
White-Box Testing: Concolic Testing
Technique: Concrete execution + Symbolic constraint collection + Constraint flipping
Function: handle() - Command Parsing Engine
Student: Saikiran (259053820)

Concolic testing combines concrete execution with symbolic reasoning:
1. Start with concrete input
2. Execute and collect path constraints
3. Flip constraints to explore new paths
4. Generate new test inputs
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import InfoSnippetAssistant


class TestCommandParsingConcolicTesting(unittest.TestCase):
    """
    Concolic Testing - Iterative Constraint Flipping
    
    Process:
    1. Initial concrete input
    2. Execute and record constraints
    3. Flip one constraint
    4. Solve for new input
    5. Repeat
    """
    
    def setUp(self):
        """Set up test fixture"""
        self.assistant = InfoSnippetAssistant()
    
    def test_concolic_iteration1_initial_input(self):
        """
        Concolic Iteration 1: Initial Concrete Input
        Initial Input: "help"
        Execution Path: x.strip() != "" (True), x.lower() in ("help","h","?") (True)
        Constraints Collected: [x.strip() != "", x.lower() == "help"]
        Result: Help menu returned
        """
        input_val = "help"
        result = self.assistant.handle(input_val)
        self.assertIn("Commands:", result)
        print(f"✓ Iteration 1: Input='{input_val}', Constraints=[x.strip() != '', x.lower() == 'help'], Result=Help menu")
    
    def test_concolic_iteration2_flip_help_constraint(self):
        """
        Concolic Iteration 2: Flip Help Constraint
        Previous Constraints: [x.strip() != "", x.lower() == "help"]
        Flipped Constraint: x.lower() != "help" AND x.lower() not in ("h", "?")
        New Input: "topics" (satisfies: x.strip() != "", x.lower() != "help", x.lower() == "topics")
        Execution Path: x.strip() != "" (True), x.lower() in ("help","h","?") (False), x.lower() == "topics" (True)
        Constraints Collected: [x.strip() != "", x.lower() != "help", x.lower() == "topics"]
        Result: Topics list returned
        """
        input_val = "topics"
        result = self.assistant.handle(input_val)
        self.assertIn("Available topics:", result)
        print(f"✓ Iteration 2: Input='{input_val}', Flipped: help constraint, Result=Topics list")
    
    def test_concolic_iteration3_flip_topics_constraint(self):
        """
        Concolic Iteration 3: Flip Topics Constraint
        Previous Constraints: [x.strip() != "", x.lower() != "help", x.lower() == "topics"]
        Flipped Constraint: x.lower() != "topics"
        New Input: "info privacy" (satisfies: x.strip() != "", x.lower() != "help", x.lower() != "topics", x.startswith("info "))
        Execution Path: x.strip() != "" (True), help check (False), topics check (False), x.startswith("info ") (True)
        Constraints Collected: [x.strip() != "", x.lower() != "help", x.lower() != "topics", x.startswith("info "), topic in snippets]
        Result: Topic information returned
        """
        input_val = "info privacy"
        result = self.assistant.handle(input_val)
        self.assertIn("privacy:", result)
        print(f"✓ Iteration 3: Input='{input_val}', Flipped: topics constraint, Result=Topic info")
    
    def test_concolic_iteration4_flip_info_prefix_constraint(self):
        """
        Concolic Iteration 4: Flip Info Prefix Constraint
        Previous Constraints: [x.strip() != "", x.lower() != "help", x.lower() != "topics", x.startswith("info ")]
        Flipped Constraint: not x.startswith("info ")
        New Input: "unknown" (satisfies: x.strip() != "", x.lower() != "help", x.lower() != "topics", not x.startswith("info "))
        Execution Path: All command checks fail → default error message
        Constraints Collected: [x.strip() != "", x.lower() != "help", x.lower() != "topics", not x.startswith("info ")]
        Result: Error message returned
        """
        input_val = "unknown"
        result = self.assistant.handle(input_val)
        self.assertIn("not sure", result.lower())
        print(f"✓ Iteration 4: Input='{input_val}', Flipped: info prefix constraint, Result=Error message")
    
    def test_concolic_iteration5_flip_empty_constraint(self):
        """
        Concolic Iteration 5: Flip Empty Input Constraint
        Previous Constraints: [x.strip() != ""]
        Flipped Constraint: x.strip() == ""
        New Input: "" (satisfies: x.strip() == "")
        Execution Path: x.strip() == "" (True) → early return
        Constraints Collected: [x.strip() == ""]
        Result: Help suggestion message
        """
        input_val = ""
        result = self.assistant.handle(input_val)
        self.assertIn("help", result.lower())
        print(f"✓ Iteration 5: Input='{input_val}', Flipped: empty constraint, Result=Help suggestion")
    
    def test_concolic_iteration6_info_empty_topic(self):
        """
        Concolic Iteration 6: Info Command with Empty Topic
        Previous Constraints: [x.startswith("info "), topic in snippets]
        Flipped Constraint: topic.strip() == ""
        Note: After _clean(), "info " becomes "info" which doesn't startswith("info ")
        New Input: "info " (after cleaning becomes "info", doesn't match pattern)
        Execution Path: x.startswith("info ") (False after cleaning) → error path
        Constraints Collected: [not x.startswith("info ") after cleaning]
        Result: Error message
        """
        input_val = "info "
        result = self.assistant.handle(input_val)
        # After _clean(), "info " becomes "info", which doesn't match "info " pattern
        self.assertIn("not sure", result.lower())
        print(f"✓ Iteration 6: Input='{input_val}', Flipped: topic empty constraint, Result=Error message (after cleaning)")
    
    def test_concolic_iteration7_info_invalid_topic(self):
        """
        Concolic Iteration 7: Info Command with Invalid Topic
        Previous Constraints: [x.startswith("info "), topic in snippets]
        Flipped Constraint: topic not in snippets AND no suggestions
        New Input: "info nonexistent123" (satisfies: x.startswith("info "), topic not in snippets, no partial match)
        Execution Path: x.startswith("info ") (True), topic.strip() != "" (True), topic in snippets (False), suggestions (False)
        Constraints Collected: [x.startswith("info "), x[5:].strip() != "", topic not in snippets, no suggestions]
        Result: No information message
        """
        input_val = "info nonexistent123"
        result = self.assistant.handle(input_val)
        self.assertIn("No information found", result)
        print(f"✓ Iteration 7: Input='{input_val}', Flipped: topic not in snippets, Result=No info message")
    
    def test_concolic_iteration8_info_with_suggestions(self):
        """
        Concolic Iteration 8: Info Command with Suggestions
        Previous Constraints: [x.startswith("info "), topic not in snippets, no suggestions]
        Flipped Constraint: topic not in snippets BUT suggestions found
        New Input: "info priv" (satisfies: x.startswith("info "), topic not in snippets, partial match found)
        Execution Path: x.startswith("info ") (True), topic.strip() != "" (True), topic in snippets (False), suggestions (True)
        Constraints Collected: [x.startswith("info "), x[5:].strip() != "", topic not in snippets, suggestions found]
        Result: Suggestions message
        """
        input_val = "info priv"
        result = self.assistant.handle(input_val)
        self.assertIn("Did you mean", result)
        print(f"✓ Iteration 8: Input='{input_val}', Flipped: suggestions constraint, Result=Suggestions message")
    
    def test_concolic_iteration9_help_shortcuts(self):
        """
        Concolic Iteration 9: Help Shortcuts
        Previous Constraints: [x.lower() == "help"]
        Flipped Constraint: x.lower() == "h" OR x.lower() == "?"
        New Input: "h" and "?" (satisfies: x.strip() != "", x.lower() in ("h", "?"))
        Execution Path: x.strip() != "" (True), x.lower() in ("help","h","?") (True)
        Constraints Collected: [x.strip() != "", x.lower() in ("h", "?")]
        Result: Help menu (same as "help")
        """
        result_h = self.assistant.handle("h")
        result_q = self.assistant.handle("?")
        self.assertIn("Commands:", result_h)
        self.assertIn("Commands:", result_q)
        print("✓ Iteration 9: Input='h' and '?', Flipped: help shortcuts, Result=Help menu")


if __name__ == '__main__':
    unittest.main(verbosity=2)

