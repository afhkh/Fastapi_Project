import asyncio
from tortoise import Tortoise

from src.utils.common_db import DB_ORM_CONFIG


async def go():
    await Tortoise.init(config=DB_ORM_CONFIG)
    from tortoise import Tortoise as T
    for name, model in T.apps["models"].items():
        fks = []
        for k, v in model._meta.fields_map.items():
            mn = getattr(v, "model_name", None)
            if mn:
                fks.append((k, mn))
        print(name, "->", fks)
    await Tortoise.close_connections()


asyncio.run(go())
