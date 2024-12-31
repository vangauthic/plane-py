from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class IssueTypeEndpoint(BaseEndpoint):
    async def get_issue_types(self, project_id: str) -> list[IssueType]:
        """
        Fetch all issue types for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[IssueType]: List of IssueType objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_types = response['results']
            elif isinstance(response, list):
                issue_types = response
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            types = []
            for type_data in issue_types:
                try:
                    type_add = IssueType(
                        id=type_data.get('id', ''),
                        name=type_data.get('name', ''),
                        description=type_data.get('description', ''),
                        logo_props=type_data.get('logo_props', {}),
                        level=type_data.get('level', 0),
                        is_active=type_data.get('is_active', True),
                        is_default=type_data.get('is_default', False),
                        deleted_at=type_data.get('deleted_at', ''),
                        workspace=type_data.get('workspace', ''),
                        project=type_data.get('project', ''),
                        created_by=type_data.get('created_by', ''),
                        updated_by=type_data.get('updated_by', ''),
                        created_at=type_data.get('created_at', ''),
                        updated_at=type_data.get('updated_at', ''),
                        external_id=type_data.get('external_id', ''),
                        external_source=type_data.get('external_source', '')
                    )
                    types.append(type_add)
                except TypeError as e:
                    logging.error(f"Error creating IssueType object: {e}")
                    logging.debug(f"IssueType data: {type_add}")
                    continue
                    
            return types
            
        except Exception as e:
            logging.error(f"Error getting IssueTypes: {e}")
            raise PlaneError("Error fetching project IssueTypes")
        
    async def get_type_details(self, project_id: str, type_id: str) -> IssueType:
        """
        Fetch specific IntakeIssue details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            type_id (str): ID of the issue type to fetch (Required)
            
        Returns:
            IssueType: IssueType object if found
        """
        try:
            type_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/"
            )
            
            if not isinstance(type_data, dict):
                raise ValueError(f"Unexpected response format: {type(type_data)}")

            return IssueType(
                id=type_data.get('id', ''),
                name=type_data.get('name', ''),
                description=type_data.get('description', ''),
                logo_props=type_data.get('logo_props', {}),
                level=type_data.get('level', 0),
                is_active=type_data.get('is_active', True),
                is_default=type_data.get('is_default', False),
                deleted_at=type_data.get('deleted_at', ''),
                workspace=type_data.get('workspace', ''),
                project=type_data.get('project', ''),
                created_by=type_data.get('created_by', ''),
                updated_by=type_data.get('updated_by', ''),
                created_at=type_data.get('created_at', ''),
                updated_at=type_data.get('updated_at', ''),
                external_id=type_data.get('external_id', ''),
                external_source=type_data.get('external_source', '')
            )
        
        except Exception as e:
            logging.error(f"Error getting issu type details: {e}")
            raise PlaneError("Error fetching issue type details")
        
    async def create_type(self, name: str, project_id: str, **kwargs) -> IssueType:
        """
        Create a new IssueType with provided data.

        Args:
            name (str): Name of the type (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid IssueType field to update

        Returns:
            IssueType: Created IssueType object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IssueType.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            type_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/", 
                json=filtered_data
            )
            
            return IssueType(
                id=type_data.get('id', ''),
                name=type_data.get('name', ''),
                description=type_data.get('description', ''),
                logo_props=type_data.get('logo_props', {}),
                level=type_data.get('level', 0),
                is_active=type_data.get('is_active', True),
                is_default=type_data.get('is_default', False),
                deleted_at=type_data.get('deleted_at', ''),
                workspace=type_data.get('workspace', ''),
                project=type_data.get('project', ''),
                created_by=type_data.get('created_by', ''),
                updated_by=type_data.get('updated_by', ''),
                created_at=type_data.get('created_at', ''),
                updated_at=type_data.get('updated_at', ''),
                external_id=type_data.get('external_id', ''),
                external_source=type_data.get('external_source', '')
            )

        except Exception as e:
            logging.error(f"Error creating IssueType: {e}")
            raise PlaneError("Error creating issue type")
        
    async def update_type(self, name: str, project_id: str, type_id: str, **kwargs) -> IssueType:
        """
        Update an IssueType with provided data.

        Args:
            name (str): Name of the type (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid IssueType field to update

        Returns:
            IssueType: Updated IssueType object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IssueType.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            type_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/", 
                json=filtered_data
            )
            
            return IssueType(
                id=type_data.get('id', ''),
                name=type_data.get('name', ''),
                description=type_data.get('description', ''),
                logo_props=type_data.get('logo_props', {}),
                level=type_data.get('level', 0),
                is_active=type_data.get('is_active', True),
                is_default=type_data.get('is_default', False),
                deleted_at=type_data.get('deleted_at', ''),
                workspace=type_data.get('workspace', ''),
                project=type_data.get('project', ''),
                created_by=type_data.get('created_by', ''),
                updated_by=type_data.get('updated_by', ''),
                created_at=type_data.get('created_at', ''),
                updated_at=type_data.get('updated_at', ''),
                external_id=type_data.get('external_id', ''),
                external_source=type_data.get('external_source', '')
            )

        except Exception as e:
            logging.error(f"Error creating IssueType: {e}")
            raise PlaneError("Error creating issue type")
        
    async def delete_issue_type(self, project_id: str, type_id: str) -> bool:
        """
        Delete an existing cycle.

        Args:
            project_id: The ID of the project containing the intake (Required)
            type_id: The ID of the type to be deleted (Required)

        Returns:
            bool: True if issue type was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting IssueType: {e}")
            return False