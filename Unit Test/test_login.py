import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BL.login_bl import validate_login 

class TestLogin(unittest.TestCase):
    def test_valid_login(self):
        """Test with valid credentials."""
        self.assertTrue(validate_login('admin', 'password'))

    def test_invalid_login(self):
        """Test with incorrect credentials."""
        self.assertFalse(validate_login('wrong_user', 'wrong_password'))

    def test_empty_username(self):
        """Test with an empty username."""
        self.assertFalse(validate_login('', 'password'))

    def test_empty_password(self):
        """Test with an empty password."""
        self.assertFalse(validate_login('admin', ''))

    def test_special_characters(self):
        """Test with special characters in username and password."""
        self.assertFalse(validate_login('admin$', 'p@ssw0rd!'))

    def test_sql_injection(self):
        """Test to prevent SQL injection attacks."""
        self.assertFalse(validate_login("' OR '1'='1", "' OR '1'='1"))

if __name__ == '__main__':
    unittest.main()


