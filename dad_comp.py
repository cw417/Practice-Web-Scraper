# Need to compare files from Dad's 3 music backup HDD's: TB, USB, HDD
# WORKFLOW: 
# TB is master
# HDD may have files that are not on TB or USB
# Need to compare HDD/TB, HDD/USB, USB/TB

import os
import json

TB_fp = ''
USB_fp = ''
HDD_fp = ''
json_fp = 'new_files.json'

TB_files = os.listdir(TB_fp)
USB_files = os.listdir(USB_fp)
HDD_files = os.listdir(HDD_fp)

def compare_HDD_TB():
    # Check if files from HDD are in TB
    not_in = []
    for file in HDD_files:
        if file in TB_files:
            not_in.append(file)
    return not_in
 
 def compare_HDD_USB():
    # Check if files from HDD are in USB
    not_in = []
    for file in HDD_files:
        if file in USB_files:
            not_in.append(file)
        return not_in

def compare_USB_TB():
    # Check if files from HDD are in TB
    not_in = []
    for file in USB_files:
        if file in TB_files:
            not_in.append(file)
    return not_in

def write_new_files(file_dict, json_fp):
    with open(json_fp, 'a') as fp:
        json.dump(file_dict, fp, sort_keys=True, indent=4)

def HDD_TB():
    new_files = compare_HDD_TB()
    write_new_files(new_files, json_fp)

def HDD_USB():
    new_files = compare_HDD_USB()
    write_new_files(new_files, json_fp)

def USB_TB():
    new_files = compare_USB_TB()
    write_new_files(new_files, json_fp)

