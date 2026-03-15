import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
from flask import Flask, request, jsonify, render_template
import requests
import pickle
import numpy as np


app = Flask(__name__, static_folder='static', template_folder='templates')

ckd_model_path = os.path.join(os.path.dirname(__file__), 'models', 'ckd_model.pkl')
with open(ckd_model_path, 'rb') as f:
    loaded_data  = pickle.load(f)
    if isinstance(loaded_data, dict):
        model = loaded_data.get('model', loaded_data.get('classifier'))
    else:
        model = loaded_data

@app.route('/ckd_analysis', methods=['GET', 'POST'])      
def ckd_analysis():
    # GET request to render the form
    if request.method == 'GET':
        return render_template('ckd_analysis.html')

    # POST request to perform the analysis
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Map frontend names to model names
            input_df = pd.DataFrame([{
                'Sex': data.get('sex'),
                'eGFRBaseline': float(data.get('egfr', 0)),
                'AgeBaseline': float(data.get('age', 0)),
                'CreatinineBaseline': float(data.get('creatinine', 0)),
                'dBPBaseline': float(data.get('dBP', 0)),
                'sBPBaseline': float(data.get('sBP', 0)),
                'CholesterolBaseline': float(data.get('cholesterol', 0)),
                'BMIBaseline': float(data.get('BMIBaseline', 0)),
                'HistoryCHD': data.get('chd'),
                'HistoryDiabetes': data.get('diabetes')
            }])

            input_encoded = pd.get_dummies(input_df)
            
            for col in model.feature_names_in_:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            
            input_final = input_encoded[model.feature_names_in_]
            print("Predicting")
            probability = model.predict_proba(input_final)[0][1]
            risk_status = "High Risk" if probability >= 0.4 else "Low Risk"
            print(f"Raw Output: {probability}, Risk Status: {risk_status}")
            return jsonify({
                'probability': round(probability * 100, 2),
                'status': risk_status,
                'recommendation': "Please consult a specialist." if risk_status == "High Risk" else "Continue regular monitoring."
            })

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Prediction failed'}), 500
        

# Hugging Face Inference API
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# Hugging Face Inference API
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"


headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

chat_history = []

def query_model(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False,
            # Stop parameters to avoid long outputs
            "stop": ["Patient:", "Doctor:", "[/INST]"]
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    generated = response.json()
    return generated[0]["generated_text"]

def generate_chat(user_input):
    global chat_history
    chat_history.append(f"Patient: {user_input}")
    chat_history = chat_history[-6:]  # Keep last 3 interactions

    # Format prompt using instruction style
    prompt = (
        "[INST] You are a helpful and medically accurate assistant specialized in Chronic Kidney Disease (CKD). "
        "Respond only with medical guidance based on CKD context. \n\n" 
        "Keep the response short, informative but concise. Don't answer more than what is asked. \n\n"
        + "\n".join(chat_history)
        + "\nDoctor: [/INST]"
    )
    response = query_model(prompt)
    cleaned = response.strip().split("Doctor:")[-1].strip()
    chat_history.append(f"Doctor: {cleaned}")
    return cleaned

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message")
        reply = generate_chat(user_input)
        return jsonify({"reply": reply})
    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Something went wrong."}), 500

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/mri_visualisation')
def mri_visualisation():
    return render_template('mri_visualisation.html')

if __name__ == '__main__':
    app.run(debug=True)
