from marshmallow import fields, Schema

from maxwell.resource.base import Resource
from maxwell.resource.blueprint import BlueprintSchema
from maxwell.resource.contact import ContactSchema


class Conversation(Resource):
    _path = "conversations"

    def __init__(
        self,
        blueprint=None,
        contacts=None,
        context=None,
        id=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent)
        self.id = id
        self.blueprint = blueprint
        self.contacts = contacts
        self.context = context

    @property
    def _data(self):
        exclude = ("id",) if self.id is None else ()
        return ConversationSchema(exclude=exclude).dump(self)


class ConversationSchema(Schema):
    id = fields.Str(allow_none=True)
    blueprint = fields.Nested(BlueprintSchema, only=("id",), allow_none=True)
    contacts = fields.Nested(
        ContactSchema, only=("id",), many=True, allow_none=True
    )
    context = fields.Dict(allow_none=True)


class Conversations(Resource):
    _path = "conversations"
    _resource = Conversation

    def create(self, obj):
        obj._client = self._client
        obj._parent = self._parent
        data = {**obj._data, "blueprint": {"id": obj.blueprint.id}}
        path = f"{obj._parent._fullpath()}/{obj._path}"
        response = self._request(fullpath=path, method="post", data=data)
        return [
            self._resource(**{**obj.__dict__, "id": conversation["id"]})
            for conversation in response["conversations"]
        ]
