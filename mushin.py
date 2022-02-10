import os
import re
import pyperclip

import dearpygui.dearpygui as dpg

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

dpg.create_context()


def copy_key_to_clipboard(key):
    pyperclip.copy(key)
    dpg.add_button(label="Key is copied to your clipboard. Paste it to save it", parent=output_results)
    dpg.add_text("------", parent=output_results)


def is_valid_file_path(app_data):
    file_path = re.search(r"(?:'selections': )(.*)", str(app_data)).group(1)
    file_path = re.search(r"(?:: )(.*)", str(file_path)).group(1)
    file_path = file_path.replace("'", "")
    file_path = file_path.replace("}", "")
    return file_path


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
            return str(key)


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


def encryption_callback(sender, app_data, user_data):
    file_path = is_valid_file_path(app_data)
    if os.path.exists(file_path):
        key = encrypt_file(file_path)
        dpg.add_text("The file is encrypted in the path:", parent=output_results)
        dpg.add_text(file_path + ".encrypted", parent=output_results)
        dpg.add_text("The file wont be recoverable if secret key is lost", parent=output_results)
        dpg.add_text("Store the secret private key safely to decrypt it later:", parent=output_results)
        dpg.add_text("Click on the key to save it to your clipboard and paste the key somewhere", parent=output_results)
        dpg.add_button(label=str(key), parent=output_results, callback=lambda: copy_key_to_clipboard(str(key)))
        dpg.add_text("------", parent=output_results)


def decrypt_file_callback(sender, app_data, user_data):
    private_secret_key = dpg.get_value("key_str")
    if private_secret_key == "":
        dpg.add_text("Private secret key not provided for decryption", parent=output_results)
        dpg.add_text("------", parent=output_results)
    else:
        decrypt_file(private_secret_key, user_data)
        dpg.add_text("File is now decrypted! You may now open the decrypted file to view its contents", parent=output_results)
        dpg.add_text("------", parent=output_results)


def decryption_callback(sender, app_data, user_data):
    file_path = is_valid_file_path(app_data)
    if os.path.exists(file_path):
        dpg.add_window(label="Decryption", height=150, width=300, pos=[250, 250], tag="decryption_window")
        dpg.add_button(label="Enter private secret key below", parent="decryption_window", width=300, height=60)
        dpg.add_input_text(parent="decryption_window", width=300, tag="key_str")
        dpg.add_button(label="Decrypt file", parent="decryption_window", pos=[110, 120], callback=lambda: decrypt_file_callback(sender, app_data, file_path))


with dpg.file_dialog(directory_selector=False, show=False, callback=encryption_callback, id="file_encryption_dialog_id",
                     width=500,
                     height=500):
    dpg.add_file_extension(".*")

with dpg.file_dialog(directory_selector=False, show=False, callback=decryption_callback, id="file_decryption_dialog_id",
                     width=500,
                     height=500):
    dpg.add_file_extension(".*")

with dpg.window(label="Select file to encrypt or decrypt", width=800, height=290, pos=[0]) as window:
    dpg.add_button(label="Encrypt file", width=400, height=280, pos=[0],
                   callback=lambda: dpg.show_item("file_encryption_dialog_id"))
    dpg.add_button(label="Decrypt file", width=400, height=280, pos=[405],
                   callback=lambda: dpg.show_item("file_decryption_dialog_id"))

with dpg.window(label="Output", width=800, height=305, pos=[0, 290], horizontal_scrollbar=True) as output_results:
    dpg.add_text("Mushin encryption and decryption logs:")


dpg.create_viewport(title='Mushin', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
