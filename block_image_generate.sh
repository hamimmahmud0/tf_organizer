#!/bin/sh

i=1
until [ $i -gt 20 ]
do
    python block_image.py $i
    i=$((i + 1))
done

