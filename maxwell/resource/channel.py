from maxwell.resource.base import Resource
from maxwell.resource.contact import Contacts
from maxwell.resource.conversation import Conversations


class Channel(Resource):
    _path = "channels/{platform}/{external_id}"

    def __init__(
        self,
        platform=None,
        external_id=None,
        name=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent)
        self.platform = platform
        self.external_id = external_id
        self.name = name
        self._contacts = None
        self._conversations = None
        self._update_path_with_parameters(
            platform=platform, external_id=external_id
        )

    @property
    def Contacts(self):
        if self._contacts is None:
            self._contacts = Contacts(self._client, self)
        return self._contacts

    @property
    def Conversations(self):
        if self._conversations is None:
            self._conversations = Conversations(self._client, self)
        return self._conversations


class Channels(Resource):
    _path = "channels"
    _resource = Channel

    def get(self, platform, external_id):
        return self._resource(
            client=self._client,
            parent=self._parent,
            **self._request(f"{platform}/{external_id}"),
        )
