import asyncio
import aiohttp
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from repositories import SensorDataRepository
from models import SensorDataDB
        
async def fetch_sensor_data(sensor_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:5000/api/v1/sensors?name=sensor{sensor_id}') as response:
            data = await response.json()
            return data

async def store_sensor_data(sensor_id, repository):
    while True:
        data = await fetch_sensor_data(sensor_id)
        data_value = data['data']  # Acessando a propriedade 'data'
        
        print(data_value)
        timestamp = datetime.now()  # Capturando o timestamp atual
        
        sensor_data = SensorDataDB(sensor_id=sensor_id, data=data_value, timestamp=timestamp)
        await repository.insert_sensor_data(sensor_data)
        await asyncio.sleep(0.3)

async def main():
    db_client = AsyncIOMotorClient("mongodb://localhost:27017")
    repository = SensorDataRepository(db_client)

    tasks = []
    for sensor_id in range(1, 4):
        task = asyncio.create_task(store_sensor_data(sensor_id, repository))
        tasks.append(task)

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
