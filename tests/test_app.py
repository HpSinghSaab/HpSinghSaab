import unittest
import json
from src.app import app

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Resource AI Platform', response.data)

    def test_calculate_api(self):
        payload = {
            "price": 1.0,
            "investment": 10000,
            "tax_rate": 0.5,
            "province": "ON"
        }
        response = self.app.post('/api/calculate',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(data['net_out_of_pocket'], 3000.0)

    def test_parse_api(self):
        payload = {"text": "5.0 g/t Au over 10m"}
        response = self.app.post('/api/parse',
                                 data=json.dumps(payload),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['au_gram_meters'], 50.0)

if __name__ == '__main__':
    unittest.main()
