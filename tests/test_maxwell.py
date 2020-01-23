import json
import re
from unittest import mock

import maxwell
from maxwell.resource.channel import Channel
from maxwell.resource.contact import Contact
from maxwell.resource.dashboard import Dashboard
from maxwell.resource.report import Report, ReportQuery
from maxwell.resource.team import Team
from maxwell.resource.user import User


RULES = {
    "2.0/teams": '{"teams": [{"id": "aaaaaaaaaaaaaaaaaaaaaaaa", "name": "Maxwell"}]}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}": '{"id": "aaaaaaaaaaaaaaaaaaaaaaaa", "name": "Maxwell"}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}/channels": '{"channels": [{"platform": "facebook", "external_id": "123"}]}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}/channels/facebook/[0-9]+": '{"platform": "facebook", "external_id": "123"}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}/analytics/dashboards": '{"dashboards": [{"id": "bbbbbbbbbbbbbbbbbbbbbbbb", "title": "default"}]}',  # noqa: E501
    r"2.0/analytics/dashboards/id/[a-z0-f]{24}": '{"id": "bbbbbbbbbbbbbbbbbbbbbbbb", "title": "default"}',  # noqa: E501
    r"2.0/analytics/dashboards/id/[a-z0-f]{24}/reports": '{"reports": [{"id": "bbbbbbbbbbbbbbbbbbbbbbbb", "title": "default", "type": "bar", "query": {"filters": [{"timestamp": {"from": "2018-03-01T09:47:34.478Z"}}, {"event_names": ["message.sent"]}, {"blueprint": {"id": "2df7ff8yu984aa9064e2456"}}], "group": ["event_name"], "sort": ["count", "-timestamp"]}}]}',  # noqa: E501
    r"2.0/analytics/reports/id/[a-z0-f]{24}": '{"id": "bbbbbbbbbbbbbbbbbbbbbbbb", "title": "default", "type": "bar", "query": {"filters": [{"timestamp": {"from": "2018-03-01T09:47:34.478Z"}}, {"event_names": ["message.sent"]}, {"blueprint": {"id": "2df7ff8yu984aa9064e2456"}}], "group": ["event_name"], "sort": ["count", "-timestamp"]}}',  # noqa: E501
    r"2.0/blueprints/id/[a-z0-f]{24}": '{"id": "bbbbbbbbbbbbbbbbbbbbbbbb", "name": "Name"}',  # noqa: E501
    r"2.0/blueprints/id/[a-z0-f]{24}/revisions": '{"blueprint_revisions": []}',  # noqa: E501
    r"2.0/channels/facebook/[0-9]+/contacts": '{"contacts": [{"id": "123123123123123123123123", "first_name": "J", "last_name": "D"}]}',  # noqa: E501
    r"2.0/channels/facebook/[0-9]+/contacts/id/[a-f0-9]{24}": '{"id": "123123123123123123123123", "first_name": "J", "last_name": "D"}',  # noqa: E501
    "2.0/customers/channels": '{"channels": [{"platform": "facebook", "external_id": "123"}]}',  # noqa: E501
    "2.0/customers/profile": '{"id": "bbbbbbbbbbbbbbbbbbbbbbbb", "first_name": "John", "last_name": "Doe", "email": "john@maxwell.ai", "picture": null}',  # noqa: E501
}


def _request(method, url, headers, data, params, timeout):
    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"].startswith("Bearer ")
    status_code = 200
    text = None
    url = url.replace(maxwell.Client.DEFAULT_BASE_URL, "")
    if method == "get":
        for rule, rule_text in RULES.items():
            if re.compile(f"{rule}").fullmatch(url):
                text = rule_text
                break
    try:
        _json = json.loads(text)
    except TypeError:
        _json = None
    response = mock.MagicMock(
        status_code=status_code,
        text=text,
        json=mock.MagicMock(return_value=_json),
    )
    return response


class _requests:
    def get(*a, **k):
        return _request("get", *a, **k)

    def post(*a, **k):
        return _request("post", *a, **k)

    def put(*a, **k):
        return _request("put", *a, **k)

    def delete(*a, **k):
        return _request("delete", *a, **k)


class TestClient:
    def setup(self):
        self.client = maxwell.Client()
        self.client.requests = _requests

    def test_users_get(self):
        result = self.client.Users.get()
        assert result == User(
            id="bbbbbbbbbbbbbbbbbbbbbbbb",
            first_name="John",
            last_name="Doe",
            email="john@maxwell.ai",
            picture=None,
        )

    def test_user_channels_list(self):
        result = self.client.Users.get().Channels.list()
        assert result == [Channel(platform="facebook", external_id="123")]

    def test_teams_list(self):
        result = self.client.Teams.list()
        assert result == [Team(id="a" * 24, name="Maxwell")]

    def test_teams_get(self):
        result = self.client.Teams.get("aaaaaaaaaaaaaaaaaaaaaaaa")
        assert result == Team(id="a" * 24, name="Maxwell")

    def test_team_channels_list(self):
        result = self.client.Teams.list()[0].Channels.list()
        assert result == [Channel(platform="facebook", external_id="123")]

    def test_channels_get(self):
        result = self.client.Teams.list()[0].Channels.get("facebook", "123")
        assert result == Channel(platform="facebook", external_id="123")

    def test_contacts_list(self):
        result = (
            self.client.Teams.list()[0]
            .Channels.get("facebook", "123")
            .Contacts.list()
        )
        assert result == [
            Contact(
                id="123123123123123123123123", first_name="J", last_name="D"
            )
        ]

    def test_contacts_get(self):
        result = (
            self.client.Teams.list()[0]
            .Channels.get("facebook", "123")
            .Contacts.get("123123123123123123123123")
        )
        assert result == Contact(
            id="123123123123123123123123", first_name="J", last_name="D"
        )

    def test_dashboards_list(self):
        result = self.client.Teams.list()[0].Dashboards.list()
        assert result == [
            Dashboard(id="bbbbbbbbbbbbbbbbbbbbbbbb", title="default")
        ]

    def test_dashboards_get(self):
        result = self.client.Teams.list()[0].Dashboards.get("b" * 24)
        assert result == Dashboard(
            id="bbbbbbbbbbbbbbbbbbbbbbbb", title="default"
        )

    def test_reports_list(self):
        result = (
            self.client.Teams.list()[0].Dashboards.get("b" * 24).Reports.list()
        )
        assert result == [
            Report(
                id="bbbbbbbbbbbbbbbbbbbbbbbb",
                title="default",
                type="bar",
                query=ReportQuery(
                    filters=[
                        {"timestamp": {"from": "2018-03-01T09:47:34.478Z"}},
                        {"event_names": ["message.sent"]},
                        {"blueprint": {"id": "2df7ff8yu984aa9064e2456"}},
                    ],
                    group=["event_name"],
                    sort=["count", "-timestamp"],
                ),
            )
        ]

    def test_reports_get(self):
        result = (
            self.client.Teams.list()[0]
            .Dashboards.get("b" * 24)
            .Reports.get("b" * 24)
        )
        assert result == Report(
            id="bbbbbbbbbbbbbbbbbbbbbbbb",
            title="default",
            type="bar",
            query=ReportQuery(
                filters=[
                    {"timestamp": {"from": "2018-03-01T09:47:34.478Z"}},
                    {"event_names": ["message.sent"]},
                    {"blueprint": {"id": "2df7ff8yu984aa9064e2456"}},
                ],
                group=["event_name"],
                sort=["count", "-timestamp"],
            ),
        )


class TestPaths:
    def setup(self):
        self.client = maxwell.Client()
        self.client.requests = _requests

    def test_users_path(self):
        obj = self.client.Users
        assert obj._get_path() == "customers"
        assert obj._get_root_path() == ""
        assert obj._get_full_path() == "customers"

    def test_users_get_path(self):
        obj = self.client.Users.get()
        assert obj._get_path() == "profile"
        assert obj._get_root_path() == "customers"
        assert obj._get_full_path() == "customers/profile"

    def test_user_channels_list_path(self):
        obj = self.client.Users.get().Channels
        assert obj._get_path() == "channels"
        assert obj._get_root_path() == "customers"
        assert obj._get_full_path() == "customers/channels"

    def test_teams_path(self):
        assert self.client.Teams._get_path() == "teams"
        assert self.client.Teams._get_root_path() == ""
        assert self.client.Teams._get_full_path() == "teams"

    def test_team_blueprints_list_path(self):
        obj = self.client.Teams.get("aaaaaaaaaaaaaaaaaaaaaaaa").Blueprints
        assert obj._get_path() == "blueprints"
        assert obj._get_root_path() == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa"
        assert (
            obj._get_full_path()
            == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa/blueprints"
        )

    def test_blueprints_get_path(self):
        parameters = dict(id="123123123123123123123123")
        obj = self.client.Teams.get("aaaaaaaaaaaaaaaaaaaaaaaa").Blueprints.get(
            **parameters
        )
        assert obj._get_path(**parameters) == "id/123123123123123123123123"
        assert obj._get_root_path() == "blueprints"
        assert (
            obj._get_full_path(**parameters)
            == "blueprints/id/123123123123123123123123"
        )

    def test_blueprint_revisions_list_path(self):
        obj = (
            self.client.Teams.get("aaaaaaaaaaaaaaaaaaaaaaaa")
            .Blueprints.get("123123123123123123123123")
            .Revisions
        )
        assert obj._get_path() == "revisions"
        assert obj._get_root_path() == "blueprints/id/123123123123123123123123"
        assert (
            obj._get_full_path()
            == "blueprints/id/123123123123123123123123/revisions"
        )

    def test_team_channels_list_path(self):
        obj = self.client.Teams.get("aaaaaaaaaaaaaaaaaaaaaaaa").Channels
        assert obj._get_path() == "channels"
        assert obj._get_root_path() == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa"
        assert (
            obj._get_full_path()
            == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa/channels"
        )

    def test_team_channels_get_path(self):
        parameters = dict(platform="facebook", external_id="123")
        obj = self.client.Teams.get("aaaaaaaaaaaaaaaaaaaaaaaa").Channels.get(
            **parameters
        )
        assert obj._get_path(**parameters) == "facebook/123"
        assert (
            obj._get_root_path()
            == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa/channels"
        )
        assert (
            obj._get_full_path(**parameters)
            == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa/channels/facebook/123"
        )

    def test_contacts_list_path(self):
        obj = (
            self.client.Teams.get("aaaaaaaaaaaaaaaaaaaaaaaa")
            .Channels.get(platform="facebook", external_id="123")
            .Contacts
        )
        assert obj._get_path() == "contacts"
        assert obj._get_root_path() == "channels/facebook/123"
        assert obj._get_full_path() == "channels/facebook/123/contacts"

    def test_contacts_get_path(self):
        parameters = dict(id="123123123123123123123123")
        obj = (
            self.client.Teams.list()[0]
            .Channels.get(platform="facebook", external_id="123")
            .Contacts.get(**parameters)
        )
        assert obj._get_path(**parameters) == "id/123123123123123123123123"
        assert obj._get_root_path() == "channels/facebook/123/contacts"
        assert (
            obj._get_full_path(**parameters)
            == "channels/facebook/123/contacts/id/123123123123123123123123"
        )

    def test_dashboards_list_path(self):
        obj = self.client.Teams.list()[0].Dashboards
        assert obj._get_path() == "analytics/dashboards"
        assert obj._get_root_path() == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa"
        assert (
            obj._get_full_path()
            == "teams/id/aaaaaaaaaaaaaaaaaaaaaaaa/analytics/dashboards"
        )

    def test_dashboards_get_path(self):
        parameters = dict(id="aaaaaaaaaaaaaaaaaaaaaaaa")
        obj = self.client.Teams.list()[0].Dashboards.get(**parameters)
        assert obj._get_path(**parameters) == "id/aaaaaaaaaaaaaaaaaaaaaaaa"
        assert obj._get_root_path() == "analytics/dashboards"
        assert (
            obj._get_full_path(**parameters)
            == "analytics/dashboards/id/aaaaaaaaaaaaaaaaaaaaaaaa"
        )

    def test_reports_list_path(self):
        parameters = dict(id="aaaaaaaaaaaaaaaaaaaaaaaa")
        obj = self.client.Teams.list()[0].Dashboards.get(**parameters).Reports
        assert obj._get_path(**parameters) == "reports"
        assert (
            obj._get_root_path()
            == "analytics/dashboards/id/aaaaaaaaaaaaaaaaaaaaaaaa"
        )
        assert (
            obj._get_full_path(**parameters)
            == "analytics/dashboards/id/aaaaaaaaaaaaaaaaaaaaaaaa/reports"
        )

    def test_reports_get_path(self):
        parameters = dict(id="aaaaaaaaaaaaaaaaaaaaaaaa")
        obj = (
            self.client.Teams.list()[0]
            .Dashboards.get(**parameters)
            .Reports.get(**parameters)
        )
        assert obj._get_path(**parameters) == "id/aaaaaaaaaaaaaaaaaaaaaaaa"
        assert obj._get_root_path() == "analytics/reports"
        assert (
            obj._get_full_path(**parameters)
            == "analytics/reports/id/aaaaaaaaaaaaaaaaaaaaaaaa"
        )


class TestModels:
    def setup(self):
        self.query = {
            "filters": [
                {"timestamp": {"from": "2018-03-01T09:47:34.478Z"}},
                {"event_names": ["message.sent"]},
                {"blueprint": {"id": "2df7ff8yu984aa9064e2456"}},
            ],
            "group": ["event_name"],
            "sort": ["count", "-timestamp"],
        }

    def test_report(self):
        report = Report(
            id=None,
            title="default",
            type="bar",
            query=ReportQuery(
                filters=self.query["filters"],
                group=self.query["group"],
                sort=self.query["sort"],
            ),
        )
        assert report._data == {
            "title": "default",
            "type": "bar",
            "query": self.query,
        }
