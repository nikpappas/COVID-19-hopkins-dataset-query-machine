from collections import OrderedDict
from datetime import timedelta, datetime
from core.mathUtils import differentiate_distinct
import core.aggregations as agg


class CountryData(object):
    def __init__(self, country, population, deathsAccPerDate, confirmedAccPerDate, recoveredAccPerDate):
        self.country = country
        self.population = population
        self.deathsAccPerDate = deathsAccPerDate
        self.confirmedAccPerDate = confirmedAccPerDate
        self.recoveredAccPerDate = recoveredAccPerDate

    def deathsPerDate(self):
        return perDate(self.deathsAccPerDate)

    def recoveredPerDate(self):
        return perDate(self.recoveredAccPerDate)

    def confirmedPerDate(self):
        return perDate(self.confirmedAccPerDate)

    def totalDeaths(self):
        return total(self.deathsAccPerDate)

    def totalRecovered(self):
        return total(self.recoveredAccPerDate)

    def totalConfirmed(self):
        return total(self.confirmedAccPerDate)

    def deathsAccPerDateRatio(self):
        return seriesPerRatio(self.deathsAccPerDate, self.population)

    def deathsPerDateRatio(self):
        return seriesPerRatio(self.deathsPerDate(), self.population)

    def confirmedAccPerDateRatio(self):
        return seriesPerRatio(self.confirmedAccPerDate, self.population)

    def confirmedPerDateRatio(self):
        return seriesPerRatio(self.confirmedPerDate(), self.population)

    def recoveredAccPerDateRatio(self):
        return seriesPerRatio(self.recoveredAccPerDate, self.population)

    def recoveredPerDateRatio(self):
        return seriesPerRatio(self.recoveredPerDate(), self.population)


def perDate(accStat):
    return differentiate_distinct(accStat, lambda day: day - timedelta(days=1))


def total(accStat):
    return max(accStat.values())

def seriesPerRatio(accStat, population):
    if population:
        return OrderedDict([(k, accStat[k] / population) for k in accStat])


