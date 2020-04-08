import csv

from core.utils import parseInt


def readCsvPopulations():
    with open('../../API_SP.POP.TOTL_DS2_en_csv_v2_887275.csv') as csvfile:
        rows = csv.DictReader(csvfile)
        return {row['\ufeffCountry Name']: parseInt(row['2018']) for row in rows}


def readCsvUsStatePopulations():
    with open('../../us-populations.csv') as csvfile:
        rows = csv.DictReader(csvfile)
        return {row['State']: parseInt(row['Pop']) for row in rows}


populations = readCsvPopulations()
usStatePopulations = readCsvUsStatePopulations()
