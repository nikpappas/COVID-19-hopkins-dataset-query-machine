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

    def deathsAccPerDateRatio(self, perPeople=1):
        return seriesPerRatio(self.deathsAccPerDate, self.population, perPeople)

    def deathsPerDateRatio(self, perPeople=1):
        return seriesPerRatio(self.deathsPerDate(), self.population, perPeople)

    def confirmedAccPerDateRatio(self, perPeople=1):
        return seriesPerRatio(self.confirmedAccPerDate, self.population, perPeople)

    def confirmedPerDateRatio(self, perPeople=1):
        return seriesPerRatio(self.confirmedPerDate(), self.population, perPeople)

    def recoveredAccPerDateRatio(self, perPeople=1):
        return seriesPerRatio(self.recoveredAccPerDate, self.population, perPeople)

    def recoveredPerDateRatio(self, perPeople=1):
        return seriesPerRatio(self.recoveredPerDate(), self.population, perPeople)


def perDate(accStat):
    return differentiate_distinct(accStat, lambda day: day - timedelta(days=1))


def total(accStat):
    return max(accStat.values())


def seriesPerRatio(accStat, population, perPeople):
    if population:
        return OrderedDict([(k, perPeople * accStat[k] / population) for k in accStat])
