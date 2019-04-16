from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import keras

import numpy as np
import matplotlib.pyplot as plt

# Supress annoying Warning and Info messages.
import os
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def ReadWeatherData(filename):
    X = np.genfromtxt(filename, delimiter=',')
    X = X[1:,1:]    # Remove header row and remove time column.
    return X


def ReadRideData(filename):
    y = np.genfromtxt(filename, delimiter=',')
    y = y[1:,-2]    # Remove header row, keep count column only.
    return y


# Adds a column to X storing that hour's hour-of-day: [0,23]
def AddHourOfDay(X):
    new_dims = [ X.shape[0], X.shape[1]+1 ]
    X_new = np.zeros(new_dims, dtype=float)
    X_new[:,:-1] = X        # Copy X into X_new (except for new column)

    for i in range(X.shape[0]):
        X_new[i,-1] = i % 24
    
    return X_new


# Adds a column to X storing the day of the week.
def AddWeekday(X):
    new_dims = [ X.shape[0], X.shape[1]+1 ]
    X_new = np.zeros(new_dims, dtype=float)
    X_new[:,:-1] = X        # Copy X into X_new (except for new column)

    for i in range(X.shape[0]):
        X_new[i,-1] = (i+5) % 7
    
    return X_new


# Creates a basic model.
def CreateModel(num_features):
    model = Sequential()
    model.add(Dense(5, input_dim=num_features, activation='tanh'))
    model.add(Dense(5, input_dim=5, activation='elu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def PlotTestResults(y, pred):
    plt.style.use('seaborn-whitegrid')
    fig = plt.figure()
    ax = plt.axes()
    x = list(range(len(y)))
    ax.plot(x, y, label='True')
    ax.plot(x, pred, label='Predicted')
    plt.legend()
    plt.show()





if __name__ == '__main__':
    X = ReadWeatherData('hourly_weather_aug-sep_2014.csv')
    X = AddHourOfDay(X)
    X = AddWeekday(X)
    X = (X - X.mean()) / X.std()    # Normalize
    
    y = ReadRideData('citi_brooklyn_weather_fixed.csv')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, shuffle=False)

    # Create the model and train it.
    model = CreateModel(X_train.shape[1])
    print('\n\nTRAINING:')
    model.fit(X_train, y_train, epochs=2000, verbose=1, validation_data=(X_test,y_test))

    # Test the model
    print('\n\nTESTING:')
    pred = model.predict(X_test, verbose=0)
    print('MSE: ', model.evaluate(X_test, y_test, verbose=0))

    # Plot the real test data next to the predictions.
    # PlotTestResults(y_test, pred)
