from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU
from pymongo.collection import Collection

item_dic = {
    "分享数": 0,
    "投币数": 1,
    "收藏数": 2,
    "弹幕数": 3,
    "播放量": 4,
    "点赞数": 5,
    "评论数": 6
}


class Processor(object):

    def __init__(self, collection: Collection):
        if not isinstance(collection, Collection):
            raise TypeError("输入对象应该为Mongodb集合")
        self._collection = collection
        if self._is_empty():
            raise FileExistsError("The Collection is Empty")
        self._array = np.transpose(self._to_numpy())
        self._increment_array = None
        self._PCA_array = None

    def _is_empty(self):
        return True if self._collection.find_one() is None else False

    def _to_numpy(self):
        data = list(self._collection.find({}, {'_id': 0, 'aid': 0, 'datetime': 0}).sort("datetime"))
        return np.asarray([list(record.values()) for record in data])

    def get_array(self):
        # ["分享数", "投币数", "收藏数", "弹幕数", "播放量", "点赞数", "评论数"]
        return self._array

    def get_score(self):
        tmp_array = self._array.T
        score = np.array([])
        for item in tmp_array:
            sc = item[item_dic["播放量"]] * (2000 + item[item_dic["播放量"]]) // (2 * item[item_dic["播放量"]])
            sc += 50 * item[item_dic["评论数"]] * (item[item_dic["收藏数"]] * 20 + item[item_dic["投币数"]] * 10) // (
                        item[item_dic["播放量"]] + item[item_dic["投币数"]] * 10 + item[item_dic["评论数"]] * 50)
            sc += 10 * item[item_dic["投币数"]] * (item[item_dic["收藏数"]] * 20 + item[item_dic["投币数"]] * 10) // (
                        item[item_dic["播放量"]] + item[item_dic["投币数"]] * 10 + item[item_dic["评论数"]] * 50)
            sc += item[item_dic["收藏数"]] * 20
            score = np.append(score, sc)
        return score

    def get_increment(self):
        self._increment_array = np.zeros(shape=(np.size(self._array, 0), np.size(self._array, 1) - 1))
        for i in range(np.size(self._array, 0)):
            self._increment_array[i] = self._array[i][1:] - self._array[i][:-1]
        return self._increment_array

    def run_pca(self):
        if self._increment_array is None:
            raise BaseException("_increment_array为空，请先调用get_increment方法")
        pca = PCA(n_components=3)
        self._PCA_array = pca.fit_transform(self._increment_array.T)
        return self._PCA_array

    def run_kernel_pca(self):
        pass
