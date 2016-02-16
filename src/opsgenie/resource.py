from six.moves.urllib.parse import urljoin


class BaseResource:
    """Provides a common base for resource classes

    Resources inheriting this must set self.path and self.api
    """
    path = None
    api = None

    def _get(self, params={}, path=None, append_path=None, process_opts={}):
        if append_path is not None:
            path = self.append_path(append_path)
        if path is None:
            path = self.get_path()
        return self.get_api().get(path, params=params, process_opts=process_opts)

    def _post(self, body_dict, path=None, append_path=None, process_opts={}):
        if append_path is not None:
            path = self.append_path(append_path)
        if path is None:
            path = self.get_path()
        return self.get_api().post(path, body_dict, process_opts=process_opts)

    def get_path(self):
        if self.path is None:
            raise NotImplementedError
        return self.path

    def append_path(self, addition):
        return "{0}/{1}".format(self.get_path(), addition)

    def get_api(self):
        if self.api is None:
            raise NotImplementedError
        return self.api
