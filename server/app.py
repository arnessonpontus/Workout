from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np 
import pandas as pd 
from sklearn.model_selection import train_test_split
import csv
import datetime
import matplotlib.dates
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.decomposition import PCA
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC 
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import ShuffleSplit

# Activate source env/bin/activate for ENV

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}) # Should only be enabled for front end domain

def getAmount(weekday, date, hour, month, degree, rain, sun):

    data = pd.read_csv("dataset_city_people_hour.csv") 
    data.sort_values('Date', ascending=True, inplace=True)

    data.drop_duplicates(keep = False, inplace = True)

    # Drop unessecary fields
    data = data.drop(['Facility'], axis=1)
    data = data.drop(['Activity'], axis=1)

    # Replace strings with integers
    data.replace(to_replace=["Jan", "Feb", "Mar", "Apr", "Maj", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], value=[1,2,3,4,5,6,7,8,9,10,11,12], inplace=True)
    data.replace(to_replace=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], value=[1,2,3,4,5,6,7], inplace=True)

    # Fill NaN
    data.fillna(method='ffill', inplace=True)

    # Seperate weather features into different classes
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

    numOfPeople = 10
    counter = 1

    # Seperate the number of people each hour to different classes
    for i in range(1, 80, numOfPeople):
        data.loc[(data["People"] >= i ) & (data["People"] < i+numOfPeople), "People"] = counter-1
        counter += 1
    data.loc[(data["People"] > 80 ), "People"] = counter-1
    
    # Convert to int
    data["Temp"] = data["Temp"].astype(int)
    data["Rain"] = data["Rain"].astype(int)

    # Get Data and target
    Y = data.iloc[:, 7]
    X = data.drop(["People"], axis=1)

    # Drop features to compare result
    #X = X.drop(["Date"], axis=1) # Drop Date
    #X = X.drop(["Rain"], axis=1) # Drop Rain
    #X = X.drop(["Sun"], axis=1) # Drop Sun
    #X = X.drop(["Month"], axis=1) # Drop Month
    #X = X.drop(["Day"], axis=1) # Drop Day
    #X = X.drop(["Temp"], axis=1) # Drop Temp
    
    cv2 = KFold(shuffle=True, n_splits=5)
    # Split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

    #KNN
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, Y_train)
    #print(knn.predict([[3, 28, hour, 9, 8, 0, 0]]))
    print("Knn: " + str(knn.score(X_test, Y_test)))

    # SVM
    svm_model_linear = SVC(kernel = 'rbf', C = 2, gamma='auto').fit(X_train, Y_train)
    svm_predictions = svm_model_linear.predict(X_test) 
    print("SVM: " + str(svm_model_linear.score(X_test, Y_test)))
    
    # Random forest
    rndF = RandomForestClassifier(100, random_state=0)
    rndF.fit(X_train, Y_train)
    rndfPred = rndF.predict(X_test)
    cm = confusion_matrix(Y_test, rndfPred) 
    print("Random forest: " + str(rndF.score(X_test, Y_test)))
    
    # Desision tree
    DTree = DecisionTreeClassifier(random_state=0)
    DTree.fit(X_train, Y_train)
    print("Decision trees: " + str(DTree.score(X_test, Y_test)))
   
    # Extra trees
    exT = ExtraTreesClassifier(n_estimators=100, random_state=0)
    exT.fit(X_train, Y_train)
    print("Extra trees: " + str(exT.score(X_test, Y_test)) )
    
    # Naive bayes
    NB = MultinomialNB()
    NB.fit(X_train, Y_train)
    print("Naive-bayes: " + str(NB.score(X_test, Y_test)))
    
    return (exT.predict([[weekday, date, hour, month, degree,rain,sun]])) # 0 = weekday, 1 = date, 2 = hour, 3 = month, 4 = temp, 5 = rain, 6 = sun

# sanity check route
@app.route('/', methods=['GET'])
def home():
    return jsonify('How many people are there at the gym?')

@app.route("/", methods=['POST'])
def return_number_at_gym():
    weekday = request.args.get('weekday')
    if weekday == "":
        weekday = 2
    else:
        weekday = (int)(weekday)

    date = request.args.get('dateNum')
    if date == "":
        date = 17
    else:
        date = (int)(date)

    time = request.args.get('time')
    if time == "":
        time = 16
    else:
        time = (int)(time)

    month = request.args.get('month')
    if month == "":
        month = 3
    else:
        month = (int)(month)

    degree = request.args.get('degree')
    if degree == "":
        degree = 5
    else:
        degree = (int)(degree)

    rain = request.args.get('rainNum')
    if rain == "":
        rain = 2
    else:
        rain = (int)(rain)

    sun = request.args.get('sunNum')
    if sun == "":
        sun = 0
    else:
        sun = (int)(sun)

    amountClass = getAmount(weekday, date, time, month, degree, rain, sun)[0]
    amount = ""
    if amountClass == 0:
        amount = "0 - 10"
    elif amountClass == 1:
        amount = "10 - 20"
    elif amountClass == 2:
        amount = "20 - 30"
    elif amountClass == 3:
        amount = "30 - 40"
    elif amountClass == 4:
        amount = "40 - 50"
    elif amountClass == 5:
        amount = "50 - 60"
    elif amountClass == 6:
        amount = "50 - 60"
    elif amountClass == 7:
        amount = "60 - 70"
    elif amountClass == 8:
        amount = "70 - 80"
    else:
        amount = "80+"
    
    return jsonify("There are probably " + amount + " people at the gym at this time!")
    
if __name__ == '__main__':
    app.run()

