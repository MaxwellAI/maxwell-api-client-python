from maxwell.resource.base import Resource
from maxwell.resource.channel import Channels


class User(Resource):
    _path = "customers"

    def __init__(
        self, client, parent, id, first_name, last_name, email, picture
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


class Users(Resource):
    _path = "customers"

    def get(self):
        return User(self._client, self._parent, **self._request("profile"))
