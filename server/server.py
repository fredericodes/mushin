import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

import os
import shutil
import flask
import uuid

from flask import Flask, request, current_app, make_response

from producer.producer import add_to_work_queue


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4000 * 1024 * 1024
app.config['ENCRYPT_FILE_UPLOAD_PATH'] = './encrypt-uploads'
app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.docx', '.doc', '.xls', '.csv', '.zip', '.mp4', '.mp3']


def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route('/upload-encrypt-file', methods=['POST', 'OPTIONS'])
def upload_encrypt_file():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "POST":  # The actual request following the preflight
        if not os.path.exists(app.config['ENCRYPT_FILE_UPLOAD_PATH']):
            os.makedirs(app.config['ENCRYPT_FILE_UPLOAD_PATH'])

        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_ext = os.path.splitext(uploaded_file.filename)[1]
            if file_ext not in current_app.config['ENCRYPT_FILE_UPLOAD_EXTENSIONS']:
                return _corsify_actual_response(flask.Response(status=400))

            upload_file_path = current_app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file.filename
            uploaded_file.save(upload_file_path)
            uploaded_file_unique_name = str(uuid.uuid4()) + "-" + str(uploaded_file.filename)
            shutil.copyfile(upload_file_path,
                            current_app.config['ENCRYPT_FILE_UPLOAD_PATH'] + "/" + uploaded_file_unique_name)
            os.remove(upload_file_path)
            # add_to_work_queue(uploaded_file_unique_name)
            # response = {"encryptionFileName": uploaded_file_unique_name}
            # response.headers.add('Access-Control-Allow-Origin', '*')
            return _corsify_actual_response(flask.Response(status=200))

        return _corsify_actual_response(flask.Response(status=404))


@app.route('/upload-decrypt-file', methods=['POST'])
def upload_decrypt_file():
    return flask.Response(status=200)


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
