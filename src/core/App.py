from  core.CSVReader import CSVReader
from core import aggregations as agg
from country import countries as c
from country import states as s
from core import scenarios as plots

COVID_19_DIR = '../../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
COVID_19_DEATHS_FILE = '../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
COVID_19_CONFIRMED_FILE = '../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
COVID_19_RECOVERED_FILE = '../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

COI = [
    c.greece,
    c.italy,
    c.spain,
    c.uk,
    c.us,
    # c.china,
    # 'India',
    # 'Iran',
    # c.southKorea
    # 'Netherlands',
    # 'Sweden',
    # c.turkey,
]


def main():
    reader = CSVReader(COVID_19_CONFIRMED_FILE, COVID_19_RECOVERED_FILE, COVID_19_DEATHS_FILE, COVID_19_DIR)
    countries, series = reader.loadCountries()
    # countries[c.italy].deathsAccPerDate = agg.transposeDays(countries[c.italy].deathsAccPerDate, 16)
    # countries[c.spain].deathsAccPerDate = agg.transposeDays(countries[c.spain].deathsAccPerDate, 10)


    # plots.plotExponential(series, [c.spain, c.italy, c.uk, c.greece, c.china, c.france, c.us])
    c4plot = [
        c.spain,
        c.italy,
        c.uk,
        # c.germany,
        # c.us,
        # c.brazil,
        c.france,
        c.greece,
        # c.southKorea,
        # 'Kenya',
        'Malta',
        'Serbia',
        'Bulgaria',
        # 'Japan'
    ]
    plots.plotCountry(countries, c4plot, numberOfDays=260, relative=True, granularity=7)
    plots.plotCountryCases(countries, c4plot, numberOfDays=260, relative=True, granularity=7)
    # Plot greecewith lockdonw line
    plots.plotWithLockDownLine(countries, c.greece, numberOfDays=160, relative=False, granularity=1, lockDownLevel=130)
    # Plot uk with lockdonw line
    plots.plotWithLockDownLine(countries, c.uk, numberOfDays=160, relative=False, granularity=1, lockDownLevel=6650)
    # plots.plotCountriesOfInterest(countries, [c.spain, c.italy, c.uk, c.france, c.germany, c.us, c.greece])
    # plots.plotCountry(countries, COI, numberOfDays=15, plotPerPopulation=False)
    # plots.plotCountry(countries, COI, numberOfDays=15, plotPerPopulation=False, pltScale='log')
    # plots.plotItaly(countries)
    # plots.plotCountriesOfInterest(countries, countries.keys())
    # plots.plotCountriesOfInterest(countries, COI)
    # plots.plotCountriesOfInterestPerPopulation(countries, COI)

    # plots.plotWorld(countries)
    #
    print("agg.totalDeaths(countries)", agg.totalDeaths(countries))
    print("agg.totalDeaths(series)", agg.totalDeaths(series))



if __name__ == '__main__':
    main()
