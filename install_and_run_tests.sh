#!/bin/bash

pip3 install . --no-deps --ignore-installed;
cd tests;
nosetests-3.2 --nocapture $1;
cd ..;
