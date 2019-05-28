"""
django_ocr_server/settings.py
This file contains default settings for OCR Server
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '21.02.2019/2019-03-29/2019-04-12'

from django.conf import settings
import os
import pathlib

STORE_FILES = True  # store uploaded files or not (True for debug)
FILE_PREVIEW = True  # show file preview in admin
TESSERACT_LANG = 'rus+eng'  # languages used by tesseract
STORE_PDF = True  # generate ocred_pdf from uploaded file and store it

STORE_FILES_DISABLED_LABEL = 'store_files_disabled'
STORE_PDF_DISABLED_LABEL = 'store_pdf_disabled'

FILE_REMOVED_LABEL = 'file_removed'
PDF_REMOVED_LABEL = 'pdf_removed'

# The types of file allowed to uploading to OCR Server 2019-03-18
ALLOWED_FILE_TYPES = (
    'application/pdf',
    'image/jpeg',
    'image/png',
    'image/bmp',
    'image/tiff',
)

FILES_UPLOAD_TO = __package__ + '/upload/'  # directory for saving uploaded files
PDF_UPLOAD_TO = __package__ + '/pdf/'  # directory for created searchable PDFs

"""
TimeToLive settings
{PARAM_NAME}_TTL = timedelta(..)
FILES_TTL = 0  # TTL for OCRedFile.files is disabled
PDF_TTL = 0  # TTL for OCRedFile.ocred_pdfs is disabled
TTL = 0  # TTL for OCRedFile is disabled
When current datetime will grater OCRedFile.uploaded+{PARAM}_TTL corresponding object will be removed
"""
FILES_TTL = 0
PDF_TTL = 0
TTL = 0

"""
Creates folders for storing uploaded files and ocred pdfs if these do not exist
"""
files_upload_to = os.path.join(settings.BASE_DIR,
                               getattr(settings, 'OCR_FILES_UPLOAD_TO', FILES_UPLOAD_TO))
pdf_upload_to = os.path.join(settings.BASE_DIR,
                             getattr(settings, 'OCR_PDF_UPLOAD_TO', PDF_UPLOAD_TO))
if not os.path.isdir(files_upload_to):
    pathlib.Path(files_upload_to).mkdir(parents=True, exist_ok=True)
if not os.path.isdir(pdf_upload_to):
    pathlib.Path(pdf_upload_to).mkdir(parents=True, exist_ok=True)
