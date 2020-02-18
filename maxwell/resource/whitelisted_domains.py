from maxwell.resource.base import ListResource


class WhitelistedDomains(ListResource):
    _path = "whitelisted-domains"
    _slug = "whitelisted_domains"
    _depth = 2

    def __init__(self, whitelisted_domains=None, client=None, parent=None):
        self.whitelisted_domains = whitelisted_domains
        super().__init__(client, parent)

    def list(self):
        path = self._get_full_path()
        response = self._request(path=path)[getattr(self, "_slug", self._path)]
        return self.__class__(
            client=self._client, parent=self, whitelisted_domains=response
        )

    def update(self, whitelisted_domains):
        return self._request(
            self._get_full_path(),
            method="put",
            data={
                "whitelisted_domains": whitelisted_domains.whitelisted_domains
            },
        )
