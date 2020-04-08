from collections import OrderedDict
from datetime import timedelta


def totalDeaths(db):
    return sum(x.totalDeaths() for x in db.values())


def sumTimeSeries(db, extractor):
    timeSeries = [extractor(x) for x in db.values()]
    keys = sorted(list(set([k for x in timeSeries for k in x.keys()])))
    res = OrderedDict()
    for timeSerie in timeSeries:
        for key in keys:
            val = res.get(key, 0) + timeSerie.get(key, 0)
            res[key] = val
    return res


def findKeyForValue(dictionary, value):
    return inverseLookup(dictionary, value)


def inverseLookup(dictionary, value):
    for key in dictionary:
        if dictionary[key] is value:
            return key
    return None


def perBucketOfDays(dictionary, days=7):
    newDict = OrderedDict()
    index = 0
    total = 0
    count = 0
    for key in dictionary:
        if count is days:
            newDict[index] = total
            index = index + 1
            total = 0
            count = 0

        total = total + dictionary[key]
        count = count + 1

    newDict[index] = total

    return newDict


def perBucketOfDaysListInt(items, days=7):
    newItems = []
    total = 0
    count = 0
    for item in items:
        if count is days:
            newItems.append(total)
            total = 0
            count = 0

        total = total + item
        count = count + 1

    if total > 0:
        newItems.append(total * (days-count+1))

    return newItems


def perBucketOfDaysListDates(items, days=7):
    newItems = []
    total = None
    count = 0
    for item in items:
        if count is days:
            newItems.append(total)
            total = None
            count = 0

        total = item
        count = count + 1

    if total:
        newItems.append(total)

    return newItems

def transposeDays(dictionary, days):
    newDict = OrderedDict()
    for key in dictionary:
        newDict[key+timedelta(days=days)] = dictionary[key]
    return newDict
