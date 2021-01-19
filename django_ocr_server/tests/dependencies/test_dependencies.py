"""
django_ocr_server/tests/dependencies/test_dependencies.py



Author: shmakovpn <shmakovpn@yandex.ru>
Date: 2021-01-11
"""
import re
from typing import List, Match, Optional
from django.test import SimpleTestCase
import subprocess


class TestDependencies(SimpleTestCase):
    def test_echo(self):
        """The testing that the *echo* command exists"""
        cmd: List[str] = ['echo', 'hello']
        try:
            popen: subprocess.Popen = subprocess.Popen(cmd,
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE,
                                                       stdin=subprocess.PIPE)
            stdout, stderr = popen.communicate()
            self.assertEqual(popen.returncode, 0)
            self.assertEqual(stdout.decode(), 'hello\n')
            self.assertEqual(stderr.decode(), '')
        except FileNotFoundError as e:
            self.assertIsNone(f'Testing the "echo" is exists was failed: {e}')

    def test_cat(self):
        """The testing the *cat* command exists"""
        cmd: List[str] = ['cat']
        popen: subprocess.Popen = subprocess.Popen(cmd,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   stdin=subprocess.PIPE)
        input: bytes = 'hello'.encode()
        stdout, stderr = popen.communicate(input=input)
        self.assertEqual(popen.returncode, 0)
        self.assertEqual(stdout.decode(), 'hello')
        self.assertEqual(stderr.decode(), '')

    def test_tesseract(self):
        """The testing that the *tesseract* command exists"""
        cmd: List[str] = ['tesseract', '--version']
        try:
            popen: subprocess.Popen = subprocess.Popen(cmd,
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE,
                                                       stdin=subprocess.PIPE)
            stdout, stderr = popen.communicate()
            self.assertEqual(popen.returncode, 0)
            self.assertEqual(stderr.decode(), '')
            match: Optional[Match] = re.search(r'^(tesseract)\s(\d+)',
                                               stdout.decode())
            version: int = int(match.group(2))
            self.assertTrue(version >= 4)
        except FileNotFoundError as e:
            self.assertIsNone(
                f'Testing the "tesseract" is exists was failed: {e}')

    def test_ocrmypdf(self):
        """The testing that the *ocrmypdf* command exists"""
        cmd: List[str] = ['ocrmypdf', '--version']
        try:
            popen: subprocess.Popen = subprocess.Popen(cmd,
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE,
                                                       stdin=subprocess.PIPE)
            stdout, stderr = popen.communicate()
            self.assertEqual(popen.returncode, 0)
            self.assertEqual(stderr.decode(), '')
            match: Optional[Match] = re.search(r'^(\d+)', stdout.decode())
            version: int = int(match.group(1))
            self.assertTrue(version >= 11)
        except FileNotFoundError as e:
            self.assertIsNone(
                f'Testing the "ocrmypdf" is exists was failed: {e}')

    def test_ghostscript(self):
        """The testing that the *gs* command exists"""
        cmd: List[str] = ['gs', '-version']
        try:
            popen: subprocess.Popen = subprocess.Popen(cmd,
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE,
                                                       stdin=subprocess.PIPE)
            stdout, stderr = popen.communicate()
            self.assertEqual(popen.returncode, 0)
            self.assertEqual(stderr.decode(), '')
            match: Optional[Match] = re.search(r'(Ghostscript)\s(\d+)',
                                               stdout.decode())
            version: int = int(match.group(2))
            self.assertTrue(version >= 9)
        except FileNotFoundError as e:
            self.assertIsNone(f'Testing the "gs" is exists was failed: {e}')