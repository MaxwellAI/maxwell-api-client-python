from maxwell.model.base import Model


class BaseResource:
    _levels = None

    def __init__(self, client, parent=None, **path_parameters):
        self._client = client
        self._parent = parent
        if path_parameters:
            self._path = self._get_path(**path_parameters)

    def _request(self, path, method="get", *args, **kwargs):
        version = self._get_version()
        return self._client._request(
            method=method, path=path, api_version=version, *args, **kwargs
        )

    @classmethod
    def _get_path(cls, **parameters):
        """
        Returns the relative, formatted path for a resource.
        """
        if parameters:
            if all([p is not None for p in parameters.values()]):
                return cls._path.format(**parameters)
        return cls._path

    def _get_full_path(self, **parameters):
        paths = [self._get_path(**parameters)]
        root = self._get_root_path()
        if root:
            paths.insert(0, root)
        return "/".join(paths)

    def _get_root_path(self):
        parent = self._parent if hasattr(self, "_parent") else None
        levels = self._levels
        paths = []
        while parent is not None and (levels is None or levels > 0):
            paths.insert(0, parent._path)
            if levels is not None:
                levels -= 1
            if hasattr(parent, "_parent"):
                parent = parent._parent
        return "/".join(paths)

    def _get_version(self):
        return (
            self._version
            if hasattr(self, "_version")
            else self._client.DEFAULT_VERSION
        )


class ListResource(BaseResource):
    def create(self, obj):
        obj._parent = self
        obj._client = self._client
        path = self._get_full_path()
        response = self._request(path=path, method="post", data=obj._data)
        obj.id = response["id"]
        return obj

    def get(self, id=None, **parameters):
        if id is not None:
            parameters["id"] = id
        resource = self._resource_class(
            client=self._client, parent=self, **parameters
        )
        path = (
            f"{resource._get_root_path()}/{resource._get_path(**parameters)}"
        )
        for key, value in self._request(path=path).items():
            setattr(resource, key, value)
        return resource

    def list(self):
        path = self._get_full_path()
        response = self._request(path=path)[getattr(self, "_slug", self._path)]
        return [
            self._resource_class(client=self._client, parent=self, **item)
            for item in response
        ]


class Resource(BaseResource, Model):
    _path = "id/{id}"
