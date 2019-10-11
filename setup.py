"""
setup.py
django-ocr-server installation script
"""
__author__ = 'shmakovpn shmakovpn@yandex.ru'
__date__ = '2019-04-16'

from setuptools import setup, find_packages
import os
import django_ocr_server


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    long_description = readme.read()

setup(
    name='django-ocr-server',
    version=django_ocr_server.__version__,
    packages=find_packages(),
    author='shmakovpn',
    author_email='shmakovpn@yandex.ru',
    url='https://github.com/shmakovpn/django_ocr_server',
    download_url='https://github.com/shmakovpn/django_ocr_server/archive/'+django_ocr_server.__version__+'.zip',
    # desctiption='Django OCR Server',
    long_description=long_description,
    entry_points={
        'console_sripts': [],
    },
    install_requires=[
        'Django>=2.1.7',
        'regex>=2019.2.21',  # Used to determine that the text layer of the loaded PDF document was automatically created as a result of recognition of images by the scanner as text in English, while the images contain text in Cyrillic.
        'PyPDF2>=1.26.0',  # used to analizing PDF documents uploaded to the server
        'pdftotext>=2.1.1',  # used to extracting text from PDF documents uploaded to the server
        'pytesseract>=0.2.6',  # wrapper for tesseract-ocr https://github.com/tesseract-ocr/tesseract
        'ocrmypdf>=8.2.0',  # used for pdf recognition
        'djangorestframework>=3.9.2',  # used for API
        'beautifulsoup4>=4.7.1',  # used for tests
        'django-rest-swagger>=2.2.0'  # used for documentation
    ],
    include_package_data=True,
    # test_suite='tests',
)
