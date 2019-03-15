#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "ERROR: Should be called with arguments <small_csv> <master_csv>."
    echo "ABORTING"
    exit 1
fi

small_csv="$1"
master_csv="$2"

tail -n +2 "$small_csv" >> "$master_csv"