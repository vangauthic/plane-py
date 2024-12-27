import asyncio
from plane_py import PlaneClient
#sequence id = 3
async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_module = await client.delete_module(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="83c29ebc-4f96-45da-8982-8f0f7c36fba9"
        )
        print(deleted_module)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())