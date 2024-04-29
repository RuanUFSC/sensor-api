from pydantic import BaseModel
from typing import List

class SensorData(BaseModel):
    sensor_id: int
    data: int

class SensorDataResponse(BaseModel):
    sensor_id: int
    data: int
    timestamp: str

class SensorDataListResponse(BaseModel):
    data: List[SensorDataResponse]
