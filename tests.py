import unittest
from app import app

class URLTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
    
    def tearDown(self):
        with open('urls.json', 'w') as f:
            f.write('')
            f.close()
    
    def test_shorten_valid_url(self):
        response = self.app.post('/acortado', follow_redirects=True, data={'data':'https://www.google.com'})
        self.assertIn(b'URL acortada:', response.data)

    def test_shorten_invalid_or_null_url(self):
        response1 = self.app.post('/acortado', follow_redirects=True, data={'data':'google'})
        response2 = self.app.post('/acortado', follow_redirects=True, data={'data':''})

        self.assertIn(b'Debes escribir una URL', response1.data)
        self.assertIn(b'Debes escribir una URL', response2.data)
    
    def test_go_to_shortened_url(self):
        response = self.app.post('/acortado', follow_redirects=True, data={'data':'https://www.google.com'})
        url_index = str(response.data).find('<a href')
        url = str(response.data)[url_index+8:url_index+37]

        response = self.app.get(f'/{url.split("/")[-1]}', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)

    def test_go_to_invalid_shortened_url(self):
        response = self.app.get('/ongonboerngonwgji', follow_redirects=True)
        
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()