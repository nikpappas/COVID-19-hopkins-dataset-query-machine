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
    newKeys = perBucketOfDaysListDates(dictionary.keys(), days)
    newValues = perBucketOfDaysListInt(dictionary.values(), days)
    for i in range(0, len(newKeys)):
        newDict[newKeys[i]] = newValues[i]
    return newDict


def perBucketOfDaysListInt(items, days=7):
    return perBucketOfDaysList(items, days, sum)


def perBucketOfDaysListIntAvg(items, days=7):
    return perBucketOfDaysList(items, days, lambda sublist: sum(sublist) / len(sublist))


def perBucketOfDaysList(items, days, smoothFunc):
    clonedItems = [x for x in items]
    toRet = []
    while len(clonedItems):
        newItem = []
        while len(clonedItems) and len(newItem) < days - 1:
            newItem.append(clonedItems.pop())
        toRet.append(smoothFunc(newItem))

    return list(reversed(toRet))


def perBucketOfDaysListDates(items, days=7):
    clonedItems = [x for x in items]
    toRet = []
    while len(clonedItems):
        newItem = []
        while len(clonedItems) and len(newItem) < days - 1:
            newItem.append(clonedItems.pop())
        toRet.append(newItem[0])

    return list(reversed(toRet))


def transposeDays(dictionary, days):
    newDict = OrderedDict()
    for key in dictionary:
        newDict[key + timedelta(days=days)] = dictionary[key]
    return newDict


def extractLastDaysFromData(x, days):
    totLength = len(x)
    if days < totLength:
        return x[-days:]
    else:
        return x
