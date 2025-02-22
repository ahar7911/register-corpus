import sys
from pathlib import Path
import json
import csv

alsatian_path = Path("corpus-original/corpus_alsacien")

def convert_register(mapping : dict, reg : str, subreg : str) -> str:
    if reg not in mapping:
        print(f"invalid CORE or CAHIER register '{reg}'", file=sys.stderr)
        sys.exit(1)
    
    map_data = mapping[reg]
    # if subregister is an exception to register mapping
    if "exceptions" in map_data and subreg in map_data["exceptions"]:
        return map_data["exceptions"][subreg]
    else:
        return map_data["maps"]

def main(): # CAHIER used over CORE, since some documents are not web documents
    # with open(Path("mappings/core.json")) as core_file:
    #   core_mapping = json.load(core_file)

    with open(Path("mappings/cahier.json")) as cahier_file: # loads mapping as a dict
        cahier_mapping = json.load(cahier_file)
    
    corpus_dir = Path("corpus")
    if not corpus_dir.exists(): # make corpus dir if does not exist
        corpus_dir.mkdir()
    
    al_tsv_path = corpus_dir / "al.tsv"
    al_tsv_path.unlink(missing_ok=True) # remove corpus/al.tsv if already exists

    text_paths = alsatian_path.glob("*/*.txt")
    
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

        if not text_lines: # no text found
            print("file contains no text, ignoring")
            continue
        text = " ".join(text_lines)

        if not cahier_reg: # or not core_reg:
            print("\nno CAHIER register metadata found for alsatian text file", file=sys.stderr) # no CORE web register and/or 
            print(f"first 50 characters of text: {text[:50]}", file=sys.stderr)
            sys.exit(1)
        
        cahier_regs = cahier_reg.split(".")
        from_cahier = convert_register(cahier_mapping, cahier_regs[0], cahier_regs[1])

        # compare registers obtained from core vs. cahier conversion, if different and not a web document
        # if core_reg != "None (not a web document)":
        #     core_regs = core_reg.split(".")
        #     from_core = convert_register(core_mapping, core_regs[0], core_regs[1])
        #     if from_core != from_cahier:
        #         print(f"Classified as {from_core} from CORE, originally {core_reg} ")
        #         print(f"Classified as {from_cahier} from CAHIER, originally {cahier_reg}")
        #         print()

        with open(al_tsv_path, "a+", encoding="utf-8", newline="") as corpus_file:
            text_writer = csv.writer(corpus_file, delimiter="\t")
            text_writer.writerow([from_cahier, text])

if __name__ == "__main__":
    print("standardizing alsatian")

    if not alsatian_path.exists() or not alsatian_path.is_dir() or not any(alsatian_path.iterdir()):
        print(f"current filepath to alsatian corpus ({alsatian_path}) does not exist, is not a directory, or is empty", file=sys.stderr)
        print("edit the alsatian_path variable in utils/alsatian/standardize_alsatian.py to the proper alsatian corpus directory", file=sys.stderr)
        sys.exit(1)

    main()
    print("completed alsatian standardization")