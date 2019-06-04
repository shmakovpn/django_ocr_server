"""
django_ocr_server/views.py
This file contains views of OCR Server,
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-03-19'


from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin


from django.conf import settings
import os





