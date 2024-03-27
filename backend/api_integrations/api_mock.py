from time import time
import httpx
import asyncio

base_url = "http://localhost:5000/mockapi/"

async def task(id: str):
    endpoints = ["api1/", "api2/", "api3/"]
    client = httpx.AsyncClient()
    tasks = [ client.get(base_url + i + id) for i in endpoints ]
    result = await asyncio.gather(*tasks)
    return result 
