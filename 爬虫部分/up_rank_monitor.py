import requests
import re
from config import video_type, high_video_data_dbs, low_video_data_dbs, video_data_page_url
from get_data import VideoDataGetter
from datetime import datetime
from bs4 import BeautifulSoup
from random import choice
import time

head = {
    "Origin": "https://space.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}


def get_new_video(up_id):
    url = "https://api.bilibili.com/x/space/arc/search?mid=" + up_id + "&pn=1&ps=25&order=pubdate&jsonp=jsonp"
    req = requests.get(url, headers=head)
    if req.status_code in [200, 201]:
        res = req.json()
        video_list = res['data']['list']['vlist']
        new_video_id = video_list[0]['aid']
        return str(new_video_id)
    else:
        print(f"请求up主{up_id}空间网页请求错误,状态码{req.status_code}。")
        return


def get_video_date(video_id):
    url = f"https://www.bilibili.com/video/av{video_id}"
    try:
        req = requests.get(url, headers=head)
        if req.status_code in [200, 201]:
            soup = BeautifulSoup(req.text, 'lxml')
            res = soup.find("meta", content=True, itemprop="uploadDate")
            return datetime.strptime(res["content"], "%Y-%m-%d %H:%M:%S")
        else:
            print(f"请求访问视频{video_id}详细信息网页请求错误， 状态码{req.status_code}。")
    except Exception as e:
        print(f"访问视频{video_id}页面发生错误, 错误详情: {e}.")
        return




def can_join_the_queue(video_date):
    interval = datetime.today() - video_date
    if interval.total_seconds() < 600:
        return True
    else:
        return False


def monitor(queue: set):
    req = requests.get("http://www.kanbilibili.com/rank/ups/fans", headers=head)
    if req.status_code in [200, 201]:
        soup = BeautifulSoup(req.text, 'lxml')
        res = soup.find_all(target="_blank", href=re.compile("//space.bilibili.com"))
        for i in res:
            up_space_url = i["href"]
            up_id = up_space_url[up_space_url.find("/", 3) + 1:]
            video_id = get_new_video(up_id)
            if video_id is None:
                continue
            video_date = get_video_date(video_id)
            if video_date is None:
                continue
            if can_join_the_queue(video_date):
                queue.add(video_id)
    else:
        print(f"请求up主排行网站错误,状态码{req.status_code}。")


def get_random_low_video():
    global video_type
    _type = choice(video_type)
    url = f"https://api.bilibili.com/x/web-interface/newlist?rid={_type}&type=0&pn=1&ps=20&\
    jsonp=jsonp&_=1576480421068"
    req = requests.get(url, headers=head)
    if req.status_code in [200, 201]:
        res = req.json()
        return str(res['data']['archives'][0]['aid'])
    else:
        print(f"访问type{_type}json页面错误，状态码{req.status_code}")
        return


if __name__ == '__main__':
    low_video_queue = set()
    high_video_queue = set()
    while len(low_video_queue) < 50:
        low_video_queue.add(video_data_page_url+get_random_low_video())
    print(low_video_queue)
    while True:
        start_time = time.time()
        if len(high_video_queue) < 50:
            monitor(high_video_queue)
            print(high_video_queue)
        for video_id in high_video_queue:
            getter = VideoDataGetter(video_id, high_video_data_dbs)
            getter.get_detail()
        for video_id in low_video_queue:
            getter = VideoDataGetter(video_id, low_video_data_dbs)
            getter.get_detail()
        spend_time = time.time()-start_time
        if spend_time < 360:
            time.sleep(360-spend_time)
