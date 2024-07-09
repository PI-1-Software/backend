from datetime import datetime
from typing import TypedDict


class PathData(TypedDict):
    id_path: int
    position: tuple[float, float]
    average_velocity: float
    instant_velocity: float
    instant_acceleration: float
    energy_consumption: float
    timestamp: datetime
    duration: float
