from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
import keras

import numpy as np

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib import rc

# Supress annoying Warning and Info messages.
import os
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

DOING_YEAR = False

def ReadWeatherData(filename):
    X = np.genfromtxt(filename, delimiter=',')
    X = X[1:,1:]    # Remove header row and remove time column.
    return X


def ReadRideData(filename):
    y = np.genfromtxt(filename, delimiter=',')
    if DOING_YEAR==False:
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
        if DOING_YEAR:
            X_new[i,-1] = ((i//24) + 2) % 7
        else:
            X_new[i,-1] = ((i//24) + 4) % 7     # Monday is 0, so fri,sat,sunday are highest.
    
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
    # Font Stuff
    font_files = font_manager.findSystemFonts(
        fontpaths=os.getcwd() + '../../../poster_figures/fonts')
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)
    mpl.rcParams['font.family'] = 'Product Sans'
    # Figure aspect ratio
    fig, ax = plt.subplots(figsize=(14, 9))
    x = list(range(len(y)))
    # Line Labels
    ax.plot(x, y, label='True', color="#00c8fc", linewidth=2)
    ax.plot(x, pred, '--', label='Predicted', color="#DB4437", linewidth=2)
    # Axis value Ranges
    plt.xlabel('Hours (since start of test)')
    plt.ylabel('Rides per hour')
    # Add title with bold font and padding
    title = "Prediction of Citi Bike use from Weather"
    plt.title(title, fontweight="bold", pad=40, size=45)
    fig.canvas.set_window_title(title)
    # Position legend and make it horizontal
    leg = plt.legend(fontsize=30, ncol=2,
                     bbox_to_anchor=(0.5, 1.01), loc='center')
    leg.get_frame().set_linewidth(0.0)
    # Remove actual tick marks
    plt.tick_params(top=False, bottom=False, left=False,
                    right=False, labelleft=True, labelbottom=True)
    for axis in [ax.xaxis, ax.yaxis]:
        axis.label.set_weight("bold")
        axis.label.set_size(38)
        axis.labelpad = 15
    # Change axis label font size
    plt.tick_params(axis='both', which='major', labelsize=30)
    # Remove lines
    plt.gca().spines["top"].set_alpha(0)
    plt.gca().spines["bottom"].set_alpha(0)
    plt.gca().spines["right"].set_alpha(0)
    plt.gca().spines["left"].set_alpha(0)
    # Set layout
    fig.tight_layout()
    fig.savefig("predict_ridecount.svg", dpi=1200)
    plt.show()




def main_2mo(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, shuffle=False)

    # Create the model and train it.
    model = CreateModel(X_train.shape[1])
    print('\n\nTRAINING:')
    model.fit(X_train, y_train, epochs=5000, verbose=0, validation_data=(X_test,y_test))

    # Test the model
    print('\n\nTESTING:')
    pred = model.predict(X_test, verbose=0)
    print('MSE: ', model.evaluate(X_test, y_test, verbose=0))

    # Plot the real test data next to the predictions.
    PlotTestResults(y_test, pred)
    plt.show()


def main_year(X,y):
    l = len(y)
    i25 = int(0.25*l); i5 = int(0.5*l); i75 = int(0.75*l)
    X_train0, X_test0, y_train0, y_test0 = train_test_split(X[:i25], y[:i25], test_size=0.1, shuffle=False)
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X[i25:i5], y[i25:i5], test_size=0.1, shuffle=False)
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X[i5:i75], y[i5:i75], test_size=0.1, shuffle=False)
    X_train3, X_test3, y_train3, y_test3 = train_test_split(X[i75:], y[i75:], test_size=0.1, shuffle=False)

    X_train = np.concatenate([X_train0,X_train1,X_train2,X_train3])
    y_train = np.concatenate([y_train0,y_train1,y_train2,y_train3])
    X_test = np.concatenate([X_test0,X_test1,X_test2,X_test3])
    y_test = np.concatenate([y_test0,y_test1,y_test2,y_test3])

    # Create the model and train it.
    model = CreateModel(X_train.shape[1])
    print('\n\nTRAINING:')
    model.fit(X_train, y_train, epochs=500, verbose=1, validation_data=(X_test,y_test))

    # Test the model
    print('\n\nTESTING:')
    pred0 = model.predict(X_test0, verbose=0)
    print('MSE 0: ', model.evaluate(X_test0, y_test0, verbose=0))
    pred1 = model.predict(X_test1, verbose=0)
    print('MSE 1: ', model.evaluate(X_test1, y_test1, verbose=0))
    pred2 = model.predict(X_test2, verbose=0)
    print('MSE 2: ', model.evaluate(X_test2, y_test2, verbose=0))
    pred3 = model.predict(X_test3, verbose=0)
    print('MSE 3: ', model.evaluate(X_test3, y_test3, verbose=0))

    # Plot the real test data next to the predictions.
    PlotTestResults(y_test0, pred0)
    PlotTestResults(y_test1, pred1)
    PlotTestResults(y_test2, pred2)
    PlotTestResults(y_test3, pred3)
    plt.show()

def main_mid_seasons(X,y):
    X = np.roll(X, 31*24, axis=0)  # Start on Dec 1
    y = np.roll(y, 31*24, axis=0)

    idxs = [0, 0.1125, 0.1375, 0.25, 0.36250, 0.3875, 0.5, 0.6125, 0.6375, 0.75, 0.8625, 0.8875, 1]
    idxs = [int(i*len(y)) for i in idxs]

    X_train0 = np.concatenate( [ X[idxs[0]:idxs[1]], X[idxs[2]:idxs[3]] ])
    X_test0 = X[idxs[1]:idxs[2]]
    X_train1 = np.concatenate( [ X[idxs[3]:idxs[4]], X[idxs[5]:idxs[6]] ])
    X_test1 = X[idxs[4]:idxs[5]]
    X_train2 = np.concatenate( [ X[idxs[6]:idxs[7]], X[idxs[8]:idxs[9]] ])
    X_test2 = X[idxs[7]:idxs[8]]
    X_train3 = np.concatenate( [ X[idxs[9]:idxs[10]], X[idxs[11]:idxs[12]] ])
    X_test3 = X[idxs[10]:idxs[11]]

    y_train0 = np.concatenate( [ y[idxs[0]:idxs[1]], y[idxs[2]:idxs[3]] ])
    y_test0 = y[idxs[1]:idxs[2]]
    y_train1 = np.concatenate( [ y[idxs[3]:idxs[4]], y[idxs[5]:idxs[6]] ])
    y_test1 = y[idxs[4]:idxs[5]]
    y_train2 = np.concatenate( [ y[idxs[6]:idxs[7]], y[idxs[8]:idxs[9]] ])
    y_test2 = y[idxs[7]:idxs[8]]
    y_train3 = np.concatenate( [ y[idxs[9]:idxs[10]], y[idxs[11]:idxs[12]] ])
    y_test3 = y[idxs[10]:idxs[11]]


    # Create the model and train it.
    # model0 = CreateModel(X_train0.shape[1])
    # model0.fit(X_train0, y_train0, epochs=1000, verbose=1, validation_data=(X_test0,y_test0))
    model1 = CreateModel(X_train0.shape[1])
    model1.fit(X_train1, y_train1, epochs=1000, verbose=1, validation_data=(X_test1,y_test1))
    # model2 = CreateModel(X_train0.shape[1])
    # model2.fit(X_train2, y_train2, epochs=1000, verbose=1, validation_data=(X_test2,y_test2))
    model3 = CreateModel(X_train0.shape[1])
    model3.fit(X_train3, y_train3, epochs=1000, verbose=1, validation_data=(X_test3,y_test3))

    # Test the model
    print('\n\nTESTING:')
    # pred0 = model0.predict(X_test0, verbose=0)
    # print('MSE 0: ', model0.evaluate(X_test0, y_test0, verbose=0))
    pred1 = model1.predict(X_test1, verbose=0)
    print('MSE 1: ', model1.evaluate(X_test1, y_test1, verbose=0))
    # pred2 = model2.predict(X_test2, verbose=0)
    # print('MSE 2: ', model2.evaluate(X_test2, y_test2, verbose=0))
    pred3 = model3.predict(X_test3, verbose=0)
    print('MSE 3: ', model3.evaluate(X_test3, y_test3, verbose=0))

    # Plot the real test data next to the predictions.
    # PlotTestResults(y_test0, pred0)
    PlotTestResults(y_test1, pred1)
    # PlotTestResults(y_test2, pred2)
    PlotTestResults(y_test3, pred3)
    plt.show()




def main_seasons(X,y):
    l = len(y)
    i25 = int(0.25*l); i5 = int(0.5*l); i75 = int(0.75*l)
    X_train0, X_test0, y_train0, y_test0 = train_test_split(X[:i25], y[:i25], test_size=0.1, shuffle=False)
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X[i25:i5], y[i25:i5], test_size=0.1, shuffle=False)
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X[i5:i75], y[i5:i75], test_size=0.1, shuffle=False)
    X_train3, X_test3, y_train3, y_test3 = train_test_split(X[i75:], y[i75:], test_size=0.1, shuffle=False)

    # Create the model and train it.
    model0 = CreateModel(X_train0.shape[1])
    model0.fit(X_train0, y_train0, epochs=1000, verbose=1, validation_data=(X_test0,y_test0))
    model1 = CreateModel(X_train0.shape[1])
    model1.fit(X_train1, y_train1, epochs=1000, verbose=1, validation_data=(X_test1,y_test1))
    model2 = CreateModel(X_train0.shape[1])
    model2.fit(X_train2, y_train2, epochs=1000, verbose=1, validation_data=(X_test2,y_test2))
    model3 = CreateModel(X_train0.shape[1])
    model3.fit(X_train3, y_train3, epochs=1000, verbose=1, validation_data=(X_test3,y_test3))

    # Test the model
    print('\n\nTESTING:')
    pred0 = model0.predict(X_test0, verbose=0)
    print('MSE 0: ', model0.evaluate(X_test0, y_test0, verbose=0))
    pred1 = model1.predict(X_test1, verbose=0)
    print('MSE 1: ', model1.evaluate(X_test1, y_test1, verbose=0))
    pred2 = model2.predict(X_test2, verbose=0)
    print('MSE 2: ', model2.evaluate(X_test2, y_test2, verbose=0))
    pred3 = model3.predict(X_test3, verbose=0)
    print('MSE 3: ', model3.evaluate(X_test3, y_test3, verbose=0))

    # Plot the real test data next to the predictions.
    PlotTestResults(y_test0, pred0)
    PlotTestResults(y_test1, pred1)
    PlotTestResults(y_test2, pred2)
    PlotTestResults(y_test3, pred3)
    plt.show()




if __name__ == '__main__':
    weather_file = 'weather_2014.csv' if DOING_YEAR else 'weather_2mo.csv'
    count_file = 'bin_counts_2014.csv' if DOING_YEAR else 'bin_counts_2mo.csv'

    X = ReadWeatherData(weather_file)
    X = AddHourOfDay(X)
    X = AddWeekday(X)
    X = (X - X.mean()) / X.std()    # Normalize
    
    y = ReadRideData(count_file)


    if DOING_YEAR:
        # main_year(X,y)
        # main_seasons(X,y)
        main_mid_seasons(X,y)
    else:
        main_2mo(X,y)