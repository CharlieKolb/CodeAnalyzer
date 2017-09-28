import os
from collections import deque, namedtuple

'''
ToDo Options:
-add_extension .ext line_comment block_comment b_nested_block   additional file types to inspect
-path <C:/some/absolute/path>                                   analysis of a path different from CodeAnalyzer.py
-print_path_absolute                                            reference files by their absolute path instead of their relative one
-exclude_dir <regex>                                            directories to be ignored
-exclude_file <regex>                                           files to be ignored
-count_unknown                                                  also count amount and line/char count of files of unknown type (e.g. csv, png)
-help                                                           help
ToDo Program:
    Use fitting comment syntax
    Optimization: Only do extensive counting if file is in extension list
'''

flag_abs_path = False
flag_count_unknown_extensions = False


DirData = namedtuple("DirData", "amount_of_files file_name_list dir_path_list")

# ToDo: Generalize this for different languages?
brace_only_options = [")", "(", "{", "}", ") {", "){", "};", ");", "{}"]


class LineData:
    def __init__(self, total_line_count=0, commented_out_count=0, blank_count=0, brace_only_count=0, char_count=0):
        self.effective_line_count = total_line_count - commented_out_count - blank_count - brace_only_count
        self.total_line_count = total_line_count
        self.commented_out_count = commented_out_count
        self.blank_count = blank_count
        self.brace_only_count = brace_only_count
        self.char_count = char_count

    def __add__(self, other):
        return LineData(self.total_line_count + other.total_line_count,
                        self.commented_out_count + other.commented_out_count,
                        self.blank_count + other.blank_count,
                        self.brace_only_count + other.brace_only_count,
                        self.char_count + other.char_count)

    def __repr__(self):
        # ToDo Dynamically assign maximum required spaces for formatting
        return ("[effective_line_count = {0:8}, total_count = {1:10}, commented_out_count = {2:8},"
                + " blank_count = {3:8}, brace_only_count = {4:8}, char_count = {5:12}]")\
            .format(self.effective_line_count, self.total_line_count, self.commented_out_count, self.blank_count, self.brace_only_count, self.char_count)

    def as_csv_line(self):
        return "{0},{1},{2},{3},{4},{5}"\
            .format(self.effective_line_count, self.total_line_count, self.commented_out_count, self.blank_count, self.brace_only_count, self.char_count)

    csv_header = "effective,total,commented_out,blank,braces_only,char_count"


class LangData:
    def __init__(self, file_count=0, line_count=0, char_count=0, commented_out_count=0, blank_count=0, brace_only_count=0):
        self.file_count = file_count
        self.line_count = line_count
        self.char_count = char_count
        self.commented_out_count = commented_out_count
        self.blank_count = blank_count
        self.brace_only_count = brace_only_count

    def __repr__(self):
        # ToDo Dynamically assign maximum required spaces for formatting
        return ("[file_count = {0:6}, line_count = {1:8}, char_count = {2:15}, commented_out_count = {3:8},"
                + " blank_count = {4:8}, brace_only_count = {5:8}]")\
            .format(self.file_count, self.line_count, self.char_count, self.commented_out_count, self.blank_count, self.brace_only_count)

# ToDo: Read this from csv
file_extensions = ['.java', '.js', '.c', '.h', '.cpp', '.hpp', '.cs', '.py', '.php']


# ToDo handle different input parameters and call the fitting functions
def main():
    pass


# ToDo:
#   - Distribution of line length?
def parse_file(file):
    line_count, char_count, commented_out_count, blank_count, brace_only_count = 0, 0, 0, 0, 0
    in_block_comment = False
    try:
        for line in file:
            line_count += 1
            char_count += len(line)
            stripped = line.strip()
            if not in_block_comment:
                if len(stripped) == 0:
                    blank_count += 1
                elif len(stripped) <= 3:
                    if stripped in brace_only_options:
                        brace_only_count += 1
                elif stripped.startswith("//"):
                    commented_out_count += 1
                elif stripped.startswith("/*"):
                    commented_out_count += 1
                    in_block_comment = True
                # this checks for start of comment blocks
                # catches a "print(\/*)", but not a "/* print(\/*", which seems like a pretty rare edge case
                elif "/*" in stripped and "\\/*" not in stripped:
                    if "*/" in stripped:
                        commented_out_count += 1
                    else:
                        in_block_comment = True
            else:
                commented_out_count += 1
                if "*/" in line:
                    in_block_comment = False                    
    except UnicodeDecodeError:
        pass
    return LineData(line_count, commented_out_count, blank_count, brace_only_count, char_count)


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
    return DirData(file_counter, file_names, dir_paths)


def analyze_file(path):
    if not os.path.isfile(path):
        raise FileNotFoundError("File {0} not found!".format(path))
    _, extension = os.path.splitext(path)
    name = path if flag_abs_path else os.path.relpath(path)
    # if extension not in file_extensions:
    #    raise ExtensionError(extension)
    file = open(path, 'r')
    # print(path, extension)
    return name, extension, parse_file(file)


def do_the_thing(start_dir=os.path.dirname(os.path.abspath(__file__))):
    dir_dict = {}
    file_dict = {}
    ext_dict = {}
    start_dir = os.path.normpath(os.path.normcase(start_dir))
    # ToDo add option for user input path
    # deque with absolute path of the file
    dir_deque = deque()
    dir_deque.append(start_dir)
    # iterate through all directories and save discovered files in dir_dict
    while dir_deque:
        curr_dir = dir_deque.popleft()
        dir_dict[curr_dir] = analyze_dir(curr_dir)
        for dir_name in dir_dict[curr_dir].dir_path_list:
            dir_deque.append(dir_name)
    for curr_dir, dir_data in dir_dict.items():
        for file_name in dir_data.file_name_list:
            file_name, file_extension, file_data = analyze_file(curr_dir + os.path.sep + file_name)
            if file_data is not None:
                file_dict[file_name] = file_data
                if flag_count_unknown_extensions or file_extension in file_extensions:
                    if file_extension not in ext_dict:
                        ext_dict[file_extension] = file_data
                    else:
                        ext_dict[file_extension] += file_data
    for k, v in ext_dict.items():
        print("{:<8}:  {}".format(k, v))

do_the_thing()
