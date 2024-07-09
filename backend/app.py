from flask import Flask, request, jsonify
import numpy as np
from sklearn import preprocessing
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Loading of the model and other csv
model = joblib.load('random_forest_model.pkl')
severity_data = pd.read_csv('Symptom-severity.csv')
description_data = pd.read_csv('symptom_Description.csv')
precaution_data = pd.read_csv('symptom_precaution.csv')

symptom_columns = pd.read_csv('Training.csv').columns[:-1]
le = preprocessing.LabelEncoder()
le.fit(pd.read_csv('Training.csv')['prognosis'])

user_data = {}  # Dictionary to store user session data

def greet_user():
    greetings = ["hi", "hello", "hey", "greetings", "sup", "what's up"]
    responses = ["hi", "hello", "hey", "hi there", "hello! how can I help?", "hello!"]
    return random.choice(responses)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_input = data.get('input', '').strip().lower()
    user_id = data.get('user_id') 

    if user_id not in user_data:
        user_data[user_id] = {'step': 1}

    step = user_data[user_id]['step']

    if user_input in ["hi", "hello", "hey", "greetings", "sup", "what's up"]:
        response = {
            'message': "Please enter your symptoms separated by commas. We'll try our best to help you out "
        }
        user_data[user_id]['step'] = 1
    elif user_input in ["thanks", "thank you", "thanks a lot", "thank you so much", "ok thank you","thank you very much", "thanking you", "a big thanks to you"]:
        response = {
            'message': "Thank you for your time! We insist you to verify your symptoms with a doctor for a clear diagnosis.\n\nHowever, you can view these websites for assistance:\n\nTeladoc: https://www.teladochealth.com/\nAmwell: https://patients.amwell.com/\nDoctor on Demand: https://doctorondemand.com/how-to-contact-us/\nLiveHealth Online: https://liveBotnline.com/\nK Health: https://khealth.com/"
        }
        user_data[user_id]['step'] = 1
    elif user_input == "bye":
        response = {
            'message': "Bye! Take care."
        }
        user_data[user_id]['step'] = 1
    else:
        if step == 1:
            symptoms = user_input.split(',')
            symptoms = [s.strip().lower() for s in symptoms]
            user_data[user_id]['symptoms'] = symptoms
            user_data[user_id]['step'] = 2
            response = {
                'message': "Please enter the total number of days you've been experiencing these symptoms."
            }
        elif step == 2:
            try:
                days = int(user_input.strip())
            except ValueError:
                response = {
                    'message': "Please enter a valid number for the total number of days."
                }
                return jsonify(response)
            
            symptoms = user_data[user_id]['symptoms']

            input_vector = np.zeros(len(symptom_columns))
            matched_symptoms = 0

            for symptom in symptoms:
                if symptom in symptom_columns:
                    index = symptom_columns.get_loc(symptom)
                    severity = severity_data[severity_data['Symptom'] == symptom]['weight'].values[0]
                    input_vector[index] = severity * (days / 2)
                    matched_symptoms += 1

            if days > 5:
                response = {
                    'message': "You have been experiencing some symptoms for more than 5 days. It is advised to consult a doctor."
                }
                user_data[user_id]['step'] = 1
            elif matched_symptoms < 2:
                response = {
                    'message': f"With these symptoms, I can't accurately determine your disease. You may or may not be suffering from some ailment; however, I would advise you to consult a doctor for a more accurate diagnosis."
                }
                user_data[user_id]['step'] = 1
            else:
                input_vector = input_vector.reshape(1, -1)
                prediction = model.predict(input_vector)
                disease = le.inverse_transform(prediction)[0]

                description = description_data.loc[description_data['Disease'] == disease, 'Description'].values[0]
                precautions = precaution_data.loc[precaution_data['Disease'] == disease].values[0][1:]
                precautions = [prec for prec in precautions if pd.notna(prec)]

                response = {
                    'message': f"From our analysis you may be suffering with {disease}.\n\nDescription: {description}.\n\nPrecautions: {', '.join(precautions)}.\n\nThere is nothing to worry about, you can take the above precautions to settle down your symptoms. However you should cross check with a doctor for more accuracy.\n\n Would you like to try again? If yes please enter your new symptoms or type 'bye' to end the conversation if not."
                }
                user_data[user_id]['step'] = 1

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
