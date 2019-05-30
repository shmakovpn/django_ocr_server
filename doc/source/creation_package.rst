.. index:: Creation a distribution package

Creation a distribution package
===============================
 As mentioned earlier, the automatic installation script 'install_ubuntu.sh'
 uses the package from the PyPI repository by default. To change this behavior or
 if you need your own distribution package you can build it.

 Run command
  | $cd path to cloned project from github
  | $python setup.py sdist

 Look in 'dist' directory, there is your package was created.

 Also you can continue automatic installation. The package will be used.