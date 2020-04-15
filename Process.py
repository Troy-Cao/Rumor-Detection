"""
File: process.py
Function: Read and Process the tweet file
"""

import re
import json
import collections

def read_file(file_path):
    """
    :param file_path: The path of the tweet file
    :return: a list containing all the tweets information
    """
    tweet_contents = []
    if "bigTwitter.json" not in file_path:
        with open(file_path, mode="r", encoding='utf-8') as f:
            contents = f.readlines()
            remove_pun = ","
            pattern = re.compile(r'[%s]$' % remove_pun)
            for i in range(len(contents) - 1):
                init_content = re.sub(pattern, "", contents[i+1])
                content = json.loads(init_content)
                tweet_contents.append(content)
    else:
        with open(file_path, mode="r", encoding="utf-8") as f:
            tweets = json.loads(f)
            records = tweets["rows"]
            for record in records:
                tweet_contents.append(record)
    return tweet_contents

def summarize_hagtags(tweets_list):
    """
    To get a the frequency of hashtags in all tweets records
    :param tweet_list: a list containing all the tweet information
    :return: an ordered dict of hashtags based on frequency
    """
    hash_tags_dict = {}
    for tweet in tweets_list:
        information_list = tweet["doc"]["entities"]["hashtags"]
        hash_tags_num = len(information_list)
        if hash_tags_num != 0:
            for num in range(hash_tags_num):
                if information_list[num]["text"].isalpha():
                    hash_tags = information_list[num]["text"].lower()
                    if hash_tags not in hash_tags_dict.keys():
                        hash_tags_dict[hash_tags] = 1
                    else:
                        hash_tags_dict[hash_tags] += 1
    ordered_hashtags_dict = collections.Counter(hash_tags_dict)
    return ordered_hashtags_dict

def summarize_language(tweets_list):
    """
    To summarize the frequency of the languange used in tweet records
    :param tweets_list:
    :return: a dict based on the frequency of languange used
    """
    language_dict = {}
    for tweet in tweets_list:
        lan_information = tweet["doc"]["lang"]
        if lan_information not in language_dict.keys():
            language_dict[lan_information] = 1
        else:
            language_dict[lan_information] += 1
    ordered_lan_dict = collections.Counter(language_dict)
    return ordered_lan_dict

def hash_tag_statistic_tool(hash_tag_dict):
    """
    Purpose on performing analysis on the init_ordered dict
    :param hash_tag_dict:
    :return:
    """
    hash_tags_list = list(hash_tag_dict.keys())
    hashtag_num = len(hash_tags_list)
    print("The Current Types of Hash Tags are: {}".format(hashtag_num))
    print(hash_tags_list)

def split_the_list(input_list, size):
    """
    Split the list into sub-list of fixed number
    :param list:
    :param size: the number of split sub-lists
    :return:
    """
    sublist_set = []
    h = 0
    for i in range(0, size):
        m = int(len(input_list) / size)
        if i == size - 1:
            obj = input_list[h:]
        else:
            obj = input_list[h:h+m]
        sublist_set.append(obj)
        h = h + m
    return sublist_set







