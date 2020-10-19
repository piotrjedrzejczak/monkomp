import unittest
import json
from monkomp.monkomp import create_app, db


class APITest(unittest.TestCase):

	def setUp(self):
		self.app = create_app()
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client()
	
	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()
	
	def test_customer(self):
		# Template
		customer = {
			'firstname': 'Jan',
			'lastname': 'Kowalski',
			'company_name': 'Jan Kowalski & Co',
			'city': 'Sosnowiec',
			'street': 'Wiejska 12',
			'email': 'jkco@giemail.com',
			'postal_code': '83-050',
			'nip': '6666666666',
			'telephone': '777888999',
			'comments': ''
		}

		# Create new customer
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json(), {"added":"1"})

		# Try to duplicate unique attributes
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		assert response.get_json()['message'].startswith('Customer with this')
		# self.assertEqual(response.get_json()[, {"error":"Bad Request","message":"Customer with this nip already exists."})

		# Try to create customer with invalid data
		invalid_data = 12
		response = self.client.post('/customers/new', json=invalid_data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Request data has to be a valid JSON object."})

		# Try to create customer with empty string
		invalid_data = ''
		response = self.client.post('/customers/new', json=invalid_data)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Request data has to be a valid JSON object."})

		# Missing required attributes
		empty_customer = {}
		response = self.client.post('/customers/new', json=empty_customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Required attribute missing [firstname]."})

		# Invalid NIP checksum.
		customer['nip'] = '6666666667'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Modulo checksum failed. You provided Invalid NIP Number."})
		
		# NIP too short
		customer['nip'] = '666666666'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid NIP Number has exactly ten digits, the one you passed has [9]."})
		
		# NIP contains characters.
		customer['nip'] = '666666666r'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid NIP Number only consists of digits."})

		# Reset to valid nip for upcoming tests.
		customer['nip'] = '6666666666'

		# Number is too long.
		customer['telephone'] = '3333333333'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid telephone number has exactly nine digits, the one you passed has [10]."})

		# Number is too short.
		customer['telephone'] = '3333333'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid telephone number has exactly nine digits, the one you passed has [7]."})

		# Number contains forbidden charachters
		customer['telephone'] = '33333333r'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid telephone number only consists of digits."})

		# Reset to valid telephone number.
		customer['telephone'] = '777888999'

		# Invalid postal code format.
		customer['postal_code'] = '777-43'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Provided postal code does not comply with the valid format [XX-XXX] where X stands for a digit."})
		
		# Empty postal code.
		customer['postal_code'] = ''
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Field [postal_code] has to be a non-empty string."})

		# Reset to valid postal code.
		customer['postal_code'] = '77-423'

		# Invalid attribute type
		customer['street'] = 12
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Field [street] has to be a string, not [int]."})

		# Reset to valid street.
		customer['street'] = 'Wiejska 12'

		# Get all customers
		# First create one extra record in DB
		customer['nip'] = '5831266157'
		customer['telephone'] = '111222333'
		customer['email'] = 'hello@gmail.com'
		customer['company_name'] = 'Efekt'
		response = self.client.post('/customers/new', json=customer)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json(), {"added":"1"})
		response = self.client.get('/customers')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.get_json()), 2)

		# Get customer by id
		response = self.client.get('/customers/1')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), {"added":"1"})
		
		