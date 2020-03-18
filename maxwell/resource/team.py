from maxwell.resource.base import Resource, ListResource
from maxwell.resource.blueprint import Blueprints
from maxwell.resource.channel import Channels
from maxwell.resource.dashboard import Dashboards
from maxwell.resource.event import Events
from maxwell.resource.invite import Invites
from maxwell.resource.member import Members


class Team(Resource):
    def __init__(self, name=None, id=None, client=None, parent=None, **kwargs):
        super().__init__(client, parent, id=id)
        self.id = id
        self.name = name

    @property
    def Blueprints(self):
        return self._child_object(Blueprints)

    @property
    def Channels(self):
        return self._child_object(Channels)

    @property
    def Dashboards(self):
        return self._child_object(Dashboards)

    @property
    def Events(self):
        return self._child_object(Events)

    @property
    def Invites(self):
        return self._child_object(Invites)

    @property
    def Members(self):
        return self._child_object(Members)


class Teams(ListResource):
    _path = "teams"
    _resource_class = Team
