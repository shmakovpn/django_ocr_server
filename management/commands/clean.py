"""
django_ocr_server/management/commands/clean.py
CleanUps folders for OCRedFile.files and OCRedFile.ocred_pdfs from files do not present in OCRedFiles
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-04-18'


from django.core.management.base import BaseCommand
from django_ocr_server.models import *


class Command(BaseCommand):
    """
    CleanUps folders for OCRedFile.files and OCRedFile.ocred_pdfs from files do not present in OCRedFiles 2019-04-18
    """
    help = 'CleanUps folders for OCRedFile.files and OCRedFile.ocred_pdfs from files do not present in OCRedFiles'

    def handle(self, *args, **options):
        """
        CleanUps folders for OCRedFile.files and OCRedFile.ocred_pdfs from files do not present in OCRedFiles 2019-04-18
        :param args: not used
        :param options: not used
        :return: None
        """
        clean_result = OCRedFile.cleanup()
        for file in clean_result[0]:
            self.stdout.write(self.style.SUCCESS('File "%s" removed' % file))
        for pdf in clean_result[1]:
            self.stdout.write(self.style.SUCCESS('PDF "%s" removed' % pdf))
        self.stdout.write(self.style.SUCCESS('------'))
        self.stdout.write(self.style.SUCCESS('Total files removed: "%s"' % len(clean_result[0])))
        self.stdout.write(self.style.SUCCESS('Total pdf removed: "%s"' % len(clean_result[1])))
