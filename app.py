from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('updates.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS updates
                          (id INTEGER PRIMARY KEY,
                          timestamp TEXT,
                          name TEXT,
                          message TEXT)''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with sqlite3.connect('updates.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO updates (timestamp, name, message) VALUES (?, ?, ?)",
                       (timestamp, name, message))
        conn.commit()
    
    return "Update submitted!"

if __name__ == '__main__':
    init_db()  # This line initializes the database and creates the table if it doesn't exist
    app.run(debug=True)

