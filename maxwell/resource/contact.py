from marshmallow import fields, Schema

from maxwell.resource.base import Resource, ListResource


class Contact(Resource):
    _include_fields = ["id"]
    _depth = 3

    def __init__(
        self,
        id=None,
        first_name=None,
        last_name=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent)
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


class ContactSchema(Schema):
    id = fields.Str(allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)


class Contacts(ListResource):
    _path = "contacts"
    _resource_class = Contact
    _depth = 2
