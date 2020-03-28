def totalDeaths(db):
    return sum(x.getTotalDeaths() for x in db.values())


def sumTimeSeries(db, extractor):
    timeSeries = [extractor(x) for x in db.values()]
    res = timeSeries.pop()
    for timeSerie in timeSeries:
        for key in  timeSerie:
            val = res.get(key, 0) + timeSerie.get(key)
            res[key] = val

