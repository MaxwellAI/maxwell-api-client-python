import json
import re
from unittest import mock

import maxwell
from maxwell.resource.channel import Channel
from maxwell.resource.contact import Contact
from maxwell.resource.dashboard import Dashboard
from maxwell.resource.team import Team
from maxwell.resource.user import User


RULES = {
    "2.0/teams": '{"teams": [{"id": "aaaaaaaaaaaaaaaaaaaaaaaa", "name": "Maxwell"}]}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}": '{"id": "aaaaaaaaaaaaaaaaaaaaaaaa", "name": "Maxwell"}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}/channels": '{"channels": [{"platform": "facebook", "external_id": "123"}]}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}/channels/facebook/[0-9]+": '{"platform": "facebook", "external_id": "123"}',  # noqa: E501
    r"2.0/teams/id/[a-z0-f]{24}/analytics/dashboards": '{"dashboards": [{"id": "bbbbbbbbbbbbbbbbbbbbbbbb", "title": "default"}]}',  # noqa: E501
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

    def test_team_channels_get(self):
        result = self.client.Teams.list()[0].Channels.get("facebook", "123")
        assert result == Channel(platform="facebook", external_id="123")

    def test_team_channel_contacts_list(self):
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

    def test_team_channel_contacts_get(self):
        result = (
            self.client.Teams.list()[0]
            .Channels.get("facebook", "123")
            .Contacts.get("123123123123123123123123")
        )
        assert result == Contact(
            id="123123123123123123123123", first_name="J", last_name="D"
        )

    def test_team_dashboards_list(self):
        result = self.client.Teams.list()[0].Dashboards.list()
        assert result == [
            Dashboard(id="bbbbbbbbbbbbbbbbbbbbbbbb", title="default")
        ]
