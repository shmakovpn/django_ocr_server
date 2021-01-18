#!/bin/bash

# Runs `sphinx build` when files in ./doc/source was changed, uses inotifywait for watching files changes
# Author: shmakovpn <shmakovpn@yandex.ru>
# Date: 2020-01-07

# Requirements:
# Ubuntu: inotify-tools
# Centos 8: inotify-tools (from epel repository)

SCRIPT_DIR="$(dirname $0)"
DOCS_SOURCE_DIR="${SCRIPT_DIR}/doc/source"

# Checking that a VIRTUALENV is activated, exit otherwise
if ! test "${VIRTUAL_ENV}" ; then
  echo "A virtualenv is not activated. \$VIRTUAL_ENV is null"
  exit 1
fi

# Checking that *inotifywait* is installed
if ! which inotifywait > /dev/null 2>&1 ; then
  echo "*inotifywait* is not installed. Install package *inotify-tools*."
  exit 1
fi

# `inotifywait -r -m -e modify -e move -e crate -e delete watching_dir` generates multiple events
# when a file was saved used vim or something else
# but we want to run `sphinx build` only once when a file was changed.
# Thus `while true` is used.
# inotifywait (without *-m* key) generates one event then stops,
# then makedoc.py runs `shpihx build`
# then next iteration of infinitive cicle `while true` starts `inotifywait -m` once again
while true; do
  inotifywait -r -e modify -e move -e create -e delete "${DOCS_SOURCE_DIR}" 2>/dev/null \
    && python "${SCRIPT_DIR}"/makedoc.py
done
