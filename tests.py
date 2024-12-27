import asyncio
from plane_py import PlaneClient
#sequence id = 3
async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_module_issue = await client.delete_module_issue(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            module_id="81522e51-d598-4b41-85f8-dd4d562a91a0",
            issue_id="dfa4c511-234e-48c6-83eb-5fda38fc108e"
        )
        print(deleted_module_issue)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())