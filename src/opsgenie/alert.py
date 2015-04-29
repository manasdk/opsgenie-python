import weakref

class AlertResource:
    def __init__(self, opsgenie_api):
        self.api = opsgenie_api
        self.path = "alert"

    def create(self, message, **optional_create_params):
        alert_dict = optional_create_params
        alert_dict["message"] = message
        response_body = self._post(alert_dict)
        return response_body

    def _post(self, body_dict, **kwargs):
        return self.api.post(self.path, body_dict, **kwargs)
