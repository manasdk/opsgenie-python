import requests

from .alert import AlertResource

class OpsGenieAPI:
    resource_map = {
        "alert":AlertResource
    }

    def __init__(self, api_key, url_base="https://api.opsgenie.com/v1/json/"):
        self.api_key = api_key

        if not url_base.startswith("https"):
            raise ValueError("Seriously?")

        if url_base[-1] != "/":
            url_base += "/"
        self.url_base = url_base

    def get_url(self, path):
        if path.startswith("/"):
            path = path[1:]
        return "{0}{1}".format(self.url_base, path)

    def post(self, path, body_dict, return_body=True, raise_for_status=True):
        url = self.get_url(path)
        body_dict["apiKey"] = self.api_key
        response = requests.post(url, json=body_dict)
        if raise_for_status:
            response.raise_for_status()
        response_body = response.json()
        if return_body:
            return response_body
        else:
            return response

    def get_resource(self, resource_name, *args, **kwargs):
        if resource_name not in self.resource_map:
            raise ValueError("{0} is not one of the available resources: {1}".format(
                resource_name, self.resource_map.keys()))
        return self.resource_map[resource_name](self, *args, **kwargs)
            
