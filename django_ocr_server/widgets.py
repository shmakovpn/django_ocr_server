"""
django_ocr_server/widgets.py
++++++++++++++++++++++++++++

| Author: shmakovpn <shmakovpn@yandex.ru>
| 2019-04-16,2021-01-22
"""
from typing import Optional
import os
# django
from django.forms.widgets import Widget
from django.urls import reverse
from django.conf import settings
# django_ocr_settings
from django_ocr_server.conf import ocr_settings


class LinkWidget(Widget):
    """
    Base class for FileLink and PdfLink 2019-04-12
    """
    template_name: Optional[str] = None

    def __init__(self, *args, **kwargs) -> None:
        """
        LinkWidget constructor, 2019-04-12
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)


class FileLink(LinkWidget):
    """
    Widget of OCRedFile.file for using in the admin interface
    """
    template_name: str = 'django_ocr_server/forms/widgets/file_link.html'
    file_type: Optional[str] = None

    def __init__(self, *args, **kwargs) -> None:
        if 'file_type' in kwargs:
            self.file_type = kwargs.pop('file_type')
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super(FileLink, self).get_context(name, value, attrs)
        if ocr_settings.OCR_FILE_PREVIEW and 'image' in self.file_type:
            context['widget']['file_preview'] = True
        if not ocr_settings.OCR_STORE_FILES:
            context['widget']['store_files_disabled'] = True
        if ocr_settings.OCR_STORE_FILES_DISABLED_LABEL in context['widget'][
                'value']:
            context['widget']['file_missing'] = True
        elif ocr_settings.OCR_FILE_REMOVED_LABEL in context['widget']['value']:
            context['widget']['file_removed'] = True
        else:
            context['widget']['filename'] = os.path.basename(str(value))
            context['widget']['url'] = reverse(
                f'{__package__}:download',
                kwargs={
                    'download_target': 'file',
                    'filename': context['widget']['filename']
                })
        return context


class PdfLink(LinkWidget):
    """
    Widget that shows a link to pdf file on the update model admin page.
    If pdf file exists the 'Remove PDF' button shows.
    If pdf file does not exists and it is possible to create it the 'Create PDF' button will shows
    """
    template_name: str = 'django_ocr_server/forms/widgets/pdf_link.html'
    can_create_pdf: Optional[bool] = None

    def __init__(self, *args, **kwargs) -> None:
        if 'can_create_pdf' in kwargs:
            self.can_create_pdf = kwargs.pop('can_create_pdf')
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        """
        This function creates context for rendering widget template.
        If pdf file exists the context['pdf_exists'] will be True
        If pdf file does not exist and it is possible to create it context['create_pdf_button'] will be True
        """
        context = super().get_context(name, value, attrs)

        if not ocr_settings.OCR_STORE_PDF:
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
            context['widget']['url'] = reverse(
                f'{__package__}:download',
                kwargs={
                    'download_target': 'pdf',
                    'filename': context['widget']['filename']
                })
            context['widget']['pdf_exists'] = True
        return context


class PdfInfo(Widget):
    template_name: str = 'django_ocr_server/forms/widgets/pdf_info.html'
    pdf_info = None

    def __init__(self, *args, **kwargs):
        if 'pdf_info' in kwargs:
            self.pdf_info = kwargs.pop('pdf_info')
            super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super(PdfInfo, self).get_context(name, value, attrs)
        context['pdf_info'] = self.pdf_info
        return context
