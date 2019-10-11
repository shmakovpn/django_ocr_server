#!/usr/bin/env bash
# run_shinx.sh generates documentation of django_ocr_server
# saves result as html at
# with the version set in django_ocr_server/__init__.py file in the __version__ variable
# to pypi.org project_folder/doc/build/html/index.html

# Author: shmakovpn <shmakovpn@yandex.ru>
# Date: 2019-10-11

SCRIPT_DIR=$(dirname $(readlink -f $0))  # directory of this script

sphinx-build -b html ${SCRIPT_DIR}/doc/source/ ${SCRIPT_DIR}/doc/build/html