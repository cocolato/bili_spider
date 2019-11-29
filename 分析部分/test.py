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
p = Processor(dbs['53893728'])
incre = p.get_increment()
dataset = p.run_pca()[:, 0]
gru_model = RNN(dataset=dataset, rnn_type="GRU", input_shape=(1, 1))
gru_model.normalize()
x_train, y_train, x_validation, y_validation, train_size, validation_size = gru_model.create_train_data(train_prop=0.67)
gru_model.fit(x_train, y_train, epochs=3)
predict_train = gru_model.predict(x_train)
predict_validation = gru_model.predict(x_validation)
predict_train, y_train = gru_model.anti_normalize(predict_train, y_train)
predict_validation, y_validation = gru_model.anti_normalize(predict_validation, y_validation)
gru_model.evaluate(predict_train, y_train)
gru_model.evaluate(predict_validation, y_validation)
gru_model.plot(predict_train, predict_validation)




# print(dataset)
# dataset = dataset.reshape(-1, 1)
# X_train, y_train = create_dataset(dataset)
# X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
#
#
# model = build_model()
#
# model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=2)
