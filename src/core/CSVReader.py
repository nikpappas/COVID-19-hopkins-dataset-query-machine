import csv
import datetime as dt
from collections import OrderedDict
import matplotlib.pyplot as plt
from dto.CountryData import CountryData
from population.populations import populations
from country import countries as c
from core.utils import parseInt

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

        # plotItaly(countries)

    countryData = [countries[x] for x in COI]
    plt.subplot(2,1,1)
    for country in countryData:
        deathsPerDateAcc = country.deathsAccPerDateRatio()
        print("Total deaths: " + country.country + " | " + str(max(deathsPerDateAcc.values())))
        plt.plot(
            list(deathsPerDateAcc.keys())[30:-1],
            list(deathsPerDateAcc.values())[30:-1],
            label=country.country + " deaths Acc"
        )
    plt.legend()
    plt.title('Deaths accumulative', fontsize=16)
    plt.subplot(2,1,2)
    for country in countryData:
        deathsPerDate = country.deathsPerDateRatio()
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


class DbEntry:
    def __init__(self, row):
        self.country = row['Country/Region']
        self.state = row['Province/State']
        del row['Country/Region']
        del row['Lat']
        del row['Long']
        del row['Province/State']
        self.stat = OrderedDict([(parseDate(x), parseInt(row[x])) for (x) in row])


def parseDate(string):
    dateTokens = [int(x) for x in string.split("/")]
    return dt.date(int(dateTokens[2]) + 2000, int(dateTokens[0]), int(dateTokens[1]))


def readStats(file):
    with open(file) as csvfile:
        return [DbEntry(x) for x in csv.DictReader(csvfile)]


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


if __name__ == '__main__':
    main()
