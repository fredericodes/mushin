import os
import re
import uuid

import dearpygui.dearpygui as dpg

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


dpg.create_context()


def callback(sender, app_data, user_data):
    file_path = re.search(r"(?:'selections': )(.*)", str(app_data)).group(1)
    file_path = re.search(r"(?:: )(.*)", str(file_path)).group(1)
    file_path = file_path.replace("'", "")
    file_path = file_path.replace("}", "")

    if os.path.exists(file_path):
        gen_uuid_key = str(uuid.uuid4().hex)
        key = str.encode(gen_uuid_key)
        cipher = AES.new(key, AES.MODE_CBC)
        with open(file_path, 'rb') as f:
            orig_file = f.read()
            encrypted_message = cipher.encrypt(pad(orig_file, AES.block_size))
            encrypted_file_path = file_path+".encrypted"
            with open(encrypted_file_path, "w") as e:
                e.write(str(encrypted_message))
                print("Your secret private key: " + gen_uuid_key)


with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=500,
                     height=500):
    dpg.add_file_extension(".*")

with dpg.window(label="Select file to encrypt", width=800, height=600):
    dpg.add_button(label="Select file", width=800, height=100, callback=lambda: dpg.show_item("file_dialog_id"))

dpg.create_viewport(title='Mushin', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
