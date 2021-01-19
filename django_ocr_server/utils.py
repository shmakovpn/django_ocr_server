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
from typing import List, Optional, Pattern, Union
import regex
from io import BytesIO  # for conversion a pdf content represented as bytes to an inmemory pdf file
import pdftotext  # needed to extraction text from pdf
import PyPDF2  # needed to get pdfInfo
from datetime import datetime
import django_ocr_server.settings as _s
from django.conf import settings


def get_store_files() -> bool:
    """Returns the mode of the storing of uploaded files"""
    return getattr(settings, 'OCR_STORE_FILES', _s.STORE_FILES)


def get_file_preview() -> bool:
    """Returns display mode of the preview of uploading images in the admin interface"""
    return getattr(settings, 'OCR_FILE_PREVIEW', _s.FILE_PREVIEW)


def get_tesseract_lang() -> str:
    """Returns the language string for Tesseract"""
    return getattr(settings, 'OCR_TESSERACT_LANG', _s.TESSERACT_LANG)


def get_store_pdf() -> bool:
    """Returns the mode of the storing of OCRed PDFs"""
    return getattr(settings, 'OCR_STORE_PDF', _s.STORE_PDF)


def get_files_upload_to() -> str:
    """Returns the path to store uploaded files"""
    return getattr(settings, 'OCR_FILES_UPLOAD_TO', _s.FILES_UPLOAD_TO)


def get_pdf_upload_to() -> str:
    """Return the path to store OCRed PDFs"""
    return getattr(settings, 'OCR_PDF_UPLOAD_TO', _s.PDF_UPLOAD_TO)


def get_ocr_files_ttl() -> int:
    """Return the time to live for uploaded files"""
    return getattr(settings, 'OCR_FILES_TTL', _s.FILES_TTL)


def read_binary_file(path: str) -> bytes:
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


def md5(content: bytes) -> str:
    """
    Generates md5 hash of content 2019-03-10
    :param content: a data for md5 generation
    :return: an md5 hash of a content
    """
    hash_md5 = hashlib.md5()
    hash_md5.update(content)
    return hash_md5.hexdigest()


def pdf2text(pdf_content: bytes) -> str:
    """
    It converts pdf_content as bytes to string 2019-03-10
    :param pdf_content: a content of a pdf file as bytes
    :return: text of pdf
    """
    pdfs: pdftotext.PDF = pdftotext.PDF(BytesIO(pdf_content))
    pdf_text: str = ''
    page: int
    for page in range(len(pdfs)):
        pdf_text += pdfs[page]
    return pdf_text


#: date regex pattern
DATE_PATTERN: Pattern = re.compile(r'((\d\d\d\d)-?(\d\d)-?(\d\d))')


def removeDateHyphens(date_string: str) -> str:
    """Removes hyphens from a string that contains a date"""
    return DATE_PATTERN.sub(r'\2\3\4', date_string, 1)


def parse_pdf_datetime(pdf_datetime: str) -> str:
    """
    This inner function parse a datetime from a string returned the PdfFileReader.getDocumentInfo()['/CreationDate'] or ['/ModDate'] 2019-03-11
    :param pdf_datetime: a string from the PdfFileReader.getDocumentInfo()['/CreationDate'] or ['/ModDate']
    :return: datetime of the pdf document creation date
    """
    pdf_datetime = pdf_datetime.strip('D')
    pdf_datetime = pdf_datetime.replace(':', '')
    pdf_datetime = pdf_datetime.replace('T', '')
    pdf_datetime = pdf_datetime.replace(' ', '')
    pdf_datetime = removeDateHyphens(pdf_datetime)
    if re.match(r'^\d{14}', pdf_datetime):
        year: str = pdf_datetime[0:4]
        month: str = pdf_datetime[4:6]
        day: str = pdf_datetime[6:8]
        hour: str = pdf_datetime[8:10]
        minute: str = pdf_datetime[10:12]
        second: str = pdf_datetime[12:14]
        pdf_datetime = pdf_datetime[14:]
        parsed_datetime: str = f'{year}-{month}-{day} {hour}:{minute}:{second}'
        pdf_datetime = pdf_datetime.strip('+')
        timezone_sign: str = '+'
        if re.match(r'^-', pdf_datetime):
            timezone_sign = '-'
            pdf_datetime = pdf_datetime.strip('-')
        pdf_datetime = pdf_datetime.strip('Z')
        if re.match(r'^\d\d', pdf_datetime):
            parsed_datetime = f'{parsed_datetime}{timezone_sign}{pdf_datetime[0:2]}'
            pdf_datetime = pdf_datetime[2:]
            pdf_datetime = pdf_datetime.strip("'")
            pdf_datetime = pdf_datetime.strip('"')
            if re.match(r'^\d\d', pdf_datetime):
                parsed_datetime = f'{parsed_datetime}{pdf_datetime[0:2]}'
        return parsed_datetime
    # otherwise
    print(
        f"could not parse pdf_datetime: '{pdf_datetime}', using now() instead")
    today = datetime.now()
    return f"{today.date()} {today.time()}"


class PdfInfo:
    """ An info of a PDF document """
    author: str = ''
    creation_date: str = ''
    creator: str = ''
    mod_date: str = ''
    producer: str = ''
    title: str = ''
    num_pages: int = 0

    def __str__(self) -> str:
        return f"PdfInfo(author='{self.author}', "\
            + f"creation_date='{self.creation_date}', "\
            + f"creator='{self.creator}', "\
            + f"mod_date='{self.mod_date}', "\
            + f"producer='{self.producer}', "\
            + f"title='{self.title}', "\
            + f"num_pages={self.num_pages})"


def pypdf_info_to_pdf_info(
        pypdf_info: PyPDF2.pdf.DocumentInformation) -> PdfInfo:
    """Converts PyPDF2.pdf.DocumentInformation to PdfInfo"""
    pdf_info: PdfInfo = PdfInfo()
    if '/Author' in pypdf_info:
        pdf_info.author = pypdf_info['/Author']
    if '/CreationDate' in pypdf_info:
        pdf_info.creation_date = parse_pdf_datetime(
            pypdf_info['/CreationDate'])
    if '/Creator' in pypdf_info:
        pdf_info.creator = pypdf_info['/Creator']
    if '/ModDate' in pypdf_info:
        pdf_info.mod_date = parse_pdf_datetime(pypdf_info['/ModDate'])
    if '/Producer' in pypdf_info:
        pdf_info.producer = pypdf_info['/Producer']
    if '/Title' in pypdf_info:
        pdf_info.title = pypdf_info['/Title']
    return pdf_info


def get_pdf_info(pdf_content: bytes) -> PdfInfo:
    """
    It extract pdfInfo from pdf 2019-03-11
    :param pdf_content: a content of a pdf file as bytes
    :return: pdf info as PdfInfo object
    """
    try:
        pdf_reader: PyPDF2.PdfFileReader = PyPDF2.PdfFileReader(
            BytesIO(pdf_content))
        pypdf_info: PyPDF2.pdf.DocumentInformation = pdf_reader.getDocumentInfo(
        )
        pdf_info: PdfInfo = pypdf_info_to_pdf_info(pypdf_info)
        pdf_info.num_pages = pdf_reader.numPages
        return pdf_info
    except Exception as e:
        print("PyPDF2.PdfFileReader exception: " + str(e))
    return PdfInfo(
    )  # reading PdfInfo was failed, return an empty (stub) object


def cmd_stdin(args: List[str], stdin: bytes) -> bytes:
    """
    Launches command using *args* and send *stdin* to its standard input.
    2019-03-10/2020-01-13
    """
    popen: subprocess.Popen = subprocess.Popen(args,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE)
    stdout, _ = popen.communicate(input=stdin)
    return stdout


TESSERACT_STRARG: List[str] = [
    'tesseract',
    '-l',
    get_tesseract_lang(),
    '-',
    '-',
]
TESSERACT_PDFARG: List[str] = TESSERACT_STRARG + ['pdf']


def ocr_img2str(stdin: bytes) -> str:
    """
    Recognize image from 'stdin' to string 2019-03-10 *4597#
    """
    return cmd_stdin(TESSERACT_STRARG, stdin).decode()


def ocr_img2pdf(stdin: bytes) -> bytes:
    """
    It recognize image from 'stdin' to pdf 2019-03-10
    :param stdin: image as bytes
    :return: content of recognuzed image as pdf (bytes)
    """
    return cmd_stdin(TESSERACT_PDFARG, stdin)


def pdf_need_ocr(pdf_text: str) -> bool:
    """
    This function analyses a text of a pdf document and determines whenever pdf document is need to be OCRed or not 2019-03-11
    :param pdf_text: a text of a pdf document
    :return: boolean. True if a pdf document need to be OCRed, False otherwise
    """
    if not len(pdf_text):
        return True  # a pdf document does not contain a text. It needs to be OCRed
    if regex.search(r'\p{IsCyrillic}', pdf_text):
        return False  # a pdf document contains cyrillic symbols. It does not need to be OCRed
    if re.search(r'the ', pdf_text, re.IGNORECASE):
        return False  # a pdf document contains the 'the' article. It needs to be OCRed
    return True  # a pdf document needs to be OCRed by default


def get_ocr_pdf_cmd(filename: str) -> List[str]:
    """
    Returns array of command line arguments,
    needed to recognize a pdf document using tesseract
    """
    args: List[str] = [
        'ocrmypdf',
        '-l',
        get_tesseract_lang(),
        '-',  # using STDIN
        filename,  #
        '--force-ocr',
        '--sidecar',
        '-'  # using STDOUT for sidecar
    ]
    return args


def ocr_pdf(pdf_content: bytes, filename: str) -> str:
    """
    This function OCRs a pdf document from the stdin,
    then saves searchable pdf to a disk if filename does not equal 'store_pdf_disabled',
    returns a recognized text 2019-04-11
    :param pdf_content: the content of document as bytes
    :param filename: the filename of a searchable pdf that will be created
    :return: a recognized text
    """
    args: List[str] = get_ocr_pdf_cmd(filename)
    process: subprocess.Popen = subprocess.Popen(args=args,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 stdin=subprocess.PIPE)
    stdout_data, stderr_data = process.communicate(input=pdf_content)
    if process.returncode:
        raise RuntimeError(
            f"Process '{' '.join(args)}' failed with code {process.returncode}: {stderr_data.decode()}"
        )
    return stdout_data.decode()
