"""
White-Box Testing: Symbolic Execution
Technique: Symbolic execution with path condition derivation
Functions: Reminder Creation, Searching, Deletion
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


class TestReminderSymbolicExecution(unittest.TestCase):
    """Symbolic Execution Derived Tests for Reminder System"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.reminder_mgr = ReminderManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    # Path 1: create_reminder - empty task
    def test_path1_create_reminder_empty(self):
        """
        Path Condition: task.strip() == ""
        Symbolic Input: x = ""
        Concrete Input: ""
        Expected Output: "Task cannot be empty."
        """
        result = self.reminder_mgr.create_reminder("")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Path 1: Create reminder (empty task) -> Error message")
    
    # Path 2: create_reminder - valid task
    def test_path2_create_reminder_valid(self):
        """
        Path Condition: task.strip() != ""
        Symbolic Input: x = "valid task"
        Concrete Input: "Buy groceries"
        Expected Output: "Reminder created. ID=1"
        """
        result = self.reminder_mgr.create_reminder("Buy groceries")
        self.assertIn("created", result.lower())
        print("✓ Path 2: Create reminder (valid task) -> Reminder created")
    
    # Path 3: search_reminders - empty keyword
    def test_path3_search_empty_keyword(self):
        """
        Path Condition: keyword.strip() == ""
        Symbolic Input: x = ""
        Concrete Input: ""
        Expected Output: "Usage: search <keyword>"
        """
        result = self.reminder_mgr.search_reminders("")
        self.assertIn("usage", result.lower())
        print("✓ Path 3: Search reminders (empty keyword) -> Usage message")
    
    # Path 4: search_reminders - no matches
    def test_path4_search_no_matches(self):
        """
        Path Condition: keyword.strip() != "" AND no matches found
        Symbolic Input: x = "nonexistent"
        Concrete Input: "nonexistent"
        Expected Output: "No reminders found"
        """
        result = self.reminder_mgr.search_reminders("nonexistent")
        self.assertIn("no reminders found", result.lower())
        print("✓ Path 4: Search reminders (no matches) -> No results")
    
    # Path 5: search_reminders - matches found
    def test_path5_search_matches_found(self):
        """
        Path Condition: keyword.strip() != "" AND matches found
        Symbolic Input: x = "groceries"
        Concrete Input: "groceries"
        Expected Output: Matching reminders list
        """
        self.reminder_mgr.create_reminder("Buy groceries")
        result = self.reminder_mgr.search_reminders("groceries")
        self.assertIn("groceries", result.lower())
        print("✓ Path 5: Search reminders (matches found) -> Results list")
    
    # Path 6: delete_reminder - invalid ID
    def test_path6_delete_invalid_id(self):
        """
        Path Condition: reminder_id <= 0
        Symbolic Input: x <= 0
        Concrete Input: -1
        Expected Output: "Invalid reminder ID."
        """
        result = self.reminder_mgr.delete_reminder(-1)
        self.assertIn("invalid", result.lower())
        print("✓ Path 6: Delete reminder (invalid ID) -> Error message")
    
    # Path 7: delete_reminder - not found
    def test_path7_delete_not_found(self):
        """
        Path Condition: reminder_id > 0 AND reminder not found
        Symbolic Input: x = 999
        Concrete Input: 999
        Expected Output: "Reminder not found: 999"
        """
        result = self.reminder_mgr.delete_reminder(999)
        self.assertIn("not found", result.lower())
        print("✓ Path 7: Delete reminder (not found) -> Not found message")
    
    # Path 8: delete_reminder - found and deleted
    def test_path8_delete_found(self):
        """
        Path Condition: reminder_id > 0 AND reminder found
        Symbolic Input: x = 1
        Concrete Input: 1
        Expected Output: "Reminder deleted. ID=1"
        """
        self.reminder_mgr.create_reminder("Task to delete")
        result = self.reminder_mgr.delete_reminder(1)
        self.assertIn("deleted", result.lower())
        print("✓ Path 8: Delete reminder (found) -> Deleted message")


if __name__ == '__main__':
    unittest.main(verbosity=2)

