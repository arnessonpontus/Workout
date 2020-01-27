from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import csv
import datetime
import matplotlib.dates
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

#source env/bin/activate for ENV

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}) # Should only be enabled for frot end domain

def getAmount(hour):
    numPeople = []
    datesRegisterd = []

    data = pd.read_csv("dataset_city_people_hour.csv") 
    data.sort_values('Date', ascending=True, inplace=True)

    data.drop_duplicates(keep = False, inplace = True)

    data = data.drop(['Facility'], axis=1)
    data = data.drop(['Activity'], axis=1)

    # Replace strings with integers
    data.replace(to_replace=["Jan", "Feb", "Mar", "Apr", "Maj", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], value=[1,2,3,4,5,6,7,8,9,10,11,12], inplace=True)
    data.replace(to_replace=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], value=[1,2,3,4,5,6,7], inplace=True)
    #data.replace({'-': ''}, inplace=True, regex=True)
    #data.replace({':': ''}, inplace=True, regex=True)

    # Fill NaN
    data.fillna(method='ffill', inplace=True)

    data.loc[(data["Sun"] > 0) & (data["Sun"] < 1200), "Sun"] = 1 # Slight sun
    data.loc[(data["Sun"] >= 1200) & (data["Sun"] < 2400), "Sun"] = 2 # Moderate sun
    data.loc[(data["Sun"] >= 2400) & (data["Sun"] < 3600), "Sun"] = 3 # Heavy sun
    data.loc[(data["Sun"] == 3600), "Sun"] = 4 # Very heavy sun

    data.loc[(data["Rain"] > 0.0) & (data["Rain"] < 0.5), "Rain"] = 1 # Slight rain 
    data.loc[(data["Rain"] >= 0.5) & (data["Rain"] < 4.0), "Rain"] = 2 # Moderate rain
    data.loc[(data["Rain"] >= 4.0) & (data["Rain"] < 8.0), "Rain"] = 3 # Heavy rain
    data.loc[(data["Rain"] > 8), "Rain"] = 4 # Very heavy rain

    data.loc[(data["Temp"] < -10.0 ), "Temp"] = 0
    data.loc[(data["Temp"] >= -10.0 ) & (data["Temp"] < -5.0), "Temp"] = 1
    data.loc[(data["Temp"] >= -5.0 ) & (data["Temp"] < 0.0), "Temp"] = 2
    data.loc[(data["Temp"] >= 0.0 ) & (data["Temp"] < 5.0), "Temp"] = 3
    data.loc[(data["Temp"] >= 5.0 ) & (data["Temp"] < 10.0), "Temp"] = 4
    data.loc[(data["Temp"] >= 10.0 ) & (data["Temp"] < 15.0), "Temp"] = 5
    data.loc[(data["Temp"] >= 15.0 ) & (data["Temp"] < 20.0), "Temp"] = 6
    data.loc[(data["Temp"] >= 20.0 ) & (data["Temp"] < 25.0), "Temp"] = 7
    data.loc[(data["Temp"] >= 25.0 ) & (data["Temp"] < 30.0), "Temp"] = 8
    data.loc[(data["Temp"] >= 30.0 ), "Temp"] = 9

    increment = 5
    counter = 1

    for i in range(1, 80, increment):
        data.loc[(data["People"] >= i ) & (data["People"] < i+increment), "People"] = counter-1
        counter += 1
    data.loc[(data["People"] > 80 ), "People"] = counter-1


    data["Temp"] = data["Temp"].astype(int)
    data["Rain"] = data["Rain"].astype(int)

    #print(data)

    # Get Data and target
    Y = data.iloc[:, 7]
    X = data.iloc[:, :7]


    #print(X)
    dates = data.iloc[:, 1] # Date part of the dataset
    meanPerDay = []
    maxPerDay = []
    minPerDay = []
    days = []
    dayCounter = 0

    '''
    # Create days instead of minutes
    for i in range(1, len(Y)+1):
        if i != len(Y)+1:
            while dates[i] == dates[i+1]:
                days[dayCounter] += Y[i]
    '''

    # Split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

    # plot
    #plt.plot(dates, Y)
    #plt.show()

    knn = KNeighborsClassifier(n_neighbors=7) 
    knn.fit(X_train, Y_train) 

    #print((X_test.iloc[370, :]).values.reshape(1, -1))

    print(knn.predict([[3, 28, hour, 9, 8, 0, 0]])) # 0 = weekday, 1 = day, 2 = hour, 3 = month, 4 = temp, 5 = rain, 6 = sun
    #print(knn.score(X_test, Y_test)) 

    '''
    rndF = RandomForestClassifier(100)
    rndF.fit(X_train, Y_train)
    #print(rndF.predict(X_test)) 
    print(rndF.score(X_test, Y_test)) 
    '''

    return (knn.predict([[3, 28, hour, 9, 8, 0, 0]]))

# sanity check route
@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify('How many people is it at the gym?')

@app.route('/<int:time>', methods=['POST'])
def return_number_at_gym(time):
    #print(getAmount(time))
    return jsonify(str(getAmount(time)[0]))
    
if __name__ == '__main__':
    app.run()

