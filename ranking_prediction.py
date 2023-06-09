# -*- coding: utf-8 -*-
"""Ranking_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VkHpS_TG1U9NrOQ2IKbWjXufPNo6QtPt

# Importing Libraries
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import accuracy_score
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

"""# Loading the Data"""

data = pd.read_csv('/content/starcraft_player_data.csv')

"""# DATA PRE-PROCESSING"""

data.head().  # displaying first few rows of the data

data.info(). # checking null values and datatype of columns

data.describe(). #checking the min, max, std and other statistics of columns

data['LeagueIndex'].value_counts().  # checking the frquency of unique values in a column

# replacing '?' with NA
data1 = data
data1['HoursPerWeek'] = data['HoursPerWeek'].replace('?', pd.NA)
data1['Age'] = data['Age'].replace('?', pd.NA)
data1['TotalHours'] = data['TotalHours'].replace('?', pd.NA)

# converting these columns into numeric
data1['HoursPerWeek'] = pd.to_numeric(data1['HoursPerWeek'])
data1['Age'] = pd.to_numeric(data1['Age'])
data1['TotalHours'] = pd.to_numeric(data1['TotalHours'])

# calculating the mean
mean_hours_per_week = data1['HoursPerWeek'].mean()
mean_total_hours = data1['TotalHours'].mean()

# replacing '?' with the mean and mode (depending on the distribution of the values)
data1['HoursPerWeek'] = data1['HoursPerWeek'].fillna(mean_hours_per_week)
data1['Age'] = data1['Age'].fillna(data1['Age'].mode()[0])
data1['TotalHours'] = data1['TotalHours'].fillna(mean_total_hours)

# converting datatype to int
data1['HoursPerWeek'] = data1['HoursPerWeek'].astype(int)
data1['Age'] = data1['Age'].astype(int)
data1['TotalHours'] = data1['TotalHours'].astype(int)

#data1['HoursPerWeek'].value_counts()
data1.dtypes

"""## PLOTS FOR EDA"""

# checking the distribution of age
plt.hist(data1['Age'], bins=20, orientation='horizontal')
plt.xlabel('Frequency')
plt.ylabel('Age')
plt.title('Distribution of Age')
plt.show()

# checking the distribution of League Index
plt.figure(figsize=(12, 6))
data1['LeagueIndex'].value_counts().sort_index().plot(kind='bar')
plt.xlabel('League Index')
plt.ylabel('Count')
plt.title('Distribution of League Index')
plt.show()

# Hours per week vs APM 
plt.figure(figsize=(8, 6))
plt.scatter(data1['HoursPerWeek'], data1['APM'])
plt.xlabel('Hours Per Week')
plt.ylabel('APM')
plt.title('Hours Per Week vs. APM')
plt.show()

data1['TotalHours']

# APM vs League Index
plt.figure(figsize=(10, 6))
sns.violinplot(x='LeagueIndex', y='APM', data=data1)
plt.xlabel('League Index')
plt.ylabel('APM')
plt.title('Distribution of APM across Player Ranks')
plt.show()

# plotting pairwise relations
columns = ['Age', 'HoursPerWeek', 'TotalHours', 'APM', 'SelectByHotkeys']
sns.pairplot(data=data1, vars=columns, hue='LeagueIndex')
plt.title('Pairwise Relationships between Selected Features')
plt.show()

# plotting heatmap to explain the correlation between two variables
plt.figure(figsize=(10, 8))
correlation_matrix = data1[['Age', 'HoursPerWeek', 'TotalHours', 'APM', 'LeagueIndex', 'ComplexUnitsMade','MinimapAttacks','ActionsInPAC','ComplexAbilitiesUsed']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# Plotting covariance plot using covariance matrix
cov_matrix = data1.cov()

threshold = 0.2
filtered_cov_matrix = cov_matrix.abs().where(np.triu(np.ones(cov_matrix.shape), k=1).astype(bool))
filtered_cov_matrix = filtered_cov_matrix.mask(filtered_cov_matrix < threshold)

sorted_cov_matrix = filtered_cov_matrix.unstack().sort_values(ascending=False).dropna()

plt.figure(figsize=(10, 8))
sns.heatmap(sorted_cov_matrix.to_frame(), annot=True, cmap='coolwarm')
plt.title('Sorted Covariance Heatmap')
plt.show()

"""# MODELING"""

# Splitting the data into features and target variable
X = data1.drop(['LeagueIndex'], axis=1)  
y = data1['LeagueIndex']

X.shape

# splitting into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# code to handle the imbalance between values of columns
oversampler = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = oversampler.fit_resample(X_train, y_train)

undersampler = RandomUnderSampler(random_state=42)
X_train_resampled, y_train_resampled = undersampler.fit_resample(X_train_resampled, y_train_resampled)

# Fitting Random Forest with resampled data
rf_model = RandomForestClassifier()
rf_model.fit(X_train_resampled, y_train_resampled)

# testing the model accuracy on test data
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Scaling the data to ensure that all features have a similar scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

X_train.shape

# Fitting a Logistic Regression model
model1 = LogisticRegression()
model1.fit(X_train_scaled, y_train)

# Checking the accuracy on scaled data
accuracy = model1.score(X_test_scaled, y_test)
print("Accuracy:", accuracy)

# Random Forest on scaled data
rf_model1 = RandomForestClassifier()

rf_model1.fit(X_train_scaled, y_train)

# Testing the accuracy on test data
y_pred = rf_model1.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

"""# FITTING DIFFERENT CLASSIFIERS"""

# Defining various other models
logistic_regression = LogisticRegression()
decision_tree = DecisionTreeClassifier()
random_forest = RandomForestClassifier()
gradient_boosting = GradientBoostingClassifier()

# Fitting the above models on X, y using cross validation
classifiers = [
    ('Logistic Regression', logistic_regression),
    ('Decision Tree', decision_tree),
    ('Random Forest', random_forest),
    ('Gradient Boosting', gradient_boosting)
]

for name, classifier in classifiers:
    scores = cross_val_score(classifier, X, y, cv=16)  # Perform 16-fold cross-validation
    accuracy = scores.mean()
    print(f'{name}: Accuracy = {accuracy:.4f}')

# Fitting Kernel Ridge model
model = KernelRidge(alpha=0.1, kernel='rbf')
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

y_pred_labels = [1 if val >= 0.5 else 0 for val in y_pred]

accuracy = accuracy_score(y_test, y_pred_labels)
print("Accuracy:", accuracy)

# Fitting RF with different hyperparameters
model_1 = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model_2 = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model_3 = RandomForestClassifier(n_estimators=300, max_depth=15, random_state=42)

# Training each model on the training data
model_1.fit(X_train_scaled, y_train)
model_2.fit(X_train_scaled, y_train)
model_3.fit(X_train_scaled, y_train)

# Making predictions using each model
pred_1 = model_1.predict(X_test_scaled)
pred_2 = model_2.predict(X_test_scaled)
pred_3 = model_3.predict(X_test_scaled)

# Combining predictions using voting (majority voting)
ensemble_pred = pd.DataFrame({'pred_1': pred_1, 'pred_2': pred_2, 'pred_3': pred_3})
ensemble_pred['final_pred'] = ensemble_pred.mode(axis=1)[0]

# Evaluating the accuracy of the ensemble predictions
accuracy = accuracy_score(y_test, ensemble_pred['final_pred'])
print("Ensemble Accuracy:", accuracy)

"""# FINDINGS & SUGGESTIONS 

1.   The data columns like 'HoursPerWeek', 'TotalHours' and 'Age' contained irregular values.
2.   There was an imbalance in the data. For example: There were around 800 samples for Index 4 whereas some of the Indices only had around 30 samples.
3.   More hours per week didn't necessarily mean more APM.
4.   As the age increased, the actions per minute and Hours per week decreased.
5.   I tried various models by setting different hyperparameters each time and even scaling the input. The best accuracy I could achieve within the 5 hours timeframe was around 43% by Random Forest using cross validation.

# HYPOTHETICAL
Some of the suggestions would be:

1.   Get cleaner data, i.e., data shouldn't contain irregular values.
2.   Collect more data for Indices with lesser samples (There should not be class imbalance).
3.   Collect additional relevant features that may provide more information about the players and their performance.
4.   Collect a lot of data so that the predictions can be better.
"""