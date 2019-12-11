from maxwell.resource.base import Resource, ListResource
from maxwell.resource.report import Reports


class Dashboard(Resource):
    _path = "analytics/dashboards/id/{id}"

    def __init__(
        self, id=None, title=None, client=None, parent=None, **kwargs,
    ):
        super().__init__(client, parent)
        self.id = id
        self.title = title
        self._reports = None
        self._update_path_with_parameters()

    @property
    def Reports(self):
        if self._reports is None:
            self._reports = Reports(self._client, self)
        return self._reports


class Dashboards(ListResource):
    _path = "analytics/dashboards"
    _resource = Dashboard
    _slug = "dashboards"
