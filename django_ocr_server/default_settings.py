"""
django_ocr_server/default_settings.py
+++++++++++++++++++++++++++++++++++++

This file contains default settings for OCR Server

| Author: shmakovpn <shmakovpn@yandex.ru>
| Date: 2019-02-21/2019-03-29/2019-04-12/2021-01-19
"""
from typing import List
import os
from datetime import timedelta
from django.conf import settings

# configure Django's settings if not configured (need for Sphinx autodoc)
if not settings.configured:
    settings.configure(
        BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

OCR_STORE_FILES: bool = True  #: Store uploaded files (True) or not (False), default to True
OCR_FILE_PREVIEW: bool = True  #: Show file preview in admin (True) or not (False), default to True
OCR_TESSERACT_LANG: str = 'rus+eng'  #: Sets priority of using languages, default to 'rus+eng'
OCR_STORE_PDF: bool = True  #: Generate and store recognized searchable PDF (True) or not (False), default to True

OCR_STORE_FILES_DISABLED_LABEL: str = 'store_files_disabled'
"""The text of storeing uploaded files disabled label in the admin interface"""

OCR_STORE_PDF_DISABLED_LABEL: str = 'store_pdf_disabled'
"""The text of storeing recognized PDF disabled label in the admin interface"""

OCR_FILE_REMOVED_LABEL: str = 'file_removed'
"""The text of the label of *file removed* in the admin interface"""

OCR_PDF_REMOVED_LABEL: str = 'pdf_removed'
"""The text of the label of *PDF removed* in the admin interface"""

OCR_ALLOWED_FILE_TYPES: List[str] = [
    'application/pdf',
    'image/jpeg',
    'image/png',
    'image/bmp',
    'image/tiff',
]
"""The types of file allowed to uploading"""
"""
2019-10-22 shmakovpn. An error was found when trying to deploy Django-OCR_Server using Apache
because usage of relative paths is a wrong way when Apache mod_wsgi is using
https://modwsgi.readthedocs.io/en/develop/user-guides/application-issues.html#application-working-directory
"""

OCR_FILES_UPLOAD_TO: str = os.path.join(settings.BASE_DIR, __package__,
                                        'upload')
"""The directory for saving uploaded files"""

OCR_PDF_UPLOAD_TO: str = os.path.join(settings.BASE_DIR, __package__, 'pdf')
"""The directory for storeing searchable PDFs"""

OCR_FILES_TTL: timedelta = timedelta(0)
"""
When current datetime will be grater then the datetime of file uploading plus this timedelta,
the uploaded file will be removed.
*timedelta(0)* means that **OCR_FILES_TTL** is disabled.
Defaults to *timedelta(0)*.
"""

OCR_PDF_TTL: timedelta = timedelta(0)
"""
When current datetime will be grater then the datetime of creating recognized PDF plus this timedelta,
the recognized PDF will be removed.
*timedelta(0)* means that **OCR_PDF_TTL** is disabled.
Defaults to *timedelta(0)*.
"""

OCR_TTL: timedelta = timedelta(0)
"""
When current datetime will be grater then the datetime of creating the model (OCRedFile) in the database plus this timedelta,
the model in the database will be removed.
*timedelta(0)* means that **OCR_TTL** is disabled.
Defaults to *timedelta(0)*.
"""
