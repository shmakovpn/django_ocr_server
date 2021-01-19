""" 
django_ocr_server/tests/default_settings.py

Author: shmakovpn <shmakovpn@yandex.ru>
Date: 2021-01-07
"""
import os
from django.test import SimpleTestCase
import django_ocr_server.settings as _s
from django.conf import settings


class TestDefaultSettings(SimpleTestCase):
    def test_store_files(self):
        self.assertTrue(_s.STORE_FILES)

    def test_file_preview(self):
        self.assertTrue(_s.FILE_PREVIEW)

    def test_tesseract_lang(self):
        self.assertEqual(_s.TESSERACT_LANG, 'rus+eng')

    def test_store_pdf(self):
        self.assertTrue(_s.STORE_PDF)

    def test_store_files_disabled_label(self):
        self.assertEqual(_s.STORE_FILES_DISABLED_LABEL, 'store_files_disabled')

    def test_store_pdf_disabled_label(self):
        self.assertEqual(_s.STORE_PDF_DISABLED_LABEL, 'store_pdf_disabled')

    def test_file_removed_label(self):
        self.assertEqual(_s.FILE_REMOVED_LABEL, 'file_removed')

    def test_pdf_removed_label(self):
        self.assertEqual(_s.PDF_REMOVED_LABEL, 'pdf_removed')

    def test_allowed_file_types(self):
        self.assertEqual(len(_s.ALLOWED_FILE_TYPES), 5)
        self.assertIn('application/pdf', _s.ALLOWED_FILE_TYPES)
        self.assertIn('image/jpeg', _s.ALLOWED_FILE_TYPES)
        self.assertIn('image/png', _s.ALLOWED_FILE_TYPES)
        self.assertIn('image/bmp', _s.ALLOWED_FILE_TYPES)
        self.assertIn('image/tiff', _s.ALLOWED_FILE_TYPES)

    def test_files_upload_to(self):
        files_upload_to: str = os.path.join(settings.BASE_DIR, 'django_ocr_server',
                                            'upload')
        self.assertEqual(_s.FILES_UPLOAD_TO, files_upload_to)

    def test_pdf_upload_to(self):
        pdf_upload_to: str = os.path.join(settings.BASE_DIR, 'django_ocr_server',
                                          'pdf')
        self.assertEqual(_s.PDF_UPLOAD_TO, pdf_upload_to)
    
    def test_files_ttl(self):
        self.assertEqual(_s.FILES_TTL, 0)
    
    def test_pdf_ttl(self):
        self.assertEqual(_s.PDF_TTL, 0)
    
    def test_ttl(self):
        self.assertEqual(_s.TTL, 0)