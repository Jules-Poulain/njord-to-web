print("Collector.py started")

import asyncio
from njordlink_query import get_latest_pgns
from db import get_session
from models import BoatData
import uuid


async def collect():
    data = await get_latest_pgns()

    if not data:
        print("No data from Njord")
        return

    print("DATA FROM NJORD:", data)

    readings = data["data"]["readings"]

    session = get_session()

    entry = BoatData(
        id=str(uuid.uuid4()),
        lat=readings["position"]["lat"],
        lng=readings["position"]["lng"],
        sog=readings["sog"],
        cog=readings["cog"],
        pgns=readings
    )

    session.add(entry)
    session.commit()
    session.close()

async def loop_collect():
    while True:
        try:
            await collect()
        except Exception as e:
            print("Collector error:", e)

        await asyncio.sleep(60)  # collect every 60 seconds

if __name__ == "__main__":
    import time
    print("Name loop entered")
    while True:
        print("Data collection in progress...")
        asyncio.run(loop_collect())
        time.sleep(1)
else:
    print("Main loop not entered")