import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import core.aggregations as agg
import country.countries as c
from core.utils import printForCountry
from core.plot.plotConfiguration import COLORS, styleFigureDark

axisDateFormatter = mdates.DateFormatter('%d-%m')


# axisDateFormatter = mdates.DateFormatter('')

# def plotMostHit(countries, numberOfCountries):
#     countries
#     coun
#

def plotExponential(countries, countryName):
    countriesToPlot = mapToCountries(countries, countryName)

    for country in countriesToPlot:
        bucketLength = 7

        print(country.country)
        deathsAccPerDate = list(agg.perBucketOfDays(country.deathsAccPerDateRatio(), days=bucketLength).values())
        deathsPerDate = list(agg.perBucketOfDays(country.deathsPerDateRatio(), days=bucketLength).values())
        x = deathsAccPerDate
        y = deathsPerDate
        # x = []
        # y = []
        # for i in range(len(deathsPerDate)):
        #     if deathsAccPerDate[i] > 0:
        #         x.append(deathsAccPerDate[i])
        #         y.append(deathsPerDate[i]/deathsAccPerDate[i])

        plt.plot(
            x,
            y,
            label=country.country
        )
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.show()


def plotCountry(countries, countryName, numberOfDays=15, plotPerPopulation=False, pltScale='linear', granularity=1):
    countriesToPlot = mapToCountries(countries, countryName)

    fig = plt.figure()
    title = "COVID-19: Deaths"
    if plotPerPopulation:
        title = title + " per 100K people"
    ax1, ax2 = fig.subplots(2, 1)
    ax1.set_title(title, color=COLORS['tainted-white'])
    styleFigureDark(fig, ax1)
    styleFigureDark(fig, ax2)

    ax1.set_yscale(pltScale)
    for country in countriesToPlot:
        if plotPerPopulation:
            deathsAccPerDate = country.deathsAccPerDateRatio(perPeople=100000)
        else:
            deathsAccPerDate = country.deathsAccPerDate

        totalDeaths = max(deathsAccPerDate.values())
        printForCountry(country.country, "Total deaths:", totalDeaths)
        lastDate = max(deathsAccPerDate.keys())
        # fig, ax = plt.subplots()  # fig, ax
        x = list(deathsAccPerDate.keys())
        y = list(deathsAccPerDate.values())

        x = agg.extractLastDaysFromData(x, numberOfDays)
        y = agg.extractLastDaysFromData(y, numberOfDays)

        if granularity > 1:
            x = agg.perBucketOfDaysListDates(x, days=granularity)
            y = agg.perBucketOfDaysListInt(y, days=granularity)

        ax1.plot(
            x,
            y,
            label="Deaths Acc in " + country.country,
            marker='.'
        )
        ax1.annotate('%02.4f' % totalDeaths, xy=(lastDate, totalDeaths), color=(1, 1, 1))
        if plotPerPopulation:
            deathsPerDate = country.deathsPerDateRatio(perPeople=100000)
        else:
            deathsPerDate = country.deathsPerDate()
        maxDeathsPerDate = max(deathsPerDate.values())
        lastDeathsPerDate = list(deathsPerDate.values())[-1]
        # Filter dates by date not by number
        printForCountry(country.country, "maxDeathsPerDate:", maxDeathsPerDate)
        printForCountry(country.country, "lastDeathsPerDate:", lastDeathsPerDate)
        numOfDaysForAggregatsion = 7
        last10Days = list(deathsPerDate.values())[-numOfDaysForAggregatsion:]
        l10DaysBeforeLast10DAys = list(deathsPerDate.values())[-numOfDaysForAggregatsion * 2:-numOfDaysForAggregatsion]
        deathsLast10Days = sum(last10Days)
        prevDeathsLast10Days = sum(l10DaysBeforeLast10DAys)
        printForCountry(country.country, "deathsLast10Days [" + str(numOfDaysForAggregatsion) + "]:", deathsLast10Days)
        printForCountry(country.country, "prevDeathsLast10Days [" + str(numOfDaysForAggregatsion) + "]:",
                        prevDeathsLast10Days)

        x = list(deathsPerDate.keys())
        y = list(deathsPerDate.values())
        x = agg.extractLastDaysFromData(x, numberOfDays)
        y = agg.extractLastDaysFromData(y, numberOfDays)

        if granularity > 1:
            x = agg.perBucketOfDaysListDates(x, days=granularity)
            y = agg.perBucketOfDaysListInt(y, days=granularity)

        ax2.plot(
            x,
            y,
            label="Deaths per day in " + country.country,
            marker='.'
        )
        maxOnDate = agg.findKeyForValue(deathsPerDate, maxDeathsPerDate)
        ax2.annotate('max: %02.4f' % maxDeathsPerDate, xy=(maxOnDate, maxDeathsPerDate), color=(1, 1, 1))
        if maxDeathsPerDate is not lastDeathsPerDate:
            ax2.annotate('%02.4f' % lastDeathsPerDate, xy=(lastDate, lastDeathsPerDate), color=(1, 1, 1))

    ax1.legend()
    ax2.legend()
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
        # linestyle=LINESTYLES['dotted']
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



# def plotTrendLine(x, y, ax):
#     z = np.polyfit(x, y, 1)
#     p = np.poly1d(z)
#     ax.plot(x, p(x), linestyle=LINESTYLES['dotted'])

def mapToCountries(countries, countryName):
    if isinstance(countryName, list):
        return [countries[x] for x in countryName]
    else:
        return [countries[countryName]]

