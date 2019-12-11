from maxwell.resource.base import Resource, ListResource


class Report(Resource):
    _path = "analytics/reports/id/{id}"

    REPORT_TYPES = ("table", "bar", "line")

    def __init__(
        self,
        id=None,
        title=None,
        type=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent)
        assert type in self.REPORT_TYPES
        self.id = id
        self.title = title
        self.type = type
        self._update_path_with_parameters()


class Reports(ListResource):
    _path = "reports"
    _resource = Report
    _slug = "reports"
