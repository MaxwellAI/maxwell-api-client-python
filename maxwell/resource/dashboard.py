from maxwell.resource.base import Resource, ListResource
from maxwell.resource.report import Reports


class Dashboard(Resource):
    _levels = 1

    def __init__(
        self, id=None, title=None, client=None, parent=None, **kwargs,
    ):
        super().__init__(client, parent, id=id)
        self.id = id
        self.title = title
        self._reports = None

    @property
    def Reports(self):
        if self._reports is None:
            self._reports = Reports(self._client, self)
        return self._reports


class Dashboards(ListResource):
    _path = "analytics/dashboards"
    _slug = "dashboards"
    _resource_class = Dashboard
    _levels = 2
