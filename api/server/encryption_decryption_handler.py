from __main__ import server


@server.route('/api/v1/encrypt-file', methods=['GET'])
def encrypt_file():
    return 'encryption!'


@server.route('/api/v1/decrypt-file', methods=['GET'])
def decrypt_file():
    return 'decryption!'
