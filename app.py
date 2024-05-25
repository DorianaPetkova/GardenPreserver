from flask import Flask, render_template, request, current_app
import os
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kookie.679234',
    'database': 'GardenPreserver',
}

app = Flask(__name__)

def load_responses():
    responses = {}
    file_path = os.path.join(current_app.root_path, 'static', 'responses.txt')
    with open(file_path, 'r') as file:
        content = file.read().strip()
        blocks = content.split('\n')
        for block in blocks:
            if ':' in block:
                keyword, response = block.split(':', 1)
                responses[keyword.lower().strip()] = response.strip()
    return responses

def extract_relevant_info(text, question):
    sentences = text.split('. ')
    keywords = question.lower().split()
    relevant_sentences = []
    
    for sentence in sentences:
        for keyword in keywords:
            if keyword in sentence.lower():
                relevant_sentences.append(sentence)
                break
                
    return '. '.join(relevant_sentences) + '.' if relevant_sentences else "I'm sorry, I don't have an answer for that question."

def get_response(question, responses):
    for keyword in responses:
        if keyword in question.lower():
            return extract_relevant_info(responses[keyword], question)
    return "I'm sorry, I don't have an answer for that question."

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
            image_path = f"/pictures/{flower_id}.jpg"
            image_phase = f"/pictures/p{flower_id}.jpg"
            return render_template('result.html', show_popup=True, flower_name=flower_name, flower_description=flower_description, image_path=image_path, image_phase=image_phase)
        else:
            return render_template('result.html', show_popup=True, error_message="Flower not found.")
    return render_template('index.html')



@app.route('/questions', methods=['GET', 'POST'])
def questions():
    response = ""
    responses = load_responses()
    if request.method == 'POST':
        user_question = request.form['question']
        response = get_response(user_question, responses)
    return render_template('questions.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
