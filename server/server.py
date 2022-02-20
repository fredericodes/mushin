import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

import shutil
import flask
import uuid
import redis
import http


from flask import Flask, request, current_app, jsonify, send_file
from flask_cors import CORS, cross_origin
from celery_async import make_celery
from pathlib import Path
from encryptor.aes import encrypt_file


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4000 * 1024 * 1024
app.config['ENCRYPT_FILE_UPLOAD_PATH'] = '/app/server/encrypt-uploads'
app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.docx', '.doc', '.xls',
                                                '.csv', '.zip', '.mp4', '.mp3', 'tif']
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

cors = CORS(app)

celery = make_celery(app)


@celery.task(name='server.celery_async.encrypt_upload_file')
def encrypt_upload_file(path):
    encrypt_file(path)


@app.route('/encryption/upload', methods=['POST', 'OPTIONS'])
@cross_origin()
def upload_file_for_encryption():
    Path(app.config['ENCRYPT_FILE_UPLOAD_PATH']).mkdir(parents=True, exist_ok=True)

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in current_app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS']:
            return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

        upload_file_path = app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file.filename
        uploaded_file.save(upload_file_path)
        uploaded_file_unique_name = str(uuid.uuid4()) + "-" + str(uploaded_file.filename)
        shutil.copyfile(upload_file_path,
                        app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name)
        os.remove(upload_file_path)

        task = encrypt_upload_file.delay(app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name)

        redis_instance = redis.Redis(host='redis', port=6379)
        redis_instance.set(task.id, app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name)

        response = {"encryptionTrackingId": str(task.id)}
        return jsonify(response), http.HTTPStatus.OK

    return flask.Response(status=http.HTTPStatus.NOT_FOUND)


@app.route('/encrypted', methods=['GET'])
@cross_origin()
def get_encrypted_file():
    tracking_id = request.args.get('trackingId')
    if tracking_id == "":
        return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

    redis_instance = redis.Redis(host='redis', port=6379)
    file_to_encrypt_path = redis_instance.get(tracking_id)
    path = app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + str(file_to_encrypt_path) + ".encrypted"
    return send_file(path, as_attachment=True)


@app.route('/decryption/upload', methods=['POST', 'OPTIONS'])
@cross_origin()
def upload_file_for_decryption():
    # TODO
    return flask.Response(status=http.HTTPStatus.OK)


if __name__ == '__main__':
    from waitress import serve

    serve(app, host='0.0.0.0', port=8080)
