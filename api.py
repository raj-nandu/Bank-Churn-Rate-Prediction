# Importing the libraries
import numpy as np
import pandas as pd
import flask
import io
app = flask.Flask(__name__)
# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

# Encoding categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

#for country
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])

#for gender
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])


onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Make the ANN
# importing keras library

import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

#initializing the ANN
classifier = Sequential()

# adding the input layer and first hidden layer with dropout
classifier.add(Dense(output_dim=64,input_dim=12,kernel_initializer = 'uniform',activation = 'relu'))
classifier.add(Dropout(p = 0.1))
classifier.add(Dense(output_dim=128,input_dim=64,kernel_initializer = 'uniform',activation = 'relu'))
classifier.add(Dropout(p = 0.2))
classifier.add(Dense(output_dim=256,input_dim=128,kernel_initializer = 'uniform',activation = 'relu'))
classifier.add(Dropout(p = 0.3))
classifier.add(Dense(output_dim=64,input_dim=256, kernel_initializer = 'uniform',activation = 'relu'))
classifier.add(Dropout(p = 0.4))
import random

#adding output layer
classifier.add(Dense(output_dim=1, input_dim=64,kernel_initializer = 'uniform',activation = 'sigmoid'))

#compiling the ANN
classifier.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics = ['accuracy'])
classifier.load_weights('model.h5')


# #
# def predict():
#     print("Enter country - 'spain','france' or 'germany'")
#     country = input()
#     print("Enter credit score")
#     score = float(input())
#     print("Enter the gender: 0 for female and 1 for male")
#     g = float(input())
#     print("Enter the age")
#     age = float(input())
#     print("Enter the tenure")
#     tenure = float(input())
#     print("Enter the balance")
#     balance = float(input())
#     print("Enter the number of products used by the customer")
#     numprods = float(input())
#     print("Does the user has a credit card? 1 for yes and 0 for no")
#     hascrd = float(input())
#     print("Is the customer an active Member?  1 for yes and 0 for no")
#     isactive = float(input())
#     print("Enter the estimated salary")
#     salary = float(input())
#     if country == 'france':
#         c1 = 1
#         c2 = 0
#         c3 = 0
#     elif country == 'spain':
#         c1 = 0
#         c2 = 1
#         c3 = 0
#     else:
#         c1 = 0
#         c2 = 0
#         c3 = 1
#
#     pred = classifier.predict(
#         sc.transform(np.array([[c1, c2, c3, score, g, age, tenure, balance, numprods, hascrd, isactive, salary]])))
#     if pred > 0.5:
#         print("The customer is likely to leave the bank")
#     else:
#         print("The customer is not likely to leave the bank")



@app.route("/")
def home():
    return flask.render_template("client.html")


# predict()
@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        print("Inside this")
        country = flask.request.form['country']
        score = float(flask.request.form['score'])
        g = float(flask.request.form['g'])
        age = float(flask.request.form['age'])
        tenure = float(flask.request.form['tenure'])
        balance = float(flask.request.form['balance'])
        numprods = float(flask.request.form['numprods'])
        hascrd = float(flask.request.form['hascrd'])
        isactive = float(flask.request.form['isactive'])
        salary = float(flask.request.form['salary'])
        if country == 'france':
            c1 = 1
            c2 = 0
            c3 = 0
        elif country == 'spain':
            c1 = 0
            c2 = 1
            c3 = 0
        else:
            c1 = 0
            c2 = 0
            c3 = 1

        pred = classifier.predict(
            sc.transform(np.array([[c1, c2, c3, score, g, age, tenure, balance, numprods, hascrd, isactive, salary]])))
        print(str(pred))
        pred = random.random()
        if pred > 0.5:
            print("The customer is likely to leave the bank")
            data['result'] = 'yes'
        else:
            print("The customer is not likely to leave the bank")
            data['result'] = "no"
        data['success'] = True
    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
           "please wait until server has fully started"))

    app.run()
    # app.run(host="172.31.45.56")
