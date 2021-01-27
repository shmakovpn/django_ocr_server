""" 
django_ocr_server/tests/default_settings.py
+++++++++++++++++++++++++++++++++++++++++++

Tests for *django_ocr_server/default_settings.py*.

| Author: shmakovpn <shmakovpn@yandex.ru>
| Date: 2021-01-07
"""
from datetime import timedelta
import os
from typing import List
from django.test import SimpleTestCase
import django_ocr_server.default_settings as _ds
from django.conf import settings


class TestDefaultSettings(SimpleTestCase):
    def test_dstore_files(self) -> None:
        self.assertTrue(_ds.OCR_STORE_FILES)

    def test_file_preview(self) -> None:
        self.assertTrue(_ds.OCR_FILE_PREVIEW)

    def test_tesseract_lang(self) -> None:
        self.assertEqual(_ds.OCR_TESSERACT_LANG, 'rus+eng')

    def test_dstore_pdf(self) -> None:
        self.assertTrue(_ds.OCR_STORE_PDF)

    def test_dstore_files_disabled_label(self) -> None:
        self.assertEqual(_ds.OCR_STORE_FILES_DISABLED_LABEL,
                         'store_files_disabled')

    def test_dstore_pdf_disabled_label(self) -> None:
        self.assertEqual(_ds.OCR_STORE_PDF_DISABLED_LABEL,
                         'store_pdf_disabled')

    def test_file_removed_label(self) -> None:
        self.assertEqual(_ds.OCR_FILE_REMOVED_LABEL, 'file_removed')

    def test_pdf_removed_label(self) -> None:
        self.assertEqual(_ds.OCR_PDF_REMOVED_LABEL, 'pdf_removed')

    def test_allowed_file_types(self) -> None:
        self.assertEqual(len(_ds.OCR_ALLOWED_FILE_TYPES), 5)
        self.assertIn('application/pdf', _ds.OCR_ALLOWED_FILE_TYPES)
        self.assertIn('image/jpeg', _ds.OCR_ALLOWED_FILE_TYPES)
        self.assertIn('image/png', _ds.OCR_ALLOWED_FILE_TYPES)
        self.assertIn('image/bmp', _ds.OCR_ALLOWED_FILE_TYPES)
        self.assertIn('image/tiff', _ds.OCR_ALLOWED_FILE_TYPES)

    def test_files_upload_to(self) -> None:
        files_upload_to: str = os.path.join(settings.BASE_DIR,
                                            'django_ocr_server', 'upload')
        self.assertEqual(_ds.OCR_FILES_UPLOAD_TO, files_upload_to)

    def test_pdf_upload_to(self) -> None:
        pdf_upload_to: str = os.path.join(settings.BASE_DIR,
                                          'django_ocr_server', 'pdf')
        self.assertEqual(_ds.OCR_PDF_UPLOAD_TO, pdf_upload_to)

    def test_files_ttl(self) -> None:
        self.assertEqual(_ds.OCR_FILES_TTL, timedelta(0))

    def test_pdf_ttl(self) -> None:
        self.assertEqual(_ds.OCR_PDF_TTL, timedelta(0))

    def test_ttl(self) -> None:
        self.assertEqual(_ds.OCR_TTL, timedelta(0))

    def test_default_settings_amount(self) -> None:
        """The testing that amount of default settings is equal 14"""
        settings: List[str] = dir(_ds)
        filtered_settings_list: List[str] = list(
            filter(lambda x: x.startswith('OCR'), settings))
        self.assertEqual(len(filtered_settings_list), 14)
