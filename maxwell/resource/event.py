from marshmallow import fields, Schema

from maxwell.resource.base import Resource, ListResource
from maxwell.resource.blueprint import BlueprintSchema
from maxwell.resource.channel import ChannelSchema
from maxwell.resource.contact import ContactSchema


class Event(Resource):
    def __init__(
        self,
        name=None,
        data=None,
        blueprint=None,
        channel=None,
        contact=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent)
        self.name = name
        self.data = data
        self.blueprint = blueprint
        self.channel = channel
        self.contact = contact

    @property
    def _data(self):
        return EventSchema().dump(self)


class EventSchema(Schema):
    name = fields.Str(allow_none=True)
    data = fields.Dict(allow_none=True)
    blueprint = fields.Nested(BlueprintSchema, only=("id",), allow_none=True)
    channel = fields.Nested(
        ChannelSchema, only=("platform", "external_id"), allow_none=True
    )
    contact = fields.Nested(ContactSchema, only=("id",), allow_none=True)


class Events(ListResource):
    _path = "events"
    _resource_class = Event

    def create(self, obj):
        obj._client = self._client
        obj._parent = self._parent
        data = {**obj._data, "blueprint": {"id": obj.blueprint.id}}
        return self._request(self._get_full_path(), method="post", data=data)
