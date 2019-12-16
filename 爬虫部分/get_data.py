import requests
import datetime
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from config import url_dic, video_detail_page_url, user_agent, rank, COOKIES,\
    video_data_page_url, video_rank, low_video_data_dbs, high_video_data_dbs, proxy, video_comment_url
from random import choice


def user_agent_factory():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': COOKIES,
        'DNT': '1',
        'Pragma': 'no-cache',
        'User-Agent': choice(user_agent)
    }
    return headers


def do_find(year, month, day, _type):
    document = video_rank.find_one({"type": _type, "datetime": {"$gt": datetime.datetime(year, month, day)}})
    return [video_data_page_url + av_num for av_num in document['rank']]


def get_task_list(year, month, day):
    return [url for _type in url_dic.keys() for url in do_find(year, month, day, _type)]


class GetError(Exception):
    pass


class VideoDataGetter(requests.Session):

    def __init__(self, url, dbs):
        super(VideoDataGetter, self).__init__()
        self.__database = dbs
        self._url = url
        self.headers.update(user_agent_factory())

    def get_keywords(self, video_id):
        try:
            req = self.get(video_detail_page_url + str(video_id))
        except Exception as e:
            raise GetError(e)
        if req.status_code in [200, 201]:
            req.encoding = 'utf-8'
            soup = BeautifulSoup(req.text, 'lxml')
            tag_list = [tag.text for tag in soup.find_all("li", "tag")]
            return tag_list
        else:
            print(f"请求视频详情网页错误，状态码{req.status_code}.")
            return []

    def get_comments(self, video_id):
        try:
            req = self.get(video_comment_url + str(video_id))
        except Exception as e:
            raise GetError(e)
        if req.status_code in [200, 201]:
            json_data = req.json()
            if json_data['message'] == '0':
                comments = json_data["data"]["hots"]
                if comments is None:
                    return []
                comments = [comment["content"]["message"] for comment in comments]
                return comments
            else:
                print(f"评论数据json返回发生错误，错误详情:{req.json()['message']}")
                return []
        else:
            print(f"请求视频评论网页错误，状态码{req.status_code}.")
            return []

    def get_detail(self):
        url = self._url
        aid = url[url.find('=') + 1:]
        print(f"开始进行视频{aid}的爬取")
        try:
            req = self.get(url)
        except Exception as e:
            raise GetError(e)
        if req.status_code in [200, 201]:
            if req.json()['message'] == '0':
                video_data = req.json()['data']
            else:
                video_data = {'aid': aid}
                print(f"视频{aid}数据json返回发生错误，错误详情: {req.json()['message']}")
        else:
            video_data = {'aid': aid}
            print(f"请求视频{aid}数据网页错误，状态码{req.status_code}.")
        try:
            video_data['keywords'] = self.get_keywords(aid)
            video_data['comments'] = self.get_comments(aid)
            # video_data['index'] = self.get_baidu_live_index(video_data['keywords'])
            video_data['datetime'] = datetime.datetime.now()
            # print(video_data)
            print(f"{aid} Complete!")
        except Exception as e:
            print(f"视频{aid}爬取过程出错，错误信息: {e}.")
            video_data['keywords'] = "None"
            video_data['comments'] = "None"
            # video_data['index'] = "None"
            video_data['datetime'] = "None"

        try:
            self.__database[str(aid)].insert_one(video_data)
        except Exception as e:
            print(f"视频{aid}存入数据库过程发生错误，错误信息：{e}")
        time.sleep(2)

    @staticmethod
    def decrypt(t: str, e: str) -> str:
        n, i, a, result = list(t), list(e), {}, []
        ln = int(len(n) / 2)
        start, end = n[ln:], n[:ln]
        a = dict(zip(end, start))
        return ''.join([a[j] for j in e])

    def get_ptbk(self, uniqid: str):
        try:
            req = self.get(f"http://index.baidu.com/Interface/ptbk?uniqid={uniqid}")
        except Exception as e:
            raise GetError(e)
        if req.status_code in [200, 201]:
            ptbk = req.json()["data"]
            return ptbk

    def get_baidu_live_index(self, keywords: list):
        result = []
        for keyword in keywords:
            try:
                req = self.get(f"http://index.baidu.com/api/LiveApi/getLive?region=0&word={keyword}")
            except Exception as e:
                raise GetError(e)
            if req.status_code in [200, 201]:
                try:
                    if req.json()["status"] == 0:
                        data = req.json()["data"]
                        all_data = data["result"][0]["index"][0]["_all"]
                        uniqid = data["uniqid"]
                        ptbk = self.get_ptbk(uniqid)
                        result.append(int(self.decrypt(ptbk, all_data).split(',')[-1]))
                    else:
                        result.append(0)
                except Exception as e:
                    result.append(0)
            else:
                print(f"请求百度指数网页错误，状态码{req.status_code}.")
                result.append(0)
            time.sleep(0.3)
        if len(result) == 0:
            return 0
        else:
            return sum(result) // len(result)


if __name__ == '__main__':
    while True:
        start = time.time()
        task_list = [video_data_page_url+str(aid) for l in list(rank.values()) for aid in l]
        for task in task_list:
            getter = VideoDataGetter(task, low_video_data_dbs)
            getter.get_detail()
        print(time.time() - start)
        time.sleep(5)
