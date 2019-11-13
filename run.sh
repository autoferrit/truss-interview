#!/usr/bin/env bash

echo "This runs on python3. Tested on 3.7 but should run on 3.3+"
echo "The library 'pytz' should also be installed"
echo ""
echo "processing ..."
echo " > sample.csv"
./process.py < sample.csv > sample-out.csv

echo " > sample-with-broken-utf8.csv"
./process.py < sample-with-broken-utf8.csv > sample-broken-out.csv
