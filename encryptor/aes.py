import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

import hashlib


def encrypt_file(args):
    file_path = args[0]
    key = args[1]

    # For AES 256 encryption, key should be 32 bytes. Key hashed is 32 bytes.
    key_bytes = hashlib.sha256(key.encode()).digest()

    cipher = AES.new(key_bytes, AES.MODE_CBC)
    with open(file_path, 'rb') as f:
        orig_file = f.read()
        encrypted_message = cipher.encrypt(pad(orig_file, AES.block_size))
        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, "wb") as e:
            e.write(cipher.iv)
            e.write(encrypted_message)
            os.remove(file_path)


def decrypt_file(args):
    file_path = args[0]
    key = args[1]

    key_bytes = hashlib.sha256(key.encode()).digest()
    with open(file_path, 'rb') as c_file:
        iv = c_file.read(16)
        cipher_text = c_file.read()

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(cipher_text), AES.block_size)

    decrypted_file_path = file_path.replace(".encrypted", "")
    with open(decrypted_file_path, "wb") as e:
        e.write(decrypted_bytes)
