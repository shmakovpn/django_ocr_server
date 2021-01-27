"""
django_ocr_server/__init__.py
+++++++++++++++++++++++++++++

| Author: shmakovpn <shmakovpn@yandex.ru>
| Date: 2019-10-22,2019-04-15,2019-10-11,2019-12-03,2021-01-22
"""
import pathlib
from django_ocr_server.conf import ocr_settings

# Creating folders for storing uploaded files and recognized PDFs if these do not exist
pathlib.Path(ocr_settings.OCR_PDF_UPLOAD_TO).mkdir(parents=True, exist_ok=True)
pathlib.Path(ocr_settings.OCR_PDF_UPLOAD_TO).mkdir(parents=True, exist_ok=True)