"""
django_ocr_server/views.py
This file contains views of OCR Server,
"""
__author__ = 'shmakovpn <shmakovpn@yandex.ru>'
__date__ = '2019-03-19'


from django.views.generic import View
from django.views.static import was_modified_since
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import http_date
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, HttpResponseNotModified
from django.conf import settings
import os
import mimetypes


PWD = "%s/%s" % (settings.BASE_DIR, __package__)  # directory of the django-ocr-server/ocr application
UPLOAD_DIR = "%s/upload/" % PWD
PDF_DIR = "%s/pdf/" % PWD


class DownloadView(LoginRequiredMixin, View):
    """
    View for downloading OCRedFile.file or OCRedFile.ocred_pdf 2019-04-09
    """
    login_url = reverse_lazy('admin:index')

    def get(self, request, download_target, filename):
        """
        The view class for downloading files 2019-04-09
        :param request:
        :return: HttpResponse
        """
        if download_target == 'file':
            path = UPLOAD_DIR + filename
        else:
            path = PDF_DIR + filename
        if not os.path.isfile(path):
            raise Http404('"%s" does not exist' % path)
        stat = os.stat(path)
        content_type, encoding = mimetypes.guess_type(path)
        content_type = content_type or 'application/octet-stream'
        if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                                  stat.st_mtime, stat.st_size):
            return HttpResponseNotModified(content_type=content_type)
        response = HttpResponse(open(path, 'rb').read(), content_type=content_type)
        response['Last-Modified'] = http_date(stat.st_mtime)
        response['Content-Length'] = stat.st_size
        if encoding:
            response['Content-Encoding'] = encoding
        return response

