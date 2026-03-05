from dotenv import load_dotenv
import os
load_dotenv()
from flask import Flask, request, jsonify, render_template
import requests
import pickle
import numpy as np


app = Flask(__name__, static_folder='static', template_folder='templates')

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

@app.route('/prediction', methods=['GET', 'POST'])      
def prediction():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)  # Debugging line

            # Extract features
            age = data.get('age', 0)
            bmi = data.get('BMIBaseline', 0)
            sex = 1 if data.get('sex') == 'male' else 0
            diabetes = 1 if data.get('diabetes') else 0
            chd = 1 if data.get('chd') else 0
            cholesterol = data.get('cholesterol', 0)
            creatinine = data.get('creatinine', 0)
            egfr = data.get('egfr', 0)
            sbp = data.get('sBP', 0)
            dbp = data.get('dBP', 0)

            features = np.array([[age, bmi, sex, diabetes, chd, cholesterol, creatinine, egfr, sbp, dbp]])
            probability = model.predict_proba(features)[0][1]
            return jsonify({'probability': round(probability * 100, 2)})
        except Exception as e:
            print("Error:", e)  # Log the error
            return jsonify({'error': str(e)}), 500

    return render_template('prediction.html')

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

if __name__ == '__main__':
    app.run(debug=True)
