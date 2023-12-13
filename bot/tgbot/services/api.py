import aiohttp

main_url = "http://web:8000"

async def update_or_create_user(user_id, full_name):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{main_url}/api/create-new-user", params={"name": full_name, "chat_id": user_id}) as response:
            return await response.json()
        
async def get_regions(lang):
    payload = {"lang": lang}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{main_url}/api/get-regions", params=payload) as response:
            return await response.json()
        
async def get_districts(region_id):
    payload = {"pk": int(region_id)}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{main_url}/api/get-districts", params=payload) as response:
            return await response.json()
        
async def get_masjidlar(district_id, page=1):
    payload = {"district_id": int(district_id),
               "page": int(page)}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{main_url}/api/get-masjidlar", params=payload) as response:
            return await response.json()
        
