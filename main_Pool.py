"""
File: mainPool.py
Function: Parallelizing the process using MPIPoolExecutor
"""

from Process_version import *
import numpy as np
from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor
from collections import Counter
import argparse

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


def process_pipeline(argument_tuple):
    file_name = argument_tuple[0]
    start_point = argument_tuple[1][0]
    end_point = argument_tuple[1][1]

    result = []
    hash_tag_dict = {}
    lan_dict = {}

    with open(file_name, "r") as file:
        count = 0
        for line in file:
            if not start_point <= count < end_point:
                count += 1
                continue

            line = line.strip()
            if line.endswith(","):
                tweet_content = preprocess_tweet(line)
                try:
                    tags = extract_hagtag(tweet_content)
                    lan = extract_language(tweet_content)
                except:
                    continue

            if tags:
                for tag in tags:
                    if tag in hash_tag_dict.keys():
                        hash_tag_dict[tag] += 1
                    else:
                        hash_tag_dict[tag] = 1
            if lan in lan_dict.keys():
                lan_dict[lan] += 1
            else:
                lan_dict[lan] = 1
            count += 1
        result.append(hash_tag_dict)
        result.append(lan_dict)
    return result

def zip_arguments(file, end_points):
    points_list = []
    for i in range(len(end_points) - 1):
        temp = (end_points[i], end_points[i + 1])
        points_list.append((file, temp))
    return points_list

def main():
    file_name = parse_argment()
    row_num = get_row_num(file_name)
    end_points_list = np.linspace(0, row_num, size + 1)
    summarized_hash_tag_dict = Counter()
    summarized_lan_dict = Counter()

    argument_list = zip_arguments(file_name, end_points_list)
    executor = MPIPoolExecutor()
    results = executor.map(process_pipeline, argument_list)
    for result in results:
        summarized_hash_tag_dict.update(result[0])
        summarized_lan_dict.update(result[1])
    print("The Top 10 Hash tags are: {}".format(summarized_hash_tag_dict.most_common(10)))
    print("The Top 10 Used Language are: {}".format(summarized_lan_dict.most_common(10)))

if __name__ == "__main__":
    main()

