from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class IssueEndpoint(BaseEndpoint):
    async def get_issues(self, project_id: str) -> list[Issue]:
        """
        Fetch all issues for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[Issue]: List of Issue objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/")
            
            if isinstance(response, dict) and 'results' in response:
                project_issues = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            issues = []
            for issue_data in project_issues:
                try:
                    issue = Issue(
                        id=issue_data.get('id', ''),
                        created_at=issue_data.get('created_at', ''),
                        updated_at=issue_data.get('updated_at', ''),
                        estimate_point=issue_data.get('estimate_point'),
                        name=issue_data.get('name', ''),
                        description_html=issue_data.get('description_html', ''),
                        description_stripped=issue_data.get('description_stripped', ''),
                        priority=issue_data.get('priority', ''),
                        start_date=issue_data.get('start_date'),
                        target_date=issue_data.get('target_date'),
                        sequence_id=issue_data.get('sequence_id', 0),
                        sort_order=float(issue_data.get('sort_order', 0.0)),
                        completed_at=issue_data.get('completed_at'),
                        archived_at=issue_data.get('archived_at'),
                        is_draft=issue_data.get('is_draft', False),
                        created_by=issue_data.get('created_by', ''),
                        updated_by=issue_data.get('updated_by', ''),
                        project=issue_data.get('project', ''),
                        workspace=issue_data.get('workspace', ''),
                        parent=issue_data.get('parent'),
                        state=issue_data.get('state', ''),
                        assignees=issue_data.get('assignees', []),
                        labels=issue_data.get('labels', [])
                    )
                    issues.append(issue)
                except TypeError as e:
                    logging.error(f"Error creating issue object: {e}")
                    logging.debug(f"Issue data: {issue_data}")
                    continue
                    
            return issues
            
        except Exception as e:
            logging.error(f"Error getting issues: {e}")
            raise PlaneError("Error fetching project issues")
        
    async def get_issue_details(self, project_id: str, issue_id: str) -> Issue:
        """
        Fetch specific issue details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue to fetch (Required)
            
        Returns:
            Issue: Issue object if found
        """
        try:
            issue_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}"
            )
            
            if not isinstance(issue_data, dict):
                raise ValueError(f"Unexpected response format: {type(issue_data)}")

            return Issue(
                id=issue_data.get('id', ''),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                estimate_point=issue_data.get('estimate_point'),
                name=issue_data.get('name', ''),
                description_html=issue_data.get('description_html', ''),
                description_stripped=issue_data.get('description_stripped', ''),
                priority=issue_data.get('priority', ''),
                start_date=issue_data.get('start_date'),
                target_date=issue_data.get('target_date'),
                sequence_id=issue_data.get('sequence_id', 0),
                sort_order=float(issue_data.get('sort_order', 0.0)),
                completed_at=issue_data.get('completed_at'),
                archived_at=issue_data.get('archived_at'),
                is_draft=issue_data.get('is_draft', False),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
                parent=issue_data.get('parent'),
                state=issue_data.get('state', ''),
                assignees=issue_data.get('assignees', []),
                labels=issue_data.get('labels', [])
            )
            
        except Exception as e:
            logging.error(f"Error getting issue details: {e}")
            raise PlaneError("Error fetching issue details")
        
    async def create_issue(self, name: str, project_id: str, **kwargs) -> Issue:
        """
        Create a new issue with provided data.

        Args:
            name (str): Name of the issue (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid Issue field to update

        Returns:
            Issue: Created Issue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Issue.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            issue_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/", 
                json=filtered_data
            )
            
            return Issue(
                id=issue_data.get('id', ''),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                estimate_point=issue_data.get('estimate_point'),
                name=issue_data.get('name', ''),
                description_html=issue_data.get('description_html', ''),
                description_stripped=issue_data.get('description_stripped', ''),
                priority=issue_data.get('priority', ''),
                start_date=issue_data.get('start_date'),
                target_date=issue_data.get('target_date'),
                sequence_id=issue_data.get('sequence_id', 0),
                sort_order=float(issue_data.get('sort_order', 0.0)),
                completed_at=issue_data.get('completed_at'),
                archived_at=issue_data.get('archived_at'),
                is_draft=issue_data.get('is_draft', False),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
                parent=issue_data.get('parent'),
                state=issue_data.get('state', ''),
                assignees=issue_data.get('assignees', []),
                labels=issue_data.get('labels', [])
            )

        except Exception as e:
            logging.error(f"Error creating Issue: {e}")
            raise PlaneError("Error creating issue")
        
    async def update_issue(self, name: str, project_id: str, issue_id: str, **kwargs) -> Issue:
        """
        Update an issue with provided fields.

        Args:
            name: Name of the issue (Required)
            project_id (str): The ID of the project to update (Required)
            issue_id (str): The ID of the issue to update (Required)
            **kwargs: Any valid Issue field to update

        Returns:
            Issue: Updated Issue object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = Issue.__annotations__.keys()
        filtered_data = {
            'name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            issue_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return Issue(
                id=issue_data.get('id', ''),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                estimate_point=issue_data.get('estimate_point'),
                name=issue_data.get('name', ''),
                description_html=issue_data.get('description_html', ''),
                description_stripped=issue_data.get('description_stripped', ''),
                priority=issue_data.get('priority', ''),
                start_date=issue_data.get('start_date'),
                target_date=issue_data.get('target_date'),
                sequence_id=issue_data.get('sequence_id', 0),
                sort_order=float(issue_data.get('sort_order', 0.0)),
                completed_at=issue_data.get('completed_at'),
                archived_at=issue_data.get('archived_at'),
                is_draft=issue_data.get('is_draft', False),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
                parent=issue_data.get('parent'),
                state=issue_data.get('state', ''),
                assignees=issue_data.get('assignees', []),
                labels=issue_data.get('labels', [])
            )
            
        except Exception as e:
            logging.error(f"Error updating issue: {e}")
            raise PlaneError("Error updating issue")
        
    async def delete_issue(self, project_id: str, issue_id: str) -> bool:
        """
        Delete an existing issue.

        Args:
            project_id: The ID of the project containing the issue (Required)
            issue_id: The ID of the issue to be deleted (Required)

        Returns:
            bool: True if issue was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting issue: {e}")
            return False