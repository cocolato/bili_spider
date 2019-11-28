from pymongo import MongoClient
from pymongo.collection import Collection
from process import Processor
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, GRU
from RNN_model import RNN


def build_model():
    model = Sequential()
    model.add(GRU(units=4, input_shape=(1, 1)))
    model.add(Dense(units=1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


seed = 7
batch_size = 1
epochs = 10
filename = 'international-airline-passengers.csv'
footer = 3
look_back = 1


def create_dataset(dataset):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        x = dataset[i: i + look_back, 0]
        dataX.append(x)
        y = dataset[i + look_back, 0]
        dataY.append(y)
        # print('X: %s, Y: %s' % (x, y))
    return np.array(dataX), np.array(dataY)


client = MongoClient('mongodb://localhost:27017')
dbs = client['videodata']
p = Processor(dbs['53766576'])
score = p.get_score()
array = p.get_array()
incre = p.get_increment()
dataset = p.run_pca()[:, 0]
gru_model = RNN(dataset=dataset, input_shape=(1, 1))
gru_model.normalize()
print(gru_model.create_train_data(train_prop=0.67))

# print(dataset)
# dataset = dataset.reshape(-1, 1)
# X_train, y_train = create_dataset(dataset)
# X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
#
#
# model = build_model()
#
# model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2)
