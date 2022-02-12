from flask import Flask

server = Flask(__name__)

import encryption_decryption_handler

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0')
