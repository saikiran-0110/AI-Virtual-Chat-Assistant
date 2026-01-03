"""
White-Box Testing: Branch Coverage
Technique: Ensure every decision (True/False) is tested
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


class TestReminderBranchCoverage(unittest.TestCase):
    """White-Box Branch Coverage Tests for Reminder System"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.reminder_mgr = ReminderManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    # Branch: if not task or not task.strip() in create_reminder
    def test_branch_create_reminder_empty_task_true(self):
        """Branch Coverage: if not task.strip() (TRUE branch)"""
        result = self.reminder_mgr.create_reminder("")
        self.assertIn("cannot be empty", result.lower())
        print("✓ Branch: create_reminder empty task (TRUE)")
    
    def test_branch_create_reminder_empty_task_false(self):
        """Branch Coverage: if not task.strip() (FALSE branch)"""
        result = self.reminder_mgr.create_reminder("Valid Task")
        self.assertIn("created", result.lower())
        print("✓ Branch: create_reminder empty task (FALSE)")
    
    # Branch: if not self._reminders in list_reminders
    def test_branch_list_reminders_empty_true(self):
        """Branch Coverage: if not self._reminders (TRUE branch)"""
        result = self.reminder_mgr.list_reminders()
        self.assertIn("no reminders", result.lower())
        print("✓ Branch: list_reminders empty (TRUE)")
    
    def test_branch_list_reminders_empty_false(self):
        """Branch Coverage: if not self._reminders (FALSE branch)"""
        self.reminder_mgr.create_reminder("Task")
        result = self.reminder_mgr.list_reminders()
        self.assertIn("Reminders:", result)
        print("✓ Branch: list_reminders empty (FALSE)")
    
    # Branch: if not keyword.strip() in search_reminders
    def test_branch_search_reminders_empty_keyword_true(self):
        """Branch Coverage: if not keyword.strip() (TRUE branch)"""
        result = self.reminder_mgr.search_reminders("")
        self.assertIn("usage", result.lower())
        print("✓ Branch: search_reminders empty keyword (TRUE)")
    
    def test_branch_search_reminders_empty_keyword_false(self):
        """Branch Coverage: if not keyword.strip() (FALSE branch)"""
        self.reminder_mgr.create_reminder("Task")
        result = self.reminder_mgr.search_reminders("Task")
        self.assertIn("Task", result)
        print("✓ Branch: search_reminders empty keyword (FALSE)")
    
    # Branch: if not matches in search_reminders
    def test_branch_search_reminders_no_matches_true(self):
        """Branch Coverage: if not matches (TRUE branch)"""
        result = self.reminder_mgr.search_reminders("nonexistent")
        self.assertIn("no reminders found", result.lower())
        print("✓ Branch: search_reminders no matches (TRUE)")
    
    def test_branch_search_reminders_no_matches_false(self):
        """Branch Coverage: if not matches (FALSE branch)"""
        self.reminder_mgr.create_reminder("Buy groceries")
        result = self.reminder_mgr.search_reminders("groceries")
        self.assertIn("groceries", result.lower())
        print("✓ Branch: search_reminders no matches (FALSE)")
    
    # Branch: if reminder_id <= 0 in delete_reminder
    def test_branch_delete_reminder_invalid_id_true(self):
        """Branch Coverage: if reminder_id <= 0 (TRUE branch)"""
        result = self.reminder_mgr.delete_reminder(-1)
        self.assertIn("invalid", result.lower())
        print("✓ Branch: delete_reminder invalid ID (TRUE)")
    
    def test_branch_delete_reminder_invalid_id_false(self):
        """Branch Coverage: if reminder_id <= 0 (FALSE branch)"""
        self.reminder_mgr.create_reminder("Task")
        result = self.reminder_mgr.delete_reminder(1)
        self.assertIn("deleted", result.lower())
        print("✓ Branch: delete_reminder invalid ID (FALSE)")
    
    # Branch: Loop in delete_reminder - found/not found
    def test_branch_delete_reminder_found_true(self):
        """Branch Coverage: reminder found in loop (TRUE branch)"""
        self.reminder_mgr.create_reminder("Task")
        result = self.reminder_mgr.delete_reminder(1)
        self.assertIn("deleted", result.lower())
        print("✓ Branch: delete_reminder found (TRUE)")
    
    def test_branch_delete_reminder_found_false(self):
        """Branch Coverage: reminder not found in loop (FALSE branch)"""
        result = self.reminder_mgr.delete_reminder(999)
        self.assertIn("not found", result.lower())
        print("✓ Branch: delete_reminder found (FALSE)")


if __name__ == '__main__':
    unittest.main(verbosity=2)

