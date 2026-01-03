"""
White-Box Testing: Statement Coverage
Technique: Ensure every line of code executes at least once
Functions: User Profile Setup, Profile Update, Profile Serialization
Student: Guna Charan (259047752)
"""

import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

try:
    from main import UserProfile
except ImportError:
    # Import from blackbox test file where UserProfile is defined
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    spec_path = os.path.join(project_root, '259047752', 'test', 'blackbox', 'specification_based')
    if spec_path not in sys.path:
        sys.path.insert(0, spec_path)
    from test_profile_system import UserProfile


class TestProfileStatementCoverage(unittest.TestCase):
    """White-Box Statement Coverage Tests for Profile System"""
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.profile = UserProfile(file_path=self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_setup_profile_statement_coverage(self):
        """Statement Coverage: setup_profile() method - all lines"""
        result = self.profile.setup_profile("TestUser", {"theme": "dark"})
        self.assertIn("complete", result.lower())
        print("✓ Covered: setup_profile() method")
    
    def test_setup_profile_empty_name_statement(self):
        """Statement Coverage: setup_profile() - empty name check"""
        result = self.profile.setup_profile("", {})
        self.assertIn("cannot be empty", result.lower())
        print("✓ Covered: setup_profile() empty name check")
    
    def test_update_profile_statement_coverage(self):
        """Statement Coverage: update_profile() method - all lines"""
        self.profile.setup_profile("User", {})
        result = self.profile.update_profile(name="NewUser", theme="light")
        self.assertIn("updated", result.lower())
        print("✓ Covered: update_profile() method")
    
    def test_update_profile_no_profile_statement(self):
        """Statement Coverage: update_profile() - no profile check"""
        new_profile = UserProfile(file_path=self.temp_file.name + "_new")
        result = new_profile.update_profile(name="User")
        self.assertIn("no profile", result.lower())
        print("✓ Covered: update_profile() no profile check")
    
    def test_get_profile_statement_coverage(self):
        """Statement Coverage: get_profile() method"""
        self.profile.setup_profile("User", {})
        result = self.profile.get_profile()
        self.assertIsInstance(result, dict)
        print("✓ Covered: get_profile() method")
    
    def test_load_profile_statement_coverage(self):
        """Statement Coverage: _load_profile() method"""
        self.profile.setup_profile("User", {})
        new_profile = UserProfile(file_path=self.temp_file.name)
        self.assertTrue(new_profile._load_profile())
        print("✓ Covered: _load_profile() method")
    
    def test_save_profile_statement_coverage(self):
        """Statement Coverage: _save_profile() method"""
        self.profile.setup_profile("User", {})
        self.assertTrue(self.profile._save_profile())
        print("✓ Covered: _save_profile() method")


if __name__ == '__main__':
    unittest.main(verbosity=2)

