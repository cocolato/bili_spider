import pandas as pd
import datetime
from pymongo import MongoClient
import os


client = MongoClient('mongodb://localhost:27017')
data_dbs = client.videodata
keys = ['aid', 'share', 'coin', 'favorite', 'danmaku', 'view', 'like', 'reply', 'datetime']


def str2datetime(str_date):
    return datetime.datetime.strptime("2019."+str_date, '%Y.%m.%d %H:%M:%S')


def transf(av_num):
    data = pd.read_csv(str(av_num)+".csv", header=None)
    data[10] = data[10].map(str2datetime)
    for r in data.values:
        r = list(r)
        r = [av_num] + r[1:6] + r[7:9] + [r[-1]]
        try:
            data_dbs[str(av_num)].insert_one(dict(zip(keys, r)))
        except Exception as e:
            print(e)


def get_task_list():
    csv_list = [file for file in os.listdir(os.getcwd()) if ".csv" in file]
    return [int(av_num.split(".")[0]) for av_num in csv_list]


if __name__ == '__main__':
    av_num_list = get_task_list()
    for av_num in av_num_list:
        transf(av_num)
        print(av_num, "done")
