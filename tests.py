import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        deleted_link = await client.delete_link(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="d4d6a6c4-7a1a-4ffe-8cd8-1135d2fb4f2e",
            link_id="357ecb87-1157-42f7-95cb-333837bfee44"
        )
        print(deleted_link)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())