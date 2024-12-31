import aiohttp
import logging
from ._types import *
from .errors import *

class PlaneClient():
    def __init__(self, api_token: str, workspace_slug: str, base_url: str = "https://api.plane.so"):
        self._base_url = base_url
        self._api_token = api_token
        self.workspace_slug = workspace_slug

    async def _request(self, method: str, endpoint: str, **kwargs):
        """Helper function to make async HTTP requests."""
        url = f"{self._base_url}{endpoint}"
        headers = {"x-api-key": f"{self._api_token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, **kwargs) as response:
                response.raise_for_status() # Will raise an error for bad responses
                if response.status == 204:
                    return None
                if response.status == 404:
                    raise NotFoundError("Not found.")
                return await response.json()
            
    async def get_projects(self) -> list[Project]:
        """
        Fetch all projects.
        
        Returns:
            list[Project]: List of Project objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/")
            
            # API returns dict with 'results' key containing projects list
            if isinstance(response, dict) and 'results' in response:
                projects_data = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            # Get valid fields from Project class
            valid_fields = Project.__annotations__.keys()
            
            # Filter project data to only include valid fields
            projects = []
            for project_data in projects_data:
                filtered_data = {k: v for k, v in project_data.items() if k in valid_fields}
                try:
                    projects.append(Project(**filtered_data))
                except TypeError as e:
                    logging.error(f"Error getting project: {e}")
                    logging.info(f"Data: {filtered_data}")
                    continue
                    
            return projects
            
        except Exception as e:
            logging.error(f"Error getting projects: {e}")
            return []
        
    async def get_project_details(self, project_id: str) -> Project:
        """
        Fetch details for a specific project.
        
        Args:
            project_id (str): The ID of the project to fetch (Required)
            
        Returns:
            Project: Project object with details
            
        Raises:
            ValueError: If response format is unexpected
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/")
            
            # Get valid fields from Project class
            valid_fields = Project.__annotations__.keys()
            
            # Filter project data to only include valid fields
            filtered_data = {k: v for k, v in response.items() if k in valid_fields}
            
            return Project(**filtered_data)
            
        except Exception as e:
            logging.error(f"Error fetching project details: {e}")
            raise PlaneError("Error fetching project details")

    async def update_project(self, project_id: str, **kwargs) -> Project:
        """
        Update a project with provided fields.

        Args:
            project_id (str): The ID of the project to update (Required)
            **kwargs: Any valid Project field to update

        Returns:
            Project: Updated Project object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = Project.__annotations__.keys()
        
        # Filter out any invalid fields from kwargs
        filtered_data = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            response = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return Project(**filtered_response)
            
        except Exception as e:
            logging.error(f"Error updating project: {e}")
            raise PlaneError("Error updating project")

    async def create_project(self, name: str, identifier: str, **kwargs) -> Project:
        """
        Create a new project with provided data.

        Args:
            name (str): Name of the project (Required)
            identifier (str): Identifier of the project (Required)
            **kwargs: Any valid Project field to update

        Returns:
            Project: Created Project object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Project.__annotations__.keys()
        filtered_data = {
            'name': name,
            'identifier': identifier
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            response = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/", 
                json=filtered_data
            )
            
            filtered_response = {k: v for k, v in response.items() if k in valid_fields}
            
            return Project(**filtered_response)

        except Exception as e:
            logging.error(f"Error creating Project: {e}")
            raise PlaneError("Error creating project")

    async def delete_project(self, project_id: str) -> bool:
        """
        Delete an existing project.

        Args:
            project_id: The ID of the project to delete (Required)

        Returns:
            bool: True if project was deleted successfully, False otherwise
        """

        try:
            response = await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting project: {e}")
            return False
        
    async def get_states(self, project_id: str) -> list[State]:
        """
        Fetch all states for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[State]: List of State objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/")
            
            if isinstance(response, dict) and 'results' in response:
                project_states = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            states = []
            for state_data in project_states:
                # Ensure workspace_slug is set from current client
                state_data['workspace_slug'] = self.workspace_slug
                
                try:
                    # Create State object with the complete data
                    state = State(
                        id=state_data.get('id', ''),
                        created_at=state_data.get('created_at', ''),
                        updated_at=state_data.get('updated_at', ''),
                        name=state_data.get('name', ''),
                        description=state_data.get('description', ''),
                        color=state_data.get('color', ''),
                        workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                        sequence=str(state_data.get('sequence', '')),
                        group=state_data.get('group', ''),
                        default=state_data.get('default', False),
                        created_by=state_data.get('created_by', ''),
                        updated_by=state_data.get('updated_by', ''),
                        project=state_data.get('project', ''),
                        workspace=state_data.get('workspace', '')
                    )
                    states.append(state)
                except TypeError as e:
                    logging.error(f"Error getting project state: {e}")
                    logging.info(f"Data: {state_data}")
                    continue
                    
            return states
            
        except Exception as e:
            logging.error(f"Error getting states: {e}")
            raise PlaneError("Error fetching project states")
        
    async def get_state_details(self, project_id: str, state_id: str) -> State:
        """
        Fetch specific state details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            state_id (str): ID of the state to fetch (Required)
            
        Returns:
            State: State object if found
        """
        try:
            state_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/{state_id}/"
            )
            
            if not isinstance(state_data, dict):
                raise ValueError(f"Unexpected response format: {type(state_data)}")
            
            # Create State object with the complete data
            return State(
                id=state_data.get('id', ''),
                created_at=state_data.get('created_at', ''),
                updated_at=state_data.get('updated_at', ''),
                name=state_data.get('name', ''),
                description=state_data.get('description', ''),
                color=state_data.get('color', ''),
                workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                sequence=str(state_data.get('sequence', '')),
                group=state_data.get('group', ''),
                default=state_data.get('default', False),
                created_by=state_data.get('created_by', ''),
                updated_by=state_data.get('updated_by', ''),
                project=state_data.get('project', ''),
                workspace=state_data.get('workspace', '')
            )
            
        except Exception as e:
            logging.error(f"Error getting state details: {e}")
            raise PlaneError("Error fetching state details")
        
    async def create_state(self, name: str, color: str, project_id: str, **kwargs) -> State:
        """
        Create a new state with provided data.

        Args:
            name (str): Name of the state (Required)
            color (str): Color of the state (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid State field to update

        Returns:
            State: Created State object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = State.__annotations__.keys()
        filtered_data = {
            'name': name,
            'color': color
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            state_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/", 
                json=filtered_data
            )
            
            return State(
                id=state_data.get('id', ''),
                created_at=state_data.get('created_at', ''),
                updated_at=state_data.get('updated_at', ''),
                name=state_data.get('name', ''),
                description=state_data.get('description', ''),
                color=state_data.get('color', ''),
                workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                sequence=str(state_data.get('sequence', '')),
                group=state_data.get('group', ''),
                default=state_data.get('default', False),
                created_by=state_data.get('created_by', ''),
                updated_by=state_data.get('updated_by', ''),
                project=state_data.get('project', ''),
                workspace=state_data.get('workspace', '')
            )

        except Exception as e:
            logging.error(f"Error creating State: {e}")
            raise PlaneError("Error creating state")
        
    async def update_state(self, project_id: str, state_id: str, **kwargs) -> State:
        """
        Update a state with provided fields.

        Args:
            project_id (str): The ID of the project to update (Required)
            state_id (str): The ID of the state to update (Required)
            **kwargs: Any valid State field to update

        Returns:
            State: Updated State object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = State.__annotations__.keys()
        
        # Filter out any invalid fields from kwargs
        filtered_data = {k: v for k, v in kwargs.items() if k in valid_fields}
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            state_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/{state_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return State(
                id=state_data.get('id', ''),
                created_at=state_data.get('created_at', ''),
                updated_at=state_data.get('updated_at', ''),
                name=state_data.get('name', ''),
                description=state_data.get('description', ''),
                color=state_data.get('color', ''),
                workspace_slug=self.workspace_slug,  # Use client's workspace_slug
                sequence=str(state_data.get('sequence', '')),
                group=state_data.get('group', ''),
                default=state_data.get('default', False),
                created_by=state_data.get('created_by', ''),
                updated_by=state_data.get('updated_by', ''),
                project=state_data.get('project', ''),
                workspace=state_data.get('workspace', '')
            )
            
        except Exception as e:
            logging.error(f"Error updating state: {e}")
            raise PlaneError("Error updating state")
        
    async def delete_state(self, project_id: str, state_id: str) -> bool:
        """
        Delete an existing state.

        Args:
            project_id: The ID of the project containing the state (Required)
            state_id: The ID of the state to delete (Required)

        Returns:
            bool: True if state was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/states/{state_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting state: {e}")
            return False
        
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
        
    async def get_issues(self, project_id: str) -> list[Issue]:
        """
        Fetch all issues for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[Issue]: List of Issue objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/")
            
            if isinstance(response, dict) and 'results' in response:
                project_issues = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            issues = []
            for issue_data in project_issues:
                try:
                    issue = Issue(
                        id=issue_data.get('id', ''),
                        created_at=issue_data.get('created_at', ''),
                        updated_at=issue_data.get('updated_at', ''),
                        estimate_point=issue_data.get('estimate_point'),
                        name=issue_data.get('name', ''),
                        description_html=issue_data.get('description_html', ''),
                        description_stripped=issue_data.get('description_stripped', ''),
                        priority=issue_data.get('priority', ''),
                        start_date=issue_data.get('start_date'),
                        target_date=issue_data.get('target_date'),
                        sequence_id=issue_data.get('sequence_id', 0),
                        sort_order=float(issue_data.get('sort_order', 0.0)),
                        completed_at=issue_data.get('completed_at'),
                        archived_at=issue_data.get('archived_at'),
                        is_draft=issue_data.get('is_draft', False),
                        created_by=issue_data.get('created_by', ''),
                        updated_by=issue_data.get('updated_by', ''),
                        project=issue_data.get('project', ''),
                        workspace=issue_data.get('workspace', ''),
                        parent=issue_data.get('parent'),
                        state=issue_data.get('state', ''),
                        assignees=issue_data.get('assignees', []),
                        labels=issue_data.get('labels', [])
                    )
                    issues.append(issue)
                except TypeError as e:
                    logging.error(f"Error creating issue object: {e}")
                    logging.debug(f"Issue data: {issue_data}")
                    continue
                    
            return issues
            
        except Exception as e:
            logging.error(f"Error getting issues: {e}")
            raise PlaneError("Error fetching project issues")
        
    async def get_issue_details(self, project_id: str, issue_id: str) -> Issue:
        """
        Fetch specific issue details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue to fetch (Required)
            
        Returns:
            Issue: Issue object if found
        """
        try:
            issue_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}"
            )
            
            if not isinstance(issue_data, dict):
                raise ValueError(f"Unexpected response format: {type(issue_data)}")

            return Issue(
                id=issue_data.get('id', ''),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                estimate_point=issue_data.get('estimate_point'),
                name=issue_data.get('name', ''),
                description_html=issue_data.get('description_html', ''),
                description_stripped=issue_data.get('description_stripped', ''),
                priority=issue_data.get('priority', ''),
                start_date=issue_data.get('start_date'),
                target_date=issue_data.get('target_date'),
                sequence_id=issue_data.get('sequence_id', 0),
                sort_order=float(issue_data.get('sort_order', 0.0)),
                completed_at=issue_data.get('completed_at'),
                archived_at=issue_data.get('archived_at'),
                is_draft=issue_data.get('is_draft', False),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
                parent=issue_data.get('parent'),
                state=issue_data.get('state', ''),
                assignees=issue_data.get('assignees', []),
                labels=issue_data.get('labels', [])
            )
            
        except Exception as e:
            logging.error(f"Error getting issue details: {e}")
            raise PlaneError("Error fetching issue details")
        
    async def create_issue(self, name: str, project_id: str, **kwargs) -> Issue:
        """
        Create a new issue with provided data.

        Args:
            name (str): Name of the issue (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid Issue field to update

        Returns:
            Issue: Created Issue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Issue.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            issue_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/", 
                json=filtered_data
            )
            
            return Issue(
                id=issue_data.get('id', ''),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                estimate_point=issue_data.get('estimate_point'),
                name=issue_data.get('name', ''),
                description_html=issue_data.get('description_html', ''),
                description_stripped=issue_data.get('description_stripped', ''),
                priority=issue_data.get('priority', ''),
                start_date=issue_data.get('start_date'),
                target_date=issue_data.get('target_date'),
                sequence_id=issue_data.get('sequence_id', 0),
                sort_order=float(issue_data.get('sort_order', 0.0)),
                completed_at=issue_data.get('completed_at'),
                archived_at=issue_data.get('archived_at'),
                is_draft=issue_data.get('is_draft', False),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
                parent=issue_data.get('parent'),
                state=issue_data.get('state', ''),
                assignees=issue_data.get('assignees', []),
                labels=issue_data.get('labels', [])
            )

        except Exception as e:
            logging.error(f"Error creating Issue: {e}")
            raise PlaneError("Error creating issue")
        
    async def update_issue(self, name: str, project_id: str, issue_id: str, **kwargs) -> Issue:
        """
        Update an issue with provided fields.

        Args:
            name: Name of the issue (Required)
            project_id (str): The ID of the project to update (Required)
            issue_id (str): The ID of the issue to update (Required)
            **kwargs: Any valid Issue field to update

        Returns:
            Issue: Updated Issue object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Project class
        valid_fields = Issue.__annotations__.keys()
        filtered_data = {
            'name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            issue_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return Issue(
                id=issue_data.get('id', ''),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                estimate_point=issue_data.get('estimate_point'),
                name=issue_data.get('name', ''),
                description_html=issue_data.get('description_html', ''),
                description_stripped=issue_data.get('description_stripped', ''),
                priority=issue_data.get('priority', ''),
                start_date=issue_data.get('start_date'),
                target_date=issue_data.get('target_date'),
                sequence_id=issue_data.get('sequence_id', 0),
                sort_order=float(issue_data.get('sort_order', 0.0)),
                completed_at=issue_data.get('completed_at'),
                archived_at=issue_data.get('archived_at'),
                is_draft=issue_data.get('is_draft', False),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
                parent=issue_data.get('parent'),
                state=issue_data.get('state', ''),
                assignees=issue_data.get('assignees', []),
                labels=issue_data.get('labels', [])
            )
            
        except Exception as e:
            logging.error(f"Error updating issue: {e}")
            raise PlaneError("Error updating issue")
        
    async def delete_issue(self, project_id: str, issue_id: str) -> bool:
        """
        Delete an existing issue.

        Args:
            project_id: The ID of the project containing the issue (Required)
            issue_id: The ID of the issue to be deleted (Required)

        Returns:
            bool: True if issue was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issues/{issue_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting issue: {e}")
            return False
        
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
        
    async def get_cycles(self, project_id: str) -> list[Cycle]:
        """
        Fetch all cycles for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[Cycle]: List of Cycle objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/")
            
            if isinstance(response, dict) and 'results' in response:
                project_cycles = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            cycles = []
            for cycle_data in project_cycles:
                try:
                    cycle = Cycle(
                        id=cycle_data.get('id', ''),
                        created_at=cycle_data.get('created_at', ''),
                        updated_at=cycle_data.get('updated_at', ''),
                        name=cycle_data.get('name', ''),
                        description=cycle_data.get('description', ''),
                        start_date=cycle_data.get('start_date'),
                        end_date=cycle_data.get('end_date'),
                        view_props=cycle_data.get('view_props', {}),
                        sort_order=float(cycle_data.get('sort_order', 0.0)),
                        created_by=cycle_data.get('created_by', ''),
                        updated_by=cycle_data.get('updated_by', ''),
                        project=cycle_data.get('project', ''),
                        workspace=cycle_data.get('workspace', ''),
                        owned_by=cycle_data.get('owned_by', '')
                    )
                    cycles.append(cycle)
                except TypeError as e:
                    logging.error(f"Error creating cycle object: {e}")
                    logging.debug(f"Cycle data: {cycle_data}")
                    continue
                    
            return cycles
            
        except Exception as e:
            logging.error(f"Error getting cycles: {e}")
            raise PlaneError("Error fetching project cycles")
        
    async def get_cycle_details(self, project_id: str, cycle_id: str) -> Cycle:
        """
        Fetch specific cycle details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            cycle_id (str): ID of the cycle to fetch (Required)
            
        Returns:
            Cycle: Cycle object if found
        """
        try:
            cycle_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}"
            )
            
            if not isinstance(cycle_data, dict):
                raise ValueError(f"Unexpected response format: {type(cycle_data)}")

            return Cycle(
                id=cycle_data.get('id', ''),
                created_at=cycle_data.get('created_at', ''),
                updated_at=cycle_data.get('updated_at', ''),
                name=cycle_data.get('name', ''),
                description=cycle_data.get('description', ''),
                start_date=cycle_data.get('start_date'),
                end_date=cycle_data.get('end_date'),
                view_props=cycle_data.get('view_props', {}),
                sort_order=float(cycle_data.get('sort_order', 0.0)),
                created_by=cycle_data.get('created_by', ''),
                updated_by=cycle_data.get('updated_by', ''),
                project=cycle_data.get('project', ''),
                workspace=cycle_data.get('workspace', ''),
                owned_by=cycle_data.get('owned_by', '')
            )
            
        except Exception as e:
            logging.error(f"Error getting cycle details: {e}")
            raise PlaneError("Error fetching cycle details")
        
    async def create_cycle(self, name: str, project_id: str, **kwargs) -> Cycle:
        """
        Create a new cycle with provided data.

        Args:
            name (str): Name of the cycle (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid Cycle field to update

        Returns:
            Cycle: Created Cycle object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = Cycle.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            cycle_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/", 
                json=filtered_data
            )
            
            return Cycle(
                id=cycle_data.get('id', ''),
                created_at=cycle_data.get('created_at', ''),
                updated_at=cycle_data.get('updated_at', ''),
                name=cycle_data.get('name', ''),
                description=cycle_data.get('description', ''),
                start_date=cycle_data.get('start_date'),
                end_date=cycle_data.get('end_date'),
                view_props=cycle_data.get('view_props', {}),
                sort_order=float(cycle_data.get('sort_order', 0.0)),
                created_by=cycle_data.get('created_by', ''),
                updated_by=cycle_data.get('updated_by', ''),
                project=cycle_data.get('project', ''),
                workspace=cycle_data.get('workspace', ''),
                owned_by=cycle_data.get('owned_by', '')
            )

        except Exception as e:
            logging.error(f"Error creating Cycle: {e}")
            raise PlaneError("Error creating cycle")
        
    async def update_cycle(self, name: str, project_id: str, cycle_id: str, **kwargs) -> Cycle:
        """
        Update a cycle with provided fields.

        Args:
            name: Name of the cycle (Required)
            project_id (str): The ID of the project to update (Required)
            cycle_id (str): The ID of the cycle to update (Required)
            **kwargs: Any valid Cycle field to update

        Returns:
            Cycle: Updated Cycle object

        Raises:
            ValueError: If response format is unexpected
        """
        # Get valid fields from Cycle class
        valid_fields = Cycle.__annotations__.keys()
        filtered_data = {
            'name': name
        }
        
        # Filter out any invalid fields from kwargs
        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})
        
        if not filtered_data:
            raise ValueError("No valid fields provided for update")
        
        try:
            cycle_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}/", 
                json=filtered_data
            )
            
            # Filter response data to only include valid fields
            return Cycle(
                id=cycle_data.get('id', ''),
                created_at=cycle_data.get('created_at', ''),
                updated_at=cycle_data.get('updated_at', ''),
                name=cycle_data.get('name', ''),
                description=cycle_data.get('description', ''),
                start_date=cycle_data.get('start_date'),
                end_date=cycle_data.get('end_date'),
                view_props=cycle_data.get('view_props', {}),
                sort_order=float(cycle_data.get('sort_order', 0.0)),
                created_by=cycle_data.get('created_by', ''),
                updated_by=cycle_data.get('updated_by', ''),
                project=cycle_data.get('project', ''),
                workspace=cycle_data.get('workspace', ''),
                owned_by=cycle_data.get('owned_by', '')
            )
            
        except Exception as e:
            logging.error(f"Error updating cycle: {e}")
            raise PlaneError("Error updating cycle")
        
    async def delete_cycle(self, project_id: str, cycle_id: str) -> bool:
        """
        Delete an existing cycle.

        Args:
            project_id: The ID of the project containing the cycle (Required)
            cycle_id: The ID of the cycle to be deleted (Required)

        Returns:
            bool: True if cycle was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/{cycle_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting cycle: {e}")
            return False
        
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
        
    async def get_intake_issues(self, project_id: str) -> list[IntakeIssue]:
        """
        Fetch all intake issues for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[IntakeIssue]: List of IntakeIssue objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/cycles/")
            
            if isinstance(response, dict) and 'results' in response:
                intake_issues = response['results']
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            issues = []
            for issue_data in intake_issues:
                try:
                    issue = IntakeIssue(
                        id=issue_data.get('id', ''),
                        pending_issue_count=issue_data.get('pending_issue_count', 0),
                        created_at=issue_data.get('created_at', ''),
                        updated_at=issue_data.get('updated_at', ''),
                        name=issue_data.get('name', ''),
                        description=issue_data.get('description', ''),
                        is_default=issue_data.get('is_default', False),
                        view_props=issue_data.get('view_props', {}),
                        created_by=issue_data.get('created_by', ''),
                        updated_by=issue_data.get('updated_by', ''),
                        project=issue_data.get('project', ''),
                        workspace=issue_data.get('workspace', ''),
                    )
                    issues.append(issue)
                except TypeError as e:
                    logging.error(f"Error creating IntakeIssue object: {e}")
                    logging.debug(f"Issue data: {issue_data}")
                    continue
                    
            return issues
            
        except Exception as e:
            logging.error(f"Error getting IntakeIssues: {e}")
            raise PlaneError("Error fetching project IntakeIssues")
        
    async def get_intake_issue_details(self, project_id: str, issue_id: str) -> IntakeIssue:
        """
        Fetch specific IntakeIssue details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue to fetch (Required)
            
        Returns:
            IntakeIssue: IntakeIssue object if found
        """
        try:
            issue_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/{issue_id}"
            )
            
            if not isinstance(issue_data, dict):
                raise ValueError(f"Unexpected response format: {type(issue_data)}")

            return IntakeIssue(
                id=issue_data.get('id', ''),
                pending_issue_count=issue_data.get('pending_issue_count', 0),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                name=issue_data.get('name', ''),
                description=issue_data.get('description', ''),
                is_default=issue_data.get('is_default', False),
                view_props=issue_data.get('view_props', {}),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
            )
        
        except Exception as e:
            logging.error(f"Error getting issue details: {e}")
            raise PlaneError("Error fetching issue details")
        
    async def create_intake_issue(self, issue: dict, project_id: str) -> IntakeIssue:
        """
        Create a new IntakeIssue with provided data.

        Args:
            issue (dict): Information to upload for the issue (Required)
            project_id (str): ID of the project (Required)

        Returns:
            IntakeIssue: Created IntakeIssue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IntakeIssue.__annotations__.keys()
        filtered_data = {"issue":{
            'name': issue.get('name', 'N/A')
        }}

        filtered_data["issue"].update({k: v for k, v in issue.items() if k in valid_fields})

        try:
            issue_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/", 
                json=filtered_data
            )
            
            return IntakeIssue(
                id=issue_data.get('id', ''),
                pending_issue_count=issue_data.get('pending_issue_count', 0),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                name=issue_data.get('name', ''),
                description=issue_data.get('description', ''),
                is_default=issue_data.get('is_default', False),
                view_props=issue_data.get('view_props', {}),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
            )

        except Exception as e:
            logging.error(f"Error creating IntakeIssue: {e}")
            raise PlaneError("Error creating IntakeIssue")
        
    async def update_intake_issue(self, issue: dict, project_id: str, issue_id: str) -> IntakeIssue:
        """
        Update a IntakeIssue with provided data.

        Args:
            issue (dict): Information to upload for the issue (Required)
            project_id (str): ID of the project (Required)
            issue_id (str): ID of the issue to update (Required)

        Returns:
            IntakeIssue: Updated IntakeIssue object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IntakeIssue.__annotations__.keys()
        filtered_data = {"issue":{
            'name': issue.get('name', 'N/A')
        }}

        filtered_data["issue"].update({k: v for k, v in issue.items() if k in valid_fields})

        try:
            issue_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/{issue_id}", 
                json=filtered_data
            )
            
            return IntakeIssue(
                id=issue_data.get('id', ''),
                pending_issue_count=issue_data.get('pending_issue_count', 0),
                created_at=issue_data.get('created_at', ''),
                updated_at=issue_data.get('updated_at', ''),
                name=issue_data.get('name', ''),
                description=issue_data.get('description', ''),
                is_default=issue_data.get('is_default', False),
                view_props=issue_data.get('view_props', {}),
                created_by=issue_data.get('created_by', ''),
                updated_by=issue_data.get('updated_by', ''),
                project=issue_data.get('project', ''),
                workspace=issue_data.get('workspace', ''),
            )

        except Exception as e:
            logging.error(f"Error creating IntakeIssue: {e}")
            raise PlaneError("Error creating IntakeIssue")
        
    async def delete_intake_issue(self, project_id: str, intake_id: str, issue_id: str) -> bool:
        """
        Delete an existing cycle.

        Args:
            project_id: The ID of the project containing the intake (Required)
            intake_id: The ID of the intake containing the issue (Required)
            issue_id: The ID of the issue to be deleted (Required)

        Returns:
            bool: True if issue was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/intake-issues/{issue_id}"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting IntakeIssue: {e}")
            return False
        
    async def get_issue_types(self, project_id: str) -> list[IssueType]:
        """
        Fetch all issue types for a project.
        
        Args:
            project_id (str): ID of the project (Required)

        Returns:
            list[IssueType]: List of IssueType objects
        """
        try:
            response = await self._request("GET", f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/")
            
            if isinstance(response, dict) and 'results' in response:
                issue_types = response['results']
            elif isinstance(response, list):
                issue_types = response
            else:
                raise ValueError(f"Unexpected response format: {type(response)}")
            
            types = []
            for type_data in issue_types:
                try:
                    type_add = IssueType(
                        id=type_data.get('id', ''),
                        name=type_data.get('name', ''),
                        description=type_data.get('description', ''),
                        logo_props=type_data.get('logo_props', {}),
                        level=type_data.get('level', 0),
                        is_active=type_data.get('is_active', True),
                        is_default=type_data.get('is_default', False),
                        deleted_at=type_data.get('deleted_at', ''),
                        workspace=type_data.get('workspace', ''),
                        project=type_data.get('project', ''),
                        created_by=type_data.get('created_by', ''),
                        updated_by=type_data.get('updated_by', ''),
                        created_at=type_data.get('created_at', ''),
                        updated_at=type_data.get('updated_at', ''),
                        external_id=type_data.get('external_id', ''),
                        external_source=type_data.get('external_source', '')
                    )
                    types.append(type_add)
                except TypeError as e:
                    logging.error(f"Error creating IssueType object: {e}")
                    logging.debug(f"IssueType data: {type_add}")
                    continue
                    
            return types
            
        except Exception as e:
            logging.error(f"Error getting IssueTypes: {e}")
            raise PlaneError("Error fetching project IssueTypes")
        
    async def get_type_details(self, project_id: str, type_id: str) -> IssueType:
        """
        Fetch specific IntakeIssue details for a project.
        
        Args:
            project_id (str): ID of the project (Required)
            type_id (str): ID of the issue type to fetch (Required)
            
        Returns:
            IssueType: IssueType object if found
        """
        try:
            type_data = await self._request(
                "GET", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/"
            )
            
            if not isinstance(type_data, dict):
                raise ValueError(f"Unexpected response format: {type(type_data)}")

            return IssueType(
                id=type_data.get('id', ''),
                name=type_data.get('name', ''),
                description=type_data.get('description', ''),
                logo_props=type_data.get('logo_props', {}),
                level=type_data.get('level', 0),
                is_active=type_data.get('is_active', True),
                is_default=type_data.get('is_default', False),
                deleted_at=type_data.get('deleted_at', ''),
                workspace=type_data.get('workspace', ''),
                project=type_data.get('project', ''),
                created_by=type_data.get('created_by', ''),
                updated_by=type_data.get('updated_by', ''),
                created_at=type_data.get('created_at', ''),
                updated_at=type_data.get('updated_at', ''),
                external_id=type_data.get('external_id', ''),
                external_source=type_data.get('external_source', '')
            )
        
        except Exception as e:
            logging.error(f"Error getting issu type details: {e}")
            raise PlaneError("Error fetching issue type details")
        
    async def create_type(self, name: str, project_id: str, **kwargs) -> IssueType:
        """
        Create a new IssueType with provided data.

        Args:
            name (str): Name of the type (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid IssueType field to update

        Returns:
            IssueType: Created IssueType object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IssueType.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            type_data = await self._request(
                "POST", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/", 
                json=filtered_data
            )
            
            return IssueType(
                id=type_data.get('id', ''),
                name=type_data.get('name', ''),
                description=type_data.get('description', ''),
                logo_props=type_data.get('logo_props', {}),
                level=type_data.get('level', 0),
                is_active=type_data.get('is_active', True),
                is_default=type_data.get('is_default', False),
                deleted_at=type_data.get('deleted_at', ''),
                workspace=type_data.get('workspace', ''),
                project=type_data.get('project', ''),
                created_by=type_data.get('created_by', ''),
                updated_by=type_data.get('updated_by', ''),
                created_at=type_data.get('created_at', ''),
                updated_at=type_data.get('updated_at', ''),
                external_id=type_data.get('external_id', ''),
                external_source=type_data.get('external_source', '')
            )

        except Exception as e:
            logging.error(f"Error creating IssueType: {e}")
            raise PlaneError("Error creating issue type")
        
    async def update_type(self, name: str, project_id: str, type_id: str, **kwargs) -> IssueType:
        """
        Update an IssueType with provided data.

        Args:
            name (str): Name of the type (Required)
            project_id (str): ID of the project (Required)
            **kwargs: Any valid IssueType field to update

        Returns:
            IssueType: Updated IssueType object

        Raises:
            ValueError: If response format is unexpected
        """
        valid_fields = IssueType.__annotations__.keys()
        filtered_data = {
            'name': name
        }

        filtered_data.update({k: v for k, v in kwargs.items() if k in valid_fields})

        try:
            type_data = await self._request(
                "PATCH", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/", 
                json=filtered_data
            )
            
            return IssueType(
                id=type_data.get('id', ''),
                name=type_data.get('name', ''),
                description=type_data.get('description', ''),
                logo_props=type_data.get('logo_props', {}),
                level=type_data.get('level', 0),
                is_active=type_data.get('is_active', True),
                is_default=type_data.get('is_default', False),
                deleted_at=type_data.get('deleted_at', ''),
                workspace=type_data.get('workspace', ''),
                project=type_data.get('project', ''),
                created_by=type_data.get('created_by', ''),
                updated_by=type_data.get('updated_by', ''),
                created_at=type_data.get('created_at', ''),
                updated_at=type_data.get('updated_at', ''),
                external_id=type_data.get('external_id', ''),
                external_source=type_data.get('external_source', '')
            )

        except Exception as e:
            logging.error(f"Error creating IssueType: {e}")
            raise PlaneError("Error creating issue type")
        
    async def delete_issue_type(self, project_id: str, type_id: str) -> bool:
        """
        Delete an existing cycle.

        Args:
            project_id: The ID of the project containing the intake (Required)
            type_id: The ID of the type to be deleted (Required)

        Returns:
            bool: True if issue type was deleted successfully, False otherwise
            
        Raises:
            PlaneError: If deletion fails
        """
        try:
            await self._request(
                "DELETE", 
                f"/api/v1/workspaces/{self.workspace_slug}/projects/{project_id}/issue-types/{type_id}/"
            )
            return True

        except Exception as e:
            logging.error(f"Error deleting IssueType: {e}")
            return False
        
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