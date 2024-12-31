from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class CycleIssueEndpoint(BaseEndpoint):
    async def get_cycle_issues(self, project_id: str, cycle_id: str) -> list[CycleIssue]:
        """
        Fetch all cycles for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            cycle_id (str): ID of the cycle (Required)

        Returns:
            list[CycleIssue]: List of CycleIssue objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/")
            
            if isinstance(response, dict) and 'results' in response:
                cycle_issues = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            issues = []
            for issue_data in cycle_issues:
                try:
                    issue = CycleIssue(
                        id=issue_data.get('id', ''),
                        sub_issues_count=issue_data.get('sub_issues_count', 0),
                        created_at=issue_data.get('created_at', ''),
                        updated_at=issue_data.get('updated_at', ''),
                        created_by=issue_data.get('created_by', ''),
                        updated_by=issue_data.get('updated_by', ''),
                        project=issue_data.get('project', ''),
                        workspace=issue_data.get('workspace', ''),
                        cycle=issue_data.get('cycle', ''),
                        issue=issue_data.get('issue', ''),
                    )
                    issues.append(issue)
                except TypeError as e:
                    logging.error(f"Error creating CycleIssue object: {e}")
                    logging.debug(f"Issue data: {issue_data}")
                    continue
                    
            return issues
            
        except Exception as e:
            logging.error(f"Error getting cycle issues: {e}")
            raise PlaneError("Error fetching cycle issues")
        
    async def create_cycle_issue(self, issues: list[str], project_id: str, cycle_id: str, **kwargs) -> CycleIssue:
        """
        Create a new cycle issue with provided data.

        Args:
            issues (list[str]): List of issue IDs to add to the cycle (Required)
            project_id (str): ID of the project (Required)
            cycle_id (str): ID of the cycle (Required)
            **kwargs: Any valid Issue field to update

        Returns:
            CycleIssue: Created CycleIssue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = CycleIssue.__annotations__.keys()
        filtered_data = {
            'issues': issues
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/", 
                json=filtered_data
            )

            if isinstance(data, list):
                if not data:
                    raise ValueError("Empty data received")
                data = data[0]
            
            processed_data = {
                'id': data.get('id', ''),
                'sub_issues_count': int(data.get('sub_issues_count', 0)),
                'created_at': data.get('created_at', ''),
                'updated_at': data.get('updated_at', ''),
                'created_by': data.get('created_by', ''),
                'updated_by': data.get('updated_by', ''),
                'project': data.get('project', ''),
                'workspace': data.get('workspace', ''),
                'cycle': data.get('cycle', ''),
                'issue': data.get('issue', '')
            }
            
            return CycleIssue(**processed_data)

        except Exception as e:
            logging.error(f"Error creating CycleIssue: {e}")
            raise PlaneError("Error creating cycle issue")
        
    async def delete_cycle_issue(self, project_id: str, cycle_id: str, issue_id: str) -> bool:
        """
        Delete an existing issue.

        Args:
            project_id: The ID of the project containing the module (Required)
            cycle_id: The ID of the cycle containing the issue (Required)
            issue_id: The ID of the issue to be deleted (Required)

        Returns:
            bool: True if issue was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting cycle issue: {e}")
            return False