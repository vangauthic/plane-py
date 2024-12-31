# Plane-py

An async Python client for the [Plane](https://plane.so) API. This package provides a clean and intuitive interface to interact with Plane's project management features.

## Installation

```bash
pip install plane-py
```

## Quick Start

```python
import asyncio
from plane_py import PlaneClient

async def main():
    # Initialize client
    client = PlaneClient(
        api_token="your_api_token",
        workspace_slug="your_workspace_slug"
    )
    
    # Get all projects
    projects = await client.get_projects()
    for project in projects:
        print(f"Project: {project.name}")
        
        # Get all issues for project
        issues = await client.get_issues(project.id)
        for issue in issues:
            print(f"- Issue: {issue.name}")

asyncio.run(main())
```

## Features

- Full async/await support
- Type hints for better IDE integration
- Comprehensive error handling
- Support for all major Plane API endpoints:
  - Projects
  - States
  - Labels
  - Issues
  - Issue Links
  - Issue Activities
  - Issue Comments
  - Modules
  - Module Issues
  - Cycles
  - Cycle Issues
  - Intake Issues
  - Issue Types
  - Issue Properties
  - Property Options
  - Property Values

## License

This project is licensed under the MIT License - see the LICENSE file for details.
