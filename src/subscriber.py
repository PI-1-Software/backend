import asyncio
import json
from typing import TypedDict

import aiomqtt
import numpy as np

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "ESP_TEST_PI1_LP/data"
USERNAME = None


class Data(TypedDict):
    velocity: float
    energy: float
    acceleration: np.ndarray


async def subscribe(callback):
    async with aiomqtt.Client(BROKER, PORT, username=USERNAME) as client:
        await client.subscribe(TOPIC)
        async for message in client.messages:
            raw_data = json.loads(message.payload)  # type: ignore
            data: Data = {
                "velocity": raw_data["Velocidade"],
                "energy": raw_data["Corrente"],
                "acceleration": np.array([raw_data["X"], raw_data["Y"]]),
            }
            await callback(data)


if __name__ == "__main__":

    async def print_message(message):
        print(f"Received message: {message}")

    asyncio.run(subscribe(print_message))
