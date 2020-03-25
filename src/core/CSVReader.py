import csv
import datetime as dt
from collections import OrderedDict
import matplotlib.pyplot as plt
from dto.CountryData import CountryData
from population.populations import populations
from country import countries as c
from core.utils import parseInt


COVID_19_FILE = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'

def main():
    with open(COVID_19_FILE) as csvfile:
        db = [DbEntry(x) for x in csv.DictReader(csvfile)]
        coi = [
            c.greece,
            # c.italy,
            # c.spain,
            c.uk,
            # c.us
        ]
        countries = {}
        for entry in db:
            if entry.country in countries.keys():
                countries[entry.country].appendDeaths(entry.deathsAccPerDate)
            else:
                countries[entry.country] = CountryData(entry.country, populations.get(entry.country),
                                                       entry.deathsAccPerDate)

        # plotItaly(countries)

        countryData = [countries[x] for x in coi]
        for country in countryData:
            deathPerRatio = country.deathsAccPerdayRatio()
            plt.plot(
                list(deathPerRatio.keys())[30:-1],
                list(deathPerRatio.values())[30:-1],
                label=country.country
            )
        plt.title('Deaths per population', fontsize=20)
        plt.legend()
        plt.show()

        print(totalDeaths)


class DbEntry:
    def __init__(self, row):
        self.country = row['Country/Region']
        self.state = row['Province/State']
        del row['Country/Region']
        del row['Lat']
        del row['Long']
        del row['Province/State']
        self.deathsAccPerDate = OrderedDict([(parseDate(x), parseInt(row[x])) for (x) in row])


def parseDate(string):
    dateTokens = [int(x) for x in string.split("/")]
    return dt.date(int(dateTokens[2]) + 2000, int(dateTokens[0]), int(dateTokens[1]))




def getDeathsPerDateIn(db, country):
    countryData = [x for x in db if x.country == country]
    if len(countryData) is 1:
        return countryData[0].deathsAccPerDay, countryData[0].deathsPerDay, countryData[0].deathsAccPerdayRatio
    else:
        countryData = [x for x in db if x.state == country]
        return countryData[0].deathsAccPerday, countryData[0].deathsPerDay, countryData[0].deathsAccPerdayRatio



def plotItaly(countries):
    deathsAccPerDate = countries[c.italy].deathsAccPerDate
    deathsPerDate = countries[c.italy].getDeathsPerDate()
    totalDeaths = countries[c.italy].getTotalDeaths()

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


def getTotalDeaths(deathsPerDate):
    return max([x[1] for x in deathsPerDate])


if __name__ == '__main__':
    main()
