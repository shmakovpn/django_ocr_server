"""
django_ocr_server/widgets.py
"""
__author__ = 'shmakovpn shmakovpn@yandex.ru'
__date__ = '2019-04-16'


from django.forms.widgets import Widget
from django.template import loader
from django.utils.safestring import mark_safe
from django.urls import reverse
import os
from django.conf import settings
from . import settings as ocr_default_settings


class LinkWidget(Widget):
    """
    Base class for FileLink and PdfLink 2019-04-12
    """
    template_name = None

    def __init__(self, *args, **kwargs):
        """
        LinkWidget constructor, 2019-04-12
        :param args:
        :param kwargs:
        """
        super(LinkWidget, self).__init__(*args, **kwargs)


class FileLink(LinkWidget):
    """
    Widget of OCRedFile.file for using in admin 2019-04-12
    """
    template_name = 'django_ocr_server/forms/widgets/file_link.html'
    file_type = None

    def __init__(self,  *args, **kwargs):
        """
        FileLink widget constructor, initializes self.file_type, 2019-04-12
        :param args:
        :param kwargs:
        """
        if 'file_type' in kwargs:
            self.file_type = kwargs['file_type']
            kwargs.pop('file_type')
        super(FileLink, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super(FileLink, self).get_context(name, value, attrs)
        if getattr(settings, 'OCR_FILE_PREVIEW', ocr_default_settings.FILE_PREVIEW) and 'image' in self.file_type:
            context['widget']['file_preview'] = True
        if not getattr(settings, 'OCR_STORE_FILES', ocr_default_settings.STORE_FILES):
            context['widget']['store_files_disabled'] = True
        if 'store_files_disabled' in context['widget']['value']:
            context['widget']['file_missing'] = True
        elif 'file_removed' in context['widget']['value']:
            context['widget']['file_removed'] = True
        else:
            context['widget']['filename'] = os.path.basename(str(value))
            context['widget']['url'] = reverse(__package__ + ':download',
                                               kwargs={
                                                   'download_target': 'file', 'filename': context['widget']['filename']
                                               })
        return context


class PdfLink(LinkWidget):
    """
    Widget that shows a link to pdf file on the update model admin page.
    If pdf file exists the 'Remove PDF' button shows.
    If pdf file does not exists and it is possible to create it the 'Create PDF' button will shows
    """
    template_name = 'django_ocr_server/forms/widgets/pdf_link.html'
    can_create_pdf = None
    # no_source_file = False
    # ocred = False

    def __init__(self, *args, **kwargs):
        if 'can_create_pdf' in kwargs:
            self.can_create_pdf = kwargs['can_create_pdf']
            kwargs.pop('can_create_pdf')
        super(PdfLink, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        """
        This function creates context for rendering widget template.
        If pdf file exists the context['pdf_exists'] will be True
        If pdf file does not exist and it is possible to create it context['create_pdf_button'] will be True
        :param name:
        :param value:
        :param attrs:
        :return:
        """
        context = super(PdfLink, self).get_context(name, value, attrs)

        if not getattr(settings, 'OCR_STORE_PDF', ocr_default_settings.STORE_PDF):
            context['widget']['store_pdf_disabled'] = True
        if not context['widget']['value']:
            # value is empty, this means that OCRedFile.file is PDF and it has text,
            # or OCRedFile.file was ocred but OCRedFile.text is empty
            # In this case no need to show Remove button, and no need to show Create button
            return context
        if self.can_create_pdf:
            context['widget']['create_pdf_button'] = True
        if 'store_pdf_disabled' in context['widget']['value']:
            context['widget']['pdf_missing'] = True
        elif 'pdf_removed' in context['widget']['value']:
            context['widget']['pdf_removed'] = True
        else:
            context['widget']['filename'] = os.path.basename(str(value))
            context['widget']['url'] = reverse(__package__ + ':download',
                                               kwargs={
                                                   'download_target': 'pdf', 'filename': context['widget']['filename']
                                               })
            context['widget']['pdf_exists'] = True
        return context


class PdfInfo(Widget):
    template_name = 'django_ocr_server/forms/widgets/pdf_info.html'
    pdf_info = None

    def __init__(self, *args, **kwargs):
        if 'pdf_info' in kwargs:
            self.pdf_info = kwargs['pdf_info']
            kwargs.pop('pdf_info')
            super(PdfInfo, self).__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super(PdfInfo, self).get_context(name, value, attrs)
        context['pdf_info'] = self.pdf_info
        return context
