import datetime as dt
from os import walk, path


def parseInt(string):
    try:
        return int(string)
    except ValueError:
        return 0


def parseDate(string):
    dateTokens = [int(x) for x in string.split("/")]
    return dt.date(int(dateTokens[2]) + 2000, int(dateTokens[0]), int(dateTokens[1]))


def addWithDefault(dict, key, default, toAdd):
    dict[key] = dict.get(key, default) + toAdd


def getCsvFilesPaths(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filter(lambda x: '.csv' in x, filenames))
    return [path.join(dir, filename) for filename in f]
