class BaseResource:
    """Provides a common base for resource classes
    
    Resources inheriting this must set self.path
    """
    def _get(self, params={}, **kwargs):
        return self.api.get(self.path, params=params, **kwargs)

    def _post(self, body_dict, **kwargs):
        return self.api.post(self.path, body_dict, **kwargs)
