from app import app
import unittest

class LoginTestCase(unittest.TestCase):

	# Ensure that Flask was set up correctly
    def test_index(self):
	  tester = app.test_client(self)
	  response = tester.get('/login', content_type='html/text')
	  self.assertEqual(response.status_code, 200)

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertIn(b'Sign in', response.data)

	# Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Status', response.data)

	# Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        tester = app.test_client()
        response = tester.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials. Please try again.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        tester = app.test_client()
        tester.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Welcome to Sensor!', response.data)

if __name__ == '__main__':
    unittest.main()
    