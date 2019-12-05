"""
django_ocr_server/management/commands/db_ping.py
Database ping test
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-12-05'


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from time import sleep

class Command(BaseCommand):
    """
    Performs a default database ping test. Prints result to stdout
    2019-12-05
    """
    help = """
    Performs a default database ping test. Prints result to stdout
    2019-12-05
    """

    def add_arguments(self, parser):
        """
        Configures command line arguments
        :param parser:
        :return:
        """
        parser.add_argument('wait_interval', nargs='?', type=int, help="Time to wait in second before ping database")

    def handle(self, *args, **options):
        """
        Performs a default database ping test. Prints result to stdout
        2019-12-05
        :param args: not used
        :param options: ['wait_interval']
        :return: None
        """
        if len(options):
            sleep(options['wait_interval'])
        if connection.is_usable():
            self.stdout.write(self.style.SUCCESS("database ping success"))
            exit(0)
        else:
            self.stderr.write(self.style.ERROR("database ping failed"))
            exit(1)
