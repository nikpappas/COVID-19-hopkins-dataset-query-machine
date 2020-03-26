def totalDeaths(db):
    return sum(x.getTotalDeaths() for x in db.values())
