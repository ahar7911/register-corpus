from argparse import ArgumentParser
import sys
import os
import glob
import gzip
import csv
import json


def openfile(filename : str, mode="r", encoding=None, newline=None):
    if filename.endswith(".gz"):
        return gzip.open(filename, mode, encoding=encoding, newline=newline) 
    else:
        return open(filename, mode, encoding=encoding, newline=newline)


def convert_register(reg_str : str, core_mappings : dict, lang : str) -> str:
    regs = [reg.upper() for reg in reg_str.split(" ")]

    if "MT" in regs: # FinCORE and mutlilang CORE
        regs.remove("MT")
    if "" in regs: # multilang CORE formatting error
        regs.remove("")
    if lang == "fi": # FinCORE has subregisters first
        regs = regs[::-1]
    if len(regs) == 0 or regs[0] not in core_mappings: # empty register or bad string
        return None
    
    reg_map = core_mappings[regs[0]]
    if "maps" in reg_map: # register singly maps to a new register, along with all subregisters
        if len(regs) == 1 or all([r in reg_map["subcategories"] for r in regs[1:]]): # text has no subregister, or all subregisters are under register
            return reg_map["maps"]
    if len(regs) == 2: # now only possible mapping is from a subregister (must be register with single subregister)
        if regs[1] in core_mappings or regs[1] not in reg_map["subcategories"]: # subregister is either actually a register (hybrid register) or incorrect subregister
            return None
        sub_reg_map = reg_map["subcategories"][regs[1]]
        if "maps" in sub_reg_map: # subregister maps
            return sub_reg_map["maps"]
    return None # register or subregister does not map


def main(lang : str, filepaths : list[str]):
    with openfile("utils_CORE/core_mappings.json") as file: # loads mappings as dict
        core_mappings = json.load(file)
    
    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    maxInt = sys.maxsize
    while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    for filepath in filepaths:
        with openfile(filepath, "rt", "utf-8") as src_file:
            src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in src_reader:
                reg_str, text = row[0], row[-1] # for some files, metadata in between
                if text != "":
                    new_reg = convert_register(reg_str, core_mappings, lang)
                    if new_reg is not None:
                        with openfile(f"corpus/{lang}.tsv", "at+", "utf-8", "") as dst_file:
                            dst_writer = csv.writer(dst_file, delimiter="\t")
                            dst_writer.writerow([new_reg, text])
        print(f"{filepath} completed standardization")
    

if __name__ == "__main__":
    with open("utils_CORE/lang2tsv.json") as file:
        lang2tsv = json.load(file)
    
    parser = ArgumentParser(prog="Standardize CORE",
                            description="Standardize CORE tsv files to new typology")
    parser.add_argument("--lang", required=True, choices=lang2tsv.keys(),
                        help="language version of CORE to standardize")
    args = parser.parse_args()

    filepath = lang2tsv[args.lang]
    
    filepaths = glob.glob(filepath)
    if len(filepaths) == 0:
        raise Exception("No files found according to utils_CORE/lang2tsv.json")
    
    if args.lang != "multi":
        main(args.lang, filepaths)
    else:
        for filepath in filepaths:
            parts = filepath.split(os.sep)
            lang = parts[-2]
            filename, ext = os.path.splitext(parts[-1])
            if lang == filename: # where the name of .tsv file matches lang name
                main(lang, [filepath])