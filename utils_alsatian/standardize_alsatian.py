import sys
from pathlib import Path
import json
import csv

corpus_path = Path("corpus-original", "corpus_alsacien")
# core_path = Path("mappings", "core.json")
cahier_path = Path("mappings", "cahier.json")
output_path = Path("corpus", "al.tsv")

def convert_register(mapping : dict, reg : str, subreg : str) -> str:
    if reg not in mapping:
        print(f"invalid CORE or CAHIER register '{reg}'")
        sys.exit(1)
    
    map_data = mapping[reg]
    if "exceptions" in map_data and subreg in map_data["exceptions"]:
        return map_data["exceptions"][subreg]
    else:
        return map_data["maps"]

def main(): # CAHIER used over CORE, since some documents are not web documents
    # if core_path.exists():
    #     with open(core_path) as core_file:
    #         core_mapping = json.load(core_file)
    # else:
    #     print(f"no CORE mapping found at {core_path}, please reload from github repository")
    #     sys.exit(1)

    if cahier_path.exists():
        with open(cahier_path) as cahier_file:
            cahier_mapping = json.load(cahier_file)
    else:
        print(f"no CAHIER mapping found at {cahier_path}, please reload from github repository")
        sys.exit(1)

    text_paths = corpus_path.glob("*/*.txt")
    
    for text_path in text_paths:
        text_lines = []
        # core_reg = ""
        cahier_reg = ""
        with open(text_path) as text_file:
            for line in text_file:
                line = line.strip()
                if line.startswith("# genreCAHIER: "):
                    cahier_reg = line.removeprefix("# genreCAHIER: ")
                # elif line.startswith("# webRegister: "):
                #     core_reg = line.removeprefix("# webRegister: ")
                elif line and not line.startswith("#"):
                    text_lines.append(line)
    
        if not text_lines:
            print("file contains no text, ignoring")
            continue
        text = " ".join(text_lines)

        if not cahier_reg: # or not core_reg:
            print("\nno CAHIER register metadata found for alsatian text file") # no CORE web register and/or 
            print(f"first 50 characters of text: {text[:50]}")
            sys.exit(1)
        
        cahier_regs = cahier_reg.split(".")
        from_cahier = convert_register(cahier_mapping, cahier_regs[0], cahier_regs[1])

        # if core_reg != "None (not a web document)":
        #     core_regs = core_reg.split(".")
        #     from_core = convert_register(core_mapping, core_regs[0], core_regs[1])
        #     if from_core != from_cahier:
        #         print(f"Classified as {from_core} and {from_cahier}")
        #         print(f"Originally {core_reg} and {cahier_reg}")
        
        if not Path("corpus").exists():
            print("\ncorpus folder does not exist, please run standardize.sh")
            sys.exit(1)

        with open(output_path, "a+", encoding="utf-8", newline="") as corpus_file:
            text_writer = csv.writer(corpus_file, delimiter="\t")
            text_writer.writerow([from_cahier, text])

if __name__ == "__main__":
    print("standardizing alsatian")

    if not corpus_path.exists() or not corpus_path.is_dir() or not any(corpus_path.iterdir()):
        print(f"current filepath to alsatian corpus ({corpus_path}) does not exist, is not a directory, or is empty")
        print("edit the corpus_path variable in utils_alsatian/standardize_alsatian.py to the proper alsatian corpus directory")
        sys.exit(1)

    main()
    print("completed alsatian standardization")