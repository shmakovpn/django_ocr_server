"""
django_ocr_server/utils.py
this file provides functions and classes of 'OCR' application of 'OCR_Server'
common for the whole project.
"""
__author__ = "shmakovpn <shmakovpn@yandex.ru>"
__date__ = "03/11/2019"

import os
import re
import hashlib  # needed to md5 hash calculation
import subprocess  # needed to run tesseract
import re
import regex
from io import BytesIO  # for conversion a pdf content represented as bytes to an inmemory pdf file
import pdftotext  # needed to extraction text from pdf
import PyPDF2  # needed to get pdfInfo
# from datetime import datetime
from .settings import TESSERACT_LANG as default_tesseract_lang
from django.conf import settings


TESSERACT_LANG = getattr(settings, 'OCR_TESSERACT_LANG', default_tesseract_lang)


def read_binary_file(path):
    """
    It reads a file from the path 2019-03-10
    :param path: path to a file
    :return: contents of the file
    """
    f = open(path, 'rb')
    content = f.read()
    f.close()
    return content


os.environ['OMP_THREAD_LIMIT'] = '1'


def md5(content):
    """
    Generates md5 hash of content 2019-03-10
    :param content: a data for md5 generation
    :return: an md5 hash of a content
    """
    hash_md5 = hashlib.md5()
    hash_md5.update(content)
    return hash_md5.hexdigest()


def pdf2text(pdf_content):
    """
    It converts pdf_content as bytes to string 2019-03-10
    :param pdf_content: a content of a pdf file as bytes
    :return: text of pdf
    """
    pdfs = pdftotext.PDF(BytesIO(pdf_content))
    pdf_text = ''
    for page in range(len(pdfs)):
        pdf_text += pdfs[page]
    return pdf_text


def pdf_info(pdf_content):
    """
    It extract pdfInfo from pdf 2019-03-11
    :param pdf_content: a content of a pdf file as bytes
    :return: pdf info as {}-object
    """
    def parse_pdf_datetime(pdf_datetime_str):
        """
        This inner function parse a datetime from a string returned the PdfFileReader.getDocumentInfo()['/CreationDate'] or ['/ModDate'] 2019-03-11
        :param pdf_datetime_str: a string from the PdfFileReader.getDocumentInfo()['/CreationDate'] or ['/ModDate']
        :return: datetime of the pdf document creation date
        """
        # parse datetime like 'D:20190122061133Z'
        match_ob = re.match(r'^D\:(\d{14})Z$', pdf_datetime_str)
        if match_ob:
            pdf_datetime_str = match_ob[1]
        # parse datetime like 20190122061133
        if len(pdf_datetime_str) == 14:
            return pdf_datetime_str[0:4] \
                   + '-' + pdf_datetime_str[4:6] \
                   + '-' + pdf_datetime_str[6:8] \
                   + ' ' + pdf_datetime_str[8:10] \
                   + ':' + pdf_datetime_str[10:12] \
                   + ':' + pdf_datetime_str[12:14]
        # like 20190309053350+00'00'
        match_ob = re.match(r"^\d{14}\+\d{2}'\d{2}'", pdf_datetime_str)
        if match_ob:
            return pdf_datetime_str[0:4] \
                   + '-' + pdf_datetime_str[4:6] \
                   + '-' + pdf_datetime_str[6:8] \
                   + ' ' + pdf_datetime_str[8:10] \
                   + ':' + pdf_datetime_str[10:12] \
                   + ':' + pdf_datetime_str[12:14] \
                   + '+' + pdf_datetime_str[15:17] \
                   + pdf_datetime_str[18:20]
        # otherwise
        return pdf_datetime_str[2:6] \
               + '-' + pdf_datetime_str[6:8] \
               + '-' + pdf_datetime_str[8:10] \
               + ' ' + pdf_datetime_str[10:12] \
               + ':' + pdf_datetime_str[12:14] \
               + ':' + pdf_datetime_str[14:16] \
               + '+' + pdf_datetime_str[17:19]

    pdf_reader = PyPDF2.PdfFileReader(BytesIO(pdf_content))
    info = pdf_reader.getDocumentInfo()
    info_out = {'Author': '', 'CreationDate': '', 'Creator': '', 'ModDate': '', 'Producer': '', 'Title': '', 'numPages': pdf_reader.numPages}
    if '/Author' in info:
        info_out['Author'] = info['/Author']
    if '/CreationDate' in info:
        info_out['CreationDate'] = parse_pdf_datetime(info['/CreationDate'])
    if '/Creator' in info:
        info_out['Creator'] = info['/Creator']
    if '/ModDate' in info:
        info_out['ModDate'] = parse_pdf_datetime(info['/ModDate'])
    if '/Producer' in info:
        info_out['Producer'] = info['/Producer']
    if '/Title' in info:
        info_out['Title'] = info['/Title']
    return info_out


def cmd_stdin(cmd, stdin):
    """
    It launches command 'cmd' and sends it to the standard input 'stdin'. 2019-03-10
    :param cmd: an array of command e.g. ['tesseract','-l','rus+eng','-','-']
    :param stdin: a content to send to the standart input of a command
    :return: the decoded stdout of result of command
    """
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return popen.communicate(input=stdin)[0]


TESSERACT_STRARG = ['tesseract', '-l', TESSERACT_LANG, '-', '-', ]
TESSERACT_PDFARG = TESSERACT_STRARG+['pdf']


def ocr_img2str(stdin):
    """
    It recognize image from 'stdin' to string 2019-03-10
    :param stdin: image as bytes
    :return: content of recognized image as a string
    """
    return cmd_stdin(TESSERACT_STRARG, stdin).decode()


def ocr_img2pdf(stdin):
    """
    It recognize image from 'stdin' to pdf 2019-03-10
    :param stdin: image as bytes
    :return: content of recognuzed image as pdf (bytes)
    """
    return cmd_stdin(TESSERACT_PDFARG, stdin)


def pdf_need_ocr(pdf_text):
    """
    This function analyses a text of a pdf document and determines whenever pdf document is need to be OCRed or not 2019-03-11
    :param pdf_text: a text of a pdf document
    :return: boolean. True if a pdf document need to be OCRed, False otherwise
    """
    if not len(pdf_text):
        return True  # a pdf document does not contain a text. It needs to be OCRed
    if regex.search(r'\p{IsCyrillic}', pdf_text):
        return False  # a pdf document contains cyrillic symbols. It does not need to be OCRed
    if re.search(r'the', pdf_text, re.IGNORECASE):
        return False  # a pdf document contains the 'the' article. It needs to be OCRed
    return True  # a pdf document needs to be OCRed by default


def ocr_pdf(stdin, filename):
    """
    This function OCRs a pdf document from the stdin, \
    then saves searchable pdf to a disk if filename does not equal 'store_pdf_disabled', returns a recognized text 2019-04-11
    :param stdin: a pdf document as bytes
    :param filename: a filename of a searchable pdf that will be created
    :return: a recognized text
    """
    popen = subprocess.Popen([
        'ocrmypdf',
        '-l',
        TESSERACT_LANG,
        '-',  # using STDIN
        filename,  #
        '--force-ocr',
        '--sidecar',
        '-'  # using STDOUT for sidecar
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return popen.communicate(input=stdin)[0].decode()
