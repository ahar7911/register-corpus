#! /bin/bash

mkdir -p ZIPS
wget "https://zenodo.org/records/3457917/files/GermInnC_release23092019.zip" -O ZIPS/innsbruck.zip

mkdir -p innsbruck
unzip ZIPS/innsbruck.zip -d innsbruck
unzip innsbruck/GermInnC.zip -d innsbruck