#!/bin/sh
# install_ubuntu.sh automates installing Django-ocr-server
# author: shmakovpn <shmakovpn@yandex.ru>
# date: 2019-04-23

PROD='django-ocr-server'
PACKAGE='django_ocr_server'
USER='django_ocr_server'  # OS username for Django project
PROJECT='ocr_server'  # name of the Django project
PWD=$(dirname $(readlink -f $0))

# installs a package using apt (apt install -y package name) 2019-04-23
# check that the package successfully installed
install_apt() {
    dpkg -l | grep -qi "^ii\s\+$1\(\s\|:\)" > /dev/null 2>&1  # check package already installed
    if [ $? -ne 0 ]; then
        echo "Info: package '$1' is not installed. Installing"
        apt install -y $1
        if [ $? -ne 0 ]; then
            echo "Error. Could not install '$1'. Install it manually, then run this script again"
            exit 1
        else
            echo "Info: package '$1' installed successfully"
        fi
    else
        echo "Info: package '$1' is already installed"
    fi
}


# exec $1 from $USER, send evironment *_PROXY and PATH 2019-04-24
exec_from_user() {
    sudo http_proxy=$http_proxy https_proxy=$https_proxy HTTP_PROXY=$HTTP_PROXY HTTPS_PROXY=$HTTPS_PROXY PATH=$PATH -H -i -u $USER $1
}


echo "This script automatically installs $PROD"

# checks root privileges
if [ $(id -u) -ne 0 ]; then
   echo "This script must be run as root"
   exit 1
fi

# DEBUG 01
# userdel -r "$USER"  # remove $USER and it's home directory
# END DEBUG 01

# check that user exists
id "$USER"  > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Info: The user '$USER' does not exist, create it."
    # creating user for Django-ocr-server
    useradd -m $USER -s /bin/bash
    id "$USER"  > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error. Could not create the user '$USER'"
    fi
else
    echo "INFO: The user '$USER' is already exits"
fi
echo "$PROD will be installed under user '$USER'"

eval "USER_HOME=$(echo ~$USER)"

PATH="$USER_HOME/.local/bin:$PATH"  #

ls -alF $PWD/dist | grep -e "$PROD.*\.tar\.gz$" > /dev/null 2>&1
# checking that the package django-ocr-server-{version}.tar.gz exists in the $PWD/dist directory
if [ $? -eq 0 ]; then
    # the package django-ocr-server-{version}.tar.gz found in the $PWD/dist directory, copying it to the $USER directory
    cp $PWD/dist/$PROD*tar.gz $USER_HOME > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Error. Could not copy $PWD/dist/$PROD*tar.gz to $USER_HOME"
        exit 1
    fi
else
    # the package does not exist in the $PWD/dist directory
    # checking that the package exists in the $PWD directory
    ls -alF $PWD | grep -e "$PROD.*\.tar\.gz$" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        # the package django-ocr-server-{version}.tar.gz found in the $PWD directory, copying it to the $USER directory
        cp $PWD/$PROD*tar.gz $USER_HOME > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            echo "Error. Could not copy $PWD/$PROD*tar.gz to $USER_HOME"
            exit 1
        fi
    else
        # the package django-ocr-server-{version}.tar.gz does not exist neither in the $PWD/dist nor in the $PWD direcory
        # do nothing, further installation process will try to download the package from PyPI
        echo "Info. The file $PROD*tar.gz not found, further installation process will try to download the package from PyPI"
    fi
fi


# Installing packages
install_apt "g++"
install_apt "libpoppler-cpp-dev"
install_apt "tesseract-ocr"
install_apt "tesseract-ocr-rus"
install_apt "python3.7"
install_apt "python3.7-dev"
install_apt "python-pip"
# install_apt "python-setuptools"  # it will be installed later using pip

# create installation script in $USER environment
echo "#!/usr/bin/env bash" > $USER_HOME/install.sh
echo "PACKAGE=$PACKAGE" >> $USER_HOME/install.sh
echo "PROJECT=$PROJECT" >> $USER_HOME/install.sh
echo "PROD=$PROD" >> $USER_HOME/install.sh
echo "PROJECT_PATH=$PROJECT_PATH" >> $USER_HOME/install.sh
chmod +x $USER_HOME/install.sh
chown $USER:$USER $USER_HOME/install.sh
cat $PWD/install_ubuntu/install.sh >> $USER_HOME/install.sh

exec_from_user "$USER_HOME/install.sh"

echo 'Installation successfully finished'