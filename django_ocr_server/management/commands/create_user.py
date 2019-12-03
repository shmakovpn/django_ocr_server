"""
django_ocr_server/management/commands/create_user.py
Creates user with username=$1 and password=$2 if it does not already exist.
If the user with username=$1 is already exists changes its password=$2
Then generates a new Token for a the user
Returns the Token of created/updated user
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-12-03'


from django.core.management.base import BaseCommand
#from django_ocr_server.models import *


class Command(BaseCommand):
    """
    Creates user with username=$1 and password=$2 if it does not already exist.
    If the user with username=$1 is already exists changes its password=$2.
    Then generates a new Token for a the user.
    Returns the Token of created/updated user.
    2019-12-03
    """
    help = """
    Creates user with username=$1 and password=$2 if it does not already exist.
    If the user with username=$1 is already exists changes its password=$2.
    Then generates a new Token for a the user.
    Returns the Token of created/updated user.
    2019-12-03
    """

    def handle(self, *args, **options):
        """
        Creates user with username=$1 and password=$2 if it does not already exist.
        If the user with username=$1 is already exists changes its password=$2.
        Then generates a new Token for a the user.
        Returns the Token of created/updated user.
        2019-12-03
        :param args: an array of command line arguments. args
        :param options: not used
        :return: None
        """
        self.stdout.write('Hello')
        #self.stdout.write(self.style.SUCCESS('Total models removed: %s' % str(ttl_result[0])))
        #self.stdout.write(self.style.SUCCESS('Total files removed: %s' % str(ttl_result[1])))
        #self.stdout.write(self.style.SUCCESS('Total pdf removed: %s' % str(ttl_result[2])))