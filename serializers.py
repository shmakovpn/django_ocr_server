"""
django_ocr_server/serializers/py
This file contains serializer for Django REST Framework
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-03-18'

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import *
from .utils import md5


class OCRedFileSerializer(serializers.ModelSerializer):
    """
    The OCRedFile model serializer 2019-03-18
    """
    def __init__(self, *args, **kwargs):
        """
        OCRedFileSerializer constructor
        :param args:
        :param kwargs:
        """
        super(OCRedFileSerializer, self).__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        """
        The OCRedFile model serializer validator 2019-03-20
        :param raise_exception:
        :return: boolean True if the data is valid
        """
        try:
            file_type = self.initial_data['file'].content_type
        except ValueError as e:
            if raise_exception:
                raise ValidationError(_('OCRedFileSerializer. The "content_type" of the "file" does not exist'))
            else:
                return False
        content = self.initial_data['file'].read()
        self.initial_data['file'].seek(0)
        if not OCRedFile.is_valid_file_type(file_type=file_type, raise_exception=raise_exception):
            return False
        md5_value = md5(content)
        print('OCRedFileSerializer.is_valid md5='+md5_value)
        if not OCRedFile.is_valid_ocr_md5(md5_value=md5_value, raise_exception=raise_exception):
            return False
        return super(OCRedFileSerializer, self).is_valid(raise_exception)

    @property
    def data(self):
        """
        This function returns filtered Serializer.data without 'file' and 'ocred_pdf' fields 2019-04-11
        :return: filtered Serializer.data dictionary without 'file' and 'ocred_pdf'
        """
        data = super(OCRedFileSerializer, self).data
        if 'file' in data:
            del data['file']
        if 'ocred_pdf' in data:
            del data['ocred_pdf']
        return data

    class Meta:
        model = OCRedFile
        fields = (
            'id',
            'md5',
            'file',
            'download_file',  # url for downloading OCRedFile.file if exists
            'file_type',
            'text',
            'uploaded',
            'ocred',
            'ocred_pdf',
            'download_ocred_pdf',  # url for downloading OCRedFile.ocred_pdf if exists
            'ocred_pdf_md5',
            'pdf_num_pages',
            'pdf_author',
            'pdf_creation_date',
            'pdf_creator',
            'pdf_mod_date',
            'pdf_producer',
            'pdf_title',
            'can_create_pdf',
            'can_remove_file',
            'can_remove_pdf',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'md5': {'read_only': True},
            'download_file': {'read_only': True},
            'file_type': {'read_only': True},
            'text': {'read_only': True},
            'uploaded': {'read_only': True},
            'ocred': {'read_only': True},
            'download_ocred_pdf': {'read_only': True},
            'ocred_pdf_md5': {'read_only': True},
            'pdf_num_pages': {'read_only': True},
            'pdf_author': {'read_only': True},
            'pdf_creation_date': {'read_only': True},
            'pdf_creator': {'read_only': True},
            'pdf_mod_date': {'read_only': True},
            'pdf_producer': {'read_only': True},
            'pdf_title': {'read_only': True},
            'can_create_pdf': {'read_only': True},
            'can_remove_file': {'read_only': True},
            'can_remove_pdf': {'read_only': True},
        }
