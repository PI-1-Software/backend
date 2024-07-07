import asyncio
from datetime import datetime
from typing import TypedDict

import numpy as np

from path_data import PathData
from publisher import publish_queue, publisher_worker
from subscriber import Data, subscribe

MAX_SECONDS_BETWEEN_EVENTS = 5


class CarState(TypedDict):
    id_path: int
    start_timestamp: datetime
    last_event_timestamp: datetime
    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray


state: CarState = {
    "id_path": 0,
    "start_timestamp": datetime.min,
    "last_event_timestamp": datetime.min,
    "position": np.array([0.0, 0.0]),
    "velocity": np.array([0.0, 0.0]),
    "acceleration": np.array([0.0, 0.0]),
}


async def subscribe_callback(data: Data):
    global state

    timestamp = datetime.now()
    delta_time = timestamp - state["last_event_timestamp"]
    if delta_time.total_seconds() > MAX_SECONDS_BETWEEN_EVENTS:
        state["id_path"] += 1
        state["start_timestamp"] = timestamp
        state["position"] = np.array([0.0, 0.0])
        state["velocity"] = np.array([0.0, 0.0])

    state["velocity"] += state["acceleration"] * delta_time.total_seconds()
    state["position"] += state["velocity"] * delta_time.total_seconds()
    state["acceleration"] = data["acceleration"]

    record: PathData = {
        "id_path": state["id_path"],
        "position": tuple(state["position"]),
        "duration": (timestamp - state["start_timestamp"]).total_seconds(),
        "instant_velocity": float(np.linalg.norm(state["velocity"])),
        "instant_acceleration": float(np.linalg.norm(state["acceleration"])),
        "energy_consumption": data["energy"],
        "timestamp": timestamp,
    }
    await publish_queue.put(record)


async def main():
    asyncio.create_task(publisher_worker())
    await subscribe(subscribe_callback)


if __name__ == "__main__":
    asyncio.run(main())
