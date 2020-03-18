from marshmallow import fields, Schema

from maxwell.resource.base import Resource, ListResource
from maxwell.resource.contact import Contacts
from maxwell.resource.conversation import Conversations
from maxwell.resource.persistent_menu import PersistentMenu
from maxwell.resource.whitelisted_domains import WhitelistedDomains


class Channel(Resource):
    _path = "{platform}/{external_id}"

    def __init__(
        self,
        platform=None,
        external_id=None,
        name=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(
            client, parent, platform=platform, external_id=external_id
        )
        self.platform = platform
        self.external_id = external_id
        self.name = name
        self._contacts = None
        self._conversations = None
        self._persistent_menu = None
        self._whitelisted_domains = None

    @property
    def Contacts(self):
        return self._child_object(Contacts)

    @property
    def Conversations(self):
        return self._child_object(Conversations)

    @property
    def PersistentMenus(self):
        return self._child_object(PersistentMenu)

    @property
    def WhitelistedDomains(self):
        return self._child_object(WhitelistedDomains)


class ChannelSchema(Schema):
    platform = fields.Str(allow_none=True)
    external_id = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)


class Channels(ListResource):
    _path = "channels"
    _resource_class = Channel

    def _get_root_path(self):
        """
        The `customers/channels` endpoint follows a non-standard URL pattern.
        """
        from maxwell.resource.user import User

        if isinstance(self._parent, User):
            return self._parent._parent._path
        return super()._get_root_path()

    def get(self, platform, external_id):
        return super().get(platform=platform, external_id=external_id)

    def add(self, obj):
        obj._client = self._client
        obj._parent = self._parent
        data = {"platform": obj.platform, "external_id": obj.external_id}
        return self._request(
            path=self._get_full_path(), method="post", data=data
        )

    def remove(self, obj):
        obj._client = self._client
        obj._parent = self._parent
        data = {"platform": obj.platform, "external_id": obj.external_id}
        return self._request(
            path=self._get_full_path(), method="delete", data=data
        )
