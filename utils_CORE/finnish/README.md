# FinCORE (Finnish)
This corpus was taken from the following FinCORE_full Github repository: https://github.com/TurkuNLP/FinCORE_full.git
We include below the README of the original FinCORE repository (https://github.com/TurkuNLP/FinCORE.git) as well as that of the FinCORE_full repository.

## Finnish Corpus of Online REgisters (FinCORE)

This repository contains the Finnish Corpus of Online REgisters (FinCORE)
data introduced in the paper
[Toward Multilingual Identification of Online Registers](https://www.aclweb.org/anthology/W19-6130/) ([pdf](https://www.aclweb.org/anthology/W19-6130)).

FinCORE annotations are licensed under
[CC BY](http://creativecommons.org/licenses/by-sa/4.0/).

The software introduced in the paper is available from
<https://github.com/spyysalo/multiling-cnn>.

### Format

The annotated texts are found in the files `train.tsv`, `dev.tsv` and
`test.tsv` in the `data/` subdirectory in a simple TSV format where each
line has the format `LABEL<TAB>TEXT`.

### Quickstart

To format the data for fastText, run

```
mkdir fasttext
for f in data/{train,dev,test}.tsv; do
    perl -pe 's/^(.*?)\t/__label__$1 /' $f > fasttext/$(basename $f .tsv).ft
done
```

Download Finnish MUSE word vectors

```
wget https://dl.fbaipublicfiles.com/arrival/vectors/wiki.multi.fi.vec
```

Train fastText, predict label probabilities for test data

```
fasttext supervised -epoch 10 -pretrainedVectors wiki.multi.fi.vec -dim 300 \
    -input fasttext/train.ft -output fasttext.model
fasttext predict-prob fasttext.model.bin fasttext/test.ft 6 > probs.txt
```

Evaluate

```
python scripts/auc.py fasttext/test.ft probs.txt
```

## FinCORE_full
Version 1.0 of the full FinCORE corpus can be found in this branch under Releases in the v1.0 tag.

FinCORE consists of over 7 million words and 10,754 documents. Based on the learning curve for English, this size was estimated to be sufficient for the purposes of register identification. Similarly, many register studies operate on smaller datasets, suggesting that the size is sufficient for linguistic purposes as well. FinCORE is based on a random sample of the Finnish Internet Parsebank, which is a mass-scale corpus of the Finnish Web, and already used in a number of studies in both linguistics and NLP. The Parsebank has been compiled with two methods. First, a dedicated crawl was established to retrieve Finnish documents from the Web. To this end, seed URLs were selected from data with a language detection tool (https://github.com/CLD2Owners/cld2), and a Web crawl was performed by using these seeds. Second, Finnish documents were identified and retrieved from Common Crawl, an organization that crawls the Internet providing its archives and datasets for public use (https://commoncrawl.org/). Texts were cleaned from menus and listings with boilerplate removal, and deduplicated using Onion (https://corpus.tools/wiki/Onion).

The FinCORE registers are annotated following the taxonomy of the English CORE. In order to better target the texts included in FinCORE, we made some minor modifications to the original CORE register scheme. Specifically, we did not use some subregister classes originally included in CORE, because they were extremely rare in Finnish, and we added some new classes in order to fully describe the registers found in the Finnish data (e.g., machine-translated/generated texts). These minor adjustments were made in an iterative manner based on the annotators’ remarks. If a text variety not denoted by any of the subregister labels was repeatedly found during the annotation, a new subregister label could be decided, and this label could be given to the documents retrospectively. On the other hand, if a register or subregister was found to be very infrequent after the first round of annotation, this register label could be deleted from the final labels. The final FinCORE scheme consists of nine main registers divided into 30 subregisters, as opposed to eight main and 39 subregisters in the original CORE.

In the English CORE, each text was annotated by four coders using Mechanical Turk. In our study, the register annotation of the data was operated individually by annotators with a linguistics background. In addition to the document text resulting from the cleaning process described above, the annotators had access to the document url. If the document was still accessible, the annotators could visit the website in order to better interpret the register. We double-annotated the texts first, and when a sufficient level of agreement was found, we changed to single annotation. Nevertheless, difficult cases were always resolved in a group. The measured human inter-annotator agreement, counted prior to the discussions, was 79.66%. When annotators used only main registers, a 83.22% consensus was reached. While the CORE hybrids (which means that a text shares characteristics of several registers) were formed based on systematic disagreements between the annotators, the FinCORE hybrids were explicitly created by the individual annotators. This allowed the creation of hybrid texts even when a text was annotated by a single person. 
