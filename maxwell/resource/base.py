from maxwell.model.base import Model


class Resource(Model):
    def __init__(self, client, parent=None):
        self._client = client
        self._parent = parent

    def _fullpath(self, subpath=None):
        paths = [self._path]
        if self._parent is not None and not (subpath or "").startswith("id/"):
            paths.insert(0, self._parent._path)
        if subpath is not None:
            paths.append(subpath)
        return "/".join(paths)

    def _update_path_with_parameters(self, **kwargs):
        if not kwargs:
            if self.id is not None:
                self._path = self._path.format(id=self.id)
        else:
            self._path = self._path.format(**kwargs)

    def _request(
        self, subpath=None, fullpath=None, method="get", *args, **kwargs
    ):
        path = self._fullpath(subpath) if fullpath is None else fullpath
        version = (
            self._version
            if hasattr(self, "_version")
            else self._client.DEFAULT_VERSION
        )
        return self._client._request(
            method=method, path=path, api_version=version, *args, **kwargs
        )

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
            for item in self._request()[getattr(self, "_slug", self._path)]
        ]
