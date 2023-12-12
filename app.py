from flask import Flask, render_template, request, session
from openai import OpenAI
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI
import os
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session
url = "https://api.apilayer.com/text_to_emotion"
client = OpenAI(api_key='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')
headers= {
    "apikey": "4ylRLhjXs7UPYtWJMNUDxoBmRSyMTT5V"
  }

def textToEmotions(text):
  if isinstance(text, str) and len(text)>10:
    payload = text.encode("utf-8")
    response = requests.request("POST", url, headers=headers, data = payload)
    status_code = response.status_code
    result = response.text

    print(result)
    result = json.loads(result)  # Convert JSON string to dictionary
    values_array = np.array(list(result.values())) #Convert dict values into a numpy array
    print(values_array)
    return(values_array)
  else:
     return(np.array([0,0,0,0,0]))

def get_emotion_score(prompt):
    final_role = "You are an expert in human emotion. Using the content of the message, return a very specific single emotion to summarize the message, followed by a colon, then exactly 5 numbers: each one a number from 0-10 grading, in order, the amount of Happiness, Anger, Surprise, Sadness, and Fear in the message. An example response would be 'Humiliated:2,5,7,5,5'"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": final_role},
            {"role": "user", "content": prompt}
        ]
    )

    completion_message = completion.choices[0].message
    total_string = completion_message.content

    try:
        parts = total_string.split(':')
        word_part = parts[0]
        emotions_string = parts[1]
        number_list = emotions_string.split(',')
        number_list = [int(num) for num in number_list]
        emotions_array = np.array(number_list)
    except Exception:
        emotions_array = textToEmotions(prompt)
    return(word_part, emotions_array)

def ask_chat(prompt):
    role = session.get('role', None)

    if role is None:
        # If role is not set, ask for it and store it in the session
        role = request.form.get('role', 'default_role')
        session['role'] = role
      

    final_role = f"You are a licensed therapist, with years of experience helping clients with their mental health. Use all your skill as a therapist, but remember that today your client wants you to take on these ideas: {role}. Take on this role in your conversation. Throughout this conversation, remember to include some emotionally probing questions, some 'nods' that encourage your client to keep talking, some validations, which make them feel like their feelings are valid, and some simple summaries to make them feel heard, as well as anything else that would be helpful. Up to this point, your conversation has been {session['conversation_string']}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": final_role},
            {"role": "user", "content": prompt}
        ]
    )

    emotion_word, emotion_values = get_emotion_score(prompt)

    completion_message = completion.choices[0].message
    
    return completion_message.content, final_role, emotion_word, emotion_values

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    emotion_word = "Default"
    emotion_values=[1,1,1,1,1]

    if request.method == 'POST':
        prompt = request.form['prompt']
        session['conversation_string'] += ("USER:  "+prompt)
        answer, final_role, emotion_word, emotion_values = ask_chat(prompt)
        session['conversation_string'] += ("THERAPIST:  "+answer)
    
    if answer:
        return render_template('indexTEST.html', answer=("ANSWER"+answer+"    HISTORY"+session['conversation_string']+ "    ROLE" + final_role + "EMOTIONS" + str(emotion_values)+emotion_word),emotion_word=emotion_word, emotion_values=emotion_values)
    else:
        session['conversation_string'] = ''
        return render_template('indexTEST.html', answer = answer, emotion_word=emotion_word, emotion_values=emotion_values)
if __name__ == '__main__':
    app.run(debug=True, port=8081)
