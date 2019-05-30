.. index:: Usage examples

Usage examples
==============
 You can download all examples from https://github.com/shmakovpn/django_ocr_server/tree/master/usage_examples

.. index:: curl usage example

curl
----
 Use curl with '@' before the path of the uploading file
  .. code-block:: bash

   #!/usr/bin/env bash
   curl -F "file=@example.png" localhost:8000/upload/

.. index:: Python usage example

python
------
 Use requests.post function
  .. code-block:: python

   import requests


   with open("example.png", 'rb') as fp:
       print(requests.post("http://localhost:8000/upload/",
                           files={'file': fp}, ).content)

.. index:: Perl usage example

perl
----
 Use LWP::UserAgent and HTTP::Request::Common
  .. code-block:: perl

   #!/usr/bin/perl
   use strict;
   use warnings FATAL => 'all';
   use LWP::UserAgent;
   use HTTP::Request::Common;

   my $ua = LWP::UserAgent->new;
   my $url = "http://localhost:8000/upload/";
   my $fname = "example.png";

   my $req = POST($url,
       Content_Type => 'form-data',
       Content => [
           file => [ $fname ]
       ]);

   my $response = $ua->request($req);

   if ($response->is_success()) {
       print "OK: ", $response->content;
   } else {
       print "Failed: ", $response->as_string;
   }

.. index:: php usage example

php
---
 Use CURLFile($file, $mime, $name)
  .. code-block:: php

   <?php
   //Initialise the cURL var
   $ch = curl_init();

   //Get the response from cURL
   curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

   //Set the Url
   curl_setopt($ch, CURLOPT_URL, 'http://localhost:8000/upload/');

   //Create a POST array with the file in it
   $file='example.png';
   $mime=getimagesize($file)['mime'];
   $name=pathinfo($file)['basename'];
   $postData = array(
       'file' => new CURLFile($file, $mime, $name),
   );

   curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);

   // Execute the request
   $response = curl_exec(  $ch);
   echo($response);

   curl_close ($ch);

   ?>