# `python3 -m pytest`

import pytest
from plane_py import *

@pytest.fixture
async def client():
    return PlaneClient(api_token="plane_api_f237301acce34f43aea61dfc7f1e90c2")

@pytest.mark.asyncio
async def test_get_projects(client: PlaneClient):
    try:
        projects = await client.get_projects()
        assert isinstance(projects, list[Project])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_project_details(client: PlaneClient):
    try:
        project = await client.get_project_details(
            project_id="50d503d8-b1a2-4815-b7a2-d69088f73411"
        )
        assert isinstance(project, Project)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_project(client: PlaneClient):
    try:
        updated_project = await client.update_project(
            project_id="50d503d8-b1a2-4815-b7a2-d69088f73411",
            name="Updated Project"
        )
        assert isinstance(updated_project, Project)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_project(client: PlaneClient):
    try:
        created_project = await client.create_project(
            name="New Project",
            identifier="PRJ01"
        )
        assert isinstance(created_project, Project)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_project(client: PlaneClient):
    try:
        deleted_project = await client.delete_project(
            project_id="50d503d8-b1a2-4815-b7a2-d69088f73411"
        )
        assert isinstance(deleted_project, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_states(client: PlaneClient):
    try:
        project_states = await client.get_states(
            project_id="50d503d8-b1a2-4815-b7a2-d69088f73411"
        )
        assert isinstance(project_states, list[State])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_state_details(client: PlaneClient):
    try:
        project_state = await client.get_state_details(
            project_id="50d503d8-b1a2-4815-b7a2-d69088f73411",
            state_id="7856896f-4792-4b4f-a478-ff0c953c4f40"
        )
        assert isinstance(project_state, State)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_state(client: PlaneClient):
    try:
        new_state = await client.create_state(
            name="New State",
            description="This is a new state",
            color="#000000",
            project_id="7856896f-4792-4b4f-a478-ff0c953c4f40"
        )

        assert isinstance(new_state, State)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_state(client: PlaneClient):
    try:
        updated_state = await client.update_state(
            name="Updated State",
            description="This is an updated state",
            project_id="7856896f-4792-4b4f-a478-ff0c953c4f40",
            state_id="ca38ca92-b3c5-4a64-923d-15490ce3b6a9"
        )
        assert isinstance(updated_state, State)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_state(client: PlaneClient):
    try:
        deleted_state = await client.delete_state(
            project_id="7856896f-4792-4b4f-a478-ff0c953c4f40",
            state_id="ca38ca92-b3c5-4a64-923d-15490ce3b6a9"
        )
        assert isinstance(deleted_state, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")