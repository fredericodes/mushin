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
from util.aes import encrypt_file, decrypt_file
from util.file_validation import is_valid_file, allowed_file_upload_limit, \
                                                allowed_encryption_file_upload_extensions, \
                                                allowed_decryption_file_upload_extensions


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = allowed_file_upload_limit
app.config['ENCRYPT_FILE_UPLOAD_PATH'] = os.environ['ENCRYPT_FILE_UPLOAD_PATH']
app.config['DECRYPT_FILE_UPLOAD_PATH'] = os.environ['DECRYPT_FILE_UPLOAD_PATH']
app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS'] = allowed_encryption_file_upload_extensions
app.config['DECRYPT_FILE_UPLOAD_EXTENSIONS'] = allowed_decryption_file_upload_extensions
app.config['CELERY_BROKER_URL'] = os.environ['CELERY_BROKER_URL']
app.config['CELERY_RESULT_BACKEND'] = os.environ['CELERY_RESULT_BACKEND']

cors = CORS(app)

celery = make_celery(app)


@celery.task(name='server.celery_async.encrypt_upload_file')
def encrypt_upload_file(args):
    encrypt_file(args)


@celery.task(name='server.celery_async.decrypt_upload_file')
def decrypt_upload_file(args):
    decrypt_file(args)


def check_if_storage_avail():
    _, _, free = shutil.disk_usage("/")
    hard_disk_limit = 8589934592  # 8 GB in bytes
    if int(str(free)) < hard_disk_limit:
        return flask.Response(status=http.HTTPStatus.INSUFFICIENT_STORAGE)


@app.route('/encryption/upload', methods=['POST', 'OPTIONS'])
@cross_origin()
def upload_file_for_encryption():
    check_if_storage_avail()
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

        file_path = app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name
        if is_valid_file(file_path, file_ext) is not True:
            return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

        key_bytes = os.urandom(32)  # Generate a key for encryption
        key = key_bytes.hex()
        args = (file_path, key)
        task = encrypt_upload_file.delay(args)

        redis_instance = redis.Redis(host='redis', port=6379)
        redis_instance.set(str(task.id), app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name)
        redis_instance.set(app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name, str(key))

        response = {
            "encryptionTrackingId": str(task.id)
        }
        return jsonify(response), http.HTTPStatus.OK

    return flask.Response(status=http.HTTPStatus.NOT_FOUND)


@app.route('/encryption/status', methods=['GET'])
@cross_origin()
def get_encryption_status():
    tracking_id = request.args.get('trackingId')
    if tracking_id == "":
        return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

    redis_instance = redis.Redis(host='redis', port=6379)
    file_path = redis_instance.get(str(tracking_id))
    if file_path is None:
        return flask.Response(status=http.HTTPStatus.NOT_FOUND)

    encryption_key = redis_instance.get(file_path.decode("utf-8"))
    if encryption_key is None:
        return flask.Response(status=http.HTTPStatus.NOT_FOUND)

    result = celery.AsyncResult(id=tracking_id)
    status = result.state

    response = {
        "encryptionTrackingId": str(tracking_id),
        "status": str(status),
        "encryptionKey": str(encryption_key.decode("utf-8")),
        "fileName": file_path.decode("utf-8").replace(app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/", "")
    }
    return jsonify(response), http.HTTPStatus.OK


@app.route('/encrypted', methods=['GET'])
@cross_origin()
def get_encrypted_file():
    tracking_id = request.args.get('trackingId')
    if tracking_id == "":
        return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

    redis_instance = redis.Redis(host='redis', port=6379)
    file_to_encrypt_path = redis_instance.get(tracking_id)
    path = str(file_to_encrypt_path.decode("utf-8")) + ".encrypted"
    return send_file(path, as_attachment=True)


@app.route('/decryption/upload', methods=['POST', 'OPTIONS'])
@cross_origin()
def upload_file_for_decryption():
    check_if_storage_avail()
    Path(app.config['DECRYPT_FILE_UPLOAD_PATH']).mkdir(parents=True, exist_ok=True)

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in current_app.config['DECRYPT_FILE_UPLOAD_EXTENSIONS']:
            return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

        upload_file_path = app.config['DECRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file.filename
        uploaded_file.save(upload_file_path)

        response = {
            "fileName": uploaded_file.filename
        }
        return jsonify(response), http.HTTPStatus.OK

    return flask.Response(status=http.HTTPStatus.NOT_FOUND)


@app.route('/decryption/upload', methods=['PUT'])
def decryption_file():
    Path(app.config['DECRYPT_FILE_UPLOAD_PATH']).mkdir(parents=True, exist_ok=True)

    uploaded_file_name = request.args.get('fileName')
    if uploaded_file_name == "":
        return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

    decryption_key = request.args.get('privateSecretKey')
    if decryption_key == "":
        return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

    file_path = app.config['DECRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_name
    args = (file_path, decryption_key)
    task = decrypt_upload_file.delay(args)

    redis_instance = redis.Redis(host='redis', port=6379)
    redis_instance.set(str(task.id), app.config['DECRYPT_FILE_UPLOAD_PATH'] + "/" +
                       uploaded_file_name.replace(".encrypted", ""))
    redis_instance.set(app.config['DECRYPT_FILE_UPLOAD_PATH'] + "/" +
                       uploaded_file_name.replace(".encrypted", ""), str(decryption_key))

    response = {
        "decryptionTrackingId": str(task.id)
    }
    return jsonify(response), http.HTTPStatus.OK


@app.route('/decryption/status', methods=['GET'])
@cross_origin()
def get_decryption_status():
    tracking_id = request.args.get('trackingId')
    if tracking_id == "":
        return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

    redis_instance = redis.Redis(host='redis', port=6379)
    file_path = redis_instance.get(str(tracking_id))
    if file_path is None:
        return flask.Response(status=http.HTTPStatus.NOT_FOUND)

    decryption_key = redis_instance.get(file_path.decode("utf-8"))
    if decryption_key is None:
        return flask.Response(status=http.HTTPStatus.NOT_FOUND)

    result = celery.AsyncResult(id=tracking_id)
    status = result.state

    response = {
        "decryptionTrackingId": str(tracking_id),
        "status": str(status),
        "decryptionKey": str(decryption_key.decode("utf-8")),
        "fileName": str(file_path.decode("utf-8")).replace(app.config['DECRYPT_FILE_UPLOAD_PATH'] + "/", "")
    }
    return jsonify(response), http.HTTPStatus.OK


@app.route('/decrypted', methods=['GET'])
@cross_origin()
def get_decrypted_file():
    tracking_id = request.args.get('trackingId')
    if tracking_id == "":
        return flask.Response(status=http.HTTPStatus.BAD_REQUEST)

    redis_instance = redis.Redis(host='redis', port=6379)
    file_to_decrypt_path = redis_instance.get(tracking_id)
    path = str(file_to_decrypt_path.decode("utf-8"))
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    from waitress import serve

    serve(app, host='0.0.0.0', port=8080)
