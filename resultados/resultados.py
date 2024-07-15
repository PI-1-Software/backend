from datetime import datetime
import json
from typing import TypedDict

import numpy as np
from matplotlib import pyplot as plt


class Trajectory(TypedDict):
    orientation: str  # Reto, Direita, Esquerda, Parado
    energy: float
    acceleration: tuple[float, float]
    time: str


class ResultItem(TypedDict):
    position: tuple[float, float]
    instant_velocity: float
    instant_acceleration: float
    time: float
    energy_consumption: float


class Result(TypedDict):
    results: list[ResultItem]
    total_energy_consumption: float
    average_velocity: float


for i in range(1, 4):
    with open(f"trajeto{i}.json") as f:
        data: list[Trajectory] = json.load(f)

    results: list[ResultItem] = [
        {
            "position": (0.0, 0.0),
            "instant_velocity": 0,
            "instant_acceleration": 0,
            "time": 0,
            "energy_consumption": 0,
        }
    ]
    last_time = datetime.strptime(data.pop(0)["time"], "%Y-%m-%d %H:%M:%S,%f")

    max_velocity = 0.1
    velocity = np.array([0, 0])
    acceleration = np.array([0.01, 0.01])
    for x in data:
        if x["orientation"] == "Parado":
            break

        time = datetime.strptime(x["time"], "%Y-%m-%d %H:%M:%S,%f")
        dt = (time - last_time).total_seconds()
        last_time = time

        angle = 8.5 * np.pi / 180
        match x["orientation"]:
            case "Direita":
                acceleration = np.array(
                    [
                        acceleration[0] * np.cos(angle) - acceleration[1] * np.sin(angle),
                        acceleration[0] * np.sin(angle) + acceleration[1] * np.cos(angle),
                    ]
                )
            case "Esquerda":
                acceleration = np.array(
                    [
                        acceleration[0] * np.cos(-angle) - acceleration[1] * np.sin(-angle),
                        acceleration[0] * np.sin(-angle) + acceleration[1] * np.cos(-angle),
                    ]
                )

        velocity = velocity + acceleration
        if np.linalg.norm(velocity) > max_velocity:
            velocity = velocity / np.linalg.norm(velocity) * max_velocity
        position = np.array(results[-1]["position"]) + velocity
        energy_consumption = x["energy"]
        results.append(
            {
                "position": (float(position[0]), float(position[1])),
                "instant_velocity": float(np.linalg.norm(velocity)),
                "instant_acceleration": float(np.linalg.norm(np.array(x["acceleration"]))),
                "time": results[-1]["time"] + dt,
                "energy_consumption": energy_consumption / 1000,
            }
        )

    total_energy_consumption = sum(x["energy_consumption"] for x in results)
    average_velocity = np.mean([x["instant_velocity"] for x in results])

    result = {
        "results": results,
        "total_energy_consumption": total_energy_consumption,
        "average_velocity": average_velocity,
    }

    plt.figure()
    plt.plot([x["position"][0] for x in results], [x["position"][1] for x in results])
    plt.savefig(f"resultado_trajeto{i}.png")

    with open(f"resultado_trajeto{i}.json", "w") as f:
        json.dump(result, f, indent=2)
