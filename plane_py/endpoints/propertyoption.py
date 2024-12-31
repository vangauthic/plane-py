from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class PropertyOptionEndpoint(BaseEndpoint):
    async def get_property_options(self, project_id: str, property_id: str) -> list[PropertyOption]:
        """
        Fetch all options for a dropdown property.
        
        Args:
            project_id (str): ID of the project (Required)
            property_id (str): ID of the property (Required)

        Returns:
            list[PropertyOption]: List of PropertyOption objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-properties/{property_id}/options/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_properties = response['results']
            elif isinstance(response, list):
                issue_properties = response
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            properties = []

            valid_fields = PropertyOption.__annotations__.keys()

            for property_data in issue_properties:
                filtered_data = {k: v for k, v in property_data.items() if k in valid_fields}
                try:
                    properties.append(PropertyOption(**filtered_data))
                except TypeError as e:
                    logging.error(f"Error getting property options: {e}")
                    logging.info(f"Data: {filtered_data}")
                    continue
                    
            return properties
            
        except Exception as e:
            logging.error(f"Error getting PropertyOptions: {e}")
            raise PlaneError("Error fetching project PropertyOptions")
        
    async def get_option_details(self, project_id: str, property_id: str, option_id: str) -> PropertyOption:
        """
        Fetch details for a property option.
        
        Args:
            project_id (str): ID of the project (Required)
            property_id (str): ID of the property (Required)
            option_id (str): ID of the option to fetch (Required)

        Returns:
            PropertyOption: PropertyOption object

        Raises:
            PlaneError: If option not found or error occurs
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-properties/{property_id}/options/")

            option = next((opt for opt in response if opt.get('id') == option_id), None)
            if not option:
                raise PlaneError(f"Option with ID {option_id} not found")
            
            valid_fields = PropertyOption.__annotations__.keys()
            filtered_data = {k: v for k, v in option.items() if k in valid_fields}
            return PropertyOption(**filtered_data)
            
        except Exception as e:
            logging.error(f"Error getting PropertyOption: {e}")
            raise PlaneError("Error fetching project PropertyOption")
        
    async def create_option(self, name: str, property_id: str, project_id: str, **kwargs) -> IssueProperty:
        """
        Create a new property with provided data.

        Args:
            name (str): Name of the option (Required)
            property_id (str): ID of the property (Required)
            project_id (str): ID of the project (Required) 
            **kwargs: Any valid PropertyOption field to update

        Returns:
            PropertyOption: Created PropertyOption object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = PropertyOption.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            response = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-properties/{property_id}/options/", 
                json=filtered_data
            )
            
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return PropertyOption(**filtered_response)

        except Exception as e:
            logging.error(f"Error creating PropertyOption: {e}")
            raise PlaneError("Error creating option")
        
    async def update_option(self, name: str, project_id: str, option_id: str, property_id: str, **kwargs) -> PropertyOption:
        """
        Update a property with provided fields.

        Args:
            project_id (str): The ID of the project (Required)
            option_id (str): The ID of the option to update (Required)
            property_id (str): The ID of the property (Required)
            name (str): Updated name of the property (Required)
            **kwargs: Any valid PropertyOption field to update

        Returns:
            PropertyOption: Updated PropertyOption object

        Raises:
            ValueError: If response format is unexpected 
        """
        valid_fields = PropertyOption.__annotations__.keys()
        filtered_data = {
            'name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            response = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/",
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return PropertyOption(**filtered_response)
            
        except Exception as e:
            logging.error(f"Error updating PropertyOption: {e}")
            raise PlaneError("Error updating option")
        
    async def delete_option(self, project_id: str, property_id: str, option_id: str) -> bool:
        """
        Delete an existing property option.

        Args:
            project_id: The ID of the project (Required)
            property_id: The ID of the property containing the option (Required)
            option_id: The ID of the option to delete (Required)

        Returns:
            bool: True if option was deleted successfully, False otherwise
        """

        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting option: {e}")
            return False