from datetime import datetime
from pydantic import BaseModel

class SensorDataDB(BaseModel):
    sensor_id: int
    data: int
    timestamp: datetime
