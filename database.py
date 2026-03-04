from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "fastapi_db"

client = None
database = None


async def connect_to_mongo():
    global client, database

    client = AsyncIOMotorClient(MONGO_URL)
    database = client[DB_NAME]

    await client.admin.command("ping")
    print("✅ MongoDB connected successfully")


async def close_mongo_connection():
    global client
    if client:
        client.close()


def get_database():
    return database
