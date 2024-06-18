BASEDIR=CORE
MAPPINGS=$BASEDIR/core_mappings.json

# CORE English
EN_SRC_DIR=$BASEDIR/../../CORE-corpus/
EN_FILE_EXT=.tsv.gz
EN_DST_DIR=$BASEDIR/english/CORE_en.tsv

rm -f $EN_DST_DIR
python $BASEDIR/standardize_core.py --map_path $MAPPINGS --src_path $EN_SRC_DIR --file_ext $EN_FILE_EXT --dst_path $EN_DST_DIR
echo "CORE (original in English) completed standardization"


# FreCORE
FR_SRC_DIR=$BASEDIR/../../Multilingual-register-corpora/data/FreCORE/
FR_FILE_EXT=.tsv
FR_DST_DIR=$BASEDIR/french/CORE_fr.tsv

rm -f $FR_DST_DIR
python $BASEDIR/standardize_core.py --map_path $MAPPINGS --src_path $FR_SRC_DIR --file_ext $FR_FILE_EXT --dst_path $FR_DST_DIR
echo "FreCORE completed standardization"


# SweCORE
SW_SRC_DIR=$BASEDIR/../../Multilingual-register-corpora/data/SweCORE/
SW_FILE_EXT=.tsv
SW_DST_DIR=$BASEDIR/swedish/CORE_sw.tsv

rm -f $SW_DST_DIR
python $BASEDIR/standardize_core.py --map_path $MAPPINGS --src_path $SW_SRC_DIR --file_ext $SW_FILE_EXT --dst_path $SW_DST_DIR
echo "SweCORE completed standardization"


# FinCORE
FI_SRC_DIR=$BASEDIR/../../FinCORE_full/
FI_FILE_EXT=.tsv
FI_DST_DIR=$BASEDIR/finnish/CORE_fi.tsv

rm -f $FI_DST_DIR
python $BASEDIR/standardize_core.py --finnish --map_path $MAPPINGS --src_path $FI_SRC_DIR --file_ext $FI_FILE_EXT --dst_path $FI_DST_DIR
echo "FinCORE completed standardization"