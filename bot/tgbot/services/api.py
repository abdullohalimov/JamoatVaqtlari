import aiohttp

main_url = "http://localhost:8000"

async def update_or_create_user(user_id, full_name):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{main_url}/api/create-new-user", params={"name": full_name, "chat_id": user_id}) as response:
            return await response.json()
        
async def get_regions(lang):
    payload = {"lang": lang}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{main_url}/api/get-regions", params=payload) as response:
            return await response.json()