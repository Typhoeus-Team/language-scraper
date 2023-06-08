#!/bin/bash

# Clean out existing builds
rm -rf ./output

# Execute Spiders
cd ./crawlers/
scrapy crawl spanish -o ../output/spanish.csv
cd -
