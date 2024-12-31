import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        issue_types = await client.get_issue_types(project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd")
        for issue_type in issue_types:
            properties = await client.get_issue_properties(project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd", type_id=issue_type.id)
            for property in properties:
                print(property.id, issue_type.id)
        deleted_issue_property = await client.delete_property(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            type_id="5ba86e3a-304a-4df2-aceb-5ae5921d4274",
            property_id="a47b4ef5-1cef-41dd-b7ce-8cd23346dce0"
        )
        print(deleted_issue_property)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())