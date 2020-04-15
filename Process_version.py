"""
File: process.py
Function: Read and Process the tweet file
"""

import re
import json
from collections import Counter
import argparse
import numpy as np

def extract_hagtag(tweet):
    """
    To get a the frequency of hashtags in all tweets records
    :param tweet: a dict containing all the  information of one tweet
    :return: an ordered dict of hashtags based on frequency
    """
    hashtags = []
    information_list = tweet["doc"]["entities"]["hashtags"]
    hash_tags_num = len(information_list)
    if hash_tags_num != 0:
        for num in range(hash_tags_num):
            if information_list[num]["text"].isalpha():
                hash_tag = information_list[num]["text"].lower()
                hashtags.append(hash_tag)
    return hashtags


def extract_language(tweet):
    """
    To summarize the frequency of the languange used in tweet records
    :param tweets: a dict containing all the information of one tweet record
    :return: a dict based on the frequency of languange used
    """
    lan_information = tweet["doc"]["lang"]
    return lan_information


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

def reform_ordereddict(list):
    counter_item = Counter()
    for item in list:
        counter_item += item
    return counter_item

def get_row_num(file_name):
    with open(file_name, "r") as file:
        row_count = 0
        line = file.readline()
        while line:
            row_count += 1
            line = file.readline()
    return row_count

def preprocess_tweet(tweet):
    """
    Remove the punctuation to make it available for json
    :param tweet:
    :return:
    """
    remove_pun = ","
    pattern = re.compile(r'[%s]$' % remove_pun)
    init_content = re.sub(pattern, "", tweet)
    twitter_content = json.loads(init_content)
    return twitter_content