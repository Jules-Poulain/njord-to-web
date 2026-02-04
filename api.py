from fastapi import FastAPI
import asyncio
from njordlink_query import get_latest_pgns  # we will create this

app = FastAPI()

@app.get("/boat")
async def boat_data():
    data = await get_latest_pgns()
    return data