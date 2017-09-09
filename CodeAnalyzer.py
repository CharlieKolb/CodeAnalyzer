import os
from collections import deque, namedtuple

DictData = namedtuple("DictData", "amount_of_files file_name_list dir_path_list")


# ToDo handle different input parameters and call the fitting functions
def main():
    pass


def analyze_dir(path):
    files_and_dirs = os.listdir(path)
    file_counter = 0
    file_names, dir_paths = [], []
    for entry in files_and_dirs:
        if os.path.isfile(entry):
            pass
        else:
            pass
    return DictData(file_counter, file_names, dir_paths)


def do_the_thing():
    dir_dict = {}

    # ToDo add option for user input path
    # deque with absolute path of the file
    dir_deque = deque()
    dir_deque.append(os.path.dirname(os.path.abspath(__file__)))
    while dir_deque:
        curr_dir = dir_deque.popleft()
        dir_dict[curr_dir] = analyze_dir(curr_dir)
        for dir_name in dir_dict[curr_dir].dir_path_list:
            dir_deque.append(dir_name)

do_the_thing()
