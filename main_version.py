"""
File: main.py
function: main function
"""

from Process_version import *
import numpy as np
from mpi4py import MPI
from collections import Counter
import argparse

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def main():
    file_path = parse_argment()
    if rank == 0:
        row_count = get_row_num(file_path)
        end_point = np.linspace(0, row_count, size + 1)
    else:
        end_point = None

    end_data = comm.bcast(end_point, root=0)

    for id in range(size):
        if rank == id:
            node_hashtag_dict = {}
            node_lan_dict = {}
            start_points = int(end_data[rank])
            end_points = int(end_data[rank + 1])


            with open(file_path, "r") as file:
                count = 0
                for line in file:
                    if not start_points <= count < end_points:
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
                                if tag in node_hashtag_dict.keys():
                                    node_hashtag_dict[tag] += 1
                                else:
                                    node_hashtag_dict[tag] = 1
                        if lan in node_lan_dict.keys():
                            node_lan_dict[lan] += 1
                        else:
                            node_lan_dict[lan] = 1

                        count += 1

    hashtag_data = comm.gather(node_hashtag_dict, root=0)
    lan_data = comm.gather(node_lan_dict, root=0)

    summarized_hashtag_dict = Counter()
    summarized_lan_dict = Counter()
    if rank == 0:
        for hashtag_dict in hashtag_data:
            summarized_hashtag_dict.update(hashtag_dict)
        for lan_dict in lan_data:
            summarized_lan_dict.update(lan_dict)
        print("The Top 10 Hash tags are: {}".format(summarized_hashtag_dict.most_common(10)))
        print("The Top 10 Used Language are: {}".format(summarized_lan_dict.most_common(10)))



if __name__ == "__main__":
    main()
