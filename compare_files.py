# This is a simple script to iterate through two folders
# and write the names of all contained files
# to a separte json file

import os
import json

path_1 = 'test'
path_2 = 'test2'
json_fp = 'new_files.json'

def compare_files(path_1, path_2):
    # Compares files in two folders and returns 
    files_1 = os.listdir(path_1)
    files_2 = os.listdir(path_2)
    file_list_1 = []
    file_list_2 = []
    file_dict = {}
    for file1 in files_1:
        if file1 not in files_2:
            file_list_2.append(file1)
    for file2 in files_2:
        if file2 not in files_1:
            file_list_2.append(file2)
    file_dict.update({path_1: file_list_1,
                    path_2: file_list_2})
    return file_dict

def write_new_files(file_dict, json_fp):
    with open(json_fp, 'a') as fp:
        json.dump(file_dict, fp, sort_keys=True, indent=4)


new_files = compare_files(path_1, path_2)
write_new_files(new_files, json_fp)