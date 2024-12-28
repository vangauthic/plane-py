import asyncio
from plane_py import PlaneClient
#sequence id = 3
async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_cycle_issue = await client.delete_cycle_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            cycle_id="872f4637-b77d-4ab3-9427-a36cc3cd387a",
            issue_id="815c4689-7525-46d3-a19d-d2f58bcfadbf"
        )
        print(deleted_cycle_issue)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())