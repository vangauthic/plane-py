from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class IssuePropertyEndpoint(BaseEndpoint):
    async def get_issue_properties(self, project_id: str, type_id: str) -> list[IssueProperty]:
        """
        Fetch all issue properties for a type.
        
        Args:
            project_id (str): ID of the project (Required)
            type_id (str): ID of the type (Required)

        Returns:
            list[IssueProperty]: List of IssueProperty objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_properties = response['results']
            elif isinstance(response, list):
                issue_properties = response
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            properties = []

            valid_fields = IssueProperty.__annotations__.keys()

            for property_data in issue_properties:
                filtered_data = {k: v for k, v in property_data.items() if k in valid_fields}
                try:
                    properties.append(IssueProperty(**filtered_data))
                except TypeError as e:
                    logging.error(f"Error getting property: {e}")
                    logging.info(f"Data: {filtered_data}")
                    continue
                    
            return properties
            
        except Exception as e:
            logging.error(f"Error getting IssueProperties: {e}")
            raise PlaneError("Error fetching project IssueProperties")
        
    async def get_property_details(self, project_id: str, type_id: str, property_id: str) -> IssueProperty:
        """
        Fetch details for a type property.
        
        Args:
            project_id (str): ID of the project (Required)
            type_id (str): ID of the type (Required)
            property_id (str): ID of the property to fetch (Required)

        Returns:
            IssueProperty: IssueProperty object
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/")
            
            valid_fields = IssueProperty.__annotations__.keys()

            filtered_data = {k: v for k, v in response.items() if k in valid_fields}
            return IssueProperty(**filtered_data)
            
        except Exception as e:
            logging.error(f"Error getting IssueProperty details: {e}")
            raise PlaneError("Error fetching project IssueProperty")

    async def update_property(self, name: str, project_id: str, type_id: str, property_id: str, **kwargs) -> IssueProperty:
        """
        Update a property with provided fields.

        Args:
            project_id (str): The ID of the project (Required)
            type_id (str): The ID of the issue type (Required) 
            property_id (str): The ID of the property to update (Required)
            name (str): Updated name of the property (Required)
            **kwargs: Any valid IssueProperty field to update

        Returns:
            IssueProperty: Updated IssueProperty object

        Raises:
            ValueError: If response format is unexpected 
        """
        # Get valid fields from IssueProperty class
        valid_fields = IssueProperty.__annotations__.keys()
        filtered_data = {
            'display_name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields and k != 'name'})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            response = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/",
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return IssueProperty(**filtered_response)
            
        except Exception as e:
            logging.error(f"Error updating property: {e}")
            raise PlaneError("Error updating property")
        
    async def create_property(self, name: str, type_id: str, project_id: str, **kwargs) -> IssueProperty:
        """
        Create a new property with provided data.

        Args:
            name (str): Name of the property (Required)
            type_id (str): ID of the issue type (Required)
            project_id (str): ID of the project (Required) 
            **kwargs: Any valid IssueProperty field to update

        Returns:
            IssueProperty: Created IssueProperty object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IssueProperty.__annotations__.keys()
        filtered_data = {
            'display_name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields and k != 'name'})

        try:
            response = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/", 
                json=filtered_data
            )
            
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return IssueProperty(**filtered_response)

        except Exception as e:
            logging.error(f"Error creating IssueProperty: {e}")
            raise PlaneError("Error creating property")
        
    async def delete_property(self, project_id: str, type_id: str, property_id: str) -> bool:
        """
        Delete an existing property.

        Args:
            project_id: The ID of the project (Required)
            type_id: The ID of the issue type (Required)
            property_id: The ID of the property to delete (Required)

        Returns:
            bool: True if property was deleted successfully, False otherwise
        """

        try:
            response = await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting property: {e}")
            return False