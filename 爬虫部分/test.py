from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests


client = MongoClient('mongodb://localhost:27017')
data_dbs = client.videodata
url_head = "https://www.bilibili.com/video/av"
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}


if __name__ == '__main__':
    req = requests.get(url_head+"53819837", headers=head)
    status = req.status_code
    if status in [200, 201]:
        req.encoding = "utf-8"
        soup = BeautifulSoup(req.text, 'lxml')
        for tag in soup.find_all("li", "tag"):
            print(tag.text)

    else:
        print("Error Code:{}".format(req.status_code))
