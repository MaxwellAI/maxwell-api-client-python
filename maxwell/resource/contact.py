from marshmallow import fields, Schema

from maxwell.resource.base import Resource


class Contact(Resource):
    _path = "contacts"
    _include_fields = ["id"]

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


class Contacts(Resource):
    _path = "contacts"
    _resource = Contact
