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


    for (where, filename) in [
        ('outdoors', 'data/iaaf_scoring_tables_2017_outdoors.xls'),
        ('indoor', 'data/iaaf_scoring_tables_2017_indoor.xls')
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
                t = row[points_col]
                points = t and int(t) or None
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


        # sanity check, should go up to 1400ish and down near 1
        maxpoints = minpoints = 700 # midrange
        for gender in 'MF':
            p = points_table[gender]
            for (event_code, stuff) in p.items():
                for ((points, value)) in stuff:
                    if points and (points > maxpoints):
                        maxpoints = points
                    if points and (points < minpoints):
                        minpoints = points

        print("    Extracted %d data points - from %d down to %d" % (datapoints, maxpoints, minpoints))
        # print("    Mens events:" , points_table['M'].keys())
        # print("    Womens events:" , points_table['F'].keys())

        outfilename = os.path.splitext(filename)[0] + '.json'
        with open(outfilename, 'w') as outfile:
            json.dump(points_table, outfile)
        print("    Saved %s" % outfilename)

        # now write two CSV files with all event points values
        # for this we want a sparse matrix, then we can loop over the indices 

        spm = {}
        for (gender, gpointsdict) in points_table.items():
            for (event_code, event_data) in gpointsdict.items():
                for (points, value) in event_data:
                    key = (gender, event_code, points)
                    spm[key] = value


        for gender in 'MF':
            outfilename = "data/points_table_%s_%s.csv" % (gender, where)

            with open(outfilename, mode='w') as outfile:
                gpointsdict = points_table[gender]
                event_codes = gpointsdict.keys()
                header = ['Points'] + event_codes
                print(gender, header)
                writer = csv.writer(outfile)
                writer.writerow(header)
                for points in range(1400, 0, -1):
                    row = [points]
                    for event_code in event_codes:
                        key = (gender, event_code, points)
                        perf = spm.get(key, None)
                        row.append(perf)
                    writer.writerow(row)
                print("Wrote %s" % outfilename)




if __name__=="__main__":
    run()