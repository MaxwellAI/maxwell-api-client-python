import json
import logging
import requests
import terminaltables
import textwrap


logging.getLogger().setLevel(logging.INFO)


def file_or_stdin(input):
    return open(input[1:]).read() if isinstance(input, str) and \
        input.startswith('@') else input


class MaxwellAPIClient:
    DEFAULT_TIMEOUT = 10

    def __init__(self, access_token, base_url='https://api.maxwell.ai/'):
        self._access_token = access_token
        self._base_url = base_url

    def _request(self, method, endpoint, api_version='2.0', headers=None,
                 data=None, params=None, timeout=None):
        url = '%s/%s/%s' % (
            self._base_url.strip('/'),
            api_version,
            endpoint.strip('/'))
        headers = headers or {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % self._access_token}
        timeout = timeout or self.DEFAULT_TIMEOUT
        data = json.dumps(data) if data else None
        response = getattr(requests, method)(
            url,
            headers=headers,
            data=data,
            params=params,
            timeout=timeout)
        logging.info('[%s] %s %s' % (
            response.status_code, method.upper(), url))
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return response.text

        try:
            print(self._response_to_table(response.json()))
        except json.decoder.JSONDecodeError:
            print(response.text)

    def _response_to_table(self, response_json):
        def format(obj):
            if isinstance(obj, list):
                return '\n'.join(sorted([format(item) for item in obj]))
            elif isinstance(obj, dict):
                return ', '.join([format(value) for value in obj.values() if
                                  format(value)])
            elif isinstance(obj, str):
                return '\n'.join(textwrap.wrap(obj))
            elif isinstance(obj, (int, float)):
                return str(obj)
            elif obj is None:
                return ''
            return 'UNKNOWN TYPE'
        table_data = []
        if len(response_json.keys()) == 1:
            objs = next(iter(response_json.values()))
        else:
            objs = response_json
        if isinstance(objs, list):
            if len(objs) == 0:
                return response_json
            headers = sorted(objs[0].keys())
            for obj in objs:
                table_data.append([format(obj[header]) for header in headers])
        elif isinstance(objs, dict):
            headers = sorted(objs.keys())
            table_data.append([format(objs[header]) for header in headers])
        else:
            return objs
        table_data = [headers] + table_data
        table = terminaltables.AsciiTable(table_data=table_data)
        table.inner_row_border = True
        return table.table

    def _execute_command(self, command, *args):
        assert command.strip('_') == command
        if not hasattr(self, command):
            commands = '\n'.join(sorted([attr for attr in dir(self) if not
                                         attr.startswith('_') and
                                         attr.islower()]))
            exit('\n"%s" is not valid. Available commands:\n\n%s\n' % (
                command, commands))
        getattr(self, command)(*args)

    def get_customer_profile(self):
        return self._request('get', 'customers/profile')

    def list_blueprint_revisions(self, blueprint_id):
        return self._request('get', 'blueprints/id/%s/revisions' %
                             blueprint_id, api_version='1.0')

    def get_blueprint_revision(self, blueprint_id, blueprint_revision_id):
        return self._request('get', 'blueprints/id/%s/revisions/id/%s' % (
            blueprint_id, blueprint_revision_id), api_version='1.0')

    def list_teams(self):
        return self._request('get', 'teams')

    def list_team_blueprints(self, team_id):
        return self._request('get', 'teams/id/%s/blueprints' % team_id)

    def list_team_channels(self, team_id):
        return self._request('get', 'teams/id/%s/channels' % team_id)

    def add_team_channel(self, team_id, channel):
        return self._request(
            'post', 'teams/id/%s/channels' % team_id, data=channel)

    def remove_team_channel(self, team_id, channel):
        return self._request(
            'delete', 'teams/id/%s/channels' % team_id, data=channel)

    def list_team_members(self, team_id):
        return self._request('get', 'teams/id/%s/members' % team_id)

    def add_team_member(self, team_id, customer_id):
        data = {'id': customer_id}
        return self._request(
            'post', 'teams/id/%s/members' % team_id, data=data)

    def remove_team_member(self, team_id, customer_id):
        data = {'id': customer_id}
        return self._request(
            'delete', 'teams/id/%s/members' % team_id, data=data)

    def get_team_invoice_address(self, team_id):
        return self._request('get', 'teams/id/%s/invoice_address' % team_id)

    def create_blueprint(self, team_id, blueprint):
        blueprint = file_or_stdin(blueprint)
        return self._request(
            'post',
            'teams/id/%s/blueprints' % team_id,
            data=blueprint)

    def create_blueprint_revision(self, blueprint_id, blueprint_revision):
        blueprint_revision = file_or_stdin(blueprint_revision)
        return self._request(
            'post',
            'blueprints/id/%s/revisions' % blueprint_id,
            api_version='1.0',
            data=blueprint_revision)

    def publish_blueprint_revision(self, blueprint_id, blueprint_revision_id):
        return self._request('post', 'blueprints/id/%s/revisions/id/%s/publish'
                             % (blueprint_id, blueprint_revision_id),
                             api_version='1.0')


class MaxwellStagingAPIClient(MaxwellAPIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, base_url='https://staging.api.maxwell.ai/', **kwargs)
