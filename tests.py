import asyncio
from plane_py import PlaneClient

async def main():
    client = PlaneClient(api_token="", workspace_slug="")
    try:
        ...
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())