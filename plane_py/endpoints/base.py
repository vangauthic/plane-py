class BaseEndpoint:
    def __init__(self, client):
        self.client = client
        self._request = client._request
        self.workspace_slug = client.workspace_slug