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
	test_product_1 = {
		'factory_number': 'kas123',
		'serial_number': 'xyz123',
		'name': '',
		'last_service': '2020-10-27 19:49:13.076826',
		'price': '19999'
	}
	test_product_2 = {
		'factory_number': 'ter123',
		'serial_number': '',
		'name': 'Terminal',
		'last_service': '2020-10-28 21:49:22.922116',
		'price': '35000'
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

	def test_get_customer_by_valid_id(self):
		response = self.client.get('/customers/1')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), self.test_customer_1)

	def test_get_customer_by_invalid_id(self):
		response = self.client.get('/customers/999999')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json(), {'error': 'resource not found'})

	def test_add_new_product(self):
		response = self.client.post('/products/new', json=self.test_product_1)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.get_json(), {"added":"1"})

	def test_get_all_products(self):
		self.client.post('/products/new', json=self.test_product_2)
		response = self.client.get('/products/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.get_json()), 2)
		self.assertEqual(response.get_json(), [self.test_product_1, self.test_product_2])

	def test_get_product_by_factory_number(self):
		response = self.client.get('/products/kas123')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.get_json(), self.test_product_1)
	
	def test_get_product_by_invalid_factory_number(self):
		response = self.client.get('/products/99999999asd')
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.get_json(), {'error': 'resource not found'})
	
	def test_add_product_with_missing_fields(self):
		del self.test_product_2['price']
		response = self.client.post('/products/new', json=self.test_product_2)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.get_json(), {'error': 'Bad Request', 'message': 'Field price cannot be empty.'})
		self.test_product_2['price'] = '35000'
