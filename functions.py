
import os

import pymongo


cluster = pymongo.MongoClient(os.getenv('CONNECTION_URL'))
database = cluster["UserData"]
collection = database["UserData"]


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def count_duplicates(x, array):
    x = x + "[" + str(array[x]) + "]"
    return x
