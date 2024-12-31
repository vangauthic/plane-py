from typing import Optional
from dataclasses import dataclass

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

@dataclass
class Label:
    """
    Represents a Plane label.
    
    :param id: UUID of the label
    :type id: str
    :param created_at: Timestamp of when the label was created
    :type created_at: str
    :param updated_at: Timestamp of when the label was last updated
    :type updated_at: str
    :param name: Name of the label
    :type name: str
    :param description: Description of the label
    :type description: str
    :param color: Color code for the label
    :type color: str
    :param sort_order: Sorting order of the label
    :type sort_order: float
    :param created_by: UUID of the user who created the label
    :type created_by: str
    :param updated_by: UUID of the user who last updated the label
    :type updated_by: str
    :param project: UUID of the project this label belongs to
    :type project: str
    :param workspace: UUID of the workspace this label belongs to
    :type workspace: str
    :param parent: UUID of the parent label if any
    :type parent: Optional[str]
    """
    id: str
    created_at: str
    updated_at: str
    name: str
    description: str
    color: str
    sort_order: float
    created_by: str
    updated_by: str
    project: str
    workspace: str
    parent: Optional[str] = None

@dataclass
class Link:
    """
    Represents a Plane link.
    
    :param id: UUID of the link
    :type id: str
    :param created_at: Timestamp of when the link was created
    :type created_at: str
    :param updated_at: Timestamp of when the link was last updated
    :type updated_at: str
    :param title: Title of the link
    :type title: str
    :param url: URL of the link
    :type url: str
    :param metadata: Additional metadata for the link
    :type metadata: dict
    :param created_by: UUID of the user who created the link
    :type created_by: str
    :param updated_by: UUID of the user who last updated the link
    :type updated_by: str
    :param project: UUID of the project this link belongs to
    :type project: str
    :param workspace: UUID of the workspace this link belongs to
    :type workspace: str
    :param issue: UUID of the issue this link is associated with
    :type issue: str
    """
    id: str
    created_at: str
    updated_at: str
    title: str
    url: str
    metadata: dict
    created_by: str
    updated_by: str
    project: str
    workspace: str
    issue: str

@dataclass
class Issue:
    """
    Represents a Plane issue.
    
    :param id: UUID of the issue
    :type id: str
    :param created_at: Timestamp of when the issue was created
    :type created_at: str
    :param updated_at: Timestamp of when the issue was last updated
    :type updated_at: str
    :param estimate_point: Story points/estimate for the issue
    :type estimate_point: Optional[float]
    :param name: Name/title of the issue
    :type name: str
    :param description_html: Description in HTML format
    :type description_html: str
    :param description_stripped: Plain text description
    :type description_stripped: str
    :param priority: Priority level of the issue
    :type priority: str
    :param start_date: Start date of the issue
    :type start_date: Optional[str]
    :param target_date: Due date of the issue
    :type target_date: Optional[str]
    :param sequence_id: Sequential identifier of the issue
    :type sequence_id: int
    :param sort_order: Sorting order of the issue
    :type sort_order: float
    :param completed_at: Timestamp when the issue was completed
    :type completed_at: Optional[str]
    :param archived_at: Timestamp when the issue was archived
    :type archived_at: Optional[str]
    :param is_draft: Whether the issue is in draft state
    :type is_draft: bool
    :param created_by: UUID of the user who created the issue
    :type created_by: str
    :param updated_by: UUID of the user who last updated the issue
    :type updated_by: str
    :param project: UUID of the project this issue belongs to
    :type project: str
    :param workspace: UUID of the workspace this issue belongs to
    :type workspace: str
    :param parent: UUID of the parent issue if any
    :type parent: Optional[str]
    :param state: UUID of the state this issue is in
    :type state: str
    :param assignees: List of UUIDs of users assigned to this issue
    :type assignees: list[str]
    :param labels: List of UUIDs of labels attached to this issue
    :type labels: list[str]
    """
    id: str
    created_at: str
    updated_at: str
    estimate_point: Optional[float]
    name: str
    description_html: str
    description_stripped: str
    priority: str
    start_date: Optional[str]
    target_date: Optional[str]
    sequence_id: int
    sort_order: float
    completed_at: Optional[str]
    archived_at: Optional[str]
    is_draft: bool
    created_by: str
    updated_by: str
    project: str
    workspace: str
    parent: Optional[str]
    state: str
    assignees: list[str]
    labels: list[str]

@dataclass
class IssueActivity:
    """
    Represents a Plane issue activity log.
    
    :param id: UUID of the activity
    :type id: str
    :param created_at: Timestamp of when the activity was created
    :type created_at: str
    :param updated_at: Timestamp of when the activity was last updated
    :type updated_at: str
    :param verb: Action performed (e.g., "created", "updated", etc.)
    :type verb: str
    :param field: Field that was modified
    :type field: Optional[str]
    :param old_value: Previous value of the field
    :type old_value: Optional[str]
    :param new_value: New value of the field
    :type new_value: Optional[str]
    :param comment: Description of the activity
    :type comment: str
    :param attachments: List of attachments related to the activity
    :type attachments: list
    :param old_identifier: Previous identifier if changed
    :type old_identifier: Optional[str]
    :param new_identifier: New identifier if changed
    :type new_identifier: Optional[str]
    :param epoch: Unix timestamp of the activity
    :type epoch: float
    :param project: UUID of the project this activity belongs to
    :type project: str
    :param workspace: UUID of the workspace this activity belongs to
    :type workspace: str
    :param issue: UUID of the issue this activity is related to
    :type issue: str
    :param issue_comment: UUID of the comment if this activity is comment-related
    :type issue_comment: Optional[str]
    :param actor: UUID of the user who performed the activity
    :type actor: str
    """
    id: str
    created_at: str
    updated_at: str
    verb: str
    field: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    comment: str
    attachments: list
    old_identifier: Optional[str]
    new_identifier: Optional[str]
    epoch: float
    project: str
    workspace: str
    issue: str
    issue_comment: Optional[str]
    actor: str

@dataclass
class IssueComment:
    """
    Represents a Plane issue comment.
    
    :param id: UUID of the comment
    :type id: str
    :param created_at: Timestamp of when the comment was created
    :type created_at: str
    :param updated_at: Timestamp of when the comment was last updated
    :type updated_at: str
    :param comment_stripped: Plain text version of the comment
    :type comment_stripped: str
    :param comment_json: JSON representation of the comment structure
    :type comment_json: dict
    :param comment_html: HTML formatted version of the comment
    :type comment_html: str
    :param attachments: List of attachments related to the comment
    :type attachments: list
    :param access: Access level of the comment (e.g., "INTERNAL")
    :type access: str
    :param created_by: UUID of the user who created the comment
    :type created_by: str
    :param updated_by: UUID of the user who last updated the comment
    :type updated_by: str
    :param project: UUID of the project this comment belongs to
    :type project: str
    :param workspace: UUID of the workspace this comment belongs to
    :type workspace: str
    :param issue: UUID of the issue this comment is associated with
    :type issue: str
    :param actor: UUID of the user who performed the comment action
    :type actor: str
    """
    id: str
    created_at: str
    updated_at: str
    comment_stripped: str
    comment_json: dict
    comment_html: str
    attachments: list
    access: str
    created_by: str
    updated_by: str
    project: str
    workspace: str
    issue: str
    actor: str

@dataclass
class Module:
    """
    Represents a Plane module.
    
    :param id: UUID of the module
    :type id: str
    :param created_at: Timestamp of when the module was created
    :type created_at: str
    :param updated_at: Timestamp of when the module was last updated
    :type updated_at: str
    :param name: Name of the module
    :type name: str
    :param description: Description of the module
    :type description: str
    :param description_text: Plain text description of the module
    :type description_text: Optional[str]
    :param description_html: HTML formatted description of the module
    :type description_html: Optional[str]
    :param start_date: Start date of the module
    :type start_date: Optional[str]
    :param target_date: Target date of the module
    :type target_date: Optional[str]
    :param status: Status of the module
    :type status: str
    :param view_props: View properties of the module
    :type view_props: dict
    :param sort_order: Sorting order of the module
    :type sort_order: float
    :param created_by: UUID of the user who created the module
    :type created_by: str
    :param updated_by: UUID of the user who last updated the module
    :type updated_by: str
    :param project: UUID of the project this module belongs to
    :type project: str
    :param workspace: UUID of the workspace this module belongs to
    :type workspace: str
    :param lead: UUID of the lead of the module
    :type lead: Optional[str]
    :param members: List of UUIDs of members of the module
    :type members: list[str]
    """
    id: str
    created_at: str
    updated_at: str
    name: str
    description: str
    description_text: Optional[str]
    description_html: Optional[str]
    start_date: Optional[str]
    target_date: Optional[str]
    status: str
    view_props: dict
    sort_order: float
    created_by: str
    updated_by: str
    project: str
    workspace: str
    lead: Optional[str]
    members: list[str]

@dataclass
class ModuleIssue:
    """
    Represents a Plane module issue.
    
    :param id: UUID of the module issue
    :type id: str
    :param sub_issues_count: Count of sub-issues
    :type sub_issues_count: int
    :param created_at: Timestamp of when the module issue was created
    :type created_at: str
    :param updated_at: Timestamp of when the module issue was last updated
    :type updated_at: str
    :param created_by: UUID of the user who created the module issue
    :type created_by: str
    :param updated_by: UUID of the user who last updated the module issue
    :type updated_by: str
    :param project: UUID of the project this module issue belongs to
    :type project: str
    :param workspace: UUID of the workspace this module issue belongs to
    :type workspace: str
    :param module: UUID of the module this issue belongs to
    :type module: str
    :param issue: UUID of the issue
    :type issue: str
    """
    id: str
    sub_issues_count: int
    created_at: str
    updated_at: str
    created_by: str
    updated_by: str
    project: str
    workspace: str
    module: str
    issue: str

@dataclass
class Cycle:
    """
    Represents a Plane cycle.
    
    :param id: UUID of the cycle
    :type id: str
    :param created_at: Timestamp of when the cycle was created
    :type created_at: str
    :param updated_at: Timestamp of when the cycle was last updated
    :type updated_at: str
    :param name: Name of the cycle
    :type name: str
    :param description: Description of the cycle
    :type description: str
    :param start_date: Start date of the cycle
    :type start_date: Optional[str]
    :param end_date: End date of the cycle
    :type end_date: Optional[str]
    :param view_props: View properties of the cycle
    :type view_props: dict
    :param sort_order: Sorting order of the cycle
    :type sort_order: float
    :param created_by: UUID of the user who created the cycle
    :type created_by: str
    :param updated_by: UUID of the user who last updated the cycle
    :type updated_by: str
    :param project: UUID of the project this cycle belongs to
    :type project: str
    :param workspace: UUID of the workspace this cycle belongs to
    :type workspace: str
    :param owned_by: UUID of the user who owns the cycle
    :type owned_by: str
    """
    id: str
    created_at: str
    updated_at: str
    name: str
    description: str
    start_date: Optional[str]
    end_date: Optional[str]
    view_props: dict
    sort_order: float
    created_by: str
    updated_by: str
    project: str
    workspace: str
    owned_by: str

@dataclass
class CycleIssue:
    """
    Represents a Plane cycle issue.
    
    :param id: UUID of the cycle issue
    :type id: str
    :param sub_issues_count: Count of sub-issues
    :type sub_issues_count: int
    :param created_at: Timestamp of when the cycle issue was created
    :type created_at: str
    :param updated_at: Timestamp of when the cycle issue was last updated
    :type updated_at: str
    :param created_by: UUID of the user who created the cycle issue
    :type created_by: str
    :param updated_by: UUID of the user who last updated the cycle issue
    :type updated_by: str
    :param project: UUID of the project this cycle issue belongs to
    :type project: str
    :param workspace: UUID of the workspace this cycle issue belongs to
    :type workspace: str
    :param cycle: UUID of the cycle this issue belongs to
    :type cycle: str
    :param issue: UUID of the issue
    :type issue: str
    """
    id: str
    sub_issues_count: int
    created_at: str
    updated_at: str
    created_by: str
    updated_by: str
    project: str
    workspace: str
    cycle: str
    issue: str

@dataclass
class IntakeIssue:
    """
    Represents a Plane intake issue.
    
    :param id: UUID of the intake issue
    :type id: str
    :param pending_issue_count: Number of pending issues
    :type pending_issue_count: int
    :param created_at: Timestamp of when the intake issue was created
    :type created_at: str
    :param updated_at: Timestamp of when the intake issue was last updated
    :type updated_at: str
    :param name: Name of the intake
    :type name: str
    :param description: Description of the intake
    :type description: str
    :param is_default: Whether this is the default intake
    :type is_default: bool
    :param view_props: View properties of the intake
    :type view_props: dict
    :param created_by: UUID of the user who created the intake
    :type created_by: str
    :param updated_by: UUID of the user who last updated the intake
    :type updated_by: str
    :param project: UUID of the project this intake belongs to
    :type project: str
    :param workspace: UUID of the workspace this intake belongs to
    :type workspace: str
    """
    id: str
    pending_issue_count: int
    created_at: str
    updated_at: str
    name: str
    description: str
    is_default: bool
    view_props: dict
    created_by: str
    updated_by: str
    project: str
    workspace: str

@dataclass
class IssueType:
    """
    Represents a Plane issue type.
    
    :param id: UUID of the issue type
    :type id: str
    :param name: Name of the issue type
    :type name: str
    :param description: Description of the issue type
    :type description: str
    :param logo_props: Properties for the issue type logo
    :type logo_props: dict
    :param level: Level of the issue type
    :type level: int
    :param is_active: Whether the issue type is active
    :type is_active: bool
    :param is_default: Whether this is the default issue type
    :type is_default: bool
    :param deleted_at: Timestamp when the issue type was deleted
    :type deleted_at: Optional[str]
    :param workspace: UUID of the workspace this issue type belongs to
    :type workspace: str
    :param project: UUID of the project this issue type belongs to
    :type project: str
    :param created_by: UUID of the user who created the issue type
    :type created_by: str
    :param updated_by: UUID of the user who last updated the issue type
    :type updated_by: str
    :param created_at: Timestamp of when the issue type was created
    :type created_at: str
    :param updated_at: Timestamp of when the issue type was last updated
    :type updated_at: str
    :param external_id: External identifier for the issue type
    :type external_id: Optional[str]
    :param external_source: Source of the external issue type
    :type external_source: Optional[str]
    """
    id: str
    name: str
    description: str
    logo_props: dict
    level: int
    is_active: bool
    is_default: bool
    deleted_at: Optional[str]
    workspace: str 
    project: str
    created_by: str
    updated_by: str
    created_at: str
    updated_at: str
    external_id: Optional[str]
    external_source: Optional[str]

@dataclass
class IssueProperty:
    """
    Represents a Plane issue property.
    
    :param id: UUID of the issue property
    :type id: str
    :param created_at: Timestamp of when the property was created
    :type created_at: str
    :param updated_at: Timestamp of when the property was last updated
    :type updated_at: str
    :param deleted_at: Timestamp of when the property was deleted
    :type deleted_at: Optional[str]
    :param name: Name of the property
    :type name: str
    :param display_name: Display name of the property
    :type display_name: str
    :param description: Description of the property
    :type description: str
    :param logo_props: Properties for the property logo
    :type logo_props: dict
    :param sort_order: Sorting order of the property
    :type sort_order: float
    :param property_type: Type of the property (e.g., "OPTION")
    :type property_type: str
    :param relation_type: Type of relation if any
    :type relation_type: Optional[str]
    :param is_required: Whether the property is required
    :type is_required: bool
    :param default_value: Default value of the property
    :type default_value: list
    :param settings: Additional settings for the property
    :type settings: dict
    :param is_active: Whether the property is active
    :type is_active: bool
    :param is_multi: Whether multiple values are allowed
    :type is_multi: bool
    :param validation_rules: Rules for validating property values
    :type validation_rules: dict
    :param external_source: Source of external property
    :type external_source: Optional[str]
    :param external_id: External identifier
    :type external_id: Optional[str]
    :param created_by: UUID of the user who created the property
    :type created_by: str
    :param updated_by: UUID of the user who last updated the property
    :type updated_by: str
    :param workspace: UUID of the workspace this property belongs to
    :type workspace: str
    :param project: UUID of the project this property belongs to
    :type project: str
    :param issue_type: UUID of the issue type this property belongs to
    :type issue_type: str
    """
    id: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    name: str
    display_name: str
    description: str
    logo_props: dict
    sort_order: float
    property_type: str
    relation_type: Optional[str]
    is_required: bool
    default_value: list
    settings: dict
    is_active: bool
    is_multi: bool
    validation_rules: dict
    external_source: Optional[str]
    external_id: Optional[str]
    created_by: str
    updated_by: str
    workspace: str
    project: str
    issue_type: str

@dataclass
class PropertyOption:
    """
    Represents a Plane property option.
    
    :param id: UUID of the property option
    :type id: str
    :param created_at: Timestamp of when the option was created
    :type created_at: str 
    :param updated_at: Timestamp of when the option was last updated
    :type updated_at: str
    :param deleted_at: Timestamp of when the option was deleted
    :type deleted_at: Optional[str]
    :param name: Name of the property option
    :type name: str
    :param sort_order: Sorting order of the option
    :type sort_order: float
    :param description: Description of the property option
    :type description: str
    :param logo_props: Properties for the option logo
    :type logo_props: dict
    :param is_active: Whether the option is active
    :type is_active: bool
    :param is_default: Whether this is the default option
    :type is_default: bool
    :param external_source: Source of external option
    :type external_source: Optional[str]
    :param external_id: External identifier
    :type external_id: Optional[str]
    :param created_by: UUID of the user who created the option
    :type created_by: str
    :param updated_by: UUID of the user who last updated the option
    :type updated_by: str
    :param workspace: UUID of the workspace this option belongs to
    :type workspace: str
    :param project: UUID of the project this option belongs to
    :type project: str
    :param property: UUID of the property this option belongs to
    :type property: str
    :param parent: UUID of the parent option if any
    :type parent: Optional[str]
    """
    id: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    name: str
    sort_order: float
    description: str
    logo_props: dict
    is_active: bool
    is_default: bool
    external_source: Optional[str]
    external_id: Optional[str]
    created_by: str
    updated_by: str
    workspace: str
    project: str
    property: str
    parent: Optional[str]

@dataclass
class PropertyValue:
    """
    Represents a Plane property value.
    
    :param id: UUID of the property value
    :type id: str
    :param created_at: Timestamp of when the value was created
    :type created_at: str
    :param updated_at: Timestamp of when the value was last updated 
    :type updated_at: str
    :param deleted_at: Timestamp of when the value was deleted
    :type deleted_at: Optional[str]
    :param name: Name of the property value
    :type name: str
    :param sort_order: Sorting order of the value
    :type sort_order: float
    :param description: Description of the property value
    :type description: str
    :param logo_props: Properties for the value logo
    :type logo_props: dict
    :param is_active: Whether the value is active
    :type is_active: bool
    :param is_default: Whether this is the default value
    :type is_default: bool
    :param external_source: Source of external value
    :type external_source: Optional[str]
    :param external_id: External identifier
    :type external_id: Optional[str]
    :param created_by: UUID of the user who created the value
    :type created_by: str
    :param updated_by: UUID of the user who last updated the value
    :type updated_by: str
    :param workspace: UUID of the workspace this value belongs to
    :type workspace: str
    :param project_ids: List of project UUIDs this value belongs to
    :type project_ids: list[str]
    :param property: UUID of the property this value belongs to
    :type property: str
    :param parent: UUID of the parent value if any
    :type parent: Optional[str]
    """
    id: str
    created_at: str
    updated_at: str
    deleted_at: Optional[str]
    name: str
    sort_order: float
    description: str
    logo_props: dict
    is_active: bool
    is_default: bool
    external_source: Optional[str]
    external_id: Optional[str]
    created_by: str
    updated_by: str
    workspace: str
    project_ids: list[str]
    property: str
    parent: Optional[str]