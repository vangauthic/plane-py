import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="plane_api_575cb3353c4842b5bdd3cc9b50446767", workspace_slug="plane-py")
    try:
        # deleted_project = await client.delete_project(
        #     project_id="7856896f-4792-4b4f-a478-ff0c953c4f40"
        # )

        states = await client.get_states(project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd")
        deleted_state = await client.delete_state(
            project_id="65bffcf2-aca0-4305-acaf-d8b0f132c7bd",
            state_id="bd3243f3-53b5-45b1-a55a-eb1003afa89e"
        )

        print(states[1].id, deleted_state)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())