from flask import Flask, render_template, request, redirect, url_for, flash
import openpyxl
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

def write_to_excel(name, message):
    file_path = 'updates.xlsx'
    print(f"Attempting to write to {file_path}")

    if not os.path.isfile(file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Updates'
        sheet.append(['Timestamp', 'Name', 'Message'])
        print("Created new workbook and sheet.")
    else:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        print("Loaded existing workbook.")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sheet.append([timestamp, name, message])
    workbook.save(file_path)
    print(f"Saved data to {file_path}.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    message = request.form.get('message')

    if name and message:
        try:
            write_to_excel(name, message)
            flash('Update submitted successfully!', 'success')
        except Exception as e:
            flash(f'Error saving to Excel: {e}', 'error')
    else:
        flash('Name and message are required!', 'warning')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

