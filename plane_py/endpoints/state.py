from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class StateEndpoint(BaseEndpoint):
    async def get_states(self, project_id: str) -> list[State]:
        """
        Fetch all states for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[State]: List of State objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/")
            
            if isinstance(response, dict) and 'results' in response:
                project_states = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            states = []
            for state_data in project_states:
                # Ensure workspace_slug is set from current client
                state_data['workspace_slug'] = self.workspace_slug
                
                try:
                    # Create State object with the complete data
                    state = State(
                        id=state_data.get('id', ''),
                        created_at=state_data.get('created_at', ''),
                        updated_at=state_data.get('updated_at', ''),
                        name=state_data.get('name', ''),
                        description=state_data.get('description', ''),
                        color=state_data.get('color', ''),
                        workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                        sequence=str(state_data.get('sequence', '')),
                        group=state_data.get('group', ''),
                        default=state_data.get('default', False),
                        created_by=state_data.get('created_by', ''),
                        updated_by=state_data.get('updated_by', ''),
                        project=state_data.get('project', ''),
                        workspace=state_data.get('workspace', '')
                    )
                    states.append(state)
                except TypeError as e:
                    logging.error(f"Error getting project state: {e}")
                    logging.info(f"Data: {state_data}")
                    continue
                    
            return states
            
        except Exception as e:
            logging.error(f"Error getting states: {e}")
            raise PlaneError("Error fetching project states")
        
    async def get_state_details(self, project_id: str, state_id: str) -> State:
        """
        Fetch specific state details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            state_id (str): ID of the state to fetch (Required)
            
        Returns:
            State: State object if found
        """
        try:
            state_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/{state_id}/"
            )
            
            if not isinstance(state_data, dict):
                raise ValueError(f"Unexpected response format: {type(state_data)}")
            
            # Create State object with the complete data
            return State(
                id=state_data.get('id', ''),
                created_at=state_data.get('created_at', ''),
                updated_at=state_data.get('updated_at', ''),
                name=state_data.get('name', ''),
                description=state_data.get('description', ''),
                color=state_data.get('color', ''),
                workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                sequence=str(state_data.get('sequence', '')),
                group=state_data.get('group', ''),
                default=state_data.get('default', False),
                created_by=state_data.get('created_by', ''),
                updated_by=state_data.get('updated_by', ''),
                project=state_data.get('project', ''),
                workspace=state_data.get('workspace', '')
            )
            
        except Exception as e:
            logging.error(f"Error getting state details: {e}")
            raise PlaneError("Error fetching state details")
        
    async def create_state(self, name: str, color: str, project_id: str, **kwargs) -> State:
        """
        Create a new state with provided data.

        Args:
            name (str): Name of the state (Required)
            color (str): Color of the state (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid State field to update

        Returns:
            State: Created State object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = State.__annotations__.keys()
        filtered_data = {
            'name': name,
            'color': color
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            state_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/", 
                json=filtered_data
            )
            
            return State(
                id=state_data.get('id', ''),
                created_at=state_data.get('created_at', ''),
                updated_at=state_data.get('updated_at', ''),
                name=state_data.get('name', ''),
                description=state_data.get('description', ''),
                color=state_data.get('color', ''),
                workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                sequence=str(state_data.get('sequence', '')),
                group=state_data.get('group', ''),
                default=state_data.get('default', False),
                created_by=state_data.get('created_by', ''),
                updated_by=state_data.get('updated_by', ''),
                project=state_data.get('project', ''),
                workspace=state_data.get('workspace', '')
            )

        except Exception as e:
            logging.error(f"Error creating State: {e}")
            raise PlaneError("Error creating state")
        
    async def update_state(self, project_id: str, state_id: str, **kwargs) -> State:
        """
        Update a state with provided fields.

        Args:
            project_id (str): The ID of the project to update (Required)
            state_id (str): The ID of the state to update (Required)
            **kwargs: Any valid State field to update

        Returns:
            State: Updated State object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = State.__annotations__.keys()
        
        # Filter out any invalid fields from kwargs
        filtered_data = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            state_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/{state_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return State(
                id=state_data.get('id', ''),
                created_at=state_data.get('created_at', ''),
                updated_at=state_data.get('updated_at', ''),
                name=state_data.get('name', ''),
                description=state_data.get('description', ''),
                color=state_data.get('color', ''),
                workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                sequence=str(state_data.get('sequence', '')),
                group=state_data.get('group', ''),
                default=state_data.get('default', False),
                created_by=state_data.get('created_by', ''),
                updated_by=state_data.get('updated_by', ''),
                project=state_data.get('project', ''),
                workspace=state_data.get('workspace', '')
            )
            
        except Exception as e:
            logging.error(f"Error updating state: {e}")
            raise PlaneError("Error updating state")
        
    async def delete_state(self, project_id: str, state_id: str) -> bool:
        """
        Delete an existing state.

        Args:
            project_id: The ID of the project containing the state (Required)
            state_id: The ID of the state to delete (Required)

        Returns:
            bool: True if state was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/{state_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting state: {e}")
            return False