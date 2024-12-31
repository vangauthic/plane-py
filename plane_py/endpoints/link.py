from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class LinkEndpoint(BaseEndpoint):
    async def get_links(self, project_id: str, issue_id: str) -> list[Link]:
        """
        Fetch all links for an issue.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)

        Returns:
            list[Link]: List of Link objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/links/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_links = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            links = []
            for link_data in issue_links:
                try:
                    link = Link(
                        id=link_data.get('id', ''),
                        created_at=link_data.get('created_at', ''),
                        updated_at=link_data.get('updated_at', ''),
                        title=link_data.get('title', ''),
                        url=link_data.get('url', ''),
                        metadata=link_data.get('metadata', {}),
                        created_by=link_data.get('created_by', ''),
                        updated_by=link_data.get('updated_by', ''),
                        project=link_data.get('project', ''),
                        workspace=link_data.get('workspace', ''),
                        issue=link_data.get('issue', '')
                    )
                    links.append(link)
                except TypeError as e:
                    logging.error(f"Error creating link object: {e}")
                    logging.debug(f"Link data: {link_data}")
                    continue
                    
            return links
            
        except Exception as e:
            logging.error(f"Error getting links: {e}")
            raise PlaneError("Error fetching issue links")
        
    async def get_link_details(self, project_id: str, issue_id: str, link_id: str) -> Link:
        """
        Fetch specific link details for an issue.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the label to fetch (Required)
            link_id (str): ID of the link to fetch (Required)
            
        Returns:
            Link: Link object if found
        """
        try:
            link_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/links/{link_id}"
            )
            
            if not isinstance(link_data, dict):
                raise ValueError(f"Unexpected response format: {type(link_data)}")

            return Link(
                id=link_data.get('id', ''),
                created_at=link_data.get('created_at', ''),
                updated_at=link_data.get('updated_at', ''),
                title=link_data.get('title', ''),
                url=link_data.get('url', ''),
                metadata=link_data.get('metadata', {}),
                created_by=link_data.get('created_by', ''),
                updated_by=link_data.get('updated_by', ''),
                project=link_data.get('project', ''),
                workspace=link_data.get('workspace', ''),
                issue=link_data.get('issue', '')
            )
            
        except Exception as e:
            logging.error(f"Error getting link details: {e}")
            raise PlaneError("Error fetching link details")
        
    async def create_link(self, url: str, project_id: str, issue_id: str, **kwargs) -> Link:
        """
        Create a new link with provided data.

        Args:
            url (str): URL of the link (Required)
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)
            **kwargs: Any valid Link field to update

        Returns:
            Link: Created Link object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Link.__annotations__.keys()
        filtered_data = {
            'url': url
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            link_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/links/", 
                json=filtered_data
            )
            
            return Link(
                id=link_data.get('id', ''),
                created_at=link_data.get('created_at', ''),
                updated_at=link_data.get('updated_at', ''),
                title=link_data.get('title', ''),
                url=link_data.get('url', ''),
                metadata=link_data.get('metadata', {}),
                created_by=link_data.get('created_by', ''),
                updated_by=link_data.get('updated_by', ''),
                project=link_data.get('project', ''),
                workspace=link_data.get('workspace', ''),
                issue=link_data.get('issue', '')
            )

        except Exception as e:
            logging.error(f"Error creating Link: {e}")
            raise PlaneError("Error creating link")
        
    async def update_link(self, project_id: str, issue_id: str, link_id: str, **kwargs) -> Link:
        """
        Update a link with provided fields.

        Args:
            project_id (str): The ID of the project to update (Required)
            issue_id (str): The ID of the label to update (Required)
            link_id (str): The ID of the link to update (Required)
            **kwargs: Any valid Link field to update

        Returns:
            Link: Updated Link object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = Link.__annotations__.keys()
        
        # Filter out any invalid fields from kwargs
        filtered_data = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            link_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/links/{link_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return Link(
                id=link_data.get('id', ''),
                created_at=link_data.get('created_at', ''),
                updated_at=link_data.get('updated_at', ''),
                title=link_data.get('title', ''),
                url=link_data.get('url', ''),
                metadata=link_data.get('metadata', {}),
                created_by=link_data.get('created_by', ''),
                updated_by=link_data.get('updated_by', ''),
                project=link_data.get('project', ''),
                workspace=link_data.get('workspace', ''),
                issue=link_data.get('issue', '')
            )

            
        except Exception as e:
            logging.error(f"Error updating link: {e}")
            raise PlaneError("Error updating link")
        
    async def delete_link(self, project_id: str, issue_id: str, link_id: str) -> bool:
        """
        Delete an existing link.

        Args:
            project_id: The ID of the project containing the issue (Required)
            issue_id: The ID of the issue containing the link (Required)
            link_id: The ID of the link to delete (Required)

        Returns:
            bool: True if link was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/links/{link_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting link: {e}")
            return False