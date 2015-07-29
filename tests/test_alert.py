import json
import random
import unittest
import urllib
import uuid

import fauxfactory
import responses

from opsgenie.api import OpsGenieAPI

class TestAlertResource(unittest.TestCase):
    def setUp(self):
        self.api = OpsGenieAPI("fake-api-key")
        self.resource = self.api.get_resource("alert")

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
            alert_response = self.resource.create(test_message)
            self.assertEqual(alert_response["status"], "successful")
            self.assertEqual(len(requests_mock.calls), 1)
            alert_request = json.loads(requests_mock.calls[0].request.body)
            check_request_vals = {
                "message":test_message
            }
            for request_key, request_value in check_request_vals.items():
                self.assertEqual(alert_request[request_key], request_value)

    def test_update(self):
        alert_id = str(uuid.uuid4())
        response_body = json.dumps(
            {'message': 'alert created', 'code': 200, 'status': 'successful', 
            'alertId': alert_id, 'took': 126})
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.POST,
                "https://api.opsgenie.com/v1/json/alert",
                body=response_body,
                status=200,
                content_type="application/json"
            )
            new_message = fauxfactory.gen_string("alphanumeric", random.randint(1,130))
            update_result = self.resource.update(id=alert_id, message=new_message)
            self.assertEquals(update_result["alertId"], alert_id)
            alert_request = json.loads(requests_mock.calls[0].request.body)
            self.assertEquals(alert_request["id"], alert_id)
            self.assertEquals(alert_request["message"], new_message)

    def test_update_id_error(self):
        with self.assertRaises(ValueError):
            self.resource.update(message="no id specified")

    def test_get(self):
        fake_alert = self.generate_fake_alert()
        alert_id = fake_alert["id"]
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.GET,
                "https://api.opsgenie.com/v1/json/alert",
                body=json.dumps(fake_alert),
                status=200,
                content_type="application/json"
            )
            alert_result = self.resource.get(id=alert_id)
            alert_request = requests_mock.calls[0].request
            query_string = urllib.parse.urlparse(alert_request.path_url).query
            request_params = urllib.parse.parse_qs(query_string)
            self.assertEqual(request_params["id"][0], alert_id)
            for alert_key, alert_val in fake_alert.items():
                self.assertEqual(alert_result[alert_key], alert_val)

    def test_get_id_error(self):
        with self.assertRaises(ValueError):
            self.resource.get()
            
    def test_list(self):
        fake_alerts_list = [self.generate_fake_alert() for x in range(0, random.randint(0,5))]
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.GET,
                "https://api.opsgenie.com/v1/json/alert",
                body=json.dumps({
                    "alerts":fake_alerts_list
                    }),
                status=200,
                content_type="application/json"
            )
            alerts_response = self.api.get_resource("alert").list(status="unacked")
            alerts_request = requests_mock.calls[0].request
            self.assertEqual(len(requests_mock.calls), 1)
            query_string = urllib.parse.urlparse(alerts_request.path_url).query
            request_params = urllib.parse.parse_qs(query_string)
            self.assertEqual(request_params["status"][0], "unacked")
            self.assertEqual(alerts_response, fake_alerts_list)

    def test_list_id_error(self):
        with self.assertRaises(ValueError):
            self.resource.list(id=str(uuid.uuid4()))

    def test_assign(self):
        fake_id = str(uuid.uuid4())
        fake_owner = fauxfactory.gen_string("alphanumeric", random.randint(1,30))
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.POST,
                "https://api.opsgenie.com/v1/json/alert/assign",
                body=json.dumps({"status":"successful", "code":200}),
                status=200,
                content_type="application/json"
            )
            assign_result = self.resource.assign(fake_owner, alertId=fake_id)
            self.assertEqual(len(requests_mock.calls), 1)
            assign_request = requests_mock.calls[0].request
            request_body = json.loads(assign_request.body)
            self.assertEqual(request_body["alertId"], fake_id)
            self.assertEqual(request_body["owner"], fake_owner)
            self.assertEqual(assign_result["status"], "successful")

    def test_assign_id_error(self):
        with self.assertRaises(ValueError):
            self.resource.assign("not a real owner")

    def test_renotify(self):
        fake_id = str(uuid.uuid4())
        fake_note = fauxfactory.gen_string("alphanumeric", random.randint(1,30))
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.POST,
                "https://api.opsgenie.com/v1/json/alert/renotify",
                body=json.dumps({"status":"successful", "code":200}),
                status=200,
                content_type="application/json"
            )
            renotify_result = self.resource.renotify(alertId=fake_id, note=fake_note)
            self.assertEqual(len(requests_mock.calls), 1)
            renotify_request = requests_mock.calls[0].request
            request_body = json.loads(renotify_request.body)
            self.assertEqual(request_body["alertId"], fake_id)
            self.assertEqual(request_body["note"], fake_note)
            self.assertEqual(renotify_result["status"], "successful")

    def test_notify_id_error(self):
        with self.assertRaises(ValueError):
            self.resource.renotify(tinyId=1234)

    def test_add_recipient(self):
        fake_id = str(uuid.uuid4())
        fake_recipient = fauxfactory.gen_string("alphanumeric", random.randint(1,30))
        fake_note = fauxfactory.gen_string("alphanumeric", random.randint(1,30))
        with responses.RequestsMock() as requests_mock:
            requests_mock.add(
                requests_mock.POST,
                "https://api.opsgenie.com/v1/json/alert/recipient",
                body=json.dumps({"status":"successful", "code":200}),
                status=200,
                content_type="application/json"
            )
            add_recipient_result = self.resource.add_recipient(fake_recipient, alertId=fake_id, note=fake_note)
            self.assertEqual(len(requests_mock.calls), 1)
            add_recipient_request = requests_mock.calls[0].request
            request_body = json.loads(add_recipient_request.body)
            self.assertEqual(request_body["alertId"], fake_id)
            self.assertEqual(request_body["note"], fake_note)
            self.assertEqual(request_body["recipient"], fake_recipient)
            self.assertEqual(add_recipient_result["status"], "successful")

    def test_add_recipient_id_error(self):
        with self.assertRaises(ValueError):
            self.resource.add_recipient("foo", tinyId=1234)
            
        
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
                for x in range(0, random.randint(0,5))]),
            "details":{fauxfactory.gen_string("alphanumeric", random.randint(1,30)): 
                fauxfactory.gen_string("alphanumeric", random.randint(1,30)) for x in range(
                    0, random.randint(0,5))},
            "entity":fauxfactory.gen_string("alphanumeric", random.randint(1,30)),
            "user":fauxfactory.gen_string("alphanumeric", random.randint(1,30)),
            "note":fauxfactory.gen_string("alphanumeric", random.randint(1,30))
        }
        for set_key, set_val in set_values.items():
            alert[sey_key] = set_val
        return alert

        
