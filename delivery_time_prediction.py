# -*- coding: utf-8 -*-
"""Delivery time prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ttdzLvgSytt3SUc_dVwaddxK5uKlu1VU

##PROBLEM STATEMENT:
 To find out the time taken by the delivery person using random forest regressor

###GIVEN:
 We are having the dataset downloaded from kaggle, which has columns about each of the delivery.

###METHODOLOGY: 
At the beginning we have imported required packages.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn import linear_model

"""Loading the dataset"""

df = pd.read_csv("/content/train.csv")

"""Viewing the required information from the dataset"""

df.head(18)

"""Replacing the NaN values, so that it will be easy to eliminate those rows using dropna function"""

df.replace({"NaN": np.nan}, regex=True, inplace = True)

"""Dropping null valued row and reordering the dataframe."""

df.isna().sum()

df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True) #reindexing

df["Delivery_person_Age"]=df["Delivery_person_Age"].astype(int)
df["Delivery_person_Ratings"]=df["Delivery_person_Ratings"].astype(float)
df.info()

"""Calculating the distance using delivery and restarurant's latitude and longitude"""

from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0
def distance_calculator(lat1,lon1,lat2,lon2):

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return(distance)

"""Calculating the distance and storing in the dist column"""

dist=[]
for i in range(len(df)):
    dist.append(distance_calculator(df["Restaurant_latitude"][i],df["Restaurant_longitude"][i],df["Delivery_location_latitude"][i],df["Delivery_location_longitude"][i]))

dist = pd.DataFrame(dist)
med = dist.median()
dist=np.array(dist)

"""According to our dataset, the delivery is done within the radius of 100 km. So replacing the larger distances by median of the distance."""

for i in range(len(dist)):
    if (dist[i]>100):
        dist[i]= med

"""Saving this distance in the dataframe as integer type"""

df["Distance"]=dist
df.info()

"""Since we have only numerical values. So changing them into required data type"""

for label,content in df.items():
    if not pd.api.types.is_numeric_dtype(content):
        df[label]=pd.Categorical(content).codes+1

df.info()

"""Setting target variable as time taken, and doing splitting inorder to train our model."""

x=df.drop("Time_taken(min)",axis=1)
y=df["Time_taken(min)"]

"""Using splitting method to train and test model"""

x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.33, random_state=42)

"""Importing RANDOM FOREST REGRESSOR to do parametric model."""

model=RandomForestRegressor(n_estimators= 100,
                                 min_samples_split= 4,
                                 min_samples_leaf= 1)
model.fit(x_train,y_train)

y_preds_forest=model.predict(x_valid)
r2_score(y_valid,y_preds_forest)

"""Our r2_score value is around 83%. This shows our model is a better fitting model.

Followed by, doing the same procedure for the test dataset.
"""

test_data=pd.read_csv("/content/test.csv")

"""Following the same procedure what we did for the training set"""

test_data.isna().sum()

test_data.replace({"NaN": np.nan}, regex=True, inplace = True)

mean=df["Time_taken(min)"].mean()

test_data=test_data.dropna()
test_data.reset_index(drop=True, inplace=True)

dist=[]
for i in range(len(test_data)):
  d = distance_calculator(test_data["Restaurant_latitude"][i],test_data["Restaurant_longitude"][i],test_data["Delivery_location_latitude"][i],test_data["Delivery_location_longitude"][i])
  dist.append(d)

dist=pd.DataFrame(dist)
a=dist.median()
dist=np.array(dist)
for i in range(len(dist)):
  if (dist[i]>100):
    dist[i]=a
test_data["Distance"]=dist
test_data["Distance"]=test_data["Distance"].astype(int)
for label,content in test_data.items():
  if not pd.api.types.is_numeric_dtype(content):
    test_data[label]=pd.Categorical(content).codes+1

"""Predicting the output from the test data using the fitted model"""

test_predicts=model.predict(test_data)

"""Creating new data frame and storing each order's delivery ID with the calculated time"""

test_output=pd.DataFrame()

test_output["ID"]=test_data["ID"]
test_output["Time_taken (min)"]=test_predicts

test_output