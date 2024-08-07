#! /bin/bash

mkdir -p ZIPS

# CORE
echo "start CORE download"
curl -L -o ZIPS/CORE_en.tar.gz https://api.github.com/repos/TurkuNLP/CORE-corpus/tarball/ 
echo "start CORE extraction"
tar -xvf ZIPS/CORE_en.tar.gz
echo "CORE download and extraction complete"
echo

#FreCORE and SweCORE
echo "start FreCORE/SweCORE download"
curl -L -o ZIPS/CORE_fr_sw.tar.gz https://api.github.com/repos/TurkuNLP/Multilingual-register-corpora/tarball
echo "start FreCORE/SweCORE extraction"
tar -xvf ZIPS/CORE_fr_sw.tar.gz
echo "FreCORE/SweCORE download and extraction complete"
echo

# FinCORE
mkdir FinCORE_full
cd FinCORE_full
echo "start FinCORE download"
curl -L -o dev.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/dev.tsv
curl -L -o fincore_labels.txt https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/fincore_labels.txt
curl -L -o test.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/test.tsv
curl -L -o train.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/train.tsv
cd ..
echo "FinCORE download complete"
echo

# multilang CORE
echo "start multilang CORE download"
curl -L -o ZIPS/CORE_multi.tar.gz https://api.github.com/repos/TurkuNLP/pytorch-registerlabeling/tarball/
echo "start multilang CORE extraction"
tar -xvf ZIPS/CORE_multi.tar.gz --wildcards "*/data"
echo "multilang CORE download and extraction complete"
echo

echo "renaming folders to remove Github info"
# renaming Github directories, removes "OWNER-" (here "TurkuNLP-"") and "-#######" (number of the commit ref)
for dir in */; do #
    if [ -d "$dir" ]; then
        new_dir=$(echo $dir | cut -d '-' -f 2- | rev | cut -d '-' -f 2- | rev)
        if [ "$dir" != "$new_dir" ]; then
            mv $dir $new_dir
        fi
    fi
done

# cleaning up multilang
echo "clean up multilang (remove en fi fr sv multi, fix ru)"
rm -r pytorch-registerlabeling/data/en
rm -r pytorch-registerlabeling/data/fi
rm -r pytorch-registerlabeling/data/fr
rm -r pytorch-registerlabeling/data/sv
rm -r pytorch-registerlabeling/data/multi
mv pytorch-registerlabeling/data/ru/test.tsv pytorch-registerlabeling/data/ru/ru.tsv # oddly, no ru.tsv so we convert