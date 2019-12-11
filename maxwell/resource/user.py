from maxwell.resource.base import Resource, ListResource
from maxwell.resource.channel import Channels


class User(Resource):
    _path = "customers"

    def __init__(
        self,
        id,
        first_name,
        last_name,
        email,
        picture,
        client=None,
        parent=None,
    ):
        super().__init__(client, parent)
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.picture = picture
        self._channels = None

    @property
    def Channels(self):
        if self._channels is None:
            self._channels = Channels(self._client, self)
        return self._channels


class Users(ListResource):
    _path = "customers"

    def get(self):
        return User(
            client=self._client,
            parent=self._parent,
            **self._request(path="profile"),
        )

    def login(self, username, password):
        return self._request(
            method="post",
            path="users/login",
            data={
                "identity_provider": "password",
                "username": username,
                "password": password,
            },
        )["access_token"]
