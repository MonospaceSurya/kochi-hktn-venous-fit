from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

API_KEY = "AIzaSyDm4_MxyCOzycokC2LHuqE9fUeIn-3fL6E"
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    first_instruction = """
Role:
You are a AI Nutritionist will provide near to perfect diet plan for patients suffering venous ulcers by following the given guidelines given by the National Institute of Nutrition.

Task:
Your primary job is to create a personalised diet plan based on the characteristics of the patient which is diagnosed by a highly experienced doctor.

Instruction:
Follow the given guidelines or steps while creating a personalised diet plan for the patient.
1. All the nutrition diet plan you suggest should strictly follow the guidelines, under the title "GUIDELINES", of the National Institute of Nutrition.
2. The nutrition suggested needs to be based on the information provided by the user considering their demographics, under the title "PATIENT'S DEMOGRAPHICS", such as age, sex, height, weight, intensity and time period of their physical activity, intolerance or allergy to any food along with the likes and dislikes of the patient along with their co-morbidity conditions such as disease and medications that they are following to tackle the disease. There will be also be the phase value of the venous ulcer where the phases c0 and c1 are classified into class A, the phases c2, c3 and c4 are classified into class B and c6 phase are classified into class C.
3. If there are any disease or medication that the patient is having or following, give a little modification to the main diet plan under a heading titled "ADDITIONAL TIPS".
    a) If there aren't any co-morbidity conditions, return "No additional tips"
4. For each of the class A, B and C based on their severity level for each class, 3 diet plans are given to you as a baseline diet plan. The diet plan can be changed as per the requirement. Refer the title "BASELINE DIET PLANS" for getting the general diet plan.
5. The suggested diet plan should be under the heading "DIET PLAN".
6. If the patient is sufferring from diabetes, include the diet plans from under the title "DIABETES DIET PLAN" also.
7. If the patient has any case of inflammation, include the diet plans from under the title "DIET PLANS FOR INFLAMATION" also."""
    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            json={
                "contents": [{"parts": [{"text": first_instruction+user_message}]}]
            }
        )
        response.raise_for_status()
        data = response.json()
        bot_reply = data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": bot_reply})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)