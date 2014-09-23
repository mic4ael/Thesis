#!/bin/bash

pip install . --no-deps --ignore-installed;
cd tests;
nosetests-3.2 --nocapture $1;
cd ..;
