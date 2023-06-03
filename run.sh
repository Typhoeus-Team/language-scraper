#!/bin/bash

# Clean out existing builds
rm -rf ./output

# Execute Spider
scrapy runspider spanish.py -o output/spanish.csv
