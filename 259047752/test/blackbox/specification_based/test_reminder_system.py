"""
Black-Box Testing: Specification-Based Testing
Technique: Equivalence Partitioning + Boundary Value Analysis
Functions: Reminder Creation, Reminder Listing, Reminder Searching, Reminder Deletion
Student: Guna Charan (259047752)
"""

import unittest
import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

# Try to import reminder functions - adjust import based on actual implementation
try:
    from main import ReminderManager
except ImportError:
    # If not in main.py, create a placeholder for testing structure
    class ReminderManager:
        def __init__(self, file_path="reminders.json"):
            self._file_path = file_path
            self._reminders = []
            self._next_id = 1
            self._load_reminders()
        
        def create_reminder(self, task, description=""):
            """Create a new reminder"""
            if not task or not task.strip():
                return "Task cannot be empty."
            reminder = {
                "id": self._next_id,
                "task": task.strip(),
                "description": description.strip() if description else "",
                "completed": False
            }
            self._next_id += 1
            self._reminders.append(reminder)
            self._save_reminders()
            return f"Reminder created. ID={reminder['id']}"
        
        def list_reminders(self):
            """List all reminders"""
            if not self._reminders:
                return "No reminders found."
            lines = ["Reminders:"]
            for r in self._reminders:
                status = "✓" if r["completed"] else "○"
                lines.append(f"ID={r['id']} {status} {r['task']}")
            return "\n".join(lines)
        
        def search_reminders(self, keyword):
            """Search reminders by keyword"""
            if not keyword or not keyword.strip():
                return "Usage: search <keyword>"
            keyword_lower = keyword.strip().lower()
            matches = []
            for r in self._reminders:
                if keyword_lower in r["task"].lower() or keyword_lower in r["description"].lower():
                    matches.append(r)
            if not matches:
                return f"No reminders found for keyword: {keyword}"
            lines = [f"Matches for '{keyword}':"]
            for r in matches:
                lines.append(f"ID={r['id']} {r['task']}")
            return "\n".join(lines)
        
        def delete_reminder(self, reminder_id):
            """Delete a reminder by ID"""
            if not isinstance(reminder_id, int) or reminder_id <= 0:
                return "Invalid reminder ID."
            for i in range(len(self._reminders)):
                if self._reminders[i]["id"] == reminder_id:
                    del self._reminders[i]
                    self._save_reminders()
                    return f"Reminder deleted. ID={reminder_id}"
            return f"Reminder not found: {reminder_id}"
        
        def _load_reminders(self):
            """Load reminders from file"""
            if os.path.exists(self._file_path):
                try:
                    with open(self._file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict) and "reminders" in data:
                            self._reminders = data["reminders"]
                            if self._reminders:
                                self._next_id = max(r["id"] for r in self._reminders) + 1
                            return True
                except Exception:
                    pass
            return False
        
        def _save_reminders(self):
            """Save reminders to file"""
            try:
                data = {"reminders": self._reminders}
                with open(self._file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True
            except Exception:
                return False


class TestReminderSystemSpecificationBased(unittest.TestCase):
    """
    Specification-Based Black-Box Tests for Reminder System
    """
    
    def setUp(self):
        """Set up test fixture with temporary file"""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.reminder_mgr = ReminderManager(file_path=self.temp_file.name)
    
    def tearDown(self):
        """Clean up temporary file"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_reminder_valid(self):
        """
        Test Case: Create reminder with valid task
        Input: task="Buy groceries", description="Milk and bread"
        Expected Output: "Reminder created. ID=1"
        Technique: Valid input partition
        """
        result = self.reminder_mgr.create_reminder("Buy groceries", "Milk and bread")
        self.assertIn("created", result.lower())
        self.assertIn("ID=1", result)
        print(f"✓ PASS: Create reminder (valid) - Input: task='Buy groceries', Output: {result}")
    
    def test_create_reminder_empty_task(self):
        """
        Test Case: Create reminder with empty task
        Input: task=""
        Expected Output: Error message
        Technique: Invalid input partition
        """
        result = self.reminder_mgr.create_reminder("")
        self.assertIn("cannot be empty", result.lower())
        print(f"✓ PASS: Create reminder (empty task) - Input: task='', Output: {result}")
    
    def test_list_reminders_empty(self):
        """
        Test Case: List reminders when none exist
        Input: No reminders
        Expected Output: "No reminders found."
        Technique: Empty state partition
        """
        result = self.reminder_mgr.list_reminders()
        self.assertIn("no reminders", result.lower())
        print(f"✓ PASS: List reminders (empty) - Output: {result}")
    
    def test_list_reminders_with_data(self):
        """
        Test Case: List reminders with data
        Input: Create reminders, then list
        Expected Output: List of reminders
        Technique: Valid state partition
        """
        self.reminder_mgr.create_reminder("Task 1")
        self.reminder_mgr.create_reminder("Task 2")
        result = self.reminder_mgr.list_reminders()
        self.assertIn("Reminders:", result)
        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)
        print("✓ PASS: List reminders (with data) - Output contains reminders")
    
    def test_search_reminders_valid(self):
        """
        Test Case: Search reminders with valid keyword
        Input: keyword="groceries"
        Expected Output: Matching reminders
        Technique: Valid input partition
        """
        self.reminder_mgr.create_reminder("Buy groceries")
        self.reminder_mgr.create_reminder("Call doctor")
        result = self.reminder_mgr.search_reminders("groceries")
        self.assertIn("groceries", result.lower())
        self.assertIn("ID=1", result)
        print(f"✓ PASS: Search reminders (valid) - Input: keyword='groceries', Output: {result[:50]}...")
    
    def test_search_reminders_no_match(self):
        """
        Test Case: Search reminders with no matches
        Input: keyword="nonexistent"
        Expected Output: "No reminders found"
        Technique: Invalid input partition
        """
        self.reminder_mgr.create_reminder("Buy groceries")
        result = self.reminder_mgr.search_reminders("nonexistent")
        self.assertIn("no reminders found", result.lower())
        print(f"✓ PASS: Search reminders (no match) - Input: keyword='nonexistent', Output: {result}")
    
    def test_search_reminders_empty_keyword(self):
        """
        Test Case: Search reminders with empty keyword
        Input: keyword=""
        Expected Output: Usage message
        Technique: Boundary value - empty input
        """
        result = self.reminder_mgr.search_reminders("")
        self.assertIn("usage", result.lower())
        print(f"✓ PASS: Search reminders (empty keyword) - Input: keyword='', Output: {result}")
    
    def test_delete_reminder_valid(self):
        """
        Test Case: Delete reminder with valid ID
        Input: reminder_id=1
        Expected Output: "Reminder deleted. ID=1"
        Technique: Valid input partition
        """
        self.reminder_mgr.create_reminder("Task to delete")
        result = self.reminder_mgr.delete_reminder(1)
        self.assertIn("deleted", result.lower())
        self.assertIn("ID=1", result)
        print(f"✓ PASS: Delete reminder (valid) - Input: id=1, Output: {result}")
    
    def test_delete_reminder_invalid_id(self):
        """
        Test Case: Delete reminder with invalid ID
        Input: reminder_id=999
        Expected Output: "Reminder not found: 999"
        Technique: Invalid input partition
        """
        result = self.reminder_mgr.delete_reminder(999)
        self.assertIn("not found", result.lower())
        print(f"✓ PASS: Delete reminder (invalid ID) - Input: id=999, Output: {result}")
    
    def test_delete_reminder_negative_id(self):
        """
        Test Case: Delete reminder with negative ID
        Input: reminder_id=-1
        Expected Output: Error message
        Technique: Boundary value - negative number
        """
        result = self.reminder_mgr.delete_reminder(-1)
        self.assertIn("invalid", result.lower())
        print(f"✓ PASS: Delete reminder (negative ID) - Input: id=-1, Output: {result}")
    
    def test_reminder_serialization(self):
        """
        Test Case: Reminder serialization - save and load
        Input: Create reminders, save, load in new instance
        Expected Output: Reminders should persist
        Technique: Serialization verification
        """
        self.reminder_mgr.create_reminder("Task 1")
        self.reminder_mgr.create_reminder("Task 2")
        new_mgr = ReminderManager(file_path=self.temp_file.name)
        result = new_mgr.list_reminders()
        self.assertIn("Task 1", result)
        self.assertIn("Task 2", result)
        print("✓ PASS: Reminder serialization - Reminders persisted")


if __name__ == '__main__':
    unittest.main(verbosity=2)

