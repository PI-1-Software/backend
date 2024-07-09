from datetime import datetime
from os import getenv
from typing import TypedDict

import asyncpg

HOST = getenv("DB_HOST", "localhost")
USER = getenv("DB_USER", "postgres")
PASSWORD = getenv("DB_PSWD", "postgres")
DATABASE = getenv("DB_NAME", "carrinho")


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


async def get_next_path_id() -> int:
    async with (await get_pool()).acquire() as connection:
        return await connection.fetchval("SELECT MAX(id_path) + 1 FROM records") or 0
    
async def calculate_averages():
    async with (await get_pool()).acquire() as connection:
        query = """
            SELECT AVG(instant_velocity) AS avg_velocity,
                   AVG(instant_acceleration) AS avg_acceleration,
                   AVG(energy_consumption) AS avg_energy
            FROM records
        """
        result = await connection.fetchrow(query)

        if result:
            averages = {
                "average_velocity": result["avg_velocity"] or 0.0,
                "average_acceleration": result["avg_acceleration"] or 0.0,
                "average_energy_consumption": result["avg_energy"] or 0.0,
            }
            return averages
        else:
            raise Exception("No records found to calculate averages")

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
        
        averages = await calculate_averages()
        print("Averages calculated:", averages)

    asyncio.run(test())
