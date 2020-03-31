from collections import OrderedDict


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
