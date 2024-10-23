import unittest
from BL.login_bl import validate_login

class TestLogin(unittest.TestCase):
    def test_valid_login(self):
        self.assertTrue(validate_login('admin', 'password'))

    def test_invalid_login(self):
        self.assertFalse(validate_login('wrong_user', 'wrong_password'))

if __name__ == '__main__':
    unittest.main()
