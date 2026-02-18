import os
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def get_latest_pgns():
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=os.getenv("API_KEY_SECRET"),
        ),
        auth_entity=os.getenv("API_KEY_ID"),
    )

    viam_client = ViamClient.create_from_dial_options(dial_options)

    try:
        data_client = viam_client.data_client

        records = await data_client.tabular_data_by_sql(
            organization_id=os.getenv("ORG_ID"),
            sql_query="""
            SELECT * FROM readings
            ORDER BY time_received DESC
            LIMIT 1
            """,
        )

        if not records:
            return None

        return records[0].data

    finally:
        await viam_client.close()
