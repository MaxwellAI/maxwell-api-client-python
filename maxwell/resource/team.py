from maxwell.resource.base import Resource, ListResource
from maxwell.resource.blueprint import Blueprints
from maxwell.resource.channel import Channels
from maxwell.resource.dashboard import Dashboards


class Team(Resource):
    _path = "teams/id/{id}"

    def __init__(self, name, id=None, client=None, parent=None, **kwargs):
        super().__init__(client, parent)
        self.id = id
        self.name = name
        self._path = self._path.format(id=id)
        self._blueprints = None
        self._channels = None
        self._dashboards = None

    @property
    def Blueprints(self):
        if self._blueprints is None:
            self._blueprints = Blueprints(self._client, self)
        return self._blueprints

    @property
    def Channels(self):
        if self._channels is None:
            self._channels = Channels(self._client, self)
        return self._channels

    @property
    def Dashboards(self):
        if self._dashboards is None:
            self._dashboards = Dashboards(self._client, self)
        return self._dashboards


class Teams(ListResource):
    _path = "teams"
    _resource = Team
