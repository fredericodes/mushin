import os
import schedule
import time
from pathlib import Path

encrypt_uploads_dir_path = '/app/server/encrypt-uploads'
decrypt_uploads_dir_path = '/app/server/decrypt-uploads'
file_removal_expiry_time = 1200  # To delete files that was created more than 20 minutes ago
cron_job_time = 30  # To run cron job every 30 seconds


def remove_files_exceeded_expiry_time():
    Path(encrypt_uploads_dir_path).mkdir(parents=True, exist_ok=True)
    Path(decrypt_uploads_dir_path).mkdir(parents=True, exist_ok=True)

    arr_encrypt_upload_files = os.listdir(encrypt_uploads_dir_path)
    arr_decrypt_upload_files = os.listdir(decrypt_uploads_dir_path)

    for encrypt_file in arr_encrypt_upload_files:
        if time.time() - os.path.getctime(encrypt_uploads_dir_path + "/" + encrypt_file) > file_removal_expiry_time:
            os.remove(encrypt_uploads_dir_path + "/" + encrypt_file)

    for decrypt_file in arr_decrypt_upload_files:
        if time.time() - os.path.getctime(decrypt_uploads_dir_path + "/" + decrypt_file) > file_removal_expiry_time:
            os.remove(decrypt_uploads_dir_path + "/" + decrypt_file)


schedule.every(cron_job_time).seconds.do(remove_files_exceeded_expiry_time)

while True:
    schedule.run_pending()
    time.sleep(1)
