import os
from collections import deque, namedtuple


# ToDo handle different input parameters and call the fitting functions
def main():
    pass

DirData = namedtuple("DirData", "file_count file_names dir_names")


def analyze_dir(path):
    files_and_dirs = os.listdir(path)
    file_counter = 0
    file_names, dir_names = list, list
    for entry in files_and_dirs:
        if os.path.isfile(entry):
            pass
        else:
            pass
    return DirData(file_counter, file_names, dir_names)


def do_the_thing():
    directory_dict = dict

    # ToDo add option for user input path
    # deque with absolute path of the file
    dir_deque = deque(os.path.dirname(os.path.abspath(__file__)))
    while dir:
        (file_count, file_list, dir_list) = analyze_dir(dir_deque.popleft())
        

do_the_thing()
