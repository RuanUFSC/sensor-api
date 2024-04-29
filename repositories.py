from motor.motor_asyncio import AsyncIOMotorClient
from models import SensorDataDB
from typing import List
from bson import ObjectId
from datetime import datetime


class SensorDataRepository:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.db_name.sensor_data
        
    async def insert_sensor_data(self, sensor_data: SensorDataDB):
        await self.collection.insert_one(sensor_data.model_dump())


    async def get_sensor_data(self, sensor_id: int) -> List[SensorDataDB]:
        cursor = self.collection.find({"sensor_id": sensor_id}).sort("_id", -1)
        sensor_data = [SensorDataDB(**data) async for data in cursor]
        return sensor_data
    
    async def get_all_sensor_data(self) -> List[dict]:
        cursor = self.collection.find().sort("_id", -1)
        sensor_data = [data async for data in cursor]
        # Converter ObjectId para string, se necessário, e converter datetime para string ISO
        for data in sensor_data:
            if "_id" in data:
                data["_id"] = str(data["_id"])
            if "timestamp" in data and isinstance(data["timestamp"], datetime):
                data["timestamp"] = data["timestamp"].isoformat()
        return sensor_data
    
    async def get_last_50_sensor_data(self) -> List[dict]:
        cursor = self.collection.find().sort("timestamp", -1).limit(50)
        sensor_data = [data async for data in cursor]
        for data in sensor_data:
            if "_id" in data:
                data["_id"] = str(data["_id"])
            if "timestamp" in data and isinstance(data["timestamp"], datetime):
                data["timestamp"] = data["timestamp"].isoformat()
        return sensor_data
