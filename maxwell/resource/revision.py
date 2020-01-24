from maxwell.resource.base import Resource, ListResource


class Revision(Resource):
    _depth = 3

    def __init__(
        self,
        welcome_messages=None,
        revision_number=None,
        workflow=None,
        is_current=None,
        id=None,
        client=None,
        parent=None,
        **kwargs,
    ):
        super().__init__(client, parent, id=id)
        self.id = id
        self.revision_number = revision_number
        self.welcome_messages = welcome_messages
        self.workflow = workflow
        self.is_current = is_current
        self._exclude_fields += ["is_current"]

    def _get_publish_path(self, **parameters):
        return f"{self._get_full_path(**parameters)}/publish"

    def publish(self):
        return self._request(self._get_publish_path(id=self.id), method="post")


class Revisions(ListResource):
    _path = "revisions"
    _slug = "blueprint_revisions"
    _resource_class = Revision
    _depth = 2
