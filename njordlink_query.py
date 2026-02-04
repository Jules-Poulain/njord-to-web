import asyncio
from pprint import pprint

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient

from dotenv import load_dotenv
import os


# Check if .env file exists and load it
load_dotenv()


# Connect to the Viam API
async def connect() -> ViamClient:
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=os.getenv("API_KEY_SECRET"),
        ),
        auth_entity=os.getenv("API_KEY_ID"),
    )
    return await ViamClient.create_from_dial_options(dial_options)


# Main function
async def get_latest_pgns():
    viam_client = await connect()
    data_client = viam_client.data_client

    my_data = await data_client.tabular_data_by_mql(
        organization_id=os.getenv("ORG_ID"),
        query=[
            {
                "$match": {
                    "component_name": "all-pgn",
                    "component_type": "rdk:component:sensor",
                    "method_name": "Readings",
                    "data.readings": {"$ne": {}}
                }
            },
            {"$sort": {"time_received": -1}},
            {"$limit": 1}
        ],
    )

    viam_client.close()
    return my_data[0]["data"]["readings"]


if __name__ == "__main__":
    asyncio.run(main())
