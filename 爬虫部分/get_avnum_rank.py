from motor.motor_asyncio import AsyncIOMotorClient
from bs4 import BeautifulSoup
from threading import Thread
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

client = AsyncIOMotorClient('mongodb://localhost:27017')
dbs = client.video
collection = dbs.avnum_rank


def get_rank(name, url):
    data = requests.get(url, headers=head)
    data.encoding = "utf-8"
    data = data.text
    soup = BeautifulSoup(data, 'lxml')
    a = soup.find_all("a", class_='title', target="_blank", href=True)
    avnum_list = []
    for pat in a:
        href = pat['href']
        avnum_list.append(href[href.index('av') + 2:href.rindex('/')])
    avnum_list = {str(rank): avnum for rank, avnum in zip(range(1, len(avnum_list) + 1), avnum_list)}
    avnum_list["datetime"] = datetime.datetime.today()
    avnum_list["type"] = name
    try:
        print(avnum_list)
        collection.insert_one(avnum_list)
    except Exception as e:
        print("Error", e)


class GetAvNumRank(Thread):
    def __init__(self, name, url):
        super(GetAvNumRank, self).__init__()
        self.name = name
        self.url = url

    def run(self) -> None:
        print("Starting " + self.name)
        get_rank(self.name, self.url)
        print("Exiting " + self.name)


if __name__ == '__main__':
    thread_list = []
    for name, url in url_dic.items():
        thread = GetAvNumRank(name, url)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

