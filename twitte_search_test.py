"""
File: main.py
function: main function
"""
from Process import *
import time
from collections import Counter
import argparse


def reform_ordereddict(list):
    counter_item = Counter()
    for item in list:
        counter_item += item
    return counter_item

def parse_argment():
    """
    Parse the argment of the command line
    :return:
    """
    parser = argparse.ArgumentParser(description="Read The File From Command Line")
    parser.add_argument("-i", action="store_true", help="Input the File")
    parser.add_argument("filepath", help="File path", type=str)

    args = parser.parse_args()

    file_path = args.filepath
    return file_path


def main():
    start_time = time.time()
    file_path = "/Users/troycao/Documents/GitHub/COMP90024_assignment1/Data/smallTwitter.json"
    contents = read_file(file_path)
    hash_tags_ordered_dict = summarize_hagtags(contents)
    print("The Top 10 Hash tags are: {}".format(hash_tags_ordered_dict.most_common(10)))
    lan_ordered_dict = summarize_language(contents)

    print("The Top 10 Used Language are: {}".format(lan_ordered_dict.most_common(10)))
    end_time = time.time()
    print("The Used time is: {} sec".format(end_time - start_time))


if __name__ == "__main__":
    main()