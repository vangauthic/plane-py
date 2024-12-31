# `python3 -m pytest`

import pytest
from plane_py import *

@pytest.fixture
async def client():
    return PlaneClient(api_token="")

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

@pytest.mark.asyncio
async def test_get_comment_details(client: PlaneClient):
    try:
        issue_comment = await client.get_comment_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e",
            comment_id = "d26db721-6c86-4071-b948-1005be594bd3"
        )
        assert isinstance(issue_comment, IssueComment)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_comment(client: PlaneClient):
    try:
        new_comment = await client.create_comment(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e",
            comment_html="This is a New Comment"
        )
        assert isinstance(new_comment, IssueComment)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_comment(client: PlaneClient):
    try:
        updated_comment = await client.update_comment(
            comment_html="This is an Updated Comment",
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e",
            comment_id="d26db721-6c86-4071-b948-1005be594bd3"
        )
        assert isinstance(updated_comment, IssueComment)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_comment(client: PlaneClient):
    try:
        deleted_comment = await client.delete_comment(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e",
            comment_id="d26db721-6c86-4071-b948-1005be594bd3"
        )
        assert isinstance(deleted_comment, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_modules(client: PlaneClient):
    try:
        project_modules = await client.get_modules(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd"
        )
        assert isinstance(project_modules, list[Module])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_module_details(client: PlaneClient):
    try:
        project_module = await client.get_module_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="81522e51-d598-4b41-85f8-dd4d562a91a0"
        )
        assert isinstance(project_module, Module)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_module(client: PlaneClient):
    try:
        new_module = await client.create_module(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            name="This is a New Module"
        )
        assert isinstance(new_module, Module)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_module(client: PlaneClient):
    try:
        updated_module = await client.update_module(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="83c29ebc-4f96-45da-8982-8f0f7c36fba9",
            name="This is an Updated Module"
        )
        assert isinstance(updated_module, Module)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_module(client: PlaneClient):
    try:
        deleted_module = await client.delete_module(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="83c29ebc-4f96-45da-8982-8f0f7c36fba9"
        )
        assert isinstance(deleted_module, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_module_issues(client: PlaneClient):
    try:
        module_issues = await client.get_module_issues(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="81522e51-d598-4b41-85f8-dd4d562a91a0"
        )
        assert isinstance(module_issues, list[ModuleIssue])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_module_issue(client: PlaneClient):
    try:
        new_module_issue = await client.create_module_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="81522e51-d598-4b41-85f8-dd4d562a91a0",
            issues=["dfa4c511-234e-48c6-83eb-5fda38fc108e"]
        )
        assert isinstance(new_module_issue, ModuleIssue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_module_issue(client: PlaneClient):
    try:
        deleted_module_issue = await client.delete_module_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="81522e51-d598-4b41-85f8-dd4d562a91a0",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e"
        )
        assert isinstance(deleted_module_issue, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_cycles(client: PlaneClient):
    try:
        project_cycles = await client.get_cycles(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd"
        )
        assert isinstance(project_cycles, list[Cycle])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_cycle_details(client: PlaneClient):
    try:
        project_cycle = await client.get_cycle_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="872f4637-b77d-4ab3-9427-a36cc3cd387a"
        )
        assert isinstance(project_cycle, Cycle)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_cycle(client: PlaneClient):
    try:
        new_cycle = await client.create_cycle(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            name="This is a New Cycle"
        )
        assert isinstance(new_cycle, Cycle)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_cycle(client: PlaneClient):
    try:
        updated_cycle = await client.update_cycle(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="b82818b7-d469-4ee6-bb5a-32b753782652",
            name="This is an Updated Cycle"
        )
        assert isinstance(updated_cycle, Cycle)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_cycle(client: PlaneClient):
    try:
        deleted_cycle = await client.delete_cycle(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="b82818b7-d469-4ee6-bb5a-32b753782652"
        )
        assert isinstance(deleted_cycle, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_cycle_issues(client: PlaneClient):
    try:
        cycle_issues = await client.get_cycle_issues(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="872f4637-b77d-4ab3-9427-a36cc3cd387a"
        )
        assert isinstance(cycle_issues, list[CycleIssue])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_cycle_issue(client: PlaneClient):
    try:
        new_cycle_issue = await client.create_cycle_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="872f4637-b77d-4ab3-9427-a36cc3cd387a",
            issues=["815c4689-7525-46d3-a19d-d2f58bcfadbf", "dfa4c511-234e-48c6-83eb-5fda38fc108e"]
        )
        assert isinstance(new_cycle_issue, CycleIssue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_cycle_issue(client: PlaneClient):
    try:
        deleted_cycle_issue = await client.delete_cycle_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="872f4637-b77d-4ab3-9427-a36cc3cd387a",
            issue_id="815c4689-7525-46d3-a19d-d2f58bcfadbf"
        )
        assert isinstance(deleted_cycle_issue, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_intake_issues(client: PlaneClient):
    try:
        intake_issues = await client.get_intake_issues(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd"
        )
        assert isinstance(intake_issues, list[IntakeIssue])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_intake_issue_details(client: PlaneClient):
    try:
        intake_issue = await client.get_intake_issue_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="43340f33-0ab2-49f4-a7f0-382249da1e94"
        )
        assert isinstance(intake_issue, IntakeIssue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_intake_issue(client: PlaneClient):
    try:
        new_intake_issue = await client.create_intake_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue={"name":"This is a New Issue", "description":"Description"},
        )
        assert isinstance(new_intake_issue, IntakeIssue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_intake_issue(client: PlaneClient):
    try:
        updated_intake_issue = await client.update_intake_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="8ac2f864-595d-4816-acbf-ffe611c1d607",
            issue={"name":"This is an Updated Issue", "description":"New Description"}
        )
        assert isinstance(updated_intake_issue, IntakeIssue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_intake_issue(client: PlaneClient):
    try:
        deleted_intake_issue = await client.delete_intake_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            intake_id="bd0614d4-a72a-4278-be00-f6b25200d167",
            issue_id="8ac2f864-595d-4816-acbf-ffe611c1d607"
        )
        assert isinstance(deleted_intake_issue, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_issue_types(client: PlaneClient):
    try:
        issue_types = await client.get_issue_types(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd"
        )
        assert isinstance(issue_types, list[IssueType])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_type_details(client: PlaneClient):
    try:
        issue_type = await client.get_type_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="5ba86e3a-304a-4df2-aceb-5ae5921d4274"
        )
        assert isinstance(issue_type, IssueType)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_type(client: PlaneClient):
    try:
        new_issue_type = await client.create_type(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            name="This is a New Issue Type",
            description="Description"
        )
        assert isinstance(new_issue_type, IssueType)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_type(client: PlaneClient):
    try:
        updated_issue_type = await client.update_type(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="01aa7856-903b-4602-b794-e2ceea5592c8",
            name="This is an Updated Issue Type",
            description="New Description"
        )
        assert isinstance(updated_issue_type, IssueType)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_issue_type(client: PlaneClient):
    try:
        deleted_issue_type = await client.delete_issue_type(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="01aa7856-903b-4602-b794-e2ceea5592c8"
        )
        assert isinstance(deleted_issue_type, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_issue_properties(client: PlaneClient):
    try:
        issue_properties = await client.get_issue_properties(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="b5155b66-019b-49f6-8a89-4526bbbf8c56"
        )
        assert isinstance(issue_properties, list[IssueProperty])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_property_details(client: PlaneClient):
    try:
        issue_property = await client.get_property_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="b5155b66-019b-49f6-8a89-4526bbbf8c56",
            property_id="8670a483-7713-4f3f-a639-330ad2f81907"
        )
        assert isinstance(issue_property, IssueProperty)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_property(client: PlaneClient):
    try:
        updated_issue_property = await client.update_property(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="b5155b66-019b-49f6-8a89-4526bbbf8c56",
            property_id="8670a483-7713-4f3f-a639-330ad2f81907",
            name="Updated Issue Property"
        )
        assert isinstance(updated_issue_property, IssueProperty)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_property(client: PlaneClient):
    try:
        new_issue_property = await client.update_property(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="b5155b66-019b-49f6-8a89-4526bbbf8c56",
            name="New Issue Property"
        )
        assert isinstance(new_issue_property, IssueProperty)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_property(client: PlaneClient):
    try:
        deleted_issue_property = await client.delete_property(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="5ba86e3a-304a-4df2-aceb-5ae5921d4274",
            property_id="a47b4ef5-1cef-41dd-b7ce-8cd23346dce0"
        )
        assert isinstance(deleted_issue_property, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_property_options(client: PlaneClient):
    try:
        property_options = await client.get_property_options(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d"
        )
        assert isinstance(property_options, list[PropertyOption])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_option_details(client: PlaneClient):
    try:
        property_option = await client.get_option_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            option_id="58851674-024b-4190-9a0b-b64c931b9481"
        )
        assert isinstance(property_option, PropertyOption)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_option(client: PlaneClient):
    try:
        new_property_option = await client.create_option(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            name="New Option"
        )
        assert isinstance(new_property_option, PropertyOption)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_update_option(client: PlaneClient):
    try:
        updated_property_option = await client.update_option(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            option_id="fef0416b-4493-4c0a-928e-92ecbfb83fdb",
            name="Updated Option"
        )
        assert isinstance(updated_property_option, PropertyOption)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_delete_option(client: PlaneClient):
    try:
        deleted_property_option = await client.delete_option(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            option_id="fef0416b-4493-4c0a-928e-92ecbfb83fdb"
        )
        assert isinstance(deleted_property_option, bool)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_get_property_values(client: PlaneClient):
    try:
        property_values = await client.get_property_values(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            issue_id="0c039e1d-0be4-4684-9454-18136203491d"
        )
        assert isinstance(property_values, list[PropertyValue])
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")

@pytest.mark.asyncio
async def test_create_value(client: PlaneClient):
    try:
        new_property_value = await client.create_value(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="0c039e1d-0be4-4684-9454-18136203491d",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            values=["test"]
        )
        assert isinstance(new_property_value, PropertyValue)
    except Exception as e:
        pytest.fail(f"Test failed with exception: {e}")