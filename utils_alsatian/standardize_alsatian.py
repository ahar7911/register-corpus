import glob
import json
import csv

FILEPATH = "corpus-original/corpus_alsacien/"

def convert_register(mapping : dict, reg : str, subreg : str) -> str:
    if reg not in mapping:
        raise Exception(f"Invalid CORE or CAHIER register '{reg}'")
    
    map_data = mapping[reg]
    if "exceptions" in map_data and subreg in map_data["exceptions"]:
        return map_data["exceptions"][subreg]
    else:
        return map_data["maps"]

def main():
    # with open("mappings/core.json") as core_file:
    #     core_mapping = json.load(core_file)

    # CAHIER used over CORE, since some documents are not web documents
    with open("mappings/cahier.json") as cahier_file:
        cahier_mapping = json.load(cahier_file)
    filepaths = glob.glob(FILEPATH + "*/*.txt")
    
    for filepath in filepaths:
        text_lines = []
        # core_reg = ""
        cahier_reg = ""
        with open(filepath) as text_file:
            for line in text_file:
                line = line.strip()
                if line.startswith("# genreCAHIER: "):
                    cahier_reg = line.removeprefix("# genreCAHIER: ")
                # elif line.startswith("# webRegister: "):
                #     core_reg = line.removeprefix("# webRegister: ")
                elif line and not line.startswith("#"):
                    text_lines.append(line)
    
        if not text_lines:
            print("ignoring blank text")
            continue
        text = " ".join(text_lines)

        if not cahier_reg: # or not core_reg:
            raise Exception("No CORE web register and/or no CAHIER register metadata found")
        
        cahier_regs = cahier_reg.split(".")
        from_cahier = convert_register(cahier_mapping, cahier_regs[0], cahier_regs[1])

        # if core_reg != "None (not a web document)":
        #     core_regs = core_reg.split(".")
        #     from_core = convert_register(core_mapping, core_regs[0], core_regs[1])
        #     if from_core != from_cahier:
        #         print(f"Classified as {from_core} and {from_cahier}")
        #         print(f"Originally {core_reg} and {cahier_reg}")
        with open(f"corpus/al.tsv", "a+", encoding="utf-8", newline="") as corpus_file:
            text_writer = csv.writer(corpus_file, delimiter="\t")
            text_writer.writerow([from_cahier, text])

if __name__ == "__main__":
    print("standardizing alsatian")
    main()
    print("completed alsatian standardization")