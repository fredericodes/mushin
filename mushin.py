import os
import re

import dearpygui.dearpygui as dpg


dpg.create_context()


def callback(sender, app_data, user_data):
    file_path = re.search(r"(?:'selections': )(.*)", str(app_data)).group(1)
    file_path = re.search(r"(?:: )(.*)", str(file_path)).group(1)
    file_path = file_path.replace("'", "")
    file_path = file_path.replace("}", "")

    if os.path.exists(file_path):
        file_name_with_ext = str(os.path.basename(file_path))
        file_name_without_ext, dot, ext = file_name_with_ext.partition('.')

    print(os.path.dirname(file_path))


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
