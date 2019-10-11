#!/usr/bin/env bash
# upload_to_pypi.sh uploads the builded python package of django_ocr_server
# with the version set in django_ocr_server/__init__.py file in the __version__ variable
# to pypi.org

# Author: shmakovpn <shmakovpn@yandex.ru>
# Date: 2019-10-11

SCRIPT_DIR=$(dirname $(readlink -f $0))  # directory of this script
PACKAGE='django_ocr_server'

PACKAGE_INIT_FILE=${SCRIPT_DIR}/${PACKAGE}/__init__.py

if [[ ! -f ${PACKAGE_INIT_FILE} ]]; then
  echo "Error: init file '${PACKAGE_INIT_FILE}' does not exist"
  exit 1
fi

VERSION=$(cat "${PACKAGE_INIT_FILE}" | sed -re '/^__version__/!d; s/ //g; s/^__version__=//; s/#.*$//' -re "s/'//g")

if [[ -z ${VERSION} ]]; then
  echo "Error: could not get version from '${PACKAGE_INIT_FILE}'"
fi

echo "Info: got version '${VERSION}'"

PACKAGE_FILE="dist/$(echo ${PACKAGE} | sed -re 's/_/-/g')-${VERSION}.tar.gz"

if [[ ! -f ${PACKAGE_FILE} ]]; then
  echo "Error: package file '${PACKAGE_FILE}' does not exist"
  exit 1
fi

python -m twine upload "${PACKAGE_FILE}"
