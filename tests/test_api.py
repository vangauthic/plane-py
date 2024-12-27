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

@pytest.mark.asyncio
async def test_get_labels(client: PlaneClient):
    try:
        project_labels = await client.get_labels(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd"
        )
        assert isinstance(project_labels, list[Label])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_label_details(client: PlaneClient):
    try:
        project_label = await client.get_label_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            label_id="02c01a1e-89ba-4016-a206-6f01826a9dfd"
        )
        assert isinstance(project_label, Label)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_label(client: PlaneClient):
    try:
        new_label = await client.create_label(
            name="New Label",
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            color="FFFFFF"
        )
        assert isinstance(new_label, Label)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_label(client: PlaneClient):
    try:
        updated_label = await client.update_label(
            name="Updated Label",
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            label_id="a29dab20-c4d2-4263-b3d6-451935d714b2",
            color="FFFF00"
        )
        assert isinstance(updated_label, Label)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_label(client: PlaneClient):
    try:
        deleted_label = await client.delete_label(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            label_id="a29dab20-c4d2-4263-b3d6-451935d714b2",
        )
        assert isinstance(deleted_label, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_links(client: PlaneClient):
    try:
        issue_links = await client.get_links(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e"
        )
        assert isinstance(issue_links, list[Link])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_link_details(client: PlaneClient):
    try:
        link_details = await client.get_link_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e",
            link_id="8cf365ce-d3c6-4876-b177-6b755737dace"
        )
        assert isinstance(link_details, Link)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_link(client: PlaneClient):
    try:
        new_link = await client.create_link(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e",
            url="https://example.com"
        )
        assert isinstance(new_link, Link)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_link(client: PlaneClient):
    try:
        updated_link = await client.update_link(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e",
            link_id="357ecb87-1157-42f7-95cb-333837bfee44",
            url="https://example2.com"
        )
        assert isinstance(updated_link, Link)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_link(client: PlaneClient):
    try:
        deleted_link = await client.delete_link(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e",
            link_id="357ecb87-1157-42f7-95cb-333837bfee44"
        )
        assert isinstance(deleted_link, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_issues(client: PlaneClient):
    try:
        project_issues = await client.get_issues(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd"
        )
        assert isinstance(project_issues, list[Issue])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_issue_details(client: PlaneClient):
    try:
        project_issue = await client.get_issue_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e"
        )
        assert isinstance(project_issue, Issue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_issue(client: PlaneClient):
    try:
        new_issue = await client.create_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            name="New Issue"
        )
        assert isinstance(new_issue, Issue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_issue(client: PlaneClient):
    try:
        updated_issue = await client.create_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="cb8a79b9-fcd5-41dd-9826-4e3999bce1fb",
            name="Updated Issue"
        )
        assert isinstance(updated_issue, Issue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_issue(client: PlaneClient):
    try:
        deleted_issue = await client.delete_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e"
        )
        assert isinstance(deleted_issue, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_issue_activity(client: PlaneClient):
    try:
        issue_activities = await client.get_issue_activity(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e"
        )
        assert isinstance(issue_activities, list[IssueActivity])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_activity_details(client: PlaneClient):
    try:
        issue_activity = await client.get_activity_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e",
            activity_id="68e46fde-023b-4c99-ab2d-b15f46a3588d"
        )
        assert isinstance(issue_activity, IssueActivity)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_issue_comments(client: PlaneClient):
    try:
        issue_comments = await client.get_issue_comments(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e"
        )
        assert isinstance(issue_comments, list[IssueComment])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")