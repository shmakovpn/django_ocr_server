"""
django_ocr_server/tests/dependencies/test_dependencies.py



Author: shmakovpn <shmakovpn@yandex.ru>
Date: 2021-01-11
"""
import re
from typing import List, Match, Optional
from django.test import TestCase
import subprocess


class TestDependencies(TestCase):
    def test_echo(self):
        """The testing that the *echo* command exists"""
        cmd: List[str] = ['echo', 'hello']
        popen: subprocess.Popen = subprocess.Popen(cmd,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   stdin=subprocess.PIPE)
        stdout, stderr = popen.communicate()
        self.assertEqual(popen.returncode, 0)
        self.assertEqual(stdout.decode(), 'hello\n')
        self.assertEqual(stderr.decode(), '')

    def test_cat(self):
        """The testing the *cat* command exists"""
        cmd: List[str] = ['cat']
        popen: subprocess.Popen = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        input: bytes = 'hello'.encode()
        stdout, stderr = popen.communicate(input=input)
        self.assertEqual(popen.returncode, 0)
        self.assertEqual(stdout.decode(), 'hello')
        self.assertEqual(stderr.decode(), '')

    def test_tesseract(self):
        """The testing the *tesseract* command exists"""
        cmd: List[str] = ['tesseract', '--version']
        popen: subprocess.Popen = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        stdout, stderr = popen.communicate()
        self.assertEqual(popen.returncode, 0)
        self.assertEqual(stderr.decode(), '')
        match: Optional[Match] = re.search(r'^(tesseract)\s(\d+)', stdout.decode())
        version: int = int(match.group(2))
        self.assertTrue(version>=4)