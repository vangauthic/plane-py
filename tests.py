import asyncio
from plane_py import PlaneClient
#sequence id = 3
async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_cycle = await client.delete_cycle(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="b82818b7-d469-4ee6-bb5a-32b753782652"
        )
        print(deleted_cycle)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())