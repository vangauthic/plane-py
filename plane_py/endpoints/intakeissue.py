from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class IntakeIssueEndpoint(BaseEndpoint):
    async def get_intake_issues(self, project_id: str) -> list[IntakeIssue]:
        """
        Fetch all intake issues for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[IntakeIssue]: List of IntakeIssue objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/")
            
            if isinstance(response, dict) and 'results' in response:
                intake_issues = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            issues = []
            for issue_data in intake_issues:
                try:
                    issue = IntakeIssue(
                        id=issue_data.get('id', ''),
                        pending_issue_count=issue_data.get('pending_issue_count', 0),
                        created_at=issue_data.get('created_at', ''),
                        updated_at=issue_data.get('updated_at', ''),
                        name=issue_data.get('name', ''),
                        description=issue_data.get('description', ''),
                        is_default=issue_data.get('is_default', False),
                        view_props=issue_data.get('view_props', {}),
                        created_by=issue_data.get('created_by', ''),
                        updated_by=issue_data.get('updated_by', ''),
                        project=issue_data.get('project', ''),
                        workspace=issue_data.get('workspace', ''),
                    )
                    issues.append(issue)
                except TypeError as e:
                    logging.error(f"Error creating IntakeIssue object: {e}")
                    logging.debug(f"Issue data: {issue_data}")
                    continue
                    
            return issues
            
        except Exception as e:
            logging.error(f"Error getting IntakeIssues: {e}")
            raise PlaneError("Error fetching project IntakeIssues")
        
    async def get_intake_issue_details(self, project_id: str, issue_id: str) -> IntakeIssue:
        """
        Fetch specific IntakeIssue details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue to fetch (Required)
            
        Returns:
            IntakeIssue: IntakeIssue object if found
        """
        try:
            issue_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/{issue_id}"
            )
            
            if not isinstance(issue_data, dict):
                raise ValueError(f"Unexpected response format: {type(issue_data)}")

            return IntakeIssue(
                id=issue_data.get('id', ''),
                pending_issue_count=issue_data.get('pending_issue_count', 0),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                name=issue_data.get('name', ''),
                description=issue_data.get('description', ''),
                is_default=issue_data.get('is_default', False),
                view_props=issue_data.get('view_props', {}),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
            )
        
        except Exception as e:
            logging.error(f"Error getting issue details: {e}")
            raise PlaneError("Error fetching issue details")
        
    async def create_intake_issue(self, issue: dict, project_id: str) -> IntakeIssue:
        """
        Create a new IntakeIssue with provided data.

        Args:
            issue (dict): Information to upload for the issue (Required)
            project_id (str): ID of the project (Required)

        Returns:
            IntakeIssue: Created IntakeIssue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IntakeIssue.__annotations__.keys()
        filtered_data = {"issue":{
            'name': issue.get('name', 'N/A')
        }}

        filtered_data["issue"].update({k: v for k, v in issue.items() if k in valid_fields})

        try:
            issue_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/", 
                json=filtered_data
            )
            
            return IntakeIssue(
                id=issue_data.get('id', ''),
                pending_issue_count=issue_data.get('pending_issue_count', 0),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                name=issue_data.get('name', ''),
                description=issue_data.get('description', ''),
                is_default=issue_data.get('is_default', False),
                view_props=issue_data.get('view_props', {}),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
            )

        except Exception as e:
            logging.error(f"Error creating IntakeIssue: {e}")
            raise PlaneError("Error creating IntakeIssue")
        
    async def update_intake_issue(self, issue: dict, project_id: str, issue_id: str) -> IntakeIssue:
        """
        Update a IntakeIssue with provided data.

        Args:
            issue (dict): Information to upload for the issue (Required)
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue to update (Required)

        Returns:
            IntakeIssue: Updated IntakeIssue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IntakeIssue.__annotations__.keys()
        filtered_data = {"issue":{
            'name': issue.get('name', 'N/A')
        }}

        filtered_data["issue"].update({k: v for k, v in issue.items() if k in valid_fields})

        try:
            issue_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/{issue_id}", 
                json=filtered_data
            )
            
            return IntakeIssue(
                id=issue_data.get('id', ''),
                pending_issue_count=issue_data.get('pending_issue_count', 0),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                name=issue_data.get('name', ''),
                description=issue_data.get('description', ''),
                is_default=issue_data.get('is_default', False),
                view_props=issue_data.get('view_props', {}),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
            )

        except Exception as e:
            logging.error(f"Error creating IntakeIssue: {e}")
            raise PlaneError("Error creating IntakeIssue")
        
    async def delete_intake_issue(self, project_id: str, intake_id: str, issue_id: str) -> bool:
        """
        Delete an existing cycle.

        Args:
            project_id: The ID of the project containing the intake (Required)
            intake_id: The ID of the intake containing the issue (Required)
            issue_id: The ID of the issue to be deleted (Required)

        Returns:
            bool: True if issue was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/{issue_id}"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting IntakeIssue: {e}")
            return False