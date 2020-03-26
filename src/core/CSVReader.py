from os import walk, path
import csv
import datetime as dt
from collections import OrderedDict
import matplotlib.pyplot as plt
from dto.CountryData import CountryData
from population.populations import populations
from country import countries as c
from core.utils import parseInt
import core.Aggregations as agg

COVID_19_DIR = '../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
COVID_19_DEATHS_FILE = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
COVID_19_CONFIRMED_FILE = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
COVID_19_RECOVERED_FILE = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

COI = [
    c.greece,
    c.italy,
    c.spain,
    c.uk,
    c.us,
    c.china
]


def warn(s):
    print('WARN: ' + str(s))


def main():
    countries, series = loadCountries()
    # plotItaly(countries)

    countryData = [countries[x] for x in COI]
    plt.subplot(2, 1, 1)
    for country in countryData:
        deathsPerDateAcc = country.deathsAccPerDate
        print("Total deaths: " + country.country + " | " + str(max(deathsPerDateAcc.values())))
        plt.plot(
            list(deathsPerDateAcc.keys())[30:-1],
            list(deathsPerDateAcc.values())[30:-1],
            label=country.country + " deaths Acc"
        )
    plt.legend()
    plt.title('Deaths accumulative', fontsize=16)
    plt.subplot(2, 1, 2)
    for country in countryData:
        deathsPerDate = country.getDeathsPerDate()
        print("Max  deathsperDate: " + country.country + " | " + str(max(deathsPerDate.values())))
        print("Last deathsperDate: " + country.country + " | " + str(list(deathsPerDate.values())[-1]))
        plt.plot(
            list(deathsPerDate.keys())[30:-1],
            list(deathsPerDate.values())[30:-1],
            label=country.country + " deaths"
        )
    plt.legend()
    plt.title('Deaths per day', fontsize=16)
    plt.show()
    print(agg.totalDeaths(countries))


class DbEntry:
    def __init__(self, row, date):
        self.country = row.get('Country/Region', row.get('Country_Region'))
        self.state = row.get('Province/State', row.get('Province_State'))
        self.deaths = parseInt(row['Deaths'])
        self.confirmed = parseInt(row['Confirmed'])
        self.recovered = parseInt(row['Recovered'])
        self.date = date


def parseDate(string):
    dateTokens = [int(x) for x in string.split("/")]
    return dt.date(int(dateTokens[2]) + 2000, int(dateTokens[0]), int(dateTokens[1]))


def readStats(file):
    with open(file) as csvfile:
        return [DbEntry(x) for x in csv.DictReader(csvfile)]


def loadCountries():
    countries = readDailyReports()
    countriesSeries = readSeries()
    return countries, countriesSeries


def getCsvFilesPaths(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend(filter(lambda x: '.csv' in x, filenames))
    return [path.join(dir, filename) for filename in f]


def readDailyReports():
    f = getCsvFilesPaths(COVID_19_DIR)
    countries = {}
    for file in sorted(f):
        with open(file) as dailyReport:
            print(file)
            dateTokens = [int(x) for x in file.split("/")[-1][:-4].split("-")]
            date = dt.date(dateTokens[2], dateTokens[0], dateTokens[1])
            entries = [DbEntry(x, date) for x in csv.DictReader(dailyReport)]
            for e in entries:
                countryName = e.country
                if countryName not in countries:
                    countries[countryName] = CountryData(countryName, populations.get(e.country), OrderedDict(),
                                                         OrderedDict(), OrderedDict())
                country = countries[countryName]
                addWithDefault(country.deathsAccPerDate, date, 0, e.deaths)
                addWithDefault(country.confirmedAccPerDate, date, 0, e.confirmed)
                addWithDefault(country.recoveredAccPerDate, date, 0, e.recovered)

    print(countries)
    return countries


def addWithDefault(dict, key, default, toAdd):
    dict[key] = dict.get(key, default) + toAdd


def mergeCountryView(db):
    res = {}
    for entry in db:
        countryName = entry.country
        if countryName not in res:
            res[countryName] = entry
        else:
            stats = res[countryName].stat
            for k, v in entry.stat.items():
                stat = stats.get(k, 0) + v
                stats[k] = stat
            res[countryName].stat = stats

    return res


def plotItaly(countries):
    deathsAccPerDate = countries[c.italy].deathsAccPerDate
    deathsPerDate = countries[c.italy].getDeathsPerDate()
    totalDeaths = countries[c.italy].getTotalDeaths()
    print(totalDeaths)

    print(deathsAccPerDate)
    print(deathsPerDate)
    plt.plot(
        list(deathsAccPerDate.keys())[:-1],
        list(deathsAccPerDate.values())[:-1],
    )
    plt.plot(
        list(deathsPerDate.keys())[:-1],
        list(deathsPerDate.values())[:-1],
    )
    plt.show()


class DbSeriesEntry:
    def __init__(self, row):
        self.country = row['Country/Region']
        self.state = row['Province/State']
        del row['Country/Region']
        del row['Lat']
        del row['Long']
        del row['Province/State']
        self.stat = OrderedDict([(parseDate(x), parseInt(row[x])) for (x) in row])


def readSeries():
    dbDeaths = mergeCountryView(readStats(COVID_19_DEATHS_FILE))
    dbConfirmed = mergeCountryView(readStats(COVID_19_CONFIRMED_FILE))
    dbRecovered = mergeCountryView(readStats(COVID_19_RECOVERED_FILE))
    countries = {}
    for countryName in dbDeaths:
        entry = dbDeaths[countryName]
    recovered = dbRecovered.get(countryName)
    if recovered:
        recovered = recovered.stat
    else:
        warn("No recovered for " + countryName)
    confirmed = dbConfirmed.get(countryName)
    if confirmed:
        confirmed = confirmed.stat
    else:
        warn("No confirmed for " + countryName)
    countries[entry.country] = CountryData(entry.country, populations.get(entry.country), entry.stat, confirmed, recovered)

    return countries


if __name__ == '__main__':
    main()
