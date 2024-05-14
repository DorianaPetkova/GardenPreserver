import mysql.connector
from flask import Flask, render_template, request


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kookie.679234',
    'database': 'GardenPreserver',
}

app = Flask(__name__)


def get_flower_info(name):
    
    mydb = mysql.connector.connect(**db_config)
    cursor = mydb.cursor()
   
    query = "SELECT name, description FROM flowers WHERE name = %s"
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
            return render_template('result.html', flower_name=flower_info[0], flower_description=flower_info[1])
        else:
            return render_template('result.html', error_message="Flower not found.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
