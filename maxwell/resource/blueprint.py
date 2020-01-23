from marshmallow import fields, Schema

from maxwell.resource.base import Resource, ListResource
from maxwell.resource.revision import Revisions


class Blueprint(Resource):
    _depth = 1

    def __init__(self, name=None, id=None, client=None, parent=None, **kwargs):
        super().__init__(client, parent, id=id)
        self.id = id
        self.name = name
        self._revisions = None

    @property
    def Revisions(self):
        if self._revisions is None:
            self._revisions = Revisions(self._client, self)
        return self._revisions


class BlueprintSchema(Schema):
    id = fields.Str(allow_none=True)
    name = fields.Str()


class Blueprints(ListResource):
    _path = "blueprints"
    _resource_class = Blueprint
