import asyncio
import uvicorn
import subprocess
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket
from sensor_data_fetcher import main as start_sensor_data_fetcher
from typing import List
from schemas import SensorDataResponse, SensorDataListResponse
from repositories import SensorDataRepository
from database import connect_to_mongo, close_mongo_connection

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.websocket("/ws/sensor_data/{sensor_id}")
async def websocket_endpoint(websocket: WebSocket, sensor_id: int = None):
    await _handle_websocket(websocket, sensor_id)

@app.websocket("/ws/all_sensor_data")
async def websocket_endpoint(websocket: WebSocket):
    await _handle_websocket(websocket)

async def _handle_websocket(websocket: WebSocket, sensor_id: int = None):
    await websocket.accept()
    db_client = await connect_to_mongo()
    repository = SensorDataRepository(db_client)
    try:
        while True:
            if sensor_id is not None:
                sensor_data = await repository.get_sensor_data(sensor_id)
                await websocket.send_json(sensor_data)
            else:
                all_sensor_data = await repository.get_last_50_sensor_data()
                await websocket.send_json(all_sensor_data)
            await asyncio.sleep(3000)
    finally:
        await close_mongo_connection(db_client)
        
async def run_sensor_data_fetcher():
    await start_sensor_data_fetcher()

if __name__ == "__main__":
    # Iniciar a API Flask como um processo separado
    # flask_process = subprocess.Popen(["python", "app.py"])

    # Iniciar o sensor_data_fetcher
    # asyncio.run(run_sensor_data_fetcher())

    # Iniciar o servidor FastAPI
    uvicorn.run(app, host="0.0.0.0", port=8000)
