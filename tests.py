import unittest
from app import app

class URLTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    def test_shorten_valid_url(self):
        response = self.app.post('/acortado', follow_redirects=True, data={'data':'https://www.google.com'})
        self.assertIn(b'URL acortada:', response.data)

    def test_shorten_invalid_or_null_url(self):
        response1 = self.app.post('/acortado', follow_redirects=True, data={'data':'google'})
        response2 = self.app.post('/acortado', follow_redirects=True, data={'data':''})

        self.assertIn(b'Debes escribir una URL', response1.data)
        self.assertIn(b'Debes escribir una URL', response2.data)

if __name__ == '__main__':
    unittest.main()