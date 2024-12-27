import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_label = await client.delete_label(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            label_id="a29dab20-c4d2-4263-b3d6-451935d714b2",
        )
        print(deleted_label)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())