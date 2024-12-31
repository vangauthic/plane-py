import aiohttp
import logging
from ._types import *
from .errors import *

from .endpoints.project import ProjectEndpoint
from .endpoints.state import StateEndpoint
from .endpoints.module import ModuleEndpoint
from .endpoints.moduleissue import ModuleIssueEndpoint
from .endpoints.link import LinkEndpoint
from .endpoints.label import LabelEndpoint
from .endpoints.issue import IssueEndpoint
from .endpoints.issuecomment import IssueCommentEndpoint
from .endpoints.issueactivity import IssueActivityEndpoint
from .endpoints.cycle import CycleEndpoint
from .endpoints.cycleissue import CycleIssueEndpoint
from .endpoints.intakeissue import IntakeIssueEndpoint
from .endpoints.issuetype import IssueTypeEndpoint
from .endpoints.issueproperty import IssuePropertyEndpoint
from .endpoints.propertyoption import PropertyOptionEndpoint
from .endpoints.propertyvalue import PropertyValueEndpoint

class PlaneClient(
        ProjectEndpoint,
        StateEndpoint,
        ModuleEndpoint,
        ModuleIssueEndpoint,
        LinkEndpoint,
        LabelEndpoint,
        IssueEndpoint,
        IssueCommentEndpoint,
        IssueActivityEndpoint,
        CycleEndpoint,
        CycleIssueEndpoint,
        IntakeIssueEndpoint,
        IssueTypeEndpoint,
        IssuePropertyEndpoint,
        PropertyOptionEndpoint,
        PropertyValueEndpoint
    ):
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