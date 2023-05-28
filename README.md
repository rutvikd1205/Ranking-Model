# Starcraft Player Ranking Prediction
This repository contains code for predicting the ranking of Starcraft players based on various features. The goal is to build a model that can accurately predict the player's ranking in the game.

Dataset
The dataset used for this project is starcraft_player_data.csv. It contains information about Starcraft players, such as their age, hours per week, total hours played, actions per minute (APM), and various other features.

Data Preprocessing
Before building the models, some preprocessing steps were performed on the dataset:

Replacing missing values: Missing values in the columns 'HoursPerWeek', 'Age', and 'TotalHours' were replaced with appropriate values, such as the mean for numerical columns and mode for categorical columns.
Converting data types: The columns 'HoursPerWeek', 'Age', and 'TotalHours' were converted to numeric data type.
Handling class imbalance: The dataset had an imbalance in the class distribution. Random oversampling and undersampling techniques were applied to balance the classes.
Exploratory Data Analysis
Several visualizations were created to gain insights from the data:

Distribution of age: A histogram was plotted to visualize the distribution of age among the players.
Distribution of League Index: A bar plot was created to show the frequency of each League Index.
Hours per week vs APM: A scatter plot was used to explore the relationship between hours per week and APM.
APM vs League Index: A violin plot was generated to examine the distribution of APM across different player ranks.
Pairwise relationships: A pair plot was created to visualize the relationships between selected features.
Modeling
Various machine learning models were trained and evaluated for ranking prediction:

Random Forest: A Random Forest classifier was trained using resampled data to handle class imbalance.
Logistic Regression: A Logistic Regression model was fitted on scaled data to account for different feature scales.
Kernel Ridge: A Kernel Ridge model was trained to explore non-linear relationships between features.
Ensemble Methods: Different ensemble methods, such as majority voting, were employed to combine predictions from multiple models.
Results and Suggestions
The best accuracy achieved within the given time frame was approximately 43% using Random Forest with cross validation.
Suggestions for further improvement include collecting cleaner data without irregular values, addressing class imbalance by collecting more data for underrepresented classes, gathering additional relevant features, and obtaining a larger dataset for better predictions.
Feel free to explore the code and experiment with different models and techniques to further improve the prediction accuracy.

Requirements
The following libraries are required to run the code:

pandas
matplotlib
seaborn
numpy
scikit-learn
tensorflow
xgboost
imbalanced-learn

Install the required libraries using pip:
pip install -r requirements.txt

Usage

Clone the repository:
bash
git clone https://github.com/your-username/starcraft-player-ranking-prediction.git

Navigate to the project directory:
bash
cd starcraft-player-ranking-prediction

Run the Jupyter Notebook or Python script to execute the code.
Contributing
Contributions to this project are welcome. If you have any suggestions or improvements, feel free to submit a pull request or open an issue.

License
This project is licensed under the MIT License.
