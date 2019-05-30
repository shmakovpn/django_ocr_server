Management Commands
===================
 Run it to clean trash. It removes all uploaded files and PDFs that do not have related models in database.
  $python manage.py clean

 Run it to remove models, uploaded files and PDFs, whose time to live (TTL) has expired.
  $python manage.py ttl
