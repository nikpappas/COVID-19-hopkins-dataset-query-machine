import csv
from core.utils import parseInt


def readCsv():
    with open('../API_SP.POP.TOTL_DS2_en_csv_v2_887275.csv') as csvfile:
        rows = csv.DictReader(csvfile)
        return {row['\ufeffCountry Name']: parseInt(row['2018']) for row in rows}


populations = readCsv()
