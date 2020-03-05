from maxwell.resource.base import Resource, ListResource
from maxwell.resource.blueprint import Blueprints
from maxwell.resource.channel import Channels
from maxwell.resource.dashboard import Dashboards
from maxwell.resource.invite import Invites
from maxwell.resource.member import Members


class Team(Resource):
    def __init__(self, name=None, id=None, client=None, parent=None, **kwargs):
        super().__init__(client, parent, id=id)
        self.id = id
        self.name = name
        self._blueprints = None
        self._channels = None
        self._dashboards = None
        self._invites = None
        self._members = None

    @property
    def Blueprints(self):
        if self._blueprints is None:
            self._blueprints = Blueprints(client=self._client, parent=self)
        return self._blueprints

    @property
    def Channels(self):
        if self._channels is None:
            self._channels = Channels(client=self._client, parent=self)
        return self._channels

    @property
    def Dashboards(self):
        if self._dashboards is None:
            self._dashboards = Dashboards(client=self._client, parent=self)
        return self._dashboards

    @property
    def Invites(self):
        if self._invites is None:
            self._invites = Invites(client=self._client, parent=self)
        return self._invites

    @property
    def Members(self):
        if self._members is None:
            self._members = Members(client=self._client, parent=self)
        return self._members


class Teams(ListResource):
    _path = "teams"
    _resource_class = Team
