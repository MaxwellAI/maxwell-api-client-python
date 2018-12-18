from maxwell import MaxwellAPIClient, MaxwellStagingAPIClient


class TestMaxwellStagingAPIClient:
    def test_has_staging_url(self):
        client = MaxwellStagingAPIClient(access_token='')
        assert client._base_url == 'https://staging.api.maxwell.ai/'


class TestMaxwellAPIClient:
    def test_has_production_url(self):
        client = MaxwellAPIClient(access_token='')
        assert client._base_url == 'https://api.maxwell.ai/'
