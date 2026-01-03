"""
White-Box Testing: Statement Coverage
Technique: Ensure every line of code executes at least once
Functions: Reminder Creation, Listing, Searching, Deletion
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


class TestReminderStatementCoverage(unittest.TestCase):
    """White-Box Statement Coverage Tests for Reminder System"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.reminder_mgr = ReminderManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_reminder_statement_coverage(self):
        """Statement Coverage: create_reminder() method - all lines"""
        result = self.reminder_mgr.create_reminder("Task", "Description")
        self.assertIn("created", result.lower())
        print("✓ Covered: create_reminder() method")
    
    def test_create_reminder_empty_task_statement(self):
        """Statement Coverage: create_reminder() - empty task check"""
        result = self.reminder_mgr.create_reminder("")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Covered: create_reminder() empty task check")
    
    def test_list_reminders_statement_coverage(self):
        """Statement Coverage: list_reminders() method - all lines"""
        self.reminder_mgr.create_reminder("Task 1")
        result = self.reminder_mgr.list_reminders()
        self.assertIn("Reminders:", result)
        print("✓ Covered: list_reminders() method")
    
    def test_list_reminders_empty_statement(self):
        """Statement Coverage: list_reminders() - empty list check"""
        result = self.reminder_mgr.list_reminders()
        self.assertIn("no reminders", result.lower())
        print("✓ Covered: list_reminders() empty check")
    
    def test_search_reminders_statement_coverage(self):
        """Statement Coverage: search_reminders() method - all lines"""
        self.reminder_mgr.create_reminder("Buy groceries")
        result = self.reminder_mgr.search_reminders("groceries")
        self.assertIn("groceries", result.lower())
        print("✓ Covered: search_reminders() method")
    
    def test_search_reminders_empty_keyword_statement(self):
        """Statement Coverage: search_reminders() - empty keyword check"""
        result = self.reminder_mgr.search_reminders("")
        self.assertIn("usage", result.lower())
        print("✓ Covered: search_reminders() empty keyword check")
    
    def test_delete_reminder_statement_coverage(self):
        """Statement Coverage: delete_reminder() method - all lines"""
        self.reminder_mgr.create_reminder("Task")
        result = self.reminder_mgr.delete_reminder(1)
        self.assertIn("deleted", result.lower())
        print("✓ Covered: delete_reminder() method")
    
    def test_delete_reminder_invalid_id_statement(self):
        """Statement Coverage: delete_reminder() - invalid ID check"""
        result = self.reminder_mgr.delete_reminder(999)
        self.assertIn("not found", result.lower())
        print("✓ Covered: delete_reminder() invalid ID check")
    
    def test_load_reminders_statement_coverage(self):
        """Statement Coverage: _load_reminders() method"""
        self.reminder_mgr.create_reminder("Task")
        new_mgr = ReminderManager(file_path=self.temp_file.name)
        self.assertTrue(new_mgr._load_reminders())
        print("✓ Covered: _load_reminders() method")
    
    def test_save_reminders_statement_coverage(self):
        """Statement Coverage: _save_reminders() method"""
        self.reminder_mgr.create_reminder("Task")
        self.assertTrue(self.reminder_mgr._save_reminders())
        print("✓ Covered: _save_reminders() method")


if __name__ == '__main__':
    unittest.main(verbosity=2)

