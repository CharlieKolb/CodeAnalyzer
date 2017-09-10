import os
from collections import deque, namedtuple

DictData = namedtuple("DictData", "amount_of_files file_name_list dir_path_list")


# ToDo handle different input parameters and call the fitting functions
def main():
    pass


def analyze_dir(path):
    # print(path)
    files_and_dirs = os.listdir(path)
    file_counter = 0
    file_names, dir_paths = [], []
    for entry in files_and_dirs:
        # print("?: " + path + os.path.sep + entry)
        if os.path.isfile(path + os.path.sep + entry):
            # print("file: " + os.path.basename(entry))
            file_names.append(os.path.basename(entry))
            file_counter += 1
        else:
            # print("dir: " + path + os.path.sep + entry)
            dir_paths.append(path + os.path.sep + entry)
    return DictData(file_counter, file_names, dir_paths)


def do_the_thing(start_dir=os.path.dirname(os.path.abspath(__file__))):
    dir_dict = {}
    start_dir = start_dir
    # ToDo add option for user input path
    # deque with absolute path of the file
    dir_deque = deque()
    dir_deque.append(start_dir)
    while dir_deque:
        curr_dir = dir_deque.popleft()
        dir_dict[curr_dir] = analyze_dir(curr_dir)
        for dir_name in dir_dict[curr_dir].dir_path_list:
            dir_deque.append(dir_name)

    for k in dir_dict:
        print(k, dir_dict[k])

do_the_thing()
