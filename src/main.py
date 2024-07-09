import asyncio
from datetime import datetime
import logging
from typing import TypedDict

import numpy as np

import database as db
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
    events_count: int
    velocity_sum: float


state: CarState = {
    "id_path": 0,
    "start_timestamp": datetime.min,
    "last_event_timestamp": datetime.min,
    "position": np.array([0.0, 0.0]),
    "velocity": np.array([0.0, 0.0]),
    "acceleration": np.array([0.0, 0.0]),
    "events_count": 0,
    "velocity_sum": 0,
}


async def subscribe_callback(data: Data):
    logging.debug("Received data: %s", data)

    if data["type"] == "averages_report":
        try:
            averages = await db.calculate_averages()
            logging.debug("Averages calculated: %s", averages)

            report_message = {
                "type": "averages_report",
                "averages": averages,
                "timestamp": datetime.now().isoformat(),
            }

            await publish_queue.put(report_message)
        except Exception as e:
            logging.error("Failed to calculate averages: %s", e)
            
        return

    global state

    timestamp = datetime.now()
    delta_time = timestamp - state["last_event_timestamp"]
    if delta_time.total_seconds() > MAX_SECONDS_BETWEEN_EVENTS:
        state["id_path"] = await db.get_next_path_id()
        state["start_timestamp"] = timestamp
        state["position"] = np.array([0.0, 0.0])
        state["velocity"] = np.array([0.0, 0.0])
        state["events_count"] = 0
        state["velocity_sum"] = 0

    state["last_event_timestamp"] = timestamp
    state["velocity"] += state["acceleration"] * delta_time.total_seconds()
    state["position"] += state["velocity"] * delta_time.total_seconds()
    state["velocity_sum"] += float(np.linalg.norm(state["velocity"]))
    state["events_count"] += 1
    state["acceleration"] = data["acceleration"]

    record: PathData = {
        "id_path": state["id_path"],
        "position": (float(state["position"][0]), float(state["position"][1])),
        "duration": (timestamp - state["start_timestamp"]).total_seconds(),
        "average_velocity": state["velocity_sum"] / state["events_count"],
        "instant_velocity": float(np.linalg.norm(state["velocity"])),
        "instant_acceleration": float(np.linalg.norm(state["acceleration"])),
        "energy_consumption": data["energy"],
        "timestamp": timestamp,
    }
    await publish_queue.put(record)


async def main():
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
        level=logging.DEBUG,
    )
    asyncio.create_task(publisher_worker())
    await subscribe(subscribe_callback)


if __name__ == "__main__":
    asyncio.run(main())
