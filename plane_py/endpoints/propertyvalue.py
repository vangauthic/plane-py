from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class PropertyValueEndpoint(BaseEndpoint):
    async def get_property_values(self, project_id: str, issue_id: str, property_id: str) -> list[PropertyValue]:
        """
        Fetch all values for a property.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required)
            property_id (str): ID of the property (Required)

        Returns:
            list[PropertyValue]: List of PropertyValue objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_properties = response['results']
            elif isinstance(response, list):
                issue_properties = response
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            properties = []

            valid_fields = PropertyValue.__annotations__.keys()

            for property_data in issue_properties:
                filtered_data = {k: v for k, v in property_data.items() if k in valid_fields}
                try:
                    properties.append(PropertyValue(**filtered_data))
                except TypeError as e:
                    logging.error(f"Error getting property value: {e}")
                    logging.info(f"Data: {filtered_data}")
                    continue
                    
            return properties
            
        except Exception as e:
            logging.error(f"Error getting PropertyValue: {e}")
            raise PlaneError("Error fetching project PropertyValues")
        
    async def create_value(self, property_id: str, project_id: str, issue_id: str, values: list) -> PropertyValue:
        """
        Create a new value for a property.

        Args:
            property_id (str): ID of the property (Required)
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue (Required) 
            values (list): List of values to add (Required)
            **kwargs: Any valid PropertyValue field to update

        Returns:
            PropertyValue: Created PropertyValue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = PropertyValue.__annotations__.keys()
        filtered_data = {
            'values': values
        }

        try:
            response = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/", 
                json=filtered_data
            )
            
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return PropertyValue(**filtered_response)

        except Exception as e:
            logging.error(f"Error creating PropertyValue: {e}")
            raise PlaneError("Error creating value")