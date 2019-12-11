from maxwell.resource.base import Resource, ListResource
from maxwell.resource.contact import Contacts
from maxwell.resource.conversation import Conversations
from maxwell.resource.persistent_menu import PersistentMenu
from maxwell.resource.whitelisted_domains import WhitelistedDomains


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
        self._persistent_menu = None
        self._whitelisted_domains = None
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

    @property
    def PersistentMenus(self):
        if self._persistent_menu is None:
            self._persistent_menu = PersistentMenu(
                client=self._client, parent=self
            )
        return self._persistent_menu

    @property
    def WhitelistedDomains(self):
        if self._whitelisted_domains is None:
            self._whitelisted_domains = WhitelistedDomains(self._client, self)
        return self._whitelisted_domains


class Channels(ListResource):
    _path = "channels"
    _resource = Channel

    def get(self, platform, external_id):
        return self._resource(
            client=self._client,
            parent=self._parent,
            **self._request(f"{platform}/{external_id}"),
        )
