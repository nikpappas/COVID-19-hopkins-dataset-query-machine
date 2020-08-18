import datetime as dt
import core.aggregations as agg

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


def printForCountry(country, *strings):
    print("[", country, "] -", strings)

def printAggregates(country, maxPerDate, lastPerDate, valuesPerDate, numOfDaysForAggregatsion, label):
    print('_______________________________')
    print(label)
    print('_______________________________')
    printForCountry(country.country, "maxPerDate:", maxPerDate)
    printForCountry(country.country, "lastPerDate:", lastPerDate)
    last10Days = list(valuesPerDate.values())[-numOfDaysForAggregatsion:]
    l10DaysBeforeLast10DAys = list(valuesPerDate.values())[-numOfDaysForAggregatsion * 2:-numOfDaysForAggregatsion]
    deathsLast10Days = sum(last10Days)
    prevDeathsLast10Days = sum(l10DaysBeforeLast10DAys)
    printForCountry(country.country, "Last10Days [" + str(numOfDaysForAggregatsion) + "]:", deathsLast10Days)
    printForCountry(country.country, "prevLast10Days [" + str(numOfDaysForAggregatsion) + "]:",
                    prevDeathsLast10Days)
    print('===============================')



def smoothenCurve(x, y, granularity):
    if granularity > 1:
        x = agg.perBucketOfDaysListDates(x, days=granularity)
        y = agg.perBucketOfDaysListIntAvg(y, days=granularity)
    return x, y

def mapToCountries(countries, countryName):
    if isinstance(countryName, list):
        return [countries[x] for x in countryName]
    else:
        return [countries[countryName]]
