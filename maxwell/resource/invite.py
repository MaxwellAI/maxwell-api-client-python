from maxwell.resource.base import Resource, ListResource


class Invite(Resource):
    _path = "invites"
    _depth = 1

    def __init__(
        self, email=None, send_email=True, client=None, parent=None, **kwargs,
    ):
        super().__init__(client, parent, email=email, send_email=send_email)
        self.email = email
        self.send_email = send_email


class Invites(ListResource):
    _path = "invites"
    _resource_class = Invite
    _depth = 2
