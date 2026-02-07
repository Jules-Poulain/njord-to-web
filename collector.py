print("Collector.py started")

import asyncio
from njordlink_query import get_latest_pgns
from db import get_session
from models import BoatData


def extract_from_pgns(readings: dict):
    lat = lon = sog = cog = heading = boatspeed = tws = twa = twd = None

    for msg in readings.values():
        pgn = msg.get("pgn")

        # Position
        if pgn in (129025, 129029):
            lat = msg.get("Latitude")
            lon = msg.get("Longitude")

        # SOG / COG
        elif pgn == 129026:
            sog = msg.get("SOG")
            cog = msg.get("COG")

        # Heading
        elif pgn == 127250:
            heading = msg.get("Heading")

        # Boat speed through water
        elif pgn == 128259:
            boatspeed = msg.get("Speed Water Referenced")

        # Wind
        elif pgn == 130306:
            tws = msg.get("Wind Speed")
            twa = msg.get("Wind Angle")

        # Wind direction sometimes separate
        elif pgn == 130577:
            twd = msg.get("Wind Direction")

    return lat, lon, sog, cog, boatspeed, heading, tws, twa, twd


async def collect():
    data = await get_latest_pgns()

    if not data:
        print("No data from Njord")
        return

    readings = data["data"]["readings"]

    lat, lon, sog, cog, boatspeed, heading, tws, twa, twd = extract_from_pgns(readings)

    print(f"LAT:{lat} LON:{lon} SOG:{sog} COG:{cog} STW:{boatspeed} HDG:{heading} TWS:{tws} TWA:{twa} TWD:{twd}")

    session = get_session()

    entry = BoatData(
        lat=lat,
        lon=lon,
        sog=sog,
        cog=cog,
        boatspeed=boatspeed,
        heading=heading,
        tws=tws,
        twa=twa,
        twd=twd,
        raw=readings
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

        await asyncio.sleep(60)


if __name__ == "__main__":
    print("Collector loop started")
    asyncio.run(loop_collect())