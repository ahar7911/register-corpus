# Multilingual Corpus for Classification of Textual Registers
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ahar7911/register-corpus/blob/master/README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/ahar7911/register-corpus/blob/master/README.fr.md)

This repository contains scripts to download, convert the register classification of (which we refer to here as "standardization"), and analyze corpora used for the multilingual classification of textual registers using large language models (LLMs).

To download the corpora, run the download scripts provided in each subfolder of the `utils` directory within the `corpus-original` directory (make the directory, and from within run `../utils/core/download_core.sh` and `../utils/innsbruck/download_innsbruck.sh`). The Alsatian corpus will have to be downloaded manually into `corpus-original/corpus-alsacien`. Alternatively, you can manually download the CORE, Alsatian, and German Innsbruck corpora and specify their folder filepaths in `utils/core/lang2tsv.json` and in the paths at the top of `utils/alsatian/standardize_alsatian.py` and `utils/innsbruck/standardize_innsbruck.py`. 

To standardize the corpora, run analyses of their register distribution, and create train-test splits, run `standardize.sh`. You can individually run: standardization using `utils/core/standardize_core.sh`, `utils/alsatian/standardize_alsatian.py`, and `utils/innsbruck/standardize_innsbruck.py`; register distribution analysis using `analyze_dist.py`; and train-test splits using `train_test_split.py`.

Register-labeled corpora are converted to the registers specified in `info/reg_abbv.json`, and stored in TSV files in the `corpus` directory where the first column specifies the register abbreviation and the second the text. The TSV files are divided by language, and are named according to the language abbreviation specified in `info/lang2name.json`, e.g. all English texts are stored in `en.tsv`. Summary JSON files containing information about the register distribution of each corpora are saved in the `summaries` directory; train and test splits are saved as TSV files in the `corpus/train` and `corpus/test` directories respectively. Both use the same naming scheme by language abbreviation used by the corpora in the `corpus` directory.

A modifiable script `load_env.sh` is used to load Python. Each script runs this when running Python scripts. Feel free to customize to your own environment, or to make the file empty is it is not needed.

The `distr_corpus.py` script creates a corpus from train splits of the corpora such that the number of texts per register is as equal as possible, and such that the number of texts per language for each register is as equal as possible. The corpus is stored in `corpus/train/distr.tsv` and an identical file is stored in `corpus/distr.tsv` to allow analysis of its register distribution. More information about how to run the script can be found by running `python distr_corpus.py --help`. This script is automatically run by `standardize.sh`.

## `info` folder
The `info` folder contains information about abbreviations used throughout this repository. `info/reg_abbv.json` maps the register abbreviations of the new registers to their full names, and `info/lang2name.json` maps the abbreviations of the languages used as corpus filenames to their full English names.

## `mappings` folder
The `mappings` directory contains JSON files that contain information about the mappings from the original typologies of the registers to the typologies of the new registers. `mappings/core_abbv.json` is used in `utils/core/standardize_core.py`; `mappings/cahier.json` and `mappings/core.json` are used in `utils/alsatian/standardize_alsatian.py`; and `mappings/innsbruck.json` is used in `utils/innsbruck/standardize_innsbruck.py`. 

The directory also contains a Sankey diagram in `mappings/sankey/sankey.html` that visualizes the relationship between the CORE registers (used to label the CORE corpora) and the CAHIER registers (used to label the Alsatian text corpus) and the new registers.

## `utils` folder
More information about the three corpora used here and the code for their standardization (provided here in `utils` folder) is provided below:

### CORE corus
The CORE corpora is comprised of the [original CORE corpus in English](https://github.com/TurkuNLP/CORE-corpus.git), [the FreCORE (French) and SweCORE (Swedish) corpora](https://github.com/TurkuNLP/Multilingual-register-corpora.git), and [the FinCORE (Finnish) corpus](https://github.com/TurkuNLP/FinCORE_full.git), all downloaded from TurkuNLP's datasets. We also include register-labeled corpora from a [multilingual TurkuNLP repository](https://github.com/TurkuNLP/pytorch-registerlabeling/tree/main/data) that includes additional register-labeled texts in Arabic, Catalan, Spanish, Farsi, Hindi, Indonesian, Japanese, Norwegian, Portuguese, Russian, Turkish, Urdu, and (Simplified) Chinese. 

The original CORE corpora includes 8 registers and 47 subregisters. We created a mapping that maps either the entire register (and all subregisters) to the new register, or maps individual subregisters to different new registers.

All standardizations are done using the `mappings/core_abbv.json`, which maps abbreviations of CORE registers to abbreviations of new registers. Each register is given its own field paired to a JSON object, which contains a field for the full name of the register and a field for information about all the subregisters of the register, which in turn contain a JSON object containing a field for the full subregister name. If the full register maps to one new register, the register's JSON object will also have "maps" field for the new register's abbreviation; if subregisters individually map to new registers, the subregisters' JSON objects will have the "maps" field. Unmapped (sub)registers (meaning that texts labeled as these registers have no appropriate corresponding new register and are not used in the converted corpora) have no "maps" field.

The FinCORE and multilingual CORE corpora add additional registers that are not present in the original typology, or allows some subregisters under a different register. Registers used only in FinCORE or subregisters allowed under different register in FinCORE are marked in the "name" field with "(FinCORE only)" at the end. Registers used only in the multilingual corpora had no explanation of the abbreviations and therefore were unmapped/ignored.

All code for the standardization of CORE corpora can be found in `utils/core`:

#### download_core.sh
This script downloads all CORE corpora from TurkuNLP's repositories to the current directory, storing the zipped corpora in a `ZIPS` subfolder. `utils/core/lang2tsv.json` is configured to assume that the repositories will be found in the directory `corpus-original`; you can do this by making the `corpus-original` directory and running `../utils/core/download_core.sh` from inside the directory. `corpus-original` is already included in the `.gitignore` file.

#### lang2tsv.json
This file stores information about the filepaths of the CORE corpora taken from the TurkuNLP repositories. It is split into two fields that each contain a JSON object: "dir", which contains information about the filepaths to the CORE corpora, and "glob", which contains glob strings used to find the corpora files (either TSV files or `.tsv.gz` files) in the specified filepaths. The file is currently configured to the default of running `utils/core/download_core.sh` in the `corpus-original` directory, but if the script is run inside a different directory or manually downloaded in a different directory, the JSON object under the "dir" field can be modified accordingly. The "glob" field should not be changed if working with a direct download of the TurkuNLP repository. 

"en" specifies the original CORE corpus in English, "fr" specifies FreCORE, "sv" specifies SweCORE, "fi" specifies FinCORE, and "multi" specifies the multilingual corpora.

#### standardize_core.py
This is the Python script that does the standardization of a CORE corpus, located using `utils/core/lang2tsv.json`, from its original CORE registers to the new registers. The script takes one argument, --lang, which specifies which corpus to run the script on. "en" specifies the original CORE corpus in English, "fr" specifies FreCORE, "sv" specifies SweCORE, "fi" specifies FinCORE, and "multi" specifies the multilingual corpora. The script uses the `mappings/core_abbv.json` file to map registers. 

Texts classified as being "hybrid" (having more than two registers) are usually ignored. If the two registers are subregisters of the same register, and that register maps ALL subregisters to the same new register, then the text is mapped to that new register.

Comments in the code provide more information about language- or corpus-specific modifications made for standardization (e.g. HTML extraction for Russian texts).

#### standardize_core.sh
This script runs `utils/core/standardize_core.py` on all CORE corpora (i.e. runs it on "en", "fi", "fr", "sv", and "multi").

### Alsatian corpus
A corpus of register-labeled Alsatian texts was provided by the LiLPa (Linguistique, Langues, Parole) research unit of the Université de Strasbourg. 

Each text is found in a subfolder that describes its origin - ALA, ALS_WKP, DIVITAL_parallel, HRM, OLCA, and theatre. 

Each text contains metadata, including information such as title, author, transcriber, source URL, source access rights, etc. in the form of hashtag-prefixed lines that begin each text file and after which the text is appended. If the document is a web document, a CORE register is included under the webRegister tag (otherwise the tag contains "None (not a web document)"). Registers are separated from subregisters using periods. All texts are additionally classified according to the [TeDDi sample typology](https://aclanthology.org/2022.lrec-1.123/) in the genreTeDDi tag and the [CAHIER typology](https://opentheso.huma-num.fr/opentheso/index.xhtml) (choose *Typologie des genres textuels (43)* in the drop-down menu) in the genreCAHIER, genreCAHIER, targetAudienceCAHIER, discourseTypeCAHIER, domainCAHIER, factualityCAHIER, formCAHIER, contentsLayoutCAHIER, originCAHIER, and channelCAHIER tags. Genres are separated from subgenres in genreCAHIER using periods. The genreCAHIER classifications are used here for standardization, although the CORE classifications were also considered (and the corresponding commented-out code is still present).

All code for the standardization of Alsatian corpus can be found in `utils/alsatian`:

#### standardize_alsatian.py
This is the Python script that does the standardization of the Alsatian corpus, located using the Path object `alsatian_path` at the top of the file, from its original CAHIER genre classifications to the new registers. The script uses the `mappings/cahier.json` file to map registers, and also used `mappings/core.json` in commented-out code to compare the new registers converted from CORE registers and from CAHIER registers, if different. These JSON files each map the full names of the CORE or CAHIER register to the abbreviations of the new registers in the "maps" field; a mapping to "unused" specifies that the register was unmapped. If a subregister maps to a different new register than its register, the "exceptions" field of the register will contain a JSON object with a field that pairs the subregister with the abbreviation of the new register it is mapped to (or "unused" if it is unmapped).

### German Innsbruck corpus
A corpus of genre-labeled German texts dating from 1800-1950. More information can be found at the [Zenodo download link](https://zenodo.org/records/3457917) and the `GermInnC corpus_documentation.pdf` file found in the download. At the moment, only texts from 1901-1950 are used in the standardization to create the new German corpus.

All code for the standardization of German Innsbruck corpus can be found in `utils/innsbruck`:

#### download_innsbruck.sh
This script downloads the German Innsbruck corpus from the Zenodo download link to the current directory, and unzips the needed folders while storing the original zipped corpus in a `ZIPS` subfolder. `utils/innsbruck/standardize_innsbruck.py` is configured to assume that the corpus will be found in the directory `corpus-original`; you can do this by making the `corpus-original` directory and running `../utils/innsbruck/download_innsbruck.sh` from inside the directory. `corpus-original` is already included in the `.gitignore` file.

#### standardize_innsbruck.py
This is the Python script that does the standardization of the German Innsbruck corpus, located using the Path object `innsbruck_path` at the top of the file, from its original classifications to the new registers. The script uses the `mappings/innsbruck.json` file to map registers.