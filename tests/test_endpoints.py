import unittest
from app import create_app
from app.model import db

class APITest(unittest.TestCase):

	test_customer_1 = {
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
	test_customer_2 = {
			'firstname': 'Adam',
			'lastname': 'Migalski',
			'company_name': 'Efekt',
			'city': 'Rzeszów',
			'street': 'Miejska 2',
			'email': 'adam@gmail.com',
			'postal_code': '22-110',
			'nip': '5831266157',
			'telephone': '111222333',
			'comments': ''
		}

	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		self.client = self.app.test_client()
	
	def tearDown(self):
		# db.session.remove()
		# db.drop_all()
		self.app_context.pop()
	
	def test_create_a_new_customer(self):
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json(), {"added":"1"})
		response = self.client.post('/customers/new', json=self.test_customer_2)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json(), {"added":"1"})
	
	def test_create_customer_with_invalid_fields(self):
		self.test_customer_1['invalid'] = 'field'
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"'invalid' is an invalid keyword argument for Customer"})
		del self.test_customer_1['invalid']
	
	def test_create_duplicated_customer(self):
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		assert response.get_json()['message'].startswith('Customer with this')

	def test_create_customer_with_invalid_data_type(self):
		invalid_data_type = 12
		response = self.client.post('/customers/new', json=invalid_data_type)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Request data has to be a valid JSON object."})

	def test_create_customer_with_missing_required_fields(self):
		customer_missing_fields = {}
		response = self.client.post('/customers/new', json=customer_missing_fields)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Field firstname cannot be empty."})

	def test_create_customer_with_invalid_nip(self):
		self.test_customer_1['nip'] = '6666666667'
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Modulo checksum failed. You provided Invalid NIP Number."})
		self.test_customer_1['nip'] = '6666666666'

	def test_create_customer_with_invalid_nip_length(self):
		self.test_customer_1['nip'] = '666666666'
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid NIP Number has exactly ten digits, the one you passed has [9]."})
		self.test_customer_1['nip'] = '6666666666'

	def test_create_customer_with_nip_containing_charachters(self):
		self.test_customer_1['nip'] = '666666666r'
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid NIP Number only consists of digits."})
		self.test_customer_1['nip'] = '6666666666'

	def test_create_customer_with_invalid_telephone_length(self):
		self.test_customer_1['telephone'] = '3333333'
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid telephone number has exactly nine digits, the one you passed has [7]."})
		self.test_customer_1['telephone'] = '777888999'

	def test_create_customer_with_telephone_containing_charachters(self):
		self.test_customer_1['telephone'] = '33333333r'
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Valid telephone number only consists of digits."})
		self.test_customer_1['telephone'] = '777888999'
		
	def test_create_customer_with_invalid_postal_code_format(self):		
		self.test_customer_1['postal_code'] = '777-43'
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Provided postal code does not comply with the valid format [XX-XXX] where X stands for a digit."})
		self.test_customer_1['postal_code'] = '83-050'

	def test_create_customer_with_empty_postal_code(self):		
		self.test_customer_1['postal_code'] = ''
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Provided postal code does not comply with the valid format [XX-XXX] where X stands for a digit."})

	def test_create_customer_with_invalid_attribute_type(self):
		self.test_customer_1['street'] = 12
		response = self.client.post('/customers/new', json=self.test_customer_1)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {"error":"Bad Request","message":"Field [street] has to be a string, not [int]."})
		self.test_customer_1['street'] = 'Wiejska 12'

	def test_get_all_customers(self):
		response = self.client.get('/customers/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.get_json()), 2)

	def test_get_all_customers(self):
		response = self.client.get('/customers/1')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), self.test_customer_1)
