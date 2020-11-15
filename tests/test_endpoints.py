import unittest

from base64 import b64encode
from app import create_app
from app.model import db
from app.model.engineer import Engineer


class APITest(unittest.TestCase):

    test_customer_1 = {
        "firstname": "Jan",
        "lastname": "Kowalski",
        "company_name": "Jan Kowalski & Co",
        "city": "Sosnowiec",
        "street": "Wiejska 12",
        "email": "jkco@giemail.com",
        "postal_code": "83-050",
        "nip": "6666666666",
        "telephone": "777888999",
        "comments": "",
    }
    test_customer_2 = {
        "firstname": "Adam",
        "lastname": "Migalski",
        "company_name": "Efekt",
        "city": "Rzeszów",
        "street": "Miejska 2",
        "email": "adam@gmail.com",
        "postal_code": "22-110",
        "nip": "5831266157",
        "telephone": "111222333",
        "comments": "",
    }
    test_product_1 = {
        "factory_number": "kas123",
        "serial_number": "xyz123",
        "name": "",
        "last_service": "2020-10-27 19:49:13.076826",
        "price": "19999",
    }
    test_product_2 = {
        "factory_number": "ter123",
        "serial_number": "",
        "name": "Terminal",
        "last_service": "2020-10-28 21:49:22.922116",
        "price": "35000",
    }
    test_service_1 = {"id": "1", "name": "Fiskalizacja", "rate": "20000"}
    test_service_2 = {"id": "2", "name": "Serwis", "rate": "5000"}
    test_field_call = {
        "comments": "Wycieczka do klienta",
        "invoiced": False,
        "settled": False,
        "date": "2020-10-30 21:49:22.922116",
        "total": "30000",
        "payment_type": "Gotówka",
        "engineer_id": "1",
        "service_id": "1",
        "customer_id": "1",
    }
    test_contract = {
        "account_number": "111122223333444455556666",
        "signed_on": "2020-10-30 21:49:22.922116",
        "expires_on": "2021-10-30 21:49:22.922116",
        "customer_id": "1",
    }
    test_engineer = {
        "firstname": "piotr",
        "lastname": "jedrzejczak",
        "email": "julian.jedrzejczak@gmail.com",
        "password": "pioter123",
    }
    email = "julian.jedrzejczak@gmail.com"
    password = "pioter123"

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.maxDiff = None
        db.session.add(Engineer.from_dict(self.test_engineer))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @staticmethod
    def get_headers(email, password):
        return {
            "Authorization": "Basic "
            + b64encode(f"{email}:{password}".encode("utf-8")).decode("utf-8"),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    # AUTHENTICATION ENDPOINT

    def test_auth(self):
        response = self.client.get(
            "/customers/", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)

    def test_no_auth(self):
        response = self.client.get("/customers/")
        self.assertEqual(response.status_code, 401)

    def test_bad_password(self):
        self.password = "bad-password"
        response = self.client.get(
            "/customers/", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 401)
        self.password = "pioter123"

    def test_bad_token_auth(self):
        response = self.client.get(
            "/customers/", headers=self.get_headers("bad-token", "")
        )
        self.assertEqual(response.status_code, 401)

    def test_good_token_auth(self):
        response = self.client.post(
            "/token", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsNotNone(payload.get("token"))
        token = payload["token"]
        # Try to send a request with valid token
        response = self.client.get("/customers/", headers=self.get_headers(token, ""))
        self.assertEqual(response.status_code, 200)

    # CUSTOMER ENDPOINT

    def test_create_new_customer(self):
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"added": "1"})
        # Try to duplicate customer
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "customer with this telephone already exists.",
            },
        )

    def test_create_customer_with_invalid_fields(self):
        self.test_customer_1["invalid"] = "field"
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "'invalid' is an invalid keyword argument for Customer",
            },
        )
        del self.test_customer_1["invalid"]

    def test_create_customer_with_invalid_data_type(self):
        invalid_data_type = 12
        response = self.client.post(
            "/customers/new",
            json=invalid_data_type,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Request data has to be a valid JSON object.",
            },
        )

    def test_create_customer_with_missing_required_fields(self):
        customer_missing_fields = {}
        response = self.client.post(
            "/customers/new",
            json=customer_missing_fields,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "firstname of customer cannot be empty.",
            },
        )

    def test_create_customer_with_invalid_nip(self):
        self.test_customer_1["nip"] = "6666666667"
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Modulo checksum failed. You provided Invalid NIP Number.",
            },
        )
        self.test_customer_1["nip"] = "6666666666"

    def test_create_customer_with_invalid_nip_length(self):
        self.test_customer_1["nip"] = "666666666"
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Valid NIP Number has exactly ten digits, the one you passed has [9].",
            },
        )
        self.test_customer_1["nip"] = "6666666666"

    def test_create_customer_with_nip_containing_charachters(self):
        self.test_customer_1["nip"] = "666666666r"
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Valid NIP Number only consists of digits.",
            },
        )
        self.test_customer_1["nip"] = "6666666666"

    def test_create_customer_with_invalid_telephone_length(self):
        self.test_customer_1["telephone"] = "3333333"
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Valid telephone number has exactly nine digits, the one you passed has [7].",
            },
        )
        self.test_customer_1["telephone"] = "777888999"

    def test_create_customer_with_telephone_containing_charachters(self):
        self.test_customer_1["telephone"] = "33333333r"
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Valid telephone number only consists of digits.",
            },
        )
        self.test_customer_1["telephone"] = "777888999"

    def test_create_customer_with_invalid_postal_code_format(self):
        self.test_customer_1["postal_code"] = "777-43"
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Provided postal code does not comply with the valid format [XX-XXX] where X stands for a digit.",
            },
        )
        self.test_customer_1["postal_code"] = "83-050"

    def test_create_customer_with_empty_postal_code(self):
        self.test_customer_1["postal_code"] = ""
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Provided postal code does not comply with the valid format [XX-XXX] where X stands for a digit.",
            },
        )

    def test_create_customer_with_invalid_attribute_type(self):
        self.test_customer_1["street"] = 12
        response = self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Field [street] has to be a string, not [int].",
            },
        )
        self.test_customer_1["street"] = "Wiejska 12"

    def test_get_all_customers(self):
        self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.client.post(
            "/customers/new",
            json=self.test_customer_2,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.get(
            "/customers/", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(), [self.test_customer_1, self.test_customer_2]
        )

    def test_get_customer_by_valid_id(self):
        self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.get(
            "/customers/1", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.test_customer_1)

    def test_get_customer_by_invalid_id(self):
        response = self.client.get(
            "/customers/999999", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "resource not found"})

    # PRODUCT ENDPOINT

    def test_add_new_product(self):
        response = self.client.post(
            "/products/new",
            json=self.test_product_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"added": "1"})
        # Try to add a duplicated product
        response = self.client.post(
            "/products/new",
            json=self.test_product_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "product with this serial_number already exists.",
            },
        )

    def test_get_all_products(self):
        response = self.client.post(
            "/products/new",
            json=self.test_product_1,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.post(
            "/products/new",
            json=self.test_product_2,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.get(
            "/products/", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(), [self.test_product_1, self.test_product_2]
        )

    def test_get_product_by_factory_number(self):
        response = self.client.post(
            "/products/new",
            json=self.test_product_1,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.get(
            "/products/kas123", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.test_product_1)

    def test_get_product_by_invalid_factory_number(self):
        response = self.client.get(
            "/products/99999999asd", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "resource not found"})

    def test_add_product_with_missing_fields(self):
        del self.test_product_2["name"]
        response = self.client.post(
            "/products/new",
            json=self.test_product_2,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Bad Request", "message": "name of product cannot be empty."},
        )
        self.test_product_2["name"] = "Terminal"

    def test_add_product_with_invalid_date_format(self):
        self.test_product_2["last_service"] = "zla data"
        response = self.client.post(
            "/products/new",
            json=self.test_product_2,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Bad Request", "message": "Invalid isoformat string: 'zla data'"},
        )
        self.test_product_2["last_service"] = "2020-10-28 21:49:22.922116"

    def test_add_product_with_invalid_price(self):
        self.test_product_2["price"] = "zla cena"
        response = self.client.post(
            "/products/new",
            json=self.test_product_2,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Bad Request", "message": "Price has to be a decimal number."},
        )
        self.test_product_2["price"] = "35000"

    def test_add_product_with_invalid_price_type(self):
        self.test_product_2["price"] = {}
        response = self.client.post(
            "/products/new",
            json=self.test_product_2,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Field price has to be a string, not dict.",
            },
        )
        self.test_product_2["price"] = "35000"

    def test_add_a_new_service(self):
        response = self.client.post(
            "/services/new",
            json=self.test_service_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(), {"added": "1"}
        )  # Try to add a duplicated service
        response = self.client.post(
            "/services/new",
            json=self.test_service_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Bad Request", "message": "service with this id already exists."},
        )

    def test_get_all_services(self):
        self.client.post(
            "/services/new",
            json=self.test_service_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.client.post(
            "/services/new",
            json=self.test_service_2,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.get(
            "/services/", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(), [self.test_service_1, self.test_service_2]
        )

    def test_get_service_by_id(self):
        self.client.post(
            "/services/new",
            json=self.test_service_1,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.get(
            "/services/1", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), self.test_service_1)

    def test_get_product_by_invalid_id(self):
        response = self.client.get(
            "/services/4", headers=self.get_headers(self.email, self.password)
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "resource not found"})

    def test_add_service_with_missing_fields(self):
        del self.test_service_2["name"]
        response = self.client.post(
            "/services/new",
            json=self.test_service_2,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Bad Request", "message": "name of service cannot be empty."},
        )
        self.test_service_2["name"] = "Serwis"

    def test_add_product_with_invalid_rate(self):
        self.test_service_2["rate"] = "zla cena"
        response = self.client.post(
            "/services/new",
            json=self.test_service_2,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Bad Request", "message": "Rate has to be a decimal number."},
        )
        self.test_service_2["rate"] = "5000"

    def test_add_product_with_invalid_rate_type(self):
        self.test_service_2["rate"] = {}
        response = self.client.post(
            "/services/new",
            json=self.test_service_2,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {
                "error": "Bad Request",
                "message": "Field rate has to be a string, not dict.",
            },
        )
        self.test_service_2["rate"] = "5000"

    def test_add_new_field_call(self):
        self.client.post(
            "/services/new",
            json=self.test_service_1,
            headers=self.get_headers(self.email, self.password),
        )
        self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.post(
            "/field-calls/new",
            json=self.test_field_call,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"added": "1"})
        response = self.client.get(
            "/field-calls/1",
            json=self.test_field_call,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "comments": "Wycieczka do klienta",
                "customer": "/customers/1",
                "date": "Fri, 30 Oct 2020 21:49:22 GMT",
                "engineer": "/engineers/1",
                "id": 1,
                "invoiced": False,
                "payment_type": "Gotówka",
                "service": "/services/1",
                "settled": False,
                "total": 30000,
            },
        )
        response = self.client.post(
            "/field-calls/new",
            json=self.test_field_call,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"added": "1"})

    def test_create_new_contract(self):
        self.client.post(
            "/customers/new",
            json=self.test_customer_1,
            headers=self.get_headers(self.email, self.password),
        )
        response = self.client.post(
            "/contracts/new",
            json=self.test_contract,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"added": "1"})
        response = self.client.get(
            "/contracts/1",
            json=self.test_field_call,
            headers=self.get_headers(self.email, self.password),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "id": 1,
                "account_number": "111122223333444455556666",
                "signed_on": "Fri, 30 Oct 2020 21:49:22 GMT",
                "expires_on": "Sat, 30 Oct 2021 21:49:22 GMT",
                "customer": "/customers/1",
            },
        )