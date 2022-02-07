import os
import re
import pyperclip

import dearpygui.dearpygui as dpg

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

dpg.create_context()


def copy_key_to_clipboard(key):
    pyperclip.copy(key)
    dpg.add_button(label="Key is copied to you clipboard. Paste Ctrl+V to save it", parent=output_results)
    dpg.add_text("------", parent=output_results)


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
            return str(key)


def decrypt_file(file_path):
    print("decryption")


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


def decryption_callback(sender, app_data, user_data):
    print("decrypt test")
    if str(sender) == "file_decryption_dialog_id":
        dpg.add_button(label="Don't forget me!", parent=output_results)
    else:
        dpg.add_button(label="Don't forget me!", parent=output_results)


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
    dpg.add_text("Mushin encryption decryption logs:")

dpg.create_viewport(title='Mushin', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
