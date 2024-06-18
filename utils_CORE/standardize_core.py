from argparse import ArgumentParser
import sys
import os
import gzip
import csv
import json


def openfile(filename : str, mode='r', encoding=None, newline=None):
    if filename.endswith('.gz'):
        return gzip.open(filename, mode, encoding=encoding, newline=newline) 
    else:
        return open(filename, mode, encoding=encoding, newline=newline)


def convert_register(reg_str : str, core_mappings : dict) -> str:
    regs = reg_str.split(' ')

    if args.finnish: # FinCORE
        if regs[0] == "MT": # remove machine translation tag if there
            regs = regs[1:]
        regs = regs[::-1]
    if len(regs) == 0 or regs[0] not in core_mappings: # empty register or bad string
        return None
    
    reg_map = core_mappings[regs[0]]
    if 'maps' in reg_map: # register singly maps to a new register, along with all subregisters
        if len(regs) == 1 or all([r in reg_map['subcategories'] for r in regs[1:]]): # text has no subregister, or all subregisters are under register
            return reg_map['maps']
    if len(regs) == 2: # now only possible mapping is from a subregister (must be register with single subregister)
        if regs[1] in core_mappings or regs[1] not in reg_map['subcategories']: # subregister is either actually a register (hybrid register) or incorrect subregister
            return None
        sub_reg_map = reg_map['subcategories'][regs[1]]
        if 'maps' in sub_reg_map: # subregister maps
            return sub_reg_map['maps']
    return None # register or subregister does not map


def main(map_path : str, src_filenames : list[str], dst_path : str):
    with openfile(map_path) as file: # loads mappings as dict
        core_mappings = json.load(file)
    
    # https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
    maxInt = sys.maxsize
    while True: # decrease the maxInt value by factor 10 as long as the OverflowError occurs
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt/10)
    
    for filename in src_filenames:
        with openfile(filename, 'rt', 'utf-8') as src_file:
            src_reader = csv.reader(src_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in src_reader:
                reg_str, text = row[0], row[-1] # for some files, metadata in between
                new_reg = convert_register(reg_str, core_mappings)
                if new_reg is not None:
                    with openfile(dst_path, 'at+', 'utf-8', '') as dst_file:
                        dst_writer = csv.writer(dst_file, delimiter='\t')
                        dst_writer.writerow([new_reg, text])
        print(f'{filename} completed standardization')
    

if __name__ == '__main__':
    parser = ArgumentParser(prog='Standardize CORE',
                            description="Standardize CORE tsv files to new typology")
    parser.add_argument("--map_path", required=True,
                        help="path to json file of typology mappings")
    parser.add_argument("--src_path", required=True,
                        help="path to the directory containing all files to be standardized")
    parser.add_argument("--file_ext", required=True,
                        help="common file extension of files in the directory that need to be standardized")
    parser.add_argument("--dst_path", required=True,
                        help="path to file that will hold standardized data")
    parser.add_argument("--finnish", action="store_true", help="original data is FinCORE (registers will be written as (subregister, register) and MT register exists)")

    args = parser.parse_args()

    # error checking
    if not args.map_path.endswith('.json') or not os.path.exists(args.map_path):
        raise Exception('Map filepath is not a .json file or file does not exist')
    if not args.src_path.endswith('/') or not os.path.exists(args.src_path):
        raise Exception('Source filepath does not exist or does not end with a / character')
    if args.file_ext[0] != '.':
        raise Exception('File extension is not valid (does not start with a period)')
    if not args.dst_path.endswith('.tsv'):
        raise Exception('Destination file must be a .tsv file')
    
    src_filepaths = []
    for file in os.listdir(args.src_path):
        if file.endswith(args.file_ext):
            src_filepaths.append(args.src_path + file)
    
    if len(src_filepaths) == 0:
        raise Exception('No files found with specified extension')

    main(args.map_path, src_filepaths, args.dst_path)
