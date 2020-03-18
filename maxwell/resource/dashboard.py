from maxwell.resource.base import Resource, ListResource
from maxwell.resource.report import Reports


class Dashboard(Resource):
    _depth = 1

    def __init__(
        self, id=None, title=None, client=None, parent=None, **kwargs,
    ):
        super().__init__(client, parent, id=id)
        self.id = id
        self.title = title
        self._reports = None

    @property
    def Reports(self):
        return self._child_object(Reports)


class Dashboards(ListResource):
    _path = "analytics/dashboards"
    _slug = "dashboards"
    _resource_class = Dashboard
    _depth = 2
