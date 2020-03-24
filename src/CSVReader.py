import csv
import datetime as dt
import matplotlib.pyplot as plt
from population.populations import populations


def main():
    with open('../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv') as csvfile:
        db = [DbEntry(x) for x in csv.DictReader(csvfile)]

        deathsAccPerDate, deathsPerDate, _ = getDeathsPerDateIn(db, 'Italy')
        totalDeaths = getTotalDeaths(deathsPerDate)
        print(deathsAccPerDate)
        print(deathsPerDate)
        # plt.plot(
        #     [x[0] for x in deathsAccPerDate][:-1],
        #     [x[1] for x in deathsAccPerDate][:-1],
        # )
        # plt.plot(
        #     [x[0] for x in deathsPerDate][:-1],
        #     [x[1] for x in deathsPerDate][:-1],
        # )

        deathsPerRatio = []
        for country in populations.keys():
            _, _, ratios = getDeathsPerDateIn(db, country)
            deathsPerRatio.append((country, ratios))

        # deathsPerRatio = [(x.country,x.deathsAccPerdayRatio) for x in db if x.country in populations.keys()]
        for deathPerRatio in deathsPerRatio:
            plt.plot(
                [x[0] for x in deathPerRatio[1]][:-1],
                [x[1] for x in deathPerRatio[1]][:-1],
                label=deathPerRatio[0]
            )
        plt.legend()
        plt.show()

        print(totalDeaths)


def getPerDay(deathsAccPerday):
    res = []
    for i in range(len(deathsAccPerday)):
        if i is 0:
            res.append(deathsAccPerday[i])
        else:
            res.append((deathsAccPerday[i][0], deathsAccPerday[i][1] - deathsAccPerday[i - 1][1]))
    return res


class DbEntry:
    def __init__(self, row):
        self.country = row['Country/Region']
        self.state = row['Province/State']
        del row['Country/Region']
        del row['Lat']
        del row['Long']
        del row['Province/State']
        self.deathsAccPerday = [(parseDate(x), parseInt(row[x])) for (x) in row]
        self.deathsPerDay = getPerDay(self.deathsAccPerday)
        if self.country in populations:
            self.deathsAccPerdayRatio = [(k, v / populations[self.country]) for k, v in self.deathsAccPerday]


def parseDate(string):
    dateTokens = [int(x) for x in string.split("/")]
    return dt.date(int(dateTokens[2]) + 2000, int(dateTokens[0]), int(dateTokens[1]))


def parseInt(string):
    try:
        return int(string)
    except ValueError:
        return 0


def getDeathsPerDateIn(db, country):
    countryData = [x for x in db if x.country == country]
    if len(countryData) is 1:
        return countryData[0].deathsAccPerday, countryData[0].deathsPerDay, countryData[0].deathsAccPerdayRatio
    else:
        countryData = [x for x in db if x.state == country]
        return countryData[0].deathsAccPerday, countryData[0].deathsPerDay, countryData[0].deathsAccPerdayRatio


def getTotalDeaths(deathsPerDate):
    return max([x[1] for x in deathsPerDate])


def getDeathsPerDate(deathsPerDate):
    return max([x[1] for x in deathsPerDate])


if __name__ == '__main__':
    main()
