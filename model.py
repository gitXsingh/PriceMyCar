# Importing the libraries
import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# Importing the dataset
dataset = pd.read_csv('new_auto_data.csv')

# Select features and target
features = ['fuel-type', 'num-of-cylinders', 'engine-size', 'fuel-system', 'horsepower', 'city-mpg', 'highway-mpg']
X = dataset[features]
y = dataset['price']

# Encode categorical features
le_fuel_type = LabelEncoder()
le_num_cyl = LabelEncoder()
le_fuel_sys = LabelEncoder()
X['fuel-type'] = le_fuel_type.fit_transform(X['fuel-type'])
X['num-of-cylinders'] = le_num_cyl.fit_transform(X['num-of-cylinders'])
X['fuel-system'] = le_fuel_sys.fit_transform(X['fuel-system'])

# Fitting Multiple Linear Regression to the Training set
regressor = LinearRegression()
regressor.fit(X, y)

# Save encoders and model to disk
pickle.dump({'model': regressor, 'le_fuel_type': le_fuel_type, 'le_num_cyl': le_num_cyl, 'le_fuel_sys': le_fuel_sys}, open('model.pkl','wb'))

# Loading model to compare the results
