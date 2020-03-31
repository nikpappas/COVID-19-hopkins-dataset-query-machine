from  core.CSVReader import CSVReader
from core import aggregations as agg
from country import countries as c
from core import scenarios as plots

COVID_19_DIR = '../../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
COVID_19_DEATHS_FILE = '../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
COVID_19_CONFIRMED_FILE = '../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
COVID_19_RECOVERED_FILE = '../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

COI = [
    # c.greece,
    c.italy,
    c.spain,
    # c.uk,
    c.us,
    c.china,
    # c.turkey,
]


def main():
    reader = CSVReader(COVID_19_CONFIRMED_FILE, COVID_19_RECOVERED_FILE, COVID_19_DEATHS_FILE, COVID_19_DIR)
    countries, series = reader.loadCountries()
    plots.plotCountry(series, c.uk)
    # plots.plotItaly(countries)
    # plots.plotCountriesOfInterest(countries, COI)
    plots.plotCountriesOfInterestPerPopulation(countries, COI)
    # plots.plotWorld(countries)
    #
    print("agg.totalDeaths(countries)", agg.totalDeaths(countries))
    print("agg.totalDeaths(series)", agg.totalDeaths(series))


if __name__ == '__main__':
    main()
