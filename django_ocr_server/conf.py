"""
django_ocr_server/conf.py
+++++++++++++++++++++++++

The settings manager for **django_ocr_server**.

Usage:

.. code-block:: python

 from django_ocr_server.conf import ocr_settings
 # Next line will print a value of **OCR_TESSERACT_LANG**
 # using the variable from the Django's *settings.py* file
 # if the variable is set there.
 # Or the default value of **OCR_TESSERACT_LANG** from
 # *django_ocr_server/default_settings.py* otherwise.
 print(ocr_settings.OCR_TESSERACT_LANG)

| Author: shmakovpn <shmakovpn@yandex.ru>
| Date: 2021-01-20
"""
from typing import List
from datetime import timedelta
from django.conf import settings as _s
import django_ocr_server.default_settings as _ds


class DjangoOcrSettings:
    """The settings manager of **django_ocr_server**"""
    @property
    def OCR_STORE_FILES(_) -> bool:
        return bool(getattr(_s, 'OCR_STORE_FILES', _ds.OCR_STORE_FILES))

    @property
    def OCR_FILE_PREVIEW(_) -> bool:
        return bool(getattr(_s, 'OCR_FILE_PREVIEW', _ds.OCR_FILE_PREVIEW))

    @property
    def OCR_TESSERACT_LANG(_) -> str:
        return str(getattr(_s, 'OCR_TESSERACT_LANG', _ds.OCR_TESSERACT_LANG))

    @property
    def OCR_STORE_PDF(_) -> bool:
        return bool(getattr(_s, 'OCR_STORE_PDF', _ds.OCR_STORE_PDF))

    @property
    def OCR_STORE_FILES_DISABLED_LABEL(_) -> str:
        return str(
            getattr(_s, 'OCR_STORE_FILES_LABEL',
                    _ds.OCR_STORE_FILES_DISABLED_LABEL))

    @property
    def OCR_STORE_PDF_DISABLED_LABEL(_) -> str:
        return str(
            getattr(_s, 'OCR_FILE_REMOVED_LABEL', _ds.OCR_FILE_REMOVED_LABEL))

    @property
    def OCR_FILE_REMOVED_LABEL(_) -> str:
        return str(
            getattr(_s, 'OCR_FILE_REMOVED_LABEL', _ds.OCR_FILE_REMOVED_LABEL))

    @property
    def OCR_PDF_REMOVED_LABEL(_) -> str:
        return str(
            getattr(_s, 'OCR_PDF_REMOVED_LABEL', _ds.OCR_PDF_REMOVED_LABEL))

    @property
    def OCR_ALLOWED_FILE_TYPES(_) -> List[str]:
        return list(
            getattr(_s, 'OCR_ALLOWED_FILE_TYPES', _ds.OCR_ALLOWED_FILE_TYPES))

    @property
    def OCR_FILES_UPLOAD_TO(_) -> str:
        return str(getattr(_s, 'OCR_FILES_UPLOAD_TO', _ds.OCR_FILES_UPLOAD_TO))

    @property
    def OCR_PDF_UPLOAD_TO(_) -> str:
        return str(getattr(_s, 'OCR_PDF_UPLOAD_TO', _ds.OCR_PDF_UPLOAD_TO))

    @property
    def OCR_FILES_TTL(_) -> timedelta:
        return getattr(_s, 'OCR_FILES_TTL', _ds.OCR_FILES_TTL)

    @property
    def OCR_PDF_TTL(_) -> timedelta:
        return getattr(_s, 'ocr_pdf_ttl', _ds.OCR_PDF_TTL)

    @property
    def OCR_TTL(_) -> timedelta:
        return getattr(_s, 'OCR_TTL', _ds.OCR_TTL)


ocr_settings: DjangoOcrSettings = DjangoOcrSettings()
"""The instance of settings manager of **django_ocr_server**"""