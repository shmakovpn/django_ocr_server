"""
django_ocr_server/management/commands/create_user.py
Creates user with username=$1 and password=$2 if it does not already exist.
If the user with username=$1 is already exists changes its password=$2
Then get or create auth_token for a the user
Returns the Token of created/updated user
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-12-03'


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    """
    Creates user with username=$1 and password=$2 if it does not already exist.
    If the user with username=$1 is already exists changes its password=$2.
    Then get or create auth_token for a the user.
    Returns the Token of created/updated user.
    2019-12-03
    """
    help = """
    Creates user with username=$1 and password=$2 if it does not already exist.
    If the user with username=$1 is already exists changes its password=$2.
    Then get or create auth_token for a the user.
    Returns the Token of created/updated user.
    2019-12-03
    """

    def add_arguments(self, parser):
        """
        Configures command line arguments
        :param parser:
        :return:
        """
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        """
        Creates user with username=$1 and password=$2 if it does not already exist.
        If the user with username=$1 is already exists changes its password=$2.
        Then get or create auth_token for a the user.
        Returns the Token of created/updated user.
        2019-12-03
        :param args: an array of command line arguments. args
        :param options: not used
        :return: None
        """
        username = options['username']
        password = options['password']
        user, created = User.objects.get_or_create(username=username)
        if not created:
            self.stderr.write(f"Warning: user with name '{username}' already exists. Change password")
        user.set_password(password)
        user.save()
        token, token_created = Token.objects.get_or_create(user=user)
        if not token_created:
            self.stderr.write(f"Info: Auth_token already exists")
        self.stdout.write(token.key)
