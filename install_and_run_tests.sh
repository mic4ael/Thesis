#!/bin/bash

pip install . --no-deps --ignore-installed;
cd tests;
nosetests-3.3 --nocapture;
cd ..;
