from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class LabelEndpoint(BaseEndpoint):
    async def get_labels(self, project_id: str) -> list[Label]:
        """
        Fetch all labels for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[Label]: List of Label objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/labels/")
            
            if isinstance(response, dict) and 'results' in response:
                project_labels = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            labels = []
            for label_data in project_labels:
                try:
                    label = Label(
                        id=label_data.get('id', ''),
                        created_at=label_data.get('created_at', ''),
                        updated_at=label_data.get('updated_at', ''),
                        name=label_data.get('name', ''),
                        description=label_data.get('description', ''),
                        color=label_data.get('color', ''),
                        sort_order=float(label_data.get('sort_order', 0.0)),
                        created_by=label_data.get('created_by', ''),
                        updated_by=label_data.get('updated_by', ''),
                        project=label_data.get('project', ''),
                        workspace=label_data.get('workspace', ''),
                        parent=label_data.get('parent')
                    )
                    labels.append(label)
                except TypeError as e:
                    logging.error(f"Error creating label object: {e}")
                    logging.debug(f"Label data: {label_data}")
                    continue
                    
            return labels
            
        except Exception as e:
            logging.error(f"Error getting labels: {e}")
            raise PlaneError("Error fetching project labels")
        
    async def get_label_details(self, project_id: str, label_id: str) -> Label:
        """
        Fetch specific label details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            label_id (str): ID of the label to fetch (Required)
            
        Returns:
            Label: Label object if found
        """
        try:
            label_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/labels/{label_id}"
            )
            
            if not isinstance(label_data, dict):
                raise ValueError(f"Unexpected response format: {type(label_data)}")

            return Label(
                id=label_data.get('id', ''),
                created_at=label_data.get('created_at', ''),
                updated_at=label_data.get('updated_at', ''),
                name=label_data.get('name', ''),
                description=label_data.get('description', ''),
                color=label_data.get('color', ''),
                sort_order=float(label_data.get('sort_order', 0.0)),
                created_by=label_data.get('created_by', ''),
                updated_by=label_data.get('updated_by', ''),
                project=label_data.get('project', ''),
                workspace=label_data.get('workspace', ''),
                parent=label_data.get('parent')
            )
            
        except Exception as e:
            logging.error(f"Error getting label details: {e}")
            raise PlaneError("Error fetching label details")
        
    async def create_label(self, name: str, project_id: str, **kwargs) -> Label:
        """
        Create a new label with provided data.

        Args:
            name (str): Name of the label (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid Label field to update

        Returns:
            Label: Created Label object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Label.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            label_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/labels/", 
                json=filtered_data
            )
            
            return Label(
                id=label_data.get('id', ''),
                created_at=label_data.get('created_at', ''),
                updated_at=label_data.get('updated_at', ''),
                name=label_data.get('name', ''),
                description=label_data.get('description', ''),
                color=label_data.get('color', ''),
                sort_order=float(label_data.get('sort_order', 0.0)),
                created_by=label_data.get('created_by', ''),
                updated_by=label_data.get('updated_by', ''),
                project=label_data.get('project', ''),
                workspace=label_data.get('workspace', ''),
                parent=label_data.get('parent')
            )

        except Exception as e:
            logging.error(f"Error creating Label: {e}")
            raise PlaneError("Error creating label")
        
    async def update_label(self, name: str, project_id: str, label_id: str, **kwargs) -> Label:
        """
        Update a label with provided fields.

        Args:
            name: The name of the label to update (Required)
            project_id (str): The ID of the project to update (Required)
            label_id (str): The ID of the label to update (Required)
            **kwargs: Any valid Label field to update

        Returns:
            Label: Updated Label object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = Label.__annotations__.keys()
        filtered_data = {
            'name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            label_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/labels/{label_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return Label(
                id=label_data.get('id', ''),
                created_at=label_data.get('created_at', ''),
                updated_at=label_data.get('updated_at', ''),
                name=label_data.get('name', ''),
                description=label_data.get('description', ''),
                color=label_data.get('color', ''),
                sort_order=float(label_data.get('sort_order', 0.0)),
                created_by=label_data.get('created_by', ''),
                updated_by=label_data.get('updated_by', ''),
                project=label_data.get('project', ''),
                workspace=label_data.get('workspace', ''),
                parent=label_data.get('parent')
            )
            
        except Exception as e:
            logging.error(f"Error updating label: {e}")
            raise PlaneError("Error updating label")
        
    async def delete_label(self, project_id: str, label_id: str) -> bool:
        """
        Delete an existing label.

        Args:
            project_id: The ID of the project containing the label (Required)
            label_id: The ID of the label to delete (Required)

        Returns:
            bool: True if label was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/labels/{label_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting label: {e}")
            return False