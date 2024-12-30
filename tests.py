import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_intake_issue = await client.delete_intake_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            intake_id="bd0614d4-a72a-4278-be00-f6b25200d167",
            issue_id="8ac2f864-595d-4816-acbf-ffe611c1d607"
        )
        print(deleted_intake_issue)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())