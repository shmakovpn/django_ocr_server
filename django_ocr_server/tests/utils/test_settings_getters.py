"""
django_ocr_server/tests/utils/test_settings_getters.py



Author: shmakovpn <shmakovpn@yandex.ru>
Date: 2021-01-19
"""
from datetime import time, timedelta
from django.test import SimpleTestCase, override_settings
from django.conf import settings
import django_ocr_server.settings as _s
import django_ocr_server.utils as _u


class TestUtilsSettingsGetters(SimpleTestCase):
    @override_settings(OCR_STORE_FILES=None)
    def test_get_store_files__not_set(self):
        """Testing get_store_files when no OCR_STORE_FILES"""
        del settings.OCR_STORE_FILES
        self.assertEqual(_u.get_store_files(), _s.STORE_FILES)

    @override_settings(OCR_STORE_FILES=True)
    def test_get_store_files__true(self):
        """Testing get_store_files() when OCR_STORE_FILES is True"""
        self.assertEqual(_u.get_store_files(), True)

    @override_settings(OCR_STORE_FILES=False)
    def test_get_store_files__false(self):
        """Testing get_store_files() when OCR_STORE_FILES is False"""
        self.assertEqual(_u.get_store_files(), False)

    @override_settings(OCR_FILE_PREVIEW=None)
    def test_get_file_preview__not_set(self):
        """Testing get_file_preview() when no OCR_FILE_PREVIEW"""
        del settings.OCR_FILE_PREVIEW
        self.assertEqual(_u.get_file_preview(), _s.FILE_PREVIEW)

    @override_settings(OCR_FILE_PREVIEW=True)
    def test_get_file_preview__true(self):
        """Testing get_file_preview() when OCR_FILE_PREVIEW is True"""
        self.assertEqual(_u.get_file_preview(), True)

    @override_settings(OCR_FILE_PREVIEW=False)
    def test_get_file_preview__false(self):
        """Testing get_file_preview() when OCR_FILE_PREVIEW is False"""
        self.assertEqual(_u.get_file_preview(), False)

    @override_settings(OCR_TESSERACT_LANG=None)
    def test_get_tesseract_lang__not_set(self):
        """Testing get_tesseract_lang() when no OCR_TESSERACT_LANG"""
        del settings.OCR_TESSERACT_LANG
        self.assertEqual(_u.get_tesseract_lang(), _s.TESSERACT_LANG)

    @override_settings(OCR_TESSERACT_LANG='new+lang')
    def test_get_tesseract_lang__overrided(self):
        """Testing get_tesseract when OCR_TESSERACT_LANG is set"""
        self.assertEqual(_u.get_tesseract_lang(), 'new+lang')

    @override_settings(OCR_STORE_PDF=None)
    def test_get_store_pdf__not_set(self):
        """Testing get_store_pdf() when no OCR_STORE_PDF"""
        del settings.OCR_STORE_PDF
        self.assertEqual(_u.get_store_pdf(), _s.STORE_PDF)

    @override_settings(OCR_STORE_PDF=True)
    def test_get_store_pdf__true(self):
        """Testing get_store_pdf() when OCR_STORE_PDF is True"""
        self.assertEqual(_u.get_store_pdf(), True)

    @override_settings(OCR_STORE_PDF=False)
    def test_get_store_pdf__false(self):
        """Testing get_store_pdf() when OCR_STORE_PDF is False"""
        self.assertEqual(_u.get_store_pdf(), False)

    @override_settings(OCR_FILES_UPLOAD_TO=None)
    def test_get_ocr_files_upload_to__not_set(self):
        """Testing get_ocr_files_upload_to() when no OCR_FILES_UPLOAD_TO"""
        del settings.OCR_FILES_UPLOAD_TO
        self.assertEqual(_u.get_files_upload_to(), _s.FILES_UPLOAD_TO)

    @override_settings(OCR_FILES_UPLOAD_TO='upload+to')
    def test_get_ocr_files_upload_to__overrided(self):
        """Testing get_ocr_file_upload_to() when is OCR_FILES_UPLOAD_TO is set"""
        self.assertEqual(_u.get_files_upload_to(), 'upload+to')

    @override_settings(OCR_PDF_UPLOAD_TO=None)
    def test_get_ocr_pdf_upload_to__not_set(self):
        """Testing get_pdf_upload_to() when no OCR_PDF_UPLOAD_TO"""
        del settings.OCR_PDF_UPLOAD_TO
        self.assertEqual(_u.get_pdf_upload_to(), _s.PDF_UPLOAD_TO)

    @override_settings(OCR_PDF_UPLOAD_TO='pdf+to')
    def test_get_ocr_pdf_upload_to__overrided(self):
        """Testing get_pdf_upload_to() when OCR_PDF_UPLOAD_TO is set"""
        self.assertEqual(_u.get_pdf_upload_to(), 'pdf+to')

    @override_settings(OCR_FILES_TTL=None)
    def test_ocr_files_ttl__not_set(self):
        """Testing get_ocr_files_ttl() when no OCR_FILES_TTL"""
        del settings.OCR_FILES_TTL
        self.assertEqual(_u.get_ocr_files_ttl(), _s.FILES_TTL)

    @override_settings(OCR_FILES_TTL=timedelta(days=36))
    def test_ocr_files_ttl__overrided(self):
        """Testing get_ocr_files_ttl() when OCR_FILES_TTL is set"""
        self.assertEqual(_u.get_ocr_files_ttl(), timedelta(days=36))

    @override_settings(OCR_PDF_TTL=None)
    def test_ocr_pdf_ttl__not_set(self):
        """Testing get_pdf_ttl() when no OCR_PDF_TTL"""
        del settings.OCR_PDF_TTL
        self.assertEqual(_u.get_ocr_pdf_ttl(), _s.PDF_TTL)

    @override_settings(OCR_PDF_TTL=timedelta(days=36))
    def test_ocr_pdf_ttl__overrided(self):
        """Testing get_ocr_pdf_ttl() when OCR_PDF_TTL is set"""
        self.assertEqual(_u.get_ocr_pdf_ttl(), timedelta(days=36))

    @override_settings(OCR_TTL=None)
    def test_ocr_ttl__not_set(self):
        """Testing get_ocr_ttl() when no OCR_TTL"""
        del settings.OCR_TTL
        self.assertEqual(_u.get_ocr_ttl(), _s.TTL)

    @override_settings(OCR_TTL=timedelta(days=36))
    def test_ocr_ttl__overrided(self):
        """Testing get_ocr_ttl() when OCR_TTL is set"""
        self.assertEqual(_u.get_ocr_ttl(), timedelta(days=36))