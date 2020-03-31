import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import country.countries as c
import core.aggregations as agg

LINESTYLES = {
    'solid': '-',
    'dashed': '--',
    'dash-dot': '-.',
    'dotted': ':'
}

axisDateFormatter = mdates.DateFormatter('%d-%m')


def plotCountry(countries, countryName):
    country = countries[countryName]
    deathsAccPerDate = country.deathsAccPerDate
    deathsPerDate = country.deathsPerDate()
    totalDeaths = country.totalDeaths()
    print(totalDeaths)
    lastDate = max(country.deathsAccPerDate.keys())
    maxDeathsPerDate = max(deathsPerDate.values())
    lastDeathsPerDate = list(deathsPerDate.values())[-1]
    print(deathsAccPerDate)
    print(deathsPerDate)
    print(maxDeathsPerDate)
    _, ax = plt.subplots()  # fig, ax

    ax.xaxis.set_major_formatter(axisDateFormatter)
    totLength = len(list(deathsAccPerDate.keys()))
    plt.plot(
        list(deathsAccPerDate.keys())[totLength-10:],
        list(deathsAccPerDate.values())[totLength-10:],
        label="Deaths Acc in " + countryName,
        marker='.'
    )
    ax.annotate('%s' % str(totalDeaths), xy=(lastDate, totalDeaths))

    plt.plot(
        list(deathsPerDate.keys())[totLength-10:],
        list(deathsPerDate.values())[totLength-10:],
        label="Deaths per day in " + countryName,
        marker='.'
    )
    maxOnDate = agg.findKeyForValue(deathsPerDate, maxDeathsPerDate)
    ax.annotate('max: %s' % str(maxDeathsPerDate), xy=(maxOnDate, maxDeathsPerDate))
    if maxDeathsPerDate is not lastDeathsPerDate:
        ax.annotate('%s' % str(lastDeathsPerDate), xy=(lastDate, lastDeathsPerDate))
    plt.legend()
    plt.show()


def plotItaly(countries):
    plotCountry(countries, c.italy)


def plotCountriesOfInterest(countries, coi):
    countryData = [countries[x] for x in coi]

    _, ax = plt.subplots()  # fig, ax

    # plt.subplot(2, 1, 1)
    for country in countryData:
        confirmedPerDateAcc = country.confirmedAccPerDate
        recoveredPerDateAcc = country.recoveredAccPerDate
        deathsPerDateAcc = country.deathsAccPerDate

        totalDeaths = max(deathsPerDateAcc.values())
        totalRecovered = max(recoveredPerDateAcc.values())
        totalConfirmed = max(confirmedPerDateAcc.values())
        onDate = max(deathsPerDateAcc.keys())
        print("Total deaths: " + country.country + " | " + str(totalDeaths))
        print("Total recovered: " + country.country + " | " + str(totalRecovered))
        print("Total confirmed: " + country.country + " | " + str(totalConfirmed))
        # ax.annotate('%s' % totalDeaths, xy=(onDate, totalDeaths))
        # plt.plot(
        #     list(deathsPerDateAcc.keys()),
        #     list(deathsPerDateAcc.values()),
        #     label=country.country + " deaths Acc"
        # )
        ax.annotate('%s' % totalConfirmed, xy=(onDate, totalConfirmed))
        plt.plot(
            list(confirmedPerDateAcc.keys()),
            list(confirmedPerDateAcc.values()),
            label=country.country + " confirmed Acc"
        )
        # ax.annotate('%s' % totalRecovered, xy=(onDate, totalRecovered))
        # plt.plot(
        #     list(recoveredPerDateAcc.keys()),
        #     list(recoveredPerDateAcc.values()),
        #     label=country.country + " recovered Acc"
        # )

    plt.legend()
    plt.title('COVID-19', fontsize=16)

    # plt.subplot(2, 1, 2)
    # countryData = [countries[x] for x in coi]
    # for country in countryData:
    #     deathsPerDate = country.confirmedPerDateRatio()
    #     print("Max  deathsperDate: " + country.country + " | " + str(max(deathsPerDate.values())))
    #     print("Last deathsperDate: " + country.country + " | " + str(list(deathsPerDate.values())[-1]))
    #     plt.plot(
    #         list(deathsPerDate.keys()),
    #         list(deathsPerDate.values()),
    #         label=country.country + " deaths"
    #     )
    # plt.legend()
    # plt.title('Deaths per day', fontsize=16)
    plt.show()




def plotWorld(countries):
    deathsPerDateAcc = agg.sumTimeSeries(countries, lambda x: x.deathsAccPerDate)
    plt.plot(
        list(deathsPerDateAcc.keys()),
        list(deathsPerDateAcc.values()),
        label="Deaths Accumulative"
    )
    confirmedPerDateAcc = agg.sumTimeSeries(countries, lambda x: x.confirmedAccPerDate)
    plt.plot(
        list(confirmedPerDateAcc.keys()),
        list(confirmedPerDateAcc.values()),
        label="Confirmed Accumulative"
    )
    recoveredPerDateAcc = agg.sumTimeSeries(countries, lambda x: x.recoveredAccPerDate)
    plt.plot(
        list(recoveredPerDateAcc.keys()),
        list(recoveredPerDateAcc.values()),
        label="Recovered Accumulative"
    )

    plt.legend()
    plt.title('COVID-19 - world stats', fontsize=16)
    plt.show()


def plotCountriesOfInterestPerPopulation(countries, coi):
    countryData = [countries[x] for x in coi]

    _, ax = plt.subplots()  # fig, ax

    for country in countryData:
        confirmedPerDateAcc = country.confirmedAccPerDateRatio()
        recoveredPerDateAcc = country.recoveredAccPerDateRatio()
        deathsPerDateAcc = country.deathsAccPerDateRatio()

        plotDeathsRatio(deathsPerDateAcc, ax, country)
        # plotConfirmedRatio(confirmedPerDateAcc, ax, country)
        # plotRecoveredRatio(recoveredPerDateAcc, ax, country)

    plt.legend()
    plt.title('COVID-19', fontsize=16)
    plt.show()


def plotConfirmedRatio(confirmedPerDateAcc, ax, country):
    onDate = max(confirmedPerDateAcc.keys())
    totalConfirmed = max(confirmedPerDateAcc.values())
    print("% confirmed: " + country.country + " | " + str(totalConfirmed))
    ax.annotate('%s' % totalConfirmed, xy=(onDate, totalConfirmed))
    plt.plot(
        list(confirmedPerDateAcc.keys()),
        list(confirmedPerDateAcc.values()),
        label=country.country + " confirmed Acc/population"
    )


def plotDeathsRatio(deathsPerDateAcc, ax, country):
    onDate = max(deathsPerDateAcc.keys())
    totalDeaths = max(deathsPerDateAcc.values())
    print("% deaths: " + country.country + " | " + str(totalDeaths))
    ax.annotate('%s' % totalDeaths, xy=(onDate, totalDeaths))
    plt.plot(
        list(deathsPerDateAcc.keys()),
        list(deathsPerDateAcc.values()),
        label=country.country + " deaths Acc/population",
        linestyle=LINESTYLES['dotted']
    )


def plotRecoveredRatio(recoveredPerDateAcc, ax, country):
    onDate = max(recoveredPerDateAcc.keys())
    totalRecovered = max(recoveredPerDateAcc.values())
    print("% recovered: " + country.country + " | " + str(totalRecovered))
    ax.annotate('%s' % totalRecovered, xy=(onDate, totalRecovered))
    plt.plot(
        list(recoveredPerDateAcc.keys()),
        list(recoveredPerDateAcc.values()),
        label=country.country + " recovered Acc/population",
        linestyle=LINESTYLES['dashed']
    )
