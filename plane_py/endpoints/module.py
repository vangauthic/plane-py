from plane_py import *
from ..errors import *
from .base import BaseEndpoint
import logging

class ModuleEndpoint(BaseEndpoint):
    async def get_modules(self, project_id: str) -> list[Module]:
        """
        Fetch all modules for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[Module]: List of Module objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/")
            
            if isinstance(response, dict) and 'results' in response:
                project_modules = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            modules = []
            for module_data in project_modules:
                try:
                    module = Module(
                        id=module_data.get('id', ''),
                        created_at=module_data.get('created_at', ''),
                        updated_at=module_data.get('updated_at', ''),
                        name=module_data.get('name', ''),
                        description=module_data.get('description', ''),
                        description_text=module_data.get('description_text', ''),
                        description_html=module_data.get('description_html', ''),
                        start_date=module_data.get('start_date'),
                        target_date=module_data.get('target_date'),
                        status=module_data.get('status', ''),
                        view_props=module_data.get('view_props', {}),
                        sort_order=module_data.get('sort_order', 0.0),
                        created_by=module_data.get('created_by', ''),
                        updated_by=module_data.get('updated_by', ''),
                        project=module_data.get('project', ''),
                        workspace=module_data.get('workspace', ''),
                        lead=module_data.get('lead', ''),
                        members=module_data.get('members', [])
                    )
                    modules.append(module)
                except TypeError as e:
                    logging.error(f"Error creating module object: {e}")
                    logging.debug(f"Module data: {module_data}")
                    continue
                    
            return modules
            
        except Exception as e:
            logging.error(f"Error getting Modules: {e}")
            raise PlaneError("Error fetching project modules")
        
    async def get_module_details(self, project_id: str, module_id: str) -> Module:
        """
        Fetch specific module details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            module_id (str): ID of the module to fetch (Required)
            
        Returns:
            Module: Module object if found
        """
        try:
            module_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/{module_id}"
            )
            
            if not isinstance(module_data, dict):
                raise ValueError(f"Unexpected response format: {type(module_data)}")

            return Module(
                id=module_data.get('id', ''),
                created_at=module_data.get('created_at', ''),
                updated_at=module_data.get('updated_at', ''),
                name=module_data.get('name', ''),
                description=module_data.get('description', ''),
                description_text=module_data.get('description_text', ''),
                description_html=module_data.get('description_html', ''),
                start_date=module_data.get('start_date'),
                target_date=module_data.get('target_date'),
                status=module_data.get('status', ''),
                view_props=module_data.get('view_props', {}),
                sort_order=module_data.get('sort_order', 0.0),
                created_by=module_data.get('created_by', ''),
                updated_by=module_data.get('updated_by', ''),
                project=module_data.get('project', ''),
                workspace=module_data.get('workspace', ''),
                lead=module_data.get('lead', ''),
                members=module_data.get('members', [])
            )
            
        except Exception as e:
            logging.error(f"Error getting module details: {e}")
            raise PlaneError("Error fetching module details")
        
    async def create_module(self, name: str, project_id: str, **kwargs) -> Module:
        """
        Create a new module with provided data.

        Args:
            name (str): Name of the module (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid Module field to update

        Returns:
            Module: Created Module object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Module.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            module_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/", 
                json=filtered_data
            )
            
            return Module(
                id=module_data.get('id', ''),
                created_at=module_data.get('created_at', ''),
                updated_at=module_data.get('updated_at', ''),
                name=module_data.get('name', ''),
                description=module_data.get('description', ''),
                description_text=module_data.get('description_text', ''),
                description_html=module_data.get('description_html', ''),
                start_date=module_data.get('start_date'),
                target_date=module_data.get('target_date'),
                status=module_data.get('status', ''),
                view_props=module_data.get('view_props', {}),
                sort_order=module_data.get('sort_order', 0.0),
                created_by=module_data.get('created_by', ''),
                updated_by=module_data.get('updated_by', ''),
                project=module_data.get('project', ''),
                workspace=module_data.get('workspace', ''),
                lead=module_data.get('lead', ''),
                members=module_data.get('members', [])
            )

        except Exception as e:
            logging.error(f"Error creating Module: {e}")
            raise PlaneError("Error creating module")
        
    async def update_module(self, name: str, project_id: str, module_id: str, **kwargs) -> Module:
        """
        Update a module with provided fields.

        Args:
            name: Name of the module (Required)
            project_id (str): The ID of the project to update (Required)
            module_id (str): The ID of the module to update (Required)
            **kwargs: Any valid Module field to update

        Returns:
            Module: Updated Module object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = Module.__annotations__.keys()
        filtered_data = {
            'name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            module_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/{module_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return Module(
                id=module_data.get('id', ''),
                created_at=module_data.get('created_at', ''),
                updated_at=module_data.get('updated_at', ''),
                name=module_data.get('name', ''),
                description=module_data.get('description', ''),
                description_text=module_data.get('description_text', ''),
                description_html=module_data.get('description_html', ''),
                start_date=module_data.get('start_date'),
                target_date=module_data.get('target_date'),
                status=module_data.get('status', ''),
                view_props=module_data.get('view_props', {}),
                sort_order=module_data.get('sort_order', 0.0),
                created_by=module_data.get('created_by', ''),
                updated_by=module_data.get('updated_by', ''),
                project=module_data.get('project', ''),
                workspace=module_data.get('workspace', ''),
                lead=module_data.get('lead', ''),
                members=module_data.get('members', [])
            )
            
        except Exception as e:
            logging.error(f"Error updating module: {e}")
            raise PlaneError("Error updating module")
        
    async def delete_module(self, project_id: str, module_id: str) -> bool:
        """
        Delete an existing module.

        Args:
            project_id: The ID of the project containing the issue (Required)
            module_id: The ID of the module to be deleted (Required)

        Returns:
            bool: True if module was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/modules/{module_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting module: {e}")
            return False