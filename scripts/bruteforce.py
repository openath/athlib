import os
import sys
import json

FILES = [
    'data/iaaf_scoring_tables_2017_outdoors.json',
    'data/iaaf_scoring_tables_2017_indoor.json'
    ]

_scores = None
def load_scores():
    global _scores
    if not _scores:
        points = 0
        _scores = {}

        for filename in FILES:
            if 'outdoors' in filename:
                where = 'OUT'
            else:
                where = 'IN'
            f = open(filename, 'r')
            stuff = json.load(f)

            for gender in stuff.keys():
                level2 = stuff[gender]
                for event_code in level2.keys():

                    series = level2[event_code]
                    points += len(series)

                    if event_code.endswith('m'):
                        event_code = event_code[0:-1]


                    key = (gender, where, event_code)
                    _scores[key] = series
        print("loaded %d scores for %d distinct events" % (points, len(_scores)))
    return _scores


def score(gender, inout, event_code, performance):
    sc = load_scores()
    key = (gender, inout, event_code)
    series = sc[key]
    print("loaded series with %d data points" % len(series))

    # binary search for the performance we need.  Somewhere between 0 and 1400 points

    upper = 1400
    lower = 0
    mid = 700
    itera = 0
    while True:
        itera += 1
        print("Iteration %d:  upper=%d, lower=%d, mid=%d" % (itera, upper, lower, mid))
        mid = int((upper + lower) / 2)
        perf = series[mid]
        one_below = series[mid - 1]

        if performance > perf:
            lower = mid
        elif performance < one_below:
            upper = mid
        else: #bullseye
            return mid

        if mid == 1400:
            return 1400
        elif mid == 0:
            return 0

    return 0

if __name__=='__main__':
    sc = load_scores()

    print("10sec in Mens 100 =", score('M', 'OUT', '100', 10.0))
