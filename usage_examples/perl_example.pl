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