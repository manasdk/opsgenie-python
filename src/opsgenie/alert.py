from .resource import BaseResource

class AlertResource(BaseResource):
    id_params = ["id", "alias", "tinyId"]
    
    #Opsgenie uses inconsisten naming  /sigh
    alert_id_params = ["alertId", "alias"]

    def __init__(self, opsgenie_api):
        self.api = opsgenie_api
        self.path = "/alert"

    def create(self, message, **optional_create_params):
        id_param = self.contains_id_param(optional_create_params)
        if id_param is not None:
            raise ValueError("You specified the ID parameter '{0}'.  This will cause"
                "the API to update the specified alert instead of creating one.  Did you mean to"
                "call {1}.update() instead?".format(id_param, self.__class__.__name__))
        alert_dict = optional_create_params
        alert_dict["message"] = message
        response_body = self._post(alert_dict)
        return response_body

    def update(self, **update_params):
        """Update an alert"""
        if not self.contains_id_param(update_params):
            raise ValueError("You must specify one of the identifier parameters: {0}"
                "  Did you mean to call {1}.create() instead?".format(
                self.id_params, self.__class__.__name__))
        return self._post(update_params)

    def get(self, **get_params):
        """Get a singe alert."""
        if not self.contains_id_param(get_params):
            raise ValueError("You must specify one of the identifier parameters: {0}"
                "  Did you mean to call {1}.list() instead?".format(
                self.id_params, self.__class__.__name__))
        return self._get(params=get_params)

    def list(self, **optional_params):
        """Get a list of alerts.

        Unpacks the result for you, returning a list of alerts.
        """
        id_param = self.contains_id_param(optional_params)
        if id_param is not None:
            raise ValueError("You specified the ID parameter '{0}'.  This will cause"
                "the API to return a single alert and not a list.  Did you mean to"
                "call {1}.get() instead?".format(id_param, self.__class__.__name__))
        alerts_response = self._get(params=optional_params)
        return alerts_response["alerts"]

    def assign(self, owner, **params):
        self.raise_no_alert_id(params)
        params["owner"] = owner
        return self._post(params, append_path = "assign")

    def renotify(self, **params):
        self.raise_no_alert_id(params)
        return self._post(params, append_path = "renotify")

    def contains_alert_id_param(self, params):
        return self.contains_id_param(params, available=self.alert_id_params)

    def contains_id_param(self, params, available=None):
        if available is None:
            available = self.id_params
        for need_param in available:
            if need_param in params:
                return need_param
        return None

    def raise_no_alert_id(self, params):
        if not self.contains_alert_id_param(params):
            raise ValueError("You must specify one of the available ID params: {0}".format(
                self.alert_id_params))

