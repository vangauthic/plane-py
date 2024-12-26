# `python3 -m pytest`

import pytest
from plane_py.api import PlaneClient
from plane_py._types import Project

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

@pytest.mark.asyncio
async def test_get_project_details(client: PlaneClient):
    try:
        project = await client.get_project_details(project_id="50d503d8-b1a2-4815-b7a2-d69088f73411")
        assert isinstance(project, Project)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_project(client: PlaneClient):
    try:
        updated_project = await client.update_project(project_id="50d503d8-b1a2-4815-b7a2-d69088f73411", name="Updated Project")
        assert isinstance(updated_project, Project)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_project(client: PlaneClient):
    try:
        created_project = await client.create_project(name="New Project", identifier="PRJ01")
        assert isinstance(created_project, Project)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_project(client: PlaneClient):
    try:
        deleted_project = await client.delete_project(project_id="50d503d8-b1a2-4815-b7a2-d69088f73411")
        assert isinstance(deleted_project, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")