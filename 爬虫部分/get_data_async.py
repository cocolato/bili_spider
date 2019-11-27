from motor.motor_asyncio import AsyncIOMotorClient
import aiohttp
import datetime
import asyncio


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}
url_dic = {
    'day_all': 'https://www.bilibili.com/ranking/all/0/0/1',
    'day_origin': 'https://www.bilibili.com/ranking/origin/0/0/1',
    'day_cinema': 'https://www.bilibili.com/ranking/cinema/177/0/1',
    'day_rookie': 'https://www.bilibili.com/ranking/rookie/0/0/1',
}
json_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='

client = AsyncIOMotorClient('mongodb://localhost:27017')
dbs = client['video']
collection = dbs['avnum_rank']
data_dbs = client['videodata']


async def do_find(year, month, day, _type):
    document = await collection.find_one({"type": _type, "datetime": {"$gt": datetime.datetime(year, month, day)}})
    return [json_url+av_num for av_num in document['rank']]


def get_task_list(year, month, day):
    return [asyncio.ensure_future(do_find(year, month, day, _type)) for _type in url_dic.keys()]


async def fetch(url):
    async with aiohttp.TCPConnector(limit=30, verify_ssl=False) as tc:
        async with aiohttp.ClientSession(connector=tc) as session:
            async with session.get(url, headers=head) as req:
                status = req.status
                if status in [200, 201]:
                    json_data = await req.json()
                    print(json_data)
                    json_data['data']['datetime'] = datetime.datetime.now()
                    av_num = str(json_data['data']['aid'])
                    try:
                        data_dbs[av_num].insert_one(json_data['data'])
                    except Exception as e:
                        print(e)
                else:
                    print("error")


if __name__ == '__main__':

    task_list = get_task_list(2019, 10, 30)
    json_url_list = []
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(task_list))
        for task in task_list:
            json_url_list.extend(task.result())
    except Exception as e:
        print(e)
    task_list = [fetch(url) for url in json_url_list]
    print(task_list)
    try:
        loop.run_until_complete(asyncio.wait(task_list))
    except Exception as e:
        print(e)
    finally:
        loop.close()



