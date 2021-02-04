import os
import sys
import xlrd

def run():
    print("This will parse the IAAF tables and output a machine readable file")


    for filename in [
        'data/iaaf_scoring_tables_2017_indoor.xls',
        'data/iaaf_scoring_tables_2017_outdoors.xls'
        ]:  
        print("Reading" + filename)

        book = xlrd.open_workbook(filename)
        print("   The number of worksheets is {0}".format(book.nsheets))


        pointstable = {}

        for sheetnum in range(book.nsheets):
            pass


if __name__=="__main__":
    run()