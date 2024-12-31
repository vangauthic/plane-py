from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class CycleEndpoint(BaseEndpoint):
    async def get_cycles(self, project_id: str) -> list[Cycle]:
        """
        Fetch all cycles for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[Cycle]: List of Cycle objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/")
            
            if isinstance(response, dict) and 'results' in response:
                project_cycles = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            cycles = []
            for cycle_data in project_cycles:
                try:
                    cycle = Cycle(
                        id=cycle_data.get('id', ''),
                        created_at=cycle_data.get('created_at', ''),
                        updated_at=cycle_data.get('updated_at', ''),
                        name=cycle_data.get('name', ''),
                        description=cycle_data.get('description', ''),
                        start_date=cycle_data.get('start_date'),
                        end_date=cycle_data.get('end_date'),
                        view_props=cycle_data.get('view_props', {}),
                        sort_order=float(cycle_data.get('sort_order', 0.0)),
                        created_by=cycle_data.get('created_by', ''),
                        updated_by=cycle_data.get('updated_by', ''),
                        project=cycle_data.get('project', ''),
                        workspace=cycle_data.get('workspace', ''),
                        owned_by=cycle_data.get('owned_by', '')
                    )
                    cycles.append(cycle)
                except TypeError as e:
                    logging.error(f"Error creating cycle object: {e}")
                    logging.debug(f"Cycle data: {cycle_data}")
                    continue
                    
            return cycles
            
        except Exception as e:
            logging.error(f"Error getting cycles: {e}")
            raise PlaneError("Error fetching project cycles")
        
    async def get_cycle_details(self, project_id: str, cycle_id: str) -> Cycle:
        """
        Fetch specific cycle details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            cycle_id (str): ID of the cycle to fetch (Required)
            
        Returns:
            Cycle: Cycle object if found
        """
        try:
            cycle_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}"
            )
            
            if not isinstance(cycle_data, dict):
                raise ValueError(f"Unexpected response format: {type(cycle_data)}")

            return Cycle(
                id=cycle_data.get('id', ''),
                created_at=cycle_data.get('created_at', ''),
                updated_at=cycle_data.get('updated_at', ''),
                name=cycle_data.get('name', ''),
                description=cycle_data.get('description', ''),
                start_date=cycle_data.get('start_date'),
                end_date=cycle_data.get('end_date'),
                view_props=cycle_data.get('view_props', {}),
                sort_order=float(cycle_data.get('sort_order', 0.0)),
                created_by=cycle_data.get('created_by', ''),
                updated_by=cycle_data.get('updated_by', ''),
                project=cycle_data.get('project', ''),
                workspace=cycle_data.get('workspace', ''),
                owned_by=cycle_data.get('owned_by', '')
            )
            
        except Exception as e:
            logging.error(f"Error getting cycle details: {e}")
            raise PlaneError("Error fetching cycle details")
        
    async def create_cycle(self, name: str, project_id: str, **kwargs) -> Cycle:
        """
        Create a new cycle with provided data.

        Args:
            name (str): Name of the cycle (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid Cycle field to update

        Returns:
            Cycle: Created Cycle object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Cycle.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            cycle_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/", 
                json=filtered_data
            )
            
            return Cycle(
                id=cycle_data.get('id', ''),
                created_at=cycle_data.get('created_at', ''),
                updated_at=cycle_data.get('updated_at', ''),
                name=cycle_data.get('name', ''),
                description=cycle_data.get('description', ''),
                start_date=cycle_data.get('start_date'),
                end_date=cycle_data.get('end_date'),
                view_props=cycle_data.get('view_props', {}),
                sort_order=float(cycle_data.get('sort_order', 0.0)),
                created_by=cycle_data.get('created_by', ''),
                updated_by=cycle_data.get('updated_by', ''),
                project=cycle_data.get('project', ''),
                workspace=cycle_data.get('workspace', ''),
                owned_by=cycle_data.get('owned_by', '')
            )

        except Exception as e:
            logging.error(f"Error creating Cycle: {e}")
            raise PlaneError("Error creating cycle")
        
    async def update_cycle(self, name: str, project_id: str, cycle_id: str, **kwargs) -> Cycle:
        """
        Update a cycle with provided fields.

        Args:
            name: Name of the cycle (Required)
            project_id (str): The ID of the project to update (Required)
            cycle_id (str): The ID of the cycle to update (Required)
            **kwargs: Any valid Cycle field to update

        Returns:
            Cycle: Updated Cycle object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Cycle class
        valid_fields = Cycle.__annotations__.keys()
        filtered_data = {
            'name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            cycle_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return Cycle(
                id=cycle_data.get('id', ''),
                created_at=cycle_data.get('created_at', ''),
                updated_at=cycle_data.get('updated_at', ''),
                name=cycle_data.get('name', ''),
                description=cycle_data.get('description', ''),
                start_date=cycle_data.get('start_date'),
                end_date=cycle_data.get('end_date'),
                view_props=cycle_data.get('view_props', {}),
                sort_order=float(cycle_data.get('sort_order', 0.0)),
                created_by=cycle_data.get('created_by', ''),
                updated_by=cycle_data.get('updated_by', ''),
                project=cycle_data.get('project', ''),
                workspace=cycle_data.get('workspace', ''),
                owned_by=cycle_data.get('owned_by', '')
            )
            
        except Exception as e:
            logging.error(f"Error updating cycle: {e}")
            raise PlaneError("Error updating cycle")
        
    async def delete_cycle(self, project_id: str, cycle_id: str) -> bool:
        """
        Delete an existing cycle.

        Args:
            project_id: The ID of the project containing the cycle (Required)
            cycle_id: The ID of the cycle to be deleted (Required)

        Returns:
            bool: True if cycle was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting cycle: {e}")
            return False