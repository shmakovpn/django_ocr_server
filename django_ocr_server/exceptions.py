"""
django_ocr_server/exceptions.py
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-03-21/2021-01-06'

from typing import Optional, Pattern, List, Tuple, Match
import re
from django.core.exceptions import ValidationError


class Md5DuplicationError(ValidationError):
    """
    OCRedFile with the same md5 already exists 2019-03-21/2021-01-06
    """
    md5 = None
    MESSAGE = 'OCRedFile with the same md5 already exists'
    CODE = 'md5_exists'

    def __init__(self, md5: str):
        self.md5 = md5
        message: str = f"{self.MESSAGE} '{self.md5}'"
        super().__init__(message=message, code=self.CODE)


class Md5PdfDuplicationError(Md5DuplicationError):
    """
    OCRedFile with the same ocred_pdf_md5 already exists 2019-03-21/2021-01-06
    """
    MESSAGE = 'OCRedFile with the same ocred_pdf_md5 already exists'
    CODE = 'pdf_md5_exists'


class FileTypeError(ValidationError):
    """
    The uploaded file has a not allowed type of content 2019-03-21/2021-01-06
    """
    file_type: Optional[str] = None
    CODE = 'wrong_file_type'

    def __init__(self, file_type: str):
        self.file_type = file_type
        super().__init__(
            message="The uploaded file has a not allowed type of content '{}'".
            format(self.file_type),
            code=self.CODE,
        )


class DoesNotSaved(RuntimeError):
    """
    Error trying to use unsaved OCRedFile 2019-04-11/2021-01-06
    """
    def __init__(self):
        super().__init__(f"Trying to use unsaved OCRedFile")


class UnresolvedDependencyError(RuntimeError):
    """
    The execution was failed via unresolved dependency 2021-01-07
    """
    message: Optional[str] = None
    program_name: Optional[str] = None
    dependency_name: Optional[str] = None

    def __init__(self, message: str, program_name: str, dependency_name: str):
        self.message = message
        self.program_name = program_name
        self.dependency_name = dependency_name
        super().__init__(
            f"'{program_name}' was failed via unresolved dependency '{dependency_name}': {message}"
        )
