import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

import os
import shutil
import flask
import uuid
import redis

from flask import Flask, request, current_app, jsonify
from flask_cors import CORS, cross_origin

from producer.producer import add_to_work_queue

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4000 * 1024 * 1024
app.config['ENCRYPT_FILE_UPLOAD_PATH'] = './encrypt-uploads'
app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.docx', '.doc', '.xls',
                                                '.csv', '.zip', '.mp4', '.mp3', 'tif']

cors = CORS(app)


@app.route('/upload-encrypt-file', methods=['POST', 'OPTIONS'])
@cross_origin()
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
        uploaded_file_unique_name = str(uuid.uuid4()) + "-" + str(uploaded_file.filename)
        shutil.copyfile(upload_file_path,
                        current_app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name)
        os.remove(upload_file_path)

        redis_instance = redis.Redis(host='redis', port=6379)
        encryption_tracking_id = str(uuid.uuid4())
        redis_instance.set(encryption_tracking_id, current_app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name)
        add_to_work_queue(encryption_tracking_id)
        response = {"encryptionTrackingId": encryption_tracking_id}
        return jsonify(response), 200

    return flask.Response(status=404)


@app.route('/upload-decrypt-file', methods=['POST'])
def upload_decrypt_file():
    return flask.Response(status=200)


if __name__ == '__main__':
    from waitress import serve

    serve(app, host='0.0.0.0', port=8080)
