import asyncio
from plane_py.api import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_133420591f5344e5ba787e62c9e250ff", workspace_slug="plane-py")
    try:
        new_project = await client.create_project(name="Test Project", identifier="testX")
        print(new_project)
        print(await client.delete_project(project_id='50d503d8-b1a2-4815-b7a2-d69088f73411'))
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())