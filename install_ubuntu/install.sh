#!/usr/bin/env bash

# cheks that pip package installed in user environment
search_pip() {
    echo $1 | grep $PROD > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        # looking for django-ocr-server
        pip freeze --all | grep $PROD > /dev/null 2>&1
    else
        # looking for another package
        pip freeze --all | grep -qi "^$1=" > /dev/null 2>&1
    fi
}


# installs a package using pip (sudo -H -u $USER pip install --user $1) 2019-04-24
# checks that the package successfully installed
install_pip() {
    search_pip $1
    if [ $? -ne 0 ]; then
        echo "INFO: '$1' is not installed. Installing"
        echo $1 | grep $PROD > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            #installing django-ocr-server
            pip install $1
        else
            #installing another pip package
            pip install --user $1
        fi
        search_pip $1
        if [ $? -ne 0 ]; then
            echo "Error. Could not install '$1'. Install it manually, then run this script again"
            exit 1
        fi
    else
        echo "INFO: '$1' is already installed"
    fi
}

# appends line $1 to $USER_HOME/.bashrc if the string does not exist 2019-04-23
append_bashrc() {
    #checking that the line $1 does not exist
    cat $HOME/.bashrc | grep -qi "^$1$" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "$1" >> $HOME/.bashrc
        echo "INFO: The line '$1' appended into '~/.bashrc'"
    else
        echo "INFO: The line '$1' already exists in '~/.bashrc'"
    fi
}

# checks that app $1 is in the django project settings file
is_app_in_django_settings() {
    # checking that the django project settings file exists
    if [ ! -f $SETTINGS_FILE ]; then
        echo "Error: The django project settings file '$SETTINGS_FILE' does not exist"
        exit 1
    fi
    cat $SETTINGS_FILE | grep -Pzo "INSTALLED_APPS\s?=\s?\[[\s\w\.,']*$1[\s\w\.,']*\]\n?" > /dev/null 2>&1
    # now $?=0 if app is in settings file
    # $? not 0 otherwise
}

# adds app $1 to the django project settings
add_app2django_settings() {
    is_app_in_django_settings "$1"
    if [ $? -ne 0 ]; then
        echo "Info. The app '$1' is not in the django project settings file '$SETTINGS_FILE'. Adding."
        sed -i -e '1h;2,$H;$!d;g' -re "s/(INSTALLED_APPS\s?=\s?\[[\n '._a-zA-Z,]*)/\1    '$1',\n/g" $SETTINGS_FILE
        # checking that app $1 successfully added to django project settings file
        is_app_in_django_settings $1
        if [ $? -ne 0 ]; then
            echo "Error. Could not add the app '$1' to the django project settings file '$SETTINGS_FILE'. Add it manually, then run this script again."
            exit 1
        else
            echo "Info. The app '$1' was successfully added to the django settings file '$SETTINGS_FILE'."
        fi
    else
        echo "Info. The app '$1' is already in the django project settings file '$SETTINGS_FILE'"
    fi
}

IMPORT_STRING=0  # The boolean flag, means that the url string is adding to the django project urls file is an import string

# checks that line is in the django project urls file
is_line_in_django_urls() {
    # checking that the django project urls file exists
    if [ ! -f $URLS_FILE ]; then
        echo "Error. The django project urls fie '$URLS_FILE' does not exist"
        exit 1
    fi
    echo "$1" | grep -iP "^from .+ import .+$" >  /dev/null 2>&1
    # check if $1 is an import string or is an url string
    if [ $? -eq 0 ]; then
        echo "Info. The url string='$1' is an import string"
        IMPORT_STRING=1
        cat $URLS_FILE | grep -i "^$1$" >  /dev/null 2>&1
    else
        echo "Info. The url string='$1' is not an import string"
        IMPORT_STRING=0
        ESCAPED_STRING=`echo $1 | sed -re "s/\(/\\\\\(/g" | sed -re "s/\)/\\\\\)/g"`
        GREP_REQ="urlpatterns\s?=\s?\[[\s\w\.,\(\)'=\/]*$ESCAPED_STRING[\s\w\.,\(\)'=\/]*\]\n?"
        cat $URLS_FILE | grep -Pzo "$GREP_REQ" > /dev/null 2>&1
    fi
    # return: $? will be not 0 if $1 does not exist in the $URLS_FILE
}

# adds string $1 to the django project urls file
add_str2django_urls() {
    is_line_in_django_urls "$1"
    # checking that string $1 does not exist in django project urls file
    if [ $? -ne 0 ]; then
        echo "Info. The url string='$1' does not exists in URLS_FILE='$URLS_FILE'"
        if [ $IMPORT_STRING -eq 1 ]; then
            echo "Info. Adding the url string='$1' as an import string"
            sed -i -re "s/^(urlpatterns)/$1\n\n\1/g" $URLS_FILE
            is_line_in_django_urls "$1"
            if [ $? -ne 0 ]; then
                echo "Error: Could not add the url string='$1' to the django project urls file '$URLS_FILE'. Add it manually, then run this script again."
                exit 1
            else
                echo "Info. The url string='$1' was successfully added to the django urls file '$URLS_FILE'."
            fi
        else
            echo "Info. Adding the url string='$1' as a path string"
            sed -i -e '1h;2,$H;$!d;g' -re "s@(urlpatterns\s?=\s?\[[\n '._a-zA-Z,()=\/]*)@\1    $1\n@g" $URLS_FILE
            is_line_in_django_urls "$1"
            if [ $? -ne 0 ]; then
                echo "Error: Could not add the url string='$1' to the django project urls file '$URLS_FILE'. Add it manually, then run this script again."
                exit 1
            else
                echo "Info. The url string='$1' was successfully added to the django urls file '$URLS_FILE'."
            fi
        fi
    else
        echo "Info. The url string='$1' already exists in URLS_FILE='$URLS_FILE'"
    fi
}


# installing setuptools
install_pip "setuptools"
# installing 'virtualenv' under user
install_pip "virtualenv"
# append_bashrc "export PATH=$HOME/.local/bin:$PATH"
append_bashrc "export PATH=$PATH"  # 2019-05-04
# installing 'wheel' under user
install_pip "wheel"
# installing 'virtualenvwrapper' under user
install_pip "virtualenvwrapper"
export VIRTUALENVWRAPPER_PYTHON=$(head -n 1 `which pip` | sed s/..//)
append_bashrc "VIRTUALENVWRAPPER_PYTHON=$VIRTUALENVWRAPPER_PYTHON"
append_bashrc ". $HOME/.local/bin/virtualenvwrapper.sh"
source $HOME/.local/bin/virtualenvwrapper.sh

# checking that django_ocr_server virtualenv exists
ls -alF $HOME/.virtualenvs/ | grep "$PACKAGE/\$" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # django_ocr_server virtualenv does not exist
    echo "Info: virtual environment '$PACKAGE' does not exit. Installing it."
    mkvirtualenv $PACKAGE -p /usr/bin/python3.7
    ls -alF $HOME/.virtualenvs/ | grep "$PACKAGE/\$" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error. Could not create virtual environment '$PACKAGE'. Create it manually and run this script once again."
        exit 1
    else
        echo "Info. The virtual environment '$PACKAGE' created successfully."
    fi
else
    # django_ocr_server virtualenv exists
    echo "Info: virtual environment '$PACKAGE' already exits. Working on it"
    workon $PACKAGE
fi

# checking that django-ocr-serer-{version}.tar.gz in $HOME folder
ls -alF $HOME | grep -e "$PROD.*\.tar.gz$" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    # django-ocr-server-{version}.tar.gz package was not found in $HOME directory, try to install it from PyPI
    echo "Info. The $PROD-{version}.tar.gz package was not found in '$HOME' directory, try to install it from PyPI"
    install_pip "$PROD"
else
    # The django-ocr-server package was found in $HOME directory, installing it.
    install_pip $HOME/`ls -alF | grep -e "$PROD.*\.tar.gz$" | sed -re "s/^.*($PROD.*\.tar\.gz)$/\1/"`
fi

# checking that Django project exists
ls -alF $HOME | grep "$PROJECT/\$" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Info: Django project folder '~/$PROJECT' does not exist. Creating Django project"
    cd $HOME
    django-admin startproject $PROJECT
    ls -alF $HOME | grep "$PROJECT/\$" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error: Could not start '$PROJECT' django project. Start it manually, then run this script again."
        exit 1
    fi
    cd $HOME/$PROJECT
else
    echo "Info: Django project folder '~/$PROJECT' exists"
fi

SETTINGS_FILE="$HOME/$PROJECT/$PROJECT/settings.py"  # the django project settings file
add_app2django_settings "rest_framework"
add_app2django_settings "rest_framework.authtoken"
add_app2django_settings "django_ocr_server"
add_app2django_settings "rest_framework_swagger"


URLS_FILE="$HOME/$PROJECT/$PROJECT/urls.py"  # the django project urls file
add_str2django_urls "from django.contrib import admin"
add_str2django_urls "from django.urls import path"
add_str2django_urls "from django.urls import include"
add_str2django_urls "from rest_framework.documentation import include_docs_urls"
add_str2django_urls "path('docs/', include_docs_urls(title='OCR Server API')),"
add_str2django_urls "path('', include('django_ocr_server.urls'), ),"
add_str2django_urls "path('admin/', admin.site.urls),"

# applying migrations
cd $HOME/$PROJECT
python manage.py migrate

# creating the django project superuser
echo "from django.contrib.auth.models import User; user=User.objects.get_or_create(username='admin')[0]; user.is_staff=True; user.is_superuser=True; user.set_password('admin'); user.save(); print('Superuser successfully created with username \'admin\' and password \'admin\'')" | python manage.py shell

# howto message
echo "Go to '$HOME/$PROJECT'; workon '$PACKAGE'; python manage.py runserver; then goto http://localhost:8000"