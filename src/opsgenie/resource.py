class BaseResource:
    """Provides a common base for resource classes
    
    Resources inheriting this must set self.path and self.api
    """
    path = None
    api = None

    def _get(self, params={}, **kwargs):
        return self.get_api().get(self.get_path(), params=params, **kwargs)

    def _post(self, body_dict, **kwargs):
        return self.get_api().post(self.get_path(), body_dict, **kwargs)

    def get_path(self):
        if self.path is None:
            raise NotImplementedError
        return self.path

    def get_api(self):
        if self.api is None:
            raise NotImplementedError
        return self.api
