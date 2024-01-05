#!/bin/bash
for i in ./test*.py
do
    python $i &
done
