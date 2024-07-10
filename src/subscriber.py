import asyncio
import json
import logging
from os import getenv
from typing import TypedDict

import aiomqtt
import numpy as np

BROKER = getenv("SUB_BROKER", "test.mosquitto.org")
PORT = int(getenv("SUB_PORT", 1883))
TOPIC = getenv("SUB_TOPIC", "/ESP_TEST_PI1_LP/data")
USERNAME = getenv("SUB_USERNAME", None)


class Data(TypedDict):
    type: str
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
                    logging.debug("Raw data: %s", raw_data)
                    data: Data = {
                        "type": raw_data["Tipo"],
                        "energy": raw_data.get("Corrente"),
                        "acceleration": np.array([raw_data["X"], raw_data["Y"]])
                        if raw_data.get("X")
                        else np.array([0.0, 0.0]),
                    }
                    await callback(data)
        except Exception as e:
            logging.error("%s", e, exc_info=True)


if __name__ == "__main__":

    async def print_message(message):
        print(f"Received message: {message}")

    asyncio.run(subscribe(print_message))
