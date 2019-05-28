"""
django_ocr_server/forms.py
Forms for the OCR Server
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-03-18'

from django import forms
from .models import *
from .widgets import *
from django.core.validators import ValidationError
from django.utils.translation import gettext as _
from .utils import md5


class OCRedFileViewForm(forms.ModelForm):
    """
    The form for view an OCRedFile 2019-03-18
    """
    pdf_info = forms.Field(label='PDF Info', required=False, )  # SEE __init__ below

    def __init__(self, *args, **kwargs):
        super(OCRedFileViewForm, self).__init__(*args, **kwargs)
        # init FileLink widget
        self.fields['file'].widget = FileLink(attrs={'target': '_blank'}, file_type=self.instance.file_type)
        # init PdfInfo widget
        pdf_info = {}
        pdf_info['pdf_num_pages'] = self.instance.pdf_num_pages
        pdf_info['pdf_author'] = self.instance.pdf_author
        pdf_info['pdf_creation_date'] = self.instance.pdf_creation_date
        pdf_info['pdf_creator'] = self.instance.pdf_creator
        pdf_info['pdf_mod_date'] = self.instance.pdf_mod_date
        pdf_info['pdf_producer'] = self.instance.pdf_producer
        pdf_info['pdf_title'] = self.instance.pdf_title
        self.fields['pdf_info'].widget = PdfInfo(attrs={}, pdf_info=pdf_info)
        # init PdfLink widget
        self.fields['ocred_pdf'].widget = PdfLink(attrs={'target': '_blank', 'readonly': True},
                                                  can_create_pdf=self.instance.can_create_pdf)

    class Meta:
        model = OCRedFile
        exclude = []
        widgets = {
            'md5': forms.TextInput(attrs={'size': 32, 'readonly': True}),
            # 'file' SEE __init__
            'file_type': forms.TextInput(attrs={'readonly': True}),
            'uploaded': forms.DateTimeInput(attrs={'readonly': True}),
            'ocred': forms.DateTimeInput(attrs={'readonly': True}),
            'text': forms.Textarea(attrs={'readonly': True, 'rows': 4}),
            # 'ocred_pdf': SEE __init__
            'ocred_pdf_md5': forms.TextInput(attrs={'size': 32, 'readonly': True}),
            'pdf_num_pages': forms.TextInput(attrs={'readonly': True}),
        }


class OCRedFileAddForm(forms.ModelForm):
    """
    The form for uploading file for OCR 2019-03-18
    """
    def clean(self):
        """
        The clean for add OCRedFile form. Checks that a md5 sum of a uploaded file does not already
         exist in the OCRedFile.md5 field or in the OCRedFile.ocred_pdf_md5 field. Checks that uploaded file is an image
         or pdf 2019-03-18
        :return: a cleaned data dict
        """
        print('OCRedFileAddForm->clean')
        cleaned_data = super(OCRedFileAddForm, self).clean()
        file = self.files.get('file')
        if not file:
            raise ValidationError(_('A file does not present'),
                                  code='invalid')
        cleaned_data['file_type'] = file.content_type
        OCRedFile.is_valid_file_type(file_type=cleaned_data['file_type'], raise_exception=True)
        content = file.read()
        file.seek(0)
        md5_txt = md5(content)
        print('OCRedFileAddForm->clean md5='+md5_txt)
        OCRedFile.is_valid_ocr_md5(md5_value=md5_txt, raise_exception=True)
        cleaned_data['md5'] = md5_txt
        return cleaned_data

    class Meta:
        model = OCRedFile
        exclude = ['uploaded', 'ocred', ]
        widgets = {
            'md5': forms.HiddenInput(),
            # 'file':
            'file_type': forms.HiddenInput(),
            'ocred': forms.HiddenInput(),
            'text': forms.HiddenInput(),
            'ocred_pdf': forms.HiddenInput(),
            'ocred_pdf_md5': forms.HiddenInput(),
            'pdf_num_pages': forms.HiddenInput(),
            'pdf_info': forms.HiddenInput(),
        }
        labels = {
            'file': 'File to upload',
        }


