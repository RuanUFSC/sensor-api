from motor.motor_asyncio import AsyncIOMotorClient

async def connect_to_mongo():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    return client

async def close_mongo_connection(client: AsyncIOMotorClient):
    client.close()
