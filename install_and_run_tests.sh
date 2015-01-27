#!/bin/bash

rm tests/images/m_*;
pip3 install . --no-deps --ignore-installed;
nosetests --processes=4 --process-timeout=600 -v -w tests --nocapture $1;
exit $?;
