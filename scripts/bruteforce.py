import os
import sys
import json
sys.path.insert(0, '..')
import athlib

from athlib.codes import FIELD_EVENTS

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


    cleaned_series = []
    for (perf, points) in series:
        if perf and points:
            cleaned_series.append((perf, points))
    series = cleaned_series
    # binary search for the performance we need.  Somewhere between 0 and 1400 points

    # for world records
    (maxpoints, bestperf) = series[0]
    if event_code in FIELD_EVENTS:
        if performance > bestperf:
            return maxpoints
    else:
        if performance < bestperf:
            return maxpoints

    for x in range(len(series)-1): 
        (points1, perf1) = series[x]
        (points2, perf2) = series[x+1]

        if event_code in FIELD_EVENTS:
            # do something
            
            if (performance >= perf2) and (performance < perf1):
                return points2

        else:

            if (performance < perf2) and (performance >= perf1):
                return points1
    return 0



    return 0

if __name__=='__main__':
    sc = load_scores()

    print("9sec in Mens 100 =", score('M', 'OUT', '100', 9.0))    
    print("110m in Mens Javelin =", score('M', 'OUT', 'JT', 110.0))    

    print("12sec in Mens 100 =", score('M', 'OUT', '100', 12.0))    
    print("50m in Mens Javelin =", score('M', 'OUT', 'JT', 50.0))    

    print("30sec in Mens 100 =", score('M', 'OUT', '100', 30.0))    
    print("1m in Mens Javelin =", score('M', 'OUT', 'JT', 1.0))    
