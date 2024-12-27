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