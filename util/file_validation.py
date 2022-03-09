import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))

from PIL import Image

import zipfile
import eyed3
import magic


mimetype_txt = 'text/plain'
mimetype_pdf = 'application/pdf'
mimetype_doc = 'application/msword'
mimetype_docx = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
mimetype_csv = 'text/csv'
mimetype_csv1 = 'application/csv'
mimetype_xls = 'application/vnd.ms-excel'
mimetype_xlsx = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def is_jpg(filename):
    try:
        i = Image.open(filename)
        if i.format == 'JPEG' or i.format == 'JPG':
            return True
    except IOError:
        return False


def is_png(filename):
    try:
        i = Image.open(filename)
        return i.format == 'PNG'
    except IOError:
        return False


def is_gif(filename):
    try:
        i = Image.open(filename)
        return i.format == 'GIF'
    except IOError:
        return False


def is_tif(filename):
    try:
        i = Image.open(filename)
        if i.format == 'TIFF' or i.format == 'TIF':
            return True
    except IOError:
        return False


def is_txt(filename):
    if magic.from_file(filename, mime=True) == mimetype_txt:
        return True

    return False


def is_pdf(filename):
    if magic.from_file(filename, mime=True) == mimetype_pdf:
        return True

    return False


def is_doc(filename):
    file_mime = magic.from_file(filename, mime=True)
    if file_mime == mimetype_doc or file_mime == mimetype_docx:
        return True

    return False


def is_csv(filename):
    file_mime = magic.from_file(filename, mime=True)
    if file_mime == mimetype_csv or file_mime == mimetype_csv1:
        return True

    return False


def is_xls(filename):
    file_mime = magic.from_file(filename, mime=True)
    if file_mime == mimetype_xls or file_mime == mimetype_xlsx:
        return True

    return False


def is_zip(filename):
    return zipfile.is_zipfile(filename)


def is_mp3(filename):
    if eyed3.load(filename) is None:
        return False

    return True


def is_valid_file(filename, file_extension):
    if file_extension == '.txt':
        return is_txt(filename)
    elif file_extension == '.jpg':
        return is_jpg(filename)
    elif file_extension == '.jpeg':
        return is_jpg(filename)
    elif file_extension == '.png':
        return is_png(filename)
    elif file_extension == '.gif':
        return is_gif(filename)
    elif file_extension == '.pdf':
        return is_pdf(filename)
    elif file_extension == '.docx':
        return is_doc(filename)
    elif file_extension == '.doc':
        return is_doc(filename)
    elif file_extension == '.xls':
        return is_xls(filename)
    elif file_extension == '.xlsx':
        return is_xls(filename)
    elif file_extension == '.csv':
        return is_csv(filename)
    elif file_extension == '.csv1':
        return is_csv(filename)
    elif file_extension == '.zip':
        return is_zip(filename)
    elif file_extension == '.mp3':
        return is_mp3(filename)
    elif file_extension == '.tif':
        return is_tif(filename)
    elif file_extension == '.tiff':
        return is_tif(filename)
    else:
        return False
