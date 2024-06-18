#! /bin/bash

cd ..
mkdir original-corpus
cd original-corpus

curl -sL -o CORE_en.tar.gz https://api.github.com/repos/TurkuNLP/CORE-corpus/tarball/ 
tar -xvf CORE_en.tar.gz

curl -sL -o CORE_fr_sw.tar.gz https://api.github.com/repos/TurkuNLP/Multilingual-register-corpora/tarball
tar -xvf CORE_fr_sw.tar.gz

mkdir FinCORE_full
cd FinCORE_full
curl -sL -o dev.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/dev.tsv
curl -sL -o fincore_labels.txt https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/fincore_labels.txt
curl -sL -o test.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/test.tsv
curl -sL -o train.tsv https://github.com/TurkuNLP/FinCORE_full/releases/download/v1.0/train.tsv
cd ..

curl -sL -o CORE_multi.tar.gz https://api.github.com/repos/TurkuNLP/pytorch-registerlabeling/tarball/
tar -xvf CORE_multi.tar.gz */data

cd ../register-corpus