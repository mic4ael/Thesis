#!/bin/bash

rm tests/images/m_*;
pip3 install . --no-deps --ignore-installed;
nosetests -v -w tests --nocapture $1;
exit $?;
