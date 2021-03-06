"""
django_ocr_server/tests/utils/test_utils.py
+++++++++++++++++++++++++++++++++++++++++++

| Author: shmakovpn <shmakovpn@yandex.ru>
| Date: 2021-01-07
"""
from typing import List, Match, Optional, NewType, Type
from django.test import SimpleTestCase
from unittest.mock import patch
from io import StringIO
import django_ocr_server.utils as _u
import os
import pdftotext
import re

#: type hint for os.path
Path: Type = NewType('Path', str)


class TestUtils(SimpleTestCase):
    def test_read_binary_file(self):
        """Testing read_binary_file(path: str)"""
        tests_dir: Path = Path(os.path.dirname(os.path.dirname(__file__)))
        empty_file: Path = Path(os.path.join(tests_dir, 'empty_file.txt'))
        empty_content: bytes = _u.read_binary_file(empty_file)
        self.assertEqual(empty_content, bytes())
        folder: Path = os.path.join(tests_dir, 'some_dir')
        with self.assertRaisesMessage(
                IsADirectoryError, f"[Errno 21] Is a directory: '{folder}'"):
            _: bytes = _u.read_binary_file(folder)
        not_empty_file: Path = Path(
            os.path.join(tests_dir, 'not_empty_file.txt'))
        not_empty_content: bytes = _u.read_binary_file(not_empty_file)
        self.assertEqual(type(not_empty_content), bytes)
        self.assertEqual(not_empty_content, 'content\n'.encode())
        no_file: Path = Path(os.path.join(tests_dir, 'no_file.txt'))
        with self.assertRaisesMessage(
                FileNotFoundError,
                f"[Errno 2] No such file or directory: '{no_file}'"):
            _: bytes = _u.read_binary_file(no_file)

    def test_omp_thread_limit(self):
        """Testing that the environment variable OMP_THREAD_LIMIT equeals to '1' """
        self.assertEqual(os.environ['OMP_THREAD_LIMIT'], '1')

    def test_md5(self):
        """Testing md5(content: bytes)"""
        EMPTY_MD5: str = 'd41d8cd98f00b204e9800998ecf8427e'
        empty_md5: str = _u.md5(''.encode())
        self.assertEqual(empty_md5, EMPTY_MD5)
        NOT_EMPTY_MD5: str = 'f75b8179e4bbe7e2b4a074dcef62de95'
        not_epmty_md5: str = _u.md5('content\n'.encode())
        self.assertEqual(not_epmty_md5, NOT_EMPTY_MD5)

    def test_pdf2text(self):
        """Testing pdf2text(pdf_content: bytes)"""
        tests_dir: Path = Path(os.path.dirname(os.path.dirname(__file__)))
        pdf_notext: Path = Path(os.path.join(tests_dir, 'test_eng_notext.pdf'))
        pdf_notext_content: bytes = _u.read_binary_file(pdf_notext)
        pdf_notext_decoded: str = _u.pdf2text(pdf_notext_content)
        self.assertEqual(pdf_notext_decoded, '')
        pdf_withtext: Path = Path(
            os.path.join(tests_dir, 'the_pdf_withtext.pdf'))
        pdf_withtext_content: bytes = _u.read_binary_file(pdf_withtext)
        pdf_withtext_decoded: str = _u.pdf2text(pdf_withtext_content)
        self.assertEqual(pdf_withtext_decoded, 'The test if pdf with text')
        not_pdf: Path = Path(os.path.join(tests_dir, 'test_eng.png'))
        not_pdf_content: bytes = _u.read_binary_file(not_pdf)
        with self.assertRaisesMessage(pdftotext.Error,
                                      f'poppler error creating document'):
            _: str = _u.pdf2text(not_pdf_content)

    def test_date_pattern(self):
        """Testing DATE_PATTERN: Pattern"""
        date_string: str = '2021-01-11 something else'
        self.assertEqual(_u.DATE_PATTERN.sub(r'\2\3\4', date_string),
                         '20210111 something else')

    def test_remove_date_hyphens(self):
        """Testing removeDateHyphens(date_string: str)"""
        date_string: str = '2021-01-11 something else'
        self.assertEqual(_u.removeDateHyphens(date_string),
                         '20210111 something else')
        twice_as_date: str = "20190311033852-00'00'"
        self.assertEqual(_u.removeDateHyphens(twice_as_date), twice_as_date)

    def test_parse_pdf_datetime(self):
        """Testing parse_pdf_datetime(pdf_datetime: str)"""
        deming_dt: str = "D:20190311033852+00'00'"
        self.assertEqual(_u.parse_pdf_datetime(deming_dt),
                         '2019-03-11 03:38:52+0000')
        shmakovpn_dt: str = "D:20190412074856+03'00'"
        self.assertEqual(_u.parse_pdf_datetime(shmakovpn_dt),
                         '2019-04-12 07:48:56+0300')
        test_eng_notext_dt1: str = "2019-03-17T09:52:26+07:00"
        self.assertEqual(_u.parse_pdf_datetime(test_eng_notext_dt1),
                         '2019-03-17 09:52:26+0700')
        test_eng_notext_dt2: str = "D:20190317095226+07'00'"
        self.assertEqual(_u.parse_pdf_datetime(test_eng_notext_dt2),
                         '2019-03-17 09:52:26+0700')
        test_eng_dt: str = "D:20190310075751Z00'00'"
        self.assertEqual(_u.parse_pdf_datetime(test_eng_dt),
                         '2019-03-10 07:57:51+0000')
        the_pdf_withtext_dt: str = "D:20190317034557Z00'00'"
        self.assertEqual(_u.parse_pdf_datetime(the_pdf_withtext_dt),
                         '2019-03-17 03:45:57+0000')
        dt = '2020-01-10 17:57:31'
        self.assertEqual(_u.parse_pdf_datetime(dt), '2020-01-10 17:57:31')
        _deming_dt: str = "D:20190311033852-00'00'"
        self.assertEqual(_u.parse_pdf_datetime(_deming_dt),
                         '2019-03-11 03:38:52-0000')
        _shmakovpn_dt: str = "D:20190412074856-03'00'"
        self.assertEqual(_u.parse_pdf_datetime(_shmakovpn_dt),
                         '2019-04-12 07:48:56-0300')
        _test_eng_notext_dt1: str = "2019-03-17T09:52:26-07:00"
        self.assertEqual(_u.parse_pdf_datetime(_test_eng_notext_dt1),
                         '2019-03-17 09:52:26-0700')
        _test_eng_notext_dt2: str = "D:20190317095226-07'00'"
        self.assertEqual(_u.parse_pdf_datetime(_test_eng_notext_dt2),
                         '2019-03-17 09:52:26-0700')
        _test_eng_dt: str = "D:20190310075751-Z00'00'"
        self.assertEqual(_u.parse_pdf_datetime(_test_eng_dt),
                         '2019-03-10 07:57:51-0000')
        _the_pdf_withtext_dt: str = "D:20190317034557-Z00'00'"
        self.assertEqual(_u.parse_pdf_datetime(_the_pdf_withtext_dt),
                         '2019-03-17 03:45:57-0000')
        not_datetime: str = 'not datetime'

        with patch('sys.stdout', new_callable=StringIO) as patched_stdout:
            fake_datetime: str = _u.parse_pdf_datetime(not_datetime)
            stdout_value: str = patched_stdout.getvalue()
            self.assertEqual(
                stdout_value,
                "could not parse pdf_datetime: 'notdatetime', using now() instead\n"
            )
            match_fake: Optional[Match] = re.search(
                r'^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d', fake_datetime)
            self.assertIsNotNone(match_fake)

    def test_pdf_info_class(self):
        """Testing class PdfInfo"""
        pdf_info: _u.PdfInfo = _u.PdfInfo()
        self.assertEqual(pdf_info.author, '')
        self.assertEqual(pdf_info.creation_date, '')
        self.assertEqual(pdf_info.creator, '')
        self.assertEqual(pdf_info.mod_date, '')
        self.assertEqual(pdf_info.producer, '')
        self.assertEqual(pdf_info.title, '')
        self.assertEqual(pdf_info.num_pages, 0)
        self.assertEqual(str(pdf_info), f"PdfInfo("\
                + f"author='', "\
                + f"creation_date='', "\
                + f"creator='', "\
                + f"mod_date='', "\
                + f"producer='', "\
                + f"title='', "\
                + f"num_pages=0"\
                + f")")

    def test_pypdf_info_to_pdf_info(self):
        """Testing pypdf_inof_to_pdf_info(pypdf_info: PyPDF2.pdf.DocumentInformation)"""
        pdf_info: _u.PdfInfo = _u.pypdf_info_to_pdf_info({
            '/Author': 'author',
            '/CreationDate': "D:20190412074856+03'00'",
            '/Creator': 'creator',
            '/ModDate': "D:20200412074856+03'00'",
            '/Producer': 'producer',
            '/Title': 'title'
        })
        self.assertEqual(pdf_info.author, 'author')
        self.assertEqual(pdf_info.creation_date, '2019-04-12 07:48:56+0300')
        self.assertEqual(pdf_info.creator, 'creator')
        self.assertEqual(pdf_info.mod_date, '2020-04-12 07:48:56+0300')
        self.assertEqual(pdf_info.producer, 'producer')
        self.assertEqual(pdf_info.title, 'title')
        self.assertEqual(pdf_info.num_pages, 0)

    def test_get_pdf_info(self):
        """Testing get_pdf_info(pdf_content: bytes)"""
        tests_dir: Path = Path(os.path.dirname(os.path.dirname(__file__)))
        test_eng_pdf: Path = Path(os.path.join(tests_dir, 'test_eng.pdf'))
        test_eng_pdf_content: bytes = _u.read_binary_file(test_eng_pdf)
        test_eng_pdf_info: _u.PdfInfo = _u.get_pdf_info(test_eng_pdf_content)
        self.assertEqual(test_eng_pdf_info.author, '')
        self.assertEqual(test_eng_pdf_info.creation_date,
                         '2019-03-10 07:57:51+0000')
        self.assertEqual(test_eng_pdf_info.creator, '')
        self.assertEqual(test_eng_pdf_info.mod_date, '')
        self.assertEqual(test_eng_pdf_info.producer, 'Tesseract 4.0.0-beta.1')
        self.assertEqual(test_eng_pdf_info.title, '')
        self.assertEqual(test_eng_pdf_info.num_pages, 1)

        with patch('sys.stdout', new_callable=StringIO) as patched_stdout:
            not_pdf_info: _u.PdfInfo = _u.get_pdf_info(bytes())
            stdout_value: str = patched_stdout.getvalue()
            self.assertEqual(
                stdout_value,
                "PyPDF2.PdfFileReader exception: Cannot read an empty file\n")
            self.assertEqual(not_pdf_info.author, '')
            self.assertEqual(not_pdf_info.creation_date, '')
            self.assertEqual(not_pdf_info.creator, '')
            self.assertEqual(not_pdf_info.mod_date, '')
            self.assertEqual(not_pdf_info.producer, '')
            self.assertEqual(not_pdf_info.title, '')
            self.assertEqual(not_pdf_info.num_pages, 0)

    def test_cmd_stdin(self):
        """The testing cmd_stdin(args: List[str], stdin: bytes)"""
        cmd: List[str] = ['cat', '-']
        stdin: bytes = 'hello'.encode()
        result: str = _u.cmd_stdin(cmd, stdin).decode()
        self.assertEqual(result, 'hello')

        not_cmd: List[str] = ['nocmdabracadabra']
        with self.assertRaisesMessage(
                FileNotFoundError,
                f"[Errno 2] No such file or directory: '{not_cmd[0]}'"):
            _: str = _u.cmd_stdin(not_cmd, stdin=stdin).decode()

    def test_tesseract_strarg(self):
        """The testing TESSERACT_STRARG"""
        tesseract_lang: str = _u.get_tesseract_lang()
        tesseract_strargs: List[str] = _u.TESSERACT_STRARG
        self.assertEqual(tesseract_strargs[0], 'tesseract')
        self.assertEqual(tesseract_strargs[1], '-l')
        self.assertEqual(tesseract_strargs[2], tesseract_lang)
        self.assertEqual(tesseract_strargs[3], '-')
        self.assertEqual(tesseract_strargs[4], '-')
        self.assertEqual(len(tesseract_strargs), 5)

    def test_tesseract_pdfarg(self):
        """The testing TESSERACT_PDFARG"""
        tesseract_pdfarg: List[str] = _u.TESSERACT_PDFARG
        self.assertEqual(len(tesseract_pdfarg), 6)
        self.assertEqual(tesseract_pdfarg[5], 'pdf')

    def test_ocr_img2str(self):
        """The testing ocr_img2str(stdin: bytes)"""
        tests_dir: Path = Path(os.path.dirname(os.path.dirname(__file__)))
        test_eng_png: Path = Path(os.path.join(tests_dir, 'test_eng.png'))
        test_eng_png_content: bytes = _u.read_binary_file(test_eng_png)
        test_eng_ocred_text: str = _u.ocr_img2str(test_eng_png_content)
        self.assertTrue(test_eng_ocred_text,
                        'A some english text to test Tesseract')

    def test_ocr_img2pdf(self):
        """The testing ocr_img2pdf(stdin: bytes)"""
        tests_dir: Path = Path(os.path.dirname(os.path.dirname(__file__)))
        test_eng_png: Path = Path(os.path.join(tests_dir, 'test_eng.png'))
        test_eng_png_content: bytes = _u.read_binary_file(test_eng_png)
        test_eng_ocred_pdf: bytes = _u.ocr_img2pdf(test_eng_png_content)
        self.assertIsNotNone(test_eng_ocred_pdf)
        test_eng_ocred_pdf_text: str = _u.pdf2text(test_eng_ocred_pdf)
        self.assertEqual(test_eng_ocred_pdf_text,
                         'A some english text to test Tesseract')

    def test_pdf_need_ocr(self):
        """The testing ocr_need_pdf(pdf_text: str)"""
        self.assertTrue(_u.pdf_need_ocr(''))
        self.assertFalse(_u.pdf_need_ocr('привет'))
        self.assertFalse(_u.pdf_need_ocr('the boy and an appple'))
        self.assertTrue(_u.pdf_need_ocr('ablaldgh'))

    def test_get_ocr_pdf_cmd(self):
        """Testing get_ocr_pdf_cmd(filename: str)"""
        args: List[str] = _u.get_ocr_pdf_cmd('Filename')
        self.assertEqual(len(args), 8)
        self.assertEqual(args[0], 'ocrmypdf')
        self.assertEqual(args[1], '-l')
        self.assertEqual(args[2], _u.get_tesseract_lang())
        self.assertEqual(args[3], '-')
        self.assertEqual(args[4], 'Filename')
        self.assertEqual(args[5], '--force-ocr')
        self.assertEqual(args[6], '--sidecar')
        self.assertEqual(args[7], '-')

    def test_ocr_pdf(self):
        """Testing ocr_pdf(pdf_content, filename)"""
        tests_dir: Path = Path(os.path.dirname(os.path.dirname(__file__)))
