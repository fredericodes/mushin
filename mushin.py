import dearpygui.dearpygui as dpg

dpg.create_context()

def callback(sender, app_data, user_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)

with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id"):
    dpg.add_file_extension(".*")

with dpg.window(label="Select file to encrypt", width=800, height=600):
    dpg.add_button(label="Select file", callback=lambda: dpg.show_item("file_dialog_id"))

dpg.create_viewport(title='Mushin', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
