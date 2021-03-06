'''tests for all the ednpoints'''
import json
from unittest import TestCase


from app import create_app


class TestOrders(TestCase):
    '''loads the configuration'''
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.order_data = {
            "name": "Burger",
            "description": "Beef burger",
            "price": 60
        }

    def test_place_new_order(self):
        ''' Test to place an order '''
        order_data = {
            "name": "Burger",
            "description": "Beef burger",
            "price": 60}

        response = self.client.post(
            "/api/v1/orders",
            data=json.dumps(order_data),
            headers={"content-type": "application/json"})

        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response_data['message'], "Food order placed", 201)

    def test_name_in_order(self):
        ''' Test to place an order '''
        data = {
            "name": "  ",
            "description": "Beef burger",
            "price": 60
        }

        response = self.client.post(
            "/api/v1/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        response_data = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response_data['message'], "Enter valid name")

    def test_description_in_order(self):
        ''' Test to place an order '''
        data = {
            "name": "Burger",
            "description": " ",
            "price": 60
        }

        response = self.client.post(
            "/api/v1/orders",
            data=json.dumps(data),
            headers={"content-type": "application/json"})

        response_data = json.loads(response.data.decode('utf-8'))

        self.assertTrue(response_data['message'],
                        "Enter valid food description")

    def test_get_all_orders(self):
        ''' Test to get all orders '''
        response = self.client.get(
            "/api/v1/orders",
            content_type='application/json')

        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_get_specififc_order(self):
        ''' Test to get specific order '''

        response = self.client.get(
            "/api/v1/orders/1",
            content_type='application/json')

        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_all_completed_orders(self):
        ''' Test to get all completed orders '''

        response = self.client.get(
            "/api/v1/completed/orders",
            content_type='application/json')

        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_get_all_accepted_orders(self):
        ''' Test to get all accepted orders '''

        response = self.client.get(
            "/api/v1/accepted/orders",
            content_type='application/json')

        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_get_all_declined_orders(self):
        ''' Test to get all declined orders '''

        response = self.client.get(
            "/api/v1/declined/orders",
            content_type='application/json')

        data = json.loads(response.data.decode('utf-8'))
        print(data)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_accept_order(self):
        ''' Test to update a specific order '''
        response = self.client.put(
            "/api/v1/accept/orders/1",
            headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, 200)

    def test_complete_order(self):
        ''' Test to update a specific order '''

        response = self.client.put(
            "/api/v1/complete/orders/1",
            headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_decline_order(self):
        ''' Test to update a specific order '''
        response = self.client.put(
            "/api/v1/decline/orders/1",
            headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)

    def test_invalid_food_name(self):
        ''' Test invalid food name '''

        order_data = {
            "name": "***",
            "description": "Sweet empty food",
            "price": 20
        }

        response = self.client.post(
            "/api/v1/orders",
            data=json.dumps(order_data),
            headers={"content-type": "application/json"}
        )

        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'], "Enter valid name")
        self.assertNotEqual(response.status_code, 200)

    def test_invalid_food_description(self):
        ''' Test invalid food description '''

        order_data = {
            "name": "Validfood",
            "description": "****",
            "price": 20
        }

        response = self.client.post(
            "/api/v1/orders",
            data=json.dumps(order_data),
            headers={"content-type": "application/json"})
        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['message'],
                         "Enter valid food description")
        self.assertNotEqual(response.status_code, 200)

    def test_delete_order(self):
        ''' Test to delete order'''
        response = self.client.delete(
            "/api/v1/orders/1",
            headers={"content-type": "application/json"})
            
        self.assertEqual(response.status_code, 200)

        self.assertNotEqual(response.status_code, 404)

    def tearDown(self):
        self.app_context.pop()
