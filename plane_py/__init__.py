from typing import TYPE_CHECKING, List, Union, Dict, Optional, Any

# Import actual types for runtime
from ._types import Project, State
from .api import PlaneClient as _BaseClient

# Create unified type exports
PlaneType = Union[Project, State]

class PlaneClient(_BaseClient):
    """
    Main client class with type hints for better IDE support
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
        
        # Internal method
        async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]: ...

# Export everything needed
__all__ = [
    "PlaneClient",
    "Project",
    "State",
    "PlaneType"
]