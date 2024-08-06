from flask import Flask, render_template, request, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, storage
import openpyxl
import os
import io
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

cred_json = os.environ.get('FIREBASE_ADMIN_SDK')
cred_dict = json.loads(cred_json)  # Convert JSON string to dictionary
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET')
})

bucket = storage.bucket()

def upload_to_firebase(file_name, blob_name):
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_name)
    print("Upload Successful")



def write_to_excel(date, name, message):
    file_path = 'updates.xlsx'
    print(f"Attempting to write to {file_path}")

    if not os.path.isfile(file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Updates'
        sheet.append(['Date', 'Name', 'Message'])
        print("Created new workbook and sheet.")
    else:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        print("Loaded existing workbook.")

    sheet.append([date, name, message])
    workbook.save(file_path)
    print(f"Saved data to {file_path}.")


@app.route('/')
def index():
    return render_template('index.html')
'''
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

'''
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    message = request.form.get('message')
    date = request.form.get('date')

    if name and date and message:
        try:
            # Write to Excel file
            write_to_excel(date, name, message)

            # Upload to Firebase Storage
            upload_to_firebase('updates.xlsx', 'updates.xlsx')

            # Flash success message
            flash('Update submitted and uploaded successfully!', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'error')
    else:
        flash('Name and message are required!', 'warning')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

