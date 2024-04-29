from motor.motor_asyncio import AsyncIOMotorClient
from models import SensorDataDB
from typing import List

class SensorDataRepository:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.db_name.sensor_data
        
    async def insert_sensor_data(self, sensor_data: SensorDataDB):
        await self.collection.insert_one(sensor_data.model_dump())


    async def get_sensor_data(self, sensor_id: int) -> List[SensorDataDB]:
        cursor = self.collection.find({"sensor_id": sensor_id}).sort("_id", -1).limit(10)  # Exemplo de consulta dos últimos 10 registros
   
