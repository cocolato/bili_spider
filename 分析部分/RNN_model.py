from process import Processor
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from pylab import mpl
import matplotlib.pyplot as plt
import numpy as np
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU


mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False


def _create_train_data(dataset, look_back):
    data_x, data_y = [], []
    for i in range(len(dataset) - look_back - 1):
        x = dataset[i: i + look_back, 0]
        data_x.append(x)
        y = dataset[i + look_back, 0]
        data_y.append(y)
        # print('X: %s, Y: %s' % (x, y))
    return np.array(data_x), np.array(data_y)


class RNN(object):

    def __init__(self, dataset, input_shape, look_back=1, rnn_type="GRU", units=3, loss="mean_squared_error",
                 optimizer="adam"):
        self.type = rnn_type
        self.look_back = look_back
        self.input_shape = input_shape
        self.units = units
        self.loss = loss
        self.optimizer = optimizer
        self.model = Sequential()
        if self.type == "GRU":
            self.model.add(GRU(units=self.units, input_shape=self.input_shape))
        elif self.type == "LSTM":
            self.model.add(LSTM(units=self.units, input_shape=self.input_shape))
        else:
            raise BaseException("RNN类型错误，应该为LSTM或GRU")
        self.model.add(Dense(units=1))
        self.model.compile(loss=self.loss, optimizer=self.optimizer)
        self.dataset = dataset
        self.scaler = MinMaxScaler()

    def normalize(self):
        self.dataset = self.dataset.reshape(-1, 1)
        self.dataset = self.scaler.fit_transform(self.dataset)

    def create_train_data(self, train_prop=0.67):
        assert isinstance(train_prop, float)
        assert train_prop > 0.5 or train_prop < 0.9

        train_size = int(len(self.dataset) * train_prop)
        validation_size = len(self.dataset) - train_size
        train, validation = self.dataset[0: train_size, :], self.dataset[train_size: len(self.dataset), :]
        x_train, y_train = _create_train_data(train, look_back=self.look_back)
        x_validation, y_validation = _create_train_data(validation, look_back=self.look_back)
        x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
        x_validation = np.reshape(x_validation, (x_validation.shape[0], 1, x_validation.shape[1]))
        return x_train, y_train, x_validation, y_validation, train_size, validation_size

    def fit(self, x_train, y_train, epochs=100, batch_size=1, verbose=2):
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)

    def predict(self, x):
        return self.model.predict(x)

    def anti_normalize(self, predict, y):
        predict = self.scaler.inverse_transform(predict)
        y = self.scaler.inverse_transform([y])
        return predict, y

    def evaluate(self, predict, y):
        train_score = math.sqrt(mean_squared_error(y[0], predict[:, 0]))
        print('Score: %.2f RMSE' % train_score)

    def plot(self, predict_train, predict_validation):
        predict_train_plot = np.empty_like(self.dataset)
        predict_train_plot[:, :] = np.nan
        predict_train_plot[self.look_back:len(predict_train) + self.look_back, :] = predict_train
        predict_validation_plot = np.empty_like(self.dataset)
        predict_validation_plot[:, :] = np.nan
        predict_validation_plot[len(predict_train) + self.look_back * 2 + 1:len(self.dataset) - 1, :] \
            = predict_validation
        dataset = self.scaler.inverse_transform(self.dataset)
        plt.figure(figsize=(24, 10), dpi=80)
        plt.xlabel("采样点")
        plt.ylabel("热度指数")
        plt.plot(dataset, color='blue', label="原始数据")
        plt.plot(predict_train_plot, color='green', label="训练集拟合数据")
        plt.plot(predict_validation_plot, color='red', label="测试集拟合数据")
        plt.legend("upper right")
        plt.show()


