import asyncio
from plane_py import PlaneClient
# dropdown PROPERTY ID: e41d0a63-0989-4e73-b7ed-b504a687a74d TYPE ID: 5ba86e3a-304a-4df2-aceb-5ae5921d4274
async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        # issue_types = await client.get_issue_types(project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd")
        # for issue_type in issue_types:
        #     properties = await client.get_issue_properties(project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd", type_id=issue_type.id)
        #     for property in properties:
        #         print(property.name, property.id, issue_type.id)

        deleted_property_option = await client.delete_option(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            option_id="fef0416b-4493-4c0a-928e-92ecbfb83fdb"
        )

        print(deleted_property_option)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())