import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_133420591f5344e5ba787e62c9e250ff", workspace_slug="plane-py")
    try:
        new_project = await client.get_states(project_id="7856896f-4792-4b4f-a478-ff0c953c4f40")
        print(new_project[0].name)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())