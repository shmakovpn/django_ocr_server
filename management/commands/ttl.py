"""
django_ocr_server/management/commands/ttl.py
Removes all instances of OCRedFile whose OCRedFile.uploaded+OCR_TTL lower current datetime
     if OCR_TTL does not 0, (NOTE: if OCR_TTL<0 all instances of OCRedFile will be removed, use only for tests).
Removes all OCRedFile.files whose OCRedFile.uploaded+OCR_FILES_TTL lower current datetime
     if OCR_FILES_TTL does not 0,
     (NOTE: if OCR_FILES_TTL<0 all OCRedFile.files will be removed, use only for tests).
Removes all OCRedFile.ocred_pdfs whose OCRedFile.uploaded+OCR_PDF_TTL lower current datetime
     if OCR_PDF_TTL does not 0,
     (NOTE: if OCR_PDF_TTL<0 all OCRedFile.ocred_pdfs will be removed, use only for tests). 2019-04-13
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-04-18'


from django.core.management.base import BaseCommand
from django_ocr_server.models import *


class Command(BaseCommand):
    """
    Removes all instances of OCRedFile whose OCRedFile.uploaded+OCR_TTL lower current datetime
         if OCR_TTL does not 0, (NOTE: if OCR_TTL<0 all instances of OCRedFile will be removed, use only for tests).
    Removes all OCRedFile.files whose OCRedFile.uploaded+OCR_FILES_TTL lower current datetime
         if OCR_FILES_TTL does not 0,
         (NOTE: if OCR_FILES_TTL<0 all OCRedFile.files will be removed, use only for tests).
    Removes all OCRedFile.ocred_pdfs whose OCRedFile.uploaded+OCR_PDF_TTL lower current datetime
         if OCR_PDF_TTL does not 0,
        (NOTE: if OCR_PDF_TTL<0 all OCRedFile.ocred_pdfs will be removed, use only for tests). 2019-04-18
    """
    help = """
    Removes all instances of OCRedFile whose OCRedFile.uploaded+OCR_TTL lower current datetime
         if OCR_TTL does not 0, (NOTE: if OCR_TTL<0 all instances of OCRedFile will be removed, use only for tests).
    Removes all OCRedFile.files whose OCRedFile.uploaded+OCR_FILES_TTL lower current datetime
         if OCR_FILES_TTL does not 0,
         (NOTE: if OCR_FILES_TTL<0 all OCRedFile.files will be removed, use only for tests).
    Removes all OCRedFile.ocred_pdfs whose OCRedFile.uploaded+OCR_PDF_TTL lower current datetime
         if OCR_PDF_TTL does not 0,
        (NOTE: if OCR_PDF_TTL<0 all OCRedFile.ocred_pdfs will be removed, use only for tests).
    """

    def handle(self, *args, **options):
        """
        Removes all instances of OCRedFile whose OCRedFile.uploaded+OCR_TTL lower current datetime
             if OCR_TTL does not 0, (NOTE: if OCR_TTL<0 all instances of OCRedFile will be removed, use only for tests).
        Removes all OCRedFile.files whose OCRedFile.uploaded+OCR_FILES_TTL lower current datetime
             if OCR_FILES_TTL does not 0,
             (NOTE: if OCR_FILES_TTL<0 all OCRedFile.files will be removed, use only for tests).
        Removes all OCRedFile.ocred_pdfs whose OCRedFile.uploaded+OCR_PDF_TTL lower current datetime
             if OCR_PDF_TTL does not 0,
             (NOTE: if OCR_PDF_TTL<0 all OCRedFile.ocred_pdfs will be removed, use only for tests). 2019-04-18
        :param args: not used
        :param options: not used
        :return: None
        """
        ttl_result = OCRedFile.ttl()
        self.stdout.write(self.style.SUCCESS('Total models removed: %s' % str(ttl_result[0])))
        self.stdout.write(self.style.SUCCESS('Total files removed: %s' % str(ttl_result[1])))
        self.stdout.write(self.style.SUCCESS('Total pdf removed: %s' % str(ttl_result[2])))
