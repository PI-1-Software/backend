from datetime import datetime
from typing import TypedDict

import asyncpg

HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
DATABASE = "carrinho"


__pool: asyncpg.Pool = None  # type: ignore


class Record(TypedDict):
    id_path: int
    position: tuple[float, float]
    instant_velocity: float
    instant_acceleration: float
    energy_consumption: float
    timestamp: datetime


async def get_pool() -> asyncpg.Pool:
    global __pool
    if __pool is None:
        __pool = await asyncpg.create_pool(  # type: ignore
            host=HOST, user=USER, password=PASSWORD, database=DATABASE
        )
    return __pool


async def insert(record: Record):
    async with (await get_pool()).acquire() as connection:
        columns, values = zip(*record.items())
        sql = "INSERT INTO records ({}) VALUES ({})".format(
            ", ".join(columns),
            ", ".join(["$" + str(i + 1) for i in range(len(columns))]),
        )
        await connection.execute(sql, *values)


if __name__ == "__main__":
    import asyncio
    from datetime import datetime

    async def test():
        record: Record = {
            "id_path": 1,
            "position": (1.0, 2.0),
            "instant_velocity": 3.0,
            "instant_acceleration": 4.0,
            "energy_consumption": 5.0,
            "timestamp": datetime.now(),
        }
        await insert(record)

    asyncio.run(test())
