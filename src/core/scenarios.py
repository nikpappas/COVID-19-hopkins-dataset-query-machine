import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

import core.aggregations as agg
import country.countries as c
from core.plot.plotConfiguration import COLORS, LINESTYLES, styleFigureDark
from core.utils import printForCountry, printAggregates, smoothenCurve, mapToCountries

axisDateFormatter = mdates.DateFormatter('%d-%m')
axisNumberFormatter = tkr.StrMethodFormatter('{x:,.0f}')


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


def plotCountry(countries, countryName, numberOfDays=15, relative=False, pltScale='linear', granularity=1):
    countriesToPlot = mapToCountries(countries, countryName)

    fig = plt.figure()
    title = "COVID-19: Deaths"
    perPeople = 100000
    if relative:
        title = f"{title} per {perPeople} people"

    ax1, ax2 = fig.subplots(2, 1)

    ax1.set_title(title, color=COLORS['tainted-white'])
    styleFigureDark(fig, ax1)
    styleFigureDark(fig, ax2)

    ax1.set_yscale(pltScale)
    for country in countriesToPlot:
        if relative:
            deathsAccPerDate = country.deathsAccPerDateRatio(perPeople=perPeople)
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

        x, y = smoothenCurve(x, y, granularity, avg=True)

        ax1.plot(
            x,
            y,
            label="Deaths Acc in " + country.country,
            marker='.'
        )
        ax1.annotate('%02.2f' % totalDeaths, xy=(lastDate, totalDeaths), color=COLORS['white'])
        if relative:
            deathsPerDate = country.deathsPerDateRatio(perPeople=1000)
        else:
            deathsPerDate = country.deathsPerDate()
        maxDeathsPerDate = max(deathsPerDate.values())
        lastDeathsPerDate = list(deathsPerDate.values())[-1]

        # Filter dates by date not by number
        numOfDaysForAggregatsion = 7
        printAggregates(country, maxDeathsPerDate, lastDeathsPerDate, deathsPerDate, numOfDaysForAggregatsion, 'Deaths')

        x = list(deathsPerDate.keys())
        y = list(deathsPerDate.values())
        x = agg.extractLastDaysFromData(x, numberOfDays)
        y = agg.extractLastDaysFromData(y, numberOfDays)

        x, y = smoothenCurve(x, y, granularity, avg=False)

        ax2.plot(
            x,
            y,
            label="Deaths per day in " + country.country,
            marker='.'
        )
        annotateWithValues(x, y, ax2)
        # maxOnDate = agg.findKeyForValue(deathsPerDate, maxDeathsPerDate)
        # ax2.annotate('max: %02.4f' % maxDeathsPerDate, xy=(maxOnDate, maxDeathsPerDate), color=COLORS['white'])
        # if maxDeathsPerDate is not lastDeathsPerDate:
        #     ax2.annotate('%02.4f' % lastDeathsPerDate, xy=(lastDate, lastDeathsPerDate), color=COLORS['white'])

    ax1.legend()
    ax2.legend()
    plt.show()


def plotWithLockDownLine(countries, countryName, numberOfDays=15, relative=False, pltScale='linear', granularity=1,
                         lockDownLevel=None):
    ax1, ax2, plt = plotCountryCases(countries, countryName, numberOfDays, relative, pltScale, granularity,
                                     dryPlot=True)
    if lockDownLevel:
        countriesToPlot = mapToCountries(countries, countryName)
        if len(countriesToPlot):
            countriesToPlot = countriesToPlot[0]
        startDate, _ = list(countriesToPlot.confirmedPerDate().items())[0]
        endDate, _ = list(countriesToPlot.confirmedPerDate().items())[-1]
        ax2.plot([startDate, endDate], [lockDownLevel, lockDownLevel], label="lockdown")
        ax1.legend()
        ax2.legend()
        plt.show()


def annotateWithValues(x, y, ax):
    maxAggPerDate = max(y)
    # maxOnDate = agg.findKeyForValue(x, maxAggPerDate)
    maxOnDate = x[y.index(maxAggPerDate)]
    ax.annotate('max: %02.4f' % maxAggPerDate, xy=(maxOnDate, maxAggPerDate), color=COLORS['white'])
    lastAggPerDate = y[-1]
    if maxAggPerDate is not lastAggPerDate:
        ax.annotate('%02.4f' % lastAggPerDate, xy=(x[-1], lastAggPerDate), color=COLORS['white'])


def plotCountryCases(countries, countryName, numberOfDays=15, relative=False, pltScale='linear', granularity=1,
                     dryPlot=False):
    countriesToPlot = mapToCountries(countries, countryName)
    perPeople = 1000
    fig = plt.figure()
    title = "COVID-19: Cases"
    if relative:
        title = title + f" per {perPeople} people"
    ax1, ax2 = fig.subplots(2, 1)
    ax1.set_title(title, color=COLORS['tainted-white'])
    styleFigureDark(fig, ax1)
    styleFigureDark(fig, ax2)

    ax1.set_yscale(pltScale)
    for country in countriesToPlot:
        if relative:
            deathsAccPerDate = country.confirmedAccPerDateRatio(perPeople=perPeople)
        else:
            deathsAccPerDate = country.confirmedAccPerDate

        totalDeaths = max(deathsAccPerDate.values())
        printForCountry(country.country, "Total cases:", totalDeaths)
        lastDate = max(deathsAccPerDate.keys())
        # fig, ax = plt.subplots()  # fig, ax
        x = list(deathsAccPerDate.keys())
        y = list(deathsAccPerDate.values())

        x = agg.extractLastDaysFromData(x, numberOfDays)
        y = agg.extractLastDaysFromData(y, numberOfDays)

        x, y = smoothenCurve(x, y, granularity, avg=True)

        ax1.plot(
            x,
            y,
            label="Cases Acc in " + country.country,
            marker='.'
        )
        ax1.annotate('%02.4f' % totalDeaths, xy=(lastDate, totalDeaths), color=COLORS['white'])
        if relative:
            deathsPerDate = country.confirmedPerDateRatio(perPeople=1000)
        else:
            deathsPerDate = country.confirmedPerDate()
        maxDeathsPerDate = max(deathsPerDate.values())
        lastDeathsPerDate = list(deathsPerDate.values())[-1]
        # Filter dates by date not by number

        numOfDaysForAggregatsion = 7
        printAggregates(country, maxDeathsPerDate, lastDeathsPerDate, deathsPerDate, numOfDaysForAggregatsion, 'Cases')

        x = list(deathsPerDate.keys())
        y = list(deathsPerDate.values())
        x = agg.extractLastDaysFromData(x, numberOfDays)
        y = agg.extractLastDaysFromData(y, numberOfDays)

        x, y = smoothenCurve(x, y, granularity, avg=False)

        ax2.plot(
            x,
            y,
            label="Cases per day in " + country.country,
            marker='.'
        )
        annotateWithValues(x, y, ax2)

    ax1.legend()
    ax2.legend()

    if dryPlot:
        return ax1, ax2, plt

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
