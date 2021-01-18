"""
makedoc.py

Generates the documentation of django_ocr_server

Usage:

.. code-block:: bash

 python makedoc.py

Author: shmakovpn <shmakovpn@yandex.ru>
Date: 2020-01-13
"""
import os
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))


def run_sphinx() -> None:
    docs_dir: str = os.path.join(SCRIPT_DIR, 'doc')
    docs_source_dir: str = os.path.join(docs_dir, 'source')
    build_dir: str = os.path.join(docs_dir, 'build')
    html_dir: str = os.path.join(build_dir, 'html')
    cmd: str = f'sphinx-build -b html "{docs_source_dir}" "{html_dir}"'
    os.system(cmd)
    print('__END__')


if __name__ == '__main__':
    run_sphinx()
