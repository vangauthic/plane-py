import asyncio
from plane_py import PlaneClient
#sequence id = 3
async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        issue_activity = await client.get_activity_details(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e",
            activity_id="68e46fde-023b-4c99-ab2d-b15f46a3588d"
        )
        print(issue_activity.created_at)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())