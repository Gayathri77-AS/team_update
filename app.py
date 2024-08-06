from flask import Flask, render_template, request, redirect, url_for, flash
import firebase_admin
from firebase_admin import credentials, storage
import openpyxl
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

cred_json = os.environ.get('FIREBASE_ADMIN_SDK')
cred = credentials.Certificate(io.StringIO(cred_json))
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET')
})

bucket = storage.bucket()

def upload_to_firebase(file_name, blob_name):
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_name)
    print("Upload Successful")



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

