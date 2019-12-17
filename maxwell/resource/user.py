from maxwell.resource.base import Resource, ListResource
from maxwell.resource.channel import Channels


class User(Resource):
    _path = "profile"

    def __init__(
        self,
        id=None,
        first_name=None,
        last_name=None,
        email=None,
        picture=None,
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
    _resource_class = User
