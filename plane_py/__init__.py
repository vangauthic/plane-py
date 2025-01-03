from typing import TYPE_CHECKING, List, Union, Dict, Optional, Any

# Import actual types for runtime
from ._types import *
from .api import PlaneClient as _BaseClient

# Create unified type exports
PlaneType = Union[
    Project,
    State,
    Label,
    Link,
    Issue,
    IssueActivity,
    IssueComment,
    Module,
    ModuleIssue,
    Cycle,
    CycleIssue,
    IntakeIssue,
    IssueType,
    IssueProperty,
    PropertyOption,
    PropertyValue
]

class PlaneClient(_BaseClient):
    """
    FULL DOCUMENTATION AVAILABLE AT https://developers.plane.so/api-reference/
    """
    if TYPE_CHECKING:
        # Project methods
        async def get_projects(self) -> List[Project]: ...
        async def get_project_details(self, project_id: str) -> Project: ...
        async def create_project(self, name: str, identifier: str, **kwargs) -> Project: ...
        async def update_project(self, project_id: str, **kwargs) -> Project: ...
        async def delete_project(self, project_id: str) -> bool: ...
        
        # State methods
        async def get_states(self, project_id: str) -> List[State]: ...
        async def get_state_details(self, project_id: str, state_id: str) -> State: ...
        async def create_state(self, name: str, color: str, project_id: str, **kwargs) -> State: ...
        async def update_state(self, project_id: str, state_id: str, **kwargs) -> State: ...
        async def delete_state(self, project_id: str, state_id: str) -> bool: ...

        # Label methods
        async def get_labels(self, project_id: str) -> List[Label]: ...
        async def get_label_details(self, project_id: str, label_id: str) -> Label: ...
        async def create_label(self, name: str, project_id: str, **kwargs) -> Label: ...
        async def update_label(self, name: str, project_id: str, label_id: str, **kwargs) -> Label: ...
        async def delete_label(self, project_id: str, label_id: str) -> bool: ...

        # Link methods
        async def get_links(self, project_id: str, issue_id: str) -> List[Link]: ...
        async def get_link_details(self, project_id: str, issue_id: str, link_id: str) -> Link: ...
        async def create_link(self, url: str, project_id: str, issue_id: str, **kwargs) -> Link: ...
        async def update_link(self, project_id: str, issue_id: str, link_id: str, **kwargs) -> Link: ...
        async def delete_link(self, project_id: str, issue_id: str, link_id: str) -> bool: ...

        # Issue methods
        async def get_issues(self, project_id: str) -> List[Issue]: ...
        async def get_issue_details(self, project_id: str, issue_id: str) -> Issue: ...
        async def create_issue(self, name: str, project_id: str, **kwargs) -> Issue: ...
        async def update_issue(self, name: str, project_id: str, issue_id: str, **kwargs) -> Issue: ...
        async def delete_issue(self, project_id: str, issue_id: str) -> bool: ...

        # IssueActivity methods
        async def get_issue_activity(self, project_id: str, issue_id: str) -> List[IssueActivity]: ...
        async def get_activity_details(self, project_id: str, issue_id: str, activity_id: str) -> IssueActivity: ...

        # IssueComment methods
        async def get_issue_comments(self, project_id: str, issue_id: str) -> List[IssueComment]: ...
        async def get_comment_details(self, project_id: str, issue_id: str, comment_id: str) -> IssueComment: ...
        async def create_comment(self, url: str, project_id: str, issue_id: str, **kwargs) -> IssueComment: ...
        async def update_comment(self, project_id: str, issue_id: str, comment_id: str, **kwargs) -> IssueComment: ...
        async def delete_comment(self, project_id: str, issue_id: str, comment_id: str) -> bool: ...

        # Module methods
        async def get_modules(self, project_id: str) -> List[Module]: ...
        async def get_module_details(self, project_id: str, module_id: str) -> Module: ...
        async def create_module(self, name: str, project_id: str, **kwargs) -> Module: ...
        async def update_module(self, name: str, project_id: str, module_id: str, **kwargs) -> Module: ...
        async def delete_module(self, project_id: str, module_id: str) -> bool: ...

        # ModuleIssue methods
        async def get_module_issues(self, project_id: str, module_id: str) -> List[ModuleIssue]: ...
        async def create_module_issue(self, issues: list[str], project_id: str, module_id: str, **kwargs) -> ModuleIssue: ...
        async def delete_module_issue(self, project_id: str, module_id: str, issue_id: str) -> bool: ...

        # Cycle methods
        async def get_cycles(self, project_id: str) -> List[Cycle]: ...
        async def get_cycle_details(self, project_id: str, cycle_id: str) -> Cycle: ...
        async def create_cycle(self, name: str, project_id: str, **kwargs) -> Cycle: ...
        async def update_cycle(self, name: str, project_id: str, cycle_id: str, **kwargs) -> Cycle: ...
        async def delete_cycle(self, project_id: str, cycle_id: str) -> bool: ...

        # CycleIssue methods
        async def get_cycle_issues(self, project_id: str, cycle_id: str) -> List[CycleIssue]: ...
        async def create_cycle_issue(self, issues: list[str], project_id: str, cycle_id: str, **kwargs) -> CycleIssue: ...
        async def delete_cycle_issue(self, project_id: str, cycle_id: str, issue_id: str) -> bool: ...

        # IntakeIssue methods
        async def get_intake_issues(self, project_id: str) -> List[IntakeIssue]: ...
        async def get_intake_issue_details(self, project_id: str, issue_id: str) -> IntakeIssue: ...
        async def create_intake_issue(self, issue: dict, project_id: str) -> IntakeIssue: ...
        async def update_intake_issue(self, issue: dict, project_id: str, issue_id: str) -> IntakeIssue: ...
        async def delete_intake_issue(self, project_id: str, intake_id: str, issue_id: str) -> bool: ...

        # IssueType methods
        async def get_issue_types(self, project_id: str) -> List[IssueType]: ...
        async def get_type_details(self, project_id: str, type_id: str) -> IssueType: ...
        async def create_type(self, name: str, project_id: str, **kwargs) -> IssueType: ...
        async def update_type(self, name: str, project_id: str, type_id: str, **kwargs) -> IssueType: ...
        async def delete_issue_type(self, project_id: str, type_id: str) -> bool: ...

        # IssueProperty methods
        async def get_properties(self, project_id: str, type_id: str) -> List[IssueProperty]: ...
        async def get_property_details(self, project_id: str, type_id: str, property_id: str) -> IssueProperty: ...
        async def create_property(self, name: str, project_id: str, type_id: str, **kwargs) -> IssueProperty: ...
        async def update_property(self, project_id: str, type_id: str, property_id: str, **kwargs) -> IssueProperty: ...
        async def delete_property(self, project_id: str, type_id: str, property_id: str) -> bool: ...

        # PropertyOption methods
        async def get_property_options(self, project_id: str, property_id: str) -> List[PropertyOption]: ...
        async def get_option_details(self, project_id: str, property_id: str, option_id: str) -> PropertyOption: ...
        async def create_option(self, name: str, project_id: str, property_id: str, **kwargs) -> PropertyOption: ...
        async def update_option(self, project_id: str, property_id: str, option_id: str, **kwargs) -> PropertyOption: ...
        async def delete_option(self, project_id: str, property_id: str, option_id: str) -> bool: ...

        # PropertyValue methods
        async def get_property_values(self, project_id: str, property_id: str, issue_id: str) -> List[PropertyValue]: ...
        async def create_value(self, values: list, project_id: str, issue_id: str, property_id: str) -> PropertyValue: ...
        
        # Internal method
        async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]: ...

# Export everything needed
__all__ = [
    "PlaneClient",
    "Project",
    "State",
    "Label",
    "Link",
    "Issue",
    "IssueActivity",
    "IssueComment",
    "Module",
    "ModuleIssue",
    "Cycle",
    "CycleIssue",
    "IntakeIssue",
    "IssueType",
    "IssueProperty",
    "PropertyOption",
    "PropertyValue",
    "PlaneType"
]