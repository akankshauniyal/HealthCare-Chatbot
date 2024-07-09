import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the training dataset
train_data_path = 'Training.csv'
train_data = pd.read_csv(train_data_path)
symptom_columns = train_data.columns[:-1]
disease_column = 'prognosis'

# Fill NaN values with an empty string
train_data = train_data.fillna('')

# Separate features and target
X_train = train_data[symptom_columns]
y_train = train_data[disease_column]

# Encode the target variable
le = preprocessing.LabelEncoder()
y_train_encoded = le.fit_transform(y_train)

# Train the Random Forest classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train_encoded)

# Save the trained model
joblib.dump(clf, 'random_forest_model.pkl')
