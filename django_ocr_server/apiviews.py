"""
django_ocr_server/apiviews.py
This file contains views for OCR Server based on Django REST API
"""
__author__ = "shmakovpn <shmakovpn@yandex.ru>"
__date__ = "2019-03-19"

import os
import mimetypes
from django.urls import reverse_lazy

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.http import http_date
from django.views.static import was_modified_since
from django.http import HttpResponse, Http404, HttpResponseNotModified
from django.db.models import Q
from .models import *
from .serializers import *
from .exceptions import *
from django.conf import settings


class OcrApiView(APIView):
    """
    Parent view class for all OCR Server API views 2019-04-11
    """
    authentication_classes = (
        TokenAuthentication,
        SessionAuthentication,
    )
    permission_classes = (IsAuthenticated,)


class UploadFile(OcrApiView):
    """
    Uploads the 'file' to OCR Server,
    If 'file' already was uploaded to OCR Server,
    the view returns the information of the uploaded file
    and status_code 200.
    Unless OCR Server processing 'file' and returns
    information about the new OCRedFile 2019-03-19.
    """

    parser_classes = (MultiPartParser,)

    def post(self, request,):
        """
        Uploads the 'file' to OCR Server, \
        If 'file' already was uploaded to OCR Server, \
        the view returns the information of the uploaded file \
        and status_code 200. \
        Unless OCR Server processing 'file' and returns \
        information about the new OCRedFile 2019-03-19.
        :param request: rest framework request
        :return: rest framework response
        """
        if 'file' not in request.FILES:
            return Response({
                'error': True,
                'message': 'A file does not present',
            }, status=status.HTTP_400_BAD_REQUEST)
        ocred_file_serializer = OCRedFileSerializer(data={'file': request.FILES['file']})
        try:
            ocred_file_serializer.is_valid(raise_exception=True)
        except (Md5DuplicationError, Md5PdfDuplicationError) as e:
            ocred_file = OCRedFile.objects.get(Q(md5=e.md5) | Q(ocred_pdf_md5=e.md5))
            ocred_file_serializer = OCRedFileSerializer(ocred_file, many=False)
            data = ocred_file_serializer.data
            return Response({
                'error': False,
                'created': False,
                'code': e.code,
                'data': data
            }, status.HTTP_200_OK)
        except FileTypeError as e:
            return Response({
                'error': True,
                'code': e.code,
                'message': e.message,
                'file_type': e.file_type,
            }, status=status.HTTP_400_BAD_REQUEST)
        ocred_file_serializer.save()
        data = ocred_file_serializer.data
        return Response({
            'error': False,
            'created': True,
            'data': data
        }, status=status.HTTP_201_CREATED)


class OCRedFileList(OcrApiView):
    """
    Returns list of OCRedFile instances in JSON format 2019-03-20
    """
    def get(self, request, *args, **kwargs):
        """
        Returns a list of OCRedFile instances in JSON format 2019-03-24
        :param request: rest framework request
        :return: rest framework response
        """
        ocred_files = OCRedFile.objects.all()[:20]
        data = OCRedFileSerializer(ocred_files, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class Md5(OcrApiView):
    """
    Returns information about an already uploaded file, \
    or message that a file with md5=md5 or ocred_pdf_md5=md5 not found 2019-03-24
    """
    def get(self, request, md5=md5):
        """
        Returns information about an already uploaded file, \
        or message that a file with md5=md5 or ocred_pdf_md5=md5 not found 2019-03-24
        :param request: rest framework request
        :return: rest framework response
        """
        try:
            ocred_file = OCRedFile.objects.get(Q(md5=md5) | Q(ocred_pdf_md5=md5))
        except OCRedFile.DoesNotExist:
            return Response({
                'error': False,
                'exists': False,
            }, status=status.HTTP_204_NO_CONTENT)
        data = OCRedFileSerializer(ocred_file).data
        return Response({
            'error': False,
            'exists': True,
            'data': data,
        }, status=status.HTTP_200_OK)


class RemoveMd5(OcrApiView):
    """
    Removes an OCRedFile if it exists with md5=md5 or ocred_pdf_md5=md5, \
    or returns message that an OCRedFile with md5=md5 or ocred_pdf_md5 not found. 2019-03-24
    """
    def delete(self, request, md5=md5):
        """
        Removes an OCRedFile if it exists with md5=md5 or ocred_pdf_md5=md5, \
        or returns message that an OCRedFile with md5=md5 or ocred_pdf_md5 not found. 2019-03-24
        :param request: rest api framework request
        :param md5: The md5 of OCRedFile which will be deleted
        :return: rest framework response
        """
        try:
            ocred_file = OCRedFile.objects.get(Q(md5=md5) | Q(ocred_pdf_md5=md5))
        except OCRedFile.DoesNotExist:
            return Response({
                'error': False,
                'exists': False,
                'removed': False,
            }, status=status.HTTP_204_NO_CONTENT)
        ocred_file.delete()
        return Response({
            'error': False,
            'exists': True,
            'removed': True,
        }, status=status.HTTP_200_OK)


class RemoveAll(OcrApiView):
    """
    Removes all OCRedFiles 2019-03-24
    """
    def delete(self, request):
        """
        Removes all OCRedFiles 2019-03-24
        :param request: rest framework request
        :return: rest framework response
        """
        ocred_files = OCRedFile.objects.all()
        num_ocred_files = ocred_files.count()
        for ocred_file in ocred_files:
            ocred_file.delete()
        return Response({
            'error': False,
            'removed': True,
            'count': num_ocred_files,
        }, status=status.HTTP_200_OK)


class RemoveFileMd5(OcrApiView):
    """
    Removes the file from the instance of OCRedFile which has md5=md5 or ocred_pdf_md5=md5 2019-03-25
    """
    def delete(self, request, md5=md5):
        """
        Removes the file from the instance of OCRedFile which has md5=md5 or ocred_pdf_md5=md5 2019-03-25
        :param request: rest framework request
        :param md5: The md5 of OCRedFile whose file will be deleted
        :return: rest framework response
        """
        try:
            ocred_file = OCRedFile.objects.get(Q(md5=md5) | Q(ocred_pdf_md5=md5))
        except OCRedFile.DoesNotExist:
            return Response({
                'error': False,
                'exists': False,
                'removed': False,
            }, status=status.HTTP_204_NO_CONTENT)
        if not ocred_file.can_remove_file:
            return Response({
                'error': False,
                'exists': True,
                'can_remove_file': False,
                'removed': False,
            }, status=status.HTTP_204_NO_CONTENT)
        ocred_file.remove_file()
        return Response({
            'error': False,
            'exists': True,
            'removed': True,
        }, status=status.HTTP_200_OK)


class RemoveFileAll(OcrApiView):
    """
    Removes files from all of instances of OCRedFile 2019-03-25
    """
    def delete(self, request, ):
        """
        Removes files from all of instances of OCRedFile 2019-03-25
        :param request: rest framework request
        :return: rest framework response
        """
        old_counter = OCRedFile.Counters.num_removed_files
        ocred_files = OCRedFile.objects.all()
        for ocred_file in ocred_files:
            ocred_file.remove_file()
        return Response({
            'error': False,
            'removed': True,
            'count': OCRedFile.Counters.num_removed_files-old_counter,
        }, status=status.HTTP_200_OK)


class RemovePdfMd5(OcrApiView):
    """
    Removes the ocred_pdf from the instance of OCRedFile which has md5=md5 or ocred_pdf_md5=md5 2019-03-25
    """
    def delete(self, request, md5=md5):
        """
        Removes the ocred_pdf from the instance of OCRedFile which has md5=md5 or ocred_pdf_md5=md5 2019-03-25
        :param request: rest framework request
        :param md5: The md5 of OCRedFile whose ocred_pdf will be deleted
        :return: rest framework response
        """
        try:
            ocred_file = OCRedFile.objects.get(Q(md5=md5) | Q(ocred_pdf_md5=md5))
        except OCRedFile.DoesNotExist:
            return Response({
                'error': False,
                'exists': False,
                'removed': False,
            }, status=status.HTTP_204_NO_CONTENT)
        if not ocred_file.can_remove_pdf:
            return Response({
                'error': False,
                'exists': True,
                'can_remove_pdf': False,
                'removed': False,
            }, status=status.HTTP_204_NO_CONTENT)
        ocred_file.remove_pdf()
        return Response({
            'error': False,
            'exists': True,
            'removed': True,
        }, status=status.HTTP_200_OK)


class RemovePdfAll(OcrApiView):
    """
    Removes ocred_pdfs from all of instances of OCRedFile 2019-03-25
    """
    def delete(self, request, ):
        """
        Removes ocred_pdfs from all of instances of OCRedFile 2019-03-25
        :param request: rest framework request
        :return: rest framework response
        """
        old_counter = OCRedFile.Counters.num_removed_pdf
        ocred_files = OCRedFile.objects.all()
        for ocred_file in ocred_files:
            ocred_file.remove_pdf()
        return Response({
            'error': False,
            'removed': True,
            'count': OCRedFile.Counters.num_removed_pdf - old_counter,
        }, status=status.HTTP_200_OK)


class CreatePdfMd5(OcrApiView):
    """
    Creates ocred_pdf in the instance of OCRedFile whose md5=md5 or ocred_pdf_md5=md5 if it is possible 2019-03-25
    """
    def get(self, request, md5=md5):
        """
        Creates ocred_pdf in the instance of OCRedFile whose md5=md5 or ocred_pdf_md5=md5 if it is possible 2019-03-25
        :param request: rest framework request
        :param md5: the md5 of the instance of OCRedFile whose ocred_pdf will be created
        :return: rest framework response
        """
        try:
            ocred_file = OCRedFile.objects.get(Q(md5=md5) | Q(ocred_pdf_md5=md5))
        except OCRedFile.DoesNotExist:
            return Response({
                'error': False,
                'exists': False,
                'created': False,
            }, status=status.HTTP_204_NO_CONTENT)
        if not ocred_file.can_create_pdf:
            return Response({
                'error': False,
                'exists': True,
                'can_create_pdf': False,
                'created': False,
            }, status=status.HTTP_204_NO_CONTENT)
        ocred_file.create_pdf()
        return Response({
            'error': False,
            'exists': True,
            'created': True,
        }, status=status.HTTP_201_CREATED)


class CreatePdfAll(OcrApiView):
    """
    Creates ocred_pdf in all instances of OCRedFile where it is possible 2019-03-25
    """
    def get(self, request, ):
        """
        Creates ocred_pdf in all instances of OCRedFile where it is possible 2019-03-25
        :param request: rest framework request
        :return: rest framework response
        """
        old_counter = OCRedFile.Counters.num_created_pdf
        ocred_files = OCRedFile.objects.all()
        for ocred_file in ocred_files:
            ocred_file.create_pdf()
        return Response({
            'error': False,
            'created': True,
            'count': OCRedFile.Counters.num_created_pdf - old_counter,
        }, status=status.HTTP_200_OK)


class Clean(OcrApiView):
    """
    CleanUps folders for OCRedFile.files and OCRedFile.ocred_pdfs from files do not present in OCRedFiles 2019-04-12
    """
    def get(self, request, ):
        """
        Removes 'files' and 'ocred_pdfs' that are not related with any the OCRedFile 2019-04-13
        :param request: not used
        :return: rest framework response
        """
        removed_files, removed_pdfs = OCRedFile.cleanup()
        return Response({
            'removed files': removed_files,
            'removed files count': len(removed_files),
            'removed ocred_pdf': removed_pdfs,
            'remoced ocred_pdf count': len(removed_pdfs),
        })


class Ttl(OcrApiView):
    """
    Removes all instances of OCRedFile whose OCRedFile.uploaded+OCR_TTL lower current datetime
             if OCR_TTL does not 0, (NOTE: if OCR_TTL<0 all instances of OCRedFile will be removed, use only for tests).
    Removes all OCRedFile.files whose OCRedFile.uploaded+OCR_FILES_TTL lower current datetime
         if OCR_FILES_TTL does not 0,
         (NOTE: if OCR_FILES_TTL<0 all OCRedFile.files will be removed, use only for tests).
    Removes all OCRedFile.ocred_pdfs whose OCRedFile.uploaded+OCR_PDF_TTL lower current datetime
         if OCR_PDF_TTL does not 0,
         (NOTE: if OCR_PDF_TTL<0 all OCRedFile.ocred_pdfs will be removed, use only for tests). 2019-04-13
    """
    def get(self, request, ):
        """
        Removes all instances of OCRedFile whose OCRedFile.uploaded+OCR_TTL lower current datetime
             if OCR_TTL does not 0, (NOTE: if OCR_TTL<0 all instances of OCRedFile will be removed, use only for tests).
        Removes all OCRedFile.files whose OCRedFile.uploaded+OCR_FILES_TTL lower current datetime
             if OCR_FILES_TTL does not 0,
             (NOTE: if OCR_FILES_TTL<0 all OCRedFile.files will be removed, use only for tests).
        Removes all OCRedFile.ocred_pdfs whose OCRedFile.uploaded+OCR_PDF_TTL lower current datetime
             if OCR_PDF_TTL does not 0,
             (NOTE: if OCR_PDF_TTL<0 all OCRedFile.ocred_pdfs will be removed, use only for tests). 2019-04-13
        :param request: not used
        :return: rest framework response
        """
        counter, files_counter, pdf_counter = OCRedFile.ttl()
        return Response({
            'removed': counter,
            'files_removed': files_counter,
            'pdf_removed': pdf_counter,
        })


PWD = "%s/%s" % (settings.BASE_DIR, __package__)  # directory of the django-ocr-server/ocr application
UPLOAD_DIR = "%s/upload/" % PWD
PDF_DIR = "%s/pdf/" % PWD


class DownloadView(OcrApiView):
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
