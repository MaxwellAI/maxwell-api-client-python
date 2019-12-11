from maxwell.resource.base import Resource, ListResource


class WhitelistedDomain(Resource):
    _path = "whitelisted-domains"

    def __init__(self, client=None, parent=None, **kwargs):
        super().__init__(client, parent)


class WhitelistedDomains(ListResource):
    _path = "whitelisted-domains"
    _resource = WhitelistedDomain
