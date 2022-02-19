import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


def encrypt_file(file_path):
    key_bytes = os.urandom(32)  # For AES 256 encryption, key should be 32 bytes
    cipher = AES.new(key_bytes, AES.MODE_CBC)
    with open(file_path, 'rb') as f:
        orig_file = f.read()
        encrypted_message = cipher.encrypt(pad(orig_file, AES.block_size))
        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, "wb") as e:
            e.write(cipher.iv)
            e.write(encrypted_message)
            key = key_bytes.hex()
            os.remove(file_path)
            return str(key)

    return None


def decrypt_file(key, file_path):
    key_bytes = bytes.fromhex(key)
    with open(file_path, 'rb') as c_file:
        iv = c_file.read(16)
        cipher_text = c_file.read()

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted_bytes = unpad(cipher.decrypt(cipher_text), AES.block_size)

    decrypted_file_path = file_path.replace(".encrypted", "")
    with open(decrypted_file_path, "wb") as e:
        e.write(decrypted_bytes)
