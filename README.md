# Maxwell API Client

## Usage

    >>> from maxwell import MaxwellAPIClient
    >>> client = MaxwellAPIClient(access_token='eyJ0eXAiOiJKV1QiLCJhbGciOi...')
    >>> client.list_teams()
    {'teams': [{'id': '5c17cedebc69d77789347dc5',
       'members': [{'id': '5c17cee6bc69d77789347dc6'}],
       'name': 'My Team'}]}

## Available commands

* add_team_channel(team_id, channel)
* add_team_member(team_id, customer_id)
* create_blueprint(team_id, blueprint)
* create_blueprint_revision(team_id, blueprint_id, blueprint_revision)
* get_blueprint_revision(blueprint_id, blueprint_revision_id)
* get_customer_profile()
* get_team_invoice_address(team_id)
* list_teams()
* list_team_blueprints(team_id)
* list_team_channels(team_id)
* list_team_members(team_id)
* list_blueprint_revisions(blueprint_id)
* publish_blueprint_revision(blueprint_id, blueprint_revision_id)
* remove_team_channel(team_id, channel)
* remove_team_member(team_id, customer_id)
