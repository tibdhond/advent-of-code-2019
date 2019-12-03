#!/bin/bash

for i in {1..25}
do
    if [ ! -d day$i ]
    then
        mkdir day$i
        echo "from day$i import *" > day$i/tests.py
        cat layout_setup/tests.py >> day$i/tests.py
        cp layout_setup/base.py day$i/day$i.py
        touch day$i/input.txt
    fi
done
