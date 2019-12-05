from maxwell.resource.base import Resource
from maxwell.resource.blueprint import Blueprints
from maxwell.resource.channel import Channels


class Team(Resource):
    _path = "teams/id/{id}"

    def __init__(self, name, id=None, client=None, parent=None, **kwargs):
        super().__init__(client, parent)
        self.id = id
        self.name = name
        self._path = self._path.format(id=id)
        self._channels = None
        self._blueprints = None

    @property
    def Channels(self):
        if self._channels is None:
            self._channels = Channels(self._client, self)
        return self._channels

    @property
    def Blueprints(self):
        if self._blueprints is None:
            self._blueprints = Blueprints(self._client, self)
        return self._blueprints


class Teams(Resource):
    _path = "teams"
    _resource = Team
