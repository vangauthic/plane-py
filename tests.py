import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_issue_type = await client.delete_issue_type(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="01aa7856-903b-4602-b794-e2ceea5592c8"
        )
        print(deleted_issue_type)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())