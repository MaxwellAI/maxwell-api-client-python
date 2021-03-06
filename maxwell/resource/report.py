from marshmallow import fields, post_load, Schema
from marshmallow.validate import OneOf

from maxwell.resource.base import Resource, ListResource
from maxwell.model.base import Model


class ReportQuerySchema(Schema):
    filters = fields.List(fields.Dict(), many=True)
    group = fields.List(fields.Str())
    sort = fields.List(fields.Str())


class ReportQuery(Model):
    def __init__(self, filters=None, group=None, sort=None):
        self.filters = filters
        self.group = group
        self.sort = sort


class Report(Resource):
    REPORT_TYPES = ("table", "bar", "line", "number")
    _depth = 1

    def __init__(
        self,
        id=None,
        title=None,
        type=None,
        query=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent, id=id)
        if type is not None:
            assert type in self.REPORT_TYPES
        self.id = id
        self.title = title
        self.type = type
        self.query = query

    @property
    def _data(self):
        exclude = ("id",) if self.id is None else ()
        return ReportSchema(exclude=exclude).dump(self)


class ReportSchema(Schema):
    id = fields.Str(allow_none=True)
    title = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True, validate=OneOf(Report.REPORT_TYPES))
    query = fields.Nested(ReportQuerySchema, allow_none=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Report(**data)


class ReportsMeta(type):
    @property
    def _path(cls):
        """
        Observe the following inconsistencies between the analytics endpoints:

        /teams/id/aaaaaaaaaaaaaaaaaaaaaaaa/analytics/dashboards
        /analytics/dashboards/id/aaaaaaaaaaaaaaaaaaaaaaaa/reports
        /analytics/reports/id/aaaaaaaaaaaaaaaaaaaaaaaa

        Since `cls._get_path` is a classmethod, calling Reports._get_path()
        will yield `reports` which is what we want for nested endpoints.
        """
        return "reports"


class Reports(ListResource, metaclass=ReportsMeta):
    _path = "analytics/reports"
    _slug = "reports"
    _resource_class = Report
    _depth = 2
