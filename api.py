from fastapi import FastAPI
import asyncio
from njordlink_query import get_latest_pgns  # we will create this

app = FastAPI()

@app.get("/boat")
async def boat_data():
    data = await get_latest_pgns()
    return data

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("Python_Example.api:app", host="0.0.0.0", port=port)