import asyncio
import json
import logging
from typing import TypedDict

import aiomqtt
import numpy as np

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "ESP_TEST_PI1_LP/data"
USERNAME = None


class Data(TypedDict):
    energy: float
    acceleration: np.ndarray


async def subscribe(callback):
    while True:
        try:
            logging.debug("Connecting to MQTT broker")
            async with aiomqtt.Client(BROKER, PORT, username=USERNAME) as client:
                logging.debug("Subscribing to topic")
                await client.subscribe(TOPIC)
                logging.info("Waiting for messages")
                async for message in client.messages:
                    raw_data = json.loads(message.payload)  # type: ignore
                    data: Data = {
                        "energy": raw_data["Corrente"],
                        "acceleration": np.array([raw_data["X"], raw_data["Y"]]),
                    }
                    await callback(data)
        except Exception as e:
            logging.error("%s", e)


if __name__ == "__main__":

    async def print_message(message):
        print(f"Received message: {message}")

    asyncio.run(subscribe(print_message))
