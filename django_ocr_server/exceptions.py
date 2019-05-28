"""
django_ocr_server/exceptions.py
This file contains exceptions of md5 duplications
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-03-21'


from django.core.exceptions import ValidationError


class Md5DuplicationError(ValidationError):
    """
    OCRedFile with the md5 already exists 2019-03-21
    """
    md5 = None
    MESSAGE = 'OCRedFile with the md5 already exists'
    CODE = 'md5_exists'

    def __init__(self, md5):
        """
        Creates Md5DuplicationError exception 2019-03-21
        :param md5:
        """
        self.md5 = md5
        super(Md5DuplicationError, self).__init__(message="{} '{}'".format(self.MESSAGE, self.md5), code=self.CODE)


class Md5PdfDuplicationError(Md5DuplicationError):
    """
    OCRedFile with the ocred_pdf_md5 already exists 2019-03-21
    """
    MESSAGE = 'OCRedFile with the ocred_pdf_md5 already exists'
    CODE = 'pdf_md5_exists'


class FileTypeError(ValidationError):
    """
    The uploaded file has a not allowed type of content 2019-03-21
    """
    file_type = None
    CODE = 'wrong_file_type'

    def __init__(self, file_type):
        """
        Creates FileTypeError exception 2019-03-21
        :param file_type:
        """
        self.file_type = file_type
        super(FileTypeError, self).__init__(
            message="The uploaded file has a not allowed type of content '{}'".format(self.file_type),
            code=self.CODE,
        )


class DoesNotSaved(ValueError):
    """
    Try to use the instance of OCRedFile that does not saved 2019-04-11
    """
    CODE = 'does_not_saved'

    def __init__(self):
        """
        Creates DoesNotSaved exception 2019-04-11
        """
        super(DoesNotSaved, self).__init__(
            message="Try to use the instance of OCRedFile that does not saved",
            code=self.CODE
        )
