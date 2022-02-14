import flask, uuid
from flask_cors import CORS
from flask import Flask, send_from_directory, request, current_app

import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4000 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.docx', '.doc', '.xls', '.csv', '.zip']
cors = CORS(app)


@app.route("/")
def demo():
    return "hello"


@app.route('/uploads', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return flask.Response(status=400)
        uploaded_file.save(str(uuid.uuid4()))
        return flask.Response(status=200)

    return flask.Response(status=404)


# serve the uploaded files
@app.route('/uploads/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path('/')
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == '__main__':
    app.run( host='0.0.0.0', debug=True)

