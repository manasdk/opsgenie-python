import json
import unittest
import uuid

import responses

from opsgenie.api import OpsGenieAPI

class TestAlertResource(unittest.TestCase):
    def setUp(self):
        self.api = OpsGenieAPI("fake-api-key")

    def test_create(self):
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.POST,
                "https://api.opsgenie.com/v1/json/alert",
                body=json.dumps({'message': 'alert created', 'status': 'successful', 'took': 144,
                    'alertId': '3e6cb390-e408-40b5-835b-c4b995a4b4a8', 'code': 200}),
                status=200,
                content_type="application/json"
            )
            test_message = str(uuid.uuid4())
            alert_response = self.api.get_resource("alert").create(test_message)
            self.assertEqual(len(requests_mock.calls), 1)
            alert_request = json.loads(requests_mock.calls[0].request.body)
            check_request_vals = {
                "message":test_message
            }
            for request_key, request_value in check_request_vals.items():
                self.assertEqual(alert_request[request_key], request_value)
            
