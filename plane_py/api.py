import aiohttp
import logging
from ._types import *
from .errors import *

class PlaneClient:
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
        
    async def update_label(self, project_id: str, label_id: str, **kwargs) -> Label:
        """
        Update a label with provided fields.

        Args:
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
        
        # Filter out any invalid fields from kwargs
        filtered_data = {k: v for k, v in kwargs.items() if k in valid_fields}
        
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