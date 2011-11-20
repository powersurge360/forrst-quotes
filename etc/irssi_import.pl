#!/usr/bin/env perl

use strict;
use warnings;

use Data::Dumper;
use LWP::UserAgent;

my $ua = LWP::UserAgent->new;

open my $fh, $ARGV[0] or die $!;
my @quotes = <$fh>;
foreach my $line(@quotes) {
    my($date, $quote) = 
        $line =~/^\d{2}\:\d{2}\:\d{2} <forrstdotcom> \[\d+\/\d+\] (\d{4}-\d{2}-\d{2})(.*)$/;
    my @req = ('http://forrst-quotes.appspot.com/api/quote', [
        date  => $date,
        quote => $quote
    ]);
    
    my $res = $ua->post(@req);
    if(!$res->is_success()) {
        print Dumper $res;
        die "SHIIIIIIIIIIIIII";
    }
}
