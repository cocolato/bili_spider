from pymongo import MongoClient
from pymongo.collection import Collection
from process import Processor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM


def build_model():
    model = Sequential()
    model.add(LSTM(units=4, input_shape=(1, 1)))
    model.add(Dense(units=1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


client = MongoClient('mongodb://localhost:27017')
dbs = client['videodata']
p = Processor(dbs['53766576'])
score = p.get_score()
array = p.get_array()
incre = p.get_increment()
scaler = MinMaxScaler()
dataset = p.run_pca()[:, 1]
dataset = dataset.reshape(-1, 1)
print(dataset)
train_X = dataset
train_Y = score[1:]
model = build_model()
model.fit(train_X, train_Y, epochs=100, batch_size=1)
