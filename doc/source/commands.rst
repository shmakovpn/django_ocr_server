.. index:: Management Commands

Management Commands
===================

Run it to clean trash. It removes all uploaded files and PDFs that do not have related models in database.

.. code-block:: shell-session

 $ python manage.py clean

Run it to remove models, uploaded files and PDFs, whose time to live (TTL) has expired.

.. code-block:: shell-session

 $ python manage.py ttl

Create the user for API (return the AUTH-token).

.. code-block:: shell-session

 $ python manage.py create_user username password
 b2db7002e037a4edb25aed33b04b97e468970376
