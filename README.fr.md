# Corpus multilingue pour la classification des registres de textes
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/ahar7911/register-corpus/blob/master/README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/ahar7911/register-corpus/blob/master/README.fr.md)

Ce dépôt Git contient des scripts permettant de télécharger, de convertir la classification des registres (que nous appelons ici la « standardisation ») et d'analyser les corpus utilisés pour la classifications multilingue des registres de textes à l'aide de grands modèles de langue (LLMs ou *large language models*).

Pour télécharger les corpus, exécutez les scripts de téléchargement fournis dans chaque sous-dossier du dossier `utils` lorsque vous êtes dans le dossier `corpus-original` (créez le dossier et à partir de celui-ci faites tourner les scripts `../utils/core/download_core.sh` et `../utils/innsbruck/download_innsbruck.sh`). Le corpus alsacien devra être téléchargé manuellement dans le dossier `corpus-original/corpus-alsacien`. Sinon, vous pouvez télécharger manuellement les corpus CORE, alsacien, et allemand Innsbruck et spécifier les chemins d'accès dans le fichier `utils/core/lang2tsv.json` et dans les chemins en haut des fichiers `utils/alsatian/standardize_alsatian.py` et `utils/innsbruck/standardize_innsbruck.py`. 

Pour standardiser les corpus, lancer des analyses de leur distribution de registres, et créer les jeux d'entraînement et d'évaluation, faites tourner le script `standardize.sh`. Vous pouvez exécuter individuellement : la standardisation à l'aide des scripts `utils/core/standardize_core.sh`, `utils/alsatian/standardize_alsatian.py`, et `utils/innsbruck/standardize_innsbruck.py`; l'analyse de la distribution de registres via le script `analyze_dist.py`; et la création des jeux d'entraînement et d'évaluation en faisant tourner le script `train_test_split.py`.

Les corpus étiquetés par registre sont convertis aux registres specifiés dans `info/reg_abbv.json`, et stockés dans des fichiers TSV dans le dossier `corpus` où la première colonne spécifie l'abréviation du registre et la seconde le texte. Les fichiers TSV sont divisés par langue, et sont nommés selon l'abréviation de la langue spécifiée dans `info/lang2name.json` (par exemple tous les textes anglais sont stockés dans `en.tsv`). Les fichiers JSON récapitulatifs contenant des informations sur la distribution des registres de chaque corpus sont sauvegardés dans le dossier `summaries` ; les jeux d'entraînement et d'évaluation sont sauvegardés comme des fichiers TSV dans les dossiers `corpus/train` et `corpus/test` respectivement. Les deux utilisent le même schéma de dénomination par abréviation de langue utilisé par les corpus dans le dossier `corpus`.

Un script modifiable `load_env.sh` est utilisé pour charger Python. Chaque script l'exécute avant d'exécuter les scripts Python. N'hésitez pas à adapter ce fichier à votre propre environnement, ou à le rendre vide s'il n'est pas requis.

Le script `distr_corpus.py` crée un corpus à partir du jeu d'entraînement des corpus de telle sorte que le nombre de textes par registre soit aussi égal que possible, et que le nombre de textes par langue pour chaque registre soit aussi égal que possible. Le corpus est stocké dans `corpus/train/distr.tsv` et un fichier identique est stocké dans `corpus/distr.tsv` pour permettre l'analyse de la distribution des registres. Plus d'informations sur l'exécution du script peuvent être trouvées en lançant `python distr_corpus.py --help`. Ce script est automatiquement exécuté par `standardize.sh`.

## Le dossier `info`
Le dossier `info` contient des informations sur les abréviations utilisées dans ce dépôt Git. `info/reg_abbv.json` associe les abréviations des nouveaux registres à leurs noms complets, et `info/lang2name.json` associe les abréviations des langues utilisées comme noms de fichiers à leurs noms anglais complets.

## Le dossier `mappings`
Le dossier `mappings` contient des fichiers JSON qui contiennent des informations sur les correspondances entre les typologies des registres originaux et les typologies des nouveaux registres. `mappings/core_abbv.json` est utilisé dans `utils/core/standardize_core.py` ; `mappings/cahier.json` et `mappings/core.json` sont utilisés dans `utils/alsatian/standardize_alsatian.py` ; et `mappings/innsbruck.json` est utilisé dans `utils/innsbruck/standardize_innsbruck.py`.

Le dossier contient également un diagramme sankey dans le fichier `mappings/sankey/sankey.html` qui visualise la relation entre les registres CORE (utilisés pour étiqueter les corpus CORE) et les registres CAHIER (utilisés pour étiqueter le corpus des textes alsaciens) et les nouveaux registres.

## Le dossier `utils`
Vous trouverez ci-dessous plus d'informations sur les trois corpus utilisés ici et le code pour leur standardisation (fourni ici dans le dossier `utils`) :

### Corpus CORE
Les corpus CORE sont composés du [corpus CORE original en anglais](https://github.com/TurkuNLP/CORE-corpus.git), des [corpus FreCORE (français) et SweCORE (suédois)](https://github.com/TurkuNLP/Multilingual-register-corpora.git), et du [corpus FinCORE (finnois)](https://github.com/TurkuNLP/FinCORE_full.git), tous téléchargés à partir des dépôts Github de TurkuNLP. Nous utilisons également un corpus multilangue de textes étiquetés par registre provenant d'un [dépôt Git de TurkuNLP](https://github.com/TurkuNLP/pytorch-registerlabeling/tree/main/data) qui comporte des textes supplémentaires étiquetés par registre en arabe, catalan, espagnol, farsi, hindi, indonésien, japonais, norvégien, portugais, russe, turc, ourdou, et chinois (simplifié).

Le corpus original de CORE comprend 8 registres et 47 sous-registres. Nous avons créé une correspondance qui associe soit le registre entier (et tous les sous-registres) au nouveau registre, soit des sous-registres individuels à différents nouveaux registres.

Toutes les standardisations sont effectuées en utilisant le fichier `mappings/core_abbv.json`, qui fait correspondre les abréviations des registres CORE aux abréviations des nouveaux registres. Chaque registre se voit associer son propre nom à un objet JavaScript, qui contient une paire nom-clé pour le nom complet du registre et une paire nom-clé « subregisters » pour toutes les informations concernant les sous-registres du registre, dont la clé est à son tour un objet JavaScript qui contient une paire nom-clé pour le nom complet du sous-registre. Si le registre dans sa totalité correspond à un seul nouveau registre, l'objet JavaScript du registre contiendra également une paire nom-clé « maps » dont la clé est l'abréviation du nouveau registre ; si les sous-registres correspondent individuellement à de nouveaux registres, les objets JavaScript des sous-registres contiendront la paire nom-clé « maps ». Les (sous-)registres non associés à un nouveau registre n'ont pas de paire nom-clé « maps ».

Les corpus FinCORE et CORE multilingue ajoutent des registres supplémentaires qui ne sont pas présents dans la typologie originale, ou permettent certains sous-registres sous un registre différent. Les registres utilisés uniquement dans FinCORE ou les sous-registres acceptés sous un registre différent dans FinCORE sont marqués dans la paire nom-clé « nom » avec « (FinCORE only) » à la fin. Les registres utilisés uniquement dans les corpus multilingues n'avaient pas d'explication sur les abréviations et ont donc été ignorés.

Tout le code pour la standardisation des corpus CORE se trouve dans le dossier `utils/core` :

#### download_core.sh
Ce script télécharge tous les corpus CORE depuis les dépôts de TurkuNLP dans le dossier actuel, en stockant les corpus zippés dans un sous-dossier `ZIPS`. `utils/core/lang2tsv.json` est configuré pour supposer que les dépôts seront trouvés dans le dossier `corpus-original` ; vous pouvez le faire en créant le dossier `corpus-original` et en lançant `../utils/core/download_core.sh` depuis ce dossier. `corpus-original` est déjà inclus dans le fichier `.gitignore`.

#### lang2tsv.json
Ce fichier enregistre des informations sur les chemins d'accès aux corpus CORE provenant des dépôts TurkuNLP. Il est divisé en deux paires nom-clé qui contiennent chacun un objet JavaScript : « dir », qui contient des informations sur les chemins d'accès aux corpus CORE, et “glob”, qui contient des chaînes de caractères utilisées par la bibliothèque `glob` pour trouver les fichiers de corpus (soit des fichiers TSV, soit des fichiers `.tsv.gz`) dans les chemins d'accès spécifiés. Le fichier est actuellement paramétré par défaut pour la configuration des corpus après l'exécution du script `utils/core/download_core.sh` dans le dossier `corpus-original`, mais si le script est exécuté dans un autre dossier ou les corpus téléchargés manuellement dans un autre dossier, l'objet JavaScript dans le champ « dir » peut être modifié en conséquence. Les informations dans la paire nom-clé « glob » ne doit pas être modifié si vous travaillez avec un téléchargement direct des dépôts de TurkuNLP. 

« en » spécifie le corpus CORE original en anglais, « fr » spécifie FreCORE, « sv » spécifie SweCORE, « fi » spécifie FinCORE, et « multi » spécifie les corpus multilingues.

#### standardize_core.py
Ce script Python effectue la standardization d'un corpus CORE, trouvé à l'aide de `utils/core/lang2tsv.json`, des registres CORE vers les nouveaux registres. Le script accepte un argument, --lang, qui spécifie le corpus sur lequel le script doit être exécuté. « en » spécifie le corpus CORE original en anglais, « fr » spécifie FreCORE, « sv » spécifie SweCORE, « fi » spécifie FinCORE, et « multi » spécifie les corpus multilingues. Le script utilise le fichier `mappings/core_abbv.json` pour faire correspondre les registres. 

Les textes classés comme « hybrides » (ayant plus de deux registres) sont généralement ignorés. Si les deux registres sont des sous-registres du même registre, et que ce registre fait correspondre TOUS les sous-registres au même nouveau registre, alors le texte est relié à ce nouveau registre.

Les commentaires dans le code fournissent plus d'informations sur les modifications spécifiques à la langue ou au corpus effectuées pour la standardization (par exemple, l'extraction HTML des textes russes).

#### standardize_core.sh
Ce script exécute `utils/core/standardize_core.py` sur tous les corpus CORE (c'est-à-dire qu'il l'exécute sur « en », « fi », « fr », « sv », et « multi »).

### Corpus alsacien
Un corpus de textes alsaciens étiquetés par registre a été fourni par l'unité de recherche LiLPa (Linguistique, Langues, Parole) de l'Université de Strasbourg. 

Chaque texte se trouve dans un sous-dossier qui décrit son origine - ALA, ALS_WKP, DIVITAL_parallel, HRM, OLCA, et théâtre. 

Chaque texte contient des métadonnées, y compris des informations telles que le titre, l'auteur, le transcripteur, l'URL de la source, les droits d'accès à la source, etc. sous la forme de lignes de texte préfixées par des dièses qui commencent chaque fichier texte et après lesquelles le texte est ajouté. Si le document est un document web, un registre CORE est inclus dans l'étiquette webRegister (sinon l'étiquette contient « None (not a web document) »). Les registres sont séparés des sous-registres par des points. Tous les textes sont en outre classés selon la [typologie de l'échantillon TeDDi](https://aclanthology.org/2022.lrec-1.123/) dans l'étiquette genreTeDDi et la [typologie CAHIER](https://opentheso.huma-num.fr/opentheso/index.xhtml) (choisissez *Typologie des genres textuels (43)* dans le menu déroulant) dans les étiquettes genreCAHIER, genreCAHIER, targetAudienceCAHIER, discourseTypeCAHIER, domainCAHIER, factualityCAHIER, formCAHIER, contentsLayoutCAHIER, originCAHIER, et channelCAHIER. Les genres sont séparés des sous-genres dans le genreCAHIER par des points. Les classifications genreCAHIER sont utilisées ici pour la standardisation, bien que les classifications CORE aient également été prises en compte (et le code commenté correspondant est toujours présent).

Tout le code pour la standardisation du corpus alsacien se trouve dans le dossier `utils/alsatian` :

#### standardize_alsatian.py
Ce script Python effectue la standardisation du corpus alsacien, trouvé à l'aide de l'objet Path `alsatian_path` en haut du fichier, de ses classifications originales de genre CAHIER vers les nouveaux registres. Le script utilise le fichier `mappings/cahier.json` pour faire correspondre les registres, et utilise également `mappings/core.json` dans un code commenté pour comparer les nouveaux registres convertis à partir des registres CORE et des registres CAHIER, s'ils sont différents. Ces fichiers JSON font correspondre les noms complets des registres CORE ou CAHIER aux abréviations des nouveaux registres dans la paire nom-clé « maps » ; une correspondance avec « unused » spécifie que le registre n'a pas été mis en correspondance. Si un sous-registre est associé à un nouveau registre différent de son registre, la paire nom-clé « exceptions » du registre contiendra un objet JavaScript avec une paire nom-clé qui associe le sous-registre à l'abréviation du nouveau registre auquel il est associé (ou « unused » s'il n'est pas associé).

### Corpus allemand Innsbruck
Un corpus de textes allemands étiquetés par genre datant de 1800 à 1950. Pour plus d'informations, consultez le [lien de téléchargement Zenodo](https://zenodo.org/records/3457917) et le fichier `GermInnC corpus_documentation.pdf` qui se trouve dans le téléchargement. Pour l'instant, seuls les textes de 1901 à 1950 sont utilisés dans la standardisation pour créer le nouveau corpus allemand.

Tout le code pour la standardisation du corpus allemand d'Innsbruck se trouve dans le dossier `utils/innsbruck` :

#### download_innsbruck.sh
Ce script télécharge le corpus allemand Innsbruck depuis le lien de téléchargement Zenodo dans le dossier actuel, et décompresse les dossiers nécessaires tout en stockant le corpus zippé original dans un sous-dossier `ZIPS`. `utils/innsbruck/standardize_innsbruck.py` est configuré pour supposer que le corpus sera trouvé dans le dossier `corpus-original` ; vous pouvez le faire en créant le dossier `corpus-original` et en lançant `../utils/innsbruck/download_innsbruck.sh` depuis ce dossier. `corpus-original` est déjà inclus dans le fichier `.gitignore`.

#### standardize_innsbruck.py
Ce script Python effectue la standardisation du corpus allemand Innsbruck, trouvé à l'aide de l'objet Path `innsbruck_path` en haut du fichier, de ses classifications originales vers les nouveaux registres. Le script utilise le fichier `mappings/innsbruck.json` pour faire correspondre les registres.