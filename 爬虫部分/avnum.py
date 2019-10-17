import os
import requests
from bs4 import BeautifulSoup
import time
from pymongo import MongoClient
import datetime


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
         (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}
url_dic = {
    'day_all': 'https://www.bilibili.com/ranking/all/0/0/1',
    'day_origin': 'https://www.bilibili.com/ranking/origin/0/0/1',
    'day_cinema': 'https://www.bilibili.com/ranking/cinema/177/0/1',
    'day_rookie': 'https://www.bilibili.com/ranking/rookie/0/0/1',
}


def get_av_number(url):
    data = requests.get(url, headers=head)
    data.encoding = 'utf-8'
    data = data.text
    soup = BeautifulSoup(data, 'lxml')
    # print(soup)
    a = soup.find_all("a", class_='title', target="_blank", href=True)
    av_number = []
    for pat in a:
        href = pat['href']
        # print(href[href.index('av') + 2:href.rindex('/')])
        av_number.append(href[href.index('av') + 2:href.rindex('/')])
    return av_number


def num_download():
    client = MongoClient()
    dbs = client.video
    avnum_collection = dbs.avnum
    for key in url_dic:
        url_list = get_av_number(url_dic[key])
        avnum_collection.insert_one({key+'_'+str(datetime.date.today()): url_list})
        # save_txt(url_list, key)


if __name__ == '__main__':
    num_download()
