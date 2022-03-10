import os
import schedule
import time
from pathlib import Path

encrypt_uploads_dir_path = os.environ['ENCRYPT_FILE_UPLOAD_PATH']
decrypt_uploads_dir_path = os.environ['DECRYPT_FILE_UPLOAD_PATH']
# To delete files that was created more than the specified time in n number of seconds
file_removal_expiry_time = os.environ['FILE_REMOVAL_EXPIRY_TIME_SECONDS']
# To run cron job every n number of seconds
cron_job_time = os.environ['CRON_JOB_TIME_SECONDS']


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
