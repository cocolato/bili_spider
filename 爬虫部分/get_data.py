import requests
import datetime
from pymongo import MongoClient


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}


if __name__ == '__main__':
    client = MongoClient()
    dbs = client.video
    avnum_collection = dbs.avnum
    data_collection = dbs.data
    doc_name = "day_all_2019-10-17"
    avnum_list = avnum_collection.find_one({doc_name: {"$exists": True}})
    json_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='
    url_list = [json_url + url for url in avnum_list[doc_name]]
    print(url_list)
    for json_url in url_list:
        try:
            data = requests.get(json_url, headers=head)
            json_data = data.json()
            json_data['data']['datetime'] = str(datetime.datetime.now())
            data_collection.insert_one(json_data['data'])
        except AttributeError:
            print("AttributeError")

