import asyncio
import json
import logging
from os import getenv

import aiomqtt

import database as db
from path_data import PathData

BROKER = getenv("PUB_BROKER", "mqtt.thingsboard.cloud")
PORT = int(getenv("PUB_PORT", 1883))
TOPIC = getenv("PUB_TOPIC", "v1/devices/me/telemetry")
USERNAME = getenv("PUB_USERNAME", "1w8wpoofr2600lb6i41b")


publish_queue: asyncio.Queue[PathData] = asyncio.Queue()


async def publisher_worker():
    while True:
        try:
            while True:
                logging.info("Waiting for events")
                data = await publish_queue.get()
                logging.debug("Connecting to MQTT broker")
                async with aiomqtt.Client(BROKER, PORT, username=USERNAME) as client:
                    logging.debug("Publishing data: %s", data)

                    dashboard_data = path_data_to_dashboard(data)
                    if data.get("finished", False):
                        average = await db.calculate_averages()
                        dashboard_data.update(path_data_to_report_dashboard(average))

                    await asyncio.gather(
                        client.publish(TOPIC, json.dumps(path_data_to_dashboard(data))),
                        db.insert(path_data_to_database(data)),
                    )
        except Exception as e:
            logging.error("%s", e, exc_info=True)


def path_data_to_dashboard(data: PathData):
    return {
        "velocidade_media": data["average_velocity"],
        "velocidade_inst": data["instant_velocity"],
        "aceleracao_inst": data["instant_acceleration"],
        "tempo_percurso": data["duration"],
        "consumo_energetico": data["energy_consumption"],
        "XPos": data["position"][0],
        "YPos": data["position"][1],
    }


def path_data_to_report_dashboard(data: dict):
    return {
        "velocidade_media_trajeto": data["average_velocity"],
        "velocidade_inst_trajeto": data["average_acceleration"],
        "consumo_energetico_trajeto": data["average_energy_consumption"],
    }


def path_data_to_database(data: PathData) -> db.Record:
    return {
        "id_path": data["id_path"],
        "position": data["position"],
        "instant_velocity": data["instant_velocity"],
        "instant_acceleration": data["instant_acceleration"],
        "energy_consumption": data["energy_consumption"],
        "timestamp": data["timestamp"],
    }


if __name__ == "__main__":
    asyncio.run(publisher_worker())
