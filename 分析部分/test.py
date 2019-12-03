from pymongo import MongoClient
from pymongo.collection import Collection
from process import Processor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU
from RNN_model import RNN
import matplotlib.pyplot as plt


client = MongoClient('mongodb://localhost:27017')
dbs = client['videodata']
p = Processor(dbs['53766576'])
# ["分享数", "投币数", "收藏数", "弹幕数", "播放量", "点赞数", "评论数"]
# p.show_data("分享数")
incre = p.get_increment()
dataset = p.run_pca()[:, 0]
gru_model = RNN(dataset=dataset, rnn_type="GRU", input_shape=(1, 1))
gru_model.normalize()
x_train, y_train, x_validation, y_validation, train_size, validation_size = gru_model.create_train_data(train_prop=0.67)
# gru_model.fit(x_train, y_train, epochs=100)
gru_model.load_model("my_model.h5")
predict_train = gru_model.predict(x_train)
predict_validation = gru_model.predict(x_validation)
predict_train, y_train = gru_model.anti_normalize(predict_train, y_train)
predict_validation, y_validation = gru_model.anti_normalize(predict_validation, y_validation)
gru_model.evaluate(predict_train, y_train)
gru_model.evaluate(predict_validation, y_validation)
gru_model.plot(predict_train, predict_validation)
# gru_model.save("my_model.h5")

