import maxwell


class TestClient:
    def test_instantiation(self):
        maxwell.Client(
            access_token="foo", base_url="https://staging.api.maxwell.ai/",
        )
