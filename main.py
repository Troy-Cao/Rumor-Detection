"""
File: main.py
function: main function
"""
from Process import *
import time
# from mpi4py import MPI
# from mpi4py.futures import MPIPoolExecutor
from collections import Counter
import argparse


# comm = MPI.COMM_WORLD
# size = comm.Get_size()

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
    # split_contents = split_the_list(contents, size)  # split the original data
    # distributed_data = comm.scatter(split_contents, root=0)  # distribute the file into different calculation nodes
    hash_tags_ordered_dict = summarize_hagtags(contents)
    # hastag_total_list = comm.gather(hash_tags_ordered_dict, root=0)
    # hastag_total_dict = reform_ordereddict(hastag_total_list)
    print("The Top 10 Hash tags are: {}".format(hash_tags_ordered_dict.most_common(10)))
    lan_ordered_dict = summarize_language(contents)
    # lan_total_list = comm.gather(lan_ordered_dict)
    # lan_total_dict = reform_ordereddict(lan_total_list)
    print("The Top 10 Used Language are: {}".format(lan_ordered_dict.most_common(10)))
    end_time = time.time()
    print("The Used time is: {} sec".format(end_time - start_time))

    # executor = MPIPoolExecutor(max_workers=size)
    # start_time = time.time()
    # contents = executor.submit(read_file, file_path).result()
    # hash_tags_ordered_dict = executor.map(summarize_hagtags, contents).result()
    # lan_ordered_dict = executor.map(summarize_language, contents).result()
    # print("The Top 10 Hash Tags are: {}".format(hash_tags_ordered_dict.most_common(10)))
    # print("The Top 10 Language used are: {}".format(lan_ordered_dict.most_common(10)))
    # end_time = time.time()
    # print("The Whole Process Time Consuming: {} sec".format(end_time - start_time))


if __name__ == "__main__":
    main()
