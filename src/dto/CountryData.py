from collections import OrderedDict
from datetime import timedelta, datetime
from core.mathUtils import differentiate_distinct

class CountryData(object):
    def __init__(self, country, population, deathsAccPerDate, confirmedAccPerDate, recoveredAccPerDate):
        self.country = country
        self.population = population
        self.deathsAccPerDate = deathsAccPerDate
        self.confirmedAccPerDate = confirmedAccPerDate
        self.recoveredAccPerDate = recoveredAccPerDate

    def getDeathsPerDate(self):
        return differentiate_distinct(self.deathsAccPerDate, lambda day: day - timedelta(days=1))

    def getTotalDeaths(self):
        return max(self.deathsAccPerDate.values())

    def deathsAccPerDateRatio(self):
        if self.population:
            return OrderedDict([(k, self.deathsAccPerDate[k] / self.population) for k in self.deathsAccPerDate])

    def deathsPerDateRatio(self):
        if self.population:
            return OrderedDict([(k, self.getDeathsPerDate()[k] / self.population) for k in self.getDeathsPerDate()])
