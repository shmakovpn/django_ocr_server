"""
django_ocr_server/models.py
+++++++++++++++++++++++++++

| Author: shmakovpn <shmakovpn@yandex.ru>
| 2019-04-16/2021-01-22
"""
import os
from io import BytesIO
from datetime import timedelta
# django imports
from django.db import models, connection
from django.utils import timezone
from django.urls import reverse
# django_ocr_server imports
from django_ocr_server.conf import ocr_settings
from django_ocr_server.utils import md5, pdf2text, ocr_img2pdf, PdfInfo, get_pdf_info, pdf_need_ocr, ocr_pdf, read_binary_file
from django_ocr_server.exceptions import *


def set_ocredfile_name(instance, filename=None):
    """
    This function returns a filename for OCRedFile.file 2019-03-18
    :param instance: an instance of the OCRedFile model
    :param filename: a name of a uploaded file
    :return: a filename for OCRedFile.file
    2019-10-22
    """
    if not ocr_settings.OCR_STORE_FILES:
        filename = ocr_settings.OCR_STORE_FILES_DISABLED_LABEL
    return os.path.join(ocr_settings.OCR_FILES_UPLOAD_TO, filename)


def set_pdffile_name(instance, filename=None):
    """
    This function returns a filename for OCRedFile.ocred_pdf 2019-03-18
    :param instance: an instance of the OCRedFile model
    :param filename: boolean if False 'store_pdf_disabled' will not use as ocred_pdf.file.name
    :return: a filename for OCRedFile.ocred_pdf
    2019-10-22
    """
    if not filename and not ocr_settings.OCR_STORE_PDF:
        filename = ocr_settings.OCR_STORE_PDF_DISABLED_LABEL
        if instance.md5:
            filename = f'{filename}_{instance.md5}'
    elif instance.md5:
        filename = instance.md5
    else:
        filename = instance.file.name
    return os.path.join(ocr_settings.OCR_PDF_UPLOAD_TO, f'{filename}.pdf')


# Create your models here.
class OCRedFile(models.Model):
    """
    The OCRedFile model class. Need to store information about uploaded file.
    """
    md5 = models.CharField(
        'md5',
        max_length=32,
        unique=True,
        blank=True,
    )
    file = models.FileField(
        'uploaded file',
        upload_to=set_ocredfile_name,
        null=True,
        max_length=500,
    )
    file_type = models.CharField(
        'content type',
        max_length=20,
        blank=True,
        null=True,
    )
    text = models.TextField('OCRed content', blank=True, null=True)
    uploaded = models.DateTimeField(
        'uploaded datetime',
        auto_now_add=True,
    )
    ocred = models.DateTimeField(
        'OCRed datetime',
        blank=True,
        null=True,
    )
    ocred_pdf = models.FileField('Searchable PDF',
                                 upload_to=set_pdffile_name,
                                 null=True,
                                 max_length=500)
    ocred_pdf_md5 = models.CharField("Searchable PDF's md5",
                                     max_length=32,
                                     null=True,
                                     blank=True)
    pdf_num_pages = models.IntegerField("PDF's num pages",
                                        null=True,
                                        blank=True)  #
    # from ocred_pdf info
    pdf_author = models.CharField("PDF's author",
                                  max_length=128,
                                  null=True,
                                  blank=True)
    pdf_creation_date = models.DateTimeField("PDF's creation date",
                                             blank=True,
                                             null=True)
    pdf_creator = models.CharField("PDF's creator",
                                   max_length=128,
                                   null=True,
                                   blank=True)
    pdf_mod_date = models.DateTimeField("PDF's mod date",
                                        blank=True,
                                        null=True)
    pdf_producer = models.CharField("PDF's producer",
                                    max_length=128,
                                    null=True,
                                    blank=True)
    pdf_title = models.CharField("PDF's title",
                                 max_length=128,
                                 null=True,
                                 blank=True)

    @staticmethod
    def is_valid_file_type(file_type, raise_exception=False):
        """
        This functions checks that file_type contains a correct value. 2019-03-20
        :param file_type:
        :param raise_exception:
        :return: boolean. True if file_type contains a correct value
        """
        if not file_type:
            if raise_exception:
                raise FileTypeError('The content type of the file is null')
            else:
                return False
        if file_type not in ocr_settings.OCR_ALLOWED_FILE_TYPES:
            if raise_exception:
                raise FileTypeError(file_type)
            else:
                return False
        return True

    @staticmethod
    def is_valid_ocr_md5(md5_value, raise_exception=False):
        """
        This function validates that the md5 does not already exist in the md5 field and ocred_pdf_md5.
        :param md5_value:
        :param raise_exception:
        :return: boolean. True if md5 does not already exist
        """
        if not md5_value:
            if raise_exception:
                raise ValidationError('The md5 value is empty')
            else:
                return False
        if OCRedFile.objects.filter(md5=md5_value).exists():
            if raise_exception:
                raise Md5DuplicationError(md5_value)
            else:
                return False
        if OCRedFile.objects.filter(ocred_pdf_md5=md5_value).exists():
            if raise_exception:
                raise Md5PdfDuplicationError(md5_value)
            else:
                return False
        return True

    def is_saved(self, raise_exception=True):
        """
        Returns True if the instance of OCRedFile is saved 2019-04-11
        :param raise_exception: boolean, if True DoesNotSaved exception will be raised
        :return: boolean True if the instance of OCRedFile is saved, False otherwise
        """
        if self.uploaded:
            return True
        elif raise_exception:
            raise DoesNotSaved
        return False

    @property
    def can_remove_file(self):
        """
        This function returns True if it is possible to remove self.file 2019-03-24
        :return: boolean True if it is possible to remove self.file
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        return os.path.isfile(self.file.path)

    @property
    def file_disabled(self):
        """
        This function returns True if OCRedFile.file does not exist because OCR_STORE_FILES is False 2019-04-11
        :return: boolean True if OCRedFile.file does not exist because OCR_STORE_FILES is False
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if self.file:
            return ocr_settings.OCR_STORE_FILES_DISABLED_LABEL in self.file.name
        return False

    @property
    def pdf_disabled(self):
        """
        This function returns True if OCRedFile.ocred_pdf does not exist because OCR_STORE_PDF is False 2019-04-11
        :return: boolean True if OCRedFile.ocred_pdf does not exist because OCR_STORE_PDF is False
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if self.ocred_pdf:
            return ocr_settings.OCR_STORE_PDF_DISABLED_LABEL in self.ocred_pdf.name
        return False

    @property
    def can_remove_pdf(self):
        """
        This function returns True if it is possible to remove self.ocred_pdf 2019-03-24
        :return: boolean True if it is possible to remove self.ocred_pdf
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if self.ocred_pdf:
            return os.path.isfile(self.ocred_pdf.path)
        return False

    @property
    def file_removed(self):
        """
        This function returns True if file was removed 2019-04-05
        :return: boolean True if file was removed
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        return ocr_settings.OCR_FILE_REMOVED_LABEL in self.file.name

    @property
    def pdf_removed(self):
        """
        This function returns True if ocred_pdf was removed 2019-04-05
        :return: boolean True if ocred_pdf was removed
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        return self.ocred_pdf and self.ocred_pdf.name and ocr_settings.OCR_PDF_REMOVED_LABEL in self.ocred_pdf.name

    def remove_file(self):
        """
        This function removes self.file.file from a disk if it exists,
        renames self.file.name to 'file_removed' and then saves the model instance
        :return: None
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)
        self.file.name = ocr_settings.OCR_FILE_REMOVED_LABEL
        # updating counters
        OCRedFile.Counters.num_removed_files += 1
        # parent method
        super(OCRedFile, self).save()

    def remove_pdf(self):
        """
        This function removes self.pdf.file from a disk if it exists,
        renames self.pdf.name to 'pdf_removed' and then saves the model instance
        :return: None
        """
        self.is_saved(
        )  # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        if self.ocred_pdf:
            if os.path.isfile(self.ocred_pdf.path):
                os.remove(self.ocred_pdf.path)
            self.ocred_pdf.name = ocr_settings.OCR_PDF_REMOVED_LABEL
            # updating counters
            OCRedFile.Counters.num_removed_pdf += 1
            # parent method
            super(OCRedFile, self).save()

    @property
    def is_pdf(self):
        """
        This function returns True if the uploaded file is pdf 2019-03-21
        :return: boolean True if the uploaded file is pdf
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        return 'pdf' in self.file_type

    @property
    def has_pdf_text(self):
        """
        This function returns True if the uploaded file is pdf and it contains text 2019-03-21
        :return: boolean True if the uploaded file is pdf and it contains text
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        return self.is_pdf and not self.ocred

    @property
    def can_create_pdf(self):
        """
        This function return True if it is possible to create searchable PDF 2019-03-24
        :return: boolean True if it is possible to create searchable PDF
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if not self.can_remove_file:
            # can not create pdf if OCRedFile.file does not exist
            return False
        if not self.ocred_pdf \
            or ocr_settings.OCR_PDF_REMOVED_LABEL in self.ocred_pdf.name \
            or ocr_settings.OCR_STORE_PDF_DISABLED_LABEL in self.ocred_pdf.name:
            # OCRedPDF does not exits
            # or it was removed
            # or it's storing was disabled
            if (not self.is_pdf or not self.has_pdf_text) and len(self.text):
                # OCRedFile.file is an image or it is pdf without text
                # and the result of ocring is not empty
                return True
        return False

    @property
    def download_file(self):
        """
        Returns url for download file if it exists 2019-04-11
        :return: url for download file if it exists, None otherwise
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if self.can_remove_file:
            return reverse(f'{__package__}:download',
                           kwargs={
                               'download_target': 'file',
                               'filename': os.path.basename(self.file.path)
                           })
        return None

    @property
    def download_ocred_pdf(self):
        """
        Returns url for download ocred_pdf if it exists 2019-04-11
        :return: url for download ocred_pdf if it exists, None otherwise
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if self.can_remove_pdf:
            return reverse(f'{__package__}:download',
                           kwargs={
                               'download_target': 'pdf',
                               'filename':
                               os.path.basename(self.ocred_pdf.path)
                           })
        return None

    def create_pdf(self, admin_obj=None, request=None):
        """
        This function creates self.pdf.file if it is possible 2019-03-13
        :admin_obj: An admin instance of the model
        :request: A request instance of the current http request
        :return: None
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        if self.can_create_pdf:
            content = self.file.file.read()
            self.file.file.seek(0)
            if 'image' in self.file_type:
                pdf_content = ocr_img2pdf(content)
                filename = set_pdffile_name(self, True)
                pdf = open(filename, 'wb')
                pdf.write(content)
                pdf.close()
                self.ocred_pdf.name = filename
                self.ocred_pdf_md5 = md5(pdf_content)
                OCRedFile.Counters.num_created_pdf += 1
                if admin_obj and request:
                    admin_obj.message_user(request, 'PDF created')
            elif 'pdf' in self.file_type:
                filename = set_pdffile_name(self, True)
                ocr_pdf(content, filename)
                self.ocred_pdf.name = filename
                self.ocred_pdf_md5 = md5(read_binary_file(filename))
                OCRedFile.Counters.num_created_pdf += 1
                if admin_obj and request:
                    admin_obj.message_user(request, 'PDF created')
            super(OCRedFile, self).save()

    def __str__(self):
        if ocr_settings.OCR_STORE_FILES_DISABLED_LABEL in self.file.name:
            return f'NO FILE "{self.md5}" "{self.uploaded}"'
        elif ocr_settings.OCR_FILE_REMOVED_LABEL in self.file.name:
            return f'REMOVED "{self.md5}" "{self.uploaded}"'
        return f'{self.file.path} "{self.md5}" "{self.uploaded}"'

    class Meta:
        verbose_name = 'OCRedFile'
        verbose_name_plural = 'OCRedFiles'

    def delete(self, *args, **kwargs):
        """
        This function deletes the instance of the model
        :param args:
        :param kwargs:
        :return: None
        """
        # checking that instance of OCRedFile is saved, raise DoesNotSaved exception otherwise
        self.is_saved()
        self.remove_file()
        self.remove_pdf()
        # updating counters
        OCRedFile.Counters.num_removed_instances += 1
        # parent method
        super(OCRedFile, self).delete(*args, **kwargs)

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        """
        This function save the instance of the model, or create it
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return: None
        """
        if self.is_saved(raise_exception=False):
            return
        if not self.file_type:
            self.file_type = self.file.file.content_type
        OCRedFile.is_valid_file_type(file_type=self.file_type,
                                     raise_exception=True)
        # read content of the 'file' field
        content = self.file.file.read()
        # return the reading pointer of the 'file' file to start position
        self.file.file.seek(0)
        # calculate md5 of 'file' field if if does not exist
        if not self.md5:
            self.md5 = md5(content)
        OCRedFile.is_valid_ocr_md5(md5_value=self.md5, raise_exception=True)
        # extract of ocr a content of the 'file' field if 'text' does not exist
        if not self.text:
            print(f'OCRedFile->save start OCR {self.md5}')
            ocr_started_datetime = timezone.now()
            if 'image' in self.file_type:
                pdf_content = ocr_img2pdf(content)
                self.text = pdf2text(pdf_content)
                if len(self.text):
                    # create ocred_pdf only for an image that contains a text
                    self.ocred_pdf_md5 = md5(pdf_content)
                    if ocr_settings.OCR_STORE_PDF:
                        self.ocred_pdf.save(set_pdffile_name(self),
                                            BytesIO(pdf_content), False)
                    else:
                        self.ocred_pdf.name = set_pdffile_name(self)
                self.ocred = timezone.now()
            elif 'pdf' in self.file_type:
                pdf_info: PdfInfo = get_pdf_info(content)
                self.pdf_num_pages = pdf_info.num_pages
                self.pdf_author = pdf_info.author
                if pdf_info.creation_date:
                    self.pdf_creation_date = pdf_info.creation_date
                self.pdf_creator = pdf_info.creator
                if pdf_info.mod_date:
                    self.pdf_mod_date = pdf_info.mod_date
                self.pdf_producer = pdf_info.producer
                self.pdf_title = pdf_info.title
                pdf_text = pdf2text(content)
                # check that loaded PDF file contains text
                if pdf_need_ocr(pdf_text):
                    print(
                        f'OCRedFile PDF OCR processing via OCRmyPDF {self.md5}'
                    )
                    pdf_filename = set_pdffile_name(self)
                    self.text = ocr_pdf(content, pdf_filename)
                    self.ocred = timezone.now(
                    )  # save datetime when uploaded PDF was ocred
                    if len(self.text):
                        # create ocred_pdf only for a pdf file that contains images with text
                        self.ocred_pdf.name = pdf_filename
                        self.ocred_pdf_md5 = md5(
                            read_binary_file(pdf_filename))
                        if not ocr_settings.OCR_STORE_PDF:
                            if os.path.isfile(pdf_filename):
                                os.remove(pdf_filename)
                    else:
                        # remove the PDF file created by ocr_pdf(content, pdf_filename)
                        if os.path.isfile(pdf_filename):
                            os.remove(pdf_filename)
                else:
                    print(
                        f'OCRedFile->save use text from loaded pdf {self.md5}')
                    self.text = pdf_text
            ocr_finished_datetime = timezone.now()
            ocr_duration: timedelta = ocr_finished_datetime - ocr_started_datetime
            print(
                f"OCRedFile->save finished OCR '{ocr_duration.seconds}.{ocr_duration.microseconds}' ms {self.md5}"
            )
        if not ocr_settings.OCR_STORE_FILES:
            os.remove(self.file.path)
        # update counters
        OCRedFile.Counters.num_created_instances += 1
        # checking database connection
        if not connection.is_usable():
            try:
                connection.connect()
            except Exception as e:
                print(f"database reconnection exception {self.md5}")
        # parent method
        super(OCRedFile, self).save(force_insert=False,
                                    force_update=False,
                                    using=None,
                                    update_fields=None)

    class Counters:
        """
        Counters of events 2019-03-25
        """
        num_removed_instances = 0  # number of removed instances of OCRedFile
        num_removed_files = 0  # number of removed files from instances of OCRedFile
        num_removed_pdf = 0  # number of removed ocred_pdfs from instances of OCRedFile
        num_created_pdf = 0  # number of created ocred_pdfs in instances of OCRedFile
        num_created_instances = 0  # number of created instances of OCRedFile

    @staticmethod
    def cleanup():
        """
        Removes 'files' and 'ocred_pdfs' that are not related with any the OCRedFile 2019-04-13
        :return: tuple ([removed_files tuple], [removed_pdf tuple],)
        """
        def remove_files(folder, files):
            """
            Removes all files in the 'folder' exclude 'files'
            :param folder: the path to the folder in which will be files removed
            :param files: files that will be excluded from removing
            :return: the list of path of removed files
            """
            removed = []
            for r, _, f in os.walk(folder):
                for file in f:
                    path = os.path.join(r, file)
                    if path not in files:
                        os.remove(path)
                        removed.append(path)
            return removed

        files = tuple(
            OCRedFile.objects\
                .exclude(file__in=ocr_settings.OCR_STORE_FILES_DISABLED_LABEL)\
                .exclude(file__in=ocr_settings.OCR_FILE_REMOVED_LABEL)\
                .values_list('file', flat=True),
        )
        removed_files = remove_files(ocr_settings.OCR_FILES_UPLOAD_TO, files)
        pdfs = tuple(
            OCRedFile.objects\
                .exclude(ocred_pdf__isnull=True)\
                .exclude(ocr_pdf__in=ocr_settings.OCR_STORE_PDF_DISABLED_LABEL)\
                .exclude(ocr_pdf__in=ocr_settings.OCR_PDF_REMOVED_LABEL)\
                .values_list('ocred_pdf', flat=True),
        )
        removed_pdfs = remove_files(ocr_settings.OCR_PDF_UPLOAD_TO, pdfs)
        return removed_files, removed_pdfs

    @staticmethod
    def ttl():
        """
        Removes all instances of OCRedFile whose OCRedFile.uploaded+OCR_TTL lower current datetime
             if OCR_TTL does not 0, (NOTE: if OCR_TTL<0 all instances of OCRedFile will be removed, use only for tests).
        Removes all OCRedFile.files whose OCRedFile.uploaded+OCR_FILES_TTL lower current datetime
             if OCR_FILES_TTL does not 0,
             (NOTE: if OCR_FILES_TTL<0 all OCRedFile.files will be removed, use only for tests).
        Removes all OCRedFile.ocred_pdfs whose OCRedFile.uploaded+OCR_PDF_TTL lower current datetime
             if OCR_PDF_TTL does not 0,
             (NOTE: if OCR_PDF_TTL<0 all OCRedFile.ocred_pdfs will be removed, use only for tests). 2019-04-13
        :return: (removed OCRedFiles counter, removed OCRedFile.files counter, removed OCRedFile.ocred_pdfs counter)
        """
        current_datetime = timezone.now()
        counter = 0
        files_counter = 0
        pdf_counter = 0
        if ocr_settings.OCR_TTL:
            removing_datetime = current_datetime - ocr_settings.OCR_TTL
            for ocred_file in OCRedFile.objects.filter(
                    uploaded__lt=removing_datetime):
                ocred_file.delete()
                counter += 1
        if ocr_settings.OCR_FILES_TTL != 0:
            files_removing_datetime = current_datetime - ocr_settings.OCR_FILES_TTL
            for ocred_file in OCRedFile.objects.filter(
                    uploaded__lt=files_removing_datetime):
                ocred_file.remove_file()
                files_counter += 1
        if ocr_settings.OCR_PDF_TTL != 0:
            pdf_removing_datetime = current_datetime - ocr_settings.OCR_PDF_TTL
            for ocred_file in OCRedFile.objects.filter(
                    uploaded__lt=pdf_removing_datetime):
                ocred_file.remove_pdf()
                pdf_counter += 1
        return counter, files_counter, pdf_counter
