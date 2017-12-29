# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 18:42:49 2017

@author: yuki.yamaguchi
"""

# -*- coding: utf-8 -*-
"""

@author: yhirayama"""

"""データの準備"""
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

#import keras.backend.tensorflow_backend
"""モデル構築"""
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM

"""データの準備"""
plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1.0 
plt.rcParams['ytick.major.width'] = 1.0 
plt.rcParams['font.size'] = 12 
plt.rcParams['axes.linewidth'] = 1.0 
plt.rcParams['font.family'] = 'Times New Roman' 

#TerraSkyStockCode
code = 3915 

x = []
y = []

file_name = "terraSky3915.csv"

data = pd.read_csv(file_name, header = 0, encoding = 'cp932')
date =list(pd.to_datetime(data.iloc[:,0] , format = '%Y-%m-%d'))
x += date[::-1]
stock_price = list(data.iloc[:,1])
y += stock_price[::-1]

z = pd.DataFrame(y)
sma75 = pd.DataFrame.rolling(z, window = 75, center = False).mean()
sma25 = pd.DataFrame.rolling(z, window = 25, center = False).mean()

plt.plot(x, y, color = "blue", linewidth = 1, linestyle = "-")
plt.plot(x, sma25, color = "g", linewidth = 1, linestyle = "-", label = "MA25")
plt.plot(x, sma75, color = "r", linewidth = 1, linestyle = "-", label = "MA75")

plt.title("TerraSky ("+str(code)+")", fontsize = 16, fontname = 'Times New Roman')
plt.xlabel("Year-Month", fontsize = 14, fontname = 'Times New Roman')
plt.ylabel("Stock price", fontsize = 14, fontname = 'Times New Roman')

plt.legend(loc="best")

plt.show()

"""データ加工"""
length_of_sequences = 50
test_size = 0.2

def load_data(file_name):
    lines = [line[:-1] for line in open(file_name, 'r', encoding='utf-8')]
    #ヘッダーは読み込まない
    split = [line.split(',') for line in lines if not (line.startswith('Date') or len(line) == 0)]
    # 日付と終値を返す
    return [line[0] for line in split], [float(line[1]) for line in split]

def create_train_data(close_values, n_pre_days):
    train_x = []
    train_y = []
    for i in np.arange(0, len(close_values) - n_pre_days):
       train_x.append(close_values.iloc[i:i + n_pre_days].as_matrix())
       train_y.append(close_values.iloc[i+n_pre_days].as_matrix())
    return np.array(train_x), np.array(train_y)

def train_test_split(close_values, test_size, n_pre_days):
    n = round(len(close_values) * (1 - test_size))
    n = int(n)
    print('★★★' + str(n))
    close_values = DataFrame(close_values)
    train_x , train_y = create_train_data(close_values.iloc[0:n], n_pre_days)
    x_test, y_test = create_train_data(close_values.iloc[n:], n_pre_days)
    return (train_x , train_y), (x_test, y_test)

date, close = load_data(file_name)
close = DataFrame(close) / DataFrame(close).mean()
(train_x , train_y), (test_x, test_y) = train_test_split(close, test_size, length_of_sequences)

"""モデル構築"""
hidden_neurons = 50
in_out_neurons = 1
epochs = 2
batch_size = 10

def create_model():
    #SequentialModelの設計
    model = Sequential()
    #LSTM
    model.add(LSTM(hidden_neurons, batch_input_shape=(None, length_of_sequences, in_out_neurons)))
    model.add(Dense(in_out_neurons))
    #恒等関数
    model.add(Activation("linear"))
    return model

model = create_model()
model.compile(loss="mean_squared_error", optimizer="SGD", metrics=['accuracy'])
history = model.fit(train_x, train_y, batch_size = batch_size, epochs = epochs, verbose=1)
#score = model.evaluate(test_x, test_y, batch_size = batch_size, verbose = 1)
predicted = model.predict(test_x)

predicted_data =  pd.DataFrame(predicted)
predicted_data.columns = ["predict"]
predicted_data["input"] = test_y
predicted_data.plot(figsize=(10, 5))