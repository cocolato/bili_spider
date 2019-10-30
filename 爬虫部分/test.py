from motor.motor_asyncio import AsyncIOMotorClient
import asyncio


client = AsyncIOMotorClient('mongodb://localhost:27017')
dbs = client.video
collection = dbs.avnum_rank

async def do_find_one():
    document = await collection.find_one({"type": "day_all"})  # find_one只能查询一条数据
    print(document['rank'])

loop = asyncio.get_event_loop()
loop.run_until_complete(do_find_one())
