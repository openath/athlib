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
import csv
from collections import defaultdict, OrderedDict

import xlrd

def run():
    print("This will parse the IAAF tables and output a machine readable file")


    points_table = {}


    for (where, filename) in [
        ('OUT', 'data/iaaf_scoring_tables_2017_outdoors.xls'),
        ('IND', 'data/iaaf_scoring_tables_2017_indoor.xls')
        ]:  
        print("Reading" + filename)

        book = xlrd.open_workbook(filename)
        print("   The number of worksheets is {0}".format(book.nsheets))




        gender = 'M'  # flip it when we see a womens' event, 100-odd pages into the 
        context = "%s-%s" % (gender, where)
        points_table[context] = OrderedDict()


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
                context = "%s-%s" % (gender, where)
                points_table[context] = OrderedDict()

            points_col = headers.index('Points')
            body = matrix[1:]
            for row in body:
                t = row[points_col]
                points = t and int(t) or None
                pairs = zip(headers, row)
                for (header, value) in pairs:
                    if header not in ('', 'Points'):
                        event_code = header
                        if event_code not in points_table[context]:
                            points_table[context][event_code] = []
                        if value != '-':
                            # keep it
                            points_table[context][event_code].append((points, value))
                            if (context == 'M-OUT') and (event_code=="100m") and (points > 1390):
                                print(context, event_code, points, '==>', value)
                            datapoints += 1
                            if datapoints > 10:
                                break

        # done looping the input files

        print("    Extracted %d data points for %s" % (datapoints, context))

        print("Event codes by context:")
        for (context, info) in points_table.items():
            print("  %s:  %s" % (context, info.keys()))
        # print("    Mens events:" , points_table['M'].keys())
        # print("    Womens events:" , points_table['F'].keys())

    # outfilename = os.path.splitext(filename)[0] + '.json'
    # with open(outfilename, 'w') as outfile:
    #     json.dump(points_table, outfile)
    # print("    Saved %s" % outfilename)

    # # now write two CSV files with all event points values
    # # for this we want a sparse matrix, then we can loop over the indices 

    # spm = {}
    # for (gender, gpointsdict) in points_table.items():
    #     for (event_code, event_data) in gpointsdict.items():
    #         for (points, value) in event_data:
    #             key = (gender, event_code, points)
    #             spm[key] = value


    # for gender in 'MF':
    #     outfilename = "data/points_table_%s_%s.csv" % (gender, where)

    #     with open(outfilename, mode='w') as outfile:
    #         gpointsdict = points_table[gender]
    #         event_codes = gpointsdict.keys()
    #         header = ['Points'] + event_codes
    #         print(gender, header)
    #         writer = csv.writer(outfile)
    #         writer.writerow(header)
    #         for points in range(1400, 0, -1):
    #             row = [points]
    #             for event_code in event_codes:
    #                 key = (gender, event_code, points)
    #                 perf = spm.get(key, None)
    #                 row.append(perf)
    #             writer.writerow(row)
    #         print("Wrote %s" % outfilename)




if __name__=="__main__":
    run()