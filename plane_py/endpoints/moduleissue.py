from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class ModuleIssueEndpoint(BaseEndpoint):
    async def get_module_issues(self, project_id: str, module_id: str) -> list[ModuleIssue]:
        """
        Fetch all issues for a module.
        
        Args:
            project_id (str): ID of the project (Required)
            module_id (str): ID of the issue (Required)

        Returns:
            list[ModuleIssue]: List of ModuleIssue objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/")
            
            if isinstance(response, dict) and 'results' in response:
                module_issues = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            issues = []
            for issue_data in module_issues:
                try:
                    issue = ModuleIssue(
                        id=issue_data.get('id', ''),
                        sub_issues_count=issue_data.get('sub_issues_count', 0),
                        created_at=issue_data.get('created_at', ''),
                        updated_at=issue_data.get('updated_at', ''),
                        created_by=issue_data.get('created_by', ''),
                        updated_by=issue_data.get('updated_by', ''),
                        project=issue_data.get('project', ''),
                        workspace=issue_data.get('workspace', ''),
                        module=issue_data.get('module', ''),
                        issue=issue_data.get('issue', ''),
                    )
                    issues.append(issue)
                except TypeError as e:
                    logging.error(f"Error creating ModelIssue object: {e}")
                    logging.debug(f"Issue data: {issue_data}")
                    continue
                    
            return issues
            
        except Exception as e:
            logging.error(f"Error getting module issues: {e}")
            raise PlaneError("Error fetching module issues")
        
    async def create_module_issue(self, issues: list[str], project_id: str, module_id: str, **kwargs) -> ModuleIssue:
        """
        Create a new module issue with provided data.

        Args:
            issues (list[str]): List of issue IDs to add to the module (Required)
            project_id (str): ID of the project (Required)
            module_id (str): ID of the module (Required)
            **kwargs: Any valid Issue field to update

        Returns:
            ModuleIssue: Created ModuleIssue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = ModuleIssue.__annotations__.keys()
        filtered_data = {
            'issues': issues
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/", 
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
                'module': data.get('module', ''),
                'issue': data.get('issue', '')
            }
            
            return ModuleIssue(**processed_data)

        except Exception as e:
            logging.error(f"Error creating ModuleIssue: {e}")
            raise PlaneError("Error creating module issue")
        
    async def delete_module_issue(self, project_id: str, module_id: str, issue_id: str) -> bool:
        """
        Delete an existing issue.

        Args:
            project_id: The ID of the project containing the module (Required)
            module_id: The ID of the module containing the issue (Required)
            issue_id: The ID of the issue to be deleted (Required)

        Returns:
            bool: True if issue was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting module issue: {e}")
            return False