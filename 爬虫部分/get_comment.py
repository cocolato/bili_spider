from pymongo import MongoClient
from bs4 import BeautifulSoup
import datetime
import time
import requests
import datetime
import math

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}
url_dic = {
    'day_all': 'https://www.bilibili.com/ranking/all/0/0/1',
    'day_origin': 'https://www.bilibili.com/ranking/origin/0/0/1',
    'day_cinema': 'https://www.bilibili.com/ranking/cinema/177/0/1',
    'day_rookie': 'https://www.bilibili.com/ranking/rookie/0/0/1',
}
comment_url_head = url = "http://api.bilibili.com/x/reply?type=1&oid="

client = MongoClient('mongodb://localhost:27017')
comment_dbs = client['videoComment']
avnum_ranl_collection = client['video']['avnum_rank']


def do_find(year, month, day, _type):
    document = avnum_ranl_collection.find_one({"type": _type, "datetime": {"$gt": datetime.datetime(year, month, day)}})
    return [av_num for av_num in document['rank']]


def get_task_list(year, month, day):
    return [do_find(year, month, day, _type) for _type in url_dic.keys()]


def get_hot_comments(av_num):
    req = requests.get(comment_url_head + str(av_num), headers=head)
    status = req.status_code
    if status in [200, 201]:
        json_data = req.json()
        hots = json_data["data"]["hots"]
        hot_comments = [hot["content"]["message"] for hot in hots]
        return hot_comments
    else:
        print("av_num: %d, Error code %d" % (av_num, status))
        return []


if __name__ == '__main__':
    task_list = get_task_list(2019, 11, 17)
    for task in task_list:
        for av_num in task:
            hot_comments = get_hot_comments(av_num)
            comment_dbs[av_num].insert_one({"comments": hot_comments, "datetime": datetime.datetime.now()})
            print("av_num: %s Done" % av_num)
            time.sleep(0.5)
