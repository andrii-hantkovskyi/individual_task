from motor.motor_asyncio import AsyncIOMotorClient

import settings

client = AsyncIOMotorClient(settings.DB_URI)
database = client.IndividualTask
