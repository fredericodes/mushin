import flask
from flask_cors import CORS
from flask import Flask, send_from_directory, request

import os

app = Flask(__name__)
cors = CORS(app)


@app.route("/")
def demo():
    return "hello"


@app.route('/uploads', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        return flask.Response(status=200)

    return flask.Response(status=404)


# serve the uploaded files
@app.route('/uploads/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path('/')
    return send_from_directory(directory=uploads, filename=filename)


if __name__ == '__main__':
    app.run( host='0.0.0.0', debug=True)

