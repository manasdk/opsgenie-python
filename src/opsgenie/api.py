from urllib.parse import urljoin

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

    def get_resource(self, resource_name, *args, **kwargs):
        if resource_name not in self.resource_map:
            raise ValueError("{0} is not one of the available resources: {1}".format(
                resource_name, self.resource_map.keys()))
        return self.resource_map[resource_name](self, *args, **kwargs)

    def get_url(self, path):
        if path.startswith("/"):
            path=path[1:]
        path = path.replace("//", "/")
        return urljoin(self.url_base, path)
    
    def get(self, path, params={}, process_opts={}):
        url = self.get_url(path)
        params["apiKey"] = self.api_key
        response = requests.get(url, params=params)
        return self._process_response(response, **process_opts)

    def post(self, path, body_dict, process_opts={}):
        url = self.get_url(path)
        body_dict["apiKey"] = self.api_key
        response = requests.post(url, json=body_dict)
        return self._process_response(response, **process_opts)

    def _process_response(self, response, return_body=True, raise_for_status=True):
        if raise_for_status:
            response.raise_for_status()
        response_body = response.json()
        if return_body:
            return response_body
        else:
            return response



