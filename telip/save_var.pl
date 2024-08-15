#!/usr/bin/perl

use strict;
use warnings;
use Asterisk::AGI;

my $agi = Asterisk::AGI->new();

my ($key, $value) = @ARGV;
$agi->set_variable($key,$value)
