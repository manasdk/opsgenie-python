from .resource import BaseResource

class AlertResource(BaseResource):
    def __init__(self, opsgenie_api):
        self.api = opsgenie_api
        self.path = "alert"

    def create(self, message, **optional_create_params):
        alert_dict = optional_create_params
        alert_dict["message"] = message
        response_body = self._post(alert_dict)
        return response_body

    def list(self, **optional_params):
        return self._get(params=optiona_params)
