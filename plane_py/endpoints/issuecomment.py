from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class IssueCommentEndpoint(BaseEndpoint):
    async def get_issue_comments(self, project_id: str, issue_id: str) -> list[IssueComment]:
        """
        Fetch all comments for an issue.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)

        Returns:
            list[IssueComment]: List of IssueComment objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_comments = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            comments = []
            for comment_data in issue_comments:
                try:
                    comment = IssueComment(
                        id=comment_data.get('id', ''),
                        created_at=comment_data.get('created_at', ''),
                        updated_at=comment_data.get('updated_at', ''),
                        comment_stripped=comment_data.get('comment_stripped', ''),
                        comment_json=comment_data.get('comment_json', {}),
                        comment_html=comment_data.get('comment_html', ''),
                        attachments=comment_data.get('attachments', []),
                        access=comment_data.get('access', ''),
                        created_by=comment_data.get('created_by', ''),
                        updated_by=comment_data.get('updated_by', ''),
                        issue=comment_data.get('issue', ''),
                        project=comment_data.get('project', ''),
                        workspace=comment_data.get('workspace', ''),
                        actor=comment_data.get('actor', '')
                    )
                    comments.append(comment)
                except TypeError as e:
                    logging.error(f"Error creating comment object: {e}")
                    logging.debug(f"Comment data: {comment_data}")
                    continue
                    
            return comments
            
        except Exception as e:
            logging.error(f"Error getting issue comments: {e}")
            raise PlaneError("Error fetching issue comments")
        
    async def get_comment_details(self, project_id: str, issue_id: str, comment_id: str) -> IssueComment:
        """
        Fetch specific comment details for an issue.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)
            comment_id (str): ID of the comment to fetch (Required)
            
        Returns:
            IssueComment: IssueComment object if found
        """
        try:
            comment_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/{comment_id}"
            )
            
            if not isinstance(comment_data, dict):
                raise ValueError(f"Unexpected response format: {type(comment_data)}")
            return IssueComment(
                id=comment_data.get('id', ''),
                created_at=comment_data.get('created_at', ''),
                updated_at=comment_data.get('updated_at', ''),
                comment_stripped=comment_data.get('comment_stripped', ''),
                comment_json=comment_data.get('comment_json', {}),
                comment_html=comment_data.get('comment_html', ''),
                attachments=comment_data.get('attachments', []),
                access=comment_data.get('access', ''),
                created_by=comment_data.get('created_by', ''),
                updated_by=comment_data.get('updated_by', ''),
                issue=comment_data.get('issue', ''),
                project=comment_data.get('project', ''),
                workspace=comment_data.get('workspace', ''),
                actor=comment_data.get('actor', '')
            )
            
        except Exception as e:
            logging.error(f"Error getting comment details: {e}")
            raise PlaneError("Error fetching comment details")

    async def create_comment(self, comment_html: str, project_id: str, issue_id: str, **kwargs) -> IssueComment:
        """
        Create a new comment with provided data.

        Args:
            url (str): URL of the link (Required)
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)
            **kwargs: Any valid IssueComment field to update

        Returns:
            IssueComment: Created IssueComment object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IssueComment.__annotations__.keys()
        filtered_data = {
            'comment_html': comment_html
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            comment_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/", 
                json=filtered_data
            )
            
            return IssueComment(
                id=comment_data.get('id', ''),
                created_at=comment_data.get('created_at', ''),
                updated_at=comment_data.get('updated_at', ''),
                comment_stripped=comment_data.get('comment_stripped', ''),
                comment_json=comment_data.get('comment_json', {}),
                comment_html=comment_data.get('comment_html', ''),
                attachments=comment_data.get('attachments', []),
                access=comment_data.get('access', ''),
                created_by=comment_data.get('created_by', ''),
                updated_by=comment_data.get('updated_by', ''),
                issue=comment_data.get('issue', ''),
                project=comment_data.get('project', ''),
                workspace=comment_data.get('workspace', ''),
                actor=comment_data.get('actor', '')
            )

        except Exception as e:
            logging.error(f"Error creating Comment: {e}")
            raise PlaneError("Error creating comment")
        
    async def update_comment(self, comment_html: str, project_id: str, issue_id: str, comment_id: str, **kwargs) -> IssueComment:
        """
        Update a comment with provided fields.

        Args:
            comment_html (str): HTML content of the comment (Required)
            project_id (str): The ID of the project to update (Required)
            issue_id (str): The ID of the issue (Required)
            comment_id (str): The ID of the comment to update (Required)
            **kwargs: Any valid IssueComment field to update

        Returns:
            IssueComment: Updated IssueComment object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = IssueComment.__annotations__.keys()
        filtered_data = {
            'comment_html': comment_html
        }

        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            comment_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return IssueComment(
                id=comment_data.get('id', ''),
                created_at=comment_data.get('created_at', ''),
                updated_at=comment_data.get('updated_at', ''),
                comment_stripped=comment_data.get('comment_stripped', ''),
                comment_json=comment_data.get('comment_json', {}),
                comment_html=comment_data.get('comment_html', ''),
                attachments=comment_data.get('attachments', []),
                access=comment_data.get('access', ''),
                created_by=comment_data.get('created_by', ''),
                updated_by=comment_data.get('updated_by', ''),
                issue=comment_data.get('issue', ''),
                project=comment_data.get('project', ''),
                workspace=comment_data.get('workspace', ''),
                actor=comment_data.get('actor', '')
            )

            
        except Exception as e:
            logging.error(f"Error updating comment: {e}")
            raise PlaneError("Error updating comment")
        
    async def delete_comment(self, project_id: str, issue_id: str, comment_id: str) -> bool:
        """
        Delete an existing comment.

        Args:
            project_id: The ID of the project containing the issue (Required)
            issue_id: The ID of the issue containing the comment (Required)
            comment_id: The ID of the comment to delete (Required)

        Returns:
            bool: True if comment was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting comment: {e}")
            return False