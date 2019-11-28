from process import Processor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU


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

    def __init__(self, dataset, input_shape, look_back=1, rnn_type="GRU", units=3, loss="mean_squared_error", optimizer="adam"):
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

    def normalize(self):
        scaler = MinMaxScaler()
        self.dataset = self.dataset.reshape(-1, 1)
        self.dataset = scaler.fit_transform(self.dataset)

    def create_train_data(self, train_prop=0.67):
        assert isinstance(train_prop, float)
        assert train_prop > 0.5 or train_prop < 0.9

        train_size = int(len(self.dataset) * train_prop)
        validation_size = len(self.dataset) - train_size
        train, validation = self.dataset[0: train_size, :], self.dataset[train_size: len(self.dataset), :]
        x_train, y_train = _create_train_data(train, look_back=self.look_back)
        x_validation, y_validation = _create_train_data(validation, look_back=self.look_back)
        return x_train, y_train, x_validation, y_validation

