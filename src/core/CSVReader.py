import csv
import datetime as dt
from collections import OrderedDict

from core.utils import parseInt, parseDate, getCsvFilesPaths, addWithDefault
from country import countries as c
from dto.CountryData import CountryData
from population.populations import populations, usStatePopulations


class CSVReader:
    def __init__(self, confirmedTS, recoveredTS, deathsTS, dailyReportDir):
        self.confirmedTS = confirmedTS
        self.recoveredTS = recoveredTS
        self.deathsTS = deathsTS
        self.dailyReportsDir = dailyReportDir

    def loadCountries(self):
        countries = self.readDailyReports()
        countriesSeries = self.readSeries()
        return countries, countriesSeries

    def readDailyReports(self):
        countrySubstitutions = {
            'Mainland China': c.china,
            ' Azerbaijan': 'Azerbaijan'
        }

        f = getCsvFilesPaths(self.dailyReportsDir)
        countries = {}
        for file in sorted(f):
            with open(file) as dailyReport:
                dateTokens = [int(x) for x in file.split("/")[-1][:-4].split("-")]
                date = dt.date(dateTokens[2], dateTokens[0], dateTokens[1])
                entries = [DbEntry(x, date) for x in csv.DictReader(dailyReport)]
                for e in entries:
                    countryName = countrySubstitutions.get(e.country, e.country)

                    if countryName not in countries:
                        countries[countryName] = CountryData(countryName, populations.get(countryName), OrderedDict(),
                                                             OrderedDict(), OrderedDict())
                    country = countries[countryName]
                    addWithDefault(country.deathsAccPerDate, date, 0, e.deaths)
                    addWithDefault(country.confirmedAccPerDate, date, 0, e.confirmed)
                    addWithDefault(country.recoveredAccPerDate, date, 0, e.recovered)
                    if e.state:
                        stateKey = countryName + ':' + e.state
                        if stateKey not in countries:
                            countries[stateKey] = CountryData(stateKey, usStatePopulations.get(e.state),
                                                                 OrderedDict(), OrderedDict(), OrderedDict())
                        state = countries[stateKey]
                        addWithDefault(state.deathsAccPerDate, date, 0, e.deaths)
                        addWithDefault(state.confirmedAccPerDate, date, 0, e.confirmed)
                        addWithDefault(state.recoveredAccPerDate, date, 0, e.recovered)

        return countries

    def readSeries(self):
        dbConfirmed = mergeCountryView(readStats(self.confirmedTS))
        dbRecovered = mergeCountryView(readStats(self.recoveredTS))
        dbDeaths = mergeCountryView(readStats(self.deathsTS))
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
            countries[entry.country] = CountryData(entry.country, populations.get(entry.country), entry.stat, confirmed,
                                                   recovered)

        return countries


def warn(s):
    print('WARN: ' + str(s))


class DbEntry:
    def __init__(self, row, date):
        self.country = row.get('Country/Region', row.get('Country_Region'))
        self.state = row.get('Province/State', row.get('Province_State'))
        self.deaths = parseInt(row['Deaths'])
        self.confirmed = parseInt(row['Confirmed'])
        self.recovered = parseInt(row['Recovered'])
        self.date = date


def readStats(file):
    with open(file) as csvfile:
        return [DbSeriesEntry(x) for x in csv.DictReader(csvfile)]


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


class DbSeriesEntry:
    def __init__(self, row):
        self.country = row['Country/Region']
        self.state = row.get('Province/State', row.get('\ufeffProvince/State'))
        del row['Country/Region']
        del row['Lat']
        del row['Long']
        try:
            del row['Province/State']
        except:
            try:
                del row['\ufeffProvince/State']
            except:
                print('Could not delete Province/State for: ' + str(row))
        self.stat = OrderedDict([(parseDate(x), parseInt(row[x])) for (x) in row])
