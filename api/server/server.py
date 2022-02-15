import os
import shutil
import flask
import uuid

from flask import Flask, request, current_app
from flask_cors import CORS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4000 * 1024 * 1024
app.config['ENCRYPT_FILE_UPLOAD_PATH'] = './encrypt-uploads'
app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.docx', '.doc', '.xls', '.csv', '.zip', 'mp4', '.mp3']
cors = CORS(app)


@app.route('/upload-encrypt-file', methods=['POST'])
def upload_encrypt_file():
    if not os.path.exists(app.config['ENCRYPT_FILE_UPLOAD_PATH']):
        os.makedirs(app.config['ENCRYPT_FILE_UPLOAD_PATH'])

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in current_app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS']:
            return flask.Response(status=400)

        upload_file_path = current_app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file.filename
        uploaded_file.save(upload_file_path)
        shutil.copyfile(upload_file_path, current_app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + str(uuid.uuid4()) + "-"+uploaded_file.filename)
        os.remove(upload_file_path)
        return flask.Response(status=200)

    return flask.Response(status=404)


@app.route('/upload-decrypt-file', methods=['POST'])
def upload_decrypt_file():
    return flask.Response(status=200)


if __name__ == '__main__':
    app.run( host='0.0.0.0', debug=True)

