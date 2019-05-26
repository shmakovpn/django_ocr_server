"""
django_ocr_server/urls.py
OCR Server URL dispatcher
"""
__author__ = 'shmakopvn <shmakovpn@yandex.ru>'
__date__ = '2019-03-19'

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from django.urls.converters import register_converter
from django.urls import reverse_lazy
from .converters import Md5Converter, DonloadTargetConverter

# importing views
from .views import *
from .apiviews import *

register_converter(Md5Converter, 'md5')
register_converter(DonloadTargetConverter, 'download_target')

schema_view = get_swagger_view(title='OCR Server API')
app_name = __package__
urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:index'), permanent=False), name='root'),
    path('login/', views.obtain_auth_token, name='login'),
    path('upload/', UploadFile.as_view(), name='upload'),
    path('list/', OCRedFileList.as_view(), name='list'),
    path('remove/file/all/', RemoveFileAll.as_view(), name='remove_file_all'),
    path('remove/file/<md5:md5>/', RemoveFileMd5.as_view(), name='remove_file_md5'),
    path('remove/pdf/all/', RemovePdfAll.as_view(), name='remove_pdf_all'),
    path('remove/pdf/<md5:md5>/', RemovePdfMd5.as_view(), name='remove_pdf_md5'),
    path('create/pdf/all/', CreatePdfAll.as_view(), name='create_pdf_all'),
    path('create/pdf/<md5:md5>/', CreatePdfMd5.as_view(), name='create_pdf_md5'),
    path('remove/all/', RemoveAll.as_view(), name='remove_all'),
    path('remove/<md5:md5>/', RemoveMd5.as_view(), name='remove_md5'),
    path('<md5:md5>/', Md5.as_view(), name='md5'),
    path('swagger/', schema_view),
    path('download/<download_target:download_target>/<str:filename>/', DownloadView.as_view(), name='download'),
    path('clean/', Clean.as_view(), name='clean'),
    path('ttl/', Ttl.as_view(), name='ttl'),
]

