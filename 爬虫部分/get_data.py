from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import requests
import datetime
import math
from get_comment import get_hot_comments
from get_index import BaiduIndex


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}
url_dic = {
    # 'day_all': 'https://www.bilibili.com/ranking/all/0/0/1',
    'day_origin': 'https://www.bilibili.com/ranking/origin/0/0/1',
    # 'day_cinema': 'https://www.bilibili.com/ranking/cinema/177/0/1',
    # 'day_rookie': 'https://www.bilibili.com/ranking/rookie/0/0/1',
}
url_head = "https://www.bilibili.com/video/av"
json_url_head = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='

client = MongoClient('mongodb://localhost:27017')
dbs = client.video
collection = dbs.avnum_rank
data_dbs = client.newVideoData


def do_find(year, month, day, _type):
    document = collection.find_one({"type": _type, "datetime": {"$gt": datetime.datetime(year, month, day)}})
    return [json_url_head+av_num for av_num in document['rank']]


def get_task_list(year, month, day):
    return [do_find(year, month, day, _type) for _type in url_dic.keys()]


# 爬取视频关键字
def get_keywords(av_num):
    req = requests.get(url_head + str(av_num), headers=head)
    status = req.status_code
    if status in [200, 201]:
        req.encoding = "utf-8"
        soup = BeautifulSoup(req.text, 'lxml')
        tag_list = [tag.text for tag in soup.find_all("li", "tag")]
        return tag_list
    else:
        print("get_key_words Error Code:{}".format(req.status_code))
        return []


def fetch(url):
            req = requests.get(url, headers=head)
            status = req.status_code
            if status in [200, 201]:
                json_data = req.json()
                json_data['data']['datetime'] = datetime.datetime.now()
                av_num = str(json_data['data']['aid'])

                try:
                    keywords = get_keywords(av_num)
                    today = str(datetime.date.today())
                    baidu_index = BaiduIndex(keywords, today, today).get_index()
                    baidu_index = [int(index["index"]) for index in baidu_index]
                    index_mean = sum(baidu_index) // len(baidu_index)
                    json_data['data']['index'] = index_mean
                    hot_comments = get_hot_comments(av_num)
                    json_data['data']['hot_comments'] = hot_comments
                    print(json_data['data'])
                    data_dbs[av_num].insert_one(json_data['data'])
                except Exception as e:
                    print(e)
            else:
                print("status_code error: {}".format(status))


def get_data_run(year, month, day):
    task_list = get_task_list(year, month, day)
    for task in task_list[0:1]:
        for url in task:
            fetch(url)
            time.sleep(0.3)

