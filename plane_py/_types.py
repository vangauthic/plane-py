from typing import TypedDict
from dataclasses import dataclass

class Task(TypedDict):
    id: str
    title: str
    description: str
    status: str

@dataclass
class State:
    """
    Represents a Plane state.
    
    :param id: UUID of the state
    :type id: str
    :param created_at: Timestamp of when the state was created
    :type created_at: str
    :param updated_at: Timestamp of when the state was last updated
    :type updated_at: str
    :param name: Name of the state
    :type name: str
    :param description: Description of the state
    :type description: str
    :param color: Color code for the state
    :type color: str
    :param workspace_slug: Slug of the workspace
    :type workspace_slug: str
    :param sequence: Sequence number of the state
    :type sequence: str
    :param group: Group the state belongs to
    :type group: str
    :param default: Whether this is the default state
    :type default: bool
    :param created_by: UUID of the user who created the state
    :type created_by: str
    :param updated_by: UUID of the user who last updated the state
    :type updated_by: str
    :param project: UUID of the project this state belongs to
    :type project: str
    :param workspace: UUID of the workspace this state belongs to
    :type workspace: str
    """
    id: str
    created_at: str
    updated_at: str
    name: str
    description: str
    color: str
    workspace_slug: str
    sequence: str
    group: str
    default: bool
    created_by: str
    updated_by: str
    project: str
    workspace: str

@dataclass
class Project:
    """
    Represents a Plane project.
    
    :param archive_in: Months in which the issue should be automatically archived (0-12)
    :type archive_in: int
    :param close_in: Months in which the issue should be automatically closed (0-12)
    :type close_in: int
    :param cover_image: Cover image of the project
    :type cover_image: str
    :param created_at: Timestamp of when the project was created
    :type created_at: str
    :param created_by: UUID of the user who created the project
    :type created_by: str
    :param cycle_view: Enable/Disable cycle for the project in the UI
    :type cycle_view: bool
    :param default_assignee: UUID of the default assignee of the project
    :type default_assignee: str
    :param default_state: Default state which will be used when issues are automatically closed
    :type default_state: str
    :param description: Description of the project
    :type description: str
    :param description_html: Description of the project in HTML format
    :type description_html: str
    :param description_text: Description of the project in text format
    :type description_text: str
    :param emoji: Emoji of the project in DEX code without '&#'
    :type emoji: str
    :param estimate: UUID of the estimate of the project
    :type estimate: str
    :param icon_prop: Saved data of the project icon
    :type icon_prop: dict
    :param id: Project ID
    :type id: str
    :param identifier: Identifier of the project
    :type identifier: str
    :param inbox_view: Enable/Disable intake for the project in the UI
    :type inbox_view: bool
    :param is_deployed: Represents whether the project is deployed or not
    :type is_deployed: bool
    :param is_member: Whether the current requesting user is a member of the project
    :type is_member: bool
    :param issue_views_view: Enable/Disable project view for the project in the UI
    :type issue_views_view: bool
    :param member_role: The role of the current requesting user in the project
    :type member_role: int
    :param module_view: Enable/Disable module for the project in the UI
    :type module_view: bool
    :param name: Name of the project
    :type name: str
    :param network: Project visibility (0: Secret, 2: Public)
    :type network: int
    :param page_view: Enable/Disable pages for the project in the UI
    :type page_view: bool
    :param project_lead: UUID of the project lead
    :type project_lead: str
    :param total_cycles: Total number of cycles in the project
    :type total_cycles: int
    :param total_members: Total members present in the project
    :type total_members: int
    :param total_modules: Total number of modules in the project
    :type total_modules: int
    :param updated_at: Timestamp of when the project was last updated
    :type updated_at: str
    :param updated_by: UUID of the user who last updated the project
    :type updated_by: str
    :param workspace: UUID of the workspace in which the project is present
    :type workspace: str
    """
    archive_in: int
    close_in: int  
    cover_image: str
    created_at: str
    created_by: str
    cycle_view: bool
    default_assignee: str
    default_state: str
    description: str
    description_html: str
    description_text: str
    emoji: str
    estimate: str
    icon_prop: dict
    id: str
    identifier: str
    inbox_view: bool
    is_deployed: bool
    is_member: bool
    issue_views_view: bool
    member_role: int
    module_view: bool
    name: str
    network: int
    page_view: bool
    project_lead: str
    total_cycles: int
    total_members: int
    total_modules: int
    updated_at: str
    updated_by: str
    workspace: str