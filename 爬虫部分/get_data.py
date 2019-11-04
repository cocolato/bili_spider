from pymongo import MongoClient
import time
import requests
import datetime


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}
url_dic = {
    'day_all': 'https://www.bilibili.com/ranking/all/0/0/1',
    'day_origin': 'https://www.bilibili.com/ranking/origin/0/0/1',
    'day_cinema': 'https://www.bilibili.com/ranking/cinema/177/0/1',
    'day_rookie': 'https://www.bilibili.com/ranking/rookie/0/0/1',
}
json_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='

client = MongoClient('mongodb://localhost:27017')
dbs = client.video
collection = dbs.avnum_rank
data_dbs = client.videodata


def do_find(year, month, day, _type):
    document = collection.find_one({"type": _type, "datetime": {"$gt": datetime.datetime(year, month, day)}})
    return [json_url+av_num for av_num in document['rank']]


def get_task_list(year, month, day):
    return [do_find(year, month, day, _type) for _type in url_dic.keys()]


def fetch(url):
            req = requests.get(url, headers=head)
            status = req.status_code
            if status in [200, 201]:
                json_data = req.json()
                print(json_data)
                try:
                    json_data['data']['datetime'] = datetime.datetime.now()
                    av_num = str(json_data['data']['aid'])
                    data_dbs[av_num].insert_one(json_data['data'])
                except Exception as e:
                    print(e)
            else:
                print("status_code error: {}".format(status))



if __name__ == '__main__':
    task_list = get_task_list(2019, 10, 30)
    for task in task_list:
        for url in task:
            fetch(url)
            time.sleep(0.5)




