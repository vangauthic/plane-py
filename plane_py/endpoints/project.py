from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class ProjectEndpoint(BaseEndpoint):
    async def get_projects(self) -> list[Project]:
        """
        Fetch all projects.
        
        Returns:
            list[Project]: List of Project objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/")
            
            # API returns dict with 'results' key containing projects list
            if isinstance(response, dict) and 'results' in response:
                projects_data = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            # Get valid fields from Project class
            valid_fields = Project.__annotations__.keys()
            
            # Filter project data to only include valid fields
            projects = []
            for project_data in projects_data:
                filtered_data = {k: v for k, v in project_data.items() if k in valid_fields}
                try:
                    projects.append(Project(**filtered_data))
                except TypeError as e:
                    logging.error(f"Error getting project: {e}")
                    logging.info(f"Data: {filtered_data}")
                    continue
            
            return projects
            
        except Exception as e:
            logging.error(f"Error getting projects: {e}")
            return []
        
    async def get_project_details(self, project_id: str) -> Project:
        """
        Fetch details for a specific project.
        
        Args:
            project_id (str): The ID of the project to fetch (Required)
            
        Returns:
            Project: Project object with details
            
        Raises:
            ValueError: If response format is unexpected
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/")
            
            # Get valid fields from Project class
            valid_fields = Project.__annotations__.keys()
            
            # Filter project data to only include valid fields
            filtered_data = {k: v for k, v in response.items() if k in valid_fields}
            
            return Project(**filtered_data)
            
        except Exception as e:
            logging.error(f"Error fetching project details: {e}")
            raise PlaneError("Error fetching project details")

    async def update_project(self, project_id: str, **kwargs) -> Project:
        """
        Update a project with provided fields.

        Args:
            project_id (str): The ID of the project to update (Required)
            **kwargs: Any valid Project field to update

        Returns:
            Project: Updated Project object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = Project.__annotations__.keys()
        
        # Filter out any invalid fields from kwargs
        filtered_data = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            response = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return Project(**filtered_response)
            
        except Exception as e:
            logging.error(f"Error updating project: {e}")
            raise PlaneError("Error updating project")

    async def create_project(self, name: str, identifier: str, **kwargs) -> Project:
        """
        Create a new project with provided data.

        Args:
            name (str): Name of the project (Required)
            identifier (str): Identifier of the project (Required)
            **kwargs: Any valid Project field to update

        Returns:
            Project: Created Project object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Project.__annotations__.keys()
        filtered_data = {
            'name': name,
            'identifier': identifier
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            response = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/", 
                json=filtered_data
            )
            
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return Project(**filtered_response)

        except Exception as e:
            logging.error(f"Error creating Project: {e}")
            raise PlaneError("Error creating project")

    async def delete_project(self, project_id: str) -> bool:
        """
        Delete an existing project.

        Args:
            project_id: The ID of the project to delete (Required)

        Returns:
            bool: True if project was deleted successfully, False otherwise
        """

        try:
            response = await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting project: {e}")
            return False