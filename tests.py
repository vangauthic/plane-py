import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="", workspace_slug="")
    try:
        # issue_types = await client.get_issue_types(project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd")
        # for issue_type in issue_types:
        #     properties = await client.get_issue_properties(project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd", type_id=issue_type.id)
        #     for property in properties:
        #         print(property.name, property.id, issue_type.id)

        property_values = await client.get_property_values(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            issue_id="0c039e1d-0be4-4684-9454-18136203491d"
        )

        new_property_value = await client.create_value(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            issue_id="0c039e1d-0be4-4684-9454-18136203491d",
            property_id="e41d0a63-0989-4e73-b7ed-b504a687a74d",
            values=["test"]
        )

        print(property_values)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())