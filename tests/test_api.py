# `python3 -m pytest`

import pytest
from plane_py.api import PlaneClient

@pytest.fixture
async def client():
    return PlaneClient(api_token="plane_api_f237301acce34f43aea61dfc7f1e90c2")

@pytest.mark.asyncio
async def test_get_projects(client: PlaneClient):
    try:
        projects = await client.get_projects()
        assert isinstance(projects, list)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")