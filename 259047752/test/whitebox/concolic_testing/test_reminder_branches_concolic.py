"""
White-Box Testing: Concolic Testing
Technique: Concrete execution + Symbolic constraint collection + Constraint flipping
Functions: Reminder System
Student: Guna Charan (259047752)
"""

import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

try:
    from main import ReminderManager
except ImportError:
    # Import from blackbox test file where ReminderManager is defined
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    spec_path = os.path.join(project_root, '259047752', 'test', 'blackbox', 'specification_based')
    if spec_path not in sys.path:
        sys.path.insert(0, spec_path)
    from test_reminder_system import ReminderManager


class TestReminderConcolicTesting(unittest.TestCase):
    """Concolic Testing - Iterative Constraint Flipping for Reminder System"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.reminder_mgr = ReminderManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_concolic_iteration1_create_reminder_valid(self):
        """
        Concolic Iteration 1: Initial Concrete Input
        Initial Input: task="Buy groceries"
        Execution Path: task.strip() != "" (True)
        Constraints Collected: [task.strip() != ""]
        Result: Reminder created
        """
        input_val = "Buy groceries"
        result = self.reminder_mgr.create_reminder(input_val)
        self.assertIn("created", result.lower())
        print(f"✓ Iteration 1: Input='{input_val}', Constraints=[task.strip() != ''], Result=Reminder created")
    
    def test_concolic_iteration2_flip_task_constraint(self):
        """
        Concolic Iteration 2: Flip Task Constraint
        Previous Constraints: [task.strip() != ""]
        Flipped Constraint: task.strip() == ""
        New Input: "" (satisfies: task.strip() == "")
        Execution Path: task.strip() == "" (True)
        Constraints Collected: [task.strip() == ""]
        Result: Error message
        """
        input_val = ""
        result = self.reminder_mgr.create_reminder(input_val)
        self.assertIn("cannot be empty", result.lower())
        print(f"✓ Iteration 2: Input='{input_val}', Flipped: task constraint, Result=Error message")
    
    def test_concolic_iteration3_search_valid_keyword(self):
        """
        Concolic Iteration 3: Search with Valid Keyword
        Initial Input: keyword="groceries"
        Execution Path: keyword.strip() != "" (True), matches found (True)
        Constraints Collected: [keyword.strip() != "", matches found]
        Result: Matching reminders
        """
        self.reminder_mgr.create_reminder("Buy groceries")
        input_val = "groceries"
        result = self.reminder_mgr.search_reminders(input_val)
        self.assertIn("groceries", result.lower())
        print(f"✓ Iteration 3: Input='{input_val}', Constraints=[keyword.strip() != '', matches found], Result=Matches")
    
    def test_concolic_iteration4_flip_search_keyword_constraint(self):
        """
        Concolic Iteration 4: Flip Search Keyword Constraint
        Previous Constraints: [keyword.strip() != "", matches found]
        Flipped Constraint: keyword.strip() == ""
        New Input: "" (satisfies: keyword.strip() == "")
        Execution Path: keyword.strip() == "" (True)
        Constraints Collected: [keyword.strip() == ""]
        Result: Usage message
        """
        input_val = ""
        result = self.reminder_mgr.search_reminders(input_val)
        self.assertIn("usage", result.lower())
        print(f"✓ Iteration 4: Input='{input_val}', Flipped: keyword constraint, Result=Usage message")
    
    def test_concolic_iteration5_search_no_matches(self):
        """
        Concolic Iteration 5: Search with No Matches
        Previous Constraints: [keyword.strip() != "", matches found]
        Flipped Constraint: keyword.strip() != "" AND no matches
        New Input: "nonexistent" (satisfies: keyword.strip() != "", no matches)
        Execution Path: keyword.strip() != "" (True), matches found (False)
        Constraints Collected: [keyword.strip() != "", no matches]
        Result: No reminders found
        """
        input_val = "nonexistent"
        result = self.reminder_mgr.search_reminders(input_val)
        self.assertIn("no reminders found", result.lower())
        print(f"✓ Iteration 5: Input='{input_val}', Flipped: matches constraint, Result=No matches")
    
    def test_concolic_iteration6_delete_valid_id(self):
        """
        Concolic Iteration 6: Delete with Valid ID
        Initial Input: reminder_id=1
        Execution Path: reminder_id > 0 (True), reminder found (True)
        Constraints Collected: [reminder_id > 0, reminder found]
        Result: Reminder deleted
        """
        self.reminder_mgr.create_reminder("Task")
        input_val = 1
        result = self.reminder_mgr.delete_reminder(input_val)
        self.assertIn("deleted", result.lower())
        print(f"✓ Iteration 6: Input={input_val}, Constraints=[id > 0, found], Result=Deleted")
    
    def test_concolic_iteration7_flip_delete_id_constraint(self):
        """
        Concolic Iteration 7: Flip Delete ID Constraint
        Previous Constraints: [reminder_id > 0, reminder found]
        Flipped Constraint: reminder_id <= 0
        New Input: -1 (satisfies: reminder_id <= 0)
        Execution Path: reminder_id <= 0 (True)
        Constraints Collected: [reminder_id <= 0]
        Result: Invalid ID message
        """
        input_val = -1
        result = self.reminder_mgr.delete_reminder(input_val)
        self.assertIn("invalid", result.lower())
        print(f"✓ Iteration 7: Input={input_val}, Flipped: id constraint, Result=Invalid ID")
    
    def test_concolic_iteration8_delete_not_found(self):
        """
        Concolic Iteration 8: Delete with Not Found
        Previous Constraints: [reminder_id > 0, reminder found]
        Flipped Constraint: reminder_id > 0 AND reminder not found
        New Input: 999 (satisfies: reminder_id > 0, not found)
        Execution Path: reminder_id > 0 (True), reminder found (False)
        Constraints Collected: [reminder_id > 0, reminder not found]
        Result: Not found message
        """
        input_val = 999
        result = self.reminder_mgr.delete_reminder(input_val)
        self.assertIn("not found", result.lower())
        print(f"✓ Iteration 8: Input={input_val}, Flipped: found constraint, Result=Not found")


if __name__ == '__main__':
    unittest.main(verbosity=2)

