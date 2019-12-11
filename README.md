# Maxwell API Client

Maxwell API client written in Python. Tested with Python versions 3.6 - 3.8.

## Usage

    >>> import maxwell
    >>> client = maxwell.Client(access_token='eyJ0eXAiOiJKV1QiLCJhbGciOi...')
    >>> client.Teams.list()
    [Team(id='5a4f74c3830f781b3b3093be', name='Maxwell'),
     Team(id='5a61ca49830f780e2dfa54c7', name='Test'),
     Team(id='5a940e3d419f570010d096e4', name='Foo')]
    >>> client.Teams.get(id='5a4f74c3830f781b3b3093be').Blueprints.list()
    [Blueprint(id='5ddfe170884854759fc1d946', name='Test 2019-Nov-28 15:03'),
     Blueprint(id='5ddfe1d4884854759fc1d95a', name='Test 2019-Nov-28 15:17')]

## Resources

* Users.get(): User
* User.Channels.list(): List[Channel]
* User.Channels.get(platform, external_id): Channel

* Channel.Contacts.list(): List[Contact]
* Channel.Contacts.get(id): Contact
* Channel.Conversations.create(Conversation): List[Conversation]
* Channel.PersistentMenu.get(): PersistentMenu
* Channel.PersistentMenu.update(PersistentMenu): PersistentMenu

* Teams.list(): List[Team]
* Teams.get(id): Team
* Team.Channels.list(): List[Channel]
* Team.Channels.get(platform, external_id): Channel
* Team.Blueprints.list(): List[Blueprint]
* Team.Blueprints.get(id): Blueprint
* Team.Blueprints.create(Blueprint): Blueprint
* Team.Dashboards.list(): List[Dashboard]
* Team.Dashboards.create(Dashboard): Dashboard

* Dashboard.Reports.list(): List[Report]
* Dashboard.Reports.create(Report): Report

* Blueprint.Revisions.list(): List[Revision]
* Blueprint.Revisions.create(Revision): Revision

* Revision.publish(): None

## Models

* maxwell.model.workflow.Workflow
* maxwell.model.message.text.TextMessage
* maxwell.model.task.send_message.SendMessageTask
