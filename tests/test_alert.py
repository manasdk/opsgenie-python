import json
import random
import unittest
import uuid

import fauxfactory
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
            self.assertEqual(alert_response["status"], "successful")
            self.assertEqual(len(requests_mock.calls), 1)
            alert_request = json.loads(requests_mock.calls[0].request.body)
            check_request_vals = {
                "message":test_message
            }
            for request_key, request_value in check_request_vals.items():
                self.assertEqual(alert_request[request_key], request_value)

    def test_list(self):
        fake_alerts_list = [self.generate_fake_alert() for x in range(0, random.randint(0,5))]
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.GET,
                "https://api.opsgenie.com/v1/json/alert",
                body=json.dumps({
                    "alerts":fake_alerts_list
                    })
                status=200,
                content_type="application/json"
            )
            alerts_response = self.api.get_resource("alert").list()
            alerts_list = alerts_response["alerts"]
            self.assertEqual(len(requests_mock.calls), 1)
            self.assertEqual(alerts, fake_alerts_list)

    def generate_fake_alert(self, **set_values):
        alert = {
            "id":str(uuid.uuid4()),
            #No tinyId because you have no good reason to want that
            "message":fauxfactory.gen_string("alphanumeric", random.randint(1,130)),
            "alias":fauxfactory.gen_string("alphanumeric", random.randint(1,30)),
            "description":fauxfactory.gen_string("alphanumeric", random.randint(1,15000)),
            "recipients":[fauxfactory.gen_string("alphanumeric", random.randint(1,30)) 
                for x in range(0, random.randint(0,5))],
            #No actions at this time check back later
            "source":fauxfactory.gen_string("alphanumeric", random.randint(1,30)),
            "tags":",".join([fauxfactory.gen_string("alphanumeric", random.randint(1,30))
                for x in range(0, random.randint(0,5))],
            "details":{fauxfactory.gen_string("alphanumeric", random.randint(1,30), 
                fauxfactory.gen_string("alphanumeric", random.randint(1,30) for x in range(
                    0, random.randint(0,5))},
            "entity":fauxfactory.gen_string("alphanumeric", random.randint(1,30)),
            "user":fauxfactory.gen_string("alphanumeric", random.randint(1,30)),
            "note":fauxfactory.gen_string("alphanumeric", random.randint(1,30))
        }
        for set_key, set_val in set_values.items():
            alert[sey_key] = set_val
        return alert
        
