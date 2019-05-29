Installation
============
Linux Mint 19 (Ubuntu bionic)
-----------------------------
  Installing packages
   | $sudo apt install g++  # need to build pdftotext
   | $sudo apt install libpoppler-cpp-dev  # need to buid pdftotext
  Installing tesseract
   | $sudo apt install tesseract-ocr
   | $sudo apt install tesseract-ocr-rus  # install languages you want
  Installing python3.7
   | $sudo apt install python3.7
   | $sudo apt install python3.7-dev
  Installing pip
   $sudo apt install python-pip
  Installing virtualenv
   | $pip install --user virtualenv
   | $echo 'PATH=~/.local/bin:$PATH' >> ~/.bashrc
   | $source ~/.bashrc
  Installing virtualenvwrapper
   | $pip install --user setuptools
   | $pip install --user wheel
   | $pip install --user virtualenvwrapper
   | $echo 'source ~/.local/bin/virtualenvwrapper.sh' >> ~/.bashrc
   | $source ~/.bashrc
  Creating virtualenv for django_ocr_server
   $mkvirtualenv django_ocr_server -p /usr/bin/python3.7
  Inslalling django-ocr-server (on virtualenv django_ocr_server). It installs Django as a dependency
   $pip install django-ocr-server-1.0.tar.gz
  Create your Django project (on virtualenv django_ocr_server)
   $django-admin startproject ocr_server
  Go to project directory
   $cd ocr_server
  Edit ocr_server/settings.py
   Add applications to INSTALLED_APPS

   .. code-block::

    INSTALLED_APPS = [
     ...
     'rest_framework',
     'rest_framework.authtoken',
     'django_ocr_server',
     'rest_framework_swagger',
    ]


  Edit ocr_server/urls.py

  .. code-block::

   from django.contrib import admin
   from django.urls import path, include
   from rest_framework.documentation import include_docs_urls

   admin.site.site_header = 'OCR Server Administration'
   admin.site.site_title = 'Welcome to OCR Server Administration Portal'

   urlpatterns = [
       path('admin/', admin.site.urls, ),
       path('docs/', include_docs_urls(title='OCR Server API')),
       path('', include('django_ocr_server.urls'), ),
   ]

  Perform migrations (on virtualenv django_ocr_server)
   $python manage.py migrate
  Create superuser (on virtualenv django_ocr_server)
   $python manage.py createsuperuser
  Run server (on virtualenv django_ocr_server), than visit http://localhost:8000/
   $python manage.py runserver

Linux Mint 19 (Ubuntu bionic) automatic installation
-----------------------------------------------------
 Clone django_ocr_server from github
  $git clone https://github.com/shmakovpn/django_ocr_server.git
 Run the installation script using sudo
  $sudo {your_path}/django_ocr_server/install_ubuntu.sh

 The script creates OS user named 'django_ocr_server', installs all needed packages.
 Creates the virtual environment.
 It installs django_ocr_server (from PyPI by default, but you can create the package from
 cloned repository, see the topic 'Creation a distribution package' how to do this).
 Then it creates the django project named 'ocr_server' in the home directory of 'django_ocr_server' OS user.
 After the script changes settings.py and urls.py is placed in ~django_ocr_server/ocr_server/ocr_server/.
 Finally it applies migrations and creates the superuser named 'admin' with the same password 'admin'.

 Run server under OS user django_ocr_server, then change 'admin' password in the http://localhost:your_port/admin/ page.
  | $sudo su
  | $su django_ocr_server
  | cd ~/ocr_server
  | workon django_ocr_server
  | python manage.py runserver

Centos 7
--------
 Install epel repository
  $sudo yum install epel-release
 Install python 3.6
  | $sudo yum install python36
  | $sudo yum install python36-devel
 Install gcc
  | $sudo yum intall gcc
  | $sudo yum install gcc-c++
 Install dependencies
  $sudo yum install poppler-cpp-devel
 Install tesseract
  | $sudo yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/CentOS_7/
  | $sudo bash -c "echo 'gpgcheck=0' >> /etc/yum.repos.d/download.opensuse.org_repositories_home_Alexander_Pozdnyakov_CentOS_7*.repo"
  | $sudo yum update
  | $sudo yum install tesseract
  | $sudo yum install tesseract-langpack-rus  # install a language pack you need
 Install pip
  $sudo yum install python-pip
 Install virtualenv
  $sudo pip install virtualenv
 Create the virtual env for django_ocr_server
  $sudo virtualenv /var/www/ocr_server/venv -p /usr/bin/python36 --distribute
 Give rights to the project folder to your user
  $sudo chown -R {your_user} /var/www/ocr_server/
 Activate virtualenv
  $source /var/www/ocr_server/venv/bin/activate
 Install postgresql 11 (The Postgresql version 9.2 that is installing in Centos 7 by default returns an error when applying migrations )
  | $sudo rpm -Uvh https://yum.postgresql.org/11/redhat/rhel-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm
  | $sudo yum install postgresql11-server
  | $sudo yum install postgresql-devel
  | $sudo /usr/pgsql-11/bin/postgresql-11-setup initdb
  | Edit /var/lib/pgsql/11/data/pg_hba.conf
  |  host    all             all             127.0.0.1/32            md5
  |  host    all             all             ::1/128                 md5
  | $sudo systemctl enable postgresql-11
  | $sudo systemctl start postgresql-11
  | $sudo -u postgres psql
  | # create database django_ocr_server encoding utf8;
  | # create user django_ocr_server with password 'django_ocr_server';
  | # alter database django_ocr_server owner to django_ocr_server;
  | # alter user django_ocr_server createdb;  # if you want to run tests
  | # \q
  | pip install psycopg2  # (on virtualenv django_ocr_server)
 Create django project (on virtualenv django_ocr_server)
  | $cd /var/www/ocr_server
  | $django-admin startproject ocr_server .

 Edit ocr_server/settings.py
   Add applications to INSTALLED_APPS

   .. code-block::

    INSTALLED_APPS = [
     ...
     'rest_framework',
     'rest_framework.authtoken',
     'django_ocr_server',
     'rest_framework_swagger',
    ]

   Configure database connection

   .. code-block::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django_ocr_server',
            'USER': 'django_ocr_server',
            'PASSWORD': 'django_ocr_server',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

 Edit ocr_server/urls.py
  .. code-block::

   from django.contrib import admin
   from django.urls import path, include
   from rest_framework.documentation import include_docs_urls

   admin.site.site_header = 'OCR Server Administration'
   admin.site.site_title = 'Welcome to OCR Server Administration Portal'

   urlpatterns = [
       path('admin/', admin.site.urls, ),
       path('docs/', include_docs_urls(title='OCR Server API')),
       path('', include('django_ocr_server.urls'), ),
   ]

  Apply migrations (on virtualenv django_ocr_server)
   $python manage.py migrate
  Create superuser (on virtualenv django_ocr_server)
   $python manage.py createsuperuser
  Run server (on virtualenv django_ocr_server), than visit http://localhost:8000/
   $python manage.py runserver