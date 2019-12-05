import json
import warnings

import requests

from maxwell.logger import logger
from maxwell.resource.team import Teams
from maxwell.resource.user import Users


__all__ = ["ApiError", "Client", "MaxwellAPIClient", "MaxwellStagingAPIClient"]


def file_or_stdin(input):
    return (
        open(input[1:]).read()
        if isinstance(input, str) and input.startswith("@")
        else input
    )


class ApiError(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"{self.response.status_code}: {self.response.text[:80]}"


class Client(object):
    DEFAULT_TIMEOUT = 60
    DEFAULT_VERSION = "2.0"

    def __init__(self, access_token, base_url="https://api.maxwell.ai/"):
        self._access_token = access_token
        self._base_url = base_url
        self.Users = Users(self)
        self.Teams = Teams(self)

    def _request(
        self,
        method,
        path,
        api_version="2.0",
        headers=None,
        data=None,
        params=None,
        timeout=None,
    ):
        url = "%s/%s/%s" % (
            self._base_url.strip("/"),
            api_version,
            path.strip("/"),
        )
        headers = headers or {
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % self._access_token,
        }
        timeout = timeout or self.DEFAULT_TIMEOUT
        data = json.dumps(data) if data else None
        response = getattr(requests, method)(
            url, headers=headers, data=data, params=params, timeout=timeout
        )
        logger.debug(
            "[%s] %s %s" % (response.status_code, method.upper(), url)
        )

        if not response.ok:
            raise ApiError(response)

        try:
            rv = response.json()
        except json.decoder.JSONDecodeError:
            rv = response.text
        return rv

    def _execute_command(self, command, *args):
        assert command.strip("_") == command
        if not hasattr(self, command):
            commands = "\n".join(
                sorted(
                    [
                        attr
                        for attr in dir(self)
                        if not attr.startswith("_") and attr.islower()
                    ]
                )
            )
            exit(
                '\n"%s" is not valid. Available commands:\n\n%s\n'
                % (command, commands)
            )
        getattr(self, command)(*args)

    def get_customer_profile(self):
        return self._request("get", "customers/profile")

    def list_blueprint_revisions(self, blueprint_id):
        return self._request(
            "get",
            "blueprints/id/%s/revisions" % blueprint_id,
            api_version="1.0",
        )

    def get_blueprint_revision(self, blueprint_id, blueprint_revision_id):
        return self._request(
            "get",
            "blueprints/id/%s/revisions/id/%s"
            % (blueprint_id, blueprint_revision_id),
            api_version="1.0",
        )

    def list_teams(self):
        return self._request("get", "teams")

    def list_team_blueprints(self, team_id):
        return self._request("get", "teams/id/%s/blueprints" % team_id)

    def trigger_blueprint(self, blueprint_id, user_id, channel, context=None):
        return self._request(
            "post",
            "triggers",
            data={
                "blueprint": {"id": blueprint_id},
                "channel": channel,
                "user": {"id": user_id},
                "context": context,
            },
        )

    def list_team_channels(self, team_id):
        return self._request("get", "teams/id/%s/channels" % team_id)

    def add_team_channel(self, team_id, channel):
        return self._request(
            "post", "teams/id/%s/channels" % team_id, data=channel
        )

    def remove_team_channel(self, team_id, channel):
        return self._request(
            "delete", "teams/id/%s/channels" % team_id, data=channel
        )

    def list_team_members(self, team_id):
        return self._request("get", "teams/id/%s/members" % team_id)

    def add_team_member(self, team_id, customer_id):
        data = {"id": customer_id}
        return self._request(
            "post", "teams/id/%s/members" % team_id, data=data
        )

    def remove_team_member(self, team_id, customer_id):
        data = {"id": customer_id}
        return self._request(
            "delete", "teams/id/%s/members" % team_id, data=data
        )

    def get_team_invoice_address(self, team_id):
        return self._request("get", "teams/id/%s/invoice_address" % team_id)

    def create_blueprint(self, team_id, blueprint):
        blueprint = file_or_stdin(blueprint)
        return self._request(
            "post", "teams/id/%s/blueprints" % team_id, data=blueprint
        )

    def create_blueprint_revision(self, blueprint_id, blueprint_revision):
        blueprint_revision = file_or_stdin(blueprint_revision)
        return self._request(
            "post",
            "blueprints/id/%s/revisions" % blueprint_id,
            api_version="1.0",
            data=blueprint_revision,
        )

    def publish_blueprint_revision(self, blueprint_id, blueprint_revision_id):
        return self._request(
            "post",
            "blueprints/id/%s/revisions/id/%s/publish"
            % (blueprint_id, blueprint_revision_id),
            api_version="1.0",
        )


class MaxwellAPIClient(Client):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "'%s' is deprecated. Use 'Client' instead."
            % self.__class__.__name__,
            DeprecationWarning,
        )
        super(MaxwellAPIClient, self).__init__(*args, **kwargs)


class MaxwellStagingAPIClient(MaxwellAPIClient):
    def __init__(self, *args, **kwargs):
        super(MaxwellStagingAPIClient, self).__init__(
            *args, base_url="https://staging.api.maxwell.ai/", **kwargs
        )
