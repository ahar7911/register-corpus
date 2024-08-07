#! /bin/bash

mkdir -p ZIPS
echo "downloading innsbruck zip file"
wget "https://zenodo.org/records/3457917/files/GermInnC_release23092019.zip" -O ZIPS/innsbruck.zip
echo "download complete"
echo

mkdir -p innsbruck
echo "extracting innsbruck zip file"
unzip ZIPS/innsbruck.zip -d innsbruck
echo "extracting GermInnC.zip file"
unzip -q innsbruck/GermInnC.zip -d innsbruck
echo "extraction complete"