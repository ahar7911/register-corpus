from argparse import ArgumentParser
import sys
from pathlib import Path
import gzip
import csv
import json

from bs4 import BeautifulSoup

lang2tsv_path = Path("utils_core", "lang2tsv.json")
core_abbv_path = Path("mappings, core_abbv.json")

def openfile(path : Path, mode="r", encoding=None, newline=None):
    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding=encoding, newline=newline) 
    else:
        return open(path, mode, encoding=encoding, newline=newline)


def convert_register(reg_str : str, mapping : dict, lang : str) -> str:
    regs = [reg.upper() for reg in reg_str.split(" ")]

    if "MT" in regs: # FinCORE and mutlilang CORE
        regs.remove("MT")
    if "" in regs: # multilang CORE formatting error
        regs.remove("")
    if lang == "fi": # FinCORE has subregisters first
        regs = regs[::-1]
    if len(regs) == 0 or regs[0] not in mapping: # empty register or bad string
        return None
    
    reg_map = mapping[regs[0]]
    if "maps" in reg_map: # register singly maps to a new register, along with all subregisters
        if len(regs) == 1 or all([r in reg_map["subcategories"] for r in regs[1:]]): # text has no subregister, or all subregisters are under register
            return reg_map["maps"]
    if len(regs) == 2: # now only possible mapping is from a subregister (must be register with single subregister)
        if regs[1] in mapping or regs[1] not in reg_map["subcategories"]: # subregister is either actually a register (hybrid register) or incorrect subregister
            return None
        sub_reg_map = reg_map["subcategories"][regs[1]]
        if "maps" in sub_reg_map: # subregister maps
            return sub_reg_map["maps"]
    return None # register or subregister does not map


def main(lang : str, filepaths : list[Path]):
    if core_abbv_path.exists():
        with openfile(core_abbv_path) as core_abbv_file: # loads mappings as dict
            mapping = json.load(core_abbv_file)
    else:
        print(f"no CORE abbreviation mapping found at {core_abbv_path}, please reload from github repository")
        sys.exit(1)
    
    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    maxInt = sys.maxsize
    while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    for filepath in filepaths:
        with openfile(filepath, "rt", encoding="utf-8") as src_file:
            src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in src_reader:
                reg_str, text = row[0], row[-1] # for some files, metadata in between
                if lang == "ru": # russian has metadata in the first couple columns instead
                    reg_str = row[-2]
                
                if text != "":
                    if lang == "ru": # russian text still contains html info
                        soup = BeautifulSoup(text, "html.parser")
                        text = ' '.join(soup.stripped_strings)

                    new_reg = convert_register(reg_str, mapping, lang)
                    if new_reg is not None:
                        if not Path("corpus").exists():
                            print("\ncorpus folder does not exist, please run standardize.sh")
                            sys.exit(1)
                        
                        output_path = Path("corpus", f"{lang}.tsv")
                        with openfile(output_path, "a+", encoding="utf-8", newline="") as out_file:
                            out_writer = csv.writer(out_file, delimiter="\t")
                            out_writer.writerow([new_reg, text])
        print(f"{filepath} completed standardization")
    

if __name__ == "__main__":
    if lang2tsv_path.exists():
        with open(lang2tsv_path) as lang2tsv_file:
            lang2tsv = json.load(lang2tsv_file)
    else:
        print(f"CORE lang2tsv file does not exist at {lang2tsv_path}")
        sys.exit(1)
    
    parser = ArgumentParser(prog="Standardize CORE",
                            description="Standardize CORE tsv files to new typology")
    parser.add_argument("--lang", required=True, choices=lang2tsv.keys(),
                        help="language version of CORE to standardize")
    args = parser.parse_args()

    lang_dir = Path(lang2tsv["dir"][args.lang])
    filepaths = lang_dir.glob(lang2tsv["glob"][args.lang])

    if len(filepaths) == 0:
        print(f"no files found according to CORE lang2tsv file at {lang2tsv_path}")
        print("you can run utils_core/download_core.sh and use the default setup of utils_core/lang2tsv.json from the github repository")
        sys.exit(1)
    
    if args.lang == "multi":
        for filepath in filepaths:
            lang = filepath.parts[-2]
            if lang == filepath.stem: # name of .tsv file matches lang name (not train.tsv or test.tsv)
                main(lang, [filepath])
    else:
        main(args.lang, filepaths)