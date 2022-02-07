import os
import re

import dearpygui.dearpygui as dpg

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

dpg.create_context()


def is_valid_file_path(app_data):
    file_path = re.search(r"(?:'selections': )(.*)", str(app_data)).group(1)
    file_path = re.search(r"(?:: )(.*)", str(file_path)).group(1)
    file_path = file_path.replace("'", "")
    file_path = file_path.replace("}", "")
    return file_path


def encrypt_file(file_path):
    key_bytes = os.urandom(32)  # For AES 256 encryption, key should be 32 bytes
    key = key_bytes.hex()
    cipher = AES.new(key_bytes, AES.MODE_CBC)
    with open(file_path, 'rb') as f:
        orig_file = f.read()
        encrypted_message = cipher.encrypt(pad(orig_file, AES.block_size))
        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, "w") as e:
            e.write(str(encrypted_message))
            print("Your secret private key: " + str(key))


def decrypt_file(file_path):
    print("decryption")


def encryption_callback(sender, app_data, user_data):
    file_path = is_valid_file_path(app_data)
    if os.path.exists(file_path):
        encrypt_file(file_path)


def decryption_callback(sender, app_data, user_data):
    print("decrypt test")


with dpg.file_dialog(directory_selector=False, show=False, callback=encryption_callback, id="file_encryption_dialog_id",
                     width=500,
                     height=500):
    dpg.add_file_extension(".*")

with dpg.file_dialog(directory_selector=False, show=False, callback=decryption_callback, id="file_decryption_dialog_id",
                     width=500,
                     height=500):
    dpg.add_file_extension(".*")

with dpg.window(label="Select file to encrypt or decrypt", width=800, height=600):
    dpg.add_button(label="Encrypt file", width=800, height=280,
                   callback=lambda: dpg.show_item("file_encryption_dialog_id"))
    dpg.add_button(label="Decrypt file", width=800, height=280,
                   callback=lambda: dpg.show_item("file_decryption_dialog_id"))

dpg.create_viewport(title='Mushin', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
