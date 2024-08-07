#! /bin/bash

mkdir -p ZIPS

# CORE
curl -L -o ZIPS/CORE_en.tar.gz https://api.github.com/repos/TurkuNLP/CORE-corpus/tarball/ 
tar -xvf ZIPS/CORE_en.tar.gz
echo "CORE download and extraction complete"

#FreCORE and SweCORE
curl -L -o ZIPS/CORE_fr_sw.tar.gz https://api.github.com/repos/TurkuNLP/Multilingual-register-corpora/tarball
tar -xvf ZIPS/CORE_fr_sw.tar.gz
echo "FreCORE/SweCORE download and extraction complete"

# FinCORE
mkdir FinCORE_full
cd FinCORE_full
curl -L -o dev.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/dev.tsv
curl -L -o fincore_labels.txt https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/fincore_labels.txt
curl -L -o test.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/test.tsv
curl -L -o train.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/train.tsv
cd ..
echo "FinCORE download and extraction complete"

# multilang CORE
curl -L -o ZIPS/CORE_multi.tar.gz https://api.github.com/repos/TurkuNLP/pytorch-registerlabeling/tarball/
tar -xvf ZIPS/CORE_multi.tar.gz --wildcards "*/data"
echo "multilang CORE download and extraction complete"

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
rm -r pytorch-registerlabeling/data/en
rm -r pytorch-registerlabeling/data/fi
rm -r pytorch-registerlabeling/data/fr
rm -r pytorch-registerlabeling/data/sv
rm -r pytorch-registerlabeling/data/multi
mv pytorch-registerlabeling/data/ru/test.tsv pytorch-registerlabeling/data/ru/ru.tsv # oddly, no ru.tsv so we convert