import mysql.connector
import openai
import os
import time
from flask import Flask, render_template, request

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kookie.679234',
    'database': 'GardenPreserver',
}

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY') or 'sk-proj-kHlgRcOA6Inqf8fSl58iT3BlbkFJAMgcCXru9iSFwvqDnzkG'


def get_chatbot_response(question):
    max_retries = 5
    retry_delay = 1  # Start with a 1 second delay

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in flowers."},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message['content'].strip()
        except openai.error.RateLimitError:
            if attempt < max_retries - 1:
                print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                return "Rate limit exceeded. Please try again later."
        except openai.error.OpenAIError as e:
            return f"An error occurred: {str(e)}"


def get_flower_info(name):
    mydb = mysql.connector.connect(**db_config)
    cursor = mydb.cursor()
    query = "SELECT id, name, description FROM flowers WHERE name = %s"
    cursor.execute(query, (name,))
    flower = cursor.fetchone()
    cursor.close()
    mydb.close()
    return flower

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        flower_name = request.form['flower_name']
        flower_info = get_flower_info(flower_name)
        if flower_info:
            flower_id, flower_name, flower_description = flower_info
            image_path = f"pictures/{flower_id}.jpg"
            image_phase = f"pictures/p{flower_id}.jpg"
            return render_template('result.html', show_popup=True, flower_name=flower_name, flower_description=flower_description, image_path=image_path, image_phase=image_phase)
        else:
            return render_template('result.html', show_popup=True, error_message="Flower not found.")
    return render_template('index.html')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    response = ""
    if request.method == 'POST':
        user_question = request.form['question']
        response = get_chatbot_response(user_question)
    return render_template('questions.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
