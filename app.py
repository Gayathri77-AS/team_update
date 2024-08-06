from flask import Flask, render_template, request, redirect, url_for
import openpyxl
import os
from datetime import datetime

app = Flask(__name__)

def write_to_excel(name, message):
    file_path = 'updates.xlsx'
    
    if not os.path.isfile(file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Updates'
        sheet.append(['Timestamp', 'Name', 'Message'])
    else:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append([timestamp, name, message])
    workbook.save(file_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    message = request.form.get('message')
    
    if name and message:
        write_to_excel(name, message)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

