"""This parses thhe Excel extracts of the IAAF tables and writes a JSON file

Thanks to Maxim Moinat for parsing the PDF in Java and producing the Excel files.
See:
    https://github.com/MaximMoinat/ScoringTablesIAAF/

Thanks to IAAF (now World Athletics) CTO for giving permission to reproduce 
the tables at AthTech Conference 2018

"""
import os
import sys
import json
from collections import defaultdict, OrderedDict

import xlrd

def run():
    print("This will parse the IAAF tables and output a machine readable file")


    for filename in [
        'data/iaaf_scoring_tables_2017_outdoors.xls',
        'data/iaaf_scoring_tables_2017_indoor.xls'
        ]:  
        print("Reading" + filename)

        book = xlrd.open_workbook(filename)
        print("   The number of worksheets is {0}".format(book.nsheets))


        points_table = {}
        points_table['M'] = OrderedDict()
        points_table['F'] = OrderedDict()


        gender = 'M'  # flip it when we see a womens' event, 100-odd pages into the 
        datapoints = 0
        for sheetnum in range(book.nsheets):
            sheet = book.sheet_by_index(sheetnum)
            matrix = []
            for rownum in range(sheet.nrows):
                row = sheet.row_values(rownum)
                matrix.append(row)

            # loop over discarding every blank column and value
            headers = matrix[0]
            if 'Points' not in headers:
                break

            if ('100mH' in headers) or ('50m' in headers):
                gender = 'F' # half way through book we flip

            points_col = headers.index('Points')
            body = matrix[1:]
            for row in body:
                points = row[points_col]
                pairs = zip(headers, row)
                for (header, value) in pairs:
                    if header not in ('', 'Points'):
                        event_code = header
                        if event_code not in points_table[gender]:
                            points_table[gender][event_code] = []
                        if value != '-':
                            # keep it
                            points_table[gender][event_code].append((points, value))
                            datapoints += 1



        print("    Extracted %d data points" % datapoints)
        print("    Mens events:" , points_table['M'].keys())
        print("    Womens events:" , points_table['F'].keys())

        outfilename = os.path.splitext(filename)[0] + '.json'
        with open(outfilename, 'w') as outfile:
            json.dump(points_table, outfile)
        print("    Saved %s" % outfilename)







if __name__=="__main__":
    run()