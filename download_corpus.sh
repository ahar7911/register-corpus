#! /bin/bash

cd ..
mkdir original-corpus
cd original-corpus

# curl -L https://api.github.com/repos/TurkuNLP/CORE-corpus/tarball/ > CORE-corpus.tar
# curl -L https://api.github.com/repos/TurkuNLP/Multilingual-register-corpora/tarball
curl -L https://api.github.com/repos/TurkuNLP/pytorch-registerlabeling/tarball/ > temp.tar
tar -xvf temp.tar */data