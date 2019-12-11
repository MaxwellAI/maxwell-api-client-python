from marshmallow import fields, Schema

from maxwell.resource.base import Resource, ListResource
from maxwell.resource.revision import Revisions


class Blueprint(Resource):
    _path = "blueprints/id/{id}"

    def __init__(self, name, id=None, client=None, parent=None, **kwargs):
        super().__init__(client, parent)
        self.id = id
        self.name = name
        self._path = self._path.format(id=id)
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
    _resource = Blueprint
