import mysql.connector
import openai
import os
from flask import Flask, render_template, request

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kookie.679234',
    'database': 'GardenPreserver',
}



app = Flask(__name__)

openai.api_key = os.getenv('sk-proj-C0lr1wjPCYsnv7DKoaePT3BlbkFJhDTyYEweGX03pf7REIJ0')
def get_chatbot_response(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"You are an expert in flowers. Answer the following question: {question}",
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

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
            image_phase=f"pictures/p{flower_id}.jpg"  # Assuming the image name is same as flower ID
            return render_template('result.html', show_popup=True, flower_name=flower_name, flower_description=flower_description, image_path=image_path, image_phase=image_phase)
        else:
            return render_template('result.html', show_popup=True, error_message="Flower not found.")
    return render_template('index.html')

@app.route('/questions')
def questions():
    # Render the questions.html template dynamically
    return render_template('questions.html')


if __name__ == '__main__':
    app.run(debug=True)
