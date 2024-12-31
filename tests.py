import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="", workspace_slug="")
    try:
        new_project = await client.get_states(project_id="085883b4-356b-4866-b21e-060b7a9c2bc1")
        print(new_project)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())