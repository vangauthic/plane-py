async def validate_response(response):
    if response.status >= 400:
        error_details = await response.json()
        raise Exception(f"Error: {error_details}")
    return await response.json()