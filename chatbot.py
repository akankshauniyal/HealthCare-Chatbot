import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
import warnings
import random

warnings.filterwarnings("ignore")

# Load the training and testing datasets
train_data_path = 'Training.csv'
test_data_path = 'Testing.csv'
severity_data_path = 'Symptom-severity.csv'
description_data_path = 'symptom_Description.csv'
precaution_data_path = 'symptom_precaution.csv'

train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)
severity_data = pd.read_csv(severity_data_path)
description_data = pd.read_csv(description_data_path)
precaution_data = pd.read_csv(precaution_data_path)

# Assuming the last column in both datasets is 'prognosis' and the rest are symptoms
disease_column = 'prognosis'
symptom_columns = train_data.columns[:-1]

# Fill NaN values with an empty string
train_data = train_data.fillna('')
test_data = test_data.fillna('')

# Separate features and target
X_train = train_data[symptom_columns]
y_train = train_data[disease_column]
X_test = test_data[symptom_columns]
y_test = test_data[disease_column]

# Encode the target variable
le = preprocessing.LabelEncoder()
y_train_encoded = le.fit_transform(y_train)
y_test_encoded = le.transform(y_test)

# Train the Random Forest classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train_encoded)

# Evaluate the model
accuracy = clf.score(X_test, y_test_encoded)
print(f"Model Accuracy: {accuracy:.2f}")

def greet_user():
    greetings = ["hi", "hello", "hey", "greetings", "sup", "what's up"]
    responses = ["hi", "hello", "hey", "hi there", "hello! how can I help?", "hello!"]
    return random.choice(responses)

def get_user_symptoms():
    symptoms = []
    days = []
    print("Healtho: Please enter your symptoms one by one. Type 'done' when you are finished.")
    while True:
        symptom = input("You: ").strip().lower()
        if symptom == 'done':
            break
        day_count = int(input(f"Healtho: How many days have you been experiencing {symptom}? ").strip())
        symptoms.append(symptom)
        days.append(day_count)
    return symptoms, days

def predict_disease(symptoms, days):
    input_vector = np.zeros(len(symptom_columns))
    matched_symptoms = 0
    for symptom, day in zip(symptoms, days):
        if symptom in symptom_columns:
            matched_symptoms += 1
            index = symptom_columns.get_loc(symptom)
            severity = severity_data[severity_data['Symptom'] == symptom]['weight'].values[0]
            input_vector[index] = severity * (day / 2)  # Adjusting the severity based on the number of days
    input_vector = input_vector.reshape(1, -1)
    prediction = clf.predict(input_vector)
    disease = le.inverse_transform(prediction)
    return disease[0], matched_symptoms

def get_disease_info(disease):
    description = description_data.loc[description_data['Disease'] == disease, 'Description'].values[0]
    precautions = precaution_data.loc[precaution_data['Disease'] == disease].values[0][1:]
    
    # Filter out NaN values from precautions
    precautions = [precaution for precaution in precautions if pd.notna(precaution)]
    
    return description, precautions


def chatbot():
    print("Healtho: My name is Healtho. I will assist you with your health queries. Type 'bye' to exit.")
    print("Healtho: " + greet_user())

    while True:
        user_input = input("You: ").strip().lower()

        if user_input == 'bye':
            print("Healtho: Bye! Take care.")
            break
        else:
            while True:
                symptoms, days = get_user_symptoms()

                if not symptoms:  # User entered 'done' immediately or no symptoms
                    print("Healtho: Please try again.")
                    continue

                if len(symptoms) < 2:  # Insufficient symptoms
                    print("Healtho: Insufficient symptoms provided. Please provide more symptoms for an accurate diagnosis or end conversation with 'done'.")
                    continue_input = input("Healtho: Do you want to try again with different symptoms? (yes/no): ").strip().lower()
                    if continue_input == 'no':
                        print("Healtho: Thank you! Take care.")
                        return
                    elif continue_input == 'yes':
                        break
                    else:
                        print("Healtho: Invalid response. Please type 'yes' or 'no'.")

                # Check if any symptom has been experienced for more than 5 days
                if any(day > 5 for day in days):
                    print("Healtho: You have been experiencing some symptoms for more than 5 days. It is advised to consult a doctor.")

                predicted_disease, matched_symptoms = predict_disease(symptoms, days)

                if matched_symptoms < 2:
                    print(f"Healtho: With these symptoms, I can't accurately determine your disease. You may likely be suffering from {predicted_disease}; however, it is advised to consult a doctor for a more accurate diagnosis.")
                else:
                    print(f"Healtho: Based on the symptoms you provided, you may have {predicted_disease}.")
                    description, precautions = get_disease_info(predicted_disease)
                    print(f"Healtho: Description: {description}")
                    print("Healtho: Precautions:")
                    for precaution in precautions:
                        print(f"- {precaution}")

                continue_input = input("Healtho: Do you want to try again with different symptoms? (yes/no): ").strip().lower()
                if continue_input == 'no':
                    print("Healtho: Thank you! Take care.")
                    return
                elif continue_input == 'yes':
                    break
                else:
                    print("Healtho: Invalid response. Please type 'yes' or 'no'.")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
