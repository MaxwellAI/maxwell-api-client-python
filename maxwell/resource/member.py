from maxwell.resource.base import Resource, ListResource


class Member(Resource):
    _depth = 1

    def __init__(
        self,
        id=None,
        first_name=None,
        last_name=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent, id=id)
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


class Members(ListResource):
    _path = "members"
    _resource_class = Member
    _depth = 2

    def add(self, obj):
        obj._client = self._client
        obj._parent = self._parent
        data = {"id": obj.id}
        return self._request(
            path=self._get_full_path(), method="post", data=data
        )

    def remove(self, obj):
        obj._client = self._client
        obj._parent = self._parent
        data = {"id": obj.id}
        return self._request(
            path=self._get_full_path(), method="delete", data=data
        )
