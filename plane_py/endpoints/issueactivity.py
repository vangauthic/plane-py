from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class IssueActivityEndpoint(BaseEndpoint):
    async def get_issue_activity(self, project_id: str, issue_id: str) -> list[IssueActivity]:
        """
        Fetch all activities for an issue.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)

        Returns:
            list[IssueActivity]: List of IssueActivity objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/activities/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_activities = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            activities = []
            for activity_data in issue_activities:
                try:
                    activity = IssueActivity(
                        id=activity_data.get('id', ''),
                        created_at=activity_data.get('created_at', ''),
                        updated_at=activity_data.get('updated_at', ''),
                        verb=activity_data.get('verb', ''),
                        field=activity_data.get('field'),
                        old_value=activity_data.get('old_value'),
                        new_value=activity_data.get('new_value'),
                        comment=activity_data.get('comment', ''),
                        attachments=activity_data.get('attachments', []),
                        old_identifier=activity_data.get('old_identifier'),
                        new_identifier=activity_data.get('new_identifier'),
                        epoch=float(activity_data.get('epoch', 0.0)),
                        project=activity_data.get('project', ''),
                        workspace=activity_data.get('workspace', ''),
                        issue=activity_data.get('issue', ''),
                        issue_comment=activity_data.get('issue_comment'),
                        actor=activity_data.get('actor', '')
                    )
                    activities.append(activity)
                except TypeError as e:
                    logging.error(f"Error creating activity object: {e}")
                    logging.debug(f"Activity data: {activity_data}")
                    continue
                    
            return activities
            
        except Exception as e:
            logging.error(f"Error getting issue activities: {e}")
            raise PlaneError("Error fetching issue activities")
        
    async def get_activity_details(self, project_id: str, issue_id: str, activity_id: str) -> IssueActivity:
        """
        Fetch specific activity details for an issue.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)
            activity_id (str): ID of the activity to fetch (Required)
            
        Returns:
            IssueActivity: IssueActivity object if found
        """
        try:
            activity_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/activities/{activity_id}"
            )
            
            if not isinstance(activity_data, dict):
                raise ValueError(f"Unexpected response format: {type(activity_data)}")
            return IssueActivity(
                id=activity_data.get('id', ''),
                created_at=activity_data.get('created_at', ''),
                updated_at=activity_data.get('updated_at', ''),
                verb=activity_data.get('verb', ''),
                field=activity_data.get('field'),
                old_value=activity_data.get('old_value'),
                new_value=activity_data.get('new_value'),
                comment=activity_data.get('comment', ''),
                attachments=activity_data.get('attachments', []),
                old_identifier=activity_data.get('old_identifier'),
                new_identifier=activity_data.get('new_identifier'),
                epoch=float(activity_data.get('epoch', 0.0)),
                project=activity_data.get('project', ''),
                workspace=activity_data.get('workspace', ''),
                issue=activity_data.get('issue', ''),
                issue_comment=activity_data.get('issue_comment'),
                actor=activity_data.get('actor', '')
            )
            
        except Exception as e:
            logging.error(f"Error getting activity details: {e}")
            raise PlaneError("Error fetching activity details")