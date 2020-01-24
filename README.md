# Maxwell API Client

Maxwell API client written in Python. Tested with Python versions 3.6 - 3.8.

The use of Python 3.7+ is strongly advised. Download the latest Python 3
release [here](https://www.python.org/downloads/).

Also, make sure to install iPython, which provides a powerful interactive
Python shell:

    pip3 install ipython

## Usage

### Creating the client, listing and getting a team

    $ ipython
    >>> import maxwell
    >>> client = maxwell.Client(access_token='eyJ0eXAiOiJKV1QiLCJhbGciOi...', base_url='https://staging.api.maxwell.ai')
    >>> client.Teams.list()
    [Team(id='5a4f74c3830f781b3b3093be', name='Maxwell'),
     Team(id='5a61ca49830f780e2dfa54c7', name='Test'),
     Team(id='5a940e3d419f570010d096e4', name='Foo')]
    >>> team = client.Teams.get('5a94144a419f570010d096eb')

### Blueprints and revisions

    >>> team.Blueprints.list()
    [Blueprint(id='5ddfe170884854759fc1d946', name='Test 2019-Nov-28 15:03'),
     Blueprint(id='5ddfe1d4884854759fc1d95a', name='Test 2019-Nov-28 15:17')]
    >>> blueprint = team.Blueprints.get('5b9b7c98bbbe77000c76e939')
    >>> blueprints.Revisions.list()

### Creating and publishing revisions

    >>> from maxwell.model.workflow import Workflow
    >>> from maxwell.model.task.send_message import SendMessageTask
    >>> from maxwell.model.message.text import TextMessage
    >>> from maxwell.resource.revision import Revision
    >>> tasks = [SendMessageTask(id='a', message=TextMessage(text='foo'), next_task_id='b'), SendMessageTask(id='b', message=TextMessage(text='bar'))]
    >>> revision = Revision(workflow=Workflow(tasks=tasks))
    >>> revision = blueprint.Revisions.create(revision)
    >>> revision.publish()

## Resources

- Users.get(): User
- User.Channels.list(): List[Channel]
- User.Channels.get(platform, external_id): Channel

- Channel.Contacts.list(): List[Contact]
- Channel.Contacts.get(id): Contact
- Channel.Conversations.create(Conversation): List[Conversation]
- Channel.PersistentMenu.get(): PersistentMenu
- Channel.PersistentMenu.update(PersistentMenu): PersistentMenu

- Teams.list(): List[Team]
- Teams.get(id): Team
- Team.Channels.list(): List[Channel]
- Team.Channels.get(platform, external_id): Channel
- Team.Blueprints.list(): List[Blueprint]
- Team.Blueprints.get(id): Blueprint
- Team.Blueprints.create(Blueprint): Blueprint
- Team.Dashboards.list(): List[Dashboard]
- Team.Dashboards.create(Dashboard): Dashboard

- Dashboard.Reports.list(): List[Report]
- Dashboard.Reports.create(Report): Report

- Blueprint.Revisions.list(): List[Revision]
- Blueprint.Revisions.create(Revision): Revision

- Revision.publish(): None

## Models

- maxwell.model.workflow.Workflow
- maxwell.model.message.text.TextMessage
- maxwell.model.task.send_message.SendMessageTask
