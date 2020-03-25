from collections import OrderedDict
from datetime import timedelta, datetime

class CountryData(object):
    def __init__(self, country, population, deathsAccPerDay):
        self.country = country
        self.population = population
        self.deathsAccPerDate = deathsAccPerDay

    def getDeathsPerDate(self):
        res = {}
        for day in self.deathsAccPerDate:
            prevDay = day - timedelta(days=1)
            if prevDay not in self.deathsAccPerDate:
               res[day] = self.deathsAccPerDate[day]
            else:
                res[day] = self.deathsAccPerDate[day] - self.deathsAccPerDate[prevDay]
        return res

    def getTotalDeaths(self):
        return max(self.deathsAccPerDate.values())

    def deathsAccPerdayRatio(self):
        if self.population:
            return OrderedDict([(k, self.deathsAccPerDate[k] / self.population) for k in self.deathsAccPerDate])

    def appendDeaths(self, deaths):
        for k in deaths:
            self.deathsAccPerDate[k] = self.deathsAccPerDate[k] + deaths[k]




def getPrevDayKey(k):
    day = parseDateKey(k)


def parseDateKey(k):
    tokens = k.split("/");
    return datetime.date(tokens[0],tokens[1],tokens[2])

