import asyncio
import uvicorn
import subprocess
from fastapi import FastAPI
from sensor_data_fetcher import main as start_sensor_data_fetcher
from typing import List
from schemas import SensorDataResponse, SensorDataListResponse
from repositories import SensorDataRepository
from database import connect_to_mongo, close_mongo_connection

app = FastAPI()

@app.get("/sensor_data/{sensor_id}", response_model=SensorDataListResponse)
async def get_sensor_data(sensor_id: int):
    db_client = await connect_to_mongo()
    repository = SensorDataRepository(db_client)
    sensor_data = await repository.get_sensor_data(sensor_id)
    await close_mongo_connection(db_client)
    if not sensor_data:
        raise HTTPException(status_code=404, detail="Sensor data not found")
    return {"data": sensor_data}

async def run_sensor_data_fetcher():
    await start_sensor_data_fetcher()

if __name__ == "__main__":
    # Iniciar a API Flask como um processo separado
    flask_process = subprocess.Popen(["python", "app.py"])

    # Iniciar o sensor_data_fetcher
    asyncio.run(run_sensor_data_fetcher())

    # Iniciar o servidor FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)

