from maxwell.model.base import Model


class BaseResource(Model):
    def __init__(self, client, parent=None):
        self._client = client
        self._parent = parent

    def _request(
        self, path=None, method="get", *args, **kwargs,
    ):
        fullpath = self._get_fullpath()
        if path:
            fullpath = f"{fullpath}/{path}"
        version = self._get_version()
        return self._client._request(
            method=method, path=fullpath, api_version=version, *args, **kwargs
        )

    def _get_fullpath(self, **parameters):
        paths = [self._get_path(**parameters)]
        if self._parent is not None:
            paths.insert(0, self._parent._get_path())
        return "/".join(paths)

    def _get_path(self, **parameters):
        return self._path.format(**parameters)

    def _get_version(self):
        return (
            self._version
            if hasattr(self, "_version")
            else self._client.DEFAULT_VERSION
        )


class ListResource(BaseResource):
    def create(self, obj):
        obj._client = self._client
        obj._parent = self._parent
        obj.id = self._request(method="post", data=obj._data)["id"]
        return obj

    def get(self, id):
        return self._resource(
            client=self._client,
            parent=self._parent,
            **self._request(f"id/{id}"),
        )

    def list(self):
        return [
            self._resource(client=self._client, parent=self._parent, **item)
            for item in self._request()[
                getattr(self, "_slug", self._get_path())
            ]
        ]


class Resource(BaseResource):
    pass
